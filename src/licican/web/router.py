from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import parse_qs

from licican.alerts import create_alert, deactivate_alert, load_alerts, summarize_alerts, update_alert
from licican.canarias_dataset import build_adjudicacion_detail, build_licitacion_detail, load_canarias_dataset
from licican.config import normalize_base_path, resolve_alerts_path, resolve_base_path
from licican.opportunity_catalog import CatalogDataSourceError, build_catalog, build_opportunity_detail
from licican.real_source_prioritization import load_real_source_prioritization, summarize_prioritization
from licican.shared.filters import CatalogFilters
from licican.source_coverage import load_source_coverage, summary_by_status
from licican.ti_classification import audit_examples, load_rule_set
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.alerts import render_alerts
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.coverage import render_coverage
from licican.web.templates.dataset import render_datos_consolidados
from licican.web.templates.detail import render_adjudicacion_detail, render_licitacion_detail, render_opportunity_detail
from licican.web.templates.prioritization import render_prioritization
from licican.web.templates.base import page_template

STATIC_DIR = Path(__file__).resolve().parent / "static"
Route = namedtuple("Route", ["method", "pattern", "handler"])


@dataclass(frozen=True)
class Request:
    environ: dict[str, object]
    method: str
    path: str
    base_path: str
    query: dict[str, list[str]]


def _parse_filters_from_multidict(values: dict[str, list[str]]) -> CatalogFilters:
    def first(name: str) -> str | None:
        candidates = values.get(name)
        if not candidates:
            return None
        value = candidates[0].strip()
        return value or None

    def integer(name: str) -> int | None:
        value = first(name)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    return CatalogFilters(
        palabra_clave=first("palabra_clave"),
        presupuesto_min=integer("presupuesto_min"),
        presupuesto_max=integer("presupuesto_max"),
        procedimiento=first("procedimiento"),
        ubicacion=first("ubicacion"),
    )


def _parse_catalog_filters(request: Request) -> CatalogFilters:
    return _parse_filters_from_multidict(request.query)


def _parse_catalog_page(request: Request) -> int:
    candidates = request.query.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def _parse_catalog_page_size(request: Request) -> int:
    candidates = request.query.get("page_size")
    if not candidates:
        return 10
    try:
        page_size = int(candidates[0])
    except ValueError:
        return 10
    return page_size if page_size in {5, 10, 25, 50} else 10


def _resolve_request_path(environ: dict[str, object], base_path: str) -> str:
    raw_path = str(environ.get("PATH_INFO", "/") or "/")
    script_name = normalize_base_path(str(environ.get("SCRIPT_NAME") or "")) or base_path
    if script_name and raw_path.startswith(script_name):
        raw_path = raw_path[len(script_name):] or "/"
    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"
    return raw_path or "/"


def _not_found(start_response) -> list[bytes]:
    return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", b"No encontrado")


def _catalog_data_error_html(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Fuente temporalmente no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La aplicacion no ha podido consultar la fuente de datos operativa configurada para el catalogo. Revisa la conexion a PostgreSQL o la configuracion del backend antes de reintentar.</p>
          <p>Ruta afectada del catalogo: <code>{escape(build_url(base_path, '/api/oportunidades'))}</code></p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Catalogo temporalmente no disponible",
        "Catalogo temporalmente no disponible",
        "Servicio de datos no disponible",
        "El catalogo y el detalle requieren acceso a la fuente de datos configurada para la aplicacion.",
        content,
        current_path="/",
        base_path=base_path,
    )


def handle_static(request: Request, start_response, filename: str) -> list[bytes]:
    relative_path = filename
    static_path = (STATIC_DIR / relative_path).resolve()
    if not str(static_path).startswith(str(STATIC_DIR.resolve())) or not static_path.is_file():
        return _not_found(start_response)
    content_type = "text/css; charset=utf-8" if static_path.suffix == ".css" else "application/octet-stream"
    return send_response(start_response, "200 OK", content_type, static_path.read_bytes())


def handle_api_dataset(request: Request, start_response) -> list[bytes]:
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(load_canarias_dataset())))


def handle_api_alerts(request: Request, start_response) -> list[bytes]:
    reference, alerts = load_alerts(resolve_alerts_path())
    payload = {"referencia_funcional": reference, "summary": summarize_alerts(alerts), "alerts": [alert.to_payload() for alert in alerts]}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_alerts_page(request: Request, start_response) -> list[bytes]:
    filters = _parse_catalog_filters(request)
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        summary = summarize_alerts(alerts)
        content = render_alerts(reference, alerts, summary, available_filters, request.base_path, filters.normalized().active_filters(), None, status_message)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_create_alert(request: Request, start_response) -> list[bytes]:
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        create_alert(form_filters, path=resolve_alerts_path())
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        summary = summarize_alerts(alerts)
        content = render_alerts(reference, alerts, summary, available_filters, request.base_path, form_filters.normalized().active_filters(), str(exc), None)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+creada+y+activa")


