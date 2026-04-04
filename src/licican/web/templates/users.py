from __future__ import annotations

from html import escape
from urllib.parse import urlencode

from licican.access import AccessContext
from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import (
    render_badges,
    render_icon_button,
    render_inline_svg_icon,
    render_role_badge,
    render_state_badge,
    render_table,
)
from licican.shared.text import format_iso_datetime


def render_users(
    payload: dict[str, object],
    base_path: str = "",
    validation_error: str | None = None,
    status_message: str | None = None,
    access_context: AccessContext | None = None,
) -> str:
    filters = payload["filtros_activos"]
    available_filters = payload["filtros_disponibles"]
    pagination = payload["paginacion"]
    selected_user = payload.get("usuario_seleccionado")
    user_rows = [_render_user_row(base_path, user) for user in payload["usuarios"]]
    users_table = _render_users_table(user_rows)
    selected_user_panel = _render_selected_user_section(base_path, selected_user)
    selected_user_block = ""
    if selected_user_panel:
        selected_user_block = f"""
        <section class="panel" id="users-selected-panel">
          <div class="panel-body">
            {_status_note_div("La fecha de alta puede generarse automaticamente durante la creacion.", "ok")}
            {selected_user_panel}
          </div>
        </section>
        """
    users_table_block = ""
    if not selected_user_panel:
        users_table_block = f"""
        <section class="panel" id="users-table-panel">
          <div class="panel-body users-table-panel-body">
            <div class="pagination-status">
              <strong>Pagina {pagination["pagina_actual"]} de {pagination["total_paginas"]}</strong>
              <span class="muted">Mostrando {pagination["resultado_desde"]}-{pagination["resultado_hasta"]} de {pagination["total_resultados"]}</span>
            </div>
            {_render_pagination(base_path, filters, pagination)}
            {users_table}
            {_render_pagination(base_path, filters, pagination)}
          </div>
        </section>
        """

    content = f"""
        <section class="users-view" aria-label="Gestion de usuarios" data-users-index-url="{escape(build_url(base_path, '/usuarios'))}">
        <div class="users-create-toggle">
          <button type="button" id="toggle-users-create" aria-controls="users-create-panel" aria-expanded="false">Nuevo usuario</button>
        </div>
        <div class="users-toast-region" id="users-toast-region" aria-live="polite" aria-atomic="true"></div>
        <section class="panel" id="users-create-panel" hidden>
          <div class="panel-body">
            <h2>Nuevo usuario</h2>
            <form method="post" action="{escape(build_url(base_path, '/usuarios'))}">
              <div class="filters">
                <div><label for="nuevo_nombre">Nombre</label><input id="nuevo_nombre" name="nombre" type="text" required /></div>
                <div><label for="nuevo_apellidos">Apellidos</label><input id="nuevo_apellidos" name="apellidos" type="text" required /></div>
                <div><label for="nuevo_email">Email</label><input id="nuevo_email" name="email" type="email" required /></div>
                <div><label for="nuevo_rol">Rol principal</label><select id="nuevo_rol" name="rol_principal">{"".join(f'<option value="{escape(item)}">{escape(item.title())}</option>' for item in available_filters["roles"])}</select></div>
                <div><label for="nuevo_estado">Estado</label><select id="nuevo_estado" name="estado">{"".join(f'<option value="{escape(item)}"' + (' selected' if item == "pendiente" else '') + f'>{escape(item)}</option>' for item in available_filters["estados"])}</select></div>
              </div>
              <div class="filter-actions"><button type="submit">Crear usuario</button></div>
            </form>
          </div>
        </section>
        <section class="panel" id="users-filters-panel">
          <div class="panel-body">
            <h2>Filtros</h2>
            <form method="get" action="{escape(build_url(base_path, '/usuarios'))}">
              <div class="filters">
                <div><label for="busqueda">Busqueda</label><input id="busqueda" name="busqueda" type="text" value="{escape(str(filters.get('busqueda', '')))}" placeholder="Nombre, apellidos, email o identificador" /></div>
                <div><label for="rol">Rol</label><select id="rol" name="rol"><option value="">Todos</option>{"".join(f'<option value="{escape(item)}"' + (' selected' if filters.get("rol") == item else '') + f'>{escape(item)}</option>' for item in available_filters["roles"])}</select></div>
              </div>
              <div class="filter-actions">
                <button type="submit">Aplicar filtros</button>
                <a class="button-link" href="{escape(build_url(base_path, '/usuarios'))}">Limpiar filtros</a>
              </div>
            </form>
            {_filter_badges(filters)}
            {_status_note_div(validation_error, "warn")}
            {_status_note_div(status_message, "ok")}
          </div>
        </section>
        {selected_user_block}
        {users_table_block}
      </section>
      <script>
        (function () {{
          const button = document.getElementById('toggle-users-create');
          const panel = document.getElementById('users-create-panel');
          if (!button || !panel) {{
            return;
          }}

          panel.hidden = true;
          button.setAttribute('aria-expanded', 'false');

          button.addEventListener('click', function () {{
            const isHidden = panel.hasAttribute('hidden');
            if (isHidden) {{
              panel.removeAttribute('hidden');
              button.setAttribute('aria-expanded', 'true');
            }} else {{
              panel.setAttribute('hidden', '');
              button.setAttribute('aria-expanded', 'false');
            }}
          }});

          const usersView = document.querySelector('.users-view');
          const toastRegion = document.getElementById('users-toast-region');
          let activeDeleteToggle = null;

          function getDeleteToggle(userId) {{
            return document.getElementById('delete-toggle-' + userId);
          }}

          function showToast(message, tone) {{
            if (!toastRegion) {{
              return;
            }}

            const toast = document.createElement('div');
            toast.className = 'users-toast ' + (tone ? 'users-toast-' + tone : 'users-toast-success');
            toast.setAttribute('role', 'status');
            toast.textContent = message;
            toastRegion.appendChild(toast);

            window.setTimeout(function () {{
              toast.classList.add('is-visible');
            }}, 10);

            window.setTimeout(function () {{
              toast.classList.remove('is-visible');
              window.setTimeout(function () {{
                if (toast.parentNode) {{
                  toast.parentNode.removeChild(toast);
                }}
              }}, 180);
            }}, 2800);
          }}

          function hideConfirm(userId, restoreFocus) {{
            const toggle = getDeleteToggle(userId) || activeDeleteToggle;
            if (!toggle) {{
              return;
            }}

            const trigger = toggle.querySelector('[data-delete-toggle]');
            const confirmation = toggle.querySelector('.delete-toggle-confirmation');
            if (confirmation) {{
              confirmation.hidden = true;
            }}
            if (trigger) {{
              trigger.hidden = false;
              trigger.setAttribute('aria-expanded', 'false');
            }}
            toggle.classList.remove('is-confirming-delete');
            if (activeDeleteToggle === toggle) {{
              activeDeleteToggle = null;
            }}
            if (restoreFocus !== false && trigger) {{
              trigger.focus();
            }}
          }}

          function showConfirm(userId, userName) {{
            const toggle = getDeleteToggle(userId);
            if (!toggle) {{
              return;
            }}

            if (activeDeleteToggle && activeDeleteToggle !== toggle) {{
              hideConfirm(activeDeleteToggle.dataset.userId, false);
            }}

            const trigger = toggle.querySelector('[data-delete-toggle]');
            const confirmation = toggle.querySelector('.delete-toggle-confirmation');
            const userNameLabel = toggle.querySelector('.delete-toggle-user-name');
            const cancelButton = toggle.querySelector('[data-delete-cancel]');

            if (userNameLabel) {{
              userNameLabel.textContent = userName || toggle.dataset.userName || '';
            }}
            if (trigger) {{
              trigger.hidden = true;
              trigger.setAttribute('aria-expanded', 'true');
            }}
            if (confirmation) {{
              confirmation.hidden = false;
            }}
            toggle.classList.add('is-confirming-delete');
            activeDeleteToggle = toggle;
            if (cancelButton) {{
              cancelButton.focus();
            }}
          }}

          async function deleteUser(userId) {{
            const toggle = getDeleteToggle(userId);
            if (!toggle) {{
              return;
            }}

            const deleteUrl = toggle.dataset.deleteUrl || '';
            if (!deleteUrl) {{
              return;
            }}

            const confirmButton = toggle.querySelector('[data-delete-confirm]');
            const cancelButton = toggle.querySelector('[data-delete-cancel]');
            if (confirmButton) {{
              confirmButton.disabled = true;
            }}
            if (cancelButton) {{
              cancelButton.disabled = true;
            }}

            try {{
              const response = await fetch(deleteUrl, {{
                method: 'POST',
                credentials: 'same-origin',
                headers: {{
                  'X-Requested-With': 'fetch',
                }},
              }});

              if (!response.ok) {{
                throw new Error('La respuesta de borrado no fue correcta.');
              }}

              const row = document.getElementById('user-row-' + userId);
              if (row) {{
                row.remove();
                if (activeDeleteToggle === toggle) {{
                  activeDeleteToggle = null;
                }}
                showToast('Usuario eliminado correctamente.', 'success');
                return;
              }}

              window.location.assign(usersView ? usersView.dataset.usersIndexUrl || '/usuarios' : '/usuarios');
            }} catch (error) {{
              showToast('No se ha podido eliminar el usuario. Inténtalo de nuevo.', 'error');
              if (confirmButton) {{
                confirmButton.disabled = false;
              }}
              if (cancelButton) {{
                cancelButton.disabled = false;
              }}
            }}
          }}

          window.showConfirm = showConfirm;
          window.hideConfirm = hideConfirm;
          window.deleteUser = deleteUser;
        }})();
      </script>
    """
    return page_template(
        "Licican | Gestion de usuarios",
        "Gestion de usuarios",
        "PB-016 - Gobierno administrativo de cuentas",
        "Permite administrar cuentas, roles y accesos desde un backoffice institucional con trazabilidad visible.",
        content,
        current_path="/usuarios",
        base_path=base_path,
        access_context=access_context,
    )


