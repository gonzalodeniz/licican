from __future__ import annotations

from licican.access import has_capability
from licican.config import resolve_pipeline_path
from licican.retention import RetentionDatabaseError, apply_retention_policy, build_retention_payload, update_retention_policy
from licican.web.http import Request, deny_html, retention_data_error_html
from licican.web.responses import build_url, html_body, read_form_data, send_redirect, send_response
from licican.web.templates.retention import render_retention_control


def handle_retention_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_retention"):
        return deny_html(request, start_response, "view_retention")
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        payload = build_retention_payload(pipeline_path=resolve_pipeline_path())
        content = render_retention_control(payload, request.base_path, None, status_message, request.access_context)
    except RetentionDatabaseError as exc:
        content = retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_update_retention_policy(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_retention"):
        return deny_html(request, start_response, "manage_retention")
    form_data = read_form_data(request.environ)
    raw_days = (form_data.get("antiguedad_dias") or [""])[0]
    mode = (form_data.get("modo") or [""])[0]
    try:
        antiguedad_dias = int(raw_days)
        update_retention_policy(antiguedad_dias=antiguedad_dias, modo=mode)
    except ValueError as exc:
        try:
            payload = build_retention_payload(pipeline_path=resolve_pipeline_path())
            content = render_retention_control(payload, request.base_path, str(exc), None, request.access_context)
            return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
        except RetentionDatabaseError as retention_exc:
            content = retention_data_error_html(request.base_path, str(retention_exc))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except RetentionDatabaseError as exc:
        content = retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/conservacion") + "?mensaje=Politica+de+conservacion+actualizada")


def handle_apply_retention_policy(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_retention"):
        return deny_html(request, start_response, "manage_retention")
    try:
        result = apply_retention_policy(pipeline_path=resolve_pipeline_path())
    except RetentionDatabaseError as exc:
        content = retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    message = f"Archivado aplicado: {result['archivadas']} licitaciones trasladadas"
    return send_redirect(start_response, build_url(request.base_path, "/conservacion") + f"?mensaje={message.replace(' ', '+')}")
