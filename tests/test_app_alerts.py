from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.shared.app_http import invoke_app, session_cookie as _session_cookie


class ApplicationAlertsTests(unittest.TestCase):
    def test_alerts_page_renders_empty_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            with patch.dict(os.environ, {"LICICAN_ALERTS_PATH": str(alerts_path)}, clear=False):
                status, headers, body = invoke_app("/alertas")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Gestión de alertas tempranas", html)
        self.assertIn("Todavía no hay alertas registradas", html)
        self.assertIn('class="nav-link active" href="/licican/alertas"', html)

    def test_alert_creation_rejects_empty_form(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            with patch.dict(os.environ, {"LICICAN_ALERTS_PATH": str(alerts_path)}, clear=False):
                status, headers, body = invoke_app("/alertas", method="POST")

        html = body.decode("utf-8")
        self.assertEqual("400 Bad Request", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("La alerta necesita al menos un criterio funcional", html)

    def test_reader_role_hides_operational_navigation_and_blocks_alert_access(self) -> None:
        reader_cookie = _session_cookie(role="invitado", username="lector-1", nombre_completo="Lector Demo")
        with patch.dict(os.environ, {"LOGIN_AUTOMATICO": "false"}, clear=False):
            status, _, body = invoke_app("/", cookies=reader_cookie)
            alerts_status, alerts_headers, alerts_body = invoke_app("/alertas", cookies=reader_cookie)

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertNotIn('href="/licican/alertas"', html)
        self.assertNotIn('href="/licican/pipeline"', html)
        self.assertEqual("403 Forbidden", alerts_status)
        self.assertEqual("text/html; charset=utf-8", alerts_headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", alerts_body.decode("utf-8"))

    def test_alert_lifecycle_is_visible_from_html_and_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            with patch.dict(os.environ, {"LICICAN_ALERTS_PATH": str(alerts_path)}, clear=False):
                created_status, created_headers, _ = invoke_app(
                    "/alertas",
                    method="POST",
                    body="palabra_clave=licencias",
                )
                self.assertEqual("303 See Other", created_status)
                self.assertEqual("/licican/alertas?mensaje=Alerta+creada+y+activa", created_headers["Location"])
                created_page_status, _, created_page_body = invoke_app("/alertas")
                self.assertEqual("200 OK", created_page_status)
                self.assertIn("Activa", created_page_body.decode("utf-8"))
                self.assertIn("Palabra clave: licencias", created_page_body.decode("utf-8"))

                invoke_app(
                    "/alertas/alerta-001/editar",
                    method="POST",
                    body="procedimiento=Abierto",
                )
                invoke_app(
                    "/alertas/alerta-001/desactivar",
                    method="POST",
                )
                page_status, page_headers, page_body = invoke_app("/alertas")
                api_status, api_headers, api_body = invoke_app("/api/alertas")

        html = page_body.decode("utf-8")
        api_payload = json.loads(api_body)

        self.assertEqual("200 OK", page_status)
        self.assertEqual("text/html; charset=utf-8", page_headers["Content-Type"])
        self.assertIn("alerta-001", html)
        self.assertIn("Inactiva", html)
        self.assertIn("Procedimiento: Abierto", html)

        self.assertEqual("200 OK", api_status)
        self.assertEqual("application/json; charset=utf-8", api_headers["Content-Type"])
        self.assertEqual(1, api_payload["summary"]["total_alertas"])
        self.assertEqual(0, api_payload["summary"]["alertas_activas"])
        self.assertEqual({"procedimiento": "Abierto"}, api_payload["alerts"][0]["filtros"])

    def test_collaborator_only_sees_own_alerts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            admin_cookie = _session_cookie(role="administrador", username="admin-1", nombre_completo="Admin Demo")
            manager_cookie = _session_cookie(role="manager", username="manager-1", nombre_completo="Manager Demo")
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LOGIN_AUTOMATICO": "false"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="palabra_clave=licencias", cookies=admin_cookie)
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LOGIN_AUTOMATICO": "false"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="procedimiento=Abierto", cookies=manager_cookie)
                page_status, _, page_body = invoke_app("/alertas", cookies=manager_cookie)
                api_status, _, api_body = invoke_app("/api/alertas", cookies=manager_cookie)

        self.assertEqual("200 OK", page_status)
        html = page_body.decode("utf-8")
        self.assertIn("alerta-002", html)
        self.assertNotIn("alerta-001", html)
        payload = json.loads(api_body)
        self.assertEqual("200 OK", api_status)
        self.assertEqual(1, payload["summary"]["total_alertas"])
        self.assertEqual("manager-1", payload["alerts"][0]["usuario_id"])

    def test_collaborator_cannot_edit_alerts_from_other_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            admin_cookie = _session_cookie(role="administrador", username="admin-1", nombre_completo="Admin Demo")
            collaborator_cookie = _session_cookie(role="colaborador", username="colab-1", nombre_completo="Colaborador Demo")
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LOGIN_AUTOMATICO": "false"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="palabra_clave=licencias", cookies=admin_cookie)
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LOGIN_AUTOMATICO": "false"},
                clear=False,
            ):
                status, headers, body = invoke_app(
                    "/alertas/alerta-001/editar",
                    method="POST",
                    body="procedimiento=Abierto",
                    cookies=collaborator_cookie,
                )

        self.assertEqual("403 Forbidden", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", body.decode("utf-8"))
