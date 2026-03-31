from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from licican.shared.xml_helpers import find_first, find_first_text, find_text_by_path, iter_local, iter_texts, local_name


class XmlHelpersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ET.fromstring(
            """
            <root xmlns:a="urn:test">
              <a:item>
                <a:name>  Uno  </a:name>
                <a:group>
                  <a:name>Dos</a:name>
                </a:group>
              </a:item>
            </root>
            """
        )

    def test_find_first_and_find_first_text_use_local_names(self) -> None:
        item = find_first(self.root, "item")
        self.assertIsNotNone(item)
        self.assertEqual("Uno", find_first_text(item, "name"))

    def test_iter_helpers_collect_nodes_and_texts(self) -> None:
        item = find_first(self.root, "item")
        self.assertEqual(2, len(iter_local(item, "name")))
        self.assertEqual(["Uno", "Dos"], iter_texts(item, "name"))

    def test_find_text_by_path_and_local_name_of(self) -> None:
        item = find_first(self.root, "item")
        self.assertEqual("Dos", find_text_by_path(item, ("group", "name")))
        self.assertEqual("name", local_name("{urn:test}name"))
