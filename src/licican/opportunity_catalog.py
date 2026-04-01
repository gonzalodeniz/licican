from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from licican.atom_consolidation import load_atom_opportunities
from licican.postgres_catalog import PostgresCatalogError, load_postgres_opportunity_records
from licican.shared.filters import CatalogFilters
from licican.shared.text import clean_text
from licican.source_coverage import load_source_coverage
from licican.ti_classification import OpportunityCandidate, classify_opportunity, load_rule_set


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = BASE_DIR / "data"
DEFAULT_CATALOG_PAGE_SIZE = 10


@dataclass(frozen=True)
class OpportunityRecord:
    id: str
    titulo: str
    descripcion: str
    organismo: str
    ubicacion: str
    procedimiento: str | None
    presupuesto: int | None
    fecha_publicacion_oficial: str
    fecha_limite: str
    estado: str
    solvencia_tecnica: str | None
    criterios_adjudicacion: tuple[str, ...]
    fuente_oficial: str
    url_fuente_oficial: str
    cpvs: tuple[str, ...]
    actualizaciones_oficiales: tuple[dict[str, object], ...]
    fichero_origen_atom: str | None = None


@dataclass(frozen=True)
class CatalogOpportunity:
    id: str
    titulo: str
    organismo: str
    ubicacion: str
    procedimiento: str | None
    presupuesto: int | None
    fecha_publicacion_oficial: str
    fecha_limite: str
    estado: str
    fuente_oficial: str
    url_fuente_oficial: str
    clasificacion_ti: str


@dataclass(frozen=True)
class OpportunityDetail:
    id: str
    titulo: str
    descripcion: str
    organismo: str
    ubicacion: str
    procedimiento: str | None
    presupuesto: int | None
    fecha_publicacion_oficial: str
    fecha_limite: str
    estado: str
    solvencia_tecnica: str | None
    criterios_adjudicacion: tuple[str, ...]
    fuente_oficial: str
    url_fuente_oficial: str
    clasificacion_ti: str
    referencia_funcional: str
    actualizacion_oficial_mas_reciente: dict[str, object] | None
    historial_actualizaciones: tuple[dict[str, object], ...]
    fichero_origen_atom: str | None


class CatalogDataSourceError(RuntimeError):
    pass


def _build_pagination(total_results: int, requested_page: int, page_size: int) -> dict[str, object]:
    safe_page_size = max(page_size, 1)
    total_pages = max((total_results + safe_page_size - 1) // safe_page_size, 1)
    current_page = min(max(requested_page, 1), total_pages)
    start_index = 0 if total_results == 0 else (current_page - 1) * safe_page_size
    end_index = min(start_index + safe_page_size, total_results)
    visible_from = 0 if total_results == 0 else start_index + 1
    visible_to = end_index
    adjusted = current_page != requested_page
    adjustment_reason = None
    if adjusted:
        adjustment_reason = "invalida" if requested_page < 1 else "fuera_de_rango"

    return {
        "pagina_solicitada": requested_page,
        "pagina_actual": current_page,
        "tamano_pagina": safe_page_size,
        "total_paginas": total_pages,
        "total_resultados": total_results,
        "resultado_desde": visible_from,
        "resultado_hasta": visible_to,
        "hay_anterior": current_page > 1,
        "hay_siguiente": current_page < total_pages,
        "pagina_anterior": current_page - 1 if current_page > 1 else None,
        "pagina_siguiente": current_page + 1 if current_page < total_pages else None,
        "ajustada": adjusted,
        "motivo_ajuste": adjustment_reason,
    }


def load_opportunity_records(
    path: Path = DEFAULT_DATA_PATH,
    backend: str | None = None,
) -> tuple[str, list[OpportunityRecord]]:
    resolved_backend = _resolve_catalog_backend(path, backend)
    if resolved_backend == "postgres":
        try:
            reference, records = load_postgres_opportunity_records()
        except PostgresCatalogError as exc:
            raise CatalogDataSourceError(
                "No se pudo cargar el catalogo desde PostgreSQL. Revisa la conexion configurada."
            ) from exc
        return reference, [OpportunityRecord(**record) for record in records]

    if path.is_dir():
        atom_files = sorted(path.glob("*.atom"))
        if atom_files:
            reference, records = load_atom_opportunities(path)
            return reference, [
                OpportunityRecord(
                    id=item.id,
                    titulo=item.titulo,
                    descripcion=item.descripcion,
                    organismo=item.organismo,
                    ubicacion=item.ubicacion,
                    procedimiento=item.procedimiento,
                    presupuesto=item.presupuesto,
                    fecha_publicacion_oficial=item.fecha_publicacion_oficial,
                    fecha_limite=item.fecha_limite,
                    estado=item.estado,
                    solvencia_tecnica=item.solvencia_tecnica,
                    criterios_adjudicacion=item.criterios_adjudicacion,
                    fuente_oficial=item.fuente_oficial,
                    url_fuente_oficial=item.url_fuente_oficial,
                    cpvs=item.cpvs,
                    actualizaciones_oficiales=(),
                    fichero_origen_atom=item.fichero_origen_atom,
                )
                for item in records
            ]

        json_path = path / "opportunities.json"
        if json_path.exists():
            path = json_path

    payload = json.loads(path.read_text(encoding="utf-8"))
    records = [
        OpportunityRecord(
            id=item["id"],
            titulo=item["titulo"],
            descripcion=item["descripcion"],
            organismo=item["organismo"],
            ubicacion=item["ubicacion"],
            procedimiento=item.get("procedimiento"),
            presupuesto=item.get("presupuesto"),
            fecha_publicacion_oficial=item["fecha_publicacion_oficial"],
            fecha_limite=item["fecha_limite"],
            estado=item["estado"],
            solvencia_tecnica=item.get("solvencia_tecnica"),
            criterios_adjudicacion=tuple(item.get("criterios_adjudicacion") or ()),
            fuente_oficial=item["fuente_oficial"],
            url_fuente_oficial=item["url_fuente_oficial"],
            cpvs=tuple(item.get("cpvs", [])),
            actualizaciones_oficiales=tuple(item.get("actualizaciones_oficiales", [])),
            fichero_origen_atom=item.get("fichero_origen_atom"),
        )
        for item in payload["opportunities"]
    ]
    return payload["referencia_funcional"], records


def _resolve_catalog_backend(path: Path, backend: str | None) -> str:
    if backend is not None:
        normalized = backend.strip().lower()
    elif path != DEFAULT_DATA_PATH:
        normalized = "file"
    else:
        normalized = os.getenv("LICICAN_CATALOG_BACKEND", "postgres").strip().lower() or "postgres"
    if normalized not in {"file", "postgres"}:
        raise ValueError(f"Backend de catalogo no soportado: {normalized}")
    return normalized


def _sorted_updates(record: OpportunityRecord) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            record.actualizaciones_oficiales,
            key=lambda item: str(item.get("fecha_publicacion", "")),
        )
    )


