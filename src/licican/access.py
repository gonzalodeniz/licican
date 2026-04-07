from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


ROLE_ADMINISTRATOR = "administrador"
ROLE_SUPERADMIN = "superadmin"
ROLE_MANAGER = "manager"
ROLE_COLLABORATOR = "colaborador"
ROLE_INVITED = "invitado"

# Compatibilidad temporal con nombres antiguos.
ROLE_ADMIN = ROLE_ADMINISTRATOR
ROLE_READER = ROLE_INVITED

DEFAULT_ROLE = ROLE_ADMINISTRATOR
DEFAULT_USER_IDS = {
    ROLE_ADMINISTRATOR: "administrador-demo",
    ROLE_SUPERADMIN: "superadmin-demo",
    ROLE_MANAGER: "manager-demo",
    ROLE_COLLABORATOR: "colaborador-demo",
    ROLE_INVITED: "invitado-demo",
}
ROLE_LABELS = {
    ROLE_ADMINISTRATOR: "Administrador",
    ROLE_SUPERADMIN: "Superadmin",
    ROLE_MANAGER: "Manager",
    ROLE_COLLABORATOR: "Colaborador",
    ROLE_INVITED: "Invitado",
}
CAPABILITY_MATRIX = {
    ROLE_ADMINISTRATOR: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "manage_alerts",
            "view_pipeline",
            "manage_pipeline",
            "view_permissions",
            "view_retention",
            "manage_retention",
            "view_users",
            "manage_users",
        }
    ),
    ROLE_SUPERADMIN: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "manage_alerts",
            "view_pipeline",
            "manage_pipeline",
            "view_permissions",
            "view_retention",
            "manage_retention",
            "view_users",
            "manage_users",
        }
    ),
    ROLE_MANAGER: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "manage_alerts",
            "view_pipeline",
            "manage_pipeline",
        }
    ),
    ROLE_COLLABORATOR: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "view_pipeline",
        }
    ),
    ROLE_INVITED: frozenset(
        {
            "view_catalog",
            "view_dataset",
        }
    ),
}


@dataclass(frozen=True)
class AccessContext:
    role: str
    role_label: str
    user_id: str
    capabilities: frozenset[str]
    csrf_token: str = ""
    display_name: str = ""
    is_superadmin: bool = False
    auto_login_active: bool = False

    @property
    def is_admin(self) -> bool:
        return self.role in {ROLE_ADMINISTRATOR, ROLE_SUPERADMIN}

    @property
    def is_manager(self) -> bool:
        return self.role == ROLE_MANAGER

    @property
    def scope_label(self) -> str:
        if self.is_admin:
            return "global"
        if self.is_manager:
            return "operativo"
        return "propio"


def _normalize_role(raw_role: str | None) -> str:
    normalized = (raw_role or "").strip().lower()
    aliases = {
        "admin": ROLE_ADMINISTRATOR,
        "administrador": ROLE_ADMINISTRATOR,
        "administrador de plataforma": ROLE_ADMINISTRATOR,
        "administrador funcional": ROLE_MANAGER,
        "responsable": ROLE_MANAGER,
        "superadmin": ROLE_SUPERADMIN,
        "super administrador": ROLE_SUPERADMIN,
        "manager": ROLE_MANAGER,
        "gestor": ROLE_MANAGER,
        "colaborador": ROLE_COLLABORATOR,
        "consultor": ROLE_COLLABORATOR,
        "lector": ROLE_INVITED,
        "lector/invitado": ROLE_INVITED,
        "invitado": ROLE_INVITED,
    }
    return aliases.get(normalized, DEFAULT_ROLE)


def resolve_access_context(
    environ: Mapping[str, object] | None = None,
    query: Mapping[str, list[str]] | None = None,
    session_user: Mapping[str, object] | None = None,
) -> AccessContext:
    if session_user is not None and session_user.get("username"):
        role = _normalize_role(str(session_user.get("rol")))
        username = str(session_user.get("username") or DEFAULT_USER_IDS[role]).strip() or DEFAULT_USER_IDS[role]
        return AccessContext(
            role=role,
            role_label=ROLE_LABELS[role],
            user_id=username,
            capabilities=CAPABILITY_MATRIX[role],
            csrf_token=str(session_user.get("csrf_token") or ""),
            display_name=str(session_user.get("nombre_completo") or username),
            is_superadmin=bool(session_user.get("is_superadmin")),
            auto_login_active=bool(session_user.get("auto_login_active")),
        )

    query = query or {}
    query_role = next(iter(query.get("rol", [])), None)
    env_role = os.getenv("LICICAN_ROLE")
    role = _normalize_role(query_role or env_role)

    query_user_id = next(iter(query.get("usuario", [])), None)
    env_user_id = os.getenv("LICICAN_USER_ID")
    user_id = (query_user_id or env_user_id or DEFAULT_USER_IDS[role]).strip() or DEFAULT_USER_IDS[role]
    return AccessContext(
        role=role,
        role_label=ROLE_LABELS[role],
        user_id=user_id,
        capabilities=CAPABILITY_MATRIX[role],
        display_name=user_id,
    )


def has_capability(access_context: AccessContext, capability: str) -> bool:
    return capability in access_context.capabilities
