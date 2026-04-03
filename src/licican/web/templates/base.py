from __future__ import annotations

from html import escape

from licican.access import AccessContext, ROLE_ADMINISTRATOR, ROLE_COLLABORATOR, ROLE_INVITED, ROLE_MANAGER
from licican.web.responses import build_url


def page_template(
    document_title: str,
    page_heading: str,
    hero_label: str,
    hero_body: str,
    content: str,
    current_path: str = "/",
    base_path: str = "",
    access_context: AccessContext | None = None,
) -> str:
    """Compone el layout HTML base de la aplicación."""
    navigation = _navigation_html(base_path, current_path, access_context)
    auto_login_notice = _auto_login_notice_html(access_context)
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(document_title)}</title>
    <link rel="stylesheet" href="{escape(build_url(base_path, '/static/style.css'))}" />
  </head>
  <body>
    <div class="app-shell">
      <div class="app-frame">
        {navigation}
        <div class="content-shell">
          <main>
            {auto_login_notice}
            <section class="hero">
              <p class="muted">{escape(hero_label)}</p>
              <h1>{escape(page_heading)}</h1>
              <p>{hero_body}</p>
            </section>
            {content}
          </main>
        </div>
      </div>
    </div>
  </body>
</html>"""


def _navigation_items(access_context: AccessContext | None = None) -> list[dict[str, str | bool]]:
    if access_context is None:
        return [
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Datos consolidados", "description": "Excel funcional, lotes y adjudicaciones", "icon": "DC", "path": "/datos-consolidados", "upcoming": False},
            {"label": "Alertas", "description": "Criterios guardados y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Clasificacion TI", "description": "Reglas auditables y casos frontera", "icon": "TI", "path": "/clasificacion-ti", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo de oportunidades", "icon": "PL", "path": "/pipeline", "upcoming": False},
            {"label": "Permisos", "description": "Roles y restricciones por superficie", "icon": "PM", "path": "", "upcoming": True},
        ]

    by_role = {
        ROLE_ADMINISTRATOR: [
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Datos consolidados", "description": "Excel funcional, lotes y adjudicaciones", "icon": "DC", "path": "/datos-consolidados", "upcoming": False},
            {"label": "Alertas", "description": "Criterios guardados y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Clasificacion TI", "description": "Reglas auditables y casos frontera", "icon": "TI", "path": "/clasificacion-ti", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo de oportunidades", "icon": "PL", "path": "/pipeline", "upcoming": False},
            {"label": "Usuarios", "description": "Cuentas, roles y accesos", "icon": "US", "path": "/usuarios", "upcoming": False},
            {"label": "KPIs", "description": "Cobertura, adopcion y uso visibles", "icon": "KP", "path": "/kpis", "upcoming": False},
            {"label": "Conservacion", "description": "Retencion y archivado operativo", "icon": "RC", "path": "/conservacion", "upcoming": False},
            {"label": "Permisos", "description": "Roles y restricciones por superficie", "icon": "PM", "path": "/permisos", "upcoming": False},
        ],
        ROLE_MANAGER: [
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Datos consolidados", "description": "Excel funcional, lotes y adjudicaciones", "icon": "DC", "path": "/datos-consolidados", "upcoming": False},
            {"label": "Alertas", "description": "Criterios propios y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Clasificacion TI", "description": "Reglas auditables y casos frontera", "icon": "TI", "path": "/clasificacion-ti", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo propio", "icon": "PL", "path": "/pipeline", "upcoming": False},
            {"label": "KPIs", "description": "Indicadores de cobertura y uso", "icon": "KP", "path": "/kpis", "upcoming": False},
        ],
        ROLE_COLLABORATOR: [
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Datos consolidados", "description": "Excel funcional, lotes y adjudicaciones", "icon": "DC", "path": "/datos-consolidados", "upcoming": False},
            {"label": "Clasificacion TI", "description": "Reglas auditables y casos frontera", "icon": "TI", "path": "/clasificacion-ti", "upcoming": False},
            {"label": "Alertas", "description": "Consulta de criterios y coincidencias", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Consulta del seguimiento operativo", "icon": "PL", "path": "/pipeline", "upcoming": False},
        ],
        ROLE_INVITED: [
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Datos consolidados", "description": "Excel funcional, lotes y adjudicaciones", "icon": "DC", "path": "/datos-consolidados", "upcoming": False},
            {"label": "Clasificacion TI", "description": "Reglas auditables y casos frontera", "icon": "TI", "path": "/clasificacion-ti", "upcoming": False},
        ],
    }
    return by_role[access_context.role]


def _context_html(base_path: str, access_context: AccessContext | None) -> str:
    if access_context is None:
        return ""
    user_menu = _user_menu_html(base_path, access_context)
    return f"""
      <div class="nav-section">
        <p class="nav-section-title">Contexto activo</p>
        <p class="nav-copy"><strong>Rol:</strong> {escape(access_context.role_label)}<br /><strong>Alcance:</strong> {escape(access_context.scope_label)}<br /><strong>Usuario:</strong> {escape(access_context.user_id)}</p>
        {user_menu}
      </div>
    """


def _user_menu_html(base_path: str, access_context: AccessContext) -> str:
    csrf_token = getattr(access_context, "csrf_token", "")
    badge = " · superadmin" if access_context.is_superadmin else ""
    hidden_token = f'<input type="hidden" name="csrf_token" value="{escape(csrf_token)}" />' if csrf_token else ""
    return f"""
      <div class="user-menu">
        <p class="nav-copy"><strong>Sesión:</strong> {escape(access_context.display_name or access_context.user_id)}{escape(badge)}</p>
        <form method="post" action="{escape(build_url(base_path, '/logout'))}">
          {hidden_token}
          <button class="button button-secondary button-small" type="submit">Cerrar sesión</button>
        </form>
      </div>
    """


def _auto_login_notice_html(access_context: AccessContext | None) -> str:
    if access_context is None or not access_context.auto_login_active:
        return ""
    return """
      <section class="note note-warning auth-mode-note">
        <strong>Sesión automática activa (entorno desarrollo)</strong>
      </section>
    """


def _path_matches_navigation(current_path: str, item_path: str) -> bool:
    if item_path == "/":
        return current_path == "/" or current_path.startswith("/oportunidades/")
    if item_path == "/datos-consolidados":
        return current_path == item_path or current_path.startswith(f"{item_path}/")
    return current_path == item_path or current_path.startswith(f"{item_path}/")


def _navigation_item_html(base_path: str, current_path: str, item: dict[str, str | bool]) -> str:
    label = str(item["label"])
    description = str(item["description"])
    icon = str(item["icon"])
    path = str(item["path"])
    upcoming = bool(item["upcoming"])
    if upcoming:
        return f"""
          <li>
            <div class="nav-link-static">
              <span class="nav-icon" aria-hidden="true">{escape(icon)}</span>
              <span class="nav-copy-block">
                <span class="nav-label">{escape(label)}</span>
                <span class="nav-help">{escape(description)}</span>
              </span>
              <span class="nav-tag">proximamente</span>
            </div>
          </li>
        """
    class_name = "nav-link active" if _path_matches_navigation(current_path, path) else "nav-link"
    return f"""
      <li>
        <a class="{class_name}" href="{escape(build_url(base_path, path))}">
          <span class="nav-icon" aria-hidden="true">{escape(icon)}</span>
          <span class="nav-copy-block">
            <span class="nav-label">{escape(label)}</span>
            <span class="nav-help">{escape(description)}</span>
          </span>
          <span class="nav-tag">activo</span>
        </a>
      </li>
    """


def _navigation_html(base_path: str, current_path: str, access_context: AccessContext | None = None) -> str:
    items = "".join(_navigation_item_html(base_path, current_path, item) for item in _navigation_items(access_context))
    list_html = f'<ul class="nav-list">{items}</ul>'
    footer_html = _navigation_footer_html(base_path, access_context)
    return f"""
      <aside class="side-nav" aria-label="Navegacion principal">
        <p class="nav-kicker">PB-010</p>
        <h2 class="nav-title">Licican</h2>
        <p class="nav-copy">Base de navegacion comun para catalogo, alertas y crecimiento de modulos sin rutas huerfanas.</p>
        {_context_html(base_path, access_context)}
        <div class="nav-section">
          <p class="nav-section-title">Modulos</p>
          {list_html}
        </div>
        {footer_html}
      </aside>
      <details class="mobile-nav">
        <summary>Menu principal</summary>
        <div class="mobile-nav-body">
          {_context_html(base_path, access_context)}
          {list_html}
          {footer_html}
        </div>
      </details>
    """


def _navigation_footer_html(base_path: str, access_context: AccessContext | None) -> str:
    logout_button = _user_menu_html(base_path, access_context) if access_context is not None else ""
    return f"""
      <div class="nav-footer">
        <p class="nav-note">
          La navegacion solo expone superficies operativas compatibles con el rol activo y mantiene la experiencia de consulta cuando una accion queda restringida.
        </p>
        {logout_button}
      </div>
    """
