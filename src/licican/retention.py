from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

from licican.config import resolve_database_url
from licican.pipeline import DEFAULT_PIPELINE_PATH, SavedPipelineEntry, load_pipeline
from licican.shared.text import slugify


DEFAULT_REFERENCE = "PB-015 · HU-15 · CU-15 · Panel de control de conservacion y archivado"
DEFAULT_RETENTION_DAYS = 180
RETENTION_MODE_FROM_CREATION = "desde_creacion"
RETENTION_MODE_CLOSED = "cerradas"
RETENTION_MODES = (RETENTION_MODE_FROM_CREATION, RETENTION_MODE_CLOSED)
ACTIVE_PIPELINE_STATES = {"Nueva", "Evaluando", "Preparando oferta", "Presentada"}
CLOSED_STATUSES = {"ADJ", "AN", "DES", "RES"}

RETENTION_SCHEMA_BOOTSTRAP_SQL = """
CREATE TABLE IF NOT EXISTS licitacion_retencion_config (
    id                  SMALLINT    NOT NULL PRIMARY KEY,
    antiguedad_dias     INTEGER     NOT NULL CHECK (antiguedad_dias > 0),
    modo                TEXT        NOT NULL CHECK (modo IN ('desde_creacion', 'cerradas')),
    actualizada_en      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT licitacion_retencion_config_singleton_ck CHECK (id = 1)
);
INSERT INTO licitacion_retencion_config (id, antiguedad_dias, modo, actualizada_en)
VALUES (1, 180, 'desde_creacion', NOW())
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS licitacion_archivada (
    LIKE licitacion INCLUDING ALL
);
ALTER TABLE licitacion_archivada ADD COLUMN IF NOT EXISTS archivada_en TIMESTAMPTZ NOT NULL DEFAULT NOW();
ALTER TABLE licitacion_archivada ADD COLUMN IF NOT EXISTS motivo_archivado TEXT NOT NULL DEFAULT 'politica_conservacion';
ALTER TABLE licitacion_archivada ADD COLUMN IF NOT EXISTS politica_modo TEXT;
ALTER TABLE licitacion_archivada ADD COLUMN IF NOT EXISTS politica_antiguedad_dias INTEGER;
CREATE INDEX IF NOT EXISTS idx_licitacion_archivada_archivada_en ON licitacion_archivada (archivada_en DESC);
"""

RETENTION_POLICY_SELECT_SQL = """
SELECT antiguedad_dias, modo, actualizada_en
FROM licitacion_retencion_config
WHERE id = 1
"""

RETENTION_POLICY_UPSERT_SQL = """
INSERT INTO licitacion_retencion_config (id, antiguedad_dias, modo, actualizada_en)
VALUES (1, %s, %s, NOW())
ON CONFLICT (id) DO UPDATE
SET antiguedad_dias = EXCLUDED.antiguedad_dias,
    modo = EXCLUDED.modo,
    actualizada_en = EXCLUDED.actualizada_en
RETURNING antiguedad_dias, modo, actualizada_en
"""

RETENTION_RECORDS_SELECT_SQL = """
SELECT
    id_plataforma,
    expediente,
    titulo,
    organo_contratacion,
    estado,
    fecha_importacion,
    updated_at
FROM licitacion
ORDER BY updated_at DESC, id_plataforma
"""

ARCHIVED_COUNT_SQL = """
SELECT COUNT(*) AS total
FROM licitacion_archivada
"""

ARCHIVE_RECORDS_INSERT_SQL = """
INSERT INTO licitacion_archivada
SELECT
    licitacion.*,
    NOW(),
    %s,
    %s,
    %s
FROM licitacion
WHERE id_plataforma = ANY(%s)
ON CONFLICT (id_plataforma) DO NOTHING
"""

ARCHIVE_RECORDS_DELETE_SQL = """
DELETE FROM licitacion
WHERE id_plataforma = ANY(%s)
"""

_SCHEMA_BOOTSTRAPPED = False


@dataclass(frozen=True)
class RetentionPolicy:
    antiguedad_dias: int
    modo: str
    actualizada_en: str | None

    @property
    def modo_label(self) -> str:
        if self.modo == RETENTION_MODE_CLOSED:
            return "Antiguedad de licitaciones cerradas"
        return "Dias desde la creacion"

    def to_payload(self) -> dict[str, object]:
        return {
            "antiguedad_dias": self.antiguedad_dias,
            "modo": self.modo,
            "modo_label": self.modo_label,
            "actualizada_en": self.actualizada_en,
        }


class RetentionDatabaseError(RuntimeError):
    pass


def _connect():
    try:
        return psycopg2.connect(resolve_database_url())
    except psycopg2.Error as exc:
        raise RetentionDatabaseError("No se pudo consultar PostgreSQL para gestionar la conservacion.") from exc


