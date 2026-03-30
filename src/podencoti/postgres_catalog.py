from __future__ import annotations

import os
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor


REFERENCE = "T-001 · Carga de datos desde PostgreSQL para la aplicacion"
SOURCE_NAME = "Plataforma de Contratación del Sector Público filtrada por órganos de Canarias"
SOURCE_URL = "https://contrataciondelestado.es/"
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

CATALOG_SQL = """
WITH latest AS (
    SELECT DISTINCT ON (COALESCE(NULLIF(expediente, ''), id_plataforma))
        COALESCE(NULLIF(expediente, ''), id_plataforma) AS expediente_id,
        id_plataforma,
        titulo,
        resumen,
        organo_contratacion,
        ubicacion_comunidad,
        ubicacion_nuts,
        procedimiento,
        COALESCE(importe_total, importe_sin_impuestos, importe_estimado, contrato_importe_total) AS presupuesto_base,
        updated_at,
        fecha_limite_presentacion,
        estado,
        organo_perfil_url,
        link_detalle,
        cpv_codes,
        fichero_origen,
        jerarquia_org
    FROM licitacion
    WHERE COALESCE(anulada, FALSE) = FALSE
      AND cpv_codes IS NOT NULL
      AND EXISTS (
          SELECT 1
          FROM unnest(cpv_codes) AS cpv
          WHERE cpv LIKE '72%%' OR cpv LIKE '48%%' OR cpv LIKE '302%%'
      )
      AND (
          COALESCE(ubicacion_nuts, '') LIKE 'ES7%%'
          OR lower(COALESCE(ubicacion_comunidad, '')) LIKE ANY (%(keyword_patterns)s)
          OR EXISTS (
              SELECT 1
              FROM unnest(COALESCE(jerarquia_org, ARRAY[]::text[])) AS node
              WHERE lower(node) LIKE ANY (%(keyword_patterns)s)
          )
      )
    ORDER BY COALESCE(NULLIF(expediente, ''), id_plataforma), updated_at DESC, COALESCE(fichero_origen, '') DESC
)
SELECT
    expediente_id,
    id_plataforma,
    titulo,
    resumen,
    organo_contratacion,
    ubicacion_comunidad,
    ubicacion_nuts,
    procedimiento,
    presupuesto_base,
    updated_at,
    fecha_limite_presentacion,
    estado,
    organo_perfil_url,
    link_detalle,
    cpv_codes,
    fichero_origen,
    jerarquia_org
FROM latest
ORDER BY fecha_limite_presentacion NULLS LAST, updated_at, expediente_id
"""


class PostgresCatalogError(RuntimeError):
    pass


@dataclass(frozen=True)
class PostgresCatalogConfig:
    database_url: str


def load_postgres_opportunity_records() -> tuple[str, list[dict[str, Any]]]:
    config = PostgresCatalogConfig(database_url=_resolve_database_url())
    keyword_patterns = [f"%{keyword}%" for keyword in CANARIAS_KEYWORDS]

    try:
        with psycopg2.connect(config.database_url) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(CATALOG_SQL, {"keyword_patterns": keyword_patterns})
                rows = cursor.fetchall()
    except psycopg2.Error as exc:
        raise PostgresCatalogError("No se pudo consultar PostgreSQL para cargar el catalogo.") from exc

    return REFERENCE, [_row_to_record(row) for row in rows]


def _resolve_database_url() -> str:
    explicit_url = os.getenv("PODENCOTI_DATABASE_URL") or os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "15432")
    database = os.getenv("DB_NAME", "licitaciones")
    user = os.getenv("DB_USER", "licitaciones_admin")
    password = os.getenv("DB_PASSWORD", "Lic1t4c10n3s_2026!")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def _row_to_record(row: dict[str, Any]) -> dict[str, Any]:
    expediente_id = str(row["expediente_id"])
    titulo = str(row.get("titulo") or expediente_id).strip()
    descripcion = str(row.get("resumen") or titulo).strip()
    ubicacion = _resolve_location_label(
        row.get("ubicacion_comunidad"),
        row.get("ubicacion_nuts"),
        row.get("jerarquia_org") or (),
    )

    return {
        "id": _slugify(expediente_id),
        "titulo": titulo,
        "descripcion": descripcion,
        "organismo": str(row.get("organo_contratacion") or "No informado").strip(),
        "ubicacion": ubicacion,
        "procedimiento": _map_procedure(row.get("procedimiento")),
        "presupuesto": _parse_budget(row.get("presupuesto_base")),
        "fecha_publicacion_oficial": _iso_date(row.get("updated_at")) or "No informado",
        "fecha_limite": _iso_date(row.get("fecha_limite_presentacion")) or "No informado",
        "estado": _map_status(row.get("estado")),
        "solvencia_tecnica": None,
        "criterios_adjudicacion": (),
        "fuente_oficial": SOURCE_NAME,
        "url_fuente_oficial": str(row.get("link_detalle") or row.get("organo_perfil_url") or SOURCE_URL),
        "cpvs": tuple(row.get("cpv_codes") or ()),
        "actualizaciones_oficiales": (),
        "fichero_origen_atom": row.get("fichero_origen"),
    }


def _resolve_location_label(
    comunidad: str | None,
    nuts_code: str | None,
    hierarchy: tuple[str, ...] | list[str],
) -> str:
    if comunidad and comunidad.strip():
        return comunidad.strip()
    if nuts_code and str(nuts_code).startswith("ES7"):
        return "Canarias"
    for item in hierarchy:
        normalized = _normalize_text(str(item))
        if any(keyword in normalized for keyword in CANARIAS_KEYWORDS):
            return str(item).strip()
    return "Canarias"


def _map_status(value: Any) -> str:
    if value is None:
        return "No informado"
    normalized = str(value).strip()
    return STATUS_LABELS.get(normalized, normalized)


def _map_procedure(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    return PROCEDURE_LABELS.get(normalized, f"Procedimiento {normalized}")


def _parse_budget(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return round(float(value))
    except (TypeError, ValueError):
        return None


def _iso_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def _slugify(value: str) -> str:
    normalized = _normalize_text(value)
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
