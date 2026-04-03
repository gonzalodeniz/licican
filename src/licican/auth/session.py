from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from http.cookies import SimpleCookie
from typing import Any

from itsdangerous import BadSignature, URLSafeSerializer

from licican.auth.config import AuthSettings


SESSION_SALT = "licican.session"


@dataclass
class SessionState:
    session: dict[str, object]
    should_persist: bool = False
    clear_cookie: bool = False


def _serializer(settings: AuthSettings) -> URLSafeSerializer:
    return URLSafeSerializer(settings.session_secret_key, salt=SESSION_SALT)


def load_session(environ: dict[str, object], settings: AuthSettings) -> SessionState:
    cookies = SimpleCookie()
    raw_cookies = str(environ.get("HTTP_COOKIE", "") or "")
    if raw_cookies:
        cookies.load(raw_cookies)
    morsel = cookies.get(settings.session_cookie_name)
    if morsel is None:
        return SessionState(session={})
    try:
        payload = _serializer(settings).loads(morsel.value)
    except BadSignature:
        return SessionState(session={}, clear_cookie=True)
    if not isinstance(payload, dict):
        return SessionState(session={}, clear_cookie=True)
    return SessionState(session={str(key): value for key, value in payload.items()})


def persist_session_headers(
    state: SessionState,
    settings: AuthSettings,
    *,
    secure_request: bool,
) -> list[tuple[str, str]]:
    headers: list[tuple[str, str]] = []
    if state.should_persist and state.session:
        signed_value = _serializer(settings).dumps(state.session)
        headers.append(("Set-Cookie", _build_cookie(settings, signed_value, secure_request=secure_request)))
    elif state.clear_cookie or state.should_persist:
        headers.append(("Set-Cookie", _build_cookie(settings, "", secure_request=secure_request, expires="Thu, 01 Jan 1970 00:00:00 GMT")))
    return headers


def clear_session(state: SessionState) -> None:
    state.session.clear()
    state.should_persist = True
    state.clear_cookie = True


def timeout_exceeded(last_activity_iso: str | None, timeout_minutes: int, now: datetime | None = None) -> bool:
    if not last_activity_iso:
        return False
    current = now or datetime.now(UTC)
    try:
        last_activity = datetime.fromisoformat(last_activity_iso.replace("Z", "+00:00"))
    except ValueError:
        return True
    if last_activity.tzinfo is None:
        last_activity = last_activity.replace(tzinfo=UTC)
    return current - last_activity.astimezone(UTC) > timedelta(minutes=timeout_minutes)


def now_iso(now: datetime | None = None) -> str:
    current = now or datetime.now(UTC)
    return current.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_cookie(settings: AuthSettings, value: str, *, secure_request: bool, expires: str | None = None) -> str:
    parts = [
        f"{settings.session_cookie_name}={value}",
        "HttpOnly",
        "Path=/",
        "SameSite=Lax",
    ]
    if settings.session_cookie_secure or secure_request:
        parts.append("Secure")
    if expires:
        parts.append(f"Expires={expires}")
        parts.append("Max-Age=0")
    return "; ".join(parts)
