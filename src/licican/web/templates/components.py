from __future__ import annotations

from html import escape

from licican.web.responses import build_url


def render_table(headers: list[str], rows: list[str], empty_message: str | None = None) -> str:
    """Renderiza una tabla HTML simple."""
    if not rows and empty_message is not None:
        return f'<section class="note">{escape(empty_message)}</section>'
    header_html = "".join(f"<th>{escape(label)}</th>" for label in headers)
    return f"""
      <div class="table-wrap">
        <table>
          <thead><tr>{header_html}</tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    """


def render_badges(items: list[tuple[str, str]] | dict[str, object], tone: str = "") -> str:
    """Renderiza badges de texto."""
    if isinstance(items, dict):
        pairs = [(key, str(value)) for key, value in items.items()]
    else:
        pairs = items
    class_name = f"badge {tone}".strip()
    return "".join(f'<span class="{class_name}">{escape(label)}: {escape(value)}</span>' for label, value in pairs)


def render_metric(value: object, label: str) -> str:
    """Renderiza un bloque métrico."""
    return f'<article class="metric"><strong>{escape(str(value))}</strong>{escape(label)}</article>'


def render_status_note(message: str | None, tone: str = "ok") -> str:
    """Renderiza una nota de estado."""
    if message is None:
        return ""
    class_name = "note" if tone == "ok" else "note note-warning"
    return f'<section class="{class_name}">{escape(message)}</section>'


def render_tab_nav(base_path: str, current_view: str, tabs: list[tuple[str, str]]) -> str:
    """Renderiza una navegación por pestañas."""
    links = []
    for view, label in tabs:
        class_name = "tab-link active" if current_view == view else "tab-link"
        href = build_url(base_path, f"/datos-consolidados?vista={view}")
        links.append(f'<a class="{class_name}" href="{escape(href)}">{escape(label)}</a>')
    return f'<nav class="tab-nav" aria-label="Pestañas de datos consolidados">{"".join(links)}</nav>'
