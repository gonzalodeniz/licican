from __future__ import annotations

import unittest

from licican.shared.filters import CatalogFilters


class CatalogFiltersTests(unittest.TestCase):
    def test_normalized_cleans_optional_text_fields(self) -> None:
        filters = CatalogFilters(palabra_clave=" backup ", procedimiento=" Abierto ", ubicacion=" Canarias ")
        normalized = filters.normalized()
        self.assertEqual("backup", normalized.palabra_clave)
        self.assertEqual("Abierto", normalized.procedimiento)
        self.assertEqual("Canarias", normalized.ubicacion)

    def test_active_filters_omits_empty_values(self) -> None:
        filters = CatalogFilters(palabra_clave="backup", presupuesto_min=1000)
        self.assertEqual({"palabra_clave": "backup", "presupuesto_min": 1000}, filters.active_filters())

    def test_validation_error_detects_invalid_budget_range(self) -> None:
        filters = CatalogFilters(presupuesto_min=10, presupuesto_max=1)
        self.assertIn("presupuesto mínimo", filters.validation_error() or "")
