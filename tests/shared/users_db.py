from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from licican import users as users_module


def _ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


@dataclass
class SeededUsersState:
    users: dict[str, dict[str, Any]]
    history: dict[str, list[dict[str, Any]]]

    @classmethod
    def seed(cls) -> "SeededUsersState":
        return cls(
            users={
                "usr-001": {
                    "id": "usr-001",
                    "nombre": "Ana",
                    "apellidos": "Lopez",
                    "email": "ana.lopez@licican.local",
                    "rol_principal": "administrador",
                    "estado": "activo",
                    "fecha_alta": _ts("2026-04-01T09:00:00Z"),
                    "ultimo_acceso": _ts("2026-04-02T08:10:00Z"),
                    "invitacion_pendiente": False,
                },
                "usr-002": {
                    "id": "usr-002",
                    "nombre": "Carlos",
                    "apellidos": "Mendez",
                    "email": "carlos.mendez@licican.local",
                    "rol_principal": "manager",
                    "estado": "activo",
                    "fecha_alta": _ts("2026-04-01T10:15:00Z"),
                    "ultimo_acceso": _ts("2026-04-02T07:50:00Z"),
                    "invitacion_pendiente": False,
                },
                "usr-003": {
                    "id": "usr-003",
                    "nombre": "Laura",
                    "apellidos": "Gonzalez",
                    "email": "laura.gonzalez@licican.local",
                    "rol_principal": "colaborador",
                    "estado": "pendiente",
                    "fecha_alta": _ts("2026-04-02T08:30:00Z"),
                    "ultimo_acceso": None,
                    "invitacion_pendiente": True,
                },
                "usr-004": {
                    "id": "usr-004",
                    "nombre": "Mario",
                    "apellidos": "Perez",
                    "email": "mario.perez@licican.local",
                    "rol_principal": "invitado",
                    "estado": "inactivo",
                    "fecha_alta": _ts("2026-03-30T11:00:00Z"),
                    "ultimo_acceso": _ts("2026-03-31T15:15:00Z"),
                    "invitacion_pendiente": False,
                },
            },
            history={
                "usr-001": [
                    {
                        "usuario_id": "usr-001",
                        "accion": "alta",
                        "fecha": _ts("2026-04-01T09:00:00Z"),
                        "detalle": "Alta inicial de la cuenta administrativa.",
                    },
                    {
                        "usuario_id": "usr-001",
                        "accion": "acceso",
                        "fecha": _ts("2026-04-02T08:10:00Z"),
                        "detalle": "Acceso de verificacion en el entorno de producto.",
                    },
                ],
                "usr-002": [
                    {
                        "usuario_id": "usr-002",
                        "accion": "alta",
                        "fecha": _ts("2026-04-01T10:15:00Z"),
                        "detalle": "Alta de administracion funcional.",
                    }
                ],
                "usr-003": [
                    {
                        "usuario_id": "usr-003",
                        "accion": "alta",
                        "fecha": _ts("2026-04-02T08:30:00Z"),
                        "detalle": "Invitacion inicial enviada.",
                    }
                ],
                "usr-004": [
                    {
                        "usuario_id": "usr-004",
                        "accion": "alta",
                        "fecha": _ts("2026-03-30T11:00:00Z"),
                        "detalle": "Alta inicial de invitado.",
                    },
                    {
                        "usuario_id": "usr-004",
                        "accion": "desactivacion",
                        "fecha": _ts("2026-04-01T12:00:00Z"),
                        "detalle": "Cuenta desactivada temporalmente.",
                    },
                ],
            },
        )

    def clone(self) -> "SeededUsersState":
        return SeededUsersState(
            users=deepcopy(self.users),
            history=deepcopy(self.history),
        )

    def user_rows(self) -> list[dict[str, Any]]:
        rows = [deepcopy(record) for record in self.users.values()]
        rows.sort(key=lambda row: (row["apellidos"].lower(), row["nombre"].lower(), row["email"].lower(), row["id"]))
        return rows

    def history_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for user_id, items in self.history.items():
            for item in items:
                rows.append(deepcopy(item))
        rows.sort(key=lambda row: (row["usuario_id"], row["fecha"], row["accion"]))
        return rows

    def insert_user(self, params: tuple[Any, ...]) -> None:
        (
            user_id,
            nombre,
            apellidos,
            email,
            rol_principal,
            estado,
            fecha_alta,
            ultimo_acceso,
            invitacion_pendiente,
        ) = params
        if user_id in self.users:
            raise AssertionError("user id already exists in test state")
        if any(record["email"] == email for record in self.users.values()):
            raise AssertionError("email already exists in test state")
        self.users[str(user_id)] = {
            "id": str(user_id),
            "nombre": str(nombre),
            "apellidos": str(apellidos),
            "email": str(email),
            "rol_principal": str(rol_principal),
            "estado": str(estado),
            "fecha_alta": fecha_alta,
            "ultimo_acceso": ultimo_acceso,
            "invitacion_pendiente": bool(invitacion_pendiente),
        }

    def update_user(self, params: tuple[Any, ...]) -> None:
        (
            nombre,
            apellidos,
            email,
            rol_principal,
            estado,
            ultimo_acceso,
            invitacion_pendiente,
            user_id,
        ) = params
        record = self.users[str(user_id)]
        record.update(
            {
                "nombre": str(nombre),
                "apellidos": str(apellidos),
                "email": str(email),
                "rol_principal": str(rol_principal),
                "estado": str(estado),
                "ultimo_acceso": ultimo_acceso,
                "invitacion_pendiente": bool(invitacion_pendiente),
            }
        )

    def insert_history(self, params: tuple[Any, ...]) -> None:
        user_id, accion, fecha, detalle = params
        self.history.setdefault(str(user_id), []).append(
            {
                "usuario_id": str(user_id),
                "accion": str(accion),
                "fecha": fecha,
                "detalle": str(detalle),
            }
        )

    def select_user(self, user_id: str) -> dict[str, Any] | None:
        record = self.users.get(str(user_id))
        return deepcopy(record) if record is not None else None


class _FakeCursor:
    def __init__(self, state: SeededUsersState):
        self.state = state
        self.rows: list[dict[str, Any]] = []

    def execute(self, sql, params=None):
        normalized = str(sql).strip()
        if normalized == users_module.USERS_SELECT_SQL.strip():
            self.rows = self.state.user_rows()
            return
        if normalized == users_module.USER_HISTORY_SELECT_SQL.strip():
            self.rows = self.state.history_rows()
            return
        if normalized == users_module.USER_INSERT_SQL.strip():
            self.state.insert_user(params)
            self.rows = []
            return
        if normalized == users_module.USER_UPDATE_SQL.strip():
            self.state.update_user(params)
            self.rows = []
            return
        if normalized == users_module.USER_INSERT_HISTORY_SQL.strip():
            self.state.insert_history(params)
            self.rows = []
            return
        if normalized == users_module.USER_SCHEMA_BOOTSTRAP_SQL.strip():
            self.rows = []
            return
        raise AssertionError(f"SQL inesperado en prueba: {normalized}")

    def fetchall(self):
        return self.rows

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConnection:
    def __init__(self, state: SeededUsersState):
        self.state = state

    def cursor(self, cursor_factory=None):
        return _FakeCursor(self.state)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def fake_users_connect(state: SeededUsersState | None = None):
    return _FakeConnection(state or SeededUsersState.seed())
