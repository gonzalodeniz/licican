from __future__ import annotations

import os
from datetime import UTC, datetime
from io import BytesIO

from itsdangerous import URLSafeSerializer
from unittest.mock import patch

from licican.app import application
from licican.auth.config import SUPERADMIN_USERNAME


def session_cookie(*, role: str, username: str, nombre_completo: str | None = None) -> str:
    signer = URLSafeSerializer("test-session-secret", salt="licican.session")
    session_payload = {
        "username": username,
        "rol": role,
        "nombre_completo": nombre_completo or username,
        "is_superadmin": (role == "superadmin" and username == SUPERADMIN_USERNAME) or (role == "administrador" and username == "admin-1"),
        "last_activity": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "csrf_token": "csrf-test-token",
        "auto_login_active": False,
    }
    return f"licican_session={signer.dumps(session_payload)}"


def invoke_app(
    path: str,
    query_string: str = "",
    script_name: str = "",
    method: str = "GET",
    body: str = "",
    content_type: str = "application/x-www-form-urlencoded",
    authenticated: bool = True,
    cookies: str = "",
) -> tuple[str, dict[str, str], bytes]:
    captured: dict[str, object] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        captured["status"] = status
        captured["headers"] = dict(headers)

    payload = body.encode("utf-8")
    environ = {
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "REQUEST_METHOD": method,
        "CONTENT_LENGTH": str(len(payload)),
        "CONTENT_TYPE": content_type,
        "wsgi.input": BytesIO(payload),
    }
    if script_name:
        environ["SCRIPT_NAME"] = script_name
    env_overrides = {"BASE_PATH": "/licican"}
    if "LOGIN_AUTOMATICO" not in os.environ:
        env_overrides["LOGIN_AUTOMATICO"] = "true"
    if "LOGIN_SUPERADMIN_ENABLED" not in os.environ:
        env_overrides["LOGIN_SUPERADMIN_ENABLED"] = "true"
    if "LOGIN_SUPERADMIN_PASS" not in os.environ:
        env_overrides["LOGIN_SUPERADMIN_PASS"] = "admin12345"
    env_overrides["SESSION_SECRET_KEY"] = "test-session-secret"
    if "LICICAN_CATALOG_BACKEND" not in os.environ:
        env_overrides["LICICAN_CATALOG_BACKEND"] = "file"
    if "LICICAN_ROLE" not in os.environ:
        env_overrides["LICICAN_ROLE"] = "administrador"
    env_overrides["DB_PASSWORD"] = "test-password"

    if authenticated and not cookies:
        role = os.environ.get("LICICAN_ROLE", "administrador")
        username = os.environ.get("LICICAN_USER_ID", "admin-1")
        session_payload = {
            "username": username,
            "rol": role,
            "nombre_completo": username,
            "is_superadmin": (role == "superadmin" and username == SUPERADMIN_USERNAME) or (role == "administrador" and username == "admin-1"),
            "last_activity": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "csrf_token": "csrf-test-token",
            "auto_login_active": False,
        }
        signer = URLSafeSerializer(
            os.environ.get("SESSION_SECRET_KEY", env_overrides["SESSION_SECRET_KEY"]),
            salt="licican.session",
        )
        cookies = f"licican_session={signer.dumps(session_payload)}"

    if cookies:
        environ["HTTP_COOKIE"] = cookies
    with patch.dict(os.environ, env_overrides, clear=False):
        body = b"".join(application(environ, start_response))
    return captured["status"], captured["headers"], body
