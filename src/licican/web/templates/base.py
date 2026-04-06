from __future__ import annotations

from html import escape

from licican.access import AccessContext, ROLE_ADMINISTRATOR, ROLE_COLLABORATOR, ROLE_INVITED, ROLE_MANAGER, ROLE_SUPERADMIN
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
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Alertas", "description": "Criterios guardados y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo de oportunidades", "icon": "PL", "path": "/pipeline", "upcoming": False},
        ]

    by_role = {
        ROLE_ADMINISTRATOR: [
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Alertas", "description": "Criterios guardados y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo de oportunidades", "icon": "PL", "path": "/pipeline", "upcoming": False},
        ],
        ROLE_SUPERADMIN: [
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Alertas", "description": "Criterios guardados y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo de oportunidades", "icon": "PL", "path": "/pipeline", "upcoming": False},
        ],
        ROLE_MANAGER: [
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Alertas", "description": "Criterios propios y coincidencias activas", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Seguimiento operativo propio", "icon": "PL", "path": "/pipeline", "upcoming": False},

        ],
        ROLE_COLLABORATOR: [
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
            {"label": "Alertas", "description": "Consulta de criterios y coincidencias", "icon": "AL", "path": "/alertas", "upcoming": False},
            {"label": "Pipeline", "description": "Consulta del seguimiento operativo", "icon": "PL", "path": "/pipeline", "upcoming": False},
        ],
        ROLE_INVITED: [
            {"label": "Dashboard", "description": "Resumen general de actividad", "icon": "DB", "path": "/dashboard", "upcoming": False},
            {"label": "Catalogo", "description": "Oportunidades, filtros y paginacion", "icon": "CT", "path": "/", "upcoming": False},
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


_CHEVRON_ICON = '<svg class="nav-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>'

_ADMIN_SUBITEMS: list[tuple[str, str, str]] = [
    (
        "Usuarios",
        "/usuarios",
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    ),
    (
        "Permisos",
        "/permisos",
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    ),
    (
        "Clasificacion TI",
        "/clasificacion-ti",
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><circle cx="7" cy="7" r="1" fill="currentColor" stroke="none"/></svg>',
    ),
    (
        "Conservacion",
        "/conservacion",
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8v13H3V8"/><path d="M1 3h22v5H1z"/><path d="M10 12h4"/></svg>',
    ),
]


def _nav_admin_group_html(base_path: str, current_path: str) -> str:
    is_open = any(_path_matches_navigation(current_path, path) for _, path, _ in _ADMIN_SUBITEMS)
    open_attr = " open" if is_open else ""
    links = "".join(
        f'<li><a class="nav-sublink{" active" if _path_matches_navigation(current_path, path) else ""}" href="{escape(build_url(base_path, path))}"><span class="nav-sublink-icon">{icon}</span><span>{escape(label)}</span></a></li>'
        for label, path, icon in _ADMIN_SUBITEMS
    )
    return f"""
      <li>
        <details class="nav-group"{open_attr}>
          <summary class="nav-link">
            <span class="nav-icon" aria-hidden="true">AD</span>
            <span class="nav-copy-block">
              <span class="nav-label">Administración</span>
            </span>
            {_CHEVRON_ICON}
          </summary>
          <ul class="nav-sublist">
            {links}
          </ul>
        </details>
      </li>
    """


def _navigation_html(base_path: str, current_path: str, access_context: AccessContext | None = None) -> str:
    nav_items = _navigation_items(access_context)
    items_html = "".join(_navigation_item_html(base_path, current_path, item) for item in nav_items)
    if access_context is not None and access_context.role in (ROLE_ADMINISTRATOR, ROLE_SUPERADMIN):
        items_html += _nav_admin_group_html(base_path, current_path)
    list_html = f'<ul class="nav-list">{items_html}</ul>'
    footer_html = _navigation_footer_html(base_path, access_context)
    return f"""
      <aside id="side-nav" class="side-nav" aria-label="Navegacion principal">
        <h2 class="nav-title">Licican</h2>
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
