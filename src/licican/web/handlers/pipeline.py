from __future__ import annotations

from licican.access import has_capability
from licican.config import resolve_pipeline_path
from licican.pipeline import add_opportunity_to_pipeline, update_pipeline_entry_status
from licican.web.http import Request, deny_html, deny_json, not_found, visible_pipeline_payload
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.pipeline import render_pipeline


def handle_api_pipeline(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return deny_json(start_response, "view_pipeline")
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(visible_pipeline_payload(request))))


def handle_pipeline_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return deny_html(request, start_response, "view_pipeline")
    status_message = (request.query.get("mensaje") or [None])[0]
    content = render_pipeline(visible_pipeline_payload(request), request.base_path, None, status_message, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_create_pipeline_entry(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    opportunity_id = (form_data.get("opportunity_id") or [""])[0].strip()
    try:
        _, created = add_opportunity_to_pipeline(opportunity_id, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return not_found(start_response)

    message = "Oportunidad guardada en el pipeline" if created else "La oportunidad ya estaba guardada en el pipeline"
    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + f"?mensaje={message.replace(' ', '+')}")


def handle_update_pipeline_entry(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado_seguimiento") or [""])[0]
    try:
        update_pipeline_entry_status(id, state, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return deny_html(request, start_response, "manage_pipeline")

    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + "?mensaje=Estado+de+pipeline+actualizado")
