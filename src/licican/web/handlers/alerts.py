from __future__ import annotations

from licican.access import has_capability
from licican.alerts import create_alert, deactivate_alert, load_alerts, summarize_alerts, update_alert
from licican.config import resolve_alerts_path
from licican.opportunity_catalog import CatalogDataSourceError, build_catalog
from licican.web.http import (
    Request,
    catalog_data_error_html,
    deny_html,
    deny_json,
    not_found,
    parse_filters_from_multidict,
    visible_alerts,
)
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.alerts import render_alerts


def _render_alerts_page(
    request: Request,
    *,
    form_active_filters: dict[str, object],
    form_error: str | None = None,
    status_message: str | None = None,
) -> str:
    reference, alerts = load_alerts(resolve_alerts_path())
    visible = visible_alerts(request, alerts)
    available_filters = build_catalog()["filtros_disponibles"]
    summary = summarize_alerts(visible)
    return render_alerts(
        reference,
        visible,
        summary,
        available_filters,
        request.base_path,
        form_active_filters,
        form_error,
        status_message,
        request.access_context,
    )


def handle_api_alerts(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return deny_json(start_response, "view_alerts")
    reference, alerts = load_alerts(resolve_alerts_path())
    visible = visible_alerts(request, alerts)
    payload = {
        "referencia_funcional": reference,
        "summary": summarize_alerts(visible),
        "alerts": [alert.to_payload() for alert in visible],
    }
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_alerts_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return deny_html(request, start_response, "view_alerts")
    filters = parse_filters_from_multidict(request.query)
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        content = _render_alerts_page(
            request,
            form_active_filters=filters.normalized().active_filters(),
            status_message=status_message,
        )
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_create_alert(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return deny_html(request, start_response, "manage_alerts")
    form_filters = parse_filters_from_multidict(read_form_data(request.environ))
    try:
        create_alert(form_filters, path=resolve_alerts_path(), user_id=request.access_context.user_id)
    except ValueError as exc:
        content = _render_alerts_page(
            request,
            form_active_filters=form_filters.normalized().active_filters(),
            form_error=str(exc),
        )
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+creada+y+activa")


def handle_update_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return deny_html(request, start_response, "manage_alerts")
    form_filters = parse_filters_from_multidict(read_form_data(request.environ))
    try:
        update_alert(
            id,
            form_filters,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except ValueError as exc:
        content = _render_alerts_page(
            request,
            form_active_filters={},
            form_error=f"No se ha actualizado {id}. {exc}",
        )
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except PermissionError:
        return deny_html(request, start_response, "manage_alerts")
    except CatalogDataSourceError as exc:
        content = catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+actualizada")


def handle_deactivate_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return deny_html(request, start_response, "manage_alerts")
    try:
        deactivate_alert(
            id,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except PermissionError:
        return deny_html(request, start_response, "manage_alerts")
    except KeyError:
        return not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+desactivada")
