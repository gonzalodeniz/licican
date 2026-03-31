from __future__ import annotations

from html import escape
from urllib.parse import urlencode

from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import render_badges, render_metric, render_status_note


def render_filter_form(base_path: str, active_filters: dict[str, object], available_filters: dict[str, list[str]], validation_error: str | None, pagination: dict[str, object]) -> str:
    """Renderiza el formulario de filtros del catálogo."""
    return f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Filtros funcionales</h2>
          <form method="get" action="{escape(build_url(base_path, '/'))}">
            <div class="filters">
              <div><label for="palabra_clave">Palabra clave</label><input id="palabra_clave" name="palabra_clave" type="text" value="{escape(str(active_filters.get('palabra_clave', '')))}" placeholder="backup, licencias, redes..." /></div>
              <div><label for="presupuesto_min">Presupuesto mínimo</label><input id="presupuesto_min" name="presupuesto_min" type="number" min="0" step="1" value="{escape(str(active_filters.get('presupuesto_min', '')))}" /></div>
              <div><label for="presupuesto_max">Presupuesto máximo</label><input id="presupuesto_max" name="presupuesto_max" type="number" min="0" step="1" value="{escape(str(active_filters.get('presupuesto_max', '')))}" /></div>
              <div><label for="procedimiento">Procedimiento</label><select id="procedimiento" name="procedimiento"><option value="">Todos</option>{"".join(f'<option value=\"{escape(item)}\"' + (' selected' if active_filters.get('procedimiento') == item else '') + f'>{escape(item)}</option>' for item in available_filters["procedimientos"])}</select></div>
              <div><label for="ubicacion">Ubicación</label><select id="ubicacion" name="ubicacion"><option value="">Todas</option>{"".join(f'<option value=\"{escape(item)}\"' + (' selected' if active_filters.get('ubicacion') == item else '') + f'>{escape(item)}</option>' for item in available_filters["ubicaciones"])}</select></div>
            </div>
            <div class="filter-actions"><button type="submit">Aplicar filtros</button><a class="button-link" href="{escape(build_url(base_path, '/'))}">Limpiar filtros</a></div>
          </form>
          {_active_filter_badges(active_filters)}
          {render_status_note(_validation_note(validation_error), "warn")}
          {render_status_note(_pagination_adjustment_message(pagination), "warn")}
        </div>
      </section>
    """


def render_pagination(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    """Renderiza los controles de paginación."""
    if int(pagination["total_paginas"]) <= 1:
        return ""
    prev_link = ""
    if pagination["pagina_anterior"] is not None:
        prev_link = f'<a class="button-link" href="{escape(_catalog_page_url(base_path, filters, int(pagination["pagina_anterior"])))}">Pagina anterior</a>'
    next_link = ""
    if pagination["pagina_siguiente"] is not None:
        next_link = f'<a class="button-link" href="{escape(_catalog_page_url(base_path, filters, int(pagination["pagina_siguiente"])))}">Pagina siguiente</a>'
    hidden_fields = "".join(f'<input type="hidden" name="{escape(str(key))}" value="{escape(str(value))}" />' for key, value in filters.items() if value not in (None, ""))
    jump = f'<form class="pagination-jump" method="get" action="{escape(build_url(base_path, "/"))}">{hidden_fields}<label for="catalog-page">Ir a la pagina</label><input id="catalog-page" name="page" type="number" min="1" max="{pagination["total_paginas"]}" value="{pagination["pagina_actual"]}" /><button type="submit">Ir</button></form>'
    return f'<div class="pagination-bar"><div class="pagination-status"><strong>Pagina {pagination["pagina_actual"]} de {pagination["total_paginas"]}</strong><span class="muted">Mostrando {pagination["resultado_desde"]}-{pagination["resultado_hasta"]} de {pagination["total_resultados"]}</span></div><div class="pagination-actions">{prev_link}{next_link}</div>{jump}</div>'


def render_catalog(catalog: dict[str, object], base_path: str = "") -> str:
    """Renderiza la vista completa del catálogo."""
    opportunities = catalog["oportunidades"]
    active_filters = catalog["filtros_activos"]
    available_filters = catalog["filtros_disponibles"]
    validation_error = catalog.get("error_validacion")
    pagination = catalog["paginacion"]
    uses_atom_consolidation = catalog["referencia_funcional"] == "PB-011"
    coverage_label = "Snapshots .atom consolidados" if uses_atom_consolidation else "Fuentes oficiales MVP aplicadas"
    coverage_note = "El catálogo consolida todos los snapshots `.atom` versionados presentes en `data/`, aplica el criterio conjunto Canarias + CPV TI de <code>PB-011</code> y conserva trazabilidad al fichero origen vigente." if uses_atom_consolidation else "El catálogo reutiliza la cobertura MVP de <code>PB-007</code>, la clasificación auditable de <code>PB-006</code> y la prioridad de fuentes reales oficiales de <code>PB-009</code>. No representa todavía cobertura total del ecosistema canario ni habilita alertas o pipeline."
    filter_form = render_filter_form(base_path, active_filters, available_filters, validation_error, pagination)
    if opportunities:
        rows = "\n".join(
            "<tr>"
            f'<td data-label="Oferta"><div class="offer-cell"><a class="offer-link" href="{escape(build_url(base_path, f"/oportunidades/{item["id"]}"))}">{escape(item["titulo"])}</a><a class="offer-action" href="{escape(build_url(base_path, f"/oportunidades/{item["id"]}"))}">Ver oferta concreta</a></div></td>'
            f'<td data-label="Organismo">{escape(item["organismo"])}</td>'
            f'<td data-label="Ubicación">{escape(item["ubicacion"])}</td>'
            f'<td data-label="Procedimiento">{escape(item["procedimiento"] or "No informado")}</td>'
            f'<td data-label="Presupuesto">{escape(_format_budget(item["presupuesto"]))}</td>'
            f'<td data-label="Publicación oficial">{escape(item["fecha_publicacion_oficial"])}</td>'
            f'<td data-label="Fecha límite">{escape(item["fecha_limite"])}</td>'
            f'<td data-label="Estado">{escape(item["estado"])}</td>'
            f'<td data-label="Fuente oficial"><a class="source-link" href="{escape(item["url_fuente_oficial"])}" target="_blank" rel="noopener noreferrer">{escape(item["fuente_oficial"])}</a></td>'
            "</tr>"
            for item in opportunities
        )
        catalog_panel = f'<section class="panel"><div class="panel-body"><div class="summary">{render_metric(catalog["total_oportunidades_catalogo"], "Oportunidades TI visibles")}{render_metric(len(catalog["cobertura_aplicada"]), coverage_label)}{render_metric(catalog["total_oportunidades_visibles"], "Oportunidades TI antes de filtrar")}</div>{render_pagination(base_path, active_filters, pagination)}<p class="muted">{coverage_note}</p></div><div class="table-wrap"><table><thead><tr><th>Oferta</th><th>Organismo</th><th>Ubicación</th><th>Procedimiento</th><th>Presupuesto</th><th>Publicación oficial</th><th>Fecha límite</th><th>Estado</th><th>Fuente oficial</th></tr></thead><tbody>{rows}</tbody></table></div><div class="panel-body">{render_pagination(base_path, active_filters, pagination)}</div></section>'
    else:
        message = "No hay resultados con los filtros activos." if active_filters and validation_error is None else ("No hay oportunidades TI disponibles en los snapshots `.atom` consolidados en este momento." if uses_atom_consolidation else "No hay oportunidades TI disponibles dentro de la cobertura MVP en este momento.")
        catalog_panel = f'<section class="note">{escape(message)}</section>'
    alert_link = build_url(base_path, "/alertas")
    active_query = _alert_filters_query(active_filters)
    save_link = f'<a class="button-link" href="{escape(alert_link)}{"?" + escape(active_query) if active_filters else ""}">Guardar estos criterios como alerta</a>' if active_filters else ""
    content = f"""
      <section class="note"><strong>Datos consolidados visibles del Excel</strong><br />La aplicación incorpora una superficie funcional alineada con <code>data/licitaciones_ti_canarias.xlsx</code> en las pestañas <strong>Licitaciones TI Canarias</strong>, <strong>Detalle Lotes</strong> y <strong>Adjudicaciones</strong>. <a class="button-link" href="{escape(build_url(base_path, '/datos-consolidados'))}">Abrir datos consolidados</a></section>
      {filter_form}
      <section class="note"><strong>Alertas tempranas del MVP</strong><br />Puedes guardar una alerta con estos mismos criterios desde <a href="{escape(alert_link)}">la gestión de alertas</a>. {save_link}</section>
      {catalog_panel}
      <p class="note">Referencia funcional activa: <code>{escape(catalog["referencia_funcional"])}</code>. Cada registro mantiene visible su fuente oficial, enlace oficial, fecha de publicación y estado oficial para facilitar verificación por <code>qa-teams</code>.</p>
    """
    return page_template("Licican | Catálogo inicial de oportunidades TI", "Catálogo inicial de oportunidades TI de Canarias", "Release 6 · PB-011 · Consolidacion funcional trazable", "Licican muestra aquí un catálogo consultable obtenido a partir de todos los snapshots `.atom` versionados presentes en `data/`. Solo se publican registros que cumplen simultáneamente criterio geográfico Canarias y criterio TI por CPV, con fuente oficial visible.", content, current_path="/", base_path=base_path)


def _format_budget(amount: int | None) -> str:
    if amount is None:
        return "Presupuesto no informado"
    return f"{amount:,.0f}".replace(",", ".") + " EUR"


def _catalog_page_url(base_path: str, filters: dict[str, object], page: int) -> str:
    query = urlencode({**{key: value for key, value in filters.items() if value not in (None, "")}, "page": page})
    return f"{build_url(base_path, '/')}" + (f"?{query}" if query else "")


def _pagination_adjustment_message(pagination: dict[str, object]) -> str | None:
    if not pagination.get("ajustada"):
        return None
    requested_page = pagination["pagina_solicitada"]
    current_page = pagination["pagina_actual"]
    if pagination.get("motivo_ajuste") == "invalida":
        return f"La pagina solicitada ({requested_page}) no es valida. Se muestra la pagina {current_page}."
    return f"La pagina solicitada ({requested_page}) no existe. Se muestra la pagina {current_page}."


def _validation_note(message: str | None) -> str | None:
    if message is None:
        return None
    return f"Corrige el rango de presupuesto. {message}"


def _active_filter_badges(filters: dict[str, object]) -> str:
    labels = {"palabra_clave": "Palabra clave", "presupuesto_min": "Presupuesto mínimo", "presupuesto_max": "Presupuesto máximo", "procedimiento": "Procedimiento", "ubicacion": "Ubicación"}
    if not filters:
        return ""
    badges = render_badges([(labels[key], str(value)) for key, value in filters.items()])
    return f'<div class="active-filters"><p><strong>Filtros activos</strong></p><div>{badges}</div></div>'


def _alert_filters_query(filters: dict[str, object]) -> str:
    return urlencode({key: value for key, value in filters.items() if value not in (None, "")})
