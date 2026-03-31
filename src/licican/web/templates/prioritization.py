from __future__ import annotations

from html import escape

from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric, render_table


def render_prioritization(reference: str, sources, out_of_scope: tuple[str, ...], summary: dict[str, int], base_path: str = "") -> str:
    """Renderiza la priorización de fuentes reales."""
    rows = [
        (
            "<tr>"
            f'<td data-label="Ola">{escape(source.ola)}</td>'
            f'<td data-label="Fuente real oficial"><a href="{escape(source.url_oficial)}">{escape(source.nombre)}</a></td>'
            f'<td data-label="Categoría">{escape(source.categoria)}</td>'
            f'<td data-label="Alcance">{escape(source.alcance)}</td>'
            f'<td data-label="Justificación">{escape(source.justificacion)}</td>'
            f'<td data-label="Trazabilidad">{escape(source.trazabilidad)}</td>'
            "</tr>"
        )
        for source in sources
    ]
    out_of_scope_html = "".join(f"<li>{escape(item)}</li>" for item in out_of_scope)
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            {render_metric(summary["Ola 1"], "Fuentes en Ola 1")}
            {render_metric(summary["Ola 2"], "Fuentes en Ola 2")}
            {render_metric(summary["Ola 3"], "Fuentes en Ola 3")}
          </div>
          <p class="muted">Esta priorización reutiliza la cobertura visible de <code>PB-007</code> y la clasificación auditable de <code>PB-006</code> para reforzar la recopilación con fuentes reales oficiales antes de abrir alertas o pipeline.</p>
        </div>
        {render_table(["Ola", "Fuente real oficial", "Categoría", "Alcance", "Justificación", "Trazabilidad"], rows)}
      </section>
      <section class="note">
        <strong>Fuera de alcance en esta iteración</strong>
        <ul>{out_of_scope_html}</ul>
      </section>
      <p class="note">
        Referencia funcional activa: <code>{escape(reference)}</code>.
        La lista priorizada nombra de forma explícita <code>BOC</code>, <code>BOP Las Palmas</code> y <code>BOE</code> con orden por olas verificable por <code>qa-teams</code>.
      </p>
    """
    return page_template(
        "Licican | Priorización de fuentes reales oficiales",
        "Priorización de fuentes reales oficiales para recopilación",
        "Release 2 · PB-009 · Recopilación priorizada por olas",
        "Licican deja aquí visible qué fuentes oficiales reales deben entrar antes en la recopilación temprana. La entrega refuerza credibilidad y trazabilidad sin ampliar todavía cobertura comercial, alertas ni pipeline.",
        content,
        current_path="/priorizacion-fuentes-reales",
        base_path=base_path,
    )
