from __future__ import annotations

import hmac
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
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
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    nombre_completo VARCHAR(255),
    rol VARCHAR(50) NOT NULL DEFAULT 'consultor',
    activo BOOLEAN NOT NULL DEFAULT true,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    bloqueado_hasta TIMESTAMPTZ,
    ultimo_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
ALTER TABLE usuario DROP CONSTRAINT IF EXISTS usuario_estado_ck;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS apellidos TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS rol_principal TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS estado TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS observaciones_internas TEXT;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS fecha_alta TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS ultimo_acceso TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS username VARCHAR(100);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre_completo VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS rol VARCHAR(50);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS activo BOOLEAN;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS bloqueado_hasta TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS ultimo_login TIMESTAMP;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW();
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW();
ALTER TABLE usuario DROP COLUMN IF EXISTS invitacion_pendiente;
ALTER TABLE usuario ALTER COLUMN nombre SET DEFAULT 'Superadministrador';
ALTER TABLE usuario ALTER COLUMN apellidos SET DEFAULT 'Licican';
ALTER TABLE usuario ALTER COLUMN email SET DEFAULT '';
ALTER TABLE usuario ALTER COLUMN rol_principal SET DEFAULT 'administrador';
ALTER TABLE usuario ALTER COLUMN estado SET DEFAULT 'deshabilitado';
ALTER TABLE usuario ALTER COLUMN observaciones_internas SET DEFAULT '';
ALTER TABLE usuario ALTER COLUMN fecha_alta SET DEFAULT NOW();
ALTER TABLE usuario ALTER COLUMN rol SET DEFAULT 'consultor';
ALTER TABLE usuario ALTER COLUMN activo SET DEFAULT true;
ALTER TABLE usuario ALTER COLUMN failed_login_attempts SET DEFAULT 0;
UPDATE usuario
SET estado = CASE
        WHEN estado IN ('activo', 'deshabilitado', 'bloqueado') THEN estado
        ELSE 'deshabilitado'
    END,
    activo = CASE
        WHEN COALESCE(NULLIF(estado, ''), 'deshabilitado') = 'activo' THEN TRUE
        ELSE FALSE
    END,
    failed_login_attempts = COALESCE(failed_login_attempts, 0),
    bloqueado_hasta = bloqueado_hasta
WHERE TRUE;
ALTER TABLE usuario ADD CONSTRAINT usuario_estado_ck CHECK (estado IN ('activo', 'deshabilitado', 'bloqueado'));
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
   OR email = %s
ORDER BY CASE WHEN username = %s THEN 0 ELSE 1 END
LIMIT 1
"""

AUTH_USER_SELECT_BY_USERNAME_SQL = """
SELECT *
FROM usuario
WHERE username = %s
LIMIT 1
"""

AUTH_USER_SELECT_SUPERADMIN_SQL = """
SELECT *
FROM usuario
WHERE rol_principal = %s
   OR rol = %s
ORDER BY
    CASE WHEN username = %s THEN 0 ELSE 1 END,
    updated_at DESC,
    fecha_alta DESC,
    id
"""

AUTH_USER_LAST_LOGIN_SQL = """
UPDATE usuario
SET ultimo_login = %s,
    ultimo_acceso = %s,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_RESET_LOGIN_STATE_SQL = """
UPDATE usuario
SET estado = 'activo',
    activo = TRUE,
    failed_login_attempts = 0,
    bloqueado_hasta = NULL,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_RECORD_FAILED_LOGIN_SQL = """
UPDATE usuario
SET estado = %s,
    activo = %s,
    failed_login_attempts = %s,
    bloqueado_hasta = %s,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_RECORD_SUCCESSFUL_LOGIN_SQL = """
UPDATE usuario
SET estado = 'activo',
    activo = TRUE,
    failed_login_attempts = 0,
    bloqueado_hasta = NULL,
    ultimo_login = %s,
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
    username,
    password_hash,
    nombre_completo,
    rol,
    activo,
    failed_login_attempts,
    bloqueado_hasta,
    ultimo_login,
    created_at,
    updated_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    username = %s,
    password_hash = %s,
    nombre_completo = %s,
    rol = %s,
    activo = %s,
    failed_login_attempts = %s,
    bloqueado_hasta = %s,
    ultimo_login = %s,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_DELETE_SQL = """
DELETE FROM usuario
WHERE id = %s
"""

AUTH_USER_CLEAR_USERNAME_SQL = """
UPDATE usuario
SET username = NULL,
    updated_at = %s
WHERE id = %s
"""

AUTH_USER_DEACTIVATE_SQL = """
UPDATE usuario
SET estado = 'deshabilitado',
    activo = FALSE,
    failed_login_attempts = 0,
    bloqueado_hasta = NULL,
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


def _now_utc() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None, microsecond=0)


