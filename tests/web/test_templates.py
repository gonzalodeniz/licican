from __future__ import annotations

import unittest
from types import SimpleNamespace

from licican.web.templates.alerts import render_alert_form
from licican.web.templates.base import page_template
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.components import render_metric, render_role_badge, render_status_note, render_table
from licican.web.templates.coverage import render_coverage
from licican.web.templates.detail import render_opportunity_detail
from licican.web.templates.kpis import render_kpis
from licican.web.templates.pipeline import render_pipeline
from licican.web.templates.prioritization import render_prioritization
from licican.web.templates.retention import render_retention_control
from licican.shared.text import slugify


class TemplateSmokeTests(unittest.TestCase):
    def test_page_template_renders_layout(self) -> None:
        html = page_template("Titulo", "Encabezado", "Hero", "Cuerpo", "<p>contenido</p>", base_path="/licican")
        self.assertIn("/licican/static/style.css", html)
        self.assertIn("Menu principal", html)
        self.assertNotIn("Datos consolidados", html)

    def test_page_template_places_logout_button_in_sidebar_footer(self) -> None:
        access_context = SimpleNamespace(
            role="administrador",
            role_label="Administrador",
            scope_label="global",
            user_id="admin",
            capabilities=frozenset({"view_catalog"}),
            display_name="Superadministrador",
            is_superadmin=True,
            csrf_token="csrf-token",
            auto_login_active=False,
        )
        html = page_template("Titulo", "Encabezado", "Hero", "Cuerpo", "<p>contenido</p>", base_path="/licican", access_context=access_context)

        self.assertIn('class="nav-footer"', html)
        self.assertIn("Cerrar sesión", html)
        self.assertLess(html.index("Cerrar sesión"), html.index("Menu principal"))

    def test_component_helpers_render_html(self) -> None:
        self.assertIn("metric", render_metric(2, "Alertas"))
        self.assertIn("note-warning", render_status_note("Error", "warn"))
        self.assertIn("<table>", render_table(["A"], ["<tr><td>x</td></tr>"]))
        self.assertIn("badge-rol--gestor", render_role_badge("manager"))
        self.assertIn("Manager", render_role_badge("manager"))
        self.assertIn("Manager", render_role_badge("gestor"))
        self.assertIn("Invitado", render_role_badge("invitado"))
        self.assertIn("badge-rol--administrador-funcional", render_role_badge("Administrador funcional"))
        self.assertEqual("administracion-funcional", slugify("Administración Funcional"))

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

    def test_opportunity_detail_template_renders_smoke(self) -> None:
        detail = {"id": "uno", "titulo": "Oferta", "actualizacion_oficial_mas_reciente": None, "criterios_adjudicacion": [], "estado": "Publicada", "fecha_limite": "2026-04-10", "presupuesto": 1000, "organismo": "Cabildo", "ubicacion": "Canarias", "procedimiento": "Abierto", "fecha_publicacion_oficial": "2026-03-31", "url_fuente_oficial": "https://example.test", "fuente_oficial": "Fuente", "fichero_origen_atom": "a.atom", "descripcion": "Desc", "solvencia_tecnica": None}
        self.assertIn("Ficha de detalle", render_opportunity_detail(detail))

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

    def test_kpis_template_renders_product_definitions(self) -> None:
        html = render_kpis(
            {
                "rol_activo": "Manager",
                "alcance": "Operativo para manager.",
                "modo_captura": "Mixto: cobertura visible automatizada y adopción/uso con primera consolidación manual si falta instrumentación completa.",
                "resumen": {
                    "fuentes_mvp": "3/3",
                    "cobertura_visible": "3 fuentes",
                    "alertas_activas": "0 alertas",
                    "pipeline_visible": "0 oportunidades",
                },
                "indicadores": [
                    {
                        "nombre": "Cobertura de fuentes priorizadas",
                        "valor_label": "Cobertura actual",
                        "valor_actual": "3/3",
                        "definicion": "Porcentaje de fuentes MVP priorizadas que producen datos visibles y trazables en la ventana de evaluacion.",
                        "formula": "fuentes_MVP_con_datos / fuentes_MVP_priorizadas x 100",
                        "umbral_inicial": "90 por ciento",
                        "decision": "Si cae por debajo del umbral, frenar expansion y estabilizar trazabilidad e ingestion.",
                        "captura": "Automatica sobre la cobertura visible del catalogo y la configuracion del MVP.",
                        "limitacion": "La medicion actual usa la cobertura visible del producto.",
                    },
                    {
                        "nombre": "Adopcion de alertas activas",
                        "valor_label": "Usuarios con alerta activa",
                        "valor_actual": "Sin alertas activas",
                        "definicion": "Porcentaje de usuarios activos semanales que disponen de al menos una alerta activa.",
                        "formula": "usuarios_activos_con_alerta_activa / usuarios_activos_semanales x 100",
                        "umbral_inicial": "30 por ciento",
                        "decision": "Si baja del umbral, simplificar onboarding y configuracion de alertas.",
                        "captura": "Consolidacion operativa de alertas activas y usuarios con alerta en la captura actual.",
                        "limitacion": "La primera captura puede ser manual.",
                    },
                ],
            },
            base_path="/licican",
        )
        self.assertIn("KPIs iniciales de cobertura, adopción y uso", html)
        self.assertIn("Cobertura de fuentes priorizadas", html)
        self.assertIn("Umbral inicial", html)
        self.assertIn("Decisión asociada", html)

    def test_retention_template_renders_smoke(self) -> None:
        html = render_retention_control(
            {
                "politica": {"antiguedad_dias": 180, "modo": "desde_creacion", "modo_label": "Dias desde la creacion", "actualizada_en": "2026-04-03T09:00:00Z"},
                "resumen": {"conservar": 2, "archivar": 1, "mantener_activas": 1, "archivadas_existentes": 4},
                "modos_disponibles": [{"valor": "desde_creacion", "etiqueta": "Dias desde la creacion"}],
                "grupos": {
                    "conservar": [],
                    "archivar": [{"expediente": "EXP-1", "titulo": "Archivada", "organismo": "Cabildo", "estado": "RES", "seguimiento_activo": False, "dias_antiguedad": 50, "motivo": "Supera politica"}],
                    "mantener_activas": [],
                },
            }
        )
        self.assertIn("Panel de control de conservacion y archivado", html)
        self.assertIn("Aplicar archivado ahora", html)
