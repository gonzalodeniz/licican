from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.templates.base import page_template


def render_classification(reference: str, rules, audited_examples: list[dict[str, object]], base_path: str = "", access_context: AccessContext | None = None) -> str:
    """Renderiza la vista de clasificación TI."""
    example_rows = "\n".join(
        (
            "<tr>"
            f'<td data-label="Ejemplo">{escape(str(example["titulo"]))}</td>'
            f'<td data-label="Esperada">{escape(str(example["clasificacion_esperada"]))}</td>'
            f'<td data-label="Obtenida">{escape(str(example["clasificacion_obtenida"]))}</td>'
            f'<td data-label="Coincidencias">{escape(", ".join(example["coincidencias_inclusion"] + example["coincidencias_exclusion"] + example["coincidencias_frontera"]) or "Sin coincidencias")}</td>'
            f'<td data-label="Trazabilidad">{escape(str(example["motivo_ejemplo"]))}</td>'
            "</tr>"
        )
        for example in audited_examples
    )
    inclusion_badges = "".join(f'<span class="badge ok">{escape(term)}</span>' for term in rules.inclusion_palabras_clave)
    cpv_badges = "".join(f'<span class="badge ok">{escape(prefix)}</span>' for prefix in rules.inclusion_cpv_prefixes)
    exclusion_badges = "".join(f'<span class="badge risk">{escape(term)}</span>' for term in rules.exclusion_palabras_clave)
    frontier_badges = "".join(f'<span class="badge warn">{escape(term)}</span>' for term in rules.frontera_palabras_clave)
    content = f"""
      <section class="classification-view">
      <section class="panel" id="classification-rules-panel">
        <div class="panel-body">
          <h2>Reglas auditables aplicadas</h2>
          <div class="rule-grid">
            <article><h3>Inclusión por palabras clave</h3><div>{inclusion_badges}</div></article>
            <article><h3>Inclusión por prefijos CPV</h3><div>{cpv_badges}</div></article>
            <article><h3>Exclusiones funcionales</h3><div>{exclusion_badges}</div></article>
            <article><h3>Casos frontera</h3><div>{frontier_badges}</div></article>
          </div>
          <p class="muted">Referencia funcional: <code>{escape(reference)}</code></p>
        </div>
      </section>
      <section class="panel" id="classification-examples-panel">
        <div class="panel-body">
          <h2>Ejemplos auditados para QA</h2>
          <p>Esta superficie permite revisar inclusiones, exclusiones y <strong>casos frontera</strong> sin depender todavía del catálogo de <code>PB-001</code>. Los expedientes mixtos o de <strong>telecomunicaciones</strong> ambiguas quedan identificados como revisables.</p>
        </div>
        <div class="table-wrap classification-table-wrap">
          <table class="classification-table">
            <thead><tr><th>Ejemplo</th><th>Esperada</th><th>Obtenida</th><th>Coincidencias</th><th>Trazabilidad funcional</th></tr></thead>
            <tbody>{example_rows}</tbody>
          </table>
        </div>
      </section>
      </section>
    """
    return page_template(
        "Licican | Clasificación TI auditable",
        "Clasificación TI auditable",
        "Release 0 · PB-006 · Regla TI verificable",
        "Licican fija aquí la regla funcional mínima para decidir qué oportunidades son TI, cuáles deben excluirse y qué expedientes requieren revisión adicional antes de aparecer en el catálogo.",
        content,
        current_path="/clasificacion-ti",
        base_path=base_path,
        access_context=access_context,
    )
