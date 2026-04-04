from __future__ import annotations

import os
import unittest
from urllib.parse import urlencode
from unittest.mock import patch

from tests.shared.app_http import invoke_app, session_cookie as _session_cookie
from tests.shared.users_db import SeededUsersState, fake_users_connect


class ApplicationUsersTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_patch = patch.dict(os.environ, {"DB_PASSWORD": "test-password"}, clear=False)
        self._env_patch.start()

    def tearDown(self) -> None:
        self._env_patch.stop()

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
        self.assertIn('value="superadmin"', html)
        self.assertIn("badge-rol--administrador", html)
        self.assertIn("badge-rol--gestor", html)
        self.assertIn("badge-rol--colaborador", html)
        self.assertIn("badge-rol--usuario", html)
        self.assertIn("Ana Lopez", html)
        self.assertIn("ana.lopez@licican.local", html)
        self.assertIn("02-04-2026 08:10", html)
        self.assertIn('<th style="width: 120px; text-align: right;">ACCIONES</th>', html)
        self.assertIn('id="toggle-users-create"', html)
        self.assertIn("Nuevo usuario", html)
        self.assertIn('id="users-create-panel" hidden', html)
        self.assertIn('id="users-filters-panel"', html)
        self.assertIn('id="users-table-panel"', html)
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
        self.assertIn('href="/licican/usuarios"', html)
        self.assertIn('class="nav-link active" href="/licican/usuarios"', html)
        self.assertIn("Cerrar sesión", html)

        create_panel_index = html.index('id="users-create-panel"')
        filters_panel_index = html.index('id="users-filters-panel"')
        table_panel_index = html.index('id="users-table-panel"')
        toggle_button_index = html.index('id="toggle-users-create"')
        self.assertLess(toggle_button_index, create_panel_index)
        self.assertLess(create_panel_index, filters_panel_index)

        filters_panel_html = html[filters_panel_index:table_panel_index]
        self.assertIn('name="busqueda"', filters_panel_html)
        self.assertIn('name="rol"', filters_panel_html)
        self.assertNotIn('name="estado"', filters_panel_html)
        self.assertNotIn('name="superficie"', filters_panel_html)
        self.assertNotIn('Area / modulo / superficie', filters_panel_html)
        self.assertIn("panel.hidden = true", html)

    def test_users_page_hides_actions_and_personal_data_for_superadmin(self) -> None:
        state = SeededUsersState.seed()
        state.users["admin"] = {
            "id": "admin",
            "nombre": "",
            "apellidos": "",
            "email": "",
            "rol_principal": "superadmin",
            "estado": "activo",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "invitacion_pendiente": False,
            "username": "admin",
            "password_hash": "hash-admin",
        }
        state.history["admin"] = []

        with self._patch_users_db(state):
            status, headers, body = invoke_app("/usuarios")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="user-row-admin"', html)
        admin_row_start = html.index('id="user-row-admin"')
        admin_row_html = html[admin_row_start:html.index("</tr>", admin_row_start)]
        self.assertIn("badge-rol--superadmin", admin_row_html)
        self.assertIn('data-label="Usuario">admin</td>', admin_row_html)
        self.assertIn('data-label="Nombre completo">-</td>', admin_row_html)
        self.assertIn('data-label="Email">-</td>', admin_row_html)
        self.assertNotIn('data-tooltip="Modificar"', admin_row_html)
        self.assertNotIn('data-tooltip="Deshabilitar"', admin_row_html)
        self.assertNotIn('data-tooltip="Reactivar"', admin_row_html)
        self.assertNotIn('data-tooltip="Eliminar"', admin_row_html)

    def test_superadmin_detail_page_hides_edit_form_and_actions(self) -> None:
        state = SeededUsersState.seed()
        state.users["admin"] = {
            "id": "admin",
            "nombre": "",
            "apellidos": "",
            "email": "",
            "rol_principal": "superadmin",
            "estado": "activo",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "invitacion_pendiente": False,
            "username": "admin",
            "password_hash": "hash-admin",
        }
        state.history["admin"] = []

        with self._patch_users_db(state):
            status, headers, body = invoke_app("/usuarios/admin")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("La cuenta superadmin no puede editarse, deshabilitarse ni eliminarse desde la interfaz.", html)
        self.assertIn('Usuario seleccionado:</strong> admin', html)
        self.assertNotIn('id="editar_username"', html)
        self.assertNotIn('id="editar_nombre"', html)
        self.assertNotIn('id="editar_email"', html)
        self.assertNotIn('data-tooltip="Modificar"', html)
        self.assertNotIn('data-tooltip="Deshabilitar"', html)
        self.assertNotIn('data-tooltip="Reactivar"', html)
        self.assertNotIn('data-tooltip="Eliminar"', html)

    def test_users_page_denied_to_reader_role(self) -> None:
        invited_cookie = _session_cookie(role="invitado", username="invitado-1", nombre_completo="Invitado Demo")
        with patch.dict(os.environ, {"LOGIN_AUTOMATICO": "false"}, clear=False):
            status, headers, body = invoke_app("/usuarios", cookies=invited_cookie)

        self.assertEqual("403 Forbidden", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn("Acceso restringido por rol", body.decode("utf-8"))

    def test_user_creation_route_redirects_and_persists_account(self) -> None:
        state = SeededUsersState.seed()
        form_data = urlencode(
            {
                "nombre": "Eva",
                "apellidos": "Santos",
                "email": "eva.santos@licican.local",
                "rol_principal": "manager",
                "estado": "pendiente",
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
        self.assertIn("pendiente", html)

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
