from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric


def _render_kpi_card(kpi: dict[str, object]) -> str:
    value = kpi.get("valor_actual")
    value_label = str(kpi.get("valor_label", "Valor actual"))
    value_html = render_metric(value, value_label) if value is not None else ""
    return f"""
      <section class="panel">
        <div class="panel-body">
          {value_html}
          <h3>{escape(str(kpi["nombre"]))}</h3>
          <p><strong>Definición:</strong> {escape(str(kpi["definicion"]))}</p>
          <p><strong>Fórmula:</strong> {escape(str(kpi["formula"]))}</p>
          <p><strong>Umbral inicial:</strong> {escape(str(kpi["umbral_inicial"]))}</p>
          <p><strong>Decisión asociada:</strong> {escape(str(kpi["decision"]))}</p>
          <p><strong>Método de captura:</strong> {escape(str(kpi["captura"]))}</p>
          <p class="muted">{escape(str(kpi["limitacion"]))}</p>
        </div>
      </section>
    """


def render_kpis(payload: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    resumen_metrics = "".join(
        render_metric(value, label)
        for value, label in [
            (payload["resumen"]["fuentes_mvp"], "Fuentes MVP priorizadas"),
            (payload["resumen"]["cobertura_visible"], "Fuentes con cobertura visible"),
            (payload["resumen"]["alertas_activas"], "Alertas activas"),
            (payload["resumen"]["pipeline_visible"], "Oportunidades en seguimiento"),
        ]
    )
    cards = "".join(_render_kpi_card(item) for item in payload["indicadores"])
    content = f"""
      <section class="note">
        <strong>Definición documental de KPIs de producto</strong><br />
        Esta vista combina la lectura operativa disponible en la aplicación con la batería mínima definida para <code>PB-008</code>. La primera captura puede seguir siendo manual si todavía no existe instrumentación completa.
      </section>
      <section class="panel">
        <div class="panel-body">
          <p><strong>Rol activo:</strong> {escape(str(payload["rol_activo"]))}</p>
          <p><strong>Alcance mostrado:</strong> {escape(str(payload["alcance"]))}</p>
          <p><strong>Captura prevista:</strong> {escape(str(payload["modo_captura"]))}</p>
          <div class="summary">{resumen_metrics}</div>
        </div>
      </section>
      {cards}
      <section class="note">
        <strong>Lectura operativa</strong><br />
        La cobertura tiene base visible en la configuración del MVP, la adopción se apoya en alertas activas y el uso se mantiene documentado para consolidación manual o instrumentación posterior.
      </section>
    """
    return page_template(
        "Licican | KPIs iniciales de producto",
        "KPIs iniciales de cobertura, adopción y uso",
        "PB-008 · Medición documental con soporte operativo",
        "La vista resume la batería mínima de cobertura, adopción y uso con umbrales y decisiones asociadas. La primera medición puede consolidarse manualmente mientras la instrumentación completa sigue en preparación.",
        content,
        current_path="/kpis",
        base_path=base_path,
        access_context=access_context,
    )
