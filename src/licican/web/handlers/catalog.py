from __future__ import annotations

from licican.access import has_capability
from licican.opportunity_catalog import CatalogDataSourceError, build_catalog, build_opportunity_detail
from licican.real_source_prioritization import load_real_source_prioritization, summarize_prioritization
from licican.source_coverage import load_source_coverage, summary_by_status
from licican.ti_classification import audit_examples, load_rule_set
from licican.web.http import (
    Request,
    catalog_data_error_html,
    deny_html,
    deny_json,
    not_found,
    parse_catalog_filters,
    parse_catalog_page,
    parse_catalog_page_size,
)
from licican.web.responses import html_body, json_body, send_response
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.coverage import render_coverage
from licican.web.templates.detail import render_opportunity_detail
from licican.web.templates.permissions import render_permissions_matrix
from licican.web.templates.prioritization import render_prioritization


def handle_api_opportunities(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=parse_catalog_filters(request),
            page=parse_catalog_page(request),
            page_size=parse_catalog_page_size(request),
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
        return not_found(start_response)
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
    content = render_classification(rules.referencia_funcional, rules, audit_examples(rules), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_coverage_page(request: Request, start_response) -> list[bytes]:
    sources = load_source_coverage()
    content = render_coverage(sources, summary_by_status(sources), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_prioritization_page(request: Request, start_response) -> list[bytes]:
    reference, sources, out_of_scope = load_real_source_prioritization()
    content = render_prioritization(reference, sources, out_of_scope, summarize_prioritization(sources), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_catalog_page(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=parse_catalog_filters(request),
            page=parse_catalog_page(request),
            page_size=parse_catalog_page_size(request),
        )
        content = render_catalog(payload, request.base_path, request.access_context)
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_opportunity_detail(request: Request, start_response, id: str) -> list[bytes]:
    try:
        detail = build_opportunity_detail(id)
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    if detail is None:
        return not_found(start_response)
    content = render_opportunity_detail(detail, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))



def handle_permissions_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_permissions"):
        return deny_html(request, start_response, "view_permissions")
    payload = {
        "rol_activo": request.access_context.role_label,
        "usuario_activo": request.access_context.user_id,
        "matriz": [
            {
                "rol": "Administrador",
                "consulta": "Catalogo, detalle, alertas y pipeline.",
                "gestion": "Puede crear y editar alertas propias o de otros contextos, y operar el pipeline.",
                "gobierno": "Puede revisar la matriz de permisos y las restricciones visibles.",
            },
            {
                "rol": "Manager",
                "consulta": "Catalogo, detalle, alertas y pipeline.",
                "gestion": "Puede gestionar alertas y pipeline operativos.",
                "gobierno": "No accede a administracion global de usuarios ni permisos.",
            },
            {
                "rol": "Colaborador",
                "consulta": "Catalogo, detalle, alertas y pipeline en modo consulta.",
                "gestion": "No puede crear ni modificar alertas, pipeline ni configuracion.",
                "gobierno": "No accede a administracion global de permisos ni usuarios.",
            },
            {
                "rol": "Invitado",
                "consulta": "Catalogo y detalle.",
                "gestion": "No puede crear ni modificar alertas, pipeline ni configuracion.",
                "gobierno": "No accede a vistas operativas de permisos.",
            },
        ],
    }
    content = render_permissions_matrix(payload, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))
