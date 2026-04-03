from __future__ import annotations

import hmac
from dataclasses import dataclass
from datetime import UTC, datetime
import logging

import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor

from licican.auth.config import AuthSettings
from licican.config import resolve_database_url

LOGGER = logging.getLogger(__name__)

AUTH_USER_BOOTSTRAP_SQL = """
CREATE TABLE IF NOT EXISTS usuario (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    rol_principal TEXT NOT NULL,
    estado TEXT NOT NULL,
    observaciones_internas TEXT NOT NULL DEFAULT '',
    fecha_alta TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ultimo_acceso TIMESTAMPTZ,
    invitacion_pendiente BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    nombre_completo VARCHAR(255),
    rol VARCHAR(50) NOT NULL DEFAULT 'consultor',
    activo BOOLEAN NOT NULL DEFAULT true,
    ultimo_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS apellidos TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS rol_principal TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS estado TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS observaciones_internas TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS fecha_alta TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS ultimo_acceso TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS invitacion_pendiente BOOLEAN;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS username VARCHAR(100);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre_completo VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS rol VARCHAR(50);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS activo BOOLEAN;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS ultimo_login TIMESTAMP;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW();
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW();
ALTER TABLE usuario ALTER COLUMN nombre SET DEFAULT 'Superadministrador';
ALTER TABLE usuario ALTER COLUMN apellidos SET DEFAULT 'Licican';
ALTER TABLE usuario ALTER COLUMN email SET DEFAULT '';
ALTER TABLE usuario ALTER COLUMN rol_principal SET DEFAULT 'administrador';
ALTER TABLE usuario ALTER COLUMN estado SET DEFAULT 'inactivo';
ALTER TABLE usuario ALTER COLUMN observaciones_internas SET DEFAULT '';
ALTER TABLE usuario ALTER COLUMN fecha_alta SET DEFAULT NOW();
ALTER TABLE usuario ALTER COLUMN invitacion_pendiente SET DEFAULT FALSE;
ALTER TABLE usuario ALTER COLUMN rol SET DEFAULT 'consultor';
ALTER TABLE usuario ALTER COLUMN activo SET DEFAULT true;
UPDATE usuario
SET rol = COALESCE(NULLIF(rol, ''), 'consultor'),
    activo = COALESCE(activo, true)
WHERE rol IS NULL OR activo IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_usuario_auth_username ON usuario (username) WHERE username IS NOT NULL;
"""

AUTH_USER_SELECT_SQL = """
SELECT *
FROM usuario
WHERE username = %s
LIMIT 1
"""

AUTH_USER_LAST_LOGIN_SQL = """
UPDATE usuario
SET ultimo_login = %s,
    ultimo_acceso = %s,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_INSERT_SQL = """