def _ensure_schema(connection) -> None:
    global _SCHEMA_BOOTSTRAPPED
    if _SCHEMA_BOOTSTRAPPED:
        return
    with connection.cursor() as cursor:
        cursor.execute(RETENTION_SCHEMA_BOOTSTRAP_SQL)
    _SCHEMA_BOOTSTRAPPED = True


def _format_timestamp(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or None
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        cleaned = value.strip().replace("Z", "+00:00")
        if not cleaned:
            return None
        parsed = datetime.fromisoformat(cleaned)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(microsecond=0)


def _load_policy_row(cursor) -> RetentionPolicy:
    cursor.execute(RETENTION_POLICY_SELECT_SQL)
    row = cursor.fetchone()
    if row is None:
        return RetentionPolicy(DEFAULT_RETENTION_DAYS, RETENTION_MODE_FROM_CREATION, None)
    return RetentionPolicy(
        antiguedad_dias=int(row.get("antiguedad_dias") or DEFAULT_RETENTION_DAYS),
        modo=str(row.get("modo") or RETENTION_MODE_FROM_CREATION),
        actualizada_en=_format_timestamp(row.get("actualizada_en")),
    )


def _validate_policy(antiguedad_dias: int, modo: str) -> tuple[int, str]:
    if antiguedad_dias <= 0:
        raise ValueError("La antiguedad de conservacion debe ser un entero positivo.")
    normalized_mode = modo.strip().lower()
    if normalized_mode not in RETENTION_MODES:
        raise ValueError("El modo de conservacion indicado no es valido.")
    return antiguedad_dias, normalized_mode


def load_retention_policy() -> RetentionPolicy:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                return _load_policy_row(cursor)
    except psycopg2.Error as exc:
        raise RetentionDatabaseError("No se pudo consultar PostgreSQL para gestionar la conservacion.") from exc


def update_retention_policy(*, antiguedad_dias: int, modo: str) -> RetentionPolicy:
    antiguedad_dias, modo = _validate_policy(antiguedad_dias, modo)
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(RETENTION_POLICY_UPSERT_SQL, (antiguedad_dias, modo))
                row = cursor.fetchone()
    except psycopg2.Error as exc:
        raise RetentionDatabaseError("No se pudo guardar la politica de conservacion en PostgreSQL.") from exc
    assert row is not None
    return RetentionPolicy(
        antiguedad_dias=int(row["antiguedad_dias"]),
        modo=str(row["modo"]),
        actualizada_en=_format_timestamp(row.get("actualizada_en")),
    )


def _record_slug(row: dict[str, object]) -> str:
    expediente = str(row.get("expediente") or "").strip()
    if expediente:
        return slugify(expediente)
    return slugify(str(row.get("id_plataforma") or ""))


def _tracked_sets(entries: list[SavedPipelineEntry]) -> tuple[set[str], set[str]]:
    tracked_ids = {entry.opportunity_id for entry in entries}
    active_ids = {
        entry.opportunity_id
        for entry in entries
        if entry.estado_seguimiento in ACTIVE_PIPELINE_STATES
    }
    return tracked_ids, active_ids


def _age_reference(row: dict[str, object], policy: RetentionPolicy) -> datetime | None:
    raw_status = str(row.get("estado") or "").strip().upper()
    if policy.modo == RETENTION_MODE_CLOSED:
        if raw_status not in CLOSED_STATUSES:
            return None
        return _parse_timestamp(row.get("updated_at"))
    return _parse_timestamp(row.get("fecha_importacion")) or _parse_timestamp(row.get("updated_at"))


def _classification_for_row(
    row: dict[str, object],
    policy: RetentionPolicy,
    threshold: datetime,
    now: datetime,
    tracked_ids: set[str],
    active_ids: set[str],
) -> tuple[str, dict[str, object]]:
    slug = _record_slug(row)
    raw_status = str(row.get("estado") or "").strip().upper()
    age_reference = _age_reference(row, policy)
    active_tracking = slug in active_ids
    tracked = slug in tracked_ids
    expired = age_reference is not None and age_reference <= threshold
    closed = raw_status in CLOSED_STATUSES

    if active_tracking and not closed:
        destination = "mantener_activas"
    elif closed and expired:
        destination = "archivar"
    else:
        destination = "conservar"

    item = {
        "id_plataforma": str(row.get("id_plataforma") or ""),
        "expediente": str(row.get("expediente") or row.get("id_plataforma") or ""),
        "slug": slug,
        "titulo": str(row.get("titulo") or row.get("expediente") or row.get("id_plataforma") or ""),
        "organismo": str(row.get("organo_contratacion") or "No informado"),
        "estado": raw_status or "No informado",
        "seguimiento_activo": active_tracking,
        "tuvo_seguimiento": tracked,
        "fecha_referencia": _format_timestamp(age_reference),
        "dias_antiguedad": None if age_reference is None else max((now - age_reference).days, 0),
        "motivo": _destination_reason(destination, policy, active_tracking, tracked),
    }
    return destination, item


def _destination_reason(destination: str, policy: RetentionPolicy, active_tracking: bool, tracked: bool) -> str:
    if destination == "mantener_activas":
        return "Mantiene seguimiento activo y permanece operativa aunque supere el umbral."
    if destination == "archivar":
        if tracked:
            return f"Supera la politica de {policy.modo_label.lower()} y conserva trazabilidad historica en archivo."
        return f"Supera la politica de {policy.modo_label.lower()} y deja de estar en la tabla operativa."
    return "Sigue dentro del horizonte operativo configurado o todavia no es archivable."


def _load_preview_groups(
    rows: list[dict[str, object]],
    policy: RetentionPolicy,
    pipeline_path: Path,
    now: datetime | None = None,
) -> dict[str, list[dict[str, object]]]:
    now = now or datetime.now(timezone.utc).replace(microsecond=0)
    threshold = now - timedelta(days=policy.antiguedad_dias)
    _, entries = load_pipeline(pipeline_path)
    tracked_ids, active_ids = _tracked_sets(entries)
    groups = {"conservar": [], "archivar": [], "mantener_activas": []}

    for row in rows:
        destination, item = _classification_for_row(row, policy, threshold, now, tracked_ids, active_ids)
        groups[destination].append(item)

    for items in groups.values():
        items.sort(
            key=lambda item: (
                999999 if item["dias_antiguedad"] is None else -int(item["dias_antiguedad"]),
                str(item["expediente"]),
            )
        )
    return groups


def _summary(groups: dict[str, list[dict[str, object]]], archived_total: int) -> dict[str, int]:
    return {
        "conservar": len(groups["conservar"]),
        "archivar": len(groups["archivar"]),
        "mantener_activas": len(groups["mantener_activas"]),
        "archivadas_existentes": archived_total,
        "total_operativas": sum(len(items) for items in groups.values()),
    }


def build_retention_payload(
    *,
    pipeline_path: Path = DEFAULT_PIPELINE_PATH,
    now: datetime | None = None,
) -> dict[str, object]:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                policy = _load_policy_row(cursor)
                cursor.execute(RETENTION_RECORDS_SELECT_SQL)
                rows = list(cursor.fetchall())
                cursor.execute(ARCHIVED_COUNT_SQL)
                archived_count_row = cursor.fetchone() or {"total": 0}
    except psycopg2.Error as exc:
        raise RetentionDatabaseError("No se pudo consultar PostgreSQL para gestionar la conservacion.") from exc

    groups = _load_preview_groups(rows, policy, pipeline_path, now=now)
    archived_total = int(archived_count_row.get("total") or 0)
    return {
        "referencia_funcional": DEFAULT_REFERENCE,
        "politica": policy.to_payload(),
        "resumen": _summary(groups, archived_total),
        "grupos": groups,
        "modos_disponibles": [
            {"valor": RETENTION_MODE_FROM_CREATION, "etiqueta": "Dias desde la creacion"},
            {"valor": RETENTION_MODE_CLOSED, "etiqueta": "Antiguedad de licitaciones cerradas"},
        ],
    }


def apply_retention_policy(
    *,
    pipeline_path: Path = DEFAULT_PIPELINE_PATH,
    now: datetime | None = None,
) -> dict[str, object]:
    try:
        with _connect() as connection:
            _ensure_schema(connection)
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                policy = _load_policy_row(cursor)
                cursor.execute(RETENTION_RECORDS_SELECT_SQL)
                rows = list(cursor.fetchall())
                groups = _load_preview_groups(rows, policy, pipeline_path, now=now)
                candidate_ids = [item["id_plataforma"] for item in groups["archivar"]]
                if candidate_ids:
                    cursor.execute(
                        ARCHIVE_RECORDS_INSERT_SQL,
                        ("politica_conservacion", policy.modo, policy.antiguedad_dias, candidate_ids),
                    )
                    cursor.execute(ARCHIVE_RECORDS_DELETE_SQL, (candidate_ids,))
                    archived = cursor.rowcount
                else:
                    archived = 0
    except psycopg2.Error as exc:
        raise RetentionDatabaseError("No se pudo aplicar la politica de conservacion sobre PostgreSQL.") from exc

    return {
        "archivadas": archived,
        "candidatas": len(groups["archivar"]),
        "politica": policy.to_payload(),
    }
