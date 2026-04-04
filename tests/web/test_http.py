from __future__ import annotations

import unittest

from licican.access import AccessContext
from licican.auth.session import SessionState
from licican.web.http import (
    Request,
    client_ip,
    is_authenticated,
    is_public_path,
    parse_catalog_filters,
    parse_catalog_page,
    parse_catalog_page_size,
    resolve_request_path,
    secure_request,
)


class HttpHelpersTests(unittest.TestCase):
    def _request(self, query: dict[str, list[str]] | None = None, path: str = "/usuarios") -> Request:
        return Request(
            environ={},
            method="GET",
            path=path,
            base_path="/licican",
            query=query or {},
            access_context=AccessContext(role="manager", role_label="Manager", user_id="user-1", capabilities=frozenset()),
            session_state=SessionState(session={}),
        )

    def test_resolve_request_path_strips_script_name(self) -> None:
        environ = {"PATH_INFO": "/licican/usuarios", "SCRIPT_NAME": "/licican"}
        self.assertEqual("/usuarios", resolve_request_path(environ, "/licican"))

    def test_security_helpers_detect_auth_and_public_paths(self) -> None:
        self.assertTrue(is_public_path("/login"))
        self.assertTrue(is_public_path("/static/style.css"))
        self.assertFalse(is_public_path("/usuarios"))
        self.assertFalse(is_authenticated({}))
        self.assertTrue(is_authenticated({"username": "demo"}))

    def test_network_helpers_detect_secure_request_and_client_ip(self) -> None:
        self.assertTrue(secure_request({"wsgi.url_scheme": "https"}))
        self.assertTrue(secure_request({"HTTP_X_FORWARDED_PROTO": "https"}))
        self.assertEqual("203.0.113.10", client_ip({"HTTP_X_FORWARDED_FOR": "203.0.113.10, 10.0.0.1"}))
        self.assertEqual("unknown", client_ip({}))

    def test_parsing_helpers_normalize_query_values(self) -> None:
        request = self._request(
            {
                "palabra_clave": ["backup"],
                "presupuesto_min": ["1000"],
                "presupuesto_max": ["oops"],
                "procedimiento": ["Abierto"],
                "ubicacion": ["Canarias"],
                "page": ["3"],
                "page_size": ["25"],
                "busqueda": ["Ana"],
                "estado": ["activo"],
                "rol": ["manager"],
            }
        )

        catalog_filters = parse_catalog_filters(request)
        self.assertEqual("backup", catalog_filters.palabra_clave)
        self.assertEqual(1000, catalog_filters.presupuesto_min)
        self.assertIsNone(catalog_filters.presupuesto_max)
        self.assertEqual("Abierto", catalog_filters.procedimiento)
        self.assertEqual("Canarias", catalog_filters.ubicacion)
        self.assertEqual(3, parse_catalog_page(request))
        self.assertEqual(25, parse_catalog_page_size(request))
