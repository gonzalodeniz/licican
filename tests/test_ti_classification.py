from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.ti_classification import (
    OpportunityCandidate,
    audit_examples,
    classify_opportunity,
    load_rule_set,
)


class TIClassificationTests(unittest.TestCase):
    def test_load_rule_set_returns_auditable_examples(self) -> None:
        rules = load_rule_set()

        self.assertIn("PB-006", rules.referencia_funcional)
        self.assertGreaterEqual(len(rules.inclusion_palabras_clave), 5)
        self.assertEqual(5, len(rules.ejemplos))

    def test_classify_opportunity_marks_clear_ti_candidate(self) -> None:
        rules = load_rule_set()
        decision = classify_opportunity(
            OpportunityCandidate(
                titulo="Servicio cloud para copias de seguridad",
                descripcion="Incluye software de respaldo y ciberseguridad gestionada.",
                cpvs=("72222300",),
            ),
            rules,
        )

        self.assertEqual("TI", decision.clasificacion)
        self.assertIn("cloud", decision.coincidencias_inclusion)
        self.assertIn("722", decision.coincidencias_inclusion)

    def test_classify_opportunity_marks_non_ti_candidate(self) -> None:
        rules = load_rule_set()
        decision = classify_opportunity(
            OpportunityCandidate(
                titulo="Suministro de mobiliario escolar",
                descripcion="Compra de mesas y sillas para centro educativo.",
                cpvs=("39160000",),
            ),
            rules,
        )

        self.assertEqual("No TI", decision.clasificacion)
        self.assertIn("mobiliario", decision.coincidencias_exclusion)

    def test_classify_opportunity_marks_frontier_case(self) -> None:
        rules = load_rule_set()
        decision = classify_opportunity(
            OpportunityCandidate(
                titulo="Proyecto de transformacion digital y telecomunicaciones del ayuntamiento",
                descripcion="Expediente mixto con conectividad y una parte menor de sistemas.",
                cpvs=("64200000", "72222300"),
            ),
            rules,
        )

        self.assertEqual("Caso frontera", decision.clasificacion)
        self.assertIn("telecomunicaciones", decision.coincidencias_frontera)

    def test_audit_examples_matches_expected_classifications(self) -> None:
        rules = load_rule_set()
        audited_examples = audit_examples(rules)

        self.assertTrue(all(item["coincide_con_esperado"] for item in audited_examples))

    def test_load_rule_set_rejects_invalid_expected_classification(self) -> None:
        payload = {
            "referencia_funcional": "PB-006",
            "inclusion": {
                "palabras_clave": ["software"],
                "cpv_prefixes": ["722"],
                "necesidades_explicitas": ["digitalizacion"]
            },
            "exclusion": {"palabras_clave": ["mobiliario"]},
            "casos_frontera": {"palabras_clave": ["telecomunicaciones"]},
            "ejemplos": [
                {
                    "id": "invalido",
                    "titulo": "Ejemplo",
                    "descripcion": "Ejemplo",
                    "cpvs": ["72222300"],
                    "clasificacion_esperada": "Dudoso",
                    "motivo": "No soportado"
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Clasificaciones TI no soportadas"):
                load_rule_set(path)
