from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor

from licican.auth.config import get_auth_settings
from licican.config import resolve_database_url


DEFAULT_REFERENCE = "PB-016 - HU-16 - CU-16 - Gestion administrativa de usuarios"
USER_STATUSES = ("activo", "deshabilitado", "bloqueado")
USER_ROLES = (
    "administrador",
    "superadmin",
    "manager",
    "colaborador",
    "invitado",
)
USERS_SELECT_SQL = """
SELECT
    id,
    nombre,
    apellidos,
    email,
    rol_principal,
    estado,
    fecha_alta,
    ultimo_acceso,
    failed_login_attempts,
    bloqueado_hasta,
    username,
    password_hash
FROM usuario
ORDER BY apellidos, nombre, email, id
"""

USER_HISTORY_SELECT_SQL = """
SELECT
    usuario_id,
    accion,
    fecha,
    detalle
FROM usuario_historial
ORDER BY usuario_id, fecha, id
"""

USER_INSERT_SQL = """
INSERT INTO usuario (
    id,
    nombre,
    apellidos,
    email,
    rol_principal,
    estado,
    fecha_alta,
    ultimo_acceso,
    failed_login_attempts,
    bloqueado_hasta,
    username,
    password_hash,
    nombre_completo,
    rol,
    activo,
    updated_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

USER_UPDATE_SQL = """
UPDATE usuario
SET nombre = %s,
    apellidos = %s,
    email = %s,
    rol_principal = %s,
    estado = %s,
    ultimo_acceso = %s,
    failed_login_attempts = %s,
    bloqueado_hasta = %s,
    username = %s,
    password_hash = %s,
    nombre_completo = %s,
    rol = %s,
    activo = %s,
    updated_at = %s
WHERE id = %s
"""

USER_INSERT_HISTORY_SQL = """
INSERT INTO usuario_historial (usuario_id, accion, fecha, detalle)
VALUES (%s, %s, %s, %s)
"""

USER_DELETE_SQL = """
DELETE FROM usuario
WHERE id = %s
"""

USER_SCHEMA_BOOTSTRAP_SQL = """
CREATE TABLE IF NOT EXISTS usuario (
    id                    TEXT        NOT NULL,
    nombre                TEXT        NOT NULL,
    apellidos             TEXT        NOT NULL,
    email                 TEXT        NOT NULL,
    rol_principal         TEXT        NOT NULL,
    estado                TEXT        NOT NULL,
    fecha_alta            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ultimo_acceso         TIMESTAMPTZ,
    CONSTRAINT usuario_pk PRIMARY KEY (id),
    CONSTRAINT usuario_email_uk UNIQUE (email),
    CONSTRAINT usuario_estado_ck CHECK (estado IN ('activo', 'deshabilitado', 'bloqueado'))
);
ALTER TABLE IF EXISTS usuario DROP COLUMN IF EXISTS observaciones_internas;
ALTER TABLE IF EXISTS usuario DROP CONSTRAINT IF EXISTS usuario_estado_ck;
ALTER TABLE IF EXISTS usuario DROP COLUMN IF EXISTS invitacion_pendiente;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS username VARCHAR(100);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre_completo VARCHAR(255);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS rol VARCHAR(50);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS bloqueado_hasta TIMESTAMPTZ;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS ultimo_login TIMESTAMP;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW();
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW();
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
    bloqueado_hasta = NULL;
