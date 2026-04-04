from __future__ import annotations

from licican.access import has_capability
from licican.alerts import load_alerts, summarize_alerts
from licican.config import resolve_alerts_path
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
    visible_alerts,
    visible_pipeline_payload,
)
from licican.web.responses import html_body, json_body, send_response
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.coverage import render_coverage
from licican.web.templates.detail import render_opportunity_detail
from licican.web.templates.kpis import render_kpis
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


def handle_kpis_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_kpis"):
        return deny_html(request, start_response, "view_kpis")
    try:
        catalog = build_catalog()
        _, alerts = load_alerts(resolve_alerts_path())
        source_coverage = load_source_coverage()
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))

    visible = visible_alerts(request, alerts)
    alerts_summary = summarize_alerts(visible)
    pipeline_payload = visible_pipeline_payload(request)
    coverage_summary = summary_by_status(source_coverage)
    coverage_visible = len(catalog["cobertura_aplicada"])
    coverage_mvp = coverage_summary["MVP"]
    active_alert_users = len({alert.usuario_id for alert in visible if alert.activa})
    if request.access_context.is_admin:
        alcance_general = "Indicadores globales"
    elif request.access_context.is_manager:
        alcance_general = "Indicadores del contexto operativo"
    else:
        alcance_general = "Indicadores del contexto propio"
    payload = {
        "rol_activo": request.access_context.role_label,
        "alcance": alcance_general,
        "modo_captura": "Mixto: cobertura visible automatizada y adopción/uso con primera consolidación manual si falta instrumentación completa.",
        "resumen": {
            "fuentes_mvp": f"{coverage_visible}/{coverage_mvp}",
            "cobertura_visible": f"{coverage_visible} fuentes",
            "alertas_activas": f"{alerts_summary['alertas_activas']} alertas",
            "pipeline_visible": f"{pipeline_payload['summary']['total_oportunidades']} oportunidades",
        },
        "indicadores": [
            {
                "nombre": "Cobertura de fuentes priorizadas",
                "valor_label": "Cobertura actual",
                "valor_actual": f"{coverage_visible}/{coverage_mvp}" if coverage_mvp else "Sin referencia",
                "definicion": "Porcentaje de fuentes MVP priorizadas que producen datos visibles y trazables en la ventana de evaluacion.",
                "formula": "fuentes_MVP_con_datos / fuentes_MVP_priorizadas x 100",
                "umbral_inicial": "90 por ciento",
                "decision": "Si cae por debajo del umbral, frenar expansion y estabilizar trazabilidad e ingestion.",
                "captura": "Automatica sobre la cobertura visible del catalogo y la configuracion del MVP.",
                "limitacion": "La medicion actual usa la cobertura visible del producto y no sustituye una telemetria completa de disponibilidad.",
            },
            {
                "nombre": "Adopcion de alertas activas",
                "valor_label": "Usuarios con alerta activa",
                "valor_actual": f"{active_alert_users} usuarios" if alerts_summary["alertas_activas"] else "Sin alertas activas",
                "definicion": "Porcentaje de usuarios activos semanales que disponen de al menos una alerta activa.",
                "formula": "usuarios_activos_con_alerta_activa / usuarios_activos_semanales x 100",
                "umbral_inicial": "30 por ciento",
                "decision": "Si baja del umbral, simplificar onboarding y configuracion de alertas.",
                "captura": "Consolidacion operativa de alertas activas y usuarios con alerta en la captura actual.",
                "limitacion": "No existe todavia telemetria completa de usuarios activos semanales; la primera captura puede ser manual.",
            },
            {
                "nombre": "Uso recurrente de consulta",
                "valor_label": "Captura actual",
                "valor_actual": "Pendiente de consolidacion manual",
                "definicion": "Frecuencia semanal de consultas de catalogo o detalle por usuario activo.",
                "formula": "consultas_catalogo_o_detalle_semana / usuarios_activos_semanales",
                "umbral_inicial": "1 interaccion semanal por usuario activo",
                "decision": "Si baja del umbral, revisar relevancia, navegacion y encaje funcional antes de ampliar cobertura.",
                "captura": "Consolidacion manual temporal o instrumentacion posterior de sesiones.",
                "limitacion": "La aplicacion aun no recoge una telemetria fina de consultas de catalogo o detalle, por lo que la primera medicion puede ser manual.",
            },
        ],
    }
    content = render_kpis(payload, request.base_path, request.access_context)
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
                "consulta": "Catalogo, detalle, KPIs, alertas y pipeline.",
                "gestion": "Puede crear y editar alertas propias o de otros contextos, y operar el pipeline.",
                "gobierno": "Puede revisar la matriz de permisos y las restricciones visibles.",
            },
            {
                "rol": "Manager",
                "consulta": "Catalogo, detalle, alertas, pipeline y KPIs operativos.",
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
                "gobierno": "No accede a vistas operativas de permisos ni KPIs.",
            },
        ],
    }
    content = render_permissions_matrix(payload, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))
