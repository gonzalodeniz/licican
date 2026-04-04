from __future__ import annotations

import os
import unittest
from unittest.mock import patch

import bcrypt

from licican.auth.config import get_auth_settings
from licican.users import (
    UserFilters,
    build_users_payload,
    change_user_state,
    create_user,
    delete_user,
    load_users,
    update_user,
)
from tests.shared.users_db import SeededUsersState, fake_users_connect


class UsersModuleTests(unittest.TestCase):
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

    def test_load_users_returns_seed_payload_from_database(self) -> None:
        with self._patch_users_db():
            reference, users = load_users()

        self.assertIn("PB-016", reference)
        self.assertEqual(4, len(users))
        self.assertEqual("usr-003", users[0].id)
        self.assertEqual("Laura Gonzalez", users[0].nombre_completo)

    def test_create_user_persists_new_disabled_account(self) -> None:
        state = SeededUsersState.seed()
        with self._patch_users_db(state):
            created = create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="manager",
            )
            reference, users = load_users()

        self.assertIn("PB-016", reference)
        self.assertEqual("usr-005", created.id)
        self.assertEqual("deshabilitado", created.estado)
        self.assertEqual(0, created.failed_login_attempts)
        self.assertIsNone(created.bloqueado_hasta)
        self.assertEqual(5, len(users))
        self.assertEqual("eva.santos@licican.local", users[-1].email)

    def test_create_user_rejects_duplicate_email(self) -> None:
        state = SeededUsersState.seed()
        with self._patch_users_db(state):
            create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="manager",
            )
            with self.assertRaisesRegex(ValueError, "El email no puede duplicarse"):
                create_user(
                    nombre="Eva",
                    apellidos="Santos",
                    email="eva.santos@licican.local",
                    rol_principal="manager",
                )

    def test_create_user_rejects_superadmin_role(self) -> None:
        with self._patch_users_db():
            with self.assertRaisesRegex(ValueError, "superadmin no puede asignarse"):
                create_user(
                    nombre="Eva",
                    apellidos="Santos",
                    email="eva.santos@licican.local",
                    rol_principal="superadmin",
                )

    def test_change_state_blocks_removing_last_active_admin(self) -> None:
        state = SeededUsersState.seed()
        state.users["usr-005"] = {
            "id": "usr-005",
            "nombre": "Sonia",
            "apellidos": "Admin",
            "email": "sonia.admin@licican.local",
            "rol_principal": "administrador",
            "estado": "activo",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "failed_login_attempts": 0,
            "bloqueado_hasta": None,
        }
        with self._patch_users_db(state):
            change_user_state("usr-001", "deshabilitado")

            with self.assertRaisesRegex(ValueError, "sin ningun usuario administrador activo"):
                change_user_state("usr-005", "deshabilitado")

    def test_build_users_payload_applies_filters_and_selection(self) -> None:
        with self._patch_users_db():
            payload = build_users_payload(
                filters=UserFilters(busqueda="laura", estado="deshabilitado"),
                selected_user_id="usr-003",
            )

        self.assertEqual(1, payload["paginacion"]["total_resultados"])
        self.assertEqual(["usr-003"], [item["id"] for item in payload["usuarios"]])
        self.assertEqual("usr-003", payload["usuario_seleccionado"]["id"])
        self.assertEqual({"busqueda": "laura", "estado": "deshabilitado"}, payload["filtros_activos"])

    def test_build_users_payload_matches_username_in_search(self) -> None:
        state = SeededUsersState.seed()
        state.users["usr-003"]["username"] = "laura-login"
        with self._patch_users_db(state):
            payload = build_users_payload(filters=UserFilters(busqueda="laura-login"))

        self.assertEqual(["usr-003"], [item["id"] for item in payload["usuarios"]])
        self.assertEqual("laura-login", payload["usuarios"][0]["username"])

    def test_update_user_allows_changing_password(self) -> None:
        state = SeededUsersState.seed()
        previous_hash = str(state.users["usr-002"]["password_hash"])

        with self._patch_users_db(state):
            updated = update_user(
                "usr-002",
                nombre="Carlos",
                apellidos="Mendez",
                email="carlos.mendez@licican.local",
                username="carlos-login",
                rol_principal="manager",
                estado="activo",
                nueva_contrasena="nueva-clave-123",
                confirmar_contrasena="nueva-clave-123",
            )

        self.assertNotEqual(previous_hash, updated.password_hash)
        self.assertTrue(bcrypt.checkpw("nueva-clave-123".encode("utf-8"), str(updated.password_hash).encode("utf-8")))
        self.assertTrue(bcrypt.checkpw("nueva-clave-123".encode("utf-8"), str(state.users["usr-002"]["password_hash"]).encode("utf-8")))
        self.assertEqual("carlos-login", updated.username)
        self.assertEqual("carlos-login", state.users["usr-002"]["username"])

    def test_update_user_rejects_superadmin_role_assignment(self) -> None:
        with self._patch_users_db():
            with self.assertRaisesRegex(ValueError, "superadmin no puede asignarse"):
                update_user(
                    "usr-002",
                    nombre="Carlos",
                    apellidos="Mendez",
                    email="carlos.mendez@licican.local",
                    username="carlos-login",
                    rol_principal="superadmin",
                    estado="activo",
                )

    def test_update_user_rejects_password_confirmation_mismatch(self) -> None:
        with self._patch_users_db():
            with self.assertRaisesRegex(ValueError, "confirmacion de contrasena no coincide"):
                update_user(
                    "usr-002",
                    nombre="Carlos",
                    apellidos="Mendez",
                    email="carlos.mendez@licican.local",
                    rol_principal="manager",
                    estado="activo",
                    nueva_contrasena="nueva-clave-123",
                    confirmar_contrasena="otra-clave-123",
                )

    def test_delete_user_removes_record_and_history(self) -> None:
        state = SeededUsersState.seed()
        with self._patch_users_db(state):
            delete_user("usr-004")

        self.assertNotIn("usr-004", state.users)
        self.assertNotIn("usr-004", state.history)

    def test_superadmin_cannot_be_updated_deleted_or_disabled(self) -> None:
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
            "failed_login_attempts": 0,
            "bloqueado_hasta": None,
            "username": "admin",
            "password_hash": bcrypt.hashpw(b"admin12345", bcrypt.gensalt()).decode("utf-8"),
        }
        state.history["admin"] = []

        with self._patch_users_db(state):
            with self.assertRaisesRegex(ValueError, "superadmin no puede editarse"):
                update_user(
                    "admin",
                    nombre="Super",
                    apellidos="Admin",
                    email="super@licican.local",
                    username="admin",
                    rol_principal="superadmin",
                    estado="activo",
                )
            with self.assertRaisesRegex(ValueError, "superadmin no puede editarse"):
                change_user_state("admin", "deshabilitado")
            with self.assertRaisesRegex(ValueError, "superadmin no puede editarse"):
                delete_user("admin")
