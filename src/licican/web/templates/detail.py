from __future__ import annotations

from html import escape

from licican.access import AccessContext, has_capability
from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric, render_state_badge


def render_opportunity_detail(detail: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    """Renderiza la ficha de detalle de una oportunidad."""
    update = detail["actualizacion_oficial_mas_reciente"]
    update_panel = ""
    if update is not None:
        update_panel = f'<section class="note">La ficha refleja el ultimo dato oficial visible publicado el <strong>{escape(str(update["fecha_publicacion"]))}</strong> mediante <strong>{escape(str(update["tipo"]))}</strong>. {escape(str(update["resumen"]))}</section>'
    criteria_items = detail["criterios_adjudicacion"]
    criteria_html = "<ul>" + "".join(f"<li>{escape(str(item))}</li>" for item in criteria_items) + "</ul>" if criteria_items else "<p>No informado</p>"
    pipeline_form = ""
    if access_context is None or has_capability(access_context, "manage_pipeline"):
        pipeline_form = f"""
        <form method="post" action="{escape(build_url(base_path, '/pipeline'))}">
          <input type="hidden" name="opportunity_id" value="{escape(str(detail["id"]))}" />
          <button type="submit">Guardar en pipeline</button>
        </form>
        """
    content = f"""
      {update_panel}
      <section class="panel" id="detail-main-panel"><div class="panel-body">
        <p><a href="{escape(build_url(base_path, '/'))}">Volver al catalogo</a></p>
        {pipeline_form}
        <div class="summary">
          {render_metric(detail["estado"], "Estado oficial visible")}
          {render_metric(detail["fecha_limite"], "Fecha limite visible")}
          {render_metric(_format_budget(detail["presupuesto"]), "Presupuesto visible")}
        </div>
        <div class="table-wrap detail-table-wrap"><table class="detail-table"><tbody>
          <tr><th>Organismo convocante</th><td>{escape(str(detail["organismo"]))}</td></tr>
          <tr><th>Ubicacion</th><td>{escape(str(detail["ubicacion"]))}</td></tr>
          <tr><th>Procedimiento</th><td>{escape(str(detail["procedimiento"] or "No informado"))}</td></tr>
          <tr><th>Presupuesto</th><td>{escape(_format_budget(detail["presupuesto"]))}</td></tr>
          <tr><th>Publicación oficial</th><td>{escape(str(detail["fecha_publicacion_oficial"]))}</td></tr>
          <tr><th>Fecha limite</th><td>{escape(str(detail["fecha_limite"]))}</td></tr>
          <tr><th>Estado oficial del expediente</th><td>{render_state_badge(detail["estado"])}</td></tr>
          <tr><th>Fuente oficial</th><td><a class="source-link" href="{escape(str(detail["url_fuente_oficial"]))}" target="_blank" rel="noopener noreferrer">{escape(str(detail["fuente_oficial"]))}</a></td></tr>
          <tr><th>Fichero .atom origen</th><td>{escape(str(detail["fichero_origen_atom"] or "No informado"))}</td></tr>
        </tbody></table></div>
      </div></section>
      <section class="panel" id="detail-context-panel"><div class="panel-body"><h2>Contexto resumido</h2><p>{escape(str(detail["descripcion"]))}</p></div></section>
      <section class="panel" id="detail-solvency-panel"><div class="panel-body"><h2>Solvencia tecnica</h2><p>{escape(str(detail["solvencia_tecnica"] or "No informado"))}</p></div></section>
      <section class="panel" id="detail-criteria-panel"><div class="panel-body"><h2>Criterios de adjudicacion</h2>{criteria_html}</div></section>
    """
    return page_template("Licican | Ficha de detalle de licitacion", str(detail["titulo"]), "Release 1 · PB-002 · Ficha resumida verificable", "La ficha resume los datos criticos del expediente y mantiene visible la fuente oficial, la fecha de publicación y el estado oficial. Cuando existe una rectificacion o modificacion publicada por el origen, se muestra el ultimo dato oficial visible.", content, current_path=f"/oportunidades/{escape(str(detail['id']))}", base_path=base_path, access_context=access_context)


def _display_value(value: object | None) -> str:
    if value in (None, ""):
        return "No informado"
    return str(value)


def _format_budget(amount: object | None) -> str:
    if amount is None:
        return "Presupuesto no informado"
    formatted = f"{int(amount):,.0f}".replace(",", ".")
    return f"{formatted} EUR"
