from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
_DEFAULT_ENV_PATH = BASE_DIR / ".env"
_ENV_LOADED = False


def load_env_file(path: Path) -> None:
    """Carga un fichero .env una sola vez por proceso."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    if path.is_file():
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            os.environ[key] = value

    _ENV_LOADED = True


def _ensure_env_loaded() -> None:
    if not _ENV_LOADED:
        load_env_file(_DEFAULT_ENV_PATH)


def normalize_base_path(raw: str | None) -> str:
    """Normaliza el prefijo base de despliegue de la aplicación."""
    if raw is None:
        return ""

    base_path = raw.strip()
    if not base_path or base_path == "/":
        return ""

    if not base_path.startswith("/"):
        base_path = f"/{base_path}"

    if len(base_path) > 1:
        base_path = base_path.rstrip("/")

    return base_path or ""


def resolve_base_path() -> str:
    """Resuelve el `BASE_PATH` efectivo."""
    _ensure_env_loaded()
    return normalize_base_path(os.environ.get("BASE_PATH", "/licican"))


def resolve_port() -> int:
    """Resuelve el puerto HTTP configurado."""
    _ensure_env_loaded()
    raw_port = os.environ.get("PORT", "8000").strip()
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError(f"PORT debe ser un numero entero valido, no {raw_port!r}") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"PORT debe estar entre 1 y 65535, no {port}")
    return port


def resolve_host() -> str:
    """Resuelve el host HTTP configurado."""
    _ensure_env_loaded()
    raw_host = os.environ.get("HOST", "127.0.0.1").strip()
    return raw_host or "127.0.0.1"


def resolve_alerts_path() -> Path:
    """Resuelve la ruta del almacén de alertas."""
    _ensure_env_loaded()
    raw_path = os.environ.get("LICICAN_ALERTS_PATH", "").strip()
    if raw_path:
        return Path(raw_path)
    return BASE_DIR / "data" / "alerts.json"


def resolve_pipeline_path() -> Path:
    """Resuelve la ruta del almacén del pipeline."""
    _ensure_env_loaded()
    raw_path = os.environ.get("LICICAN_PIPELINE_PATH", "").strip()
    if raw_path:
        return Path(raw_path)
    return BASE_DIR / "data" / "pipeline.json"


def resolve_users_path() -> Path:
    """Resuelve la ruta del almacén de usuarios."""
    _ensure_env_loaded()
    raw_path = os.environ.get("LICICAN_USERS_PATH", "").strip()
    if raw_path:
        return Path(raw_path)
    return BASE_DIR / "data" / "users.json"
