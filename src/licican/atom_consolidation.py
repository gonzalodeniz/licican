from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

from licican.shared.domain_constants import (
    CANARIAS_KEYWORDS,
    TI_CPV_PREFIXES,
    map_procedure,
    map_status,
)
from licican.shared.text import clean_text, normalize_text, slugify
from licican.shared.xml_helpers import (
    find_first,
    find_first_text,
    find_text_by_path,
    iter_local,
    iter_texts,
    local_name,
)


ATOM_NS = "http://www.w3.org/2005/Atom"
SOURCE_NAME = "Plataforma de Contratacion del Sector Publico"
REFERENCE = "PB-011"
@dataclass(frozen=True)
class ConsolidatedAtomRecord:
    expediente_id: str
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
    fichero_origen_atom: str


@dataclass(frozen=True)
class _ParsedEntry:
    expediente_id: str
    updated_at: datetime
    record: ConsolidatedAtomRecord


def load_atom_opportunities(data_dir: Path) -> tuple[str, list[ConsolidatedAtomRecord]]:
    latest_by_expediente: dict[str, _ParsedEntry] = {}

    for atom_path in sorted(data_dir.glob("*.atom")):
        root = ET.parse(atom_path).getroot()
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            parsed = _parse_entry(entry, atom_path.name)
            if parsed is None:
                continue

            current = latest_by_expediente.get(parsed.expediente_id)
            if current is None or _is_newer(parsed, current):
                latest_by_expediente[parsed.expediente_id] = parsed

    records = [item.record for item in latest_by_expediente.values()]
    records.sort(key=lambda record: (record.fecha_limite, record.fecha_publicacion_oficial, record.id))
    return REFERENCE, records


def _is_newer(candidate: _ParsedEntry, current: _ParsedEntry) -> bool:
    if candidate.updated_at != current.updated_at:
        return candidate.updated_at > current.updated_at
    return candidate.record.fichero_origen_atom > current.record.fichero_origen_atom


def _parse_entry(entry: ET.Element, source_filename: str) -> _ParsedEntry | None:
    contract_status = find_first(entry, "ContractFolderStatus")
    if contract_status is None:
        return None

    expediente_id = find_first_text(contract_status, "ContractFolderID")
    updated_text = entry.findtext(f"{{{ATOM_NS}}}updated")
    if not expediente_id or not updated_text:
        return None

    procurement_project = find_first(contract_status, "ProcurementProject")
    if procurement_project is None:
        return None

    cpvs = tuple(iter_texts(procurement_project, "ItemClassificationCode"))
    if not _matches_ti(cpvs):
        return None

    geographic_context = _build_geographic_context(contract_status, procurement_project)
    if not _matches_canarias(geographic_context):
        return None

    updated_at = datetime.fromisoformat(updated_text)
    titulo = (find_first_text(procurement_project, "Name") or entry.findtext(f"{{{ATOM_NS}}}title") or expediente_id).strip()
    descripcion = (_first_non_empty((entry.findtext(f"{{{ATOM_NS}}}summary"), titulo)) or titulo).strip()
    organismo = _find_party_name(contract_status) or "No informado"
    ubicacion = _resolve_location_label(geographic_context)
    presupuesto = _resolve_budget(procurement_project)
    procedimiento = map_procedure(find_text_by_path(contract_status, ("TenderingProcess", "ProcedureCode")))
    fecha_publicacion = updated_at.date().isoformat()
    fecha_limite = find_text_by_path(contract_status, ("TenderingProcess", "TenderSubmissionDeadlinePeriod", "EndDate")) or "No informado"
    estado = map_status(find_first_text(contract_status, "ContractFolderStatusCode"))
    solvencia = _resolve_technical_solvency(contract_status)
    criterios = tuple(_unique_in_order(_iter_awarding_criteria(contract_status)))
    url_fuente = _find_atom_link(entry)

    record = ConsolidatedAtomRecord(
        expediente_id=expediente_id,
        id=slugify(expediente_id),
        titulo=titulo,
        descripcion=descripcion,
        organismo=organismo,
        ubicacion=ubicacion,
        procedimiento=procedimiento,
        presupuesto=presupuesto,
        fecha_publicacion_oficial=fecha_publicacion,
        fecha_limite=fecha_limite,
        estado=estado,
        solvencia_tecnica=solvencia,
        criterios_adjudicacion=criterios,
        fuente_oficial=SOURCE_NAME,
        url_fuente_oficial=url_fuente,
        cpvs=cpvs,
        fichero_origen_atom=source_filename,
    )
    return _ParsedEntry(expediente_id=expediente_id, updated_at=updated_at, record=record)


