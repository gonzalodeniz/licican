from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric, render_table


def render_coverage(sources, summary: dict[str, int], base_path: str = "", access_context: AccessContext | None = None) -> str:
    """Renderiza la vista de cobertura inicial."""
    rows = [
        (
            "<tr>"
            f'<td data-label="Fuente oficial">{escape(source.nombre)}</td>'
            f'<td data-label="Categoría">{escape(source.categoria)}</td>'
            f'<td data-label="Estado">{escape(source.estado)}</td>'
            f'<td data-label="Alcance">{escape(source.alcance)}</td>'
            f'<td data-label="Justificación funcional">{escape(source.descripcion)}</td>'
            f'<td data-label="Trazabilidad">{escape(source.referencia_funcional)}</td>'
            "</tr>"
        )
        for source in sources
    ]
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            {render_metric(summary["MVP"], "Fuentes objetivo en MVP")}
            {render_metric(summary["Posterior"], "Fuentes planificadas después del MVP")}
            {render_metric(summary["Por definir"], "Fuentes pendientes de decisión")}
          </div>
          <p class="muted">Los datos se cargan desde una configuración versionada en <code>data/source_coverage.json</code>.</p>
        </div>
        {render_table(["Fuente oficial", "Categoría", "Estado", "Alcance", "Justificación funcional", "Trazabilidad"], rows)}
      </section>
      <p class="note">
        Referencia funcional alineada con <code>product-manager/refinamiento-funcional.md</code> y <code>product-manager/roadmap.md</code>.
        Esta cobertura sirve de base para el catálogo inicial del MVP sin inducir una expectativa de exhaustividad.
      </p>
    """
    return page_template(
        "Licican | Cobertura inicial del MVP",
        "Cobertura inicial de fuentes oficiales del MVP",
        "Release 0 · PB-007 · Cobertura visible y verificable",
        "Licican no comunica cobertura total del ecosistema canario en esta entrega. Esta vista delimita qué fuentes oficiales entran en el MVP, cuáles quedan para una fase posterior y cuáles siguen pendientes de decisión funcional.",
        content,
        current_path="/cobertura-fuentes",
        base_path=base_path,
        access_context=access_context,
    )
