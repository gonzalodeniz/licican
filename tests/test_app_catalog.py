from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

import psycopg2

from tests.shared.app_http import invoke_app


class ApplicationCatalogTests(unittest.TestCase):
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
        self.assertIn('<link rel="stylesheet" href="/licican/static/style.css"', html)
        self.assertNotIn("Pagina 1 de 1", html)
        self.assertNotIn("Mostrando 1-3 de 3", html)
        self.assertNotIn("Pagina siguiente", html)
        self.assertNotIn("Ir a la pagina", html)
        self.assertIn("Menu principal", html)
        self.assertIn('class="nav-link active" href="/licican/"', html)
        self.assertNotIn("Datos consolidados", html)
        self.assertIn("Alertas", html)
        self.assertIn('href="/licican/conservacion"', html)
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

    def test_removed_dataset_routes_return_not_found(self) -> None:
        for path in (
            "/datos-consolidados",
            "/datos-consolidados/licitaciones/114-2025",
            "/datos-consolidados/adjudicaciones/2565-2024-pt1-pccntr-4934579",
            "/api/datos-consolidados",
        ):
            status, _, body = invoke_app(path)
            self.assertEqual("404 Not Found", status)
            self.assertIn(b"No encontrado", body)

        status, _, body = invoke_app("/datos-consolidados", "vista=lotes")
        self.assertEqual("404 Not Found", status)
        self.assertIn(b"No encontrado", body)

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