def _filter_badges(filters: dict[str, object]) -> str:
    if not filters:
        return ""
    labels = {
        "busqueda": "Busqueda",
        "rol": "Rol",
    }
    return f'<div class="active-filters"><p><strong>Filtros activos</strong></p><div>{render_badges([(labels[key], str(value)) for key, value in filters.items() if key in labels])}</div></div>'


def _status_note_div(message: str | None, tone: str = "ok") -> str:
    if message is None:
        return ""
    class_name = "note" if tone == "ok" else "note note-warning"
    return f'<div class="{class_name}">{escape(message)}</div>'


def _render_users_table(user_rows: list[str]) -> str:
    if not user_rows:
        return '<section class="note">Todavia no hay usuarios que mostrar con los filtros activos.</section>'

    headers = ["Usuario", "Nombre completo", "Email", "Rol principal", "Estado", "Ultimo acceso"]
    header_html = "".join(f"<th>{escape(label)}</th>" for label in headers)
    return f"""
      <div class="table-wrap users-table-wrap">
        <table class="users-table">
          <colgroup>
            <col class="users-col users-col-username" />
            <col class="users-col users-col-name" />
            <col class="users-col users-col-email" />
            <col class="users-col users-col-role" />
            <col class="users-col users-col-state" />
            <col class="users-col users-col-last-access" />
            <col class="users-col users-col-actions" />
          </colgroup>
          <thead><tr>{header_html}<th style="width: 120px; text-align: right;">ACCIONES</th></tr></thead>
          <tbody>{''.join(user_rows)}</tbody>
        </table>
      </div>
    """


