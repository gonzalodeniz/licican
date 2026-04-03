from __future__ import annotations

import os
import io
import json
import unittest
from contextlib import redirect_stdout
from io import BytesIO
from pathlib import Path
import tempfile
from unittest.mock import patch
from urllib.parse import urlencode

import psycopg2

from licican.app import application, main
from tests.shared.users_db import SeededUsersState, fake_users_connect


def invoke_app(
    path: str,
    query_string: str = "",
    script_name: str = "",
    method: str = "GET",
    body: str = "",
    content_type: str = "application/x-www-form-urlencoded",
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
    env_overrides = {}
    env_overrides["BASE_PATH"] = "/licican"
    if "LICICAN_CATALOG_BACKEND" not in os.environ:
        env_overrides["LICICAN_CATALOG_BACKEND"] = "file"
    if "LICICAN_ROLE" not in os.environ:
        env_overrides["LICICAN_ROLE"] = "administrador"
    if "DB_PASSWORD" not in os.environ:
        env_overrides["DB_PASSWORD"] = "test-password"
    with patch.dict(os.environ, env_overrides, clear=False):
        body = b"".join(application(environ, start_response))
    return captured["status"], captured["headers"], body


class ApplicationTests(unittest.TestCase):
    def _patch_users_db(self, state: SeededUsersState | None = None):
        current_state = state or SeededUsersState.seed()
        return patch("licican.users.psycopg2.connect", side_effect=lambda *args, **kwargs: fake_users_connect(current_state))

    def test_api_returns_controlled_error_when_postgresql_is_unavailable(self) -> None:
        with patch.dict(os.environ, {"LICICAN_CATALOG_BACKEND": "postgres"}, clear=False):
            with patch(
                "licican.postgres_catalog.psycopg2.connect",
                side_effect=psycopg2.OperationalError("db down"),
            ):
                status, headers, body = invoke_app("/api/oportunidades")

        payload = json.loads(body)
        self.assertEqual("503 Service Unavailable", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertIn("No se pudo cargar el catalogo desde PostgreSQL", payload["error"])

    def test_root_renders_catalog_page(self) -> None:
        status, headers, body = invoke_app("/")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Catálogo inicial de oportunidades TI de Canarias", html)
        self.assertIn('id="catalog-filters-panel"', html)
        self.assertIn('id="catalog-results-panel"', html)
        self.assertIn("Servicio cloud para copias de seguridad y continuidad de sistemas corporativos", html)
        self.assertIn("Ver oferta concreta", html)
        self.assertIn("Publicación oficial", html)
        self.assertIn("Fuente oficial", html)
        self.assertIn('/licican/oportunidades/pcsp-cabildo-licencias-2026', html)
        self.assertIn('action="/licican/"', html)
        self.assertIn("Licitaciones TI Canarias", html)
        self.assertIn("Detalle Lotes", html)
        self.assertIn("Adjudicaciones", html)
        self.assertIn('/licican/datos-consolidados', html)
        self.assertIn('<link rel="stylesheet" href="/licican/static/style.css"', html)
        self.assertNotIn("Pagina 1 de 1", html)
        self.assertNotIn("Mostrando 1-3 de 3", html)
        self.assertNotIn("Pagina siguiente", html)
        self.assertNotIn("Ir a la pagina", html)
        self.assertIn("Menu principal", html)
        self.assertIn('class="nav-link active" href="/licican/"', html)
        self.assertIn("Datos consolidados", html)
        self.assertIn("Alertas", html)
        self.assertIn('href="/licican/kpis"', html)
        self.assertIn('href="/licican/pipeline"', html)
        self.assertIn('href="/licican/permisos"', html)

    def test_root_pagination_keeps_single_page_when_results_fit(self) -> None:
        status, headers, body = invoke_app("/", "page=2")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("La pagina solicitada (2) no existe. Se muestra la pagina 1.", html)
        self.assertIn("pcsp-cabildo-licencias-2026", html)
        self.assertIn("govcan-backup-cloud-2026", html)
        self.assertIn("cabildo-redes-2026", html)
        self.assertNotIn("Pagina siguiente", html)

    def test_catalog_page_accepts_prefixed_base_path_route(self) -> None:
        status, headers, body = invoke_app("/licican/")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Catálogo inicial de oportunidades TI de Canarias", html)
        self.assertIn('/licican/oportunidades/pcsp-cabildo-licencias-2026', html)
        self.assertIn('href="/licican/"', html)

    def test_static_route_serves_css_file(self) -> None:
        status, headers, body = invoke_app("/static/style.css")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/css; charset=utf-8", headers["Content-Type"])
        self.assertIn(b"--accent: #0f4c5c;", body)

    def test_api_returns_catalog_only_with_mvp_ti_opportunities(self) -> None:
        status, headers, body = invoke_app("/api/oportunidades")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(3, payload["total_oportunidades_catalogo"])
        self.assertEqual(5, payload["total_registros_origen"])
        self.assertEqual("2026-03-22", payload["oportunidades"][0]["fecha_publicacion_oficial"])
        self.assertEqual(97000, payload["oportunidades"][0]["presupuesto"])
        self.assertEqual(1, payload["paginacion"]["pagina_actual"])
        self.assertEqual(10, payload["paginacion"]["tamano_pagina"])
        self.assertEqual(1, payload["paginacion"]["total_paginas"])
        self.assertTrue(all(item["clasificacion_ti"] == "TI" for item in payload["oportunidades"]))

    def test_api_applies_page_size_from_query_string(self) -> None:
        status, headers, body = invoke_app("/api/oportunidades", "page_size=5")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(5, payload["paginacion"]["tamano_pagina"])
        self.assertEqual(1, payload["paginacion"]["total_paginas"])
        self.assertEqual(3, payload["paginacion"]["resultado_hasta"])

    def test_api_applies_functional_filters_from_query_string(self) -> None:
        status, headers, body = invoke_app(
            "/api/oportunidades",
            "palabra_clave=licencias&presupuesto_min=90000&presupuesto_max=120000&procedimiento=Abierto+simplificado&ubicacion=Santa+Cruz+de+Tenerife",
        )
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(1, payload["total_oportunidades_catalogo"])
        self.assertEqual(["pcsp-cabildo-licencias-2026"], [item["id"] for item in payload["oportunidades"]])
        self.assertEqual("licencias", payload["filtros_activos"]["palabra_clave"])

    def test_api_clamps_out_of_range_page_with_default_page_size(self) -> None:
        status, headers, body = invoke_app("/api/oportunidades", "page=2")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(1, payload["paginacion"]["pagina_actual"])
        self.assertEqual(1, payload["paginacion"]["resultado_desde"])
        self.assertEqual(3, payload["paginacion"]["resultado_hasta"])
        self.assertEqual(["pcsp-cabildo-licencias-2026", "govcan-backup-cloud-2026", "cabildo-redes-2026"], [item["id"] for item in payload["oportunidades"]])
        self.assertTrue(payload["paginacion"]["ajustada"])
        self.assertEqual("fuera_de_rango", payload["paginacion"]["motivo_ajuste"])

    def test_api_normalizes_invalid_page_requests(self) -> None:
        status, _, body = invoke_app("/api/oportunidades", "page=99")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertTrue(payload["paginacion"]["ajustada"])
        self.assertEqual("fuera_de_rango", payload["paginacion"]["motivo_ajuste"])
        self.assertEqual(1, payload["paginacion"]["pagina_actual"])
        self.assertEqual(["pcsp-cabildo-licencias-2026", "govcan-backup-cloud-2026", "cabildo-redes-2026"], [item["id"] for item in payload["oportunidades"]])

    def test_root_preserves_filters_in_pagination_links(self) -> None:
        paginated_catalog = {
            "referencia_funcional": "PB-014",
            "cobertura_aplicada": ["Gobierno de Canarias"],
            "total_registros_origen": 3,
            "total_oportunidades_visibles": 3,
            "total_oportunidades_catalogo": 3,
            "filtros_activos": {"ubicacion": "Gran Canaria"},
            "filtros_disponibles": {"procedimientos": ["Abierto"], "ubicaciones": ["Gran Canaria"]},
            "error_validacion": None,
            "paginacion": {
                "pagina_solicitada": 1,
                "pagina_actual": 1,
                "tamano_pagina": 2,
                "total_paginas": 2,
                "total_resultados": 3,
                "resultado_desde": 1,
                "resultado_hasta": 2,
                "hay_anterior": False,
                "hay_siguiente": True,
                "pagina_anterior": None,
                "pagina_siguiente": 2,
                "ajustada": False,
                "motivo_ajuste": None,
            },
            "oportunidades": [
                {
                    "id": "uno",
                    "titulo": "Oferta 1",
                    "organismo": "Cabildo",
                    "ubicacion": "Gran Canaria",
                    "procedimiento": "Abierto",
                    "presupuesto": 1000,
                    "fecha_publicacion_oficial": "2026-03-20",
                    "fecha_limite": "2026-04-10",
                    "estado": "Abierta",
                    "fuente_oficial": "Cabildo",
                    "url_fuente_oficial": "https://example.test/1",
                    "clasificacion_ti": "TI",
                }
            ],
        }

        with patch("licican.web.router.build_catalog", return_value=paginated_catalog):
            status, _, body = invoke_app("/", "ubicacion=Gran+Canaria")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertIn("ubicacion=Gran+Canaria&amp;page=2", html)
        self.assertIn("page_size=2", html)
        self.assertIn("/licican/?ubicacion=Gran+Canaria&amp;page=2&amp;page_size=2", html)
        self.assertIn('<select id="catalog-page-size" name="page_size" onchange="this.form.submit()">', html)
        self.assertIn('<option value="5">5</option>', html)
        self.assertIn('<option value="10">10</option>', html)
        self.assertIn('<option value="25">25</option>', html)
        self.assertIn('<option value="50">50</option>', html)
        self.assertEqual(1, html.count('class="pagination-bar"'))
        self.assertLess(html.rfind('<tbody>'), html.rfind('class="pagination-bar"'))

    def test_root_reports_adjusted_invalid_page_consistently(self) -> None:
        status, _, body = invoke_app("/", "page=0")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertIn("La pagina solicitada (0) no es valida. Se muestra la pagina 1.", html)

    def test_api_rejects_invalid_budget_range_with_explicit_message(self) -> None:
        status, headers, body = invoke_app(
            "/api/oportunidades",
            "presupuesto_min=120000&presupuesto_max=90000",
        )
        payload = json.loads(body)

        self.assertEqual("400 Bad Request", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(
            "El presupuesto mínimo no puede ser mayor que el presupuesto máximo. "
            "Revisa el rango antes de aplicar los filtros.",
            payload["error_validacion"],
        )
        self.assertEqual(3, payload["total_oportunidades_catalogo"])

    def test_detail_page_renders_critical_fields_and_latest_visible_update(self) -> None:
        status, headers, body = invoke_app("/oportunidades/pcsp-cabildo-licencias-2026")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Suministro de licencias y software de gestion tributaria insular", html)
        self.assertIn("2026-03-22", html)
        self.assertIn("2026-04-10", html)
        self.assertIn("97.000 EUR", html)
        self.assertIn("Rectificacion", html)

    def test_detail_api_returns_structured_detail_payload(self) -> None:
        status, headers, body = invoke_app("/api/oportunidades/pcsp-cabildo-licencias-2026")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual("pcsp-cabildo-licencias-2026", payload["id"])
        self.assertEqual("2026-03-22", payload["fecha_publicacion_oficial"])
        self.assertEqual("2026-04-10", payload["fecha_limite"])
        self.assertIsNone(payload["fichero_origen_atom"])
        self.assertEqual(
            ["Oferta economica", "Cobertura funcional de la plataforma", "Plan de migracion y soporte"],
            payload["criterios_adjudicacion"],
        )

    def test_consolidated_dataset_page_renders_excel_tabs_and_rows(self) -> None:
        status, headers, body = invoke_app("/datos-consolidados")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="dataset-summary-panel"', html)
        self.assertIn('class="table-wrap dataset-table-wrap"', html)
        self.assertIn("Licitaciones TI Canarias", html)
        self.assertIn("Detalle Lotes", html)
        self.assertIn("Adjudicaciones", html)
        self.assertIn("Servicios y suministros de un conjunto de soluciones digitales innovadoras", html)
        self.assertIn("licitacionesPerfilesContratanteCompleto3_20260322_190106.atom", html)

    def test_consolidated_dataset_supports_lot_and_award_tabs(self) -> None:
        lot_status, _, lot_body = invoke_app("/datos-consolidados", "vista=lotes")
        award_status, _, award_body = invoke_app("/datos-consolidados", "vista=adjudicaciones")

        self.assertEqual("200 OK", lot_status)
        self.assertIn("LOTE 1: Portal web de análisis de turismo inteligente", lot_body.decode("utf-8"))
        self.assertEqual("200 OK", award_status)
        self.assertIn("SOLUCIONES AVANZADAS EN INFORMATICA APLICADA", award_body.decode("utf-8"))
        self.assertIn("Fichero Origen", award_body.decode("utf-8"))

    def test_consolidated_dataset_api_returns_excel_counts(self) -> None:
        status, headers, body = invoke_app("/api/datos-consolidados")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual("PB-012", payload["referencia_funcional"])
        self.assertEqual({"licitaciones": 23, "lotes": 29, "adjudicaciones": 18}, payload["resumen"])
        self.assertEqual(
            "licitacionesPerfilesContratanteCompleto3_20260322_190106.atom",
            payload["licitaciones"][0]["fichero_origen_atom"],
        )

    def test_excel_detail_pages_show_atom_traceability(self) -> None:
        licitacion_status, _, licitacion_body = invoke_app("/datos-consolidados/licitaciones/114-2025")
        adjudicacion_status, _, adjudicacion_body = invoke_app(
            "/datos-consolidados/adjudicaciones/2565-2024-pt1-pccntr-4934579"
        )

        licitacion_html = licitacion_body.decode("utf-8")
        adjudicacion_html = adjudicacion_body.decode("utf-8")

        self.assertEqual("200 OK", licitacion_status)
        self.assertIn('id="detail-licitacion-panel"', licitacion_html)
        self.assertIn('class="table-wrap detail-table-wrap"', licitacion_html)
        self.assertIn("Fichero .atom origen", licitacion_html)
        self.assertIn("licitacionesPerfilesContratanteCompleto3_20260322_190106.atom", licitacion_html)
        self.assertEqual("200 OK", adjudicacion_status)
        self.assertIn('id="detail-adjudicacion-panel"', adjudicacion_html)
        self.assertIn('class="table-wrap detail-table-wrap"', adjudicacion_html)
        self.assertIn("Fichero .atom origen", adjudicacion_html)

    def test_coverage_page_remains_available_on_dedicated_route(self) -> None:
        status, headers, body = invoke_app("/cobertura-fuentes")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="coverage-summary-panel"', html)
        self.assertIn('class="table-wrap coverage-table-wrap"', html)
        self.assertIn("Cobertura inicial de fuentes oficiales del MVP", html)
        self.assertIn("Gobierno de Canarias", html)

    def test_api_returns_configured_source_coverage(self) -> None:
        status, headers, body = invoke_app("/api/fuentes")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(6, len(payload["sources"]))
        self.assertEqual({"MVP": 3, "Posterior": 2, "Por definir": 1}, payload["summary"])

    def test_real_source_prioritization_page_lists_named_official_sources_by_wave(self) -> None:
        status, headers, body = invoke_app("/priorizacion-fuentes-reales")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Priorización de fuentes reales oficiales para recopilación", html)
        self.assertIn("BOC", html)
        self.assertIn("BOP Las Palmas", html)
        self.assertIn("BOE", html)
        self.assertIn("Ola 1", html)
        self.assertIn("Fuera de alcance en esta iteración", html)

    def test_real_source_prioritization_api_returns_waves_and_out_of_scope(self) -> None:
        status, headers, body = invoke_app("/api/fuentes-prioritarias")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(["BOC", "BOP Las Palmas", "BOE"], [item["nombre"] for item in payload["sources"]])
        self.assertEqual({"Ola 1": 1, "Ola 2": 1, "Ola 3": 1}, payload["summary"])
        self.assertIn("Alertas tempranas", payload["fuera_de_alcance"])

    def test_classification_page_renders_auditable_rules(self) -> None:
        status, headers, body = invoke_app("/clasificacion-ti")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="classification-rules-panel"', html)
        self.assertIn('id="classification-examples-panel"', html)
        self.assertIn('class="table-wrap classification-table-wrap"', html)
        self.assertIn("Clasificación TI auditable", html)
        self.assertIn("Casos frontera", html)
        self.assertIn("telecomunicaciones", html)

    def test_classification_api_returns_rules_and_audited_examples(self) -> None:
        status, headers, body = invoke_app("/api/clasificacion-ti")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertIn("PB-006", payload["referencia_funcional"])
        self.assertEqual(5, len(payload["ejemplos_auditados"]))
        self.assertTrue(all(item["coincide_con_esperado"] for item in payload["ejemplos_auditados"]))

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
        with patch.dict(os.environ, {"LICICAN_ROLE": "lector"}, clear=False):
            status, _, body = invoke_app("/")
            alerts_status, alerts_headers, alerts_body = invoke_app("/alertas")

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
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LICICAN_ROLE": "administrador", "LICICAN_USER_ID": "admin-1"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="palabra_clave=licencias")
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LICICAN_ROLE": "colaborador", "LICICAN_USER_ID": "colab-1"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="procedimiento=Abierto")
                page_status, _, page_body = invoke_app("/alertas")
                api_status, _, api_body = invoke_app("/api/alertas")

        self.assertEqual("200 OK", page_status)
        html = page_body.decode("utf-8")
        self.assertIn("alerta-002", html)
        self.assertNotIn("alerta-001", html)
        payload = json.loads(api_body)
        self.assertEqual("200 OK", api_status)
        self.assertEqual(1, payload["summary"]["total_alertas"])
        self.assertEqual("colab-1", payload["alerts"][0]["usuario_id"])

    def test_collaborator_cannot_edit_alerts_from_other_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LICICAN_ROLE": "administrador", "LICICAN_USER_ID": "admin-1"},
                clear=False,
            ):
                invoke_app("/alertas", method="POST", body="palabra_clave=licencias")
            with patch.dict(
                os.environ,
                {"LICICAN_ALERTS_PATH": str(alerts_path), "LICICAN_ROLE": "colaborador", "LICICAN_USER_ID": "colab-1"},
                clear=False,
            ):
                status, headers, body = invoke_app("/alertas/alerta-001/editar", method="POST", body="procedimiento=Abierto")

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
        with patch.dict(os.environ, {"LICICAN_ROLE": "colaborador", "LICICAN_USER_ID": "colab-1"}, clear=False):
            kpi_status, _, kpi_body = invoke_app("/kpis")

        self.assertEqual("200 OK", admin_status)
        admin_html = admin_body.decode("utf-8")
        self.assertIn('id="permissions-summary-panel"', admin_html)
        self.assertIn('id="permissions-matrix-panel"', admin_html)
        self.assertIn('class="table-wrap permissions-table-wrap"', admin_html)
        self.assertIn("Matriz funcional de roles y permisos", admin_html)
        self.assertEqual("200 OK", kpi_status)
        self.assertIn("KPIs operativos visibles por rol", kpi_body.decode("utf-8"))

    def test_unknown_path_returns_404(self) -> None:
        status, headers, body = invoke_app("/desconocido")

        self.assertEqual("404 Not Found", status)
        self.assertEqual("text/plain; charset=utf-8", headers["Content-Type"])
        self.assertEqual("No encontrado", body.decode("utf-8"))

    def test_detail_path_returns_404_for_non_visible_opportunity(self) -> None:
        status, headers, body = invoke_app("/oportunidades/govcan-teleco-mixto-2026")

        self.assertEqual("404 Not Found", status)
        self.assertEqual("text/plain; charset=utf-8", headers["Content-Type"])
        self.assertEqual("No encontrado", body.decode("utf-8"))

    def test_main_handles_keyboard_interrupt_with_controlled_shutdown(self) -> None:
        stdout = io.StringIO()

        with patch.dict(os.environ, {"BASE_PATH": "/licican", "PORT": "8123"}, clear=False):
            with patch("licican.app.make_server") as make_server_mock:
                server = make_server_mock.return_value.__enter__.return_value
                server.serve_forever.side_effect = KeyboardInterrupt

                with redirect_stdout(stdout):
                    main()

        output = stdout.getvalue()
        self.assertIn("Servidor disponible en http://127.0.0.1:8123/licican", output)
        self.assertIn("Servidor detenido de forma controlada.", output)
        make_server_mock.assert_called_once_with("127.0.0.1", 8123, application)
        server.server_close.assert_called_once_with()

    def test_main_uses_configured_host_when_present(self) -> None:
        stdout = io.StringIO()

        with patch.dict(os.environ, {"BASE_PATH": "/licican", "HOST": "0.0.0.0", "PORT": "8124"}, clear=False):
            with patch("licican.app.make_server") as make_server_mock:
                server = make_server_mock.return_value.__enter__.return_value
                server.serve_forever.side_effect = KeyboardInterrupt

                with redirect_stdout(stdout):
                    main()

        output = stdout.getvalue()
        self.assertIn("Servidor disponible en http://0.0.0.0:8124/licican", output)
        make_server_mock.assert_called_once_with("0.0.0.0", 8124, application)

    def test_main_rejects_invalid_port_configuration(self) -> None:
        with patch.dict(os.environ, {"BASE_PATH": "/licican", "PORT": "not-a-number"}, clear=False):
            with self.assertRaisesRegex(ValueError, "PORT debe ser un numero entero valido"):
                main()

    def test_root_shows_empty_state_when_catalog_has_no_visible_opportunities(self) -> None:
        empty_catalog = {
            "referencia_funcional": "PB-001",
            "cobertura_aplicada": ["Gobierno de Canarias"],
            "total_registros_origen": 0,
            "total_oportunidades_visibles": 0,
            "total_oportunidades_catalogo": 0,
            "filtros_activos": {},
            "filtros_disponibles": {"procedimientos": [], "ubicaciones": []},
            "paginacion": {
                "pagina_solicitada": 1,
                "pagina_actual": 1,
                "tamano_pagina": 2,
                "total_paginas": 1,
                "total_resultados": 0,
                "resultado_desde": 0,
                "resultado_hasta": 0,
                "hay_anterior": False,
                "hay_siguiente": False,
                "pagina_anterior": None,
                "pagina_siguiente": None,
                "ajustada": False,
                "motivo_ajuste": None,
            },
            "oportunidades": [],
        }

        with patch("licican.web.router.build_catalog", return_value=empty_catalog):
            status, headers, body = invoke_app("/")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("No hay oportunidades TI disponibles dentro de la cobertura MVP en este momento.", html)

    def test_root_renders_active_filters_and_empty_state_for_filtered_catalog(self) -> None:
        status, headers, body = invoke_app("/", "palabra_clave=inexistente")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Filtros activos", html)
        self.assertIn("Palabra clave: inexistente", html)
        self.assertIn("No hay resultados con los filtros activos.", html)
        self.assertIn("Limpiar filtros", html)

    def test_root_requests_correction_for_invalid_budget_range(self) -> None:
        status, headers, body = invoke_app("/", "presupuesto_min=120000&presupuesto_max=90000")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Corrige el rango de presupuesto.", html)
        self.assertIn("El presupuesto mínimo no puede ser mayor que el presupuesto máximo.", html)
        self.assertNotIn("No hay resultados con los filtros activos.", html)

    def test_users_page_renders_summary_table_and_navigation_for_admin(self) -> None:
        with self._patch_users_db():
            status, headers, body = invoke_app("/usuarios")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Gestion de usuarios", html)
        self.assertNotIn("Usuarios totales", html)
        self.assertNotIn("Gestion administrativa de cuentas", html)
        self.assertIn("Ana Lopez", html)
        self.assertIn('id="toggle-users-create"', html)
        self.assertIn("Nuevo usuario", html)
        self.assertIn('id="users-create-panel" hidden', html)
        self.assertIn('id="users-filters-panel"', html)
        self.assertIn('id="users-table-panel"', html)
        self.assertIn('class="table-wrap users-table-wrap"', html)
        self.assertNotIn('id="users-selected-panel"', html)
        self.assertIn('href="/licican/usuarios"', html)
        self.assertIn('class="nav-link active" href="/licican/usuarios"', html)

        create_panel_index = html.index('id="users-create-panel"')
        filters_panel_index = html.index('id="users-filters-panel"')
        table_panel_index = html.index('id="users-table-panel"')
        toggle_button_index = html.index('id="toggle-users-create"')
        self.assertLess(toggle_button_index, create_panel_index)
        self.assertLess(create_panel_index, filters_panel_index)

        filters_panel_html = html[filters_panel_index:table_panel_index]
        self.assertIn('name="busqueda"', filters_panel_html)
        self.assertIn('name="rol"', filters_panel_html)
        self.assertNotIn('name="estado"', filters_panel_html)
        self.assertNotIn('name="superficie"', filters_panel_html)
        self.assertNotIn('Area / modulo / superficie', filters_panel_html)
        self.assertIn("panel.hidden = true", html)

    def test_users_page_denied_to_reader_role(self) -> None:
        with patch.dict(os.environ, {"LICICAN_ROLE": "lector"}, clear=False):
            status, headers, body = invoke_app("/usuarios")

        self.assertEqual("403 Forbidden", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", body.decode("utf-8"))

    def test_user_creation_route_redirects_and_persists_account(self) -> None:
        state = SeededUsersState.seed()
        form_data = urlencode(
            {
                "nombre": "Eva",
                "apellidos": "Santos",
                "email": "eva.santos@licican.local",
                "rol_principal": "responsable",
                "estado": "pendiente",
                "observaciones_internas": "Alta desde pruebas",
            }
        )
        with self._patch_users_db(state):
            status, headers, _ = invoke_app("/usuarios", method="POST", body=form_data)
            page_status, _, page_body = invoke_app("/usuarios")

        html = page_body.decode("utf-8")
        self.assertEqual("303 See Other", status)
        self.assertEqual("/licican/usuarios?mensaje=Usuario+creado+y+registrado", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("Eva Santos", html)
        self.assertIn("eva.santos@licican.local", html)
        self.assertIn("usr-005", html)
        self.assertIn("pendiente", html)

    def test_user_detail_page_shows_selected_user_history(self) -> None:
        with self._patch_users_db():
            status, headers, body = invoke_app("/usuarios/usr-003")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Detalle y edicion", html)
        self.assertIn("Laura Gonzalez", html)
        self.assertIn("Reenviar invitacion", html)
        self.assertIn("Historial de cambios", html)
