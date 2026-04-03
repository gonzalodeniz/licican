from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from functools import lru_cache

from licican.config import _ensure_env_loaded


LOGGER = logging.getLogger(__name__)
DEFAULT_SESSION_SECRET_KEY = "cambiar-en-produccion-por-valor-aleatorio-seguro"


def _parse_bool(raw_value: str | None, default: bool) -> bool:
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


@dataclass(frozen=True)
class AuthSettings:
    login_automatico: bool
    login_superadmin_enabled: bool
    login_superadmin_name: str
    login_superadmin_pass: str
    session_timeout_minutes: int
    session_secret_key: str
    session_cookie_name: str = "licican_session"
    session_cookie_secure: bool = False

    @property
    def automatic_login_effective(self) -> bool:
        return self.login_automatico and self.login_superadmin_enabled


@lru_cache(maxsize=1)
def get_auth_settings() -> AuthSettings:
    _ensure_env_loaded()
    login_automatico = _parse_bool(os.getenv("LOGIN_AUTOMATICO"), False)
    login_superadmin_enabled = _parse_bool(os.getenv("LOGIN_SUPERADMIN_ENABLED"), False)
    raw_timeout = (os.getenv("SESSION_TIMEOUT_MINUTES") or "30").strip()
    try:
        timeout_minutes = max(1, int(raw_timeout))
    except ValueError:
        LOGGER.warning("SESSION_TIMEOUT_MINUTES no es valido (%s). Se usa 30.", raw_timeout)
        timeout_minutes = 30

    settings = AuthSettings(
        login_automatico=login_automatico,
        login_superadmin_enabled=login_superadmin_enabled,
        login_superadmin_name=(os.getenv("LOGIN_SUPERADMIN_NAME") or "").strip(),
        login_superadmin_pass=os.getenv("LOGIN_SUPERADMIN_PASS") or "",
        session_timeout_minutes=timeout_minutes,
        session_secret_key=(os.getenv("SESSION_SECRET_KEY") or DEFAULT_SESSION_SECRET_KEY).strip() or DEFAULT_SESSION_SECRET_KEY,
        session_cookie_secure=_parse_bool(os.getenv("SESSION_COOKIE_SECURE"), False),
    )
    _log_configuration_warnings(settings)
    return settings


def _log_configuration_warnings(settings: AuthSettings) -> None:
    if settings.login_automatico and not settings.login_superadmin_enabled:
        LOGGER.warning(
            "LOGIN_AUTOMATICO=true pero LOGIN_SUPERADMIN_ENABLED=false. Se desactiva el login automatico."
        )
    if settings.login_superadmin_enabled and len(settings.login_superadmin_pass) < 8:
        LOGGER.warning("La contraseña del superadmin es débil.")
    if settings.session_secret_key == DEFAULT_SESSION_SECRET_KEY:
        LOGGER.warning("Cambie SESSION_SECRET_KEY en producción.")
    mode = "automático" if settings.automatic_login_effective else "manual"
    LOGGER.info("Modo login: %s", mode)
