from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
import logging
from html import escape
from pathlib import Path

from licican.access import AccessContext, resolve_access_context
from licican.alerts import filter_alerts_by_user
from licican.auth.config import get_auth_settings
from licican.auth.csrf import ensure_csrf_token
from licican.auth.service import AuthenticationError, synchronize_superadmin_account
from licican.auth.session import SessionState, now_iso
from licican.config import normalize_base_path, resolve_pipeline_path
from licican.pipeline import build_pipeline_payload
from licican.shared.filters import CatalogFilters
from licican.web.responses import build_url, html_body, json_body, send_response
from licican.web.templates.base import page_template

STATIC_DIR = Path(__file__).resolve().parent / "static"
PUBLIC_PATH_PREFIXES = ("/static/",)
PUBLIC_PATHS = frozenset({"/login"})
Route = namedtuple("Route", ["method", "pattern", "handler"])
LOGGER = logging.getLogger(__name__)


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


def is_public_path(path: str) -> bool:
    return path in PUBLIC_PATHS or any(path.startswith(prefix) for prefix in PUBLIC_PATH_PREFIXES)


def is_authenticated(session: dict[str, object]) -> bool:
    return bool(session.get("username"))


def secure_request(environ: dict[str, object]) -> bool:
    scheme = str(environ.get("wsgi.url_scheme", "http") or "http").lower()
    forwarded_proto = str(environ.get("HTTP_X_FORWARDED_PROTO", "") or "").lower()
    return scheme == "https" or forwarded_proto == "https"


def client_ip(environ: dict[str, object]) -> str:
    forwarded_for = str(environ.get("HTTP_X_FORWARDED_FOR", "") or "").strip()
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return str(environ.get("REMOTE_ADDR", "") or "unknown")


def redirect(start_response, location: str) -> list[bytes]:
    return send_response(
        start_response,
        "302 Found",
        "text/plain; charset=utf-8",
        b"",
        extra_headers=[("Location", location)],
    )


def forbidden(start_response, message: str = "CSRF invalido") -> list[bytes]:
    return send_response(start_response, "403 Forbidden", "text/plain; charset=utf-8", message.encode("utf-8"))


def activate_superadmin_session(request: Request) -> Request:
    settings = get_auth_settings()
    try:
        synchronize_superadmin_account(settings)
    except AuthenticationError:
        LOGGER.debug("No se pudo sincronizar el superadmin al activar la sesion automatica.")
    request.session.clear()
    request.session.update(
        {
            "username": settings.login_superadmin_name,
            "rol": "superadmin",
            "nombre_completo": "",
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


def parse_filters_from_multidict(values: dict[str, list[str]]) -> CatalogFilters:
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


def parse_catalog_filters(request: Request) -> CatalogFilters:
    return parse_filters_from_multidict(request.query)


def parse_catalog_page(request: Request) -> int:
    candidates = request.query.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def parse_catalog_page_size(request: Request) -> int:
    candidates = request.query.get("page_size")
    if not candidates:
        return 10
    try:
        page_size = int(candidates[0])
    except ValueError:
        return 10
    return page_size if page_size in {5, 10, 25, 50} else 10


def resolve_request_path(environ: dict[str, object], base_path: str) -> str:
    raw_path = str(environ.get("PATH_INFO", "/") or "/")
    script_name = normalize_base_path(str(environ.get("SCRIPT_NAME") or "")) or base_path
    if script_name and raw_path.startswith(script_name):
        raw_path = raw_path[len(script_name):] or "/"
    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"
    return raw_path or "/"


def not_found(start_response) -> list[bytes]:
    return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", b"No encontrado")


def access_denied_html(request: Request, capability: str) -> str:
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


def deny_html(request: Request, start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "text/html; charset=utf-8",
        b"".join(html_body(access_denied_html(request, capability))),
    )


def deny_json(start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "application/json; charset=utf-8",
        b"".join(json_body({"error": f"Acceso restringido por permisos para {capability}."})),
    )


def visible_alerts(request: Request, alerts):
    return alerts if request.access_context.is_admin else filter_alerts_by_user(alerts, request.access_context.user_id)


def visible_pipeline_payload(request: Request) -> dict[str, object]:
    return build_pipeline_payload(
        path=resolve_pipeline_path(),
        usuario_id=None if request.access_context.is_admin else request.access_context.user_id,
    )


def catalog_data_error_html(base_path: str, message: str) -> str:
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


def users_data_error_html(base_path: str, message: str) -> str:
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


def retention_data_error_html(base_path: str, message: str) -> str:
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
