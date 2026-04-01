from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.templates.base import page_template
from licican.web.templates.components import render_metric


def render_kpis(payload: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    cards = "".join(
        f"""
      <section class="panel">
        <div class="panel-body">
          {render_metric(item["valor"], item["nombre"])}
          <p><strong>Lectura:</strong> {escape(str(item["lectura"]))}</p>
          <p class="muted">{escape(str(item["alcance"]))}</p>
        </div>
      </section>
    """
        for item in payload["indicadores"]
    )
    content = f"""
      <section class="note">
        <strong>Indicadores operativos provisionales</strong><br />
        Esta vista reutiliza senales ya disponibles en el producto para consulta operativa por rol y no sustituye la definicion documental de KPIs de <code>PB-008</code>.
      </section>
      <section class="panel">
        <div class="panel-body">
          <p><strong>Rol activo:</strong> {escape(str(payload["rol_activo"]))}</p>
          <p><strong>Alcance mostrado:</strong> {escape(str(payload["alcance"]))}</p>
        </div>
      </section>
      {cards}
    """
    return page_template(
        "Licican | KPIs operativos",
        "KPIs operativos visibles por rol",
        "PB-013 · Lectura operativa acotada por permisos",
        "La vista resume senales de cobertura, adopcion y uso sin exponer controles de gestion a roles que no deben operarlos.",
        content,
        current_path="/kpis",
        base_path=base_path,
        access_context=access_context,
    )
