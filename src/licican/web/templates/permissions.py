from __future__ import annotations

from html import escape

from licican.access import AccessContext
from licican.web.templates.base import page_template


def render_permissions_matrix(payload: dict[str, object], base_path: str = "", access_context: AccessContext | None = None) -> str:
    rows = "".join(
        "<tr>"
        f"<th>{escape(str(item['rol']))}</th>"
        f"<td>{escape(str(item['consulta']))}</td>"
        f"<td>{escape(str(item['gestion']))}</td>"
        f"<td>{escape(str(item['gobierno']))}</td>"
        "</tr>"
        for item in payload["matriz"]
    )
    content = f"""
      <section class="permissions-view">
      <section class="panel" id="permissions-summary-panel">
        <div class="panel-body">
          <p><strong>Rol activo:</strong> {escape(str(payload["rol_activo"]))}</p>
          <p><strong>Contexto de usuario:</strong> {escape(str(payload["usuario_activo"]))}</p>
          <p class="muted">La primera iteracion gobierna catalogo, detalle, alertas y la propia matriz de permisos. El pipeline mantiene la misma base de control y queda preparado para ampliaciones posteriores sin redefinir reglas.</p>
        </div>
      </section>
      <section class="panel" id="permissions-matrix-panel">
        <div class="table-wrap permissions-table-wrap">
          <table class="permissions-table">
            <thead>
              <tr><th>Rol</th><th>Consulta</th><th>Gestion</th><th>Gobierno</th></tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </section>
      </section>
    """
    return page_template(
        "Licican | Matriz de permisos",
        "Matriz funcional de roles y permisos",
        "PB-013 · Gobierno funcional visible",
        "Esta superficie deja trazable que acciones consulta cada rol, que puede gestionar y donde existen restricciones operativas visibles.",
        content,
        current_path="/permisos",
        base_path=base_path,
        access_context=access_context,
    )