ALTER TABLE usuario ADD CONSTRAINT usuario_estado_ck CHECK (estado IN ('activo', 'deshabilitado', 'bloqueado'));
CREATE TABLE IF NOT EXISTS usuario_historial (
    id         BIGSERIAL NOT NULL,
    usuario_id TEXT NOT NULL,
    accion     TEXT NOT NULL,
    fecha      TIMESTAMPTZ NOT NULL,
    detalle    TEXT NOT NULL,
    CONSTRAINT usuario_historial_pk PRIMARY KEY (id),
    CONSTRAINT usuario_historial_uk UNIQUE (usuario_id, fecha, accion, detalle),
    CONSTRAINT usuario_historial_usuario_fk FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_usuario_estado ON usuario (estado);
CREATE INDEX IF NOT EXISTS idx_usuario_rol_principal ON usuario (rol_principal);
CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario (email);
CREATE INDEX IF NOT EXISTS idx_usuario_fecha_alta ON usuario (fecha_alta);
CREATE INDEX IF NOT EXISTS idx_usuario_historial_usuario_fecha ON usuario_historial (usuario_id, fecha DESC, id DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_usuario_auth_username ON usuario (username) WHERE username IS NOT NULL;
INSERT INTO usuario (id, nombre, apellidos, email, rol_principal, estado, fecha_alta, ultimo_acceso, failed_login_attempts, bloqueado_hasta)
VALUES
    ('usr-001', 'Ana', 'Lopez', 'ana.lopez@licican.local', 'administrador', 'activo', '2026-04-01T09:00:00Z', '2026-04-02T08:10:00Z', 0, NULL),
    ('usr-002', 'Carlos', 'Mendez', 'carlos.mendez@licican.local', 'manager', 'activo', '2026-04-01T10:15:00Z', '2026-04-02T07:50:00Z', 0, NULL),
    ('usr-003', 'Laura', 'Gonzalez', 'laura.gonzalez@licican.local', 'colaborador', 'deshabilitado', '2026-04-02T08:30:00Z', NULL, 0, NULL),
    ('usr-004', 'Mario', 'Perez', 'mario.perez@licican.local', 'invitado', 'deshabilitado', '2026-03-30T11:00:00Z', '2026-03-31T15:15:00Z', 0, NULL)
ON CONFLICT (id) DO NOTHING;
INSERT INTO usuario_historial (usuario_id, accion, fecha, detalle)
VALUES
    ('usr-001', 'alta', '2026-04-01T09:00:00Z', 'Alta inicial de la cuenta administrativa.'),
    ('usr-001', 'acceso', '2026-04-02T08:10:00Z', 'Acceso de verificacion en el entorno de producto.'),
    ('usr-002', 'alta', '2026-04-01T10:15:00Z', 'Alta de administracion funcional.'),
    ('usr-003', 'alta', '2026-04-02T08:30:00Z', 'Alta inicial de la cuenta.'),
    ('usr-004', 'alta', '2026-03-30T11:00:00Z', 'Alta inicial de invitado.'),
    ('usr-004', 'desactivacion', '2026-04-01T12:00:00Z', 'Cuenta desactivada temporalmente.')
ON CONFLICT (usuario_id, fecha, accion, detalle) DO NOTHING;
"""

_SCHEMA_BOOTSTRAPPED = False


@dataclass(frozen=True)
class UserEvent:
    accion: str
    fecha: str
    detalle: str

    def to_payload(self) -> dict[str, object]:
        return {"accion": self.accion, "fecha": self.fecha, "detalle": self.detalle}


@dataclass(frozen=True)
class ManagedUser:
    id: str
    nombre: str
    apellidos: str
    email: str
    rol_principal: str
    estado: str
    fecha_alta: str
    ultimo_acceso: str | None
    historial: tuple[UserEvent, ...]
    failed_login_attempts: int = 0
    bloqueado_hasta: str | None = None
    username: str | None = None
    password_hash: str | None = None

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellidos}".strip()

    def to_payload(self) -> dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "username": self.username,
            "rol_principal": self.rol_principal,
            "estado": self.estado,
            "fecha_alta": self.fecha_alta,
            "ultimo_acceso": self.ultimo_acceso,
            "failed_login_attempts": self.failed_login_attempts,
            "bloqueado_hasta": self.bloqueado_hasta,
            "historial": [event.to_payload() for event in self.historial],
        }


@dataclass(frozen=True)
class UserFilters:
    busqueda: str | None = None
    estado: str | None = None
    rol: str | None = None

    def normalized(self) -> "UserFilters":
        return UserFilters(
            busqueda=_clean_text(self.busqueda),
            estado=_clean_text(self.estado),
            rol=_clean_text(self.rol),
        )

    def active_filters(self) -> dict[str, str]:
        normalized = self.normalized()
        payload = {}
        if normalized.busqueda:
            payload["busqueda"] = normalized.busqueda
        if normalized.estado:
            payload["estado"] = normalized.estado
        if normalized.rol:
            payload["rol"] = normalized.rol
        return payload


class UsersDatabaseError(RuntimeError):
    pass


def _current_timestamp() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _format_timestamp(value: datetime | date | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or None
    if isinstance(value, datetime):
        normalized = value.astimezone(timezone.utc).replace(microsecond=0)
        return normalized.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _parse_timestamp(value: str | datetime | None) -> datetime:
    if value is None:
        return _current_timestamp()
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).replace(microsecond=0)
    cleaned = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(cleaned)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(microsecond=0)


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _normalize_email(raw: str) -> str:
    return raw.strip().lower()


def _normalize_role(raw: str) -> str:
    normalized = raw.strip().lower()
    aliases = {
        "administrador de plataforma": "administrador",
        "superadmin": "superadmin",
        "super administrador": "superadmin",
        "administrador funcional": "manager",
        "responsable": "manager",
        "lector": "invitado",
        "lector/invitado": "invitado",
    }
    return aliases.get(normalized, normalized)


def _normalize_state(raw: str) -> str:
    normalized = raw.strip().lower()
    return normalized if normalized in {"activo", "deshabilitado", "bloqueado"} else "deshabilitado"


def _state_metadata_for_user(state: str, now: datetime | None = None) -> tuple[int, str | None]:
    if state == "bloqueado":
        settings = get_auth_settings()
        moment = now or _current_timestamp()
        return settings.login_max_failed_attempts, _format_timestamp(moment + timedelta(minutes=settings.login_lock_minutes))
    return 0, None


def _is_admin_role(role: str) -> bool:
    return _normalize_role(role) in {"administrador", "superadmin"}


def _is_superadmin_user(user: ManagedUser) -> bool:
    return _normalize_role(user.rol_principal) == "superadmin"


def _superadmin_mutation_error() -> ValueError:
    return ValueError("La cuenta superadmin no puede editarse, deshabilitarse ni borrarse desde la interfaz. Solo se gestiona mediante el fichero .env.")


def _connect():
    try:
        return psycopg2.connect(resolve_database_url())
    except psycopg2.Error as exc:
        raise UsersDatabaseError("No se pudo consultar PostgreSQL para gestionar usuarios.") from exc


def _ensure_schema(connection) -> None:
    global _SCHEMA_BOOTSTRAPPED
    if _SCHEMA_BOOTSTRAPPED:
        return
    with connection.cursor() as cursor:
        cursor.execute(USER_SCHEMA_BOOTSTRAP_SQL)
    _SCHEMA_BOOTSTRAPPED = True


def _default_history(action: str, detail: str, now: datetime | None = None) -> tuple[UserEvent, ...]:
    return (_event(action, detail, now),)


def _event(action: str, detail: str, now: datetime | None = None) -> UserEvent:
    return UserEvent(accion=action, fecha=_format_timestamp(now or _current_timestamp()) or "", detalle=detail)


def _user_from_record(record: dict[str, object]) -> ManagedUser:
    return ManagedUser(
        id=str(record["id"]),
        nombre=str(record.get("nombre") or ""),
        apellidos=str(record.get("apellidos") or ""),
        email=str(record.get("email") or ""),
        rol_principal=str(record.get("rol_principal") or ""),
        estado=_normalize_state(str(record.get("estado") or "deshabilitado")),
        fecha_alta=_format_timestamp(record.get("fecha_alta")) or _format_timestamp(_current_timestamp()) or "",
        ultimo_acceso=_format_timestamp(record.get("ultimo_acceso")),
        failed_login_attempts=int(record.get("failed_login_attempts") or 0),
        bloqueado_hasta=_format_timestamp(record.get("bloqueado_hasta")),
        username=_clean_text(str(record.get("username") or "")),
        password_hash=_clean_text(str(record.get("password_hash") or "")),
        historial=(),
    )


def _load_aggregated_rows() -> tuple[str, list[dict[str, object]], list[dict[str, object]]]:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(USERS_SELECT_SQL)
                users = list(cursor.fetchall())
                cursor.execute(USER_HISTORY_SELECT_SQL)
                history = list(cursor.fetchall())
    except psycopg2.Error as exc:
        raise UsersDatabaseError("No se pudo consultar PostgreSQL para gestionar usuarios.") from exc
    return DEFAULT_REFERENCE, users, history


def _assemble_users(
    user_rows: list[dict[str, object]],
    history_rows: list[dict[str, object]],
) -> list[ManagedUser]:
    users = [_user_from_record(row) for row in user_rows]
    users_by_id = {user.id: user for user in users}

    history_by_user: dict[str, list[tuple[datetime, UserEvent]]] = {user_id: [] for user_id in users_by_id}
    for row in history_rows:
        user_id = str(row.get("usuario_id") or "")
        if not user_id:
            continue
        history_by_user.setdefault(user_id, []).append(
            (
                _parse_timestamp(row.get("fecha")),
                UserEvent(
                    accion=str(row.get("accion") or "evento"),
                    fecha=_format_timestamp(row.get("fecha")) or "",
                    detalle=str(row.get("detalle") or ""),
                ),
            )
        )

    assembled: list[ManagedUser] = []
    for user in users:
        history = tuple(event for _, event in sorted(history_by_user.get(user.id, []), key=lambda item: item[0]))
        assembled.append(
            ManagedUser(
                id=user.id,
                nombre=user.nombre,
                apellidos=user.apellidos,
                email=user.email,
                rol_principal=user.rol_principal,
                estado=user.estado,
                fecha_alta=user.fecha_alta,
                ultimo_acceso=user.ultimo_acceso,
                username=user.username,
                password_hash=user.password_hash,
                historial=history,
                failed_login_attempts=user.failed_login_attempts,
                bloqueado_hasta=user.bloqueado_hasta,
            )
        )
    return assembled


def load_users() -> tuple[str, list[ManagedUser]]:
    reference, user_rows, history_rows = _load_aggregated_rows()
    return reference, _assemble_users(user_rows, history_rows)


def _ensure_admin_guard(users: list[ManagedUser], candidate_user: ManagedUser, new_role: str, new_state: str) -> None:
    current_is_active_admin = _is_admin_role(candidate_user.rol_principal) and candidate_user.estado == "activo"
    candidate_would_be_active_admin = _is_admin_role(new_role) and new_state == "activo"
    if current_is_active_admin and not candidate_would_be_active_admin and _active_admin_count(users, candidate_user.id) == 0:
        raise ValueError("No se puede dejar el sistema sin ningun usuario administrador activo.")


def _active_admin_count(users: list[ManagedUser], exclude_user_id: str | None = None) -> int:
    return sum(
        1
        for user in users
        if user.id != exclude_user_id and _is_admin_role(user.rol_principal) and user.estado == "activo"
    )


def _validate_user_fields(
    users: list[ManagedUser],
    nombre: str,
    apellidos: str,
    email: str,
    username: str | None,
    rol_principal: str,
    estado: str,
    user_id: str | None = None,
) -> tuple[str, str, str, str, str, str | None]:
    nombre = _clean_text(nombre) or ""
    apellidos = _clean_text(apellidos) or ""
    email = _clean_text(email) or ""
    username = _clean_text(username)
    rol_principal = _clean_text(rol_principal) or ""
    estado = _clean_text(estado) or "deshabilitado"

    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if not apellidos:
        raise ValueError("Los apellidos son obligatorios.")
    if not email:
        raise ValueError("El email es obligatorio.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("El email no tiene un formato valido.")
    if not rol_principal:
        raise ValueError("El rol principal es obligatorio.")
    if _normalize_role(rol_principal) == "superadmin":
        raise ValueError("El rol superadmin no puede asignarse desde la interfaz. Solo se gestiona mediante el fichero .env.")
    if _normalize_state(estado) not in USER_STATUSES:
        raise ValueError("El estado indicado no es valido.")

    normalized_email = _normalize_email(email)
    for existing in users:
        if user_id is not None and existing.id == user_id:
            continue
        if _normalize_email(existing.email) == normalized_email:
            raise ValueError("El email no puede duplicarse entre usuarios.")
        existing_username = _clean_text(existing.username)
        if username and existing_username and existing_username == username:
            raise ValueError("El nombre de usuario no puede duplicarse entre usuarios.")
        if username and _normalize_email(existing.email) == _normalize_email(username):
            raise ValueError("El nombre de usuario no puede duplicarse con un email existente.")
        if existing_username and _normalize_email(existing_username) == normalized_email:
            raise ValueError("El email no puede duplicarse con un nombre de usuario existente.")

    return nombre, apellidos, normalized_email, _normalize_role(rol_principal), _normalize_state(estado), username


def _display_optional_text(value: object | None) -> str:
    cleaned = _clean_text(str(value or "")) if value is not None else None
    return cleaned if cleaned else "-"


def _login_name_for_user(user: dict[str, object]) -> str:
    username = _clean_text(str(user.get("username") or ""))
    if username:
        return username
    email = _clean_text(str(user.get("email") or ""))
    if email:
        return email
    return str(user.get("id") or "—")


def summarize_users(users: list[ManagedUser]) -> dict[str, int]:
    return {
        "usuarios_totales": len(users),
        "usuarios_activos": sum(1 for user in users if user.estado == "activo"),
        "usuarios_deshabilitados": sum(1 for user in users if user.estado == "deshabilitado"),
        "usuarios_bloqueados": sum(1 for user in users if user.estado == "bloqueado"),
        "roles_definidos": len({user.rol_principal for user in users}) if users else len(USER_ROLES),
    }


def filter_users(users: list[ManagedUser], filters: UserFilters) -> list[ManagedUser]:
    normalized = filters.normalized()
    result = users
    if normalized.busqueda:
        query = normalized.busqueda.lower()
        result = [
            user
            for user in result
            if query in user.id.lower()
            or query in user.nombre.lower()
            or query in user.apellidos.lower()
            or query in user.email.lower()
            or (user.username is not None and query in user.username.lower())
        ]
    if normalized.estado:
        result = [user for user in result if user.estado == normalized.estado]
    if normalized.rol:
        result = [user for user in result if user.rol_principal == normalized.rol]
    return sorted(result, key=lambda user: (user.apellidos.lower(), user.nombre.lower(), user.email.lower()))


def available_filter_options(users: list[ManagedUser]) -> dict[str, list[str]]:
    return {
        "estados": list(USER_STATUSES),
        "roles": list(USER_ROLES),
    }


def paginate_users(users: list[ManagedUser], page: int, page_size: int) -> dict[str, object]:
    page = max(1, page)
    page_size = page_size if page_size in {5, 10, 25, 50} else 10
    total_resultados = len(users)
    total_paginas = max(1, (total_resultados + page_size - 1) // page_size)
    adjusted = False
    reason = None
    if page > total_paginas:
        adjusted = True
        reason = "fuera_de_rango"
        page = 1

    start = (page - 1) * page_size
    end = start + page_size
    visible = users[start:end]
    resultado_desde = start + 1 if visible else 0
    resultado_hasta = start + len(visible) if visible else 0
    return {
        "pagina_solicitada": page,
        "pagina_actual": page,
        "tamano_pagina": page_size,
        "total_paginas": total_paginas,
        "total_resultados": total_resultados,
        "resultado_desde": resultado_desde,
        "resultado_hasta": resultado_hasta,
        "hay_anterior": page > 1 and total_paginas > 1,
        "hay_siguiente": page < total_paginas,
        "pagina_anterior": page - 1 if page > 1 and total_paginas > 1 else None,
        "pagina_siguiente": page + 1 if page < total_paginas else None,
        "ajustada": adjusted,
        "motivo_ajuste": reason,
        "items": [user.to_payload() for user in visible],
    }


def build_users_payload(
    filters: UserFilters | None = None,
    page: int = 1,
    page_size: int = 10,
    selected_user_id: str | None = None,
) -> dict[str, object]:
    reference, users = load_users()
    active_filters = (filters or UserFilters()).normalized()
    filtered = filter_users(users, active_filters)
    pagination = paginate_users(filtered, page, page_size)
    selected_user = None
    if selected_user_id:
        selected_user = next((user for user in users if user.id == selected_user_id), None)
    return {
        "referencia_funcional": reference,
        "summary": summarize_users(users),
        "filtros_activos": active_filters.active_filters(),
        "filtros_disponibles": available_filter_options(users),
        "paginacion": {key: value for key, value in pagination.items() if key != "items"},
        "usuarios": pagination["items"],
        "usuario_seleccionado": None if selected_user is None else selected_user.to_payload(),
    }


def create_user(
    *,
    nombre: str,
    apellidos: str,
    email: str,
    rol_principal: str,
    estado: str = "deshabilitado",
    now: str | datetime | None = None,
) -> ManagedUser:
    _, users = load_users()
    nombre, apellidos, normalized_email, normalized_role, normalized_state, _ = _validate_user_fields(
        users,
        nombre,
        apellidos,
        email,
        None,
        rol_principal,
        estado,
    )
    timestamp = _parse_timestamp(now)
    failed_login_attempts, bloqueado_hasta = _state_metadata_for_user(normalized_state, timestamp)
    new_user = ManagedUser(
        id=_next_user_id(users),
        nombre=nombre,
        apellidos=apellidos,
        email=normalized_email,
        rol_principal=normalized_role,
        estado=normalized_state,
        fecha_alta=_format_timestamp(timestamp) or "",
        ultimo_acceso=None,
        failed_login_attempts=failed_login_attempts,
        bloqueado_hasta=bloqueado_hasta,
        username=normalized_email,
        password_hash=None,
        historial=_default_history("alta", "Alta inicial de la cuenta.", timestamp),
    )
    _persist_user(new_user)
    return new_user


def update_user(
    user_id: str,
    *,
    nombre: str,
    apellidos: str,
    email: str,
    username: str | None = None,
    rol_principal: str,
    estado: str,
    nueva_contrasena: str | None = None,
    confirmar_contrasena: str | None = None,
    now: str | datetime | None = None,
) -> ManagedUser:
    _, users = load_users()
    for current in users:
        if current.id != user_id:
            continue
        if _is_superadmin_user(current):
            raise _superadmin_mutation_error()
        nombre, apellidos, normalized_email, normalized_role, normalized_state, normalized_username = _validate_user_fields(
            users,
            nombre,
            apellidos,
            email,
            username,
            rol_principal,
            estado,
            user_id=user_id,
        )
        _ensure_admin_guard(users, current, normalized_role, normalized_state)
        timestamp = _parse_timestamp(now)
        failed_login_attempts, bloqueado_hasta = _state_metadata_for_user(normalized_state, timestamp)
        password_hash = current.password_hash
        history_detail = "Datos basicos, rol o estado actualizados."
        if nueva_contrasena or confirmar_contrasena:
            password_hash = _hash_password(nueva_contrasena, confirmar_contrasena)
            history_detail = "Datos basicos, rol, estado y contrasena actualizados."
        updated = ManagedUser(
            id=current.id,
            nombre=nombre,
            apellidos=apellidos,
            email=normalized_email,
            rol_principal=normalized_role,
            estado=normalized_state,
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            username=normalized_username or current.username or normalized_email,
            password_hash=password_hash,
            historial=(
                *current.historial,
                _event("edicion", history_detail, timestamp),
            ),
            failed_login_attempts=failed_login_attempts,
            bloqueado_hasta=bloqueado_hasta,
        )
        _replace_user_record(updated)
        return updated
    raise KeyError(user_id)


def change_user_state(
    user_id: str,
    state: str,
    *,
    now: str | datetime | None = None,
) -> ManagedUser:
    _, users = load_users()
    normalized_state = _normalize_state(state)
    if normalized_state not in USER_STATUSES:
        raise ValueError("El estado indicado no es valido.")
    for current in users:
        if current.id != user_id:
            continue
        if _is_superadmin_user(current):
            raise _superadmin_mutation_error()
        _ensure_admin_guard(users, current, current.rol_principal, normalized_state)
        timestamp = _parse_timestamp(now)
        failed_login_attempts, bloqueado_hasta = _state_metadata_for_user(normalized_state, timestamp)
        updated = ManagedUser(
            id=current.id,
            nombre=current.nombre,
            apellidos=current.apellidos,
            email=current.email,
            rol_principal=current.rol_principal,
            estado=normalized_state,
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            username=current.username,
            password_hash=current.password_hash,
            historial=(
                *current.historial,
                _event("cambio_estado", f"Estado cambiado a {normalized_state}.", timestamp),
            ),
            failed_login_attempts=failed_login_attempts,
            bloqueado_hasta=bloqueado_hasta,
        )
        _replace_user_record(updated)
        return updated
    raise KeyError(user_id)


def delete_user(
    user_id: str,
) -> None:
    _, users = load_users()
    for current in users:
        if current.id != user_id:
            continue
        if _is_superadmin_user(current):
            raise _superadmin_mutation_error()
        if _is_admin_role(current.rol_principal) and current.estado == "activo" and _active_admin_count(users, user_id) == 0:
            raise ValueError("No se puede eliminar el ultimo usuario administrador activo.")
        try:
            with _connect() as connection:
                _ensure_schema(connection)
                with connection.cursor() as cursor:
                    cursor.execute(USER_DELETE_SQL, (user_id,))
        except psycopg2.Error as exc:
            raise UsersDatabaseError("No se pudo consultar PostgreSQL para gestionar usuarios.") from exc
        return
    raise KeyError(user_id)


def _replace_user_record(updated_user: ManagedUser) -> None:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor() as cursor:
                cursor.execute(
                    USER_UPDATE_SQL,
                    (
                        updated_user.nombre,
                        updated_user.apellidos,
                        updated_user.email,
                        updated_user.rol_principal,
                        updated_user.estado,
                        _parse_timestamp(updated_user.ultimo_acceso) if updated_user.ultimo_acceso else None,
                        updated_user.failed_login_attempts,
                        _parse_timestamp(updated_user.bloqueado_hasta) if updated_user.bloqueado_hasta else None,
                        updated_user.username,
                        updated_user.password_hash,
                        updated_user.nombre_completo,
                        updated_user.rol_principal,
                        updated_user.estado == "activo",
                        _current_timestamp().replace(tzinfo=None),
                        updated_user.id,
                    ),
                )
                cursor.execute(
                    USER_INSERT_HISTORY_SQL,
                    (
                        updated_user.id,
                        updated_user.historial[-1].accion,
                        _parse_timestamp(updated_user.historial[-1].fecha),
                        updated_user.historial[-1].detalle,
                    ),
                )
    except psycopg2.Error as exc:
        raise UsersDatabaseError("No se pudo consultar PostgreSQL para gestionar usuarios.") from exc


def _persist_user(new_user: ManagedUser) -> None:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor() as cursor:
                cursor.execute(
                    USER_INSERT_SQL,
                    (
                        new_user.id,
                        new_user.nombre,
                        new_user.apellidos,
                        new_user.email,
                        new_user.rol_principal,
                        new_user.estado,
                        _parse_timestamp(new_user.fecha_alta),
                        None,
                        new_user.failed_login_attempts,
                        _parse_timestamp(new_user.bloqueado_hasta) if new_user.bloqueado_hasta else None,
                        new_user.username,
                        new_user.password_hash,
                        new_user.nombre_completo,
                        new_user.rol_principal,
                        new_user.estado == "activo",
                        _current_timestamp().replace(tzinfo=None),
                    ),
                )
                for event in new_user.historial:
                    cursor.execute(
                        USER_INSERT_HISTORY_SQL,
                        (
                            new_user.id,
                            event.accion,
                            _parse_timestamp(event.fecha),
                            event.detalle,
                        ),
                    )
    except psycopg2.Error as exc:
        raise UsersDatabaseError("No se pudo consultar PostgreSQL para gestionar usuarios.") from exc


def _next_user_id(users: list[ManagedUser]) -> str:
    numbers = []
    for user in users:
        if user.id.startswith("usr-"):
            try:
                numbers.append(int(user.id.split("-", 1)[1]))
            except ValueError:
                continue
    next_number = (max(numbers) if numbers else 0) + 1
    existing_ids = {user.id for user in users}
    while True:
        candidate = f"usr-{next_number:03d}"
        if candidate not in existing_ids:
            return candidate
        next_number += 1


def _hash_password(
    nueva_contrasena: str | None,
    confirmar_contrasena: str | None,
) -> str:
    password = (nueva_contrasena or "").strip()
    confirm = (confirmar_contrasena or "").strip()
    if not password:
        raise ValueError("La nueva contrasena no puede estar vacia.")
    if len(password) < 8:
        raise ValueError("La nueva contrasena debe tener al menos 8 caracteres.")
    if password != confirm:
        raise ValueError("La confirmacion de contrasena no coincide.")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
