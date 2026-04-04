from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
import logging
from pathlib import Path
from urllib.parse import parse_qs

from licican.access import AccessContext, has_capability, resolve_access_context
from licican.alerts import create_alert, deactivate_alert, filter_alerts_by_user, load_alerts, summarize_alerts, update_alert
from licican.auth.config import get_auth_settings
from licican.auth.csrf import ensure_csrf_token, validate_csrf_token
from licican.auth.rate_limiter import rate_limiter
from licican.auth.service import AuthenticationError, authenticate_user, synchronize_superadmin_account
from licican.auth.session import SessionState, clear_session, load_session, now_iso, persist_session_headers, timeout_exceeded
from licican.config import normalize_base_path, resolve_alerts_path, resolve_base_path, resolve_pipeline_path
from licican.opportunity_catalog import CatalogDataSourceError, build_catalog, build_opportunity_detail
from licican.pipeline import add_opportunity_to_pipeline, build_pipeline_payload, update_pipeline_entry_status
from licican.retention import (
    RetentionDatabaseError,
    apply_retention_policy,
    build_retention_payload,
    update_retention_policy,
)
from licican.real_source_prioritization import load_real_source_prioritization, summarize_prioritization
from licican.shared.filters import CatalogFilters
from licican.source_coverage import load_source_coverage, summary_by_status
from licican.ti_classification import audit_examples, load_rule_set
from licican.users import UsersDatabaseError, UserFilters, build_users_payload, change_user_state, create_user, delete_user, update_user
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.alerts import render_alerts
from licican.web.templates.base import page_template
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.coverage import render_coverage
from licican.web.templates.detail import render_opportunity_detail
from licican.web.templates.kpis import render_kpis
from licican.web.templates.permissions import render_permissions_matrix
from licican.web.templates.pipeline import render_pipeline
from licican.web.templates.prioritization import render_prioritization
from licican.web.templates.retention import render_retention_control
from licican.web.templates.users import render_users
from licican.web.templates.login import render_login

STATIC_DIR = Path(__file__).resolve().parent / "static"
Route = namedtuple("Route", ["method", "pattern", "handler"])
LOGGER = logging.getLogger(__name__)
PUBLIC_PATH_PREFIXES = ("/static/",)
PUBLIC_PATHS = frozenset({"/login"})


@dataclass(frozen=True)
class Request:
    environ: dict[str, object]
    method: str
    path: str
    base_path: str
    query: dict[str, list[str]]
    access_context: AccessContext
    session_state: SessionState

    @property
    def session(self) -> dict[str, object]:
        return self.session_state.session


def _is_public_path(path: str) -> bool:
    return path in PUBLIC_PATHS or any(path.startswith(prefix) for prefix in PUBLIC_PATH_PREFIXES)


def _is_authenticated(session: dict[str, object]) -> bool:
    return bool(session.get("username"))


def _secure_request(environ: dict[str, object]) -> bool:
    scheme = str(environ.get("wsgi.url_scheme", "http") or "http").lower()
    forwarded_proto = str(environ.get("HTTP_X_FORWARDED_PROTO", "") or "").lower()
    return scheme == "https" or forwarded_proto == "https"


def _client_ip(environ: dict[str, object]) -> str:
    forwarded_for = str(environ.get("HTTP_X_FORWARDED_FOR", "") or "").strip()
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return str(environ.get("REMOTE_ADDR", "") or "unknown")


def _redirect(start_response, location: str) -> list[bytes]:
    return send_response(
        start_response,
        "302 Found",
        "text/plain; charset=utf-8",
        b"",
        extra_headers=[("Location", location)],
    )


def _forbidden(start_response, message: str = "CSRF invalido") -> list[bytes]:
    return send_response(start_response, "403 Forbidden", "text/plain; charset=utf-8", message.encode("utf-8"))


