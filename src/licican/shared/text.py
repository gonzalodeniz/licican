from __future__ import annotations

import unicodedata


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
