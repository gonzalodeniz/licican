from __future__ import annotations

import unicodedata
from datetime import datetime, date, timezone


def normalize_text(value: str) -> str:
    """Normaliza texto a ASCII, minúsculas y sin espacios extremos."""
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def slugify(value: str) -> str:
    """Genera un slug alfanumérico separado por guiones."""
    normalized = normalize_text(value)
    chunks: list[str] = []
    current: list[str] = []
    for char in normalized:
        if char.isalnum():
            current.append(char)
            continue
        if current:
            chunks.append("".join(current))
            current = []
    if current:
        chunks.append("".join(current))
    return "-".join(chunks) or "expediente-sin-id"


def clean_text(value: str | None) -> str | None:
    """Limpia espacios repetidos y extremos conservando nulos."""
    if value is None:
        return None
    cleaned = " ".join(value.split())
    return cleaned or None


def normalize_optional(value: str | None) -> str | None:
    """Normaliza texto opcional conservando nulos y vacíos."""
    cleaned = clean_text(value)
    if cleaned is None:
        return None
    return normalize_text(cleaned)


def format_iso_datetime(value: str | datetime | date | None) -> str | None:
    """Convierte un ISO 8601 con hora a `DD-MM-YYYY HH:MM`.

    Si el valor no es un ISO 8601 con componente temporal, se devuelve como texto
    sin modificar para no alterar otros formatos ya existentes.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value.astimezone(timezone.utc) if value.tzinfo is not None else value
        return dt.strftime("%d-%m-%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d-%m-%Y")

    cleaned = clean_text(value)
    if not cleaned:
        return cleaned
    if "T" not in cleaned:
        return cleaned

    try:
        parsed = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return cleaned
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc)
    return parsed.strftime("%d-%m-%Y %H:%M")
