from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_PATH = BASE_DIR / "data" / "licitaciones_ti_canarias.xlsx"
REFERENCE = "PB-012"

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"x": MAIN_NS, "r": REL_NS}

SHEET_NAMES = {
    "Licitaciones TI Canarias": "licitaciones",
    "Detalle Lotes": "lotes",
    "Adjudicaciones": "adjudicaciones",
}


@dataclass(frozen=True)
class CanariasLicitacion:
    slug: str
    id_expediente: str
    titulo: str
    estado: str | None
    organo_contratacion: str | None
    importe_estimado: str | None
    importe_con_iva: str | None
    importe_sin_iva: str | None
    cpvs_informaticos: str | None
    ubicacion: str | None
    procedimiento: str | None
    plazo_presentacion: str | None
    numero_lotes: str | None
    numero_adjudicaciones: str | None
    enlace_placsp: str | None
    fecha_actualizacion: str | None
    fichero_origen_atom: str | None


@dataclass(frozen=True)
class CanariasLote:
    slug: str
    id_expediente: str
    titulo_licitacion: str
    numero_lote: str | None
    nombre_lote: str | None
    importe_con_iva: str | None
    importe_sin_iva: str | None
    cpvs: str | None
    ubicacion: str | None
    nuts: str | None
    ciudad: str | None
    criterios_adjudicacion: str | None
    licitacion_slug: str


@dataclass(frozen=True)
class CanariasAdjudicacion:
    slug: str
    id_expediente: str
    titulo: str
    resultado: str | None
    descripcion: str | None
    fecha_adjudicacion: str | None
    lote: str | None
    ganador: str | None
    nif_ganador: str | None
    ciudad_ganador: str | None
    pais: str | None
    importe_adjudicacion_sin_iva: str | None
    importe_adjudicacion_total: str | None
    ofertas_recibidas: str | None
    ofertas_pyme: str | None
    pyme_adjudicatario: str | None
    oferta_mayor: str | None
    oferta_menor: str | None
    anormalmente_baja: str | None
    id_contrato: str | None
    fecha_contrato: str | None
    tasa_subcontratacion: str | None
    fichero_origen_atom: str | None
    licitacion_slug: str | None


def load_canarias_dataset(path: Path = DEFAULT_DATASET_PATH) -> dict[str, object]:
    resolved = path.resolve()
    return _load_canarias_dataset_cached(str(resolved))


def build_licitacion_detail(slug: str, path: Path = DEFAULT_DATASET_PATH) -> dict[str, object] | None:
    dataset = load_canarias_dataset(path)
    for item in dataset["licitaciones"]:
        if item["slug"] == slug:
            return item
    return None


def build_adjudicacion_detail(slug: str, path: Path = DEFAULT_DATASET_PATH) -> dict[str, object] | None:
    dataset = load_canarias_dataset(path)
    for item in dataset["adjudicaciones"]:
        if item["slug"] == slug:
            return item
    return None


@lru_cache(maxsize=4)
def _load_canarias_dataset_cached(path_str: str) -> dict[str, object]:
    path = Path(path_str)
    sheet_rows = _read_workbook_rows(path)

    licitaciones = [_build_licitacion(row) for row in sheet_rows["licitaciones"]]
    licitaciones_by_id = {item.id_expediente: item for item in licitaciones}
    lotes = [_build_lote(row, licitaciones_by_id) for row in sheet_rows["lotes"]]
    adjudicaciones = [_build_adjudicacion(row, licitaciones_by_id) for row in sheet_rows["adjudicaciones"]]

    return {
        "referencia_funcional": REFERENCE,
        "archivo_origen": str(path.relative_to(BASE_DIR)),
        "resumen": {
            "licitaciones": len(licitaciones),
            "lotes": len(lotes),
            "adjudicaciones": len(adjudicaciones),
        },
        "licitaciones": [item.__dict__ for item in licitaciones],
        "lotes": [item.__dict__ for item in lotes],
        "adjudicaciones": [item.__dict__ for item in adjudicaciones],
    }


def _read_workbook_rows(path: Path) -> dict[str, list[dict[str, str | None]]]:
    with ZipFile(path) as workbook:
        sheet_targets = _resolve_sheet_targets(workbook)
        return {
            key: _read_sheet_rows(workbook, sheet_targets[name])
            for name, key in SHEET_NAMES.items()
        }


def _resolve_sheet_targets(workbook: ZipFile) -> dict[str, str]:
    workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
    rels_root = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
    relationships = {
        node.attrib["Id"]: node.attrib["Target"]
        for node in rels_root.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
    }

    targets: dict[str, str] = {}
    for sheet in workbook_root.findall("x:sheets/x:sheet", NS):
        name = sheet.attrib["name"]
        rel_id = sheet.attrib[f"{{{REL_NS}}}id"]
        target = relationships[rel_id]
        normalized_target = target.lstrip("/")
        if not normalized_target.startswith("xl/"):
            normalized_target = f"xl/{normalized_target}"
        targets[name] = normalized_target
    return targets


def _read_sheet_rows(workbook: ZipFile, sheet_target: str) -> list[dict[str, str | None]]:
    root = ET.fromstring(workbook.read(sheet_target))
    rows = root.find("x:sheetData", NS)
    if rows is None:
        return []

    parsed_rows: list[dict[str, str | None]] = []
    headers: dict[str, str] = {}
    for index, row in enumerate(rows.findall("x:row", NS)):
        values: dict[str, str | None] = {}
        for cell in row.findall("x:c", NS):
            column = _column_letters(cell.attrib["r"])
            values[column] = _cell_value(cell)

        if index == 0:
            headers = {column: value or column for column, value in values.items()}
            continue

        parsed_rows.append({header: values.get(column) for column, header in headers.items()})

    return parsed_rows