def _render_selected_user_section(base_path: str, selected_user: dict[str, object] | None) -> str:
    if selected_user is None:
        return ""

    history_rows = "".join(
        f"<tr><td>{escape(_format_user_datetime(item['fecha']))}</td><td>{escape(str(item['accion']))}</td><td>{escape(str(item['detalle']))}</td></tr>"
        for item in selected_user["historial"]
    )
    history_table = render_table(["Fecha", "Accion", "Detalle"], [history_rows], "Todavia no hay historial disponible.") if history_rows else '<section class="note">Todavia no hay historial disponible.</section>'
    role_options = "".join(
        f'<option value="{escape(role)}"' + (" selected" if selected_user["rol_principal"] == role else "") + f'>{escape(role.title())}</option>'
        for role in _role_options()
    )
    state_options = "".join(
        f'<option value="{escape(state)}"' + (" selected" if selected_user["estado"] == state else "") + f'>{escape(state)}</option>'
        for state in _state_options()
    )
    return f"""
        <h2>Detalle y edicion</h2>
        <p><strong>Usuario seleccionado:</strong> {escape(str(selected_user["nombre_completo"]))}</p>
        <p><strong>Estado actual:</strong> {render_state_badge(selected_user["estado"])}</p>
        <p><strong>Ultimo acceso:</strong> {escape(_format_user_datetime(selected_user["ultimo_acceso"]))}</p>
        <form method="post" action="{escape(build_url(base_path, f'/usuarios/{selected_user["id"]}'))}">
          <div class="filters">
            <div><label for="editar_username">Usuario</label><input id="editar_username" name="username" type="text" value="{escape(str(selected_user.get("username") or selected_user["email"]))}" /></div>
            <div><label for="editar_nombre">Nombre</label><input id="editar_nombre" name="nombre" type="text" value="{escape(str(selected_user["nombre"]))}" required /></div>
            <div><label for="editar_apellidos">Apellidos</label><input id="editar_apellidos" name="apellidos" type="text" value="{escape(str(selected_user["apellidos"]))}" required /></div>
            <div><label for="editar_email">Email</label><input id="editar_email" name="email" type="email" value="{escape(str(selected_user["email"]))}" required /></div>
            <div><label for="editar_rol">Rol principal</label><select id="editar_rol" name="rol_principal">{role_options}</select></div>
            <div><label for="editar_estado">Estado</label><select id="editar_estado" name="estado">{state_options}</select></div>
            <div><label for="editar_nueva_contrasena">Nueva contrasena</label><input id="editar_nueva_contrasena" name="nueva_contrasena" type="password" minlength="8" autocomplete="new-password" /></div>
            <div><label for="editar_confirmar_contrasena">Confirmar nueva contrasena</label><input id="editar_confirmar_contrasena" name="confirmar_contrasena" type="password" minlength="8" autocomplete="new-password" /></div>
          </div>
          <p class="muted">Fecha de alta: {escape(_format_user_datetime(selected_user["fecha_alta"]))}</p>
          <div class="filter-actions">
            <button type="submit">Guardar cambios</button>
            <a class="button-link" href="{escape(build_url(base_path, '/usuarios'))}">Cancelar</a>
          </div>
        </form>
        <div class="inline-actions">
          <a class="button-link" href="#editar_nueva_contrasena">Cambiar contrasena</a>
        </div>
        {_render_selected_user_actions(base_path, selected_user)}
        <h3>Historial de cambios</h3>
        {history_table}
    """