INSERT INTO usuario (
    id,
    nombre,
    apellidos,
    email,
    rol_principal,
    estado,
    observaciones_internas,
    fecha_alta,
    ultimo_acceso,
    invitacion_pendiente,
    username,
    password_hash,
    nombre_completo,
    rol,
    activo,
    ultimo_login,
    created_at,
    updated_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

AUTH_USER_UPDATE_SUPERADMIN_SQL = """
UPDATE usuario
SET nombre = %s,
    apellidos = %s,
    email = %s,
    rol_principal = %s,
    estado = %s,
    observaciones_internas = %s,
    fecha_alta = %s,
    ultimo_acceso = %s,
    invitacion_pendiente = %s,
    username = %s,
    password_hash = %s,
    nombre_completo = %s,
    rol = %s,
    activo = %s,
    ultimo_login = %s,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_DEACTIVATE_SQL = """
UPDATE usuario
SET estado = 'inactivo',
    activo = FALSE,
    invitacion_pendiente = FALSE,
    updated_at = %s
WHERE id = %s
"""


@dataclass(frozen=True)
class AuthenticatedUser:
    username: str
    rol: str
    nombre_completo: str
    is_superadmin: bool = False


class AuthenticationError(RuntimeError):
    def __init__(self, message: str, *, code: str = "invalid_credentials") -> None:
        super().__init__(message)
        self.code = code


def authenticate_user(username: str, password: str, settings: AuthSettings) -> AuthenticatedUser:
    normalized_username = username.strip()
    if not normalized_username or not password:
        raise AuthenticationError("Usuario o contraseña incorrectos.")

    superadmin_user = _authenticate_superadmin(normalized_username, password, settings)
    if superadmin_user is not None:
        try:
            synchronize_superadmin_account(settings)
        except AuthenticationError:
            LOGGER.warning("No se pudo sincronizar el superadmin durante el inicio de sesion.")
        return superadmin_user

    synchronize_superadmin_account(settings)

    try:
        with psycopg2.connect(resolve_database_url()) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(AUTH_USER_BOOTSTRAP_SQL)
                cursor.execute(AUTH_USER_SELECT_SQL, (normalized_username,))
                row = cursor.fetchone()
                if row is None:
                    raise AuthenticationError("Usuario o contraseña incorrectos.")
                if not bool(row.get("activo")):
                    raise AuthenticationError("Usuario desactivado. Contacte al administrador.", code="inactive_user")
                password_hash = str(row.get("password_hash") or "")
                if not password_hash or not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
                    raise AuthenticationError("Usuario o contraseña incorrectos.")
                current = datetime.now(UTC).replace(tzinfo=None, microsecond=0)
                cursor.execute(AUTH_USER_LAST_LOGIN_SQL, (current, current, current, row["id"]))
                return AuthenticatedUser(
                    username=str(row["username"]),
                    rol=str(row.get("rol") or "consultor"),
                    nombre_completo=str(row.get("nombre_completo") or row["username"]),
                )
    except AuthenticationError:
        raise
    except psycopg2.Error as exc:
        raise AuthenticationError("No se pudo validar la autenticacion.", code="database_error") from exc


def _authenticate_superadmin(username: str, password: str, settings: AuthSettings) -> AuthenticatedUser | None:
    if not settings.login_superadmin_enabled:
        return None
    if not hmac.compare_digest(username, settings.login_superadmin_name):
        return None
    if not hmac.compare_digest(password, settings.login_superadmin_pass):
        raise AuthenticationError("Usuario o contraseña incorrectos.")
    return AuthenticatedUser(
        username=settings.login_superadmin_name,
        rol="administrador",
        nombre_completo="Superadministrador",
        is_superadmin=True,
    )


def synchronize_superadmin_account(settings: AuthSettings) -> None:
    superadmin_name = settings.login_superadmin_name.strip()
    if not superadmin_name:
        return

    current = datetime.now(UTC).replace(tzinfo=None, microsecond=0)
    superadmin_id = superadmin_name
    superadmin_email = _superadmin_email(superadmin_name)
    try:
        with psycopg2.connect(resolve_database_url()) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(AUTH_USER_BOOTSTRAP_SQL)
                cursor.execute(AUTH_USER_SELECT_SQL, (superadmin_name,))
                existing = cursor.fetchone()
                if settings.login_superadmin_enabled:
                    password_hash = bcrypt.hashpw(
                        settings.login_superadmin_pass.encode("utf-8"),
                        bcrypt.gensalt(),
                    ).decode("utf-8")
                    if existing is None:
                        cursor.execute(
                            AUTH_USER_INSERT_SQL,
                            (
                                superadmin_id,
                                _superadmin_display_name(),
                                _superadmin_surname(),
                                superadmin_email,
                                "administrador",
                                "activo",
                                _superadmin_observations(),
                                current,
                                None,
                                False,
                                superadmin_name,
                                password_hash,
                                "Superadministrador",
                                "administrador",
                                True,
                                None,
                                current,
                                current,
                            ),
                        )
                    else:
                        cursor.execute(
                            AUTH_USER_UPDATE_SUPERADMIN_SQL,
                            (
                                _superadmin_display_name(),
                                _superadmin_surname(),
                                superadmin_email,
                                "administrador",
                                "activo",
                                _superadmin_observations(),
                                existing.get("fecha_alta") or current,
                                existing.get("ultimo_acceso"),
                                False,
                                superadmin_name,
                                password_hash,
                                "Superadministrador",
                                "administrador",
                                True,
                                existing.get("ultimo_login"),
                                current,
                                existing["id"],
                            ),
                        )
                    return

                if existing is not None:
                    cursor.execute(AUTH_USER_DEACTIVATE_SQL, (current, existing["id"]))
    except psycopg2.Error as exc:
        LOGGER.warning("No se pudo sincronizar el usuario superadmin en PostgreSQL.")
        raise AuthenticationError("No se pudo validar la autenticacion.", code="database_error") from exc


def _superadmin_display_name() -> str:
    return "Superadministrador"


def _superadmin_surname() -> str:
    return "Licican"


def _superadmin_observations() -> str:
    return "Cuenta superadmin sincronizada automaticamente."


def _superadmin_email(username: str) -> str:
    return "superadmin@licitan.local"
