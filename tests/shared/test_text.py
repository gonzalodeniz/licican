from __future__ import annotations

import unittest

from licican.shared.text import clean_text, normalize_optional, normalize_text, slugify


class TextHelpersTests(unittest.TestCase):
    def test_normalize_text_removes_accents_and_lowercases(self) -> None:
        self.assertEqual("organo de contratacion", normalize_text("Órgano de Contratación"))

    def test_normalize_text_strips_outer_whitespace(self) -> None:
        self.assertEqual("canarias", normalize_text("  Canarias  "))

    def test_normalize_text_preserves_inner_spacing(self) -> None:
        self.assertEqual("gran   canaria", normalize_text("Gran   Canaria"))

    def test_slugify_builds_hyphenated_ascii_slug(self) -> None:
        self.assertEqual("expediente-2026-lote-1", slugify("Expediente 2026 / Lote 1"))

    def test_slugify_collapses_non_alphanumeric_segments(self) -> None:
        self.assertEqual("santa-cruz-de-tenerife", slugify("Santa Cruz... de Tenerife"))

    def test_slugify_returns_default_for_empty_input(self) -> None:
        self.assertEqual("expediente-sin-id", slugify("   "))

    def test_clean_text_collapses_internal_whitespace(self) -> None:
        self.assertEqual("uno dos tres", clean_text(" uno \n dos\t tres "))

    def test_clean_text_returns_none_for_blank_input(self) -> None:
        self.assertIsNone(clean_text("   "))

    def test_clean_text_keeps_none(self) -> None:
        self.assertIsNone(clean_text(None))

    def test_normalize_optional_normalizes_non_empty_values(self) -> None:
        self.assertEqual("santa cruz", normalize_optional("  Santa CRUZ "))

    def test_normalize_optional_collapses_whitespace_before_normalizing(self) -> None:
        self.assertEqual("organo de contratacion", normalize_optional("Órgano   de contratación"))

    def test_normalize_optional_returns_none_for_blank_or_none(self) -> None:
        self.assertIsNone(normalize_optional(" \n "))
        self.assertIsNone(normalize_optional(None))