def _resolve_latest_visible_snapshot(record: OpportunityRecord) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "procedimiento": record.procedimiento,
        "presupuesto": record.presupuesto,
        "fecha_limite": record.fecha_limite,
        "estado": record.estado,
        "solvencia_tecnica": record.solvencia_tecnica,
        "criterios_adjudicacion": list(record.criterios_adjudicacion),
    }
    for update in _sorted_updates(record):
        for field in (
            "procedimiento",
            "presupuesto",
            "fecha_limite",
            "estado",
            "solvencia_tecnica",
            "criterios_adjudicacion",
        ):
            if field in update:
                value = update[field]
                if field == "criterios_adjudicacion":
                    snapshot[field] = list(value or [])
                else:
                    snapshot[field] = value
    return snapshot


def _classify_record(record: OpportunityRecord, rules) -> str:
    if record.fichero_origen_atom is not None and any(cpv.startswith(("72", "48", "302")) for cpv in record.cpvs):
        return "TI"

    decision = classify_opportunity(
        OpportunityCandidate(
            titulo=record.titulo,
            descripcion=record.descripcion,
            cpvs=record.cpvs,
        ),
        rules,
    )
    return decision.clasificacion


def _matches_filters(record: OpportunityRecord, snapshot: dict[str, object], filters: CatalogFilters) -> bool:
    normalized_filters = filters.normalized()

    if normalized_filters.palabra_clave is not None:
        haystack = " ".join(
            (
                record.titulo,
                record.descripcion,
                record.organismo,
                record.ubicacion,
                snapshot["procedimiento"] or "",
            )
        ).lower()
        if normalized_filters.palabra_clave.lower() not in haystack:
            return False

    presupuesto = snapshot["presupuesto"]
    if normalized_filters.presupuesto_min is not None:
        if presupuesto is None or int(presupuesto) < normalized_filters.presupuesto_min:
            return False

    if normalized_filters.presupuesto_max is not None:
        if presupuesto is None or int(presupuesto) > normalized_filters.presupuesto_max:
            return False

    if normalized_filters.procedimiento is not None:
        procedimiento = clean_text(str(snapshot["procedimiento"] or ""))
        if procedimiento is None or procedimiento.lower() != normalized_filters.procedimiento.lower():
            return False

    if normalized_filters.ubicacion is not None:
        ubicacion = clean_text(record.ubicacion)
        if ubicacion is None or ubicacion.lower() != normalized_filters.ubicacion.lower():
            return False

    return True


