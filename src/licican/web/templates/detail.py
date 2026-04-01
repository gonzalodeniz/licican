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
      <section class="panel"><div class="panel-body">
        <p><a href="{escape(build_url(base_path, '/'))}">Volver al catalogo</a></p>
        {pipeline_form}
        <div class="summary">
          {render_metric(detail["estado"], "Estado oficial visible")}
          {render_metric(detail["fecha_limite"], "Fecha limite visible")}
          {render_metric(_format_budget(detail["presupuesto"]), "Presupuesto visible")}
        </div>
        <div class="table-wrap"><table><tbody>
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
      <section class="panel"><div class="panel-body"><h2>Contexto resumido</h2><p>{escape(str(detail["descripcion"]))}</p></div></section>
      <section class="panel"><div class="panel-body"><h2>Solvencia tecnica</h2><p>{escape(str(detail["solvencia_tecnica"] or "No informado"))}</p></div></section>
      <section class="panel"><div class="panel-body"><h2>Criterios de adjudicacion</h2>{criteria_html}</div></section>
    """
    return page_template("Licican | Ficha de detalle de licitacion", str(detail["titulo"]), "Release 1 · PB-002 · Ficha resumida verificable", "La ficha resume los datos criticos del expediente y mantiene visible la fuente oficial, la fecha de publicación y el estado oficial. Cuando existe una rectificacion o modificacion publicada por el origen, se muestra el ultimo dato oficial visible.", content, current_path=f"/oportunidades/{escape(str(detail['id']))}", base_path=base_path, access_context=access_context)


def render_licitacion_detail(detail: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    """Renderiza el detalle de una licitación del Excel."""
    rows = [
        ("ID Expediente", detail["id_expediente"]),
        ("Estado", detail["estado"]),
        ("Órgano Contratación", detail["organo_contratacion"]),
        ("Importe estimado", detail["importe_estimado"]),
        ("Importe con IVA", detail["importe_con_iva"]),
        ("Importe sin IVA", detail["importe_sin_iva"]),
        ("CPVs Informáticos", detail["cpvs_informaticos"]),
        ("Ubicación", detail["ubicacion"]),
        ("Procedimiento", detail["procedimiento"]),
        ("Plazo Presentación", detail["plazo_presentacion"]),
        ("Nº Lotes", detail["numero_lotes"]),
        ("Nº Adjudicaciones", detail["numero_adjudicaciones"]),
        ("Fecha Actualización", detail["fecha_actualizacion"]),
        ("Fichero .atom origen", detail["fichero_origen_atom"]),
    ]
    table_rows = "".join(
        f"<tr><th>{escape(label)}</th><td>{render_state_badge(value) if label == 'Estado' else escape(_display_value(value))}</td></tr>"
        for label, value in rows
    )
    extra_link = f'<p><a class="offer-action" href="{escape(str(detail["enlace_placsp"]))}" target="_blank" rel="noopener noreferrer">Abrir expediente en PLACSP</a></p>' if detail["enlace_placsp"] else ""
    content = f'<section class="panel"><div class="panel-body"><p><a href="{escape(build_url(base_path, "/datos-consolidados?vista=licitaciones"))}">Volver a Licitaciones TI Canarias</a></p><div class="table-wrap"><table><tbody>{table_rows}</tbody></table></div>{extra_link}</div></section>'
    return page_template("Licican | Detalle de licitación consolidada", str(detail["titulo"]), "PB-012 · Detalle trazable del expediente", "La ficha mantiene visible la correspondencia funcional con el Excel de referencia y deja explícito el fichero `.atom` que alimenta la versión consolidada mostrada al usuario.", content, current_path="/datos-consolidados", base_path=base_path, access_context=access_context)


def render_adjudicacion_detail(detail: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    """Renderiza el detalle de una adjudicación del Excel."""
    rows = [
        ("ID Expediente", detail["id_expediente"]),
        ("Resultado", detail["resultado"]),
        ("Fecha Adjudicación", detail["fecha_adjudicacion"]),
        ("Lote", detail["lote"]),
        ("Ganador", detail["ganador"]),
        ("NIF Ganador", detail["nif_ganador"]),
        ("Ciudad Ganador", detail["ciudad_ganador"]),
        ("País", detail["pais"]),
        ("Importe Adj. sin IVA", detail["importe_adjudicacion_sin_iva"]),
        ("Importe Adj. Total", detail["importe_adjudicacion_total"]),
        ("Ofertas Recibidas", detail["ofertas_recibidas"]),
        ("Ofertas PYME", detail["ofertas_pyme"]),
        ("PYME Adjudicatario", detail["pyme_adjudicatario"]),
        ("ID Contrato", detail["id_contrato"]),
        ("Fecha Contrato", detail["fecha_contrato"]),
        ("Fichero .atom origen", detail["fichero_origen_atom"]),
    ]
    table_rows = "".join(f"<tr><th>{escape(label)}</th><td>{escape(_display_value(value))}</td></tr>" for label, value in rows)
    licitacion_link = ""
    if detail["licitacion_slug"] is not None:
        licitacion_link = f'<p><a class="offer-action" href="{escape(build_url(base_path, f"/datos-consolidados/licitaciones/{detail["licitacion_slug"]}"))}">Ver licitación asociada</a></p>'
    content = f'<section class="panel"><div class="panel-body"><p><a href="{escape(build_url(base_path, "/datos-consolidados?vista=adjudicaciones"))}">Volver a Adjudicaciones</a></p><p>{escape(_display_value(detail["descripcion"]))}</p><div class="table-wrap"><table><tbody>{table_rows}</tbody></table></div>{licitacion_link}</div></section>'
    return page_template("Licican | Detalle de adjudicación consolidada", str(detail["titulo"]), "PB-012 · Contrato adjudicado con trazabilidad", "Esta ficha deja visible el resultado contractual de la muestra actual y, cuando existe correspondencia con la licitación, hereda la trazabilidad del fichero `.atom` origen.", content, current_path="/datos-consolidados", base_path=base_path, access_context=access_context)


def _display_value(value: object | None) -> str:
    if value in (None, ""):
        return "No informado"
    return str(value)


def _format_budget(amount: object | None) -> str:
    if amount is None:
        return "Presupuesto no informado"
    formatted = f"{int(amount):,.0f}".replace(",", ".")
    return f"{formatted} EUR"
