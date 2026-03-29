#!/usr/bin/env python3
"""
Importador de ficheros ATOM de licitaciones de la Plataforma de
Contratación del Sector Público a PostgreSQL.

FILTROS:
  - Geográfico: Solo licitaciones de Canarias (NUTS ES7* o "Canarias"
    en la jerarquía ParentLocatedParty o en CountrySubentity).
  - Tipo de contrato: Solo licitaciones con CPV informático:
      72xxxxxx — Servicios TI
      48xxxxxx — Paquetes de software
      302xxxxx — Equipos informáticos (hardware)
    Se buscan CPVs tanto en el proyecto principal como en todos los lotes.

Reglas de importación:
  - Si la licitación NO existe en la BBDD, se inserta.
  - Si la licitación YA existe y el registro del fichero es MÁS RECIENTE, se actualiza.
  - Si la licitación YA existe y el registro del fichero es MÁS ANTIGUO o IGUAL, NO se actualiza.

Flujo de lectura:
  1. Siempre se lee el fichero principal (licitacionesPerfilesContratanteCompleto3.atom).
  2. Se sigue la cadena de links rel="next" dentro de cada fichero.
  3. Cuando el siguiente fichero de la cadena ya está registrado en la tabla
     fichero_procesado, se detiene la lectura.
  El fichero principal NUNCA se registra en fichero_procesado.

Uso:
  python3 importar_licitaciones.py /ruta/directorio/
  python3 importar_licitaciones.py --force /ruta/directorio/  (ignora fichero_procesado)
"""

import sys
import os
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

import psycopg2
from psycopg2.extras import execute_values

# ============================================================
# Configuración
# ============================================================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "licitaciones"),
    "user": os.getenv("DB_USER", "licitaciones_admin"),
    "password": os.getenv("DB_PASSWORD", "Lic1t4c10n3s_2026!"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("importador")

# ============================================================
# Namespaces XML
# ============================================================
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
    "cac-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
    "cbc-place-ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
    "at": "http://purl.org/atompub/tombstones/1.0",
}

# ============================================================
# Prefijos CPV de contratos informáticos
# ============================================================
CPV_IT_PREFIXES = tuple(
    p.strip()
    for p in os.getenv("FILTRO_CPV_PREFIXES", "72,48,302").split(",")
    if p.strip()
)

# ============================================================
# Filtro geográfico
# ============================================================
NUTS_PREFIXES = tuple(
    p.strip()
    for p in os.getenv("FILTRO_NUTS_PREFIXES", "ES7").split(",")
    if p.strip()
)

GEO_KEYWORDS = [
    k.strip().lower()
    for k in os.getenv("FILTRO_GEO_KEYWORDS", "canarias").split(",")
    if k.strip()
]


# ============================================================
# Funciones auxiliares de extracción XML
# ============================================================
def text(element, xpath):
    """Extrae el texto de un xpath relativo, o None."""
    el = element.find(xpath, NS)
    if el is not None and el.text:
        return el.text.strip()
    return None


def attr(element, xpath, attribute):
    """Extrae un atributo de un elemento encontrado por xpath."""
    el = element.find(xpath, NS)
    if el is not None:
        return el.get(attribute)
    return None


def to_decimal(value):
    """Convierte a Decimal o None."""
    if value is None:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def to_bool(value):
    """Convierte texto a boolean."""
    if value is None:
        return None
    return value.lower() == "true"


