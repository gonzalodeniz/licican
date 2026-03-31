from __future__ import annotations

import json
from io import BytesIO
from urllib.parse import parse_qs


def send_response(
    start_response,
    status: str,
    content_type: str,
    body: bytes,
    extra_headers: list[tuple[str, str]] | None = None,
) -> list[bytes]:
    """Envía una respuesta WSGI con cabeceras estándar."""
    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
    ]
    headers.extend(extra_headers or [])
    start_response(status, headers)
    return [body]


def send_redirect(start_response, location: str) -> list[bytes]:
    """Envía una redirección HTTP 303."""
    return send_response(start_response, "303 See Other", "text/plain; charset=utf-8", b"", [("Location", location)])


def json_body(payload: dict[str, object]) -> list[bytes]:
    """Serializa un payload JSON en UTF-8."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return [body]


def html_body(content: str) -> list[bytes]:
    """Codifica una respuesta HTML en UTF-8."""
    return [content.encode("utf-8")]


def read_form_data(environ: dict[str, object]) -> dict[str, list[str]]:
    """Lee y parsea un formulario `application/x-www-form-urlencoded`."""
    content_length = str(environ.get("CONTENT_LENGTH", "")).strip()
    try:
        body_length = int(content_length or "0")
    except ValueError:
        body_length = 0

    stream = environ.get("wsgi.input", BytesIO())
    if not hasattr(stream, "read"):
        stream = BytesIO()
    body = stream.read(body_length).decode("utf-8") if body_length > 0 else ""
    return parse_qs(body, keep_blank_values=True)


def build_url(base_path: str, path: str) -> str:
    """Construye una URL absoluta interna respetando `BASE_PATH`."""
    normalized_path = path if path.startswith("/") else f"/{path}"
    if not base_path:
        return normalized_path
    if normalized_path == "/":
        return base_path
    return f"{base_path}{normalized_path}"
