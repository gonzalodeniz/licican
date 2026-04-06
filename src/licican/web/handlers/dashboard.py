from __future__ import annotations

from licican.web.http import Request
from licican.web.responses import html_body, send_response
from licican.web.templates.dashboard import render_dashboard


def handle_dashboard_page(request: Request, start_response) -> list[bytes]:
    content = render_dashboard(request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))
