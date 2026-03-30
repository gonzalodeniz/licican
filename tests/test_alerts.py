from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from podencoti.alerts import create_alert, deactivate_alert, load_alerts, summarize_alerts, update_alert
from podencoti.opportunity_catalog import CatalogFilters


class AlertsTests(unittest.TestCase):
    def test_create_alert_requires_at_least_one_criterion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"

            with self.assertRaisesRegex(ValueError, "La alerta necesita al menos un criterio funcional"):
                create_alert(CatalogFilters(), path=alerts_path, now="2026-03-25T10:00:00Z")

    def test_create_alert_persists_active_alert_with_internal_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"

            created_alert = create_alert(
                CatalogFilters(palabra_clave="backup"),
                path=alerts_path,
                catalog_path=Path("data"),
                now="2026-03-25T10:00:00Z",
            )
            reference, alerts = load_alerts(alerts_path)

        self.assertIn("PB-004", reference)
        self.assertEqual("alerta-001", created_alert.id)
        self.assertEqual(1, len(alerts))
        self.assertTrue(alerts[0].activa)
        self.assertEqual({"palabra_clave": "backup"}, alerts[0].filtros.active_filters())
        self.assertEqual(["govcan-backup-cloud-2026"], [match.id for match in alerts[0].coincidencias])

    def test_update_alert_recomputes_criteria_and_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            create_alert(
                CatalogFilters(palabra_clave="backup"),
                path=alerts_path,
                catalog_path=Path("data"),
                now="2026-03-25T10:00:00Z",
            )

            updated_alert = update_alert(
                "alerta-001",
                CatalogFilters(procedimiento="Abierto"),
                path=alerts_path,
                catalog_path=Path("data"),
                now="2026-03-25T11:00:00Z",
            )

        self.assertEqual({"procedimiento": "Abierto"}, updated_alert.filtros.active_filters())
        self.assertEqual(
            ["govcan-backup-cloud-2026", "cabildo-redes-2026"],
            [match.id for match in updated_alert.coincidencias],
        )
        self.assertEqual("2026-03-25T11:00:00Z", updated_alert.actualizada_en)

    def test_deactivate_alert_marks_it_inactive_without_deleting_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            create_alert(
                CatalogFilters(palabra_clave="backup"),
                path=alerts_path,
                catalog_path=Path("data"),
                now="2026-03-25T10:00:00Z",
            )

            deactivated_alert = deactivate_alert("alerta-001", path=alerts_path, now="2026-03-25T11:30:00Z")
            _, alerts = load_alerts(alerts_path)
            summary = summarize_alerts(alerts)

        self.assertFalse(deactivated_alert.activa)
        self.assertEqual(1, len(deactivated_alert.coincidencias))
        self.assertEqual(
            {
                "total_alertas": 1,
                "alertas_activas": 0,
                "alertas_inactivas": 1,
                "coincidencias_activas": 0,
            },
            summary,
        )

    def test_create_alert_excludes_non_actionable_official_states_from_matches(self) -> None:
        opportunities_payload = {
            "referencia_funcional": "PB-001",
            "opportunities": [
                {
                    "id": "licitacion-anulada",
                    "titulo": "Servicio TI cancelado",
                    "descripcion": "Contrato de software para prueba.",
                    "organismo": "Gobierno de Canarias",
                    "ubicacion": "Canarias",
                    "procedimiento": "Abierto",
                    "presupuesto": 50000,
                    "fecha_publicacion_oficial": "2026-03-24",
                    "fecha_limite": "2026-04-01",
                    "estado": "Abierta",
                    "fuente_oficial": "Gobierno de Canarias",
                    "url_fuente_oficial": "https://www.gobiernodecanarias.org/perfil_del_contratante/",
                    "cpvs": ["72250000"],
                    "actualizaciones_oficiales": [
                        {
                            "fecha_publicacion": "2026-03-25",
                            "tipo": "Rectificacion",
                            "estado": "anulada",
                            "resumen": "El expediente queda anulado.",
                        }
                    ],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            alerts_path = Path(tmp_dir) / "alerts.json"
            opportunities_path = Path(tmp_dir) / "opportunities.json"
            opportunities_path.write_text(json.dumps(opportunities_payload), encoding="utf-8")

            created_alert = create_alert(
                CatalogFilters(palabra_clave="software"),
                path=alerts_path,
                catalog_path=opportunities_path,
                now="2026-03-25T10:00:00Z",
            )

        self.assertEqual([], list(created_alert.coincidencias))
