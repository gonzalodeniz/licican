from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from licican.users import (
    UserFilters,
    build_users_payload,
    change_user_state,
    create_user,
    load_users,
    resend_invitation,
    reset_access,
)
from tests.shared.users_db import SeededUsersState, fake_users_connect


class UsersModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_patch = patch.dict(os.environ, {"DB_PASSWORD": "test-password"}, clear=False)
        self._env_patch.start()

    def tearDown(self) -> None:
        self._env_patch.stop()

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

    def test_create_user_persists_new_pending_account(self) -> None:
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
        self.assertEqual("pendiente", created.estado)
        self.assertTrue(created.invitacion_pendiente)
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

    def test_change_state_blocks_removing_last_active_admin(self) -> None:
        state = SeededUsersState.seed()
        state.users["usr-005"] = {
            "id": "usr-005",
            "nombre": "Sonia",
            "apellidos": "Admin",
            "email": "sonia.admin@licican.local",
            "rol_principal": "administrador",
            "estado": "activo",
            "observaciones_internas": "Cuenta administrativa secundaria.",
            "fecha_alta": state.users["usr-001"]["fecha_alta"],
            "ultimo_acceso": None,
            "invitacion_pendiente": False,
        }
        with self._patch_users_db(state):
            change_user_state("usr-001", "inactivo")

            with self.assertRaisesRegex(ValueError, "sin ningun usuario administrador activo"):
                change_user_state("usr-005", "inactivo")

    def test_resend_invitation_requires_pending_user(self) -> None:
        with self._patch_users_db():
            with self.assertRaisesRegex(ValueError, "pendientes de activacion"):
                resend_invitation("usr-001")

            updated = resend_invitation("usr-003")

        self.assertTrue(updated.invitacion_pendiente)
        self.assertEqual("pendiente", updated.estado)

    def test_build_users_payload_applies_filters_and_selection(self) -> None:
        with self._patch_users_db():
            payload = build_users_payload(
                filters=UserFilters(busqueda="laura", estado="pendiente"),
                selected_user_id="usr-003",
            )

        self.assertEqual(1, payload["paginacion"]["total_resultados"])
        self.assertEqual(["usr-003"], [item["id"] for item in payload["usuarios"]])
        self.assertEqual("usr-003", payload["usuario_seleccionado"]["id"])
        self.assertEqual({"busqueda": "laura", "estado": "pendiente"}, payload["filtros_activos"])

    def test_reset_access_rejects_pending_accounts(self) -> None:
        with self._patch_users_db():
            with self.assertRaisesRegex(ValueError, "pendiente de activacion"):
                reset_access("usr-003")

    def test_user_storage_remains_consistent_after_operations(self) -> None:
        state = SeededUsersState.seed()
        with self._patch_users_db(state):
            create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="manager",
            )
            change_user_state("usr-004", "activo")
            updated = resend_invitation("usr-003")

        self.assertEqual("activo", state.users["usr-004"]["estado"])
        self.assertEqual("pendiente", state.users["usr-003"]["estado"])
        self.assertTrue(updated.invitacion_pendiente)
        self.assertGreaterEqual(len(state.history_rows()), 9)
