from __future__ import annotations

import secrets


def ensure_csrf_token(session: dict[str, object]) -> str:
    token = str(session.get("csrf_token") or "").strip()
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def validate_csrf_token(session: dict[str, object], provided_token: str | None) -> bool:
    expected_token = str(session.get("csrf_token") or "")
    candidate = (provided_token or "").strip()
    return bool(expected_token) and secrets.compare_digest(expected_token, candidate)
