from __future__ import annotations

import unittest

from licican.shared.domain_constants import (
    CANARIAS_KEYWORDS,
    PROCEDURE_LABELS,
    STATUS_LABELS,
    TI_CPV_PREFIXES,
    map_procedure,
    map_status,
)


class DomainConstantsTests(unittest.TestCase):
    def test_shared_constants_keep_expected_catalog_values(self) -> None:
        self.assertIn("canarias", CANARIAS_KEYWORDS)
        self.assertEqual(("72", "48", "302"), TI_CPV_PREFIXES)
        self.assertEqual("Publicada", STATUS_LABELS["PUB"])
        self.assertEqual("Abierto", PROCEDURE_LABELS["1"])

    def test_map_status_returns_label_or_original_value(self) -> None:
        self.assertEqual("Adjudicada", map_status("ADJ"))
        self.assertEqual("XYZ", map_status("XYZ"))
        self.assertEqual("No informado", map_status(None))

    def test_map_procedure_returns_label_none_or_fallback(self) -> None:
        self.assertEqual("Abierto simplificado", map_procedure("9"))
        self.assertEqual("Procedimiento 42", map_procedure("42"))
        self.assertIsNone(map_procedure(" "))