def handle_update_alert(request: Request, start_response, id: str) -> list[bytes]:
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        update_alert(id, form_filters, path=resolve_alerts_path())
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        summary = summarize_alerts(alerts)
        content = render_alerts(reference, alerts, summary, available_filters, request.base_path, {}, f"No se ha actualizado {id}. {exc}", None)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+actualizada")


def handle_deactivate_alert(request: Request, start_response, id: str) -> list[bytes]:
    try:
        deactivate_alert(id, path=resolve_alerts_path())
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+desactivada")


def handle_api_opportunities(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=_parse_catalog_filters(request),
            page=_parse_catalog_page(request),
            page_size=_parse_catalog_page_size(request),
        )
    except CatalogDataSourceError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    status = "400 Bad Request" if payload["error_validacion"] else "200 OK"
    return send_response(start_response, status, "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_opportunity_detail(request: Request, start_response, id: str) -> list[bytes]:
    try:
        detail = build_opportunity_detail(id)
    except CatalogDataSourceError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    if detail is None:
        return _not_found(start_response)
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(detail)))


def handle_api_sources(request: Request, start_response) -> list[bytes]:
    sources = load_source_coverage()
    payload = {"sources": [source.__dict__ for source in sources], "summary": summary_by_status(sources)}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_prioritized_sources(request: Request, start_response) -> list[bytes]:
    reference, sources, out_of_scope = load_real_source_prioritization()
    payload = {"referencia_funcional": reference, "sources": [source.__dict__ for source in sources], "summary": summarize_prioritization(sources), "fuera_de_alcance": list(out_of_scope)}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_classification(request: Request, start_response) -> list[bytes]:
    rules = load_rule_set()
    payload = {
        "referencia_funcional": rules.referencia_funcional,
        "reglas": {
            "inclusion_palabras_clave": list(rules.inclusion_palabras_clave),
            "inclusion_cpv_prefixes": list(rules.inclusion_cpv_prefixes),
            "inclusion_necesidades_explicitas": list(rules.inclusion_necesidades_explicitas),
            "exclusion_palabras_clave": list(rules.exclusion_palabras_clave),
            "casos_frontera": list(rules.frontera_palabras_clave),
        },
        "ejemplos_auditados": audit_examples(rules),
    }
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_classification_page(request: Request, start_response) -> list[bytes]:
    rules = load_rule_set()
    content = render_classification(rules.referencia_funcional, rules, audit_examples(rules), request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_coverage_page(request: Request, start_response) -> list[bytes]:
    sources = load_source_coverage()
    content = render_coverage(sources, summary_by_status(sources), request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_prioritization_page(request: Request, start_response) -> list[bytes]:
    reference, sources, out_of_scope = load_real_source_prioritization()
    content = render_prioritization(reference, sources, out_of_scope, summarize_prioritization(sources), request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_dataset_page(request: Request, start_response) -> list[bytes]:
    dataset = load_canarias_dataset()
    selected_view = (request.query.get("vista") or ["licitaciones"])[0]
    selected_view = selected_view if selected_view in {"licitaciones", "lotes", "adjudicaciones"} else "licitaciones"
    if selected_view == "licitaciones":
        rows = dataset["licitaciones"]
        columns = [("id_expediente", "ID Expediente"), ("titulo", "Título"), ("estado", "Estado"), ("organo_contratacion", "Órgano Contratación"), ("importe_sin_iva", "Importe sin IVA"), ("procedimiento", "Procedimiento"), ("plazo_presentacion", "Plazo Presentación"), ("numero_lotes", "Nº Lotes"), ("numero_adjudicaciones", "Nº Adjudicaciones"), ("fichero_origen_atom", "Fichero Origen")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/licitaciones/{item["slug"]}"))}">Ver detalle</a>' for item in rows]
        heading = "Licitaciones TI Canarias"
        description = "La vista replica la hoja principal del Excel versionado y expone el expediente, su estado, el órgano contratante, los importes clave y el fichero `.atom` consolidado visible para trazabilidad."
    elif selected_view == "lotes":
        rows = dataset["lotes"]
        columns = [("id_expediente", "ID Expediente"), ("titulo_licitacion", "Título Licitación"), ("numero_lote", "Nº Lote"), ("nombre_lote", "Nombre Lote"), ("importe_sin_iva", "Importe sin IVA (€)"), ("importe_con_iva", "Importe con IVA (€)"), ("cpvs", "CPVs"), ("ubicacion", "Ubicación"), ("criterios_adjudicacion", "Criterios Adjudicación")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/licitaciones/{item["licitacion_slug"]}"))}">Ver licitación</a>' for item in rows]
        heading = "Detalle Lotes"
        description = "La hoja de lotes permite revisar el desglose funcional de cada expediente por lote, manteniendo importes, ubicación, CPVs y criterios de adjudicación."
    else:
        rows = dataset["adjudicaciones"]
        columns = [("id_expediente", "ID Expediente"), ("titulo", "Título"), ("fecha_adjudicacion", "Fecha Adjudicación"), ("lote", "Lote"), ("ganador", "Ganador"), ("importe_adjudicacion_sin_iva", "Importe Adj. sin IVA"), ("importe_adjudicacion_total", "Importe Adj. Total"), ("id_contrato", "ID Contrato"), ("fichero_origen_atom", "Fichero Origen")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/adjudicaciones/{item["slug"]}"))}">Ver contrato</a>' for item in rows]
        heading = "Adjudicaciones"
        description = "La hoja de adjudicaciones expone el resultado contractual visible para la muestra actual, incluyendo adjudicatario, importes, lote y trazabilidad al origen cuando la licitación asociada la aporta."
    content = render_datos_consolidados(dataset, selected_view, heading, description, columns, actions, rows, request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_licitacion_detail(request: Request, start_response, id: str) -> list[bytes]:
    detail = build_licitacion_detail(id)
    if detail is None:
        return _not_found(start_response)
    content = render_licitacion_detail(detail, request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_adjudicacion_detail(request: Request, start_response, id: str) -> list[bytes]:
    detail = build_adjudicacion_detail(id)
    if detail is None:
        return _not_found(start_response)
    content = render_adjudicacion_detail(detail, request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_catalog_page(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=_parse_catalog_filters(request),
            page=_parse_catalog_page(request),
            page_size=_parse_catalog_page_size(request),
        )
        content = render_catalog(payload, request.base_path)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_opportunity_detail(request: Request, start_response, id: str) -> list[bytes]:
    try:
        detail = build_opportunity_detail(id)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    if detail is None:
        return _not_found(start_response)
    content = render_opportunity_detail(detail, request.base_path)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


routes = [
    Route("GET", "/static/{filename}", handle_static),
    Route("GET", "/api/datos-consolidados", handle_api_dataset),
    Route("GET", "/api/alertas", handle_api_alerts),
    Route("POST", "/alertas", handle_create_alert),
    Route("POST", "/alertas/{id}/editar", handle_update_alert),
    Route("POST", "/alertas/{id}/desactivar", handle_deactivate_alert),
    Route("GET", "/api/oportunidades/{id}", handle_api_opportunity_detail),
    Route("GET", "/api/oportunidades", handle_api_opportunities),
    Route("GET", "/api/fuentes", handle_api_sources),
    Route("GET", "/api/fuentes-prioritarias", handle_api_prioritized_sources),
    Route("GET", "/api/clasificacion-ti", handle_api_classification),
    Route("GET", "/clasificacion-ti", handle_classification_page),
    Route("GET", "/cobertura-fuentes", handle_coverage_page),
    Route("GET", "/priorizacion-fuentes-reales", handle_prioritization_page),
    Route("GET", "/alertas", handle_alerts_page),
    Route("GET", "/datos-consolidados", handle_dataset_page),
    Route("GET", "/datos-consolidados/licitaciones/{id}", handle_licitacion_detail),
    Route("GET", "/datos-consolidados/adjudicaciones/{id}", handle_adjudicacion_detail),
    Route("GET", "/oportunidades/{id}", handle_opportunity_detail),
    Route("GET", "/", handle_catalog_page),
]


def _match_pattern(path: str, pattern: str) -> dict[str, str] | None:
    path_parts = [part for part in path.strip("/").split("/") if part]
    pattern_parts = [part for part in pattern.strip("/").split("/") if part]
    if pattern == "/":
        return {} if path == "/" else None
    if len(path_parts) != len(pattern_parts):
        return None
    params: dict[str, str] = {}
    for path_part, pattern_part in zip(path_parts, pattern_parts):
        if pattern_part.startswith("{") and pattern_part.endswith("}"):
            params[pattern_part[1:-1]] = path_part
            continue
        if path_part != pattern_part:
            return None
    return params


def application(environ, start_response):
    base_path = resolve_base_path()
    request = Request(
        environ=environ,
        method=(environ.get("REQUEST_METHOD", "GET") or "GET").upper(),
        path=_resolve_request_path(environ, base_path),
        base_path=base_path,
        query=parse_qs(str(environ.get("QUERY_STRING", "")), keep_blank_values=False),
    )
    for route in routes:
        if route.method != request.method:
            continue
        params = _match_pattern(request.path, route.pattern)
        if params is None:
            continue
        return route.handler(request, start_response, **params)
    return _not_found(start_response)
