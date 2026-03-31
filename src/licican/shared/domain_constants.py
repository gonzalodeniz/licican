from __future__ import annotations


CANARIAS_KEYWORDS = (
    "canarias",
    "gran canaria",
    "tenerife",
    "fuerteventura",
    "lanzarote",
    "la palma",
    "la gomera",
    "el hierro",
    "la graciosa",
    "santa cruz de tenerife",
    "las palmas",
)
TI_CPV_PREFIXES = ("72", "48", "302")
STATUS_LABELS = {
    "ADJ": "Adjudicada",
    "AN": "Anulada",
    "DES": "Desierta",
    "EV": "En evaluacion",
    "PUB": "Publicada",
    "RES": "Resuelta",
}
PROCEDURE_LABELS = {
    "1": "Abierto",
    "9": "Abierto simplificado",
}


def map_status(value: str | None) -> str:
    """Mapea el estado oficial a una etiqueta visible."""
    if value is None:
        return "No informado"
    normalized = value.strip()
    return STATUS_LABELS.get(normalized, normalized)


def map_procedure(value: str | None) -> str | None:
    """Mapea el procedimiento oficial a una etiqueta visible."""
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    return PROCEDURE_LABELS.get(normalized, f"Procedimiento {normalized}")
