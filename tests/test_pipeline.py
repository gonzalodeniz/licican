from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.pipeline import (
    add_opportunity_to_pipeline,
    build_pipeline_payload,
    load_pipeline,
    update_pipeline_entry_status,
)


class PipelineTests(unittest.TestCase):
    def test_add_opportunity_creates_single_entry_with_initial_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"

            created_entry, created = add_opportunity_to_pipeline(
                "govcan-backup-cloud-2026",
                path=pipeline_path,
                catalog_path=Path("data"),
                now="2026-03-31T10:00:00Z",
            )
            reference, entries = load_pipeline(pipeline_path)

        self.assertTrue(created)
        self.assertIn("PB-005", reference)
        self.assertEqual("Nueva", created_entry.estado_seguimiento)
        self.assertEqual(1, len(entries))
        self.assertEqual("govcan-backup-cloud-2026", entries[0].opportunity_id)

    def test_add_opportunity_avoids_duplicates_for_same_user(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            add_opportunity_to_pipeline(
                "govcan-backup-cloud-2026",
                path=pipeline_path,
                catalog_path=Path("data"),
                now="2026-03-31T10:00:00Z",
            )

            duplicated_entry, created = add_opportunity_to_pipeline(
                "govcan-backup-cloud-2026",
                path=pipeline_path,
                catalog_path=Path("data"),
                now="2026-03-31T10:05:00Z",
            )
            _, entries = load_pipeline(pipeline_path)

        self.assertFalse(created)
        self.assertEqual("govcan-backup-cloud-2026", duplicated_entry.opportunity_id)
        self.assertEqual(1, len(entries))

    def test_update_pipeline_status_persists_new_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            add_opportunity_to_pipeline(
                "pcsp-cabildo-licencias-2026",
                path=pipeline_path,
                catalog_path=Path("data"),
                now="2026-03-31T10:00:00Z",
            )

            updated_entry = update_pipeline_entry_status(
                "pcsp-cabildo-licencias-2026",
                "Preparando oferta",
                path=pipeline_path,
                now="2026-03-31T11:00:00Z",
            )

        self.assertEqual("Preparando oferta", updated_entry.estado_seguimiento)
        self.assertEqual("2026-03-31T11:00:00Z", updated_entry.actualizada_en)

    def test_build_pipeline_payload_warns_when_official_state_is_non_actionable(self) -> None:
        opportunities_payload = {
            "referencia_funcional": "PB-001",
            "opportunities": [
                {
                    "id": "licitacion-desierta",
                    "titulo": "Servicio TI desierto",
                    "descripcion": "Contrato TI que queda desierto.",
                    "organismo": "Gobierno de Canarias",
                    "ubicacion": "Canarias",
                    "procedimiento": "Abierto",
                    "presupuesto": 45000,
                    "fecha_publicacion_oficial": "2026-03-20",
                    "fecha_limite": "2026-04-01",
                    "estado": "Abierta",
                    "fuente_oficial": "Gobierno de Canarias",
                    "url_fuente_oficial": "https://www.gobiernodecanarias.org/perfil_del_contratante/",
                    "cpvs": ["72250000"],
                    "actualizaciones_oficiales": [
                        {
                            "fecha_publicacion": "2026-03-25",
                            "tipo": "Rectificacion",
                            "resumen": "El expediente queda desierto.",
                            "estado": "desierta",
                        }
                    ],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            opportunities_path = Path(tmp_dir) / "opportunities.json"
            opportunities_path.write_text(json.dumps(opportunities_payload), encoding="utf-8")
            add_opportunity_to_pipeline(
                "licitacion-desierta",
                path=pipeline_path,
                catalog_path=opportunities_path,
                now="2026-03-31T10:00:00Z",
            )

            payload = build_pipeline_payload(path=pipeline_path, catalog_path=opportunities_path)

        self.assertEqual(1, payload["summary"]["con_advertencia_oficial"])
        self.assertEqual("desierta", payload["pipeline"][0]["oportunidad"]["estado_oficial"])
        self.assertIn("Se mantiene en el pipeline", payload["pipeline"][0]["advertencia_oficial"])
