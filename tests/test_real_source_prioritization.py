from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.real_source_prioritization import (
    load_real_source_prioritization,
    summarize_prioritization,
)


class RealSourcePrioritizationTests(unittest.TestCase):
    def test_load_real_source_prioritization_returns_sources_in_priority_order(self) -> None:
        reference, sources, out_of_scope = load_real_source_prioritization()

        self.assertIn("PB-009", reference)
        self.assertEqual(["BOC", "BOP Las Palmas", "BOE"], [source.nombre for source in sources])
        self.assertEqual(("Alertas tempranas", "Pipeline de seguimiento", "Ampliacion de cobertura a nuevas administraciones no confirmadas"), out_of_scope)

    def test_summarize_prioritization_counts_all_declared_waves(self) -> None:
        _, sources, _ = load_real_source_prioritization()

        self.assertEqual({"Ola 1": 1, "Ola 2": 1, "Ola 3": 1}, summarize_prioritization(sources))

    def test_load_real_source_prioritization_rejects_unsupported_waves(self) -> None:
        payload = {
            "referencia_funcional": "PB-009",
            "sources": [
                {
                    "nombre": "Fuente inválida",
                    "ola": "Ola 9",
                    "url_oficial": "https://example.com",
                    "categoria": "Prueba",
                    "prioridad": 9,
                    "alcance": "No aplica",
                    "justificacion": "Dato inválido",
                    "trazabilidad": "Test",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Olas de priorizacion no soportadas"):
                load_real_source_prioritization(path)
