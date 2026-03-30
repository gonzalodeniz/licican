from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.source_coverage import load_source_coverage, summary_by_status


class SourceCoverageTests(unittest.TestCase):
    def test_load_source_coverage_returns_expected_sources(self) -> None:
        sources = load_source_coverage()

        self.assertEqual(6, len(sources))
        self.assertEqual("MVP", sources[0].estado)
        self.assertEqual("Gobierno de Canarias", sources[1].nombre)

    def test_summary_by_status_counts_all_declared_statuses(self) -> None:
        summary = summary_by_status(load_source_coverage())

        self.assertEqual({"MVP": 3, "Posterior": 2, "Por definir": 1}, summary)

    def test_load_source_coverage_rejects_unsupported_status(self) -> None:
        payload = {
            "sources": [
                {
                    "nombre": "Fuente inválida",
                    "categoria": "Prueba",
                    "estado": "Descartada",
                    "descripcion": "Dato inválido",
                    "alcance": "No aplica",
                    "referencia_funcional": "Test",
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Estados de cobertura no soportados"):
                load_source_coverage(path)
