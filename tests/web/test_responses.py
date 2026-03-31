from __future__ import annotations

import unittest
from io import BytesIO

from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response


class ResponsesTests(unittest.TestCase):
    def test_build_url_respects_base_path(self) -> None:
        self.assertEqual("/licican/alertas", build_url("/licican", "/alertas"))
        self.assertEqual("/alertas", build_url("", "/alertas"))
        self.assertEqual("/licican", build_url("/licican", "/"))

    def test_read_form_data_parses_urlencoded_body(self) -> None:
        environ = {
            "CONTENT_LENGTH": "42",
            "wsgi.input": BytesIO(b"palabra_clave=backup&procedimiento=Abierto"),
        }
        self.assertEqual(
            {"palabra_clave": ["backup"], "procedimiento": ["Abierto"]},
            read_form_data(environ),
        )

    def test_body_helpers_encode_utf8(self) -> None:
        self.assertEqual(b"<h1>Licican</h1>", b"".join(html_body("<h1>Licican</h1>")))
        self.assertIn("á".encode("utf-8"), b"".join(json_body({"titulo": "Catálogo"})))

    def test_send_response_and_redirect_emit_wsgi_headers(self) -> None:
        captured: dict[str, object] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(send_response(start_response, "200 OK", "text/plain; charset=utf-8", b"ok"))
        self.assertEqual(b"ok", body)
        self.assertEqual("200 OK", captured["status"])
        self.assertEqual("2", captured["headers"]["Content-Length"])

        captured.clear()
        body = b"".join(send_redirect(start_response, "/licican/alertas"))
        self.assertEqual(b"", body)
        self.assertEqual("303 See Other", captured["status"])
        self.assertEqual("/licican/alertas", captured["headers"]["Location"])
