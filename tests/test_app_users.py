from __future__ import annotations

import os
import unittest
from urllib.parse import urlencode
from unittest.mock import patch

import psycopg2

from licican.auth.config import get_auth_settings
from tests.shared.app_http import invoke_app, session_cookie as _session_cookie
from tests.shared.users_db import SeededUsersState, fake_users_connect


class ApplicationUsersTests(unittest.TestCase):
    def setUp(self) -> None:
        get_auth_settings.cache_clear()
        self._env_patch = patch.dict(os.environ, {"DB_PASSWORD": "test-password"}, clear=False)
        self._env_patch.start()

    def tearDown(self) -> None:
        self._env_patch.stop()
        get_auth_settings.cache_clear()

    def _patch_users_db(self, state: SeededUsersState | None = None):
        current_state = state or SeededUsersState.seed()
        return patch("licican.users.psycopg2.connect", side_effect=lambda *args, **kwargs: fake_users_connect(current_state))

    def test_users_page_renders_summary_table_and_navigation_for_admin(self) -> None:
        with self._patch_users_db():
            status, headers, body = invoke_app("/usuarios")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Gestion de usuarios", html)
        self.assertNotIn("Usuarios totales", html)
        self.assertNotIn("Gestion administrativa de cuentas", html)
        self.assertIn("<th>Usuario</th>", html)
        self.assertIn("<th>Rol</th>", html)
        self.assertIn("badge-rol--administrador", html)
        self.assertIn("badge-rol--gestor", html)
        self.assertIn(">Manager<", html)
        self.assertIn("badge-rol--colaborador", html)
        self.assertIn("badge-rol--usuario", html)
        self.assertIn("Ana Lopez", html)
        self.assertIn("ana.lopez@licican.local", html)
        self.assertIn("02-04-2026 08:10", html)
        self.assertIn('<th style="width: 120px; text-align: right;">ACCIONES</th>', html)
        self.assertIn('id="toggle-users-create"', html)
        self.assertIn("Nuevo usuario", html)
        self.assertIn('id="users-create-panel" hidden', html)
        self.assertIn('id="users-table-panel"', html)
        self.assertNotIn('id="users-filters-panel"', html)
        self.assertIn('id="users-filter-form"', html)
        self.assertIn('class="table-wrap users-table-wrap"', html)
        self.assertIn('class="actions-cell"', html)
        self.assertIn('class="btn-icon btn-icon--edit"', html)
        self.assertIn('class="btn-icon btn-icon--ban"', html)
        self.assertIn('class="btn-icon btn-icon--restore"', html)
        self.assertIn('class="btn-icon btn-icon--delete delete-toggle-trigger"', html)
        self.assertIn('data-tooltip="Modificar"', html)
        self.assertIn('data-tooltip="Deshabilitar"', html)
        self.assertIn('data-tooltip="Reactivar"', html)
        self.assertIn('data-tooltip="Eliminar"', html)
        self.assertNotIn("Cambiar contrasena", html)
        self.assertIn('class="btn-icon btn-icon--delete delete-toggle-confirm"', html)
        self.assertIn('data-tooltip="Eliminar"', html)
        self.assertIn("data-delete-toggle", html)
        self.assertIn("showConfirm(this.dataset.userId, this.dataset.userName)", html)
        self.assertIn("deleteUser(this.closest('.delete-toggle').dataset.userId)", html)
        self.assertIn("hideConfirm(this.closest('.delete-toggle').dataset.userId)", html)
        self.assertNotIn("confirm(", html)
        self.assertNotIn("Reenviar invitacion", html)
        self.assertNotIn("Reiniciar acceso", html)
        self.assertNotIn("Baja logica", html)
        self.assertNotIn('id="users-selected-panel"', html)
        self.assertIn('>Rol<', html)
        self.assertIn('href="/licican/usuarios"', html)
        self.assertIn('class="nav-link active" href="/licican/usuarios"', html)
        self.assertIn("Cerrar sesión", html)

        create_panel_index = html.index('id="users-create-panel"')
        table_panel_index = html.index('id="users-table-panel"')
        toggle_button_index = html.index('id="toggle-users-create"')
        self.assertLess(toggle_button_index, create_panel_index)
        self.assertLess(create_panel_index, table_panel_index)

        create_panel_html = html[create_panel_index:table_panel_index]
        self.assertNotIn('value="superadmin"', create_panel_html)
        self.assertIn('value="administrador"', create_panel_html)
        self.assertIn('value="manager"', create_panel_html)
        self.assertIn('value="colaborador"', create_panel_html)
        self.assertIn('value="invitado"', create_panel_html)

        table_panel_html = html[table_panel_index:]
        self.assertIn('name="busqueda"', table_panel_html)
        self.assertIn('name="rol"', table_panel_html)
        self.assertIn('data-users-filter-search', table_panel_html)
        self.assertIn('data-users-filter-role', table_panel_html)
        self.assertNotIn('name="superficie"', table_panel_html)
        self.assertNotIn('Area / modulo / superficie', table_panel_html)
        self.assertNotIn('Aplicar filtros', table_panel_html)
        self.assertNotIn('Limpiar filtros</a>', table_panel_html)
        self.assertIn("panel.hidden = true", html)

    def test_users_page_shows_inline_clear_filter_action_only_when_filters_exist(self) -> None:
        with self._patch_users_db():
            status_without_filters, _, html_without_filters = invoke_app("/usuarios")
            status_with_filters, _, html_with_filters = invoke_app("/usuarios", query_string="busqueda=ana&rol=administrador")

        self.assertEqual("200 OK", status_without_filters)
        self.assertEqual("200 OK", status_with_filters)
        self.assertNotIn('data-tooltip="Limpiar filtros"', html_without_filters.decode("utf-8"))
        self.assertIn('data-tooltip="Limpiar filtros"', html_with_filters.decode("utf-8"))
        self.assertIn('data-users-filter-search', html_with_filters.decode("utf-8"))
        self.assertIn('data-users-filter-role', html_with_filters.decode("utf-8"))

    def test_users_page_shows_floating_success_toast_from_query_message(self) -> None:
        with self._patch_users_db():
            status, _, body = invoke_app("/usuarios", query_string="mensaje=Usuario+actualizado")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertIn('id="users-toast-region"', html)
        self.assertIn('data-users-toast', html)
        self.assertIn('users-toast-success', html)
        self.assertIn('Usuario actualizado', html)
        self.assertIn('toastLifetimeMs = 5000', html)
        self.assertNotIn('note-warning', html)

    def test_users_page_shows_floating_error_toast_for_validation_errors(self) -> None:
        form_data = urlencode(
            {
                "nombre": "Eva",
                "apellidos": "Santos",
                "email": "ana.lopez@licican.local",
                "rol_principal": "manager",
                "estado": "activo",
            }
        )
        with self._patch_users_db():
            status, _, body = invoke_app("/usuarios", method="POST", body=form_data)

        html = body.decode("utf-8")
        self.assertEqual("400 Bad Request", status)
        self.assertIn('id="users-toast-region"', html)
        self.assertIn('users-toast-error', html)
        self.assertIn('El email no puede duplicarse entre usuarios.', html)
        self.assertNotIn('note-warning', html)

    def test_users_page_hides_actions_and_personal_data_for_superadmin(self) -> None:
        state = SeededUsersState.seed()
        state.users["superadmin"] = {
            "id": "superadmin",
            "nombre": "",
            "apellidos": "",
            "email": "",
            "rol_principal": "superadmin",
            "estado": "activo",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "failed_login_attempts": 0,
            "bloqueado_hasta": None,
            "username": "superadmin",
            "password_hash": "hash-admin",
        }
        state.history["superadmin"] = []

        with self._patch_users_db(state), patch.dict(os.environ, {"LOGIN_SUPERADMIN_ENABLED": "true"}, clear=False):
            get_auth_settings.cache_clear()
            status, headers, body = invoke_app("/usuarios")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="user-row-superadmin"', html)
        self.assertLess(html.index('id="user-row-superadmin"'), html.index('id="user-row-usr-001"'))
        admin_row_start = html.index('id="user-row-superadmin"')
        admin_row_html = html[admin_row_start:html.index("</tr>", admin_row_start)]
        self.assertIn("badge-rol--superadmin", admin_row_html)
        self.assertIn('data-label="Usuario">superadmin</td>', admin_row_html)
        self.assertIn('data-label="Nombre completo">-</td>', admin_row_html)
        self.assertIn('data-label="Email">-</td>', admin_row_html)
        self.assertNotIn('data-tooltip="Modificar"', admin_row_html)
        self.assertNotIn('data-tooltip="Deshabilitar"', admin_row_html)
        self.assertNotIn('data-tooltip="Reactivar"', admin_row_html)
        self.assertNotIn('data-tooltip="Eliminar"', admin_row_html)

    def test_superadmin_detail_page_hides_edit_form_and_actions(self) -> None:
        state = SeededUsersState.seed()
        state.users["superadmin"] = {
            "id": "superadmin",
            "nombre": "",
            "apellidos": "",
            "email": "",
            "rol_principal": "superadmin",
            "estado": "activo",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "failed_login_attempts": 0,
            "bloqueado_hasta": None,
            "username": "superadmin",
            "password_hash": "hash-admin",
        }
        state.history["superadmin"] = []

        with self._patch_users_db(state), patch.dict(os.environ, {"LOGIN_SUPERADMIN_ENABLED": "true"}, clear=False):
            get_auth_settings.cache_clear()
            status, headers, body = invoke_app("/usuarios/superadmin")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("La cuenta superadmin no puede editarse, deshabilitarse ni eliminarse desde la interfaz.", html)
        self.assertIn('Usuario seleccionado:</strong> superadmin', html)
        self.assertNotIn('id="editar_username"', html)
        self.assertNotIn('id="editar_nombre"', html)
        self.assertNotIn('id="editar_email"', html)
        self.assertNotIn('data-tooltip="Modificar"', html)
        self.assertNotIn('data-tooltip="Deshabilitar"', html)
        self.assertNotIn('data-tooltip="Reactivar"', html)
        self.assertNotIn('data-tooltip="Eliminar"', html)

    def test_users_page_denied_to_reader_role(self) -> None:
        invited_cookie = _session_cookie(role="invitado", username="invitado-1", nombre_completo="Invitado Demo")
        with self._patch_users_db(), patch.dict(os.environ, {"LOGIN_AUTOMATICO": "false"}, clear=False):
            status, headers, body = invoke_app("/usuarios", cookies=invited_cookie)

        self.assertEqual("403 Forbidden", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", body.decode("utf-8"))

    def test_users_page_shows_database_unavailable_message_when_postgresql_fails(self) -> None:
        with patch("licican.users.psycopg2.connect", side_effect=psycopg2.OperationalError("db down")):
            status, headers, body = invoke_app("/usuarios")

        html = body.decode("utf-8")
        self.assertEqual("503 Service Unavailable", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Usuarios temporalmente no disponibles", html)
        self.assertIn("El modulo de gestion de usuarios requiere acceso a la base de datos configurada.", html)
        self.assertIn("Base de datos de usuarios no disponible", html)
        self.assertIn("No se pudo consultar PostgreSQL para gestionar usuarios.", html)
        self.assertIn("La gestion de usuarios depende de PostgreSQL y no puede renderizarse mientras la conexion no responda.", html)

    def test_user_creation_route_redirects_and_persists_account(self) -> None:
        state = SeededUsersState.seed()
        form_data = urlencode(
            {
                "nombre": "Eva",
                "apellidos": "Santos",
                "email": "eva.santos@licican.local",
                "rol_principal": "manager",
                "estado": "deshabilitado",
            }
        )
        with self._patch_users_db(state):
            status, headers, _ = invoke_app("/usuarios", method="POST", body=form_data)
            page_status, _, page_body = invoke_app("/usuarios")

        html = page_body.decode("utf-8")
        self.assertEqual("303 See Other", status)
        self.assertEqual("/licican/usuarios?mensaje=Usuario+creado+y+registrado", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("Eva Santos", html)
        self.assertIn("eva.santos@licican.local", html)
        self.assertIn("usr-005", html)
        self.assertIn("deshabilitado", html)

    def test_user_detail_page_shows_selected_user_history(self) -> None:
        with self._patch_users_db():
            status, headers, body = invoke_app("/usuarios/usr-003")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Detalle y edicion", html)
        self.assertIn("Laura Gonzalez", html)
        self.assertIn('id="editar_username"', html)
        self.assertIn('name="username"', html)
        self.assertNotIn('id="toggle-users-create"', html)
        username_index = html.index('id="editar_username"')
        nombre_index = html.index('id="editar_nombre"')
        self.assertLess(username_index, nombre_index)
        self.assertIn('id="users-selected-panel"', html)
        self.assertNotIn('id="users-table-panel"', html)
        self.assertIn("Nueva contrasena", html)
        self.assertIn("Confirmar nueva contrasena", html)
        self.assertIn('href="#editar_nueva_contrasena"', html)
        self.assertIn(">Cancelar</a>", html)
        self.assertIn('class="btn-icon btn-icon--edit"', html)
        self.assertIn('class="btn-icon btn-icon--restore"', html)
        self.assertIn('class="btn-icon btn-icon--delete delete-toggle-trigger"', html)
        self.assertIn('class="btn-icon btn-icon--delete delete-toggle-confirm"', html)
        self.assertIn('data-tooltip="Modificar"', html)
        self.assertIn('data-tooltip="Reactivar"', html)
        self.assertIn('data-tooltip="Eliminar"', html)
        self.assertIn('data-tooltip="Eliminar"', html)
        self.assertIn("data-delete-toggle", html)
        self.assertIn("showConfirm(this.dataset.userId, this.dataset.userName)", html)
        self.assertIn("deleteUser(this.closest('.delete-toggle').dataset.userId)", html)
        self.assertIn("hideConfirm(this.closest('.delete-toggle').dataset.userId)", html)
        self.assertNotIn("confirm(", html)
        self.assertIn("Fecha de alta: 02-04-2026 08:30", html)
        self.assertIn("02-04-2026 08:30", html)
        self.assertIn("Historial de cambios", html)

        edit_role_select_start = html.index('id="editar_rol"')
        edit_role_select_end = html.index('</select>', edit_role_select_start)
        edit_role_select_html = html[edit_role_select_start:edit_role_select_end]
        self.assertNotIn('value="superadmin"', edit_role_select_html)
        self.assertIn('value="administrador"', edit_role_select_html)
        self.assertIn('value="manager"', edit_role_select_html)
        self.assertIn('value="colaborador"', edit_role_select_html)
        self.assertIn('value="invitado"', edit_role_select_html)

    def test_user_update_route_redirects_back_to_list_after_save(self) -> None:
        state = SeededUsersState.seed()
        form_data = urlencode(
            {
                "nombre": "Laura",
                "apellidos": "Gonzalez",
                "email": "laura.gonzalez@licican.local",
                "rol_principal": "colaborador",
                "estado": "activo",
                "nueva_contrasena": "clave-segura-123",
                "confirmar_contrasena": "clave-segura-123",
            }
        )

        with self._patch_users_db(state):
            status, headers, _ = invoke_app("/usuarios/usr-003", method="POST", body=form_data)
            page_status, _, page_body = invoke_app("/usuarios")

        html = page_body.decode("utf-8")
        self.assertEqual("303 See Other", status)
        self.assertEqual("/licican/usuarios?mensaje=Usuario+actualizado", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn('id="users-table-panel"', html)
        self.assertNotIn('id="users-selected-panel"', html)
        self.assertIn("Laura Gonzalez", html)

    def test_user_delete_route_redirects_back_to_list_after_delete(self) -> None:
        state = SeededUsersState.seed()

        with self._patch_users_db(state):
            status, headers, _ = invoke_app("/usuarios/usr-004/borrar", method="POST")
            page_status, _, page_body = invoke_app("/usuarios")

        html = page_body.decode("utf-8")
        self.assertEqual("303 See Other", status)
        self.assertEqual("/licican/usuarios?mensaje=Usuario+eliminado", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertNotIn("Mario Perez", html)
        self.assertNotIn("usr-004", html)

    def test_user_state_route_redirects_back_to_list_after_activation(self) -> None:
        state = SeededUsersState.seed()
        form_data = urlencode({"estado": "activo"})

        with self._patch_users_db(state):
            status, headers, _ = invoke_app("/usuarios/usr-003/estado", method="POST", body=form_data)
            page_status, _, page_body = invoke_app("/usuarios")

        html = page_body.decode("utf-8")
        self.assertEqual("303 See Other", status)
        self.assertEqual("/licican/usuarios?mensaje=Estado+de+usuario+actualizado", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn('id="users-table-panel"', html)
        self.assertNotIn('id="users-selected-panel"', html)
