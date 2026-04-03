from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.catalog import _format_budget
from licican.web.templates.components import render_metric, render_status_note


def render_pipeline(
    payload: dict[str, object],
    base_path: str = "",
    error_message: str | None = None,
    status_message: str | None = None,
    access_context: AccessContext | None = None,
) -> str:
    entries = list(payload["pipeline"])
    summary = payload["summary"]
    states = list(payload["estados_disponibles"])

    if entries:
        sections = [
            _render_pipeline_entry(base_path, entry, states)
            for entry in entries
        ]
        entries_html = "".join(sections)
    else:
        entries_html = '<section class="note">Todavía no hay oportunidades guardadas en el pipeline.</section>'

    scope_note = "Visibilidad global de seguimiento." if access_context is not None and access_context.is_admin else "Visibilidad limitada al contexto funcional activo."
    content = f"""
      {render_status_note(status_message)}
      {render_status_note(error_message, "warn")}
      <section class="pipeline-view">
      <section class="panel" id="pipeline-summary-panel">
        <div class="panel-body">
          <div class="summary">
            {render_metric(summary["total_oportunidades"], "Oportunidades guardadas")}
            {render_metric(summary["con_advertencia_oficial"], "Expedientes con advertencia oficial")}
            {render_metric(summary["estado_nueva"], "En estado Nueva")}
          </div>
          <p class="muted">El pipeline mantiene una única entrada por oportunidad y usuario, conserva el seguimiento aunque el estado oficial del expediente cambie y permite mover cada registro por los estados operativos definidos en <code>PB-005</code>.</p>
          <p class="muted">{escape(scope_note)}</p>
        </div>
      </section>
      {entries_html}
      <p class="note">Referencia funcional activa: <code>{escape(str(payload["referencia_funcional"]))}</code>. Estados de seguimiento disponibles: <code>{escape(", ".join(states))}</code>.</p>
      </section>
    """
    return page_template(
        "Licican | Pipeline de seguimiento",
        "Pipeline de seguimiento de oportunidades",
        "PB-005 · Seguimiento operativo persistido",
        "La vista permite guardar oportunidades visibles del catálogo, revisar su contexto oficial y mover cada expediente por un estado de trabajo sin perder trazabilidad cuando la licitación cambia.",
        content,
        current_path="/pipeline",
        base_path=base_path,
        access_context=access_context,
    )


def _render_pipeline_entry(base_path: str, entry: dict[str, object], states: list[str]) -> str:
    opportunity = dict(entry["oportunidad"])
    warning = entry["advertencia_oficial"]
    opportunity_id = str(entry["opportunity_id"])
    detail_url = build_url(base_path, f"/oportunidades/{opportunity_id}")
    update_url = build_url(base_path, f"/pipeline/{opportunity_id}/estado")
    options = "".join(
        f'<option value="{escape(state)}"{" selected" if entry["estado_seguimiento"] == state else ""}>{escape(state)}</option>'
        for state in states
    )
    warning_html = ""
    if warning is not None:
        warning_html = f'<section class="note note-warning"><strong>Advertencia oficial</strong><br />{escape(str(warning))}</section>'

    return f"""
      <section class="panel pipeline-entry-panel" id="pipeline-entry-{escape(opportunity_id)}">
        <div class="panel-body">
          <p><strong>{escape(str(opportunity["titulo"]))}</strong></p>
          <div class="summary">
            {render_metric(entry["estado_seguimiento"], "Estado de seguimiento")}
            {render_metric(opportunity["estado_oficial"], "Estado oficial visible")}
            {render_metric(opportunity["fecha_limite"], "Fecha limite visible")}
          </div>
          {warning_html}
          <div class="table-wrap pipeline-table-wrap">
            <table class="pipeline-table">
              <tbody>
                <tr><th>Organismo</th><td>{escape(str(opportunity["organismo"]))}</td></tr>
                <tr><th>Ubicacion</th><td>{escape(str(opportunity["ubicacion"]))}</td></tr>
                <tr><th>Procedimiento</th><td>{escape(str(opportunity["procedimiento"] or "No informado"))}</td></tr>
                <tr><th>Presupuesto</th><td>{escape(_format_budget(opportunity["presupuesto"]))}</td></tr>
                <tr><th>Publicacion oficial</th><td>{escape(str(opportunity["fecha_publicacion_oficial"]))}</td></tr>
                <tr><th>Creada en pipeline</th><td>{escape(str(entry["creada_en"]))}</td></tr>
                <tr><th>Ultima actualizacion</th><td>{escape(str(entry["actualizada_en"]))}</td></tr>
              </tbody>
            </table>
          </div>
          <div class="filter-actions">
            <a class="button-link" href="{escape(detail_url)}">Ver detalle</a>
            <a class="button-link" href="{escape(str(opportunity["url_fuente_oficial"]))}" target="_blank" rel="noopener noreferrer">Fuente oficial</a>
          </div>
          <form method="post" action="{escape(update_url)}">
            <div class="filters">
              <div>
                <label for="estado-{escape(opportunity_id)}">Estado de seguimiento</label>
                <select id="estado-{escape(opportunity_id)}" name="estado_seguimiento">{options}</select>
              </div>
            </div>
            <div class="filter-actions">
              <button type="submit">Actualizar estado</button>
            </div>
          </form>
        </div>
      </section>
    """
