from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.shared.app_http import invoke_app, session_cookie as _session_cookie


class ApplicationWorkflowTests(unittest.TestCase):
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

    def test_pipeline_page_renders_empty_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            with patch.dict(os.environ, {"LICICAN_PIPELINE_PATH": str(pipeline_path)}, clear=False):
                status, headers, body = invoke_app("/pipeline")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="pipeline-summary-panel"', html)
        self.assertIn("Pipeline de seguimiento de oportunidades", html)
        self.assertIn("Todavía no hay oportunidades guardadas en el pipeline.", html)
        self.assertIn('class="nav-link active" href="/licican/pipeline"', html)

    def test_detail_page_keeps_catalog_navigation_active(self) -> None:
        status, _, body = invoke_app("/oportunidades/pcsp-cabildo-licencias-2026")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertIn('class="nav-link active" href="/licican/"', html)
        self.assertIn("Menu principal", html)

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
        self.assertNotIn('href="/licican/kpis"', html)
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

    def test_pipeline_lifecycle_is_visible_from_html_and_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            with patch.dict(os.environ, {"LICICAN_PIPELINE_PATH": str(pipeline_path)}, clear=False):
                created_status, created_headers, _ = invoke_app(
                    "/pipeline",
                    method="POST",
                    body="opportunity_id=pcsp-cabildo-licencias-2026",
                )
                self.assertEqual("303 See Other", created_status)
                self.assertEqual("/licican/pipeline?mensaje=Oportunidad+guardada+en+el+pipeline", created_headers["Location"])

                duplicate_status, duplicate_headers, _ = invoke_app(
                    "/pipeline",
                    method="POST",
                    body="opportunity_id=pcsp-cabildo-licencias-2026",
                )
                self.assertEqual("303 See Other", duplicate_status)
                self.assertEqual(
                    "/licican/pipeline?mensaje=La+oportunidad+ya+estaba+guardada+en+el+pipeline",
                    duplicate_headers["Location"],
                )

                update_status, update_headers, _ = invoke_app(
                    "/pipeline/pcsp-cabildo-licencias-2026/estado",
                    method="POST",
                    body="estado_seguimiento=Evaluando",
                )
                self.assertEqual("303 See Other", update_status)
                self.assertEqual("/licican/pipeline?mensaje=Estado+de+pipeline+actualizado", update_headers["Location"])

                page_status, page_headers, page_body = invoke_app("/pipeline")
                api_status, api_headers, api_body = invoke_app("/api/pipeline")

        html = page_body.decode("utf-8")
        api_payload = json.loads(api_body)

        self.assertEqual("200 OK", page_status)
        self.assertEqual("text/html; charset=utf-8", page_headers["Content-Type"])
        self.assertIn('id="pipeline-summary-panel"', html)
        self.assertIn("pcsp-cabildo-licencias-2026", html)
        self.assertIn("Evaluando", html)
        self.assertIn("Fuente oficial", html)

        self.assertEqual("200 OK", api_status)
        self.assertEqual("application/json; charset=utf-8", api_headers["Content-Type"])
        self.assertEqual(1, api_payload["summary"]["total_oportunidades"])
        self.assertEqual(0, api_payload["summary"]["con_advertencia_oficial"])
        self.assertEqual("Evaluando", api_payload["pipeline"][0]["estado_seguimiento"])

    def test_admin_can_access_permissions_page_and_collaborator_kpis(self) -> None:
        with patch.dict(os.environ, {"LICICAN_ROLE": "administrador"}, clear=False):
            admin_status, _, admin_body = invoke_app("/permisos")
        with patch.dict(os.environ, {"LICICAN_ROLE": "manager", "LICICAN_USER_ID": "manager-1"}, clear=False):
            kpi_status, _, kpi_body = invoke_app("/kpis")

        self.assertEqual("200 OK", admin_status)
        admin_html = admin_body.decode("utf-8")
        self.assertIn('id="permissions-summary-panel"', admin_html)
        self.assertIn('id="permissions-matrix-panel"', admin_html)
        self.assertIn('class="table-wrap permissions-table-wrap"', admin_html)
        self.assertIn("Matriz funcional de roles y permisos", admin_html)
        self.assertEqual("200 OK", kpi_status)
        kpi_html = kpi_body.decode("utf-8")
        self.assertIn("KPIs iniciales de cobertura, adopción y uso", kpi_html)
        self.assertIn("Cobertura de fuentes priorizadas", kpi_html)
        self.assertIn("Umbral inicial", kpi_html)
        self.assertIn("Decisión asociada", kpi_html)

    def test_admin_can_access_retention_page(self) -> None:
        payload = {
            "politica": {"antiguedad_dias": 180, "modo": "desde_creacion", "modo_label": "Dias desde la creacion", "actualizada_en": "2026-04-03T09:00:00Z"},
            "resumen": {"conservar": 2, "archivar": 1, "mantener_activas": 1, "archivadas_existentes": 0},
            "modos_disponibles": [{"valor": "desde_creacion", "etiqueta": "Dias desde la creacion"}],
            "grupos": {"conservar": [], "archivar": [], "mantener_activas": []},
        }

        with patch("licican.web.router.build_retention_payload", return_value=payload):
            status, headers, body = invoke_app("/conservacion")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Panel de control de conservacion y archivado", html)
        self.assertIn('class="nav-link active" href="/licican/conservacion"', html)

    def test_retention_page_denied_to_reader_role(self) -> None:
        reader_cookie = _session_cookie(role="lector", username="lector-1", nombre_completo="Lector Demo")
        with patch.dict(os.environ, {"LOGIN_AUTOMATICO": "false"}, clear=False):
            status, headers, body = invoke_app("/conservacion", cookies=reader_cookie)

        self.assertEqual("403 Forbidden", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", body.decode("utf-8"))
