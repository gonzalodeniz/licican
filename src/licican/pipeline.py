from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from licican.config import BASE_DIR
from licican.opportunity_catalog import CatalogDataSourceError, DEFAULT_DATA_PATH, build_opportunity_detail


DEFAULT_PIPELINE_PATH = BASE_DIR / "data" / "pipeline.json"
DEFAULT_REFERENCE = "PB-005 · HU-05 · CU-05 · Pipeline funcional de seguimiento de oportunidades"
DEFAULT_USER_ID = "usuario-demo"
PIPELINE_STATES = ("Nueva", "Evaluando", "Preparando oferta", "Presentada", "Descartada")
OFFICIAL_WARNING_STATES = {"anulada", "desierta", "desistida"}


@dataclass(frozen=True)
class PipelineSnapshot:
    id: str
    titulo: str
    organismo: str
    ubicacion: str
    procedimiento: str | None
    presupuesto: int | None
    fecha_publicacion_oficial: str
    fecha_limite: str
    estado_oficial: str
    fuente_oficial: str
    url_fuente_oficial: str


@dataclass(frozen=True)
class SavedPipelineEntry:
    opportunity_id: str
    usuario_id: str
    estado_seguimiento: str
    creada_en: str
    actualizada_en: str
    oportunidad: PipelineSnapshot

    def to_payload(self) -> dict[str, object]:
        return {
            "opportunity_id": self.opportunity_id,
            "usuario_id": self.usuario_id,
            "estado_seguimiento": self.estado_seguimiento,
            "creada_en": self.creada_en,
            "actualizada_en": self.actualizada_en,
            "oportunidad": self.oportunidad.__dict__,
        }


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _snapshot_from_detail(detail: dict[str, object]) -> PipelineSnapshot:
    return PipelineSnapshot(
        id=str(detail["id"]),
        titulo=str(detail["titulo"]),
        organismo=str(detail["organismo"]),
        ubicacion=str(detail["ubicacion"]),
        procedimiento=None if detail.get("procedimiento") is None else str(detail.get("procedimiento")),
        presupuesto=None if detail.get("presupuesto") is None else int(detail["presupuesto"]),
        fecha_publicacion_oficial=str(detail["fecha_publicacion_oficial"]),
        fecha_limite=str(detail["fecha_limite"]),
        estado_oficial=str(detail["estado"]),
        fuente_oficial=str(detail["fuente_oficial"]),
        url_fuente_oficial=str(detail["url_fuente_oficial"]),
    )


def _entry_from_payload(payload: dict[str, object]) -> SavedPipelineEntry:
    opportunity = dict(payload.get("oportunidad") or {})
    return SavedPipelineEntry(
        opportunity_id=str(payload["opportunity_id"]),
        usuario_id=str(payload.get("usuario_id") or DEFAULT_USER_ID),
        estado_seguimiento=str(payload.get("estado_seguimiento") or "Nueva"),
        creada_en=str(payload["creada_en"]),
        actualizada_en=str(payload.get("actualizada_en") or payload["creada_en"]),
        oportunidad=PipelineSnapshot(
            id=str(opportunity["id"]),
            titulo=str(opportunity["titulo"]),
            organismo=str(opportunity["organismo"]),
            ubicacion=str(opportunity["ubicacion"]),
            procedimiento=None if opportunity.get("procedimiento") is None else str(opportunity.get("procedimiento")),
            presupuesto=None if opportunity.get("presupuesto") is None else int(opportunity["presupuesto"]),
            fecha_publicacion_oficial=str(opportunity["fecha_publicacion_oficial"]),
            fecha_limite=str(opportunity["fecha_limite"]),
            estado_oficial=str(opportunity["estado_oficial"]),
            fuente_oficial=str(opportunity["fuente_oficial"]),
            url_fuente_oficial=str(opportunity["url_fuente_oficial"]),
        ),
    )


def load_pipeline(path: Path = DEFAULT_PIPELINE_PATH) -> tuple[str, list[SavedPipelineEntry]]:
    if not path.is_file():
        return DEFAULT_REFERENCE, []

    payload = json.loads(path.read_text(encoding="utf-8"))
    reference = str(payload.get("referencia_funcional") or DEFAULT_REFERENCE)
    entries = [_entry_from_payload(item) for item in payload.get("pipeline", [])]
    return reference, entries