def _activate_superadmin_session(request: Request) -> Request:
    settings = get_auth_settings()
    synchronize_superadmin_account(settings)
    request.session.clear()
    request.session.update(
        {
            "username": settings.login_superadmin_name,
            "rol": "superadmin",
            "nombre_completo": "Superadministrador",
            "is_superadmin": True,
            "last_activity": now_iso(),
            "auto_login_active": True,
        }
    )
    ensure_csrf_token(request.session)
    request.session_state.should_persist = True
    return Request(
        environ=request.environ,
        method=request.method,
        path=request.path,
        base_path=request.base_path,
        query=request.query,
        access_context=resolve_access_context(request.environ, request.query, session_user=request.session),
        session_state=request.session_state,
    )


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


def _parse_user_filters(request: Request) -> UserFilters:
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


def _access_denied_html(request: Request, capability: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Acceso bloqueado por permisos</strong><br />
        El rol activo <strong>{escape(request.access_context.role_label)}</strong> no puede ejecutar la accion requerida para <code>{escape(capability)}</code>.
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La aplicacion mantiene visibles solo las acciones compatibles con el rol actual y bloquea de forma consistente los intentos de gestion no autorizados.</p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Acceso restringido",
        "Acceso restringido por rol",
        "PB-013 · Restriccion consistente de acciones",
        "La accion solicitada no esta disponible para el rol funcional activo.",
        content,
        current_path=request.path,
        base_path=request.base_path,
        access_context=request.access_context,
    )


def _deny_html(request: Request, start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "text/html; charset=utf-8",
        b"".join(html_body(_access_denied_html(request, capability))),
    )


def _deny_json(start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "application/json; charset=utf-8",
        b"".join(json_body({"error": f"Acceso restringido por permisos para {capability}."})),
    )


def _visible_alerts(request: Request, alerts):
    return alerts if request.access_context.is_admin else filter_alerts_by_user(alerts, request.access_context.user_id)


def _visible_pipeline_payload(request: Request) -> dict[str, object]:
    return build_pipeline_payload(
        path=resolve_pipeline_path(),
        usuario_id=None if request.access_context.is_admin else request.access_context.user_id,
    )


def _visible_users_payload(request: Request, selected_user_id: str | None = None) -> dict[str, object]:
    return build_users_payload(
        filters=_parse_user_filters(request),
        page=_parse_users_page(request),
        page_size=_parse_users_page_size(request),
        selected_user_id=selected_user_id,
    )


def _users_data_error_html(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Base de datos de usuarios no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La gestion de usuarios depende de PostgreSQL y no puede renderizarse mientras la conexion no responda.</p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Usuarios temporalmente no disponibles",
        "Usuarios temporalmente no disponibles",
        "Servicio de datos no disponible",
        "El modulo de gestion de usuarios requiere acceso a la base de datos configurada.",
        content,
        current_path="/usuarios",
        base_path=base_path,
    )


def handle_login_page(request: Request, start_response) -> list[bytes]:
    if _is_authenticated(request.session):
        return _redirect(start_response, build_url(request.base_path, "/"))
    ensure_csrf_token(request.session)
    request.session_state.should_persist = True
    reason = (request.query.get("reason") or [None])[0]
    content = render_login(
        base_path=request.base_path,
        csrf_token=str(request.session.get("csrf_token") or ""),
        reason=reason,
    )
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_login_submit(request: Request, start_response) -> list[bytes]:
    form_data = read_form_data(request.environ)
    if not validate_csrf_token(request.session, (form_data.get("csrf_token") or [None])[0]):
        return _forbidden(start_response)

    client_ip = _client_ip(request.environ)
    if rate_limiter.is_limited(client_ip):
        return send_response(
            start_response,
            "429 Too Many Requests",
            "text/html; charset=utf-8",
            b"".join(
                html_body(
                    render_login(
                        base_path=request.base_path,
                        csrf_token=ensure_csrf_token(request.session),
                        error_message="Demasiados intentos. Espere unos minutos.",
                    )
                )
            ),
        )

    settings = get_auth_settings()
    username = (form_data.get("username") or [""])[0]
    password = (form_data.get("password") or [""])[0]
    try:
        user = authenticate_user(username, password, settings)
    except AuthenticationError as exc:
        if exc.code != "database_error":
            rate_limiter.register_failure(client_ip)
        request.session_state.should_persist = True
        return send_response(
            start_response,
            "401 Unauthorized",
            "text/html; charset=utf-8",
            b"".join(
                html_body(
                    render_login(
                        base_path=request.base_path,
                        csrf_token=ensure_csrf_token(request.session),
                        error_message=str(exc),
                    )
                )
            ),
        )

    rate_limiter.reset(client_ip)
    request.session.clear()
    ensure_csrf_token(request.session)
    request.session.update(
        {
            "username": user.username,
            "rol": user.rol,
            "nombre_completo": user.nombre_completo,
            "is_superadmin": user.is_superadmin,
            "last_activity": now_iso(),
            "auto_login_active": False,
        }
    )
    request.session_state.should_persist = True
    return _redirect(start_response, build_url(request.base_path, "/"))


