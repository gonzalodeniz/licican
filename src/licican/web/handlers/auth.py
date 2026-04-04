from __future__ import annotations

from licican.auth.config import get_auth_settings
from licican.auth.csrf import ensure_csrf_token, validate_csrf_token
from licican.auth.rate_limiter import rate_limiter
from licican.auth.service import AuthenticationError, authenticate_user
from licican.auth.session import clear_session, now_iso
from licican.web.http import Request, client_ip, forbidden, is_authenticated, redirect
from licican.web.responses import build_url, html_body, read_form_data, send_response
from licican.web.templates.login import render_login


def handle_login_page(request: Request, start_response) -> list[bytes]:
    if is_authenticated(request.session):
        return redirect(start_response, build_url(request.base_path, "/"))
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
        return forbidden(start_response)

    current_client_ip = client_ip(request.environ)
    if rate_limiter.is_limited(current_client_ip):
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
            rate_limiter.register_failure(current_client_ip)
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

    rate_limiter.reset(current_client_ip)
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
    return redirect(start_response, build_url(request.base_path, "/"))


def handle_logout(request: Request, start_response) -> list[bytes]:
    form_data = read_form_data(request.environ)
    if not validate_csrf_token(request.session, (form_data.get("csrf_token") or [None])[0]):
        return forbidden(start_response)
    clear_session(request.session_state)
    return redirect(start_response, build_url(request.base_path, "/login?reason=logout"))
