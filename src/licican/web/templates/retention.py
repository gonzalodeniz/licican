from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric, render_state_badge, render_status_note, render_table


def render_retention_control(
    payload: dict[str, object],
    base_path: str = "",
    validation_error: str | None = None,
    status_message: str | None = None,
    access_context: AccessContext | None = None,
) -> str:
    policy = payload["politica"]
    summary = payload["resumen"]
    groups = payload["grupos"]
    modes = payload["modos_disponibles"]
    metrics = "".join(
        (
            render_metric(summary["conservar"], "Conservar en operativo"),
            render_metric(summary["archivar"], "Archivar al aplicar politica"),
            render_metric(summary["mantener_activas"], "Mantener activas"),
            render_metric(summary["archivadas_existentes"], "Ya archivadas"),
        )
    )
    content = f"""
      <section class="note">
        <strong>Gobierno operativo de retencion</strong><br />
        La politica permite fijar el umbral en dias y previsualizar que expedientes seguiran en operativo, cuales pasaran a archivo y cuales se mantendran activos por seguimiento.
      </section>
      {render_status_note(validation_error, "warn")}
      {render_status_note(status_message)}
      <section class="panel">
        <h2>Politica vigente</h2>
        <div class="metrics-grid">{metrics}</div>
        <p><strong>Modo actual:</strong> {escape(str(policy["modo_label"]))}</p>
        <p><strong>Antiguedad configurada:</strong> {escape(str(policy["antiguedad_dias"]))} dias</p>
        <p><strong>Ultima actualizacion:</strong> {escape(str(policy.get("actualizada_en") or "No informada"))}</p>
        <form method="post" action="{escape(build_url(base_path, '/conservacion/politica'))}">
          <div class="filters">
            <div>
              <label for="antiguedad_dias">Antiguedad de conservacion en dias</label>
              <input id="antiguedad_dias" name="antiguedad_dias" type="number" min="1" value="{escape(str(policy['antiguedad_dias']))}" required />
            </div>
            <div>
              <label for="modo">Modo de politica</label>
              <select id="modo" name="modo">
                {"".join(_mode_option_html(item, str(policy["modo"])) for item in modes)}
              </select>
            </div>
          </div>
          <div class="filter-actions">
            <button type="submit">Guardar politica</button>
          </div>
        </form>
      </section>
      <section class="panel">
        <h2>Ejecucion controlada</h2>
        <p class="muted">La aplicacion no borra licitaciones con seguimiento activo. Al aplicar la politica, las cerradas que superan el umbral pasan a <code>licitacion_archivada</code> y salen de la tabla operativa.</p>
        <form method="post" action="{escape(build_url(base_path, '/conservacion/aplicar'))}">
          <button type="submit">Aplicar archivado ahora</button>
        </form>
      </section>
      <section class="panel">
        <h2>Previsualizacion operativa</h2>
        <p class="muted">Los listados muestran una muestra de expedientes por destino operativo. La decision se calcula con la politica actual y el estado de seguimiento disponible.</p>
        {_group_section("Conservar", groups["conservar"], "Quedaran en la tabla operativa porque siguen dentro del horizonte configurado o todavia no son archivables.")}
        {_group_section("Archivar", groups["archivar"], "Se moveran a la tabla archivada cuando se aplique la politica, conservando trazabilidad del expediente.")}
        {_group_section("Mantener activas", groups["mantener_activas"], "Permanecen operativas porque tienen seguimiento activo y no deben desaparecer del flujo de trabajo.")}
      </section>
    """
    return page_template(
        "Licican | Conservacion y archivado",
        "Panel de control de conservacion y archivado",
        "PB-015 · Gobierno de retencion del dato operativo",
        "Permite ajustar la politica de antiguedad y hacer visible el efecto sobre las licitaciones operativas, archivadas y con seguimiento activo.",
        content,
        current_path="/conservacion",
        base_path=base_path,
        access_context=access_context,
    )


def _mode_option_html(item: dict[str, object], selected: str) -> str:
    value = str(item["valor"])
    is_selected = " selected" if selected == value else ""
    return f'<option value="{escape(value)}"{is_selected}>{escape(str(item["etiqueta"]))}</option>'


def _group_section(title: str, items: list[dict[str, object]], description: str) -> str:
    rows = []
    for item in items[:10]:
        rows.append(
            "<tr>"
            f'<td data-label="Expediente">{escape(str(item["expediente"]))}</td>'
            f'<td data-label="Titulo">{escape(str(item["titulo"]))}</td>'
            f'<td data-label="Organismo">{escape(str(item["organismo"]))}</td>'
            f'<td data-label="Estado">{render_state_badge(item["estado"])}</td>'
            f'<td data-label="Seguimiento">{escape("Activo" if item["seguimiento_activo"] else "No activo")}</td>'
            f'<td data-label="Antiguedad">{escape(str(item["dias_antiguedad"] if item["dias_antiguedad"] is not None else "No aplica"))}</td>'
            f'<td data-label="Motivo">{escape(str(item["motivo"]))}</td>'
            "</tr>"
        )
    table = render_table(
        ["Expediente", "Titulo", "Organismo", "Estado", "Seguimiento", "Dias", "Motivo"],
        rows,
        "No hay expedientes en este grupo con la politica actual.",
    )
    return f"""
      <article class="panel">
        <h3>{escape(title)}</h3>
        <p class="muted">{escape(description)}</p>
        {table}
      </article>
    """
