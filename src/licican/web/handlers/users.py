from __future__ import annotations

from licican.access import has_capability
from licican.users import UserFilters, UsersDatabaseError, build_users_payload, change_user_state, create_user, delete_user, update_user
from licican.web.http import (
    Request,
    deny_html,
    deny_json,
    not_found,
    users_data_error_html,
)
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.users import render_users


def _visible_users_payload(request: Request, selected_user_id: str | None = None) -> dict[str, object]:
    return build_users_payload(
        filters=_parse_user_filters(request),
        page=_parse_users_page(request),
        page_size=_parse_users_page_size(request),
        selected_user_id=selected_user_id,
    )


def _parse_user_filters(request: Request):
    query = request.query
    return UserFilters(
        busqueda=(query.get("busqueda") or [None])[0],
        estado=(query.get("estado") or [None])[0],
        rol=(query.get("rol") or [None])[0],
    )


def _parse_users_page(request: Request) -> int:
    candidates = request.query.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def _parse_users_page_size(request: Request) -> int:
    candidates = request.query.get("page_size")
    if not candidates:
        return 10
    try:
        page_size = int(candidates[0])
    except ValueError:
        return 10
    return page_size if page_size in {5, 10, 25, 50} else 10


def _user_form_values(form_data: dict[str, list[str]]) -> dict[str, object]:
    return {
        "nombre": (form_data.get("nombre") or [""])[0],
        "apellidos": (form_data.get("apellidos") or [""])[0],
        "email": (form_data.get("email") or [""])[0],
        "username": (form_data.get("username") or [""])[0],
        "rol_principal": (form_data.get("rol_principal") or [""])[0],
        "estado": (form_data.get("estado") or ["pendiente"])[0],
    }


def _users_error_response(request: Request, start_response, message: str, status: str = "400 Bad Request", selected_user_id: str | None = None) -> list[bytes]:
    content = render_users(_visible_users_payload(request, selected_user_id=selected_user_id), request.base_path, message, None, request.access_context)
    return send_response(start_response, status, "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_users_page(request: Request, start_response, id: str | None = None) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return deny_html(request, start_response, "view_users")
    status_message = (request.query.get("mensaje") or [None])[0]
    selected_user_id = id
    try:
        if selected_user_id is None and request.path != "/usuarios":
            selected_user_id = request.path.rsplit("/", 1)[-1]
        payload = _visible_users_payload(request, selected_user_id=selected_user_id)
        content = render_users(payload, request.base_path, None, status_message, request.access_context)
    except UsersDatabaseError as exc:
        content = users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except Exception as exc:
        content = render_users(_visible_users_payload(request), request.base_path, str(exc), status_message, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_api_users(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_user_detail(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request, selected_user_id=id)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    user = payload.get("usuario_seleccionado")
    if user is None:
        return not_found(start_response)
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(user)))


def handle_create_user(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return deny_html(request, start_response, "manage_users")
    form_data = _user_form_values(read_form_data(request.environ))
    try:
        create_user(
            nombre=str(form_data["nombre"]),
            apellidos=str(form_data["apellidos"]),
            email=str(form_data["email"]),
            rol_principal=str(form_data["rol_principal"]),
            estado=str(form_data["estado"]),
        )
    except ValueError as exc:
        return _users_error_response(request, start_response, str(exc))
    except UsersDatabaseError as exc:
        content = users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+creado+y+registrado")


def handle_update_user(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return deny_html(request, start_response, "manage_users")
    form_data = _user_form_values(read_form_data(request.environ))
    try:
        update_user(
            id,
            nombre=str(form_data["nombre"]),
            apellidos=str(form_data["apellidos"]),
            email=str(form_data["email"]),
            username=str(form_data["username"]),
            rol_principal=str(form_data["rol_principal"]),
            estado=str(form_data["estado"]),
            nueva_contrasena=(form_data.get("nueva_contrasena") or [""])[0],
            confirmar_contrasena=(form_data.get("confirmar_contrasena") or [""])[0],
        )
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha actualizado {id}. {exc}", selected_user_id=id)
    except KeyError:
        return not_found(start_response)
    except UsersDatabaseError as exc:
        content = users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+actualizado")


def handle_change_user_state(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return deny_html(request, start_response, "manage_users")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado") or [""])[0]
    try:
        change_user_state(id, state)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha actualizado el estado de {id}. {exc}", selected_user_id=id)
    except KeyError:
        return not_found(start_response)
    except UsersDatabaseError as exc:
        content = users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Estado+de+usuario+actualizado")


def handle_delete_user(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return deny_html(request, start_response, "manage_users")
    try:
        delete_user(id)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha eliminado {id}. {exc}", selected_user_id=id)
    except KeyError:
        return not_found(start_response)
    except UsersDatabaseError as exc:
        content = users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+eliminado")