def _as_naive_utc(value: object | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(microsecond=0)
        return value.astimezone(UTC).replace(tzinfo=None, microsecond=0)
    cleaned = str(value).strip().replace("Z", "+00:00")
    if not cleaned:
        return None
    parsed = datetime.fromisoformat(cleaned)
    if parsed.tzinfo is None:
        return parsed.replace(microsecond=0)
    return parsed.astimezone(UTC).replace(tzinfo=None, microsecond=0)


def _normalize_status(value: object | None) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in {"activo", "deshabilitado", "bloqueado"} else "deshabilitado"


def _user_blocked_until(row: dict[str, object]) -> datetime | None:
    return _as_naive_utc(row.get("bloqueado_hasta"))


def _failed_attempts(row: dict[str, object]) -> int:
    try:
        return max(0, int(row.get("failed_login_attempts") or 0))
    except (TypeError, ValueError):
        return 0


def _block_until(now: datetime, settings: AuthSettings) -> datetime:
    return now + timedelta(minutes=settings.login_lock_minutes)


def _is_superadmin_row(row: dict[str, object]) -> bool:
    role_principal = str(row.get("rol_principal") or "").strip().lower()
    role = str(row.get("rol") or "").strip().lower()
    return role_principal == "superadmin" or role == "superadmin"


def _mark_successful_login(cursor, row_id: object, now: datetime) -> None:
    cursor.execute(
        AUTH_USER_RECORD_SUCCESSFUL_LOGIN_SQL,
        (
            now,
            now,
            now,
            row_id,
        ),
    )


def _unlock_expired_user(cursor, row_id: object, now: datetime) -> None:
    cursor.execute(
        AUTH_USER_RESET_LOGIN_STATE_SQL,
        (
            now,
            row_id,
        ),
    )


def _record_failed_login(cursor, row: dict[str, object], now: datetime, settings: AuthSettings) -> None:
    if _is_superadmin_row(row):
        cursor.execute(
            AUTH_USER_RECORD_FAILED_LOGIN_SQL,
            (
                "activo",
                True,
                0,
                None,
                now,
                row["id"],
            ),
        )
        return
    failed_attempts = _failed_attempts(row) + 1
    if failed_attempts >= settings.login_max_failed_attempts:
        cursor.execute(
            AUTH_USER_RECORD_FAILED_LOGIN_SQL,
            (
                "bloqueado",
                False,
                failed_attempts,
                _block_until(now, settings),
                now,
                row["id"],
            ),
        )
        return

    current_status = _normalize_status(row.get("estado"))
    if current_status == "bloqueado":
        current_status = "activo"
    cursor.execute(
        AUTH_USER_RECORD_FAILED_LOGIN_SQL,
        (
            current_status if current_status in {"activo", "deshabilitado"} else "activo",
            current_status == "activo",
            failed_attempts,
            _user_blocked_until(row),
            now,
            row["id"],
        ),
    )


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
                cursor.execute(AUTH_USER_SELECT_SQL, (normalized_username, normalized_username, normalized_username))
                row = cursor.fetchone()
                if row is None:
                    raise AuthenticationError("Usuario o contraseña incorrectos.")
                current = _now_utc()
                state = _normalize_status(row.get("estado"))
                blocked_until = _user_blocked_until(row)
                if _is_superadmin_row(row) and state == "bloqueado":
                    _unlock_expired_user(cursor, row["id"], current)
                    state = "activo"
                    row["estado"] = "activo"
                    row["failed_login_attempts"] = 0
                    row["bloqueado_hasta"] = None
                if state == "bloqueado":
                    if blocked_until is None:
                        blocked_until = _block_until(current, settings)
                        cursor.execute(
                            AUTH_USER_RECORD_FAILED_LOGIN_SQL,
                            (
                                "bloqueado",
                                False,
                                max(_failed_attempts(row), settings.login_max_failed_attempts),
                                blocked_until,
                                current,
                                row["id"],
                            ),
                        )
                        raise AuthenticationError(
                            f"Usuario bloqueado temporalmente. Espere {settings.login_lock_minutes} minuto(s) antes de volver a intentarlo.",
                            code="locked_user",
                        )
                    if blocked_until > current:
                        raise AuthenticationError(
                            f"Usuario bloqueado temporalmente. Espere {settings.login_lock_minutes} minuto(s) antes de volver a intentarlo.",
                            code="locked_user",
                        )
                    _unlock_expired_user(cursor, row["id"], current)
                    state = "activo"
                    row["estado"] = "activo"
                    row["failed_login_attempts"] = 0
                    row["bloqueado_hasta"] = None
                if state == "deshabilitado":
                    raise AuthenticationError("Usuario deshabilitado. Contacte al administrador.", code="inactive_user")
                password_hash = str(row.get("password_hash") or "")
                if not password_hash or not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
                    _record_failed_login(cursor, row, current, settings)
                    raise AuthenticationError("Usuario o contraseña incorrectos.")
                _mark_successful_login(cursor, row["id"], current)
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
    superadmin_name = settings.login_superadmin_name.strip()
    if not superadmin_name:
        return None
    aliases = [superadmin_name]
    email_alias = _superadmin_email(superadmin_name)
    if email_alias not in aliases:
        aliases.append(email_alias)
    if not any(alias and hmac.compare_digest(username, alias) for alias in aliases):
        return None
    if not hmac.compare_digest(password, settings.login_superadmin_pass):
        raise AuthenticationError("Usuario o contraseña incorrectos.")
    return AuthenticatedUser(
        username=settings.login_superadmin_name,
        rol="superadmin",
        nombre_completo="",
        is_superadmin=True,
    )


def synchronize_superadmin_account(settings: AuthSettings) -> None:
    superadmin_name = settings.login_superadmin_name.strip()
    if not superadmin_name:
        return

    current = datetime.now(UTC).replace(tzinfo=None, microsecond=0)
    superadmin_email = _superadmin_email(superadmin_name)
    try:
        with psycopg2.connect(resolve_database_url()) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(AUTH_USER_BOOTSTRAP_SQL)
                cursor.execute(AUTH_USER_SELECT_SUPERADMIN_SQL, ("superadmin", "superadmin", superadmin_name))
                superadmin_rows = list(cursor.fetchall())
                if settings.login_superadmin_enabled:
                    password_hash = bcrypt.hashpw(
                        settings.login_superadmin_pass.encode("utf-8"),
                        bcrypt.gensalt(),
                    ).decode("utf-8")
                    if not superadmin_rows:
                        cursor.execute(AUTH_USER_SELECT_BY_USERNAME_SQL, (superadmin_name,))
                        conflicting_user = cursor.fetchone()
                        if conflicting_user is not None:
                            cursor.execute(
                                AUTH_USER_CLEAR_USERNAME_SQL,
                                (
                                    current,
                                    conflicting_user["id"],
                                ),
                            )
                        cursor.execute(
                            AUTH_USER_INSERT_SQL,
                            (
                                superadmin_name,
                                _superadmin_display_name(),
                                _superadmin_surname(),
                                superadmin_email,
                                "superadmin",
                                "activo",
                                _superadmin_observations(),
                                current,
                                None,
                                superadmin_name,
                                password_hash,
                                f"{_superadmin_display_name()} {_superadmin_surname()}".strip(),
                                "superadmin",
                                True,
                                0,
                                None,
                                None,
                                current,
                                current,
                            ),
                        )
                    else:
                        canonical = superadmin_rows[0]
                        canonical_id = canonical["id"]
                        for duplicate in superadmin_rows[1:]:
                            cursor.execute(AUTH_USER_DELETE_SQL, (duplicate["id"],))
                        cursor.execute(AUTH_USER_SELECT_BY_USERNAME_SQL, (superadmin_name,))
                        conflicting_user = cursor.fetchone()
                        if conflicting_user is not None and str(conflicting_user["id"]) != str(canonical_id):
                            conflict_is_superadmin = any(str(row["id"]) == str(conflicting_user["id"]) for row in superadmin_rows)
                            if not conflict_is_superadmin:
                                cursor.execute(
                                    AUTH_USER_CLEAR_USERNAME_SQL,
                                    (
                                        current,
                                        conflicting_user["id"],
                                    ),
                                )
                        cursor.execute(
                            AUTH_USER_UPDATE_SUPERADMIN_SQL,
                            (
                                _superadmin_display_name(),
                                _superadmin_surname(),
                                superadmin_email,
                                "superadmin",
                                "activo",
                                _superadmin_observations(),
                                canonical.get("fecha_alta") or current,
                                canonical.get("ultimo_acceso"),
                                superadmin_name,
                                password_hash,
                                f"{_superadmin_display_name()} {_superadmin_surname()}".strip(),
                                "superadmin",
                                True,
                                0,
                                None,
                                canonical.get("ultimo_login"),
                                current,
                                canonical_id,
                            ),
                        )
                    return

                if superadmin_rows:
                    canonical = superadmin_rows[0]
                    for duplicate in superadmin_rows[1:]:
                        cursor.execute(AUTH_USER_DELETE_SQL, (duplicate["id"],))
                    cursor.execute(AUTH_USER_DEACTIVATE_SQL, (current, canonical["id"]))
    except psycopg2.Error as exc:
        LOGGER.debug("No se pudo sincronizar el usuario superadmin en PostgreSQL.")
        raise AuthenticationError("No se pudo validar la autenticacion.", code="database_error") from exc


def _superadmin_display_name() -> str:
    return "Superadministrador"


def _superadmin_surname() -> str:
    return "Licican"


def _superadmin_observations() -> str:
    return "Cuenta superadmin sincronizada automaticamente."


def _superadmin_email(username: str) -> str:
    return "superadmin@licitan.local"