def _render_selected_user_actions(base_path: str, selected_user: dict[str, object]) -> str:
    actions = _build_action_controls(base_path, selected_user)
    if not actions:
        return ""
    return f'<div class="inline-actions">{ "".join(actions) }</div>'


def _render_user_row(base_path: str, user: dict[str, object]) -> str:
    actions = _build_action_controls(base_path, user)
    login_name = str(user.get("username") or user["email"])
    return (
        f'<tr id="user-row-{escape(str(user["id"]))}">'
        f'<td data-label="Usuario">{escape(login_name)}</td>'
        f'<td data-label="Nombre completo">{escape(str(user["nombre_completo"]))}</td>'
        f'<td data-label="Email">{escape(str(user["email"]))}</td>'
        f'<td data-label="Rol principal">{render_role_badge(user["rol_principal"])}</td>'
        f'<td data-label="Estado">{render_state_badge(user["estado"])}</td>'
        f'<td data-label="Ultimo acceso">{escape(_format_user_datetime(user["ultimo_acceso"]))}</td>'
        f'<td data-label="ACCIONES"><div class="actions-cell">{"".join(actions)}</div></td>'
        "</tr>"
    )


def _build_action_controls(base_path: str, user: dict[str, object]) -> list[str]:
    actions: list[str] = []
    actions.append(
        render_icon_button(
            label="Modificar",
            icon_svg=render_inline_svg_icon("edit"),
            href=build_url(base_path, f"/usuarios/{user["id"]}"),
            css_class="btn-icon--edit",
            tooltip="Modificar",
            aria_label=f"Modificar usuario {user['nombre_completo']}",
        )
    )
    if user["estado"] == "activo":
        actions.append(_action_form(base_path, user["id"], "Deshabilitar", "inactivo"))
    else:
        actions.append(_action_form(base_path, user["id"], "Reactivar", "activo"))
    actions.append(_delete_toggle_fragment(base_path, user))
    return actions


def _action_form(base_path: str, user_id: str, label: str, state: str | None, query_href: str | None = None) -> str:
    if query_href is not None:
        return render_icon_button(
            label=label,
            icon_svg=render_inline_svg_icon("more"),
            href=build_url(base_path, query_href),
            css_class="btn-icon--edit",
            tooltip=label,
            aria_label=label,
        )
    assert state is not None
    button_class = "btn-icon--ban" if state == "inactivo" else "btn-icon--restore"
    icon_name = "ban" if state == "inactivo" else "restore"
    return f"""
      <form class="btn-icon-form" method="post" action="{escape(build_url(base_path, f'/usuarios/{user_id}/estado'))}">
        <input type="hidden" name="estado" value="{escape(state)}" />
        <button type="submit" class="btn-icon {button_class}" data-tooltip="{escape(label)}" aria-label="{escape(label)}">
          {render_inline_svg_icon(icon_name)}
        </button>
      </form>
    """