def _save_pipeline(reference: str, entries: list[SavedPipelineEntry], path: Path) -> None:
    payload = {
        "referencia_funcional": reference,
        "pipeline": [entry.to_payload() for entry in entries],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_detail_snapshot(opportunity_id: str, catalog_path: Path = DEFAULT_DATA_PATH) -> PipelineSnapshot | None:
    backend = "file" if catalog_path != DEFAULT_DATA_PATH else None
    try:
        detail = build_opportunity_detail(opportunity_id, path=catalog_path, backend=backend)
    except CatalogDataSourceError:
        return None
    if detail is None:
        return None
    return _snapshot_from_detail(detail)


def validate_pipeline_state(state: str) -> str | None:
    normalized = state.strip()
    if normalized in PIPELINE_STATES:
        return None
    return "El estado de seguimiento indicado no es valido para el pipeline."


def add_opportunity_to_pipeline(
    opportunity_id: str,
    path: Path = DEFAULT_PIPELINE_PATH,
    catalog_path: Path = DEFAULT_DATA_PATH,
    now: str | None = None,
    usuario_id: str = DEFAULT_USER_ID,
) -> tuple[SavedPipelineEntry, bool]:
    if not opportunity_id.strip():
        raise ValueError("La oportunidad indicada no es valida para el pipeline.")

    reference, entries = load_pipeline(path)
    for entry in entries:
        if entry.opportunity_id == opportunity_id and entry.usuario_id == usuario_id:
            return entry, False

    snapshot = _load_detail_snapshot(opportunity_id, catalog_path)
    if snapshot is None:
        raise KeyError(opportunity_id)

    timestamp = now or _current_timestamp()
    entry = SavedPipelineEntry(
        opportunity_id=opportunity_id,
        usuario_id=usuario_id,
        estado_seguimiento="Nueva",
        creada_en=timestamp,
        actualizada_en=timestamp,
        oportunidad=snapshot,
    )
    entries.append(entry)
    _save_pipeline(reference, entries, path)
    return entry, True


def update_pipeline_entry_status(
    opportunity_id: str,
    state: str,
    path: Path = DEFAULT_PIPELINE_PATH,
    now: str | None = None,
    usuario_id: str = DEFAULT_USER_ID,
) -> SavedPipelineEntry:
    validation_error = validate_pipeline_state(state)
    if validation_error is not None:
        raise ValueError(validation_error)

    reference, entries = load_pipeline(path)
    timestamp = now or _current_timestamp()
    for index, current_entry in enumerate(entries):
        if current_entry.opportunity_id != opportunity_id or current_entry.usuario_id != usuario_id:
            continue
        updated = SavedPipelineEntry(
            opportunity_id=current_entry.opportunity_id,
            usuario_id=current_entry.usuario_id,
            estado_seguimiento=state.strip(),
            creada_en=current_entry.creada_en,
            actualizada_en=timestamp,
            oportunidad=current_entry.oportunidad,
        )
        entries[index] = updated
        _save_pipeline(reference, entries, path)
        return updated
    raise KeyError(opportunity_id)


def _warning_message(estado_oficial: str) -> str | None:
    normalized = estado_oficial.strip().lower()
    if normalized not in OFFICIAL_WARNING_STATES:
        return None
    return (
        f"El expediente figura en estado oficial {estado_oficial}. "
        "Se mantiene en el pipeline para conservar el seguimiento histórico del usuario."
    )


def summarize_pipeline(entries: list[dict[str, object]]) -> dict[str, int]:
    summary = {
        "total_oportunidades": len(entries),
        "con_advertencia_oficial": sum(1 for entry in entries if entry["advertencia_oficial"] is not None),
    }
    for state in PIPELINE_STATES:
        key = f"estado_{state.lower().replace(' ', '_')}"
        summary[key] = sum(1 for entry in entries if entry["estado_seguimiento"] == state)
    return summary


def build_pipeline_payload(
    path: Path = DEFAULT_PIPELINE_PATH,
    catalog_path: Path = DEFAULT_DATA_PATH,
    usuario_id: str | None = None,
) -> dict[str, object]:
    reference, saved_entries = load_pipeline(path)
    entries: list[dict[str, object]] = []
    for saved_entry in saved_entries:
        if usuario_id is not None and saved_entry.usuario_id != usuario_id:
            continue
        refreshed_snapshot = _load_detail_snapshot(saved_entry.opportunity_id, catalog_path) or saved_entry.oportunidad
        warning = _warning_message(refreshed_snapshot.estado_oficial)
        entries.append(
            {
                "opportunity_id": saved_entry.opportunity_id,
                "usuario_id": saved_entry.usuario_id,
                "estado_seguimiento": saved_entry.estado_seguimiento,
                "creada_en": saved_entry.creada_en,
                "actualizada_en": saved_entry.actualizada_en,
                "oportunidad": refreshed_snapshot.__dict__,
                "advertencia_oficial": warning,
            }
        )

    return {
        "referencia_funcional": reference,
        "estados_disponibles": list(PIPELINE_STATES),
        "summary": summarize_pipeline(entries),
        "pipeline": entries,
    }
