from __future__ import annotations

from html import escape

from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import render_badges, render_metric, render_status_note


def render_alert_form(base_path: str, form_active_filters: dict[str, object], available_filters: dict[str, list[str]], form_error: str | None = None, status_message: str | None = None) -> str:
    """Renderiza el formulario de alertas."""
    return f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Crear alerta</h2>
          <p class="muted">La alerta reutiliza exactamente los mismos criterios funcionales del catálogo. En este MVP registra coincidencias internas visibles, sin notificación saliente.</p>
          {render_status_note(status_message, 'ok')}
          {render_status_note(form_error, 'warn')}
          <form method="post" action="{escape(build_url(base_path, '/alertas'))}">
            <div class="filters">
              <div><label for="alerta_palabra_clave">Palabra clave</label><input id="alerta_palabra_clave" name="palabra_clave" type="text" value="{escape(str(form_active_filters.get('palabra_clave', '')))}" placeholder="backup, licencias, redes..." /></div>
              <div><label for="alerta_presupuesto_min">Presupuesto mínimo</label><input id="alerta_presupuesto_min" name="presupuesto_min" type="number" min="0" step="1" value="{escape(str(form_active_filters.get('presupuesto_min', '')))}" /></div>
              <div><label for="alerta_presupuesto_max">Presupuesto máximo</label><input id="alerta_presupuesto_max" name="presupuesto_max" type="number" min="0" step="1" value="{escape(str(form_active_filters.get('presupuesto_max', '')))}" /></div>
              <div><label for="alerta_procedimiento">Procedimiento</label><select id="alerta_procedimiento" name="procedimiento"><option value="">Todos</option>{"".join(f'<option value=\"{escape(item)}\"' + (' selected' if form_active_filters.get('procedimiento') == item else '') + f'>{escape(item)}</option>' for item in available_filters["procedimientos"])}</select></div>
              <div><label for="alerta_ubicacion">Ubicación</label><select id="alerta_ubicacion" name="ubicacion"><option value="">Todas</option>{"".join(f'<option value=\"{escape(item)}\"' + (' selected' if form_active_filters.get('ubicacion') == item else '') + f'>{escape(item)}</option>' for item in available_filters["ubicaciones"])}</select></div>
            </div>
            <div class="filter-actions"><button type="submit">Guardar alerta</button><a class="button-link" href="{escape(build_url(base_path, '/alertas'))}">Limpiar formulario</a></div>
          </form>
        </div>
      </section>
    """


def render_alerts(reference: str, alerts, summary: dict[str, int], available_filters: dict[str, list[str]], base_path: str = "", form_active_filters: dict[str, object] | None = None, form_error: str | None = None, status_message: str | None = None) -> str:
    """Renderiza la gestión completa de alertas."""
    create_form = render_alert_form(base_path, form_active_filters or {}, available_filters, form_error, status_message)
    sections = []
    for alert in alerts:
        alert_filters = alert.filtros.active_filters()
        badges = render_badges({
            "Palabra clave": str(alert_filters.get("palabra_clave", "")),
            "Presupuesto mínimo": str(alert_filters.get("presupuesto_min", "")),
            "Presupuesto máximo": str(alert_filters.get("presupuesto_max", "")),
            "Procedimiento": str(alert_filters.get("procedimiento", "")),
            "Ubicación": str(alert_filters.get("ubicacion", "")),
        })
        coincidence_items = "".join(
            f'<li><a class="offer-link" href="{escape(build_url(base_path, f"/oportunidades/{match.id}"))}">{escape(match.titulo)}</a> · {escape(match.organismo)} · {escape(match.estado)}</li>'
            for match in alert.coincidencias
        ) or "<li>Sin coincidencias accionables registradas en este momento.</li>"
        sections.append(f'<section class="panel"><div class="panel-body"><div class="summary">{render_metric("Activa" if alert.activa else "Inactiva", "Estado actual")}{render_metric(len(alert.coincidencias), "Coincidencias accionables")}{render_metric(alert.id, "Identificador interno")}</div><p><strong>Criterios actuales:</strong> {_alert_summary_text(alert_filters)}</p><p class="muted">Creada: {escape(alert.creada_en)} · Última actualización: {escape(alert.actualizada_en)}</p><div>{badges}</div><h3>Coincidencias internas registradas</h3><ul>{coincidence_items}</ul></div></section>')
    alert_list = "".join(sections) if alerts else '<section class="note">Todavía no hay alertas registradas. Guarda la primera para dejar visible el criterio activo del MVP.</section>'
    content = f"""
      {create_form}
      <section class="panel"><div class="panel-body"><div class="summary">{render_metric(summary["total_alertas"], "Alertas totales")}{render_metric(summary["alertas_activas"], "Alertas activas")}{render_metric(summary["coincidencias_activas"], "Coincidencias accionables activas")}</div><p class="muted">Referencia funcional activa: <code>{escape(reference)}</code>. Esta vista no envía notificaciones; solo registra coincidencias internas accionables del MVP.</p></div></section>
      {alert_list}
    """
    return page_template("Licican | Alertas tempranas del MVP", "Gestión de alertas tempranas", "Release 2 · PB-004 · Registro interno de anticipación", "Licican permite guardar criterios persistentes para dejar visible qué oportunidades TI deben seguirse sin búsqueda manual recurrente. En esta primera entrega las coincidencias quedan registradas en la propia aplicación como soporte interno del MVP.", content, current_path="/alertas", base_path=base_path)


def _alert_summary_text(filters: dict[str, object]) -> str:
    labels = {"palabra_clave": "Palabra clave", "presupuesto_min": "Presupuesto mínimo", "presupuesto_max": "Presupuesto máximo", "procedimiento": "Procedimiento", "ubicacion": "Ubicación"}
    if not filters:
        return "Sin criterios informados"
    return " · ".join(f"{labels[key]}: {value}" for key, value in filters.items())