def _delete_toggle_fragment(base_path: str, user: dict[str, object]) -> str:
    raw_user_id = str(user["id"])
    user_id = escape(raw_user_id)
    user_name = escape(str(user["nombre_completo"]))
    delete_url = escape(build_url(base_path, f"/usuarios/{raw_user_id}/borrar"))
    return f"""
      <div class="delete-toggle" id="delete-toggle-{user_id}" data-user-id="{user_id}" data-user-name="{user_name}" data-delete-url="{delete_url}">
        <button
          type="button"
          class="btn-icon btn-icon--delete delete-toggle-trigger"
          data-delete-toggle
          data-user-id="{user_id}"
          data-user-name="{user_name}"
          data-delete-url="{delete_url}"
          aria-controls="delete-confirm-{user_id}"
          aria-expanded="false"
          onclick="showConfirm(this.dataset.userId, this.dataset.userName)"
          aria-label="Eliminar usuario"
          data-tooltip="Eliminar"
        >{render_inline_svg_icon("trash")}</button>
        <div class="delete-toggle-confirmation" id="delete-confirm-{user_id}" hidden>
          <span class="delete-toggle-message">¿Confirmar eliminación de <strong class="delete-toggle-user-name">{user_name}</strong>?</span>
          <button type="button" class="btn-icon btn-icon--delete delete-toggle-confirm" data-delete-confirm onclick="deleteUser(this.closest('.delete-toggle').dataset.userId)" aria-label="Eliminar usuario" data-tooltip="Eliminar">{render_inline_svg_icon("trash")}</button>
          <button type="button" class="btn-icon btn-icon--edit delete-toggle-cancel" data-delete-cancel onclick="hideConfirm(this.closest('.delete-toggle').dataset.userId)" aria-label="Cancelar" data-tooltip="Cancelar">{render_inline_svg_icon("cancel")}</button>
        </div>
      </div>
    """


def _state_options() -> list[str]:
    return ["pendiente", "activo", "inactivo", "bloqueado"]


def _role_options() -> list[str]:
    return ["administrador", "manager", "colaborador", "invitado"]


def _format_user_datetime(value: object | None) -> str:
    formatted = format_iso_datetime(value)
    if formatted is None:
        return "Nunca"
    return formatted


def _render_pagination(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    if int(pagination["total_paginas"]) <= 1:
        return ""
    hidden_fields = "".join(f'<input type="hidden" name="{escape(str(key))}" value="{escape(str(value))}" />' for key, value in filters.items())
    prev_link = ""
    if pagination["pagina_anterior"] is not None:
        prev_link = f'<a class="button-link" href="{escape(_page_url(base_path, filters, int(pagination["pagina_anterior"]), int(pagination["tamano_pagina"])))}">Pagina anterior</a>'
    next_link = ""
    if pagination["pagina_siguiente"] is not None:
        next_link = f'<a class="button-link" href="{escape(_page_url(base_path, filters, int(pagination["pagina_siguiente"]), int(pagination["tamano_pagina"])))}">Pagina siguiente</a>'
    page_size_options = "".join(
        f'<option value="{value}"' + (" selected" if int(pagination["tamano_pagina"]) == value else "") + f">{value}</option>"
        for value in (5, 10, 25, 50)
    )
    return f'''
      <div class="pagination-bar">
        <div class="pagination-status">
          <strong>Pagina {pagination["pagina_actual"]} de {pagination["total_paginas"]}</strong>
          <span class="muted">Mostrando {pagination["resultado_desde"]}-{pagination["resultado_hasta"]} de {pagination["total_resultados"]}</span>
        </div>
        <div class="pagination-actions">{prev_link}{next_link}</div>
        <form class="pagination-jump" method="get" action="{escape(build_url(base_path, "/usuarios"))}">
          {hidden_fields}
          <label for="users-page-size">Resultados por pagina</label>
          <select id="users-page-size" name="page_size" onchange="this.form.submit()">{page_size_options}</select>
          <label for="users-page">Ir a la pagina</label>
          <input id="users-page" name="page" type="number" min="1" max="{pagination["total_paginas"]}" value="{pagination["pagina_actual"]}" />
          <button type="submit">Ir</button>
        </form>
      </div>
    '''


def _page_url(base_path: str, filters: dict[str, object], page: int, page_size: int) -> str:
    query = urlencode({**{key: value for key, value in filters.items() if value not in (None, "")}, "page": page, "page_size": page_size})
    return f"{build_url(base_path, '/usuarios')}" + (f"?{query}" if query else "")