def to_int(value):
    """Convierte texto a int o None."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def to_date(value):
    """Convierte texto ISO a date o None."""
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def combine_datetime(date_text, time_text, tz_offset="+01:00"):
    """Combina fecha y hora en un datetime con zona horaria."""
    if date_text is None:
        return None
    dt_str = date_text
    if time_text:
        dt_str += f"T{time_text}"
    else:
        dt_str += "T00:00:00"
    # Añadir zona horaria si no la tiene
    if "+" not in dt_str and "Z" not in dt_str:
        dt_str += tz_offset
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None


def extract_jerarquia(located_party):
    """Extrae la cadena jerárquica de ParentLocatedParty como lista."""
    result = []
    parent = located_party.find("cac-place-ext:ParentLocatedParty", NS)
    while parent is not None:
        name = text(parent, "cac:PartyName/cbc:Name")
        if name:
            result.append(name)
        parent = parent.find("cac-place-ext:ParentLocatedParty", NS)
    return result if result else None


def extract_all_cpvs(cfs):
    """
    Extrae TODOS los códigos CPV de un ContractFolderStatus,
    tanto del proyecto principal como de todos los lotes.
    Devuelve una lista de códigos únicos ordenados.
    """
    cpvs = set()
    for cpv_el in cfs.findall(".//cbc:ItemClassificationCode", NS):
        if cpv_el.text:
            cpvs.add(cpv_el.text.strip())
    return sorted(cpvs) if cpvs else None


# ============================================================
# Filtros de importación
# ============================================================
def is_canarias(cfs, jerarquia_org):
    """
    Comprueba si la licitación pertenece a la zona geográfica configurada.
    Criterios (cualquiera de ellos):
      1. Código NUTS (CountrySubentityCode) empieza por algún prefijo de NUTS_PREFIXES
      2. CountrySubentity contiene alguna palabra de GEO_KEYWORDS (case-insensitive)
      3. Jerarquía ParentLocatedParty contiene alguna palabra de GEO_KEYWORDS (case-insensitive)
    """
    # 1. Código NUTS en cualquier ubicación (proyecto + lotes)
    for code_el in cfs.findall(".//cbc:CountrySubentityCode", NS):
        if code_el.text and code_el.text.strip().startswith(NUTS_PREFIXES):
            return True

    # 2. CountrySubentity contiene alguna keyword geográfica
    for sub_el in cfs.findall(".//cbc:CountrySubentity", NS):
        if sub_el.text:
            sub_lower = sub_el.text.lower()
            if any(kw in sub_lower for kw in GEO_KEYWORDS):
                return True

    # 3. Jerarquía ParentLocatedParty contiene alguna keyword geográfica
    if jerarquia_org:
        for name in jerarquia_org:
            name_lower = name.lower()
            if any(kw in name_lower for kw in GEO_KEYWORDS):
                return True

    return False


def has_cpv_informatico(cpv_codes):
    """
    Comprueba si alguno de los CPVs corresponde a contratos informáticos:
      72xxxxxx — Servicios TI
      48xxxxxx — Paquetes de software
      302xxxxx — Equipos informáticos
    """
    if not cpv_codes:
        return False
    return any(cpv.startswith(CPV_IT_PREFIXES) for cpv in cpv_codes)


# ============================================================
# Parser de entries
# ============================================================
def parse_entry(entry, fichero_origen):
    """Extrae todos los campos de un <entry> del ATOM.
    Devuelve None si no pasa los filtros (Canarias + CPV informático).
    """

    id_plataforma = text(entry, "atom:id")
    updated_text = text(entry, "atom:updated")
    link_el = entry.find("atom:link", NS)
    link_detalle = link_el.get("href") if link_el is not None else None

    titulo = text(entry, "atom:title")
    resumen = text(entry, "atom:summary")

    # Timestamp de actualización
    try:
        updated_at = datetime.fromisoformat(updated_text) if updated_text else None
    except ValueError:
        updated_at = None

    # ContractFolderStatus
    cfs = entry.find(".//cac-place-ext:ContractFolderStatus", NS)
    if cfs is None:
        log.warning(f"Entry sin ContractFolderStatus: {id_plataforma}")
        return None

    expediente = text(cfs, "cbc:ContractFolderID")
    estado = text(cfs, "cbc-place-ext:ContractFolderStatusCode")
    uuid_ted = text(cfs, "cbc:UUID")

    # --- Órgano de contratación ---
    lcp = cfs.find("cac-place-ext:LocatedContractingParty", NS)
    tipo_organo = text(lcp, "cbc:ContractingPartyTypeCode") if lcp is not None else None
    actividad_organo = text(lcp, "cbc:ActivityCode") if lcp is not None else None
    organo_perfil_url = text(lcp, "cbc:BuyerProfileURIID") if lcp is not None else None

    party = lcp.find("cac:Party", NS) if lcp is not None else None
    organo_contratacion = text(party, "cac:PartyName/cbc:Name") if party is not None else None
    organo_web = text(party, "cbc:WebsiteURI") if party is not None else None
    organo_email = text(party, "cac:Contact/cbc:ElectronicMail") if party is not None else None
    organo_telefono = text(party, "cac:Contact/cbc:Telephone") if party is not None else None
    organo_direccion = text(party, "cac:PostalAddress/cac:AddressLine/cbc:Line") if party is not None else None
    organo_ciudad = text(party, "cac:PostalAddress/cbc:CityName") if party is not None else None
    organo_cp = text(party, "cac:PostalAddress/cbc:PostalZone") if party is not None else None

    # NIF e ID_PLATAFORMA del órgano
    organo_nif = None
    organo_id_plataforma = None
    if party is not None:
        for pi in party.findall("cac:PartyIdentification", NS):
            id_el = pi.find("cbc:ID", NS)
            if id_el is not None:
                scheme = id_el.get("schemeName", "")
                if scheme == "NIF":
                    organo_nif = id_el.text.strip() if id_el.text else None
                elif scheme == "ID_PLATAFORMA":
                    organo_id_plataforma = id_el.text.strip() if id_el.text else None

    # Jerarquía organizativa
    jerarquia_org = extract_jerarquia(lcp) if lcp is not None else None

    # Todos los CPVs (proyecto + lotes)
    cpv_codes = extract_all_cpvs(cfs)

    # ======================================================
    # FILTROS: Canarias + CPV informático
    # Ambos deben cumplirse para importar la licitación
    # ======================================================
    if not is_canarias(cfs, jerarquia_org):
        return None

    if not has_cpv_informatico(cpv_codes):
        return None

    # --- Proyecto de contratación ---
    pp = cfs.find("cac:ProcurementProject", NS)
    tipo_contrato = text(pp, "cbc:TypeCode") if pp is not None else None
    subtipo_contrato = text(pp, "cbc:SubTypeCode") if pp is not None else None
    contrato_mixto = to_bool(text(pp, "cbc:MixContractIndicator")) if pp is not None else None

    # Presupuesto
    budget = pp.find("cac:BudgetAmount", NS) if pp is not None else None
    importe_total = to_decimal(text(budget, "cbc:TotalAmount")) if budget is not None else None
    importe_sin_impuestos = to_decimal(text(budget, "cbc:TaxExclusiveAmount")) if budget is not None else None
    importe_estimado = to_decimal(text(budget, "cbc:EstimatedOverallContractAmount")) if budget is not None else None
    moneda = attr(budget, "cbc:TotalAmount", "currencyID") if budget is not None else "EUR"

    # Ubicación
    loc = pp.find("cac:RealizedLocation", NS) if pp is not None else None
    ubicacion_nuts = text(loc, "cbc:CountrySubentityCode") if loc is not None else None
    ubicacion_comunidad = text(loc, "cbc:CountrySubentity") if loc is not None else None
    ubicacion_ciudad = text(loc, "cac:Address/cbc:CityName") if loc is not None else None
    ubicacion_cp = text(loc, "cac:Address/cbc:PostalZone") if loc is not None else None
    ubicacion_pais = text(loc, "cac:Address/cac:Country/cbc:IdentificationCode") if loc is not None else "ES"

    # Plazos de ejecución
    planned = pp.find("cac:PlannedPeriod", NS) if pp is not None else None
    fecha_inicio_ejecucion = to_date(text(planned, "cbc:StartDate")) if planned is not None else None
    fecha_fin_ejecucion = to_date(text(planned, "cbc:EndDate")) if planned is not None else None

    # --- Proceso de licitación ---
    tp = cfs.find("cac:TenderingProcess", NS)
    procedimiento = text(tp, "cbc:ProcedureCode") if tp is not None else None
    urgencia = text(tp, "cbc:UrgencyCode") if tp is not None else None
    forma_presentacion = text(tp, "cbc:PartPresentationCode") if tp is not None else None
    sistema_contratacion = text(tp, "cbc:ContractingSystemCode") if tp is not None else None
    metodo_envio = text(tp, "cbc:SubmissionMethodCode") if tp is not None else None
    sobre_umbral = to_bool(text(tp, "cbc:OverThresholdIndicator")) if tp is not None else None
    subasta = to_bool(text(tp, "cac:AuctionTerms/cbc:AuctionConstraintIndicator")) if tp is not None else None

    # Plazos
    sub_deadline = tp.find("cac:TenderSubmissionDeadlinePeriod", NS) if tp is not None else None
    fecha_limite_presentacion = combine_datetime(
        text(sub_deadline, "cbc:EndDate"),
        text(sub_deadline, "cbc:EndTime"),
    ) if sub_deadline is not None else None

    doc_avail = tp.find("cac:DocumentAvailabilityPeriod", NS) if tp is not None else None
    fecha_limite_documentacion = combine_datetime(
        text(doc_avail, "cbc:EndDate"),
        text(doc_avail, "cbc:EndTime"),
    ) if doc_avail is not None else None

    # --- Condiciones ---
    tt = cfs.find("cac:TenderingTerms", NS)
    financiacion_ue = text(tt, "cbc:FundingProgramCode") if tt is not None else None
    legislacion_nacional = text(tt, "cbc:ProcurementNationalLegislationCode") if tt is not None else None
    legislacion_referencia = text(tt, "cac:ProcurementLegislationDocumentReference/cbc:ID") if tt is not None else None
    idioma = text(tt, "cac:Language/cbc:ID") if tt is not None else None

    # --- Resultado (TenderResult) ---
    tr = cfs.find("cac:TenderResult", NS)
    resultado_codigo = text(tr, "cbc:ResultCode") if tr is not None else None
    resultado_descripcion = text(tr, "cbc:Description") if tr is not None else None
    fecha_adjudicacion = to_date(text(tr, "cbc:AwardDate")) if tr is not None else None
    ofertas_recibidas = to_int(text(tr, "cbc:ReceivedTenderQuantity")) if tr is not None else None
    ofertas_pymes = to_int(text(tr, "cbc:SMEsReceivedTenderQuantity")) if tr is not None else None
    adjudicada_pyme = to_bool(text(tr, "cbc:SMEAwardedIndicator")) if tr is not None else None
    importe_oferta_menor = to_decimal(text(tr, "cbc:LowerTenderAmount")) if tr is not None else None
    importe_oferta_mayor = to_decimal(text(tr, "cbc:HigherTenderAmount")) if tr is not None else None

    # Adjudicatario
    wp = tr.find("cac:WinningParty", NS) if tr is not None else None
    adjudicatario_nombre = text(wp, "cac:PartyName/cbc:Name") if wp is not None else None
    adjudicatario_nif = text(wp, "cac:PartyIdentification/cbc:ID") if wp is not None else None
    adjudicatario_ciudad = text(wp, "cac:PhysicalLocation/cac:Address/cbc:CityName") if wp is not None else None
    adjudicatario_cp = text(wp, "cac:PhysicalLocation/cac:Address/cbc:PostalZone") if wp is not None else None

    # Contrato formalizado
    contrato = tr.find("cac:Contract", NS) if tr is not None else None
    contrato_id = text(contrato, "cbc:ID") if contrato is not None else None
    contrato_fecha = to_date(text(contrato, "cbc:IssueDate")) if contrato is not None else None

    awarded = tr.find("cac:AwardedTenderedProject/cac:LegalMonetaryTotal", NS) if tr is not None else None
    contrato_importe_sin_iva = to_decimal(text(awarded, "cbc:TaxExclusiveAmount")) if awarded is not None else None
    contrato_importe_total = to_decimal(text(awarded, "cbc:PayableAmount")) if awarded is not None else None

    # XML original del entry
    entry_xml = ET.tostring(entry, encoding="unicode")

    return {
        "id_plataforma": id_plataforma,
        "expediente": expediente,
        "uuid_ted": uuid_ted,
        "link_detalle": link_detalle,
        "estado": estado,
        "updated_at": updated_at,
        "anulada": False,
        "fecha_anulacion": None,
        "titulo": titulo,
        "resumen": resumen,
        "tipo_contrato": tipo_contrato,
        "subtipo_contrato": subtipo_contrato,
        "contrato_mixto": contrato_mixto,
        "cpv_codes": cpv_codes,
        "importe_total": importe_total,
        "importe_sin_impuestos": importe_sin_impuestos,
        "importe_estimado": importe_estimado,
        "moneda": moneda,
        "ubicacion_nuts": ubicacion_nuts,
        "ubicacion_comunidad": ubicacion_comunidad,
        "ubicacion_ciudad": ubicacion_ciudad,
        "ubicacion_cp": ubicacion_cp,
        "ubicacion_pais": ubicacion_pais,
        "fecha_inicio_ejecucion": fecha_inicio_ejecucion,
        "fecha_fin_ejecucion": fecha_fin_ejecucion,
        "organo_contratacion": organo_contratacion,
        "organo_nif": organo_nif,
        "organo_id_plataforma": organo_id_plataforma,
        "organo_web": organo_web,
        "organo_email": organo_email,
        "organo_telefono": organo_telefono,
        "organo_direccion": organo_direccion,
        "organo_ciudad": organo_ciudad,
        "organo_cp": organo_cp,
        "organo_perfil_url": organo_perfil_url,
        "tipo_organo": tipo_organo,
        "actividad_organo": actividad_organo,
        "procedimiento": procedimiento,
        "urgencia": urgencia,
        "forma_presentacion": forma_presentacion,
        "sistema_contratacion": sistema_contratacion,
        "metodo_envio": metodo_envio,
        "sobre_umbral": sobre_umbral,
        "fecha_limite_presentacion": fecha_limite_presentacion,
        "fecha_limite_documentacion": fecha_limite_documentacion,
        "resultado_codigo": resultado_codigo,
        "resultado_descripcion": resultado_descripcion,
        "fecha_adjudicacion": fecha_adjudicacion,
        "ofertas_recibidas": ofertas_recibidas,
        "ofertas_pymes": ofertas_pymes,
        "adjudicada_pyme": adjudicada_pyme,
        "importe_oferta_menor": importe_oferta_menor,
        "importe_oferta_mayor": importe_oferta_mayor,
        "adjudicatario_nombre": adjudicatario_nombre,
        "adjudicatario_nif": adjudicatario_nif,
        "adjudicatario_ciudad": adjudicatario_ciudad,
        "adjudicatario_cp": adjudicatario_cp,
        "contrato_id": contrato_id,
        "contrato_fecha": contrato_fecha,
        "contrato_importe_sin_iva": contrato_importe_sin_iva,
        "contrato_importe_total": contrato_importe_total,
        "financiacion_ue": financiacion_ue,
        "legislacion_nacional": legislacion_nacional,
        "legislacion_referencia": legislacion_referencia,
        "idioma": idioma,
        "subasta": subasta,
        "jerarquia_org": jerarquia_org,
        "fichero_origen": fichero_origen,
        "entry_xml": entry_xml,
    }


def parse_deleted_entry(deleted, fichero_origen):
    """Extrae datos de un <at:deleted-entry>."""
    ref = deleted.get("ref")
    when = deleted.get("when")
    comment_el = deleted.find("at:comment", NS)
    comment_type = comment_el.get("type") if comment_el is not None else None

    try:
        fecha_anulacion = datetime.fromisoformat(when) if when else None
    except ValueError:
        fecha_anulacion = None

    return {
        "id_plataforma": ref,
        "anulada": True,
        "fecha_anulacion": fecha_anulacion,
        "updated_at": fecha_anulacion,
        "estado": comment_type,  # Normalmente "ANULADA"
        "fichero_origen": fichero_origen,
    }


# ============================================================
# Nombre del fichero principal (siempre se lee, nunca se registra)
# ============================================================
FICHERO_PRINCIPAL = "licitacionesPerfilesContratanteCompleto3.atom"


# ============================================================
# Procesamiento de fichero ATOM
# ============================================================
def parse_atom_file(filepath):
    """Parsea un fichero ATOM y devuelve (entries, deleted_entries, total_entries, next_filename).
    Solo se devuelven entries que pasan los filtros de Canarias + CPV informático.
    Los deleted_entries se devuelven todos (se aplican solo si ya existen en BBDD).
    next_filename es el nombre del siguiente fichero en la cadena (rel="next"), o None.
    """
    fichero_origen = os.path.basename(filepath)
    log.info(f"Procesando fichero: {fichero_origen}")

    tree = ET.parse(filepath)
    root = tree.getroot()

    # Extraer link rel="next"
    next_filename = None
    for link in root.findall("atom:link", NS):
        if link.get("rel") == "next":
            next_filename = link.get("href")
            break

    total_entries = 0
    entries = []
    deleted = []

    for entry in root.findall("atom:entry", NS):
        total_entries += 1
        data = parse_entry(entry, fichero_origen)
        if data:
            entries.append(data)

    for del_entry in root.findall("at:deleted-entry", NS):
        data = parse_deleted_entry(del_entry, fichero_origen)
        if data:
            deleted.append(data)

    log.info(
        f"  -> {total_entries} entries totales, "
        f"{len(entries)} pasan filtros (Canarias+TI), "
        f"{len(deleted)} anuladas"
        + (f", next: {next_filename}" if next_filename else ", fin de cadena")
    )
    return entries, deleted, total_entries, next_filename


# ============================================================
# UPSERT en la base de datos
# ============================================================
COLUMNS = [
    "id_plataforma", "expediente", "uuid_ted", "link_detalle",
    "estado", "updated_at", "anulada", "fecha_anulacion",
    "titulo", "resumen", "tipo_contrato", "subtipo_contrato",
    "contrato_mixto", "cpv_codes",
    "importe_total", "importe_sin_impuestos", "importe_estimado", "moneda",
    "ubicacion_nuts", "ubicacion_comunidad", "ubicacion_ciudad",
    "ubicacion_cp", "ubicacion_pais",
    "fecha_inicio_ejecucion", "fecha_fin_ejecucion",
    "organo_contratacion", "organo_nif", "organo_id_plataforma",
    "organo_web", "organo_email", "organo_telefono",
    "organo_direccion", "organo_ciudad", "organo_cp",
    "organo_perfil_url", "tipo_organo", "actividad_organo",
    "procedimiento", "urgencia", "forma_presentacion",
    "sistema_contratacion", "metodo_envio", "sobre_umbral",
    "fecha_limite_presentacion", "fecha_limite_documentacion",
    "resultado_codigo", "resultado_descripcion", "fecha_adjudicacion",
    "ofertas_recibidas", "ofertas_pymes", "adjudicada_pyme",
    "importe_oferta_menor", "importe_oferta_mayor",
    "adjudicatario_nombre", "adjudicatario_nif",
    "adjudicatario_ciudad", "adjudicatario_cp",
    "contrato_id", "contrato_fecha",
    "contrato_importe_sin_iva", "contrato_importe_total",
    "financiacion_ue", "legislacion_nacional", "legislacion_referencia",
    "idioma", "subasta", "jerarquia_org",
    "fichero_origen", "entry_xml",
]

UPDATE_COLUMNS = [c for c in COLUMNS if c != "id_plataforma"]


def build_upsert_sql():
    """Construye la sentencia SQL de UPSERT."""
    cols = ", ".join(COLUMNS)
    placeholders = ", ".join(["%s"] * len(COLUMNS))
    updates = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in UPDATE_COLUMNS]
    )

    sql = f"""
        INSERT INTO licitacion ({cols})
        VALUES ({placeholders})
        ON CONFLICT (id_plataforma) DO UPDATE
        SET {updates},
            fecha_ultima_sync = NOW()
        WHERE licitacion.updated_at < EXCLUDED.updated_at
    """
    return sql


def build_anulacion_sql():
    """SQL para marcar licitaciones como anuladas.
    Solo actualiza si la licitación ya existe en la BBDD
    (es decir, si previamente pasó los filtros).
    """
    return """
        UPDATE licitacion
        SET anulada = TRUE,
            fecha_anulacion = %s,
            estado = COALESCE(%s, estado),
            fichero_origen = %s,
            fecha_ultima_sync = NOW()
        WHERE id_plataforma = %s
          AND (anulada = FALSE OR fecha_anulacion IS NULL OR fecha_anulacion < %s)
    """


# ============================================================
# Control de ficheros ya procesados
# ============================================================
def get_ficheros_procesados(cursor):
    """Devuelve el conjunto de nombres de ficheros ya procesados."""
    cursor.execute("SELECT nombre_fichero FROM fichero_procesado")
    return {row[0] for row in cursor.fetchall()}


def registrar_fichero_procesado(cursor, nombre_fichero, stats):
    """Registra un fichero como procesado con sus estadísticas."""
    cursor.execute("""
        INSERT INTO fichero_procesado
            (nombre_fichero, entries_totales, entries_filtradas,
             entries_insertadas, deleted_entries, anulaciones_aplicadas)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (nombre_fichero) DO UPDATE
        SET fecha_procesado = NOW(),
            entries_totales = EXCLUDED.entries_totales,
            entries_filtradas = EXCLUDED.entries_filtradas,
            entries_insertadas = EXCLUDED.entries_insertadas,
            deleted_entries = EXCLUDED.deleted_entries,
            anulaciones_aplicadas = EXCLUDED.anulaciones_aplicadas
    """, (
        nombre_fichero,
        stats["entries_totales"],
        stats["entries_filtradas"],
        stats["entries_insertadas"],
        stats["deleted_entries"],
        stats["anulaciones_aplicadas"],
    ))


def upsert_entries(cursor, entries):
    """Inserta o actualiza licitaciones en la BBDD."""
    if not entries:
        return 0

    sql = build_upsert_sql()
    inserted = 0

    for entry in entries:
        values = tuple(entry.get(c) for c in COLUMNS)
        cursor.execute(sql, values)
        inserted += cursor.rowcount

    return inserted


def process_deleted(cursor, deleted_entries):
    """Marca licitaciones como anuladas (solo si ya existen en BBDD)."""
    if not deleted_entries:
        return 0

    sql = build_anulacion_sql()
    updated = 0

    for d in deleted_entries:
        cursor.execute(sql, (
            d["fecha_anulacion"],
            d.get("estado"),
            d["fichero_origen"],
            d["id_plataforma"],
            d["fecha_anulacion"],
        ))
        updated += cursor.rowcount

    return updated


# ============================================================
# Main
# ============================================================
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Detectar flag --force para reprocesar ficheros ya leídos
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]

    # El argumento debe ser el directorio donde están los .atom
    directorio = args[0] if args else None
    if not directorio or not os.path.isdir(directorio):
        log.error(f"Se requiere un directorio válido con ficheros .atom: {directorio}")
        sys.exit(1)

    # Verificar que el fichero principal existe
    fichero_principal_path = os.path.join(directorio, FICHERO_PRINCIPAL)
    if not os.path.isfile(fichero_principal_path):
        log.error(f"No se encuentra el fichero principal: {fichero_principal_path}")
        sys.exit(1)

    log.info(f"Directorio de ficheros ATOM: {directorio}")
    log.info(f"Filtros activos:")
    log.info(f"  Geográfico — NUTS: {', '.join(NUTS_PREFIXES)}*  |  Keywords: {', '.join(GEO_KEYWORDS)}")
    log.info(f"  CPV        — Prefijos: {', '.join(CPV_IT_PREFIXES)}xxxxxx")
    if force:
        log.info(f"  Modo --force: se ignorará la tabla fichero_procesado")

    # Conectar a la BBDD
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        log.info("Conectado a PostgreSQL")
    except psycopg2.Error as e:
        log.error(f"Error conectando a PostgreSQL: {e}")
        sys.exit(1)

    total_insertadas = 0
    total_anuladas = 0
    total_procesados = 0

    try:
        cursor = conn.cursor()

        # Obtener ficheros ya procesados
        ya_procesados = get_ficheros_procesados(cursor)
        if ya_procesados:
            log.info(f"Ficheros registrados en BBDD: {len(ya_procesados)}")

        # -----------------------------------------------------------
        # 1. Siempre procesar el fichero principal
        # -----------------------------------------------------------
        entries, deleted, total_entries, next_filename = parse_atom_file(fichero_principal_path)

        affected = upsert_entries(cursor, entries)
        log.info(f"  -> {affected} registros insertados/actualizados")
        total_insertadas += affected

        anuladas = process_deleted(cursor, deleted)
        if anuladas:
            log.info(f"  -> {anuladas} licitaciones marcadas como anuladas")
        total_anuladas += anuladas
        total_procesados += 1
        # El fichero principal NO se registra en fichero_procesado

        # -----------------------------------------------------------
        # 2. Seguir la cadena rel="next"
        # -----------------------------------------------------------
        while next_filename:
            # Si ya está procesado y no es --force, detenemos
            if next_filename in ya_procesados and not force:
                log.info(f"Fichero '{next_filename}' ya procesado -> deteniendo cadena")
                break

            next_path = os.path.join(directorio, next_filename)
            if not os.path.isfile(next_path):
                log.warning(f"Fichero siguiente no encontrado en disco: {next_path} -> deteniendo cadena")
                break

            entries, deleted, total_entries, siguiente = parse_atom_file(next_path)

            affected = upsert_entries(cursor, entries)
            log.info(f"  -> {affected} registros insertados/actualizados")
            total_insertadas += affected

            anuladas = process_deleted(cursor, deleted)
            if anuladas:
                log.info(f"  -> {anuladas} licitaciones marcadas como anuladas")
            total_anuladas += anuladas

            # Registrar como procesado (solo los de la cadena, no el principal)
            registrar_fichero_procesado(cursor, next_filename, {
                "entries_totales": total_entries,
                "entries_filtradas": len(entries),
                "entries_insertadas": affected,
                "deleted_entries": len(deleted),
                "anulaciones_aplicadas": anuladas,
            })
            total_procesados += 1

            # Avanzar al siguiente eslabón
            next_filename = siguiente

        conn.commit()
        log.info("=" * 60)
        log.info(f"RESUMEN:")
        log.info(f"  Ficheros procesados (cadena):       {total_procesados}")
        log.info(f"  Registros insertados/actualizados:  {total_insertadas}")
        log.info(f"  Licitaciones anuladas:              {total_anuladas}")
        log.info("=" * 60)

    except Exception as e:
        conn.rollback()
        log.error(f"Error durante la importación: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        log.info("Conexión cerrada")


if __name__ == "__main__":
    main()