def build_opportunity_detail(
    opportunity_id: str,
    path: Path = DEFAULT_DATA_PATH,
    backend: str | None = None,
) -> dict[str, object] | None:
    reference, records = load_opportunity_records(path, backend=backend)
    rules = load_rule_set()
    mvp_sources = {source.nombre for source in load_source_coverage() if source.estado == "MVP"}

    for record in records:
        if record.id != opportunity_id:
            continue
        if record.fichero_origen_atom is None and record.fuente_oficial not in mvp_sources:
            return None

        classification = _classify_record(record, rules)
        if classification != "TI":
            return None

        snapshot = _resolve_latest_visible_snapshot(record)
        updates = _sorted_updates(record)
        detail = OpportunityDetail(
            id=record.id,
            titulo=record.titulo,
            descripcion=record.descripcion,
            organismo=record.organismo,
            ubicacion=record.ubicacion,
            procedimiento=snapshot["procedimiento"],
            presupuesto=snapshot["presupuesto"],
            fecha_publicacion_oficial=record.fecha_publicacion_oficial,
            fecha_limite=str(snapshot["fecha_limite"]),
            estado=str(snapshot["estado"]),
            solvencia_tecnica=snapshot["solvencia_tecnica"],
            criterios_adjudicacion=tuple(snapshot["criterios_adjudicacion"]),
            fuente_oficial=record.fuente_oficial,
            url_fuente_oficial=record.url_fuente_oficial,
            clasificacion_ti=classification,
            referencia_funcional=reference,
            actualizacion_oficial_mas_reciente=(dict(updates[-1]) if updates else None),
            historial_actualizaciones=tuple(dict(item) for item in updates),
            fichero_origen_atom=record.fichero_origen_atom,
        )
        return detail.__dict__

    return None


def build_catalog(
    path: Path = DEFAULT_DATA_PATH,
    filters: CatalogFilters | None = None,
    page: int = 1,
    page_size: int = DEFAULT_CATALOG_PAGE_SIZE,
    backend: str | None = None,
) -> dict[str, object]:
    reference, records = load_opportunity_records(path, backend=backend)
    rules = load_rule_set()
    mvp_sources = {source.nombre for source in load_source_coverage() if source.estado == "MVP"}
    active_filters = (filters or CatalogFilters()).normalized()
    validation_error = active_filters.validation_error()
    atom_sources = sorted({record.fichero_origen_atom for record in records if record.fichero_origen_atom})
    applied_coverage = atom_sources if atom_sources else sorted(mvp_sources)

    opportunities: list[CatalogOpportunity] = []
    available_locations: set[str] = set()
    available_procedures: set[str] = set()
    total_visible_before_filters = 0
    for record in records:
        if record.fichero_origen_atom is None and record.fuente_oficial not in mvp_sources:
            continue

        classification = _classify_record(record, rules)
        if classification != "TI":
            continue
        snapshot = _resolve_latest_visible_snapshot(record)
        total_visible_before_filters += 1
        available_locations.add(record.ubicacion)
        if snapshot["procedimiento"]:
            available_procedures.add(str(snapshot["procedimiento"]))

        if validation_error is None and not _matches_filters(record, snapshot, active_filters):
            continue

        opportunities.append(
            CatalogOpportunity(
                id=record.id,
                titulo=record.titulo,
                organismo=record.organismo,
                ubicacion=record.ubicacion,
                procedimiento=snapshot["procedimiento"],
                presupuesto=snapshot["presupuesto"],
                fecha_publicacion_oficial=record.fecha_publicacion_oficial,
                fecha_limite=str(snapshot["fecha_limite"]),
                estado=str(snapshot["estado"]),
                fuente_oficial=record.fuente_oficial,
                url_fuente_oficial=record.url_fuente_oficial,
                clasificacion_ti=classification,
            )
        )

    opportunities.sort(key=lambda opportunity: opportunity.fecha_limite)
    pagination = _build_pagination(len(opportunities), page, page_size)
    page_slice = slice(
        max(int(pagination["resultado_desde"]) - 1, 0),
        int(pagination["resultado_hasta"]),
    )
    return {
        "referencia_funcional": reference,
        "cobertura_aplicada": applied_coverage,
        "total_registros_origen": len(records),
        "total_oportunidades_visibles": total_visible_before_filters,
        "total_oportunidades_catalogo": len(opportunities),
        "filtros_activos": active_filters.active_filters(),
        "error_validacion": validation_error,
        "filtros_disponibles": {
            "procedimientos": sorted(available_procedures),
            "ubicaciones": sorted(available_locations),
        },
        "paginacion": pagination,
        "oportunidades": [opportunity.__dict__ for opportunity in opportunities[page_slice]],
    }