def _cell_value(cell: ET.Element) -> str | None:
    inline = cell.find("x:is", NS)
    if inline is not None:
        text = "".join(node.text or "" for node in inline.iter(f"{{{MAIN_NS}}}t"))
        return _normalize_text(text)

    value = cell.findtext("x:v", default="", namespaces=NS)
    return _normalize_text(value)


def _build_licitacion(row: dict[str, str | None]) -> CanariasLicitacion:
    expediente_id = row["ID Expediente"] or "Expediente sin identificar"
    return CanariasLicitacion(
        slug=_slugify(expediente_id),
        id_expediente=expediente_id,
        titulo=row["Título"] or expediente_id,
        estado=row["Estado"],
        organo_contratacion=row["Órgano Contratación"],
        importe_estimado=_format_decimal(row["Importe Estimado"]),
        importe_con_iva=_format_decimal(row["Importe con IVA"]),
        importe_sin_iva=_format_decimal(row["Importe sin IVA"]),
        cpvs_informaticos=row["CPVs Informáticos"],
        ubicacion=row["Ubicación"],
        procedimiento=row["Procedimiento"],
        plazo_presentacion=row["Plazo Presentación"],
        numero_lotes=_format_integer(row["Nº Lotes"]),
        numero_adjudicaciones=_format_integer(row["Nº Adjudicaciones"]),
        enlace_placsp=row["Enlace PLACSP"],
        fecha_actualizacion=row["Fecha Actualización"],
        fichero_origen_atom=row["Fichero Origen"],
    )


def _build_lote(row: dict[str, str | None], licitaciones_by_id: dict[str, CanariasLicitacion]) -> CanariasLote:
    expediente_id = row["ID Expediente"] or "Expediente sin identificar"
    numero_lote = row["Nº Lote"]
    licitacion = licitaciones_by_id.get(expediente_id)
    return CanariasLote(
        slug=_slugify(f"{expediente_id}-{numero_lote or 'sin-lote'}-{row['Nombre Lote'] or ''}"),
        id_expediente=expediente_id,
        titulo_licitacion=row["Título Licitación"] or expediente_id,
        numero_lote=numero_lote,
        nombre_lote=row["Nombre Lote"],
        importe_con_iva=_format_decimal(row["Importe con IVA (€)"]),
        importe_sin_iva=_format_decimal(row["Importe sin IVA (€)"]),
        cpvs=row["CPVs"],
        ubicacion=row["Ubicación"],
        nuts=row["NUTS"],
        ciudad=row["Ciudad"],
        criterios_adjudicacion=row["Criterios Adjudicación"],
        licitacion_slug=licitacion.slug if licitacion is not None else _slugify(expediente_id),
    )


def _build_adjudicacion(
    row: dict[str, str | None], licitaciones_by_id: dict[str, CanariasLicitacion]
) -> CanariasAdjudicacion:
    expediente_id = row["ID Expediente"] or "Expediente sin identificar"
    licitacion = licitaciones_by_id.get(expediente_id)
    contract_id = row["ID Contrato"]
    return CanariasAdjudicacion(
        slug=_slugify(f"{expediente_id}-{contract_id or row['Ganador'] or row['Fecha Adjudicación'] or 'adjudicacion'}"),
        id_expediente=expediente_id,
        titulo=row["Título"] or expediente_id,
        resultado=row["Resultado"],
        descripcion=row["Descripción"],
        fecha_adjudicacion=row["Fecha Adjudicación"],
        lote=row["Lote"],
        ganador=row["Ganador"],
        nif_ganador=row["NIF Ganador"],
        ciudad_ganador=row["Ciudad Ganador"],
        pais=row["País"],
        importe_adjudicacion_sin_iva=_format_decimal(row["Importe Adj. sin IVA"]),
        importe_adjudicacion_total=_format_decimal(row["Importe Adj. Total"]),
        ofertas_recibidas=_format_integer(row["Ofertas Recibidas"]),
        ofertas_pyme=_format_integer(row["Ofertas PYME"]),
        pyme_adjudicatario=_format_boolean(row["PYME Adjudicatario"]),
        oferta_mayor=_format_decimal(row["Oferta Mayor"]),
        oferta_menor=_format_decimal(row["Oferta Menor"]),
        anormalmente_baja=_format_boolean(row["Anorm. Baja"]),
        id_contrato=contract_id,
        fecha_contrato=row["Fecha Contrato"],
        tasa_subcontratacion=row["Tasa Subcontrat."],
        fichero_origen_atom=licitacion.fichero_origen_atom if licitacion is not None else None,
        licitacion_slug=licitacion.slug if licitacion is not None else None,
    )


def _format_decimal(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        quantized = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return value
    normalized = f"{quantized:,.2f}"
    return normalized.replace(",", "_").replace(".", ",").replace("_", ".")


def _format_integer(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return str(int(Decimal(value)))
    except (InvalidOperation, ValueError):
        return value


def _format_boolean(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized == "true":
        return "Sí"
    if normalized == "false":
        return "No"
    return value


def _normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _column_letters(reference: str) -> str:
    letters: list[str] = []
    for char in reference:
        if char.isalpha():
            letters.append(char)
            continue
        break
    return "".join(letters)


def _slugify(value: str) -> str:
    chunks: list[str] = []
    current: list[str] = []
    for char in value.strip().lower():
        if char.isalnum():
            current.append(char)
            continue
        if current:
            chunks.append("".join(current))
            current = []
    if current:
        chunks.append("".join(current))
    return "-".join(chunks) or "registro-sin-id"