def handle_logout(request: Request, start_response) -> list[bytes]:
    form_data = read_form_data(request.environ)
    if not validate_csrf_token(request.session, (form_data.get("csrf_token") or [None])[0]):
        return _forbidden(start_response)
    clear_session(request.session_state)
    return _redirect(start_response, build_url(request.base_path, "/login?reason=logout"))


def _retention_data_error_html(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Control de conservacion no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La politica de retencion y el archivado requieren acceso operativo a PostgreSQL.</p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Conservacion temporalmente no disponible",
        "Conservacion temporalmente no disponible",
        "Servicio de datos no disponible",
        "La gestion de conservacion y archivado depende de la base de datos operativa.",
        content,
        current_path="/conservacion",
        base_path=base_path,
    )


def handle_static(request: Request, start_response, filename: str) -> list[bytes]:
    relative_path = filename
    static_path = (STATIC_DIR / relative_path).resolve()
    if not str(static_path).startswith(str(STATIC_DIR.resolve())) or not static_path.is_file():
        return _not_found(start_response)
    content_type = "text/css; charset=utf-8" if static_path.suffix == ".css" else "application/octet-stream"
    return send_response(start_response, "200 OK", content_type, static_path.read_bytes())


def handle_api_alerts(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return _deny_json(start_response, "view_alerts")
    reference, alerts = load_alerts(resolve_alerts_path())
    visible_alerts = _visible_alerts(request, alerts)
    payload = {"referencia_funcional": reference, "summary": summarize_alerts(visible_alerts), "alerts": [alert.to_payload() for alert in visible_alerts]}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_pipeline(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return _deny_json(start_response, "view_pipeline")
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(_visible_pipeline_payload(request))))


