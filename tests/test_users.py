from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.users import (
    UserFilters,
    build_users_payload,
    change_user_state,
    create_user,
    load_users,
    resend_invitation,
    reset_access,
)


class UsersModuleTests(unittest.TestCase):
    def test_load_users_returns_seed_payload_when_file_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            reference, users = load_users(Path(tmp_dir) / "users.json")

        self.assertIn("PB-016", reference)
        self.assertEqual(4, len(users))
        self.assertEqual("usr-001", users[0].id)

    def test_create_user_persists_new_pending_account(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"
            created = create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="responsable",
                superficies="Catalogo, Alertas",
                path=storage,
            )
            reference, users = load_users(storage)

        self.assertIn("PB-016", reference)
        self.assertEqual("usr-005", created.id)
        self.assertEqual("pendiente", created.estado)
        self.assertTrue(created.invitacion_pendiente)
        self.assertEqual(5, len(users))
        self.assertEqual("eva.santos@licican.local", users[-1].email)

    def test_create_user_rejects_duplicate_email(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"
            create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="responsable",
                superficies="Catalogo, Alertas",
                path=storage,
            )

            with self.assertRaisesRegex(ValueError, "El email no puede duplicarse"):
                create_user(
                    nombre="Eva",
                    apellidos="Santos",
                    email="eva.santos@licican.local",
                    rol_principal="responsable",
                    superficies="Catalogo",
                    path=storage,
                )

    def test_change_state_blocks_removing_last_active_admin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"
            change_user_state("usr-001", "inactivo", path=storage)

            with self.assertRaisesRegex(ValueError, "sin ningun usuario administrador activo"):
                change_user_state("usr-002", "inactivo", path=storage)

    def test_resend_invitation_requires_pending_user(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"

            with self.assertRaisesRegex(ValueError, "pendientes de activacion"):
                resend_invitation("usr-001", path=storage)

            updated = resend_invitation("usr-003", path=storage)

        self.assertTrue(updated.invitacion_pendiente)
        self.assertEqual("pendiente", updated.estado)

    def test_build_users_payload_applies_filters_and_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"
            payload = build_users_payload(
                path=storage,
                filters=UserFilters(busqueda="laura", estado="pendiente"),
                selected_user_id="usr-003",
            )

        self.assertEqual(1, payload["paginacion"]["total_resultados"])
        self.assertEqual(["usr-003"], [item["id"] for item in payload["usuarios"]])
        self.assertEqual("usr-003", payload["usuario_seleccionado"]["id"])
        self.assertEqual({"busqueda": "laura", "estado": "pendiente"}, payload["filtros_activos"])

    def test_reset_access_rejects_pending_accounts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"

            with self.assertRaisesRegex(ValueError, "pendiente de activacion"):
                reset_access("usr-003", path=storage)

    def test_user_storage_is_json_serializable_after_operations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = Path(tmp_dir) / "users.json"
            create_user(
                nombre="Eva",
                apellidos="Santos",
                email="eva.santos@licican.local",
                rol_principal="responsable",
                superficies="Catalogo, Alertas",
                path=storage,
            )
            payload = json.loads(storage.read_text(encoding="utf-8"))

        self.assertIn("users", payload)
        self.assertEqual(5, len(payload["users"]))