def _build_geographic_context(contract_status: ET.Element, procurement_project: ET.Element) -> dict[str, tuple[str, ...]]:
    located_party = find_first(contract_status, "LocatedContractingParty")
    parent_names: list[str] = []
    if located_party is not None:
        for parent in iter_local(located_party, "ParentLocatedParty"):
            parent_names.extend(iter_texts(parent, "Name"))

    return {
        "codes": tuple(iter_texts(procurement_project, "CountrySubentityCode")),
        "subentities": tuple(iter_texts(procurement_project, "CountrySubentity")),
        "parent_names": tuple(parent_names),
    }


def _matches_canarias(geographic_context: dict[str, tuple[str, ...]]) -> bool:
    normalized_codes = tuple(normalize_text(value) for value in geographic_context["codes"])
    if any(code.startswith("es7") for code in normalized_codes):
        return True

    normalized_texts = tuple(
        normalize_text(value)
        for value in geographic_context["subentities"] + geographic_context["parent_names"]
    )
    return any(any(keyword in value for keyword in CANARIAS_KEYWORDS) for value in normalized_texts)


def _matches_ti(cpvs: tuple[str, ...]) -> bool:
    return any(cpv.startswith(TI_CPV_PREFIXES) for cpv in cpvs)


def _resolve_location_label(geographic_context: dict[str, tuple[str, ...]]) -> str:
    for value in geographic_context["subentities"]:
        if value.strip():
            return value.strip()
    for value in geographic_context["codes"]:
        if value.startswith("ES7"):
            return "Canarias"
    for value in geographic_context["parent_names"]:
        if any(keyword in normalize_text(value) for keyword in CANARIAS_KEYWORDS):
            return value.strip()
    return "Canarias"


def _resolve_budget(procurement_project: ET.Element) -> int | None:
    budget_amount = find_first(procurement_project, "BudgetAmount")
    if budget_amount is None:
        return None

    for field_name in ("TotalAmount", "TaxExclusiveAmount", "EstimatedOverallContractAmount"):
        value = find_first_text(budget_amount, field_name)
        parsed = _parse_budget(value)
        if parsed is not None:
            return parsed
    return None


def _parse_budget(value: str | None) -> int | None:
    if value is None:
        return None
    normalized = value.strip().replace(",", ".")
    if not normalized:
        return None
    try:
        return round(float(normalized))
    except ValueError:
        return None


def _resolve_technical_solvency(contract_status: ET.Element) -> str | None:
    descriptions = iter_texts(contract_status, "Description")
    collected: list[str] = []
    for description in descriptions:
        normalized = normalize_text(description)
        if "pliego" in normalized or "solvencia" in normalized or "capacidad" in normalized:
            collected.append(description)
    unique = tuple(_unique_in_order(collected))
    if not unique:
        return None
    return " | ".join(unique)


def _iter_awarding_criteria(contract_status: ET.Element) -> list[str]:
    awarding_terms = find_first(contract_status, "AwardingTerms")
    if awarding_terms is None:
        return []

    criteria: list[str] = []
    for awarding_criteria in iter_local(awarding_terms, "AwardingCriteria"):
        description = find_first_text(awarding_criteria, "Description")
        if description:
            criteria.append(description)
    return criteria


def _find_party_name(contract_status: ET.Element) -> str | None:
    located_party = find_first(contract_status, "LocatedContractingParty")
    if located_party is None:
        return None
    party = find_first(located_party, "Party")
    if party is None:
        return None
    party_name = find_first(party, "PartyName")
    if party_name is None:
        return None
    return find_first_text(party_name, "Name")


def _find_atom_link(entry: ET.Element) -> str:
    for child in entry:
        if local_name(child.tag) == "link":
            href = child.attrib.get("href")
            if href:
                return href
    return ""


def _first_non_empty(values: tuple[str | None, ...]) -> str | None:
    for value in values:
        if value is not None and value.strip():
            return value
    return None


def _unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
