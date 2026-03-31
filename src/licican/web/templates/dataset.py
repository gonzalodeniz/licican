from __future__ import annotations

from html import escape

from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric, render_tab_nav, render_table


def render_datos_consolidados(
    dataset: dict[str, object],
    selected_view: str,
    heading: str,
    description: str,
    columns: list[tuple[str, str]],
    actions: list[str] | None,
    rows: list[dict[str, object]],
    base_path: str = "",
) -> str:
    """Renderiza la vista de datos consolidados."""
    headers = [label for _, label in columns] + (["Detalle"] if actions is not None else [])
    body_rows: list[str] = []
    for index, row in enumerate(rows):
        cells = "".join(
            f'<td data-label="{escape(label)}">{escape(_display_value(row.get(key)))}</td>'
            for key, label in columns
        )
        if actions is not None:
            cells += f'<td data-label="Detalle">{actions[index]}</td>'
        body_rows.append(f"<tr>{cells}</tr>")
    tabs = render_tab_nav(
        base_path,
        selected_view,
        [("licitaciones", "Licitaciones TI Canarias"), ("lotes", "Detalle Lotes"), ("adjudicaciones", "Adjudicaciones")],
    )
    summary = dataset["resumen"]
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            {render_metric(summary["licitaciones"], "Licitaciones en la muestra")}
            {render_metric(summary["lotes"], "Lotes visibles")}
            {render_metric(summary["adjudicaciones"], "Adjudicaciones visibles")}
          </div>
          <p class="muted">La fuente visible de esta entrega es <code>{escape(str(dataset["archivo_origen"]))}</code>, alineada con <code>{escape(str(dataset["referencia_funcional"]))}</code>.</p>
          {tabs}
          <p>{description}</p>
        </div>
        {render_table(headers, body_rows, "No hay filas disponibles en la hoja seleccionada para la muestra actual del Excel.")}
      </section>
    """
    return page_template(
        "Licican | Datos consolidados TI Canarias",
        heading,
        "Release 7 · PB-012 · Excel funcional visible en la aplicación",
        "Licican expone aquí la misma estructura funcional que el Excel versionado de licitaciones TI Canarias, con pestañas separadas para licitaciones, lotes y adjudicaciones.",
        content,
        current_path="/datos-consolidados",
        base_path=base_path,
    )


def _display_value(value: object | None) -> str:
    if value in (None, ""):
        return "No informado"
    return str(value)
