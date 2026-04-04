from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from tests.shared.app_http import invoke_app, session_cookie as _session_cookie


class ApplicationGovernanceTests(unittest.TestCase):
    def test_detail_page_keeps_catalog_navigation_active(self) -> None:
        status, _, body = invoke_app("/oportunidades/pcsp-cabildo-licencias-2026")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertIn('class="nav-link active" href="/licican/"', html)
        self.assertIn("Menu principal", html)

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
