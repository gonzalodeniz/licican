from __future__ import annotations

from html import escape
from urllib.parse import urlencode

from licican.access import AccessContext
from licican.web.responses import build_url
from licican.web.templates.base import page_template
from licican.web.templates.components import (
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
    has_active_filters = bool(filters)
    user_rows = [_render_user_row(base_path, user) for user in payload["usuarios"]]
    users_table = _render_users_table(user_rows)
    selected_user_panel = _render_selected_user_section(base_path, selected_user)
    create_toggle_block = ""
    if not selected_user_panel:
        create_toggle_block = """
        <div class="users-create-toggle">
          <button type="button" id="toggle-users-create" aria-controls="users-create-panel" aria-expanded="false">Nuevo usuario</button>
        </div>
        """
    selected_user_block = ""
    if selected_user_panel:
        selected_user_block = f"""
        <section class="panel" id="users-selected-panel">
          <div class="panel-body">
            {_status_toast_div("La fecha de alta puede generarse automaticamente durante la creacion.", "success")}
            {selected_user_panel}
          </div>
        </section>
        """
    users_table_block = ""
    if not selected_user_panel:
        users_table_block = f"""
        <section class="panel" id="users-table-panel">
          <div class="panel-body users-table-panel-body">
            {_render_users_table_header(base_path, filters, pagination, available_filters, has_active_filters)}
            {users_table}
            {_render_users_table_footer(base_path, filters, pagination)}
          </div>
        </section>
        """

    content = f"""
        <section class="users-view" aria-label="Gestion de usuarios" data-users-index-url="{escape(build_url(base_path, '/usuarios'))}">
        {create_toggle_block}
        <div class="users-toast-region" id="users-toast-region" aria-live="polite" aria-atomic="true">
          {_status_toast_div(validation_error, "error")}
          {_status_toast_div(status_message, "success")}
        </div>
        {_render_create_password_modal(base_path)}
        {_render_password_modal()}
        <section class="panel" id="users-create-panel" hidden>
          <div class="panel-body">
            <h2>Nuevo usuario</h2>
            <form method="post" action="{escape(build_url(base_path, '/usuarios'))}" id="users-create-form">
              <div class="filters">
                <div><label for="nuevo_username">Usuario</label><input id="nuevo_username" name="username" type="text" required /></div>
                <div><label for="nuevo_nombre_completo">Nombre completo</label><input id="nuevo_nombre_completo" name="nombre_completo" type="text" required /></div>
                <div><label for="nuevo_email">Email</label><input id="nuevo_email" name="email" type="email" required /></div>
                <div><label for="nuevo_rol">Rol</label><select id="nuevo_rol" name="rol_principal">{_render_role_options(_role_options(), include_superadmin=False, capitalize_labels=True)}</select></div>
                <div><label for="nuevo_estado">Estado</label><select id="nuevo_estado" name="estado">{"".join(f'<option value="{escape(item)}"' + (' selected' if item == "deshabilitado" else '') + f'>{escape(item)}</option>' for item in _state_options_for_form())}</select></div>
              </div>
              <div class="filter-actions">
                <button type="button" id="open-create-password-modal" aria-controls="create-password-modal" aria-expanded="false">Crear usuario</button>
                <button type="button" id="cancel-users-create">Cancelar</button>
              </div>
            </form>
          </div>
        </section>
        {selected_user_block}
        {users_table_block}
      </section>
      <script>
        (function () {{
          const button = document.getElementById('toggle-users-create');
          const panel = document.getElementById('users-create-panel');
          const createForm = document.getElementById('users-create-form');
          const createPasswordModal = document.getElementById('create-password-modal');
          const createPasswordForm = document.getElementById('create-password-form');
          const createPasswordUserName = document.getElementById('create-password-modal-user-name');
          const createPasswordNewInput = document.getElementById('create-password-modal-new');
          const createPasswordConfirmInput = document.getElementById('create-password-modal-confirm');
          const createPasswordHiddenUsername = document.getElementById('create-modal-username');
          const createPasswordHiddenFullName = document.getElementById('create-modal-nombre-completo');
          const createPasswordHiddenEmail = document.getElementById('create-modal-email');
          const createPasswordHiddenRole = document.getElementById('create-modal-rol');
          const createPasswordHiddenState = document.getElementById('create-modal-estado');
          const createPasswordOpenButton = document.getElementById('open-create-password-modal');
          const createPanelCancelButton = document.getElementById('cancel-users-create');
          const filterForm = document.getElementById('users-filter-form');
          if (button && panel) {{
            function closeCreatePanel() {{
              panel.setAttribute('hidden', '');
              button.setAttribute('aria-expanded', 'false');
              if (createForm) {{
                createForm.reset();
              }}
              closeCreatePasswordModal();
            }}

            function openCreatePanel() {{
              panel.removeAttribute('hidden');
              button.setAttribute('aria-expanded', 'true');
              if (createForm) {{
                createForm.reset();
              }}
              closeCreatePasswordModal();
            }}

            panel.hidden = true;
            button.setAttribute('aria-expanded', 'false');

            button.addEventListener('click', function () {{
              const isHidden = panel.hasAttribute('hidden');
              if (isHidden) {{
                openCreatePanel();
              }} else {{
                closeCreatePanel();
              }}
            }});

            if (createPanelCancelButton) {{
              createPanelCancelButton.addEventListener('click', closeCreatePanel);
            }}
          }}

          const usersView = document.querySelector('.users-view');
          const toastRegion = document.getElementById('users-toast-region');
          const passwordModal = document.getElementById('password-change-modal');
          const passwordOpenButtons = document.querySelectorAll('[data-password-open]');
          const passwordModalForm = document.getElementById('password-change-form');
          const passwordModalUserName = document.getElementById('password-modal-user-name');
          const passwordModalNewInput = document.getElementById('password-modal-new');
          const passwordModalConfirmInput = document.getElementById('password-modal-confirm');
          const editForm = document.getElementById('users-edit-form');
          const editSaveButton = document.getElementById('users-edit-save');
          let activeDeleteToggle = null;
          let searchSubmitTimer = null;
          const toastLifetimeMs = 5000;

          function submitFilterForm() {{
            if (!filterForm) {{
              return;
            }}
            if (typeof filterForm.requestSubmit === 'function') {{
              filterForm.requestSubmit();
              return;
            }}
            filterForm.submit();
          }}

          function getDeleteToggle(userId) {{
            return document.getElementById('delete-toggle-' + userId);
          }}

          function updatePasswordMatchState(newInput, confirmInput) {{
            if (!newInput || !confirmInput) {{
              return;
            }}

            const newValue = newInput.value;
            const confirmValue = confirmInput.value;
            const hasValue = confirmValue.length > 0;
            const matches = hasValue && newValue === confirmValue;

            confirmInput.classList.toggle('is-password-match', matches);
            confirmInput.classList.toggle('is-password-mismatch', hasValue && !matches);
          }}

          function setEditSaveState() {{
            if (!editForm || !editSaveButton) {{
              return;
            }}

            const controls = Array.from(editForm.querySelectorAll('input[name], select[name], textarea[name]')).filter(function (control) {{
              return !control.disabled && control.type !== 'hidden' && control.type !== 'button' && control.type !== 'submit' && control.type !== 'reset';
            }});
            const hasChanges = controls.some(function (control) {{
              return control.value !== control.defaultValue;
            }});

            editSaveButton.disabled = !hasChanges;
            editSaveButton.setAttribute('aria-disabled', hasChanges ? 'false' : 'true');
          }}

          function setEditPasswordMatchState() {{
            updatePasswordMatchState(passwordModalNewInput, passwordModalConfirmInput);
          }}

          function setCreatePasswordMatchState() {{
            updatePasswordMatchState(createPasswordNewInput, createPasswordConfirmInput);
          }}

          function closeCreatePasswordModal() {{
            if (!createPasswordModal) {{
              return;
            }}

            createPasswordModal.hidden = true;
            createPasswordModal.setAttribute('aria-hidden', 'true');
            if (createPasswordNewInput) {{
              createPasswordNewInput.value = '';
            }}
            if (createPasswordConfirmInput) {{
              createPasswordConfirmInput.value = '';
              createPasswordConfirmInput.classList.remove('is-password-match', 'is-password-mismatch');
            }}
            if (createPasswordUserName) {{
              createPasswordUserName.textContent = '';
            }}
            if (createPasswordHiddenUsername) {{
              createPasswordHiddenUsername.value = '';
            }}
            if (createPasswordHiddenFullName) {{
              createPasswordHiddenFullName.value = '';
            }}
            if (createPasswordHiddenEmail) {{
              createPasswordHiddenEmail.value = '';
            }}
            if (createPasswordHiddenRole) {{
              createPasswordHiddenRole.value = '';
            }}
            if (createPasswordHiddenState) {{
              createPasswordHiddenState.value = '';
            }}
            if (createPasswordOpenButton) {{
              createPasswordOpenButton.setAttribute('aria-expanded', 'false');
            }}
          }}

          function openCreatePasswordModal() {{
            if (!createForm || !createPasswordModal || !createPasswordForm) {{
              return;
            }}

            if (typeof createForm.reportValidity === 'function' && !createForm.reportValidity()) {{
              return;
            }}

            const createFormData = new FormData(createForm);
            const username = String(createFormData.get('username') || '').trim();
            const fullName = String(createFormData.get('nombre_completo') || '').trim();
            const email = String(createFormData.get('email') || '').trim();
            const role = String(createFormData.get('rol_principal') || '').trim();
            const state = String(createFormData.get('estado') || '').trim();

            if (createPasswordHiddenUsername) {{
              createPasswordHiddenUsername.value = username;
            }}
            if (createPasswordHiddenFullName) {{
              createPasswordHiddenFullName.value = fullName;
            }}
            if (createPasswordHiddenEmail) {{
              createPasswordHiddenEmail.value = email;
            }}
            if (createPasswordHiddenRole) {{
              createPasswordHiddenRole.value = role;
            }}
            if (createPasswordHiddenState) {{
              createPasswordHiddenState.value = state;
            }}
            if (createPasswordUserName) {{
              createPasswordUserName.textContent = fullName || username;
            }}

            createPasswordModal.hidden = false;
            createPasswordModal.setAttribute('aria-hidden', 'false');
            if (createPasswordOpenButton) {{
              createPasswordOpenButton.setAttribute('aria-expanded', 'true');
            }}
            if (createPasswordNewInput) {{
              createPasswordNewInput.focus();
            }}
          }}

          function openPasswordModal(button) {{
            if (!passwordModal) {{
              return;
            }}

            if (button && passwordModalForm) {{
              passwordModalForm.action = button.dataset.passwordUrl || '';
            }}
            if (button && passwordModalUserName) {{
              passwordModalUserName.textContent = button.dataset.userName || '';
            }}
            passwordModal.hidden = false;
            passwordModal.setAttribute('aria-hidden', 'false');
            if (button) {{
              button.setAttribute('aria-expanded', 'true');
            }}
            if (passwordModalNewInput) {{
              passwordModalNewInput.focus();
            }}
          }}

          function closePasswordModal() {{
            if (!passwordModal) {{
              return;
            }}

            passwordModal.hidden = true;
            passwordModal.setAttribute('aria-hidden', 'true');
            passwordOpenButtons.forEach(function (button) {{
              button.setAttribute('aria-expanded', 'false');
            }});
            if (passwordModalNewInput) {{
              passwordModalNewInput.value = '';
            }}
            if (passwordModalConfirmInput) {{
              passwordModalConfirmInput.value = '';
              passwordModalConfirmInput.classList.remove('is-password-match', 'is-password-mismatch');
            }}
            if (passwordModalUserName) {{
              passwordModalUserName.textContent = '';
            }}
          }}

          function activateToast(toast, lifetimeMs) {{
            if (!toast) {{
              return;
            }}

            window.setTimeout(function () {{
              toast.classList.add('is-visible');
            }}, 10);

            window.setTimeout(function () {{
              toast.classList.remove('is-visible');
              window.setTimeout(function () {{
                if (toast.parentNode) {{
                  toast.parentNode.removeChild(toast);
                }}
              }}, 220);
            }}, lifetimeMs);
          }}

          function showToast(message, tone) {{
            if (!toastRegion) {{
              return;
            }}

            const toast = document.createElement('div');
            const normalizedTone = tone === 'warn' ? 'warning' : (tone || 'success');
            toast.className = 'users-toast users-toast-' + normalizedTone;
            toast.setAttribute('role', normalizedTone === 'error' ? 'alert' : 'status');
            toast.textContent = message;
            toastRegion.appendChild(toast);
            activateToast(toast, toastLifetimeMs);
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

          if (filterForm) {{
            const searchInput = filterForm.querySelector('[data-users-filter-search]');
            const roleSelect = filterForm.querySelector('[data-users-filter-role]');
            if (searchInput) {{
              searchInput.addEventListener('input', function () {{
                window.clearTimeout(searchSubmitTimer);
                searchSubmitTimer = window.setTimeout(submitFilterForm, 220);
              }});
              searchInput.addEventListener('keydown', function (event) {{
                if (event.key === 'Enter') {{
                  event.preventDefault();
                  submitFilterForm();
                }}
              }});
            }}
            if (roleSelect) {{
              roleSelect.addEventListener('change', submitFilterForm);
            }}
          }}

          if (toastRegion) {{
            toastRegion.querySelectorAll('[data-users-toast]').forEach(function (toast) {{
              activateToast(toast, toastLifetimeMs);
            }});
          }}

          if (editForm && editSaveButton) {{
            setEditSaveState();
            editForm.querySelectorAll('input[name], select[name], textarea[name]').forEach(function (control) {{
              if (control.disabled || control.type === 'hidden' || control.type === 'button' || control.type === 'submit' || control.type === 'reset') {{
                return;
              }}
              control.addEventListener('input', setEditSaveState);
              control.addEventListener('change', setEditSaveState);
            }});
          }}

          if (createPasswordOpenButton) {{
            createPasswordOpenButton.addEventListener('click', openCreatePasswordModal);
          }}
          if (createPasswordModal) {{
            createPasswordModal.querySelectorAll('[data-create-password-modal-close]').forEach(function (button) {{
              button.addEventListener('click', closeCreatePasswordModal);
            }});
          }}
          if (createPasswordNewInput && createPasswordConfirmInput) {{
            createPasswordNewInput.addEventListener('input', setCreatePasswordMatchState);
            createPasswordConfirmInput.addEventListener('input', setCreatePasswordMatchState);
          }}

          passwordOpenButtons.forEach(function (button) {{
            button.addEventListener('click', function () {{
              openPasswordModal(button);
            }});
          }});
          if (passwordModal) {{
            passwordModal.querySelectorAll('[data-password-modal-close]').forEach(function (button) {{
              button.addEventListener('click', closePasswordModal);
            }});
          }}
          if (passwordModalNewInput && passwordModalConfirmInput) {{
            passwordModalNewInput.addEventListener('input', setEditPasswordMatchState);
            passwordModalConfirmInput.addEventListener('input', setEditPasswordMatchState);
          }}
          document.addEventListener('keydown', function (event) {{
            if (event.key === 'Escape' && createPasswordModal && !createPasswordModal.hidden) {{
              closeCreatePasswordModal();
              return;
            }}
            if (event.key === 'Escape' && passwordModal && !passwordModal.hidden) {{
              closePasswordModal();
            }}
          }});

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


def _status_toast_div(message: str | None, tone: str = "success") -> str:
    if message is None:
        return ""
    toast_tone = "warning" if tone == "warn" else tone
    role = "alert" if toast_tone == "error" else "status"
    return f'<div class="users-toast users-toast-{escape(toast_tone)}" data-users-toast role="{role}" aria-atomic="true">{escape(message)}</div>'


def _render_create_password_modal(base_path: str) -> str:
    return f"""
        <div class="users-password-modal users-password-modal--create" id="create-password-modal" hidden aria-hidden="true">
          <div class="users-password-modal__backdrop" data-create-password-modal-close></div>
          <div class="users-password-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="create-password-title">
            <h3 id="create-password-title">Crear usuario</h3>
            <p class="muted users-password-modal__copy">Usuario: <strong id="create-password-modal-user-name"></strong></p>
            <form method="post" action="{escape(build_url(base_path, '/usuarios'))}" id="create-password-form">
              <input type="hidden" id="create-modal-username" name="username" />
              <input type="hidden" id="create-modal-nombre-completo" name="nombre_completo" />
              <input type="hidden" id="create-modal-email" name="email" />
              <input type="hidden" id="create-modal-rol" name="rol_principal" />
              <input type="hidden" id="create-modal-estado" name="estado" />
              <input type="password" id="create-password-modal-new" name="nueva_contrasena" minlength="8" autocomplete="new-password" placeholder="Nueva contrasena" required />
              <input type="password" id="create-password-modal-confirm" name="confirmar_contrasena" minlength="8" autocomplete="new-password" placeholder="Confirmar contrasena" required />
              <div class="users-password-modal__actions">
                <button type="submit" class="users-password-modal__action users-password-modal__action--save" aria-label="Crear usuario" data-tooltip="Crear usuario">Crear</button>
                <button type="button" class="users-password-modal__action users-password-modal__action--cancel" data-create-password-modal-close aria-label="Cancelar alta de usuario" data-tooltip="Cancelar alta de usuario">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
    """


def _render_password_modal() -> str:
    return """
        <div class="users-password-modal" id="password-change-modal" hidden aria-hidden="true">
          <div class="users-password-modal__backdrop" data-password-modal-close></div>
          <div class="users-password-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="password-change-title">
            <h3 id="password-change-title">Cambiar contrasena</h3>
            <p class="muted users-password-modal__copy">Usuario: <strong id="password-modal-user-name"></strong></p>
            <form method="post" action="" id="password-change-form">
              <input type="password" id="password-modal-new" name="nueva_contrasena" minlength="8" autocomplete="new-password" placeholder="Nueva contrasena" required />
              <input type="password" id="password-modal-confirm" name="confirmar_contrasena" minlength="8" autocomplete="new-password" placeholder="Confirmar contrasena" required />
              <div class="users-password-modal__actions">
                <button type="submit" class="users-password-modal__action users-password-modal__action--save" aria-label="Modificar contrasena" data-tooltip="Modificar contrasena">Modificar</button>
                <button type="button" class="users-password-modal__action users-password-modal__action--cancel" data-password-modal-close aria-label="Cancelar cambio de contrasena" data-tooltip="Cancelar cambio de contrasena">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
    """


def _render_users_table_header(
    base_path: str,
    filters: dict[str, object],
    pagination: dict[str, object],
    available_filters: dict[str, list[str]],
    has_active_filters: bool,
) -> str:
    return f"""
      <div class="users-table-header__shell">
        {_render_users_filter_bar(base_path, filters, available_filters, pagination, has_active_filters)}
      </div>
    """


def _render_users_table_footer(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    return f"""
      <div class="users-table-footer">
        <div class="users-table-summary">
          <strong>Pagina {pagination["pagina_actual"]} de {pagination["total_paginas"]}</strong>
          <span class="muted">Mostrando {pagination["resultado_desde"]}-{pagination["resultado_hasta"]} de {pagination["total_resultados"]}</span>
        </div>
        {_render_pagination(base_path, filters, pagination)}
      </div>
    """


def _render_users_filter_bar(
    base_path: str,
    filters: dict[str, object],
    available_filters: dict[str, list[str]],
    pagination: dict[str, object],
    has_active_filters: bool,
) -> str:
    search_value = escape(str(filters.get("busqueda", "")))
    role_value = str(filters.get("rol", ""))
    role_options = "".join(
        f'<option value="{escape(item)}"' + (" selected" if role_value == item else "") + f'>{escape(item)}</option>'
        for item in available_filters["roles"]
    )
    clear_link = ""
    if has_active_filters:
        clear_link = render_icon_button(
            label="Limpiar filtros",
            icon_svg=render_inline_svg_icon("cancel"),
            href=build_url(base_path, "/usuarios"),
            css_class="users-filter-clear",
            tooltip="Limpiar filtros",
            aria_label="Limpiar filtros",
        )
    return f"""
      <form id="users-filter-form" class="users-filter-bar" method="get" action="{escape(build_url(base_path, '/usuarios'))}" role="search">
        <input type="hidden" name="page" value="1" />
        <input type="hidden" name="page_size" value="{escape(str(pagination["tamano_pagina"]))}" />
        <div class="users-filter-search">
          <label class="sr-only" for="busqueda">Busqueda</label>
          <span class="users-filter-icon" aria-hidden="true">{render_inline_svg_icon("search")}</span>
          <input
            id="busqueda"
            name="busqueda"
            type="text"
            value="{search_value}"
            placeholder="Nombre, apellidos, email o identificador"
            aria-label="Buscar usuario"
            data-users-filter-search
          />
        </div>
        <div class="users-filter-role">
          <label class="sr-only" for="rol">Rol</label>
          <span class="users-filter-prefix" aria-hidden="true">Rol:</span>
          <select id="rol" name="rol" aria-label="Filtrar por rol" data-users-filter-role>
            <option value="">Rol: todos</option>
            {role_options}
          </select>
        </div>
        {clear_link}
      </form>
    """


def _render_users_table(user_rows: list[str]) -> str:
    if not user_rows:
        return '<section class="note">Todavia no hay usuarios que mostrar con los filtros activos.</section>'

    headers = ["Usuario", "Nombre completo", "Email", "Rol", "Estado", "Ultimo acceso"]
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
    login_name = _user_login_name(selected_user)
    is_superadmin = _is_superadmin_user(selected_user)
    if is_superadmin:
        return f"""
        <h2>Detalle y edicion</h2>
        <p><strong>Usuario seleccionado:</strong> {escape(login_name)}</p>
        <p><strong>Estado actual:</strong> {render_state_badge(selected_user["estado"])}</p>
        <p><strong>Ultimo acceso:</strong> {escape(_format_user_datetime(selected_user["ultimo_acceso"]))}</p>
        <section class="note note-warning">
          La cuenta superadmin no puede editarse, deshabilitarse ni eliminarse desde la interfaz.
          Solo se gestiona mediante el fichero <code>.env</code>.
        </section>
        <p class="muted">Fecha de alta: {escape(_format_user_datetime(selected_user["fecha_alta"]))}</p>
        <h3>Historial de cambios</h3>
        {history_table}
    """
    role_options = "".join(
        f'<option value="{escape(role)}"' + (" selected" if selected_user["rol_principal"] == role else "") + f'>{escape(role.title())}</option>'
        for role in _form_role_options(_role_options())
    )
    state_options = "".join(
        f'<option value="{escape(state)}"' + (" selected" if selected_user["estado"] == state else "") + f'>{escape(state)}</option>'
        for state in _state_options_for_form(str(selected_user["estado"]))
    )
    return f"""
        <h2>Detalle y edicion</h2>
        <p><strong>Usuario seleccionado:</strong> {escape(str(selected_user["nombre_completo"]))}</p>
        <p><strong>Estado actual:</strong> {render_state_badge(selected_user["estado"])}</p>
        <p><strong>Ultimo acceso:</strong> {escape(_format_user_datetime(selected_user["ultimo_acceso"]))}</p>
        <form method="post" action="{escape(build_url(base_path, f"/usuarios/{selected_user['id']}"))}" id="users-edit-form">
          <div class="filters">
            <div><label for="editar_username">Usuario</label><input id="editar_username" name="username" type="text" value="{escape(str(selected_user.get("username") or selected_user["email"]))}" /></div>
            <div><label for="editar_nombre">Nombre</label><input id="editar_nombre" name="nombre" type="text" value="{escape(str(selected_user["nombre"]))}" required /></div>
            <div><label for="editar_apellidos">Apellidos</label><input id="editar_apellidos" name="apellidos" type="text" value="{escape(str(selected_user["apellidos"]))}" required /></div>
            <div><label for="editar_email">Email</label><input id="editar_email" name="email" type="email" value="{escape(str(selected_user["email"]))}" required /></div>
            <div><label for="editar_rol">Rol</label><select id="editar_rol" name="rol_principal">{role_options}</select></div>
            <div><label for="editar_estado">Estado</label><select id="editar_estado" name="estado">{state_options}</select></div>
          </div>
          <p class="muted">Fecha de alta: {escape(_format_user_datetime(selected_user["fecha_alta"]))}</p>
          <div class="users-edit-actions">
            <button type="submit" class="users-edit-action users-edit-action--save" id="users-edit-save" aria-label="Guardar cambios" data-tooltip="Guardar cambios" disabled aria-disabled="true">
              {render_inline_svg_icon("confirm")}
              <span class="users-edit-action__label">Guardar</span>
            </button>
            <a class="button-link users-edit-action users-edit-action--cancel" href="{escape(build_url(base_path, '/usuarios'))}" aria-label="Cancelar edición" data-tooltip="Cancelar edición">
              {render_inline_svg_icon("cancel")}
              <span class="users-edit-action__label">Cancelar</span>
            </a>
            <button type="button" class="users-edit-action users-edit-action--password" id="open-password-modal" data-password-open data-password-url="{escape(build_url(base_path, f"/usuarios/{selected_user['id']}/contrasena"))}" data-user-name="{escape(str(selected_user['nombre_completo']))}" aria-controls="password-change-modal" aria-expanded="false" aria-label="Cambiar contraseña" data-tooltip="Cambiar contraseña">
              {render_inline_svg_icon("key")}
              <span class="users-edit-action__label">Contrasena</span>
            </button>
          </div>
        </form>
        <h3>Historial de cambios</h3>
        {history_table}
    """


def _render_user_row(base_path: str, user: dict[str, object]) -> str:
    actions = _build_action_controls(base_path, user)
    login_name = _user_login_name(user)
    return (
        f'<tr id="user-row-{escape(str(user["id"]))}">'
        f'<td data-label="Usuario">{escape(login_name)}</td>'
        f'<td data-label="Nombre completo">{escape(_display_optional_text(user["nombre_completo"]))}</td>'
        f'<td data-label="Email">{escape(_display_optional_text(user["email"]))}</td>'
        f'<td data-label="Rol">{render_role_badge(user["rol_principal"])}</td>'
        f'<td data-label="Estado">{render_state_badge(user["estado"])}</td>'
        f'<td data-label="Ultimo acceso">{escape(_format_user_datetime(user["ultimo_acceso"]))}</td>'
        f'<td data-label="ACCIONES"><div class="actions-cell">{"".join(actions)}</div></td>'
        "</tr>"
    )


def _build_action_controls(base_path: str, user: dict[str, object]) -> list[str]:
    if _is_superadmin_user(user):
        return []
    actions: list[str] = []
    actions.append(
        render_icon_button(
            label="Modificar",
            icon_svg=render_inline_svg_icon("edit"),
            href=build_url(base_path, f"/usuarios/{user['id']}"),
            css_class="btn-icon--edit",
            tooltip="Modificar",
            aria_label=f"Modificar usuario {_user_login_name(user)}",
        )
    )
    actions.append(_password_modal_trigger(base_path, user))
    if user["estado"] == "activo":
        actions.append(_action_form(base_path, user["id"], "Deshabilitar", "deshabilitado"))
    else:
        actions.append(_action_form(base_path, user["id"], "Reactivar", "activo"))
    actions.append(_delete_toggle_fragment(base_path, user))
    return actions


def _is_superadmin_user(user: dict[str, object]) -> bool:
    return str(user.get("rol_principal") or "").strip().lower() == "superadmin"


def _display_optional_text(value: object | None) -> str:
    text = str(value or "").strip()
    return text if text else "-"


def _user_login_name(user: dict[str, object]) -> str:
    username = str(user.get("username") or "").strip()
    if username:
        return username
    email = str(user.get("email") or "").strip()
    if email:
        return email
    return str(user.get("id") or "")


def _password_modal_trigger(base_path: str, user: dict[str, object]) -> str:
    raw_user_id = str(user["id"])
    user_name = escape(str(user["nombre_completo"]))
    password_url = escape(build_url(base_path, f"/usuarios/{raw_user_id}/contrasena"))
    return f"""
      <button
        type="button"
        class="btn-icon btn-icon--password"
        data-password-open
        data-password-url="{password_url}"
        data-user-name="{user_name}"
        aria-controls="password-change-modal"
        aria-expanded="false"
        aria-label="Cambiar contrasena"
        data-tooltip="Cambiar contrasena"
      >{render_inline_svg_icon("key")}</button>
    """


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
    button_class = "btn-icon--ban" if state == "deshabilitado" else "btn-icon--restore"
    icon_name = "ban" if state == "deshabilitado" else "restore"
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
    return ["activo", "deshabilitado", "bloqueado"]


def _state_options_for_form(current_state: str | None = None) -> list[str]:
    states = ["activo", "deshabilitado"]
    if current_state == "bloqueado":
        states.append("bloqueado")
    return states


def _role_options() -> list[str]:
    return ["administrador", "superadmin", "manager", "colaborador", "invitado"]


def _form_role_options(roles: list[str]) -> list[str]:
    return [role for role in roles if role != "superadmin"]


def _render_role_options(roles: list[str], *, include_superadmin: bool = False, capitalize_labels: bool = False) -> str:
    visible_roles = roles if include_superadmin else [role for role in roles if role != "superadmin"]
    return "".join(
        f'<option value="{escape(role)}">{escape(role.title() if capitalize_labels else role)}</option>'
        for role in visible_roles
    )


def _format_user_datetime(value: object | None) -> str:
    formatted = format_iso_datetime(value)
    if formatted is None:
        return "Nunca"
    return formatted


def _render_pagination(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    hidden_fields = "".join(f'<input type="hidden" name="{escape(str(key))}" value="{escape(str(value))}" />' for key, value in filters.items())
    prev_link = ""
    if pagination["pagina_anterior"] is not None:
        prev_link = render_icon_button(
            label="Pagina anterior",
            icon_svg=render_inline_svg_icon("chevron-left"),
            href=_page_url(base_path, filters, int(pagination["pagina_anterior"]), int(pagination["tamano_pagina"])),
            css_class="pagination-action pagination-action--prev",
            tooltip="Pagina anterior",
            aria_label="Pagina anterior",
        )
    next_link = ""
    if pagination["pagina_siguiente"] is not None:
        next_link = render_icon_button(
            label="Pagina siguiente",
            icon_svg=render_inline_svg_icon("chevron-right"),
            href=_page_url(base_path, filters, int(pagination["pagina_siguiente"]), int(pagination["tamano_pagina"])),
            css_class="pagination-action pagination-action--next",
            tooltip="Pagina siguiente",
            aria_label="Pagina siguiente",
        )
    page_size_options = "".join(
        f'<option value="{value}"' + (" selected" if int(pagination["tamano_pagina"]) == value else "") + f">{value}</option>"
        for value in (5, 10, 25, 50)
    )
    page_jump = ""
    if int(pagination["total_paginas"]) > 1:
        page_jump = f"""
          <label for="users-page">Ir a la pagina</label>
          <input id="users-page" name="page" type="number" min="1" max="{pagination["total_paginas"]}" value="{pagination["pagina_actual"]}" />
          <button type="submit">Ir</button>
        """
    return f'''
      <div class="pagination-bar">
        <form class="pagination-jump" method="get" action="{escape(build_url(base_path, "/usuarios"))}">
          {hidden_fields}
          <label for="users-page-size">Resultados por pagina</label>
          <select id="users-page-size" name="page_size" onchange="this.form.submit()">{page_size_options}</select>
          {page_jump}
        </form>
        <div class="pagination-actions">{prev_link}{next_link}</div>
      </div>
    '''


def _page_url(base_path: str, filters: dict[str, object], page: int, page_size: int) -> str:
    query = urlencode({**{key: value for key, value in filters.items() if value not in (None, "")}, "page": page, "page_size": page_size})
    return f"{build_url(base_path, '/usuarios')}" + (f"?{query}" if query else "")
