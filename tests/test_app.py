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

import psycopg2

from licican.app import application, main


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
    with patch.dict(os.environ, env_overrides, clear=False):
        body = b"".join(application(environ, start_response))
    return captured["status"], captured["headers"], body


class ApplicationTests(unittest.TestCase):
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
        self.assertIn("Servicio cloud para copias de seguridad y continuidad de sistemas corporativos", html)
        self.assertIn("Ver oferta concreta", html)
        self.assertIn("Publicación oficial", html)
        self.assertIn("Fuente oficial", html)
        self.assertIn('/licican/oportunidades/pcsp-cabildo-licencias-2026', html)
        self.assertIn('action="/licican"', html)
        self.assertIn("Licitaciones TI Canarias", html)
        self.assertIn("Detalle Lotes", html)
        self.assertIn("Adjudicaciones", html)
        self.assertIn('/licican/datos-consolidados', html)
        self.assertIn("Pagina 1 de 2", html)
        self.assertIn("Mostrando 1-2 de 3", html)
        self.assertIn("Pagina siguiente", html)
        self.assertIn("Ir a la pagina", html)

    def test_catalog_page_accepts_prefixed_base_path_route(self) -> None:
        status, headers, body = invoke_app("/licican/")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Catálogo inicial de oportunidades TI de Canarias", html)
        self.assertIn('/licican/oportunidades/pcsp-cabildo-licencias-2026', html)
        self.assertIn('href="/licican"', html)

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
        self.assertEqual(2, payload["paginacion"]["tamano_pagina"])
        self.assertEqual(2, payload["paginacion"]["total_paginas"])
        self.assertTrue(all(item["clasificacion_ti"] == "TI" for item in payload["oportunidades"]))

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

    def test_api_allows_requesting_a_specific_page(self) -> None:
        status, headers, body = invoke_app("/api/oportunidades", "page=2")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertEqual("application/json; charset=utf-8", headers["Content-Type"])
        self.assertEqual(2, payload["paginacion"]["pagina_actual"])
        self.assertEqual(3, payload["paginacion"]["resultado_desde"])
        self.assertEqual(3, payload["paginacion"]["resultado_hasta"])
        self.assertEqual(["cabildo-redes-2026"], [item["id"] for item in payload["oportunidades"]])

    def test_api_normalizes_invalid_page_requests(self) -> None:
        status, _, body = invoke_app("/api/oportunidades", "page=99")
        payload = json.loads(body)

        self.assertEqual("200 OK", status)
        self.assertTrue(payload["paginacion"]["ajustada"])
        self.assertEqual("fuera_de_rango", payload["paginacion"]["motivo_ajuste"])
        self.assertEqual(2, payload["paginacion"]["pagina_actual"])
        self.assertEqual(["cabildo-redes-2026"], [item["id"] for item in payload["oportunidades"]])

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

        with patch("licican.app.build_catalog", return_value=paginated_catalog):
            status, _, body = invoke_app("/", "ubicacion=Gran+Canaria")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertIn("ubicacion=Gran+Canaria&amp;page=2", html)

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

        self.assertEqual("200 OK", licitacion_status)
        self.assertIn("Fichero .atom origen", licitacion_body.decode("utf-8"))
        self.assertIn("licitacionesPerfilesContratanteCompleto3_20260322_190106.atom", licitacion_body.decode("utf-8"))
        self.assertEqual("200 OK", adjudicacion_status)
        self.assertIn("Fichero .atom origen", adjudicacion_body.decode("utf-8"))

    def test_coverage_page_remains_available_on_dedicated_route(self) -> None:
        status, headers, body = invoke_app("/cobertura-fuentes")
        html = body.decode("utf-8")

        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
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

    def test_alert_creation_rejects_empty_form(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            with patch.dict(os.environ, {"LICICAN_ALERTS_PATH": str(alerts_path)}, clear=False):
                status, headers, body = invoke_app("/alertas", method="POST")

        html = body.decode("utf-8")
        self.assertEqual("400 Bad Request", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("La alerta necesita al menos un criterio funcional", html)

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

        with patch("licican.app.build_catalog", return_value=empty_catalog):
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
