from __future__ import annotations

from licican.access import AccessContext
from licican.web.templates.base import page_template


def render_dashboard(base_path: str = "", access_context: AccessContext | None = None) -> str:
    return page_template(
        document_title="Licican | Dashboard",
        page_heading="Dashboard",
        hero_label="Resumen general",
        hero_body="Vista de resumen de actividad y estado del sistema.",
        content="",
        current_path="/dashboard",
        base_path=base_path,
        access_context=access_context,
    )
