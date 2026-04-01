from __future__ import annotations

import unittest
from types import SimpleNamespace

from licican.web.templates.alerts import render_alert_form
from licican.web.templates.base import page_template
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.components import render_metric, render_status_note, render_tab_nav, render_table
from licican.web.templates.coverage import render_coverage
from licican.web.templates.dataset import render_datos_consolidados
from licican.web.templates.detail import render_adjudicacion_detail, render_licitacion_detail, render_opportunity_detail
from licican.web.templates.pipeline import render_pipeline
from licican.web.templates.prioritization import render_prioritization


class TemplateSmokeTests(unittest.TestCase):
    def test_page_template_renders_layout(self) -> None:
        html = page_template("Titulo", "Encabezado", "Hero", "Cuerpo", "<p>contenido</p>", base_path="/licican")
        self.assertIn("/licican/static/style.css", html)
        self.assertIn("Menu principal", html)

    def test_component_helpers_render_html(self) -> None:
        self.assertIn("metric", render_metric(2, "Alertas"))
        self.assertIn("note-warning", render_status_note("Error", "warn"))
        self.assertIn("Licitaciones TI Canarias", render_tab_nav("", "licitaciones", [("licitaciones", "Licitaciones TI Canarias")]))
        self.assertIn("<table>", render_table(["A"], ["<tr><td>x</td></tr>"]))

    def test_catalog_template_renders_catalog(self) -> None:
        html = render_catalog(
            {
                "referencia_funcional": "PB-011",
                "cobertura_aplicada": ["snapshot.atom"],
                "total_oportunidades_visibles": 1,
                "total_oportunidades_catalogo": 1,
                "filtros_activos": {},
                "filtros_disponibles": {"procedimientos": ["Abierto"], "ubicaciones": ["Canarias"]},
                "error_validacion": None,
                "paginacion": {"total_paginas": 1, "pagina_actual": 1, "resultado_desde": 1, "resultado_hasta": 1, "total_resultados": 1, "hay_anterior": False, "hay_siguiente": False, "pagina_anterior": None, "pagina_siguiente": None, "ajustada": False, "motivo_ajuste": None, "pagina_solicitada": 1},
                "oportunidades": [{"id": "uno", "titulo": "Oferta", "organismo": "Cabildo", "ubicacion": "Canarias", "procedimiento": "Abierto", "presupuesto": 1000, "fecha_publicacion_oficial": "2026-03-31", "fecha_limite": "2026-04-10", "estado": "Publicada", "url_fuente_oficial": "https://example.test", "fuente_oficial": "Fuente"}],
            }
        )
        self.assertIn("Ver oferta concreta", html)

    def test_view_templates_render_smoke(self) -> None:
        source = SimpleNamespace(nombre="Fuente", categoria="Portal", estado="MVP", alcance="Insular", descripcion="Desc", referencia_funcional="PB-007")
        self.assertIn("Cobertura inicial", render_coverage([source], {"MVP": 1, "Posterior": 0, "Por definir": 0}))
        prioritized = SimpleNamespace(ola="Ola 1", url_oficial="https://example.test", nombre="BOC", categoria="Boletín", alcance="Canarias", justificacion="Alta", trazabilidad="PB-009")
        self.assertIn("Priorización", render_prioritization("PB-009", [prioritized], ("BOE",), {"Ola 1": 1, "Ola 2": 0, "Ola 3": 0}))
        rules = SimpleNamespace(inclusion_palabras_clave=("software",), inclusion_cpv_prefixes=("72",), exclusion_palabras_clave=("mobiliario",), frontera_palabras_clave=("teleco",))
        audited = [{"titulo": "Oferta", "clasificacion_esperada": "TI", "clasificacion_obtenida": "TI", "coincidencias_inclusion": ["software"], "coincidencias_exclusion": [], "coincidencias_frontera": [], "motivo_ejemplo": "PB-006"}]
        self.assertIn("Clasificación TI auditable", render_classification("PB-006", rules, audited))

    def test_dataset_and_detail_templates_render_smoke(self) -> None:
        dataset = {"archivo_origen": "data/file.xlsx", "referencia_funcional": "PB-012", "resumen": {"licitaciones": 1, "lotes": 0, "adjudicaciones": 0}}
        self.assertIn("Datos consolidados TI Canarias", render_datos_consolidados(dataset, "licitaciones", "Licitaciones TI Canarias", "Desc", [("id_expediente", "ID")], ['<a>Ver</a>'], [{"id_expediente": "EXP-1"}]))
        detail = {"id": "uno", "titulo": "Oferta", "actualizacion_oficial_mas_reciente": None, "criterios_adjudicacion": [], "estado": "Publicada", "fecha_limite": "2026-04-10", "presupuesto": 1000, "organismo": "Cabildo", "ubicacion": "Canarias", "procedimiento": "Abierto", "fecha_publicacion_oficial": "2026-03-31", "url_fuente_oficial": "https://example.test", "fuente_oficial": "Fuente", "fichero_origen_atom": "a.atom", "descripcion": "Desc", "solvencia_tecnica": None}
        self.assertIn("Ficha de detalle", render_opportunity_detail(detail))
        lic = {"titulo": "Licitación", "id_expediente": "EXP-1", "estado": "Publicada", "organo_contratacion": "Cabildo", "importe_estimado": None, "importe_con_iva": None, "importe_sin_iva": None, "cpvs_informaticos": None, "ubicacion": None, "procedimiento": None, "plazo_presentacion": None, "numero_lotes": None, "numero_adjudicaciones": None, "fecha_actualizacion": None, "fichero_origen_atom": "a.atom", "enlace_placsp": None}
        self.assertIn("Detalle de licitación", render_licitacion_detail(lic))
        adj = {"titulo": "Adjudicación", "id_expediente": "EXP-1", "resultado": None, "fecha_adjudicacion": None, "lote": None, "ganador": None, "nif_ganador": None, "ciudad_ganador": None, "pais": None, "importe_adjudicacion_sin_iva": None, "importe_adjudicacion_total": None, "ofertas_recibidas": None, "ofertas_pyme": None, "pyme_adjudicatario": None, "id_contrato": None, "fecha_contrato": None, "fichero_origen_atom": "a.atom", "descripcion": None, "licitacion_slug": None}
        self.assertIn("Detalle de adjudicación", render_adjudicacion_detail(adj))

    def test_alert_template_renders_smoke(self) -> None:
        html = render_alert_form("", {}, {"procedimientos": ["Abierto"], "ubicaciones": ["Canarias"]})
        self.assertIn("Guardar alerta", html)

    def test_pipeline_template_renders_smoke(self) -> None:
        html = render_pipeline(
            {
                "referencia_funcional": "PB-005",
                "estados_disponibles": ["Nueva", "Evaluando"],
                "summary": {"total_oportunidades": 1, "con_advertencia_oficial": 0, "estado_nueva": 1},
                "pipeline": [
                    {
                        "opportunity_id": "uno",
                        "estado_seguimiento": "Nueva",
                        "creada_en": "2026-03-31T10:00:00Z",
                        "actualizada_en": "2026-03-31T10:00:00Z",
                        "advertencia_oficial": None,
                        "oportunidad": {
                            "titulo": "Oferta",
                            "organismo": "Cabildo",
                            "ubicacion": "Canarias",
                            "procedimiento": "Abierto",
                            "presupuesto": 1000,
                            "fecha_publicacion_oficial": "2026-03-31",
                            "fecha_limite": "2026-04-10",
                            "estado_oficial": "Abierta",
                            "url_fuente_oficial": "https://example.test",
                        },
                    }
                ],
            }
        )
        self.assertIn("Pipeline de seguimiento de oportunidades", html)
        self.assertIn("Actualizar estado", html)
