from __future__ import annotations

import xml.etree.ElementTree as ET

from licican.shared.text import clean_text


def find_first(root: ET.Element, local_tag: str) -> ET.Element | None:
    """Devuelve el primer nodo hijo por nombre local."""
    for child in root:
        if local_name(child.tag) == local_tag:
            return child
    return None


def find_first_text(root: ET.Element, local_tag: str) -> str | None:
    """Devuelve el primer texto hijo por nombre local."""
    element = find_first(root, local_tag)
    if element is None:
        return None
    return clean_text(element.text)


def iter_local(root: ET.Element, local_tag: str) -> list[ET.Element]:
    """Itera nodos por nombre local."""
    return [element for element in root.iter() if local_name(element.tag) == local_tag]


def iter_texts(root: ET.Element, local_tag: str) -> list[str]:
    """Itera textos limpios por nombre local."""
    values: list[str] = []
    for element in root.iter():
        if local_name(element.tag) != local_tag:
            continue
        value = clean_text(element.text)
        if value is not None:
            values.append(value)
    return values


def find_text_by_path(root: ET.Element, path: tuple[str, ...]) -> str | None:
    """Busca un texto siguiendo una ruta de nombres locales."""
    current = root
    for item in path:
        current = find_first(current, item)
        if current is None:
            return None
    return clean_text(current.text)


def local_name(tag: str) -> str:
    """Extrae el nombre local de un tag XML con o sin namespace."""
    if "}" not in tag:
        return tag
    return tag.rsplit("}", 1)[-1]
