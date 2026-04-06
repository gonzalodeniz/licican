from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import parse_qs

from licican.access import resolve_access_context
from licican.access import has_capability
from licican.auth.config import get_auth_settings
from licican.auth.csrf import ensure_csrf_token
from licican.auth.service import AuthenticationError, synchronize_superadmin_account
from licican.auth.session import clear_session, load_session, now_iso, persist_session_headers, timeout_exceeded
from licican.config import resolve_base_path, resolve_pipeline_path
from licican.opportunity_catalog import CatalogDataSourceError
from licican.opportunity_catalog import build_catalog
from licican.retention import RetentionDatabaseError, build_retention_payload
from licican.web.handlers.alerts import (
    handle_alerts_page,
    handle_api_alerts,
    handle_create_alert,
    handle_deactivate_alert,
    handle_update_alert,
)
from licican.web.handlers.auth import handle_login_page, handle_login_submit, handle_logout
from licican.web.handlers.catalog import (
    handle_api_classification,
    handle_api_opportunities,
    handle_api_opportunity_detail,
    handle_api_prioritized_sources,
    handle_api_sources,
    handle_catalog_page,
    handle_classification_page,
    handle_coverage_page,
    handle_kpis_page,
    handle_opportunity_detail,
    handle_permissions_page,
    handle_prioritization_page,
)
from licican.web.handlers.pipeline import (
    handle_api_pipeline,
    handle_create_pipeline_entry,
    handle_pipeline_page,
    handle_update_pipeline_entry,
)
from licican.web.handlers.retention import (
    handle_apply_retention_policy,
    handle_retention_page,
    handle_update_retention_policy,
)
from licican.web.handlers.dashboard import handle_dashboard_page
from licican.web.handlers.users import (
    handle_api_user_detail,
    handle_api_users,
    handle_change_user_password,
    handle_change_user_state,
    handle_create_user,
    handle_delete_user,
    handle_update_user,
    handle_users_page,
)
from licican.web.http import (
    Request,
    Route,
    activate_superadmin_session as _activate_superadmin_session,
    catalog_data_error_html as _catalog_data_error_html,
    deny_html as _deny_html,
    is_authenticated as _is_authenticated,
    is_public_path as _is_public_path,
    not_found as _not_found,
    parse_catalog_filters as _parse_catalog_filters,
    parse_catalog_page as _parse_catalog_page,
    parse_catalog_page_size as _parse_catalog_page_size,
    redirect as _redirect,
    resolve_request_path as _resolve_request_path,
    secure_request as _secure_request,
    retention_data_error_html as _retention_data_error_html,
)
from licican.web.responses import build_url, html_body, send_response
from licican.web.templates.catalog import render_catalog
from licican.web.templates.retention import render_retention_control

STATIC_DIR = Path(__file__).resolve().parent / "static"
LOGGER = logging.getLogger(__name__)
CSS_IMPORT_RE = re.compile(r'@import\s+url\(["\']?(?P<path>[^"\')]+)["\']?\)\s*;?')


def _read_static_css(static_path: Path, visited: set[Path] | None = None) -> bytes:
    visited = visited or set()
    resolved_path = static_path.resolve()
    if resolved_path in visited:
        return b""
    visited.add(resolved_path)

    chunks: list[bytes] = []
    for line in static_path.read_text(encoding="utf-8").splitlines():
        match = CSS_IMPORT_RE.fullmatch(line.strip())
        if match is None:
            chunks.append((line + "\n").encode("utf-8"))
            continue
        imported_path = (static_path.parent / match.group("path")).resolve()
        if not str(imported_path).startswith(str(STATIC_DIR.resolve())) or not imported_path.is_file():
            continue
        chunks.append(_read_static_css(imported_path, visited))
    return b"".join(chunks)


def handle_static(request: Request, start_response, filename: str) -> list[bytes]:
    relative_path = filename
    static_path = (STATIC_DIR / relative_path).resolve()
    if not str(static_path).startswith(str(STATIC_DIR.resolve())) or not static_path.is_file():
        return _not_found(start_response)
    content_type = "text/css; charset=utf-8" if static_path.suffix == ".css" else "application/octet-stream"
    if static_path.suffix == ".css":
        return send_response(start_response, "200 OK", content_type, _read_static_css(static_path))
    return send_response(start_response, "200 OK", content_type, static_path.read_bytes())


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


def handle_retention_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_retention"):
        return _deny_html(request, start_response, "view_retention")
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        payload = build_retention_payload(pipeline_path=resolve_pipeline_path())
    except RetentionDatabaseError as exc:
        content = _retention_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    content = render_retention_control(payload, request.base_path, None, status_message, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


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
    Route("POST", "/usuarios/{id}/contrasena", handle_change_user_password),
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
    Route("GET", "/dashboard", handle_dashboard_page),
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
        LOGGER.debug("No se pudo sincronizar el superadmin al procesar la petición.")
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