def handle_alerts_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return _deny_html(request, start_response, "view_alerts")
    filters = _parse_catalog_filters(request)
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        reference, alerts = load_alerts(resolve_alerts_path())
        visible_alerts = _visible_alerts(request, alerts)
        available_filters = build_catalog()["filtros_disponibles"]
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, filters.normalized().active_filters(), None, status_message, request.access_context)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_pipeline_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return _deny_html(request, start_response, "view_pipeline")
    status_message = (request.query.get("mensaje") or [None])[0]
    content = render_pipeline(_visible_pipeline_payload(request), request.base_path, None, status_message, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_users_page(request: Request, start_response, id: str | None = None) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_html(request, start_response, "view_users")
    status_message = (request.query.get("mensaje") or [None])[0]
    selected_user_id = id
    try:
        if selected_user_id is None and request.path != "/usuarios":
            selected_user_id = request.path.rsplit("/", 1)[-1]
        payload = _visible_users_payload(request, selected_user_id=selected_user_id)
        content = render_users(payload, request.base_path, None, status_message, request.access_context)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except Exception as exc:
        content = render_users(_visible_users_payload(request), request.base_path, str(exc), status_message, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_retention_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_retention"):
        return _deny_html(request, start_response, "view_retention")
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        payload = build_retention_payload(pipeline_path=resolve_pipeline_path())
        content = render_retention_control(payload, request.base_path, None, status_message, request.access_context)
    except RetentionDatabaseError as exc:
        content = _retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_update_retention_policy(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_retention"):
        return _deny_html(request, start_response, "manage_retention")
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
            content = _retention_data_error_html(request.base_path, str(retention_exc))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except RetentionDatabaseError as exc:
        content = _retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/conservacion") + "?mensaje=Politica+de+conservacion+actualizada")


def handle_apply_retention_policy(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_retention"):
        return _deny_html(request, start_response, "manage_retention")
    try:
        result = apply_retention_policy(pipeline_path=resolve_pipeline_path())
    except RetentionDatabaseError as exc:
        content = _retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    message = f"Archivado aplicado: {result['archivadas']} licitaciones trasladadas"
    return send_redirect(start_response, build_url(request.base_path, "/conservacion") + f"?mensaje={message.replace(' ', '+')}")


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


def handle_create_user(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
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
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+creado+y+registrado")


def handle_update_user(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
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
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+actualizado")


def handle_change_user_state(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado") or [""])[0]
    try:
        change_user_state(id, state)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha actualizado el estado de {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Estado+de+usuario+actualizado")


def handle_delete_user(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    try:
        delete_user(id)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha eliminado {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+eliminado")



def handle_create_alert(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        create_alert(form_filters, path=resolve_alerts_path(), user_id=request.access_context.user_id)
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        visible_alerts = _visible_alerts(request, alerts)
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, form_filters.normalized().active_filters(), str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+creada+y+activa")


def handle_update_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        update_alert(
            id,
            form_filters,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        visible_alerts = _visible_alerts(request, alerts)
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, {}, f"No se ha actualizado {id}. {exc}", None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except PermissionError:
        return _deny_html(request, start_response, "manage_alerts")
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+actualizada")


def handle_deactivate_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    try:
        deactivate_alert(
            id,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except PermissionError:
        return _deny_html(request, start_response, "manage_alerts")
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+desactivada")


def handle_create_pipeline_entry(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return _deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    opportunity_id = (form_data.get("opportunity_id") or [""])[0].strip()
    try:
        _, created = add_opportunity_to_pipeline(opportunity_id, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(_visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _not_found(start_response)

    message = "Oportunidad guardada en el pipeline" if created else "La oportunidad ya estaba guardada en el pipeline"
    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + f"?mensaje={message.replace(' ', '+')}")


def handle_update_pipeline_entry(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return _deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado_seguimiento") or [""])[0]
    try:
        update_pipeline_entry_status(id, state, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(_visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _deny_html(request, start_response, "manage_pipeline")

    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + "?mensaje=Estado+de+pipeline+actualizado")


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
            filters=_parse_catalog_filters(request),
            page=_parse_catalog_page(request),
            page_size=_parse_catalog_page_size(request),
        )
        content = render_catalog(payload, request.base_path, request.access_context)
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
    content = render_opportunity_detail(detail, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_kpis_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_kpis"):
        return _deny_html(request, start_response, "view_kpis")
    try:
        catalog = build_catalog()
        _, alerts = load_alerts(resolve_alerts_path())
        source_coverage = load_source_coverage()
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))

    visible_alerts = _visible_alerts(request, alerts)
    alerts_summary = summarize_alerts(visible_alerts)
    pipeline_payload = _visible_pipeline_payload(request)
    coverage_summary = summary_by_status(source_coverage)
    coverage_visible = len(catalog["cobertura_aplicada"])
    coverage_mvp = coverage_summary["MVP"]
    active_alert_users = len({alert.usuario_id for alert in visible_alerts if alert.activa})
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
        return _deny_html(request, start_response, "view_permissions")
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


def handle_api_users(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_user_detail(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request, selected_user_id=id)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    user = payload.get("usuario_seleccionado")
    if user is None:
        return _not_found(start_response)
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(user)))


routes = [
    Route("GET", "/static/{filename}", handle_static),
    Route("GET", "/login", handle_login_page),
    Route("POST", "/login", handle_login_submit),
    Route("POST", "/logout", handle_logout),
    Route("GET", "/api/alertas", handle_api_alerts),
    Route("GET", "/api/pipeline", handle_api_pipeline),
    Route("GET", "/api/usuarios/{id}", handle_api_user_detail),
    Route("GET", "/api/usuarios", handle_api_users),
    Route("POST", "/alertas", handle_create_alert),
    Route("POST", "/alertas/{id}/editar", handle_update_alert),
    Route("POST", "/alertas/{id}/desactivar", handle_deactivate_alert),
    Route("POST", "/pipeline", handle_create_pipeline_entry),
    Route("POST", "/pipeline/{id}/estado", handle_update_pipeline_entry),
    Route("POST", "/conservacion/politica", handle_update_retention_policy),
    Route("POST", "/conservacion/aplicar", handle_apply_retention_policy),
    Route("POST", "/usuarios", handle_create_user),
    Route("POST", "/usuarios/{id}", handle_update_user),
    Route("POST", "/usuarios/{id}/estado", handle_change_user_state),
    Route("POST", "/usuarios/{id}/borrar", handle_delete_user),
    Route("GET", "/api/oportunidades/{id}", handle_api_opportunity_detail),
    Route("GET", "/api/oportunidades", handle_api_opportunities),
    Route("GET", "/api/fuentes", handle_api_sources),
    Route("GET", "/api/fuentes-prioritarias", handle_api_prioritized_sources),
    Route("GET", "/api/clasificacion-ti", handle_api_classification),
    Route("GET", "/clasificacion-ti", handle_classification_page),
    Route("GET", "/cobertura-fuentes", handle_coverage_page),
    Route("GET", "/priorizacion-fuentes-reales", handle_prioritization_page),
    Route("GET", "/kpis", handle_kpis_page),
    Route("GET", "/conservacion", handle_retention_page),
    Route("GET", "/permisos", handle_permissions_page),
    Route("GET", "/usuarios/{id}", handle_users_page),
    Route("GET", "/usuarios", handle_users_page),
    Route("GET", "/alertas", handle_alerts_page),
    Route("GET", "/pipeline", handle_pipeline_page),
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
    settings = get_auth_settings()
    try:
        synchronize_superadmin_account(settings)
    except AuthenticationError:
        LOGGER.warning("No se pudo sincronizar el superadmin al procesar la petición.")
    base_path = resolve_base_path()
    query = parse_qs(str(environ.get("QUERY_STRING", "")), keep_blank_values=False)
    session_state = load_session(environ, settings)
    secure_request = _secure_request(environ)
    request = Request(
        environ=environ,
        method=(environ.get("REQUEST_METHOD", "GET") or "GET").upper(),
        path=_resolve_request_path(environ, base_path),
        base_path=base_path,
        query=query,
        access_context=resolve_access_context(environ, query, session_user=session_state.session),
        session_state=session_state,
    )

    if _is_authenticated(request.session):
        if timeout_exceeded(str(request.session.get("last_activity") or ""), settings.session_timeout_minutes):
            clear_session(session_state)
            if settings.automatic_login_effective and not _is_public_path(request.path):
                request = _activate_superadmin_session(request)
            else:
                return _redirect(
                    lambda status, headers: start_response(
                        status,
                        headers + persist_session_headers(session_state, settings, secure_request=secure_request),
                    ),
                    build_url(base_path, "/login?reason=timeout"),
                )
        else:
            request.session["last_activity"] = now_iso()
            request.session_state.should_persist = True
            request = Request(
                environ=request.environ,
                method=request.method,
                path=request.path,
                base_path=request.base_path,
                query=request.query,
                access_context=resolve_access_context(environ, query, session_user=request.session),
                session_state=request.session_state,
            )
    elif not _is_public_path(request.path):
        if settings.automatic_login_effective:
            request = _activate_superadmin_session(request)
        else:
            ensure_csrf_token(request.session)
            request.session_state.should_persist = True
            return _redirect(
                lambda status, headers: start_response(
                    status,
                    headers + persist_session_headers(session_state, settings, secure_request=secure_request),
                ),
                build_url(base_path, "/login"),
            )

    def secured_start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response_headers = list(headers)
        response_headers.extend(
            [
                ("X-Content-Type-Options", "nosniff"),
                ("X-Frame-Options", "DENY"),
            ]
        )
        if _is_authenticated(request.session):
            response_headers.append(("Cache-Control", "no-store, no-cache"))
        response_headers.extend(persist_session_headers(session_state, settings, secure_request=secure_request))
        start_response(status, response_headers)

    for route in routes:
        if route.method != request.method:
            continue
        params = _match_pattern(request.path, route.pattern)
        if params is None:
            continue
        return route.handler(request, secured_start_response, **params)
    return _not_found(secured_start_response)
