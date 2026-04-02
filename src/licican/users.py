from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from licican.config import BASE_DIR


DEFAULT_USERS_PATH = BASE_DIR / "data" / "users.json"
DEFAULT_REFERENCE = "PB-016 - HU-16 - CU-16 - Gestion administrativa de usuarios"
USER_STATUSES = ("activo", "inactivo", "pendiente", "bloqueado", "baja logica")
USER_ROLES = (
    "administrador de plataforma",
    "administrador funcional",
    "responsable",
    "colaborador",
    "lector",
)
DEFAULT_SURFACES = ("Catalogo", "Datos consolidados", "Alertas", "Pipeline", "KPIs", "Permisos")


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
    superficies: tuple[str, ...]
    observaciones_internas: str
    fecha_alta: str
    ultimo_acceso: str | None
    invitacion_pendiente: bool
    historial: tuple[UserEvent, ...]

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
            "rol_principal": self.rol_principal,
            "estado": self.estado,
            "superficies": list(self.superficies),
            "observaciones_internas": self.observaciones_internas,
            "fecha_alta": self.fecha_alta,
            "ultimo_acceso": self.ultimo_acceso,
            "invitacion_pendiente": self.invitacion_pendiente,
            "historial": [event.to_payload() for event in self.historial],
        }


@dataclass(frozen=True)
class UserFilters:
    busqueda: str | None = None
    estado: str | None = None
    rol: str | None = None
    superficie: str | None = None

    def normalized(self) -> "UserFilters":
        return UserFilters(
            busqueda=_clean_text(self.busqueda),
            estado=_clean_text(self.estado),
            rol=_clean_text(self.rol),
            superficie=_clean_text(self.superficie),
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
        if normalized.superficie:
            payload["superficie"] = normalized.superficie
        return payload


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _split_surfaces(raw: str | Iterable[str] | None) -> tuple[str, ...]:
    if raw is None:
        return ()
    if isinstance(raw, str):
        values = raw.replace(";", ",").split(",")
    else:
        values = list(raw)
    return tuple(item.strip() for item in values if str(item).strip())


def _normalize_email(raw: str) -> str:
    return raw.strip().lower()


def _normalize_role(raw: str) -> str:
    return raw.strip().lower()


def _normalize_state(raw: str) -> str:
    return raw.strip().lower()


def _default_history(action: str, detail: str, now: str | None = None) -> tuple[UserEvent, ...]:
    return (UserEvent(accion=action, fecha=now or _current_timestamp(), detalle=detail),)


def _seed_users() -> list[dict[str, object]]:
    return [
        {
            "id": "usr-001",
            "nombre": "Ana",
            "apellidos": "Lopez",
            "email": "ana.lopez@licican.local",
            "rol_principal": "administrador de plataforma",
            "estado": "activo",
            "superficies": ["Catalogo", "Usuarios", "Permisos", "KPIs"],
            "observaciones_internas": "Cuenta administrativa principal.",
            "fecha_alta": "2026-04-01T09:00:00Z",
            "ultimo_acceso": "2026-04-02T08:10:00Z",
            "invitacion_pendiente": False,
            "historial": [
                {"accion": "alta", "fecha": "2026-04-01T09:00:00Z", "detalle": "Alta inicial de la cuenta administrativa."},
                {"accion": "acceso", "fecha": "2026-04-02T08:10:00Z", "detalle": "Acceso de verificacion en el entorno de producto."},
            ],
        },
        {
            "id": "usr-002",
            "nombre": "Carlos",
            "apellidos": "Mendez",
            "email": "carlos.mendez@licican.local",
            "rol_principal": "administrador funcional",
            "estado": "activo",
            "superficies": ["Catalogo", "Alertas", "Pipeline"],
            "observaciones_internas": "Apoyo funcional de operaciones.",
            "fecha_alta": "2026-04-01T10:15:00Z",
            "ultimo_acceso": "2026-04-02T07:50:00Z",
            "invitacion_pendiente": False,
            "historial": [
                {"accion": "alta", "fecha": "2026-04-01T10:15:00Z", "detalle": "Alta de administracion funcional."}
            ],
        },
        {
            "id": "usr-003",
            "nombre": "Laura",
            "apellidos": "Gonzalez",
            "email": "laura.gonzalez@licican.local",
            "rol_principal": "responsable",
            "estado": "pendiente",
            "superficies": ["Catalogo", "Datos consolidados"],
            "observaciones_internas": "Invitacion pendiente de activacion.",
            "fecha_alta": "2026-04-02T08:30:00Z",
            "ultimo_acceso": None,
            "invitacion_pendiente": True,
            "historial": [
                {"accion": "alta", "fecha": "2026-04-02T08:30:00Z", "detalle": "Invitacion inicial enviada."}
            ],
        },
        {
            "id": "usr-004",
            "nombre": "Mario",
            "apellidos": "Perez",
            "email": "mario.perez@licican.local",
            "rol_principal": "colaborador",
            "estado": "inactivo",
            "superficies": ["Catalogo", "Alertas"],
            "observaciones_internas": "Usuario en pausa operativa.",
            "fecha_alta": "2026-03-30T11:00:00Z",
            "ultimo_acceso": "2026-03-31T15:15:00Z",
            "invitacion_pendiente": False,
            "historial": [
                {"accion": "alta", "fecha": "2026-03-30T11:00:00Z", "detalle": "Alta inicial de colaborador."},
                {"accion": "desactivacion", "fecha": "2026-04-01T12:00:00Z", "detalle": "Cuenta desactivada temporalmente."},
            ],
        },
    ]


def _default_payload() -> dict[str, object]:
    return {
        "referencia_funcional": DEFAULT_REFERENCE,
        "users": _seed_users(),
    }


def _user_from_payload(payload: dict[str, object]) -> ManagedUser:
    historial = tuple(
        UserEvent(
            accion=str(item.get("accion") or "evento"),
            fecha=str(item.get("fecha") or _current_timestamp()),
            detalle=str(item.get("detalle") or ""),
        )
        for item in payload.get("historial", [])
    )
    return ManagedUser(
        id=str(payload["id"]),
        nombre=str(payload.get("nombre") or ""),
        apellidos=str(payload.get("apellidos") or ""),
        email=str(payload.get("email") or ""),
        rol_principal=str(payload.get("rol_principal") or ""),
        estado=str(payload.get("estado") or "pendiente"),
        superficies=tuple(str(item) for item in payload.get("superficies", []) if str(item).strip()),
        observaciones_internas=str(payload.get("observaciones_internas") or ""),
        fecha_alta=str(payload.get("fecha_alta") or _current_timestamp()),
        ultimo_acceso=None if payload.get("ultimo_acceso") in (None, "") else str(payload.get("ultimo_acceso")),
        invitacion_pendiente=bool(payload.get("invitacion_pendiente", False)),
        historial=historial,
    )


def load_users(path: Path = DEFAULT_USERS_PATH) -> tuple[str, list[ManagedUser]]:
    if not path.is_file():
        payload = _default_payload()
        return payload["referencia_funcional"], [_user_from_payload(item) for item in payload["users"]]

    payload = json.loads(path.read_text(encoding="utf-8"))
    reference = str(payload.get("referencia_funcional") or DEFAULT_REFERENCE)
    users = [_user_from_payload(item) for item in payload.get("users", [])]
    return reference, users


def _save_users(reference: str, users: list[ManagedUser], path: Path) -> None:
    payload = {"referencia_funcional": reference, "users": [user.to_payload() for user in users]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def _is_admin_role(role: str) -> bool:
    return _normalize_role(role).startswith("administrador")


def _validate_user_fields(
    users: list[ManagedUser],
    nombre: str,
    apellidos: str,
    email: str,
    rol_principal: str,
    superficies: Iterable[str],
    estado: str,
    user_id: str | None = None,
) -> tuple[str, str, str, str, tuple[str, ...], str]:
    nombre = _clean_text(nombre) or ""
    apellidos = _clean_text(apellidos) or ""
    email = _clean_text(email) or ""
    rol_principal = _clean_text(rol_principal) or ""
    estado = _clean_text(estado) or "pendiente"
    surfaces = tuple(item for item in _split_surfaces(superficies) if item)

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
    if _normalize_state(estado) not in USER_STATUSES:
        raise ValueError("El estado indicado no es valido.")
    if not surfaces:
        raise ValueError("Debe indicarse al menos una superficie, area o modulo.")

    normalized_email = _normalize_email(email)
    for existing in users:
        if user_id is not None and existing.id == user_id:
            continue
        if _normalize_email(existing.email) == normalized_email:
            raise ValueError("El email no puede duplicarse entre usuarios.")

    return nombre, apellidos, normalized_email, _normalize_role(rol_principal), surfaces, _normalize_state(estado)


def _active_admin_count(users: list[ManagedUser], exclude_user_id: str | None = None) -> int:
    return sum(
        1
        for user in users
        if user.id != exclude_user_id and _is_admin_role(user.rol_principal) and user.estado == "activo"
    )


def _ensure_admin_guard(users: list[ManagedUser], candidate_user: ManagedUser, new_role: str, new_state: str) -> None:
    current_is_active_admin = _is_admin_role(candidate_user.rol_principal) and candidate_user.estado == "activo"
    candidate_would_be_active_admin = _is_admin_role(new_role) and new_state == "activo"
    if current_is_active_admin and not candidate_would_be_active_admin and _active_admin_count(users, candidate_user.id) == 0:
        raise ValueError("No se puede dejar el sistema sin ningun usuario administrador activo.")


def _event(action: str, detail: str, now: str | None = None) -> UserEvent:
    return UserEvent(accion=action, fecha=now or _current_timestamp(), detalle=detail)


def _replace_user(users: list[ManagedUser], updated_user: ManagedUser) -> list[ManagedUser]:
    return [updated_user if user.id == updated_user.id else user for user in users]


def summarize_users(users: list[ManagedUser]) -> dict[str, int]:
    return {
        "usuarios_totales": len(users),
        "usuarios_activos": sum(1 for user in users if user.estado == "activo"),
        "usuarios_inactivos": sum(1 for user in users if user.estado == "inactivo"),
        "invitaciones_pendientes": sum(1 for user in users if user.estado == "pendiente" or user.invitacion_pendiente),
        "roles_definidos": len({user.rol_principal for user in users}),
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
        ]
    if normalized.estado:
        result = [user for user in result if user.estado == normalized.estado]
    if normalized.rol:
        result = [user for user in result if user.rol_principal == normalized.rol]
    if normalized.superficie:
        query = normalized.superficie.lower()
        result = [
            user
            for user in result
            if any(query in surface.lower() for surface in user.superficies)
        ]
    return sorted(result, key=lambda user: (user.apellidos.lower(), user.nombre.lower(), user.email.lower()))


def available_filter_options(users: list[ManagedUser]) -> dict[str, list[str]]:
    return {
        "estados": list(USER_STATUSES),
        "roles": sorted({user.rol_principal for user in users}),
        "superficies": sorted({surface for user in users for surface in user.superficies}),
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
    path: Path = DEFAULT_USERS_PATH,
    filters: UserFilters | None = None,
    page: int = 1,
    page_size: int = 10,
    selected_user_id: str | None = None,
) -> dict[str, object]:
    reference, users = load_users(path)
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
    superficies: Iterable[str],
    estado: str = "pendiente",
    observaciones_internas: str = "",
    now: str | None = None,
    path: Path = DEFAULT_USERS_PATH,
) -> ManagedUser:
    reference, users = load_users(path)
    nombre, apellidos, normalized_email, normalized_role, normalized_surfaces, normalized_state = _validate_user_fields(
        users,
        nombre,
        apellidos,
        email,
        rol_principal,
        superficies,
        estado,
    )
    timestamp = now or _current_timestamp()
    new_user = ManagedUser(
        id=_next_user_id(users),
        nombre=nombre,
        apellidos=apellidos,
        email=normalized_email,
        rol_principal=normalized_role,
        estado=normalized_state,
        superficies=normalized_surfaces,
        observaciones_internas=_clean_text(observaciones_internas) or "",
        fecha_alta=timestamp,
        ultimo_acceso=None,
        invitacion_pendiente=normalized_state == "pendiente",
        historial=_default_history("alta", "Alta inicial de la cuenta.", timestamp),
    )
    _save_users(reference, [*users, new_user], path)
    return new_user


def update_user(
    user_id: str,
    *,
    nombre: str,
    apellidos: str,
    email: str,
    rol_principal: str,
    superficies: Iterable[str],
    estado: str,
    observaciones_internas: str = "",
    now: str | None = None,
    path: Path = DEFAULT_USERS_PATH,
) -> ManagedUser:
    reference, users = load_users(path)
    for index, current in enumerate(users):
        if current.id != user_id:
            continue
        nombre, apellidos, normalized_email, normalized_role, normalized_surfaces, normalized_state = _validate_user_fields(
            users,
            nombre,
            apellidos,
            email,
            rol_principal,
            superficies,
            estado,
            user_id=user_id,
        )
        _ensure_admin_guard(users, current, normalized_role, normalized_state)
        timestamp = now or _current_timestamp()
        updated = ManagedUser(
            id=current.id,
            nombre=nombre,
            apellidos=apellidos,
            email=normalized_email,
            rol_principal=normalized_role,
            estado=normalized_state,
            superficies=normalized_surfaces,
            observaciones_internas=_clean_text(observaciones_internas) or "",
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            invitacion_pendiente=normalized_state == "pendiente",
            historial=(
                *current.historial,
                _event("edicion", "Datos basicos, rol o superficies actualizados.", timestamp),
            ),
        )
        users[index] = updated
        _save_users(reference, users, path)
        return updated
    raise KeyError(user_id)


def change_user_state(
    user_id: str,
    state: str,
    *,
    path: Path = DEFAULT_USERS_PATH,
    now: str | None = None,
) -> ManagedUser:
    reference, users = load_users(path)
    normalized_state = _normalize_state(state)
    if normalized_state not in USER_STATUSES:
        raise ValueError("El estado indicado no es valido.")
    for index, current in enumerate(users):
        if current.id != user_id:
            continue
        _ensure_admin_guard(users, current, current.rol_principal, normalized_state)
        timestamp = now or _current_timestamp()
        updated = ManagedUser(
            id=current.id,
            nombre=current.nombre,
            apellidos=current.apellidos,
            email=current.email,
            rol_principal=current.rol_principal,
            estado=normalized_state,
            superficies=current.superficies,
            observaciones_internas=current.observaciones_internas,
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            invitacion_pendiente=normalized_state == "pendiente",
            historial=(
                *current.historial,
                _event("cambio_estado", f"Estado cambiado a {normalized_state}.", timestamp),
            ),
        )
        users[index] = updated
        _save_users(reference, users, path)
        return updated
    raise KeyError(user_id)


def resend_invitation(
    user_id: str,
    *,
    path: Path = DEFAULT_USERS_PATH,
    now: str | None = None,
) -> ManagedUser:
    reference, users = load_users(path)
    timestamp = now or _current_timestamp()
    for index, current in enumerate(users):
        if current.id != user_id:
            continue
        if current.estado != "pendiente":
            raise ValueError("Solo se puede reenviar invitacion a usuarios pendientes de activacion.")
        updated = ManagedUser(
            id=current.id,
            nombre=current.nombre,
            apellidos=current.apellidos,
            email=current.email,
            rol_principal=current.rol_principal,
            estado=current.estado,
            superficies=current.superficies,
            observaciones_internas=current.observaciones_internas,
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            invitacion_pendiente=True,
            historial=(
                *current.historial,
                _event("reenvio_invitacion", "Se reenvio la invitacion de activacion.", timestamp),
            ),
        )
        users[index] = updated
        _save_users(reference, users, path)
        return updated
    raise KeyError(user_id)


def reset_access(
    user_id: str,
    *,
    path: Path = DEFAULT_USERS_PATH,
    now: str | None = None,
) -> ManagedUser:
    reference, users = load_users(path)
    timestamp = now or _current_timestamp()
    for index, current in enumerate(users):
        if current.id != user_id:
            continue
        if current.estado == "pendiente":
            raise ValueError("No se puede reiniciar el acceso de un usuario pendiente de activacion.")
        updated = ManagedUser(
            id=current.id,
            nombre=current.nombre,
            apellidos=current.apellidos,
            email=current.email,
            rol_principal=current.rol_principal,
            estado=current.estado,
            superficies=current.superficies,
            observaciones_internas=current.observaciones_internas,
            fecha_alta=current.fecha_alta,
            ultimo_acceso=current.ultimo_acceso,
            invitacion_pendiente=current.invitacion_pendiente,
            historial=(
                *current.historial,
                _event("reinicio_acceso", "Se reinicio el acceso o la contrasena.", timestamp),
            ),
        )
        users[index] = updated
        _save_users(reference, users, path)
        return updated
    raise KeyError(user_id)
