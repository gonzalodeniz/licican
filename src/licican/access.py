from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


ROLE_ADMIN = "administrador"
ROLE_COLLABORATOR = "colaborador"
ROLE_READER = "lector"

DEFAULT_ROLE = ROLE_ADMIN
DEFAULT_USER_IDS = {
    ROLE_ADMIN: "administrador-demo",
    ROLE_COLLABORATOR: "colaborador-demo",
    ROLE_READER: "lector-demo",
}
ROLE_LABELS = {
    ROLE_ADMIN: "Administrador",
    ROLE_COLLABORATOR: "Colaborador",
    ROLE_READER: "Lector/Invitado",
}
CAPABILITY_MATRIX = {
    ROLE_ADMIN: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "manage_alerts",
            "view_pipeline",
            "manage_pipeline",
            "view_kpis",
            "view_permissions",
        }
    ),
    ROLE_COLLABORATOR: frozenset(
        {
            "view_catalog",
            "view_dataset",
            "view_alerts",
            "manage_alerts",
            "view_pipeline",
            "manage_pipeline",
            "view_kpis",
        }
    ),
    ROLE_READER: frozenset(
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

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    @property
    def scope_label(self) -> str:
        return "global" if self.is_admin else "propio"


def _normalize_role(raw_role: str | None) -> str:
    normalized = (raw_role or "").strip().lower()
    aliases = {
        "admin": ROLE_ADMIN,
        "administrador": ROLE_ADMIN,
        "colaborador": ROLE_COLLABORATOR,
        "lector": ROLE_READER,
        "lector/invitado": ROLE_READER,
        "invitado": ROLE_READER,
    }
    return aliases.get(normalized, DEFAULT_ROLE)


def resolve_access_context(
    environ: Mapping[str, object] | None = None,
    query: Mapping[str, list[str]] | None = None,
) -> AccessContext:
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
    )


def has_capability(access_context: AccessContext, capability: str) -> bool:
    return capability in access_context.capabilities
