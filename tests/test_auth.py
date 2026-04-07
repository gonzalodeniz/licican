from __future__ import annotations

import os
import re
import unittest
from contextlib import ExitStack
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import bcrypt
import psycopg2

import licican.auth.service as auth_service
from licican.auth.config import get_auth_settings
from licican.auth.rate_limiter import rate_limiter
from licican.auth.service import (
    AUTH_USER_BOOTSTRAP_SQL,
    AUTH_USER_CLEAR_USERNAME_SQL,
    AUTH_USER_DEACTIVATE_SQL,
    AUTH_USER_INSERT_SQL,
    AUTH_USER_LAST_LOGIN_SQL,
    AUTH_USER_RECORD_FAILED_LOGIN_SQL,
    AUTH_USER_RECORD_SUCCESSFUL_LOGIN_SQL,
    AUTH_USER_RESET_LOGIN_STATE_SQL,
    AUTH_USER_SELECT_SQL,
    AUTH_USER_SELECT_BY_USERNAME_SQL,
    AUTH_USER_SELECT_SUPERADMIN_SQL,
    AUTH_USER_DELETE_SQL,
    AUTH_USER_UPDATE_SUPERADMIN_SQL,
    synchronize_superadmin_account,
)
from tests.shared.app_http import invoke_app


class _BrowserSession:
    def __init__(self) -> None:
        self.cookies = ""

    def request(self, path: str, **kwargs):
        status, headers, body = invoke_app(path, authenticated=False, cookies=self.cookies, **kwargs)
        set_cookie = headers.get("Set-Cookie")
        if set_cookie:
            self.cookies = set_cookie.split(";", 1)[0]
        return status, headers, body


class _FakeAuthCursor:
    def __init__(self, state: dict[str, dict[str, object]]) -> None:
        self.state = state
        self.row: dict[str, object] | None = None

    def execute(self, sql: str, params=None) -> None:
        normalized = str(sql).strip()
        if normalized == AUTH_USER_BOOTSTRAP_SQL.strip():
            return
        if normalized == AUTH_USER_SELECT_SUPERADMIN_SQL.strip():
            role_principal = str(params[0])
            role = str(params[1])
            preferred_username = str(params[2])
            rows = [
                deepcopy(record)
                for record in self.state.values()
                if record.get("rol_principal") == role_principal or record.get("rol") == role
            ]
            rows.sort(
                key=lambda record: (
                    0 if record.get("username") == preferred_username else 1,
                    str(record.get("updated_at") or ""),
                    str(record.get("fecha_alta") or ""),
                    str(record.get("id") or ""),
                )
            )
            self.rows = rows
            self.row = rows[0] if rows else None
            return
        if normalized == AUTH_USER_SELECT_BY_USERNAME_SQL.strip():
            username = str(params[0])
            record = self.state.get(username)
            self.row = deepcopy(record) if record is not None else None
            return
        if normalized == AUTH_USER_SELECT_SQL.strip():
            login_name = str(params[0])
            email = str(params[1]) if params and len(params) > 1 else login_name
            record = self.state.get(login_name)
            if record is None:
                record = next((row for row in self.state.values() if row.get("email") == email), None)
            self.row = deepcopy(record) if record is not None else None
            return
        if normalized == AUTH_USER_CLEAR_USERNAME_SQL.strip():
            updated_at, user_id = params
            for key, record in list(self.state.items()):
                if record["id"] == user_id:
                    previous_username = str(record.get("username") or "")
                    record["username"] = None
                    record["updated_at"] = updated_at
                    if key != str(record["id"]):
                        self.state.pop(key, None)
                    self.state[str(record["id"])] = record
                    if previous_username and previous_username != str(record["id"]):
                        self.state.pop(previous_username, None)
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_LAST_LOGIN_SQL.strip():
            last_login, last_access, updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["ultimo_login"] = last_login
                    record["ultimo_acceso"] = last_access
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_INSERT_SQL.strip():
            (
                user_id,
                nombre,
                apellidos,
                email,
                rol_principal,
                estado,
                observaciones_internas,
                fecha_alta,
                ultimo_acceso,
                username,
                password_hash,
                nombre_completo,
                rol,
                activo,
                failed_login_attempts,
                bloqueado_hasta,
                ultimo_login,
                created_at,
                updated_at,
            ) = params
            self.state[str(username)] = {
                "id": user_id,
                "nombre": str(nombre),
                "apellidos": str(apellidos),
                "email": str(email),
                "rol_principal": str(rol_principal),
                "estado": str(estado),
                "observaciones_internas": str(observaciones_internas),
                "fecha_alta": fecha_alta,
                "ultimo_acceso": ultimo_acceso,
                "failed_login_attempts": int(failed_login_attempts),
                "bloqueado_hasta": bloqueado_hasta,
                "username": str(username),
                "password_hash": str(password_hash),
                "nombre_completo": str(nombre_completo),
                "rol": str(rol),
                "activo": bool(activo),
                "ultimo_login": ultimo_login,
                "created_at": created_at,
                "updated_at": updated_at,
            }
            return
        if normalized == AUTH_USER_DELETE_SQL.strip():
            (user_id,) = params
            for key, record in list(self.state.items()):
                if record["id"] == user_id:
                    self.state.pop(key, None)
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_UPDATE_SUPERADMIN_SQL.strip():
            (
                nombre,
                apellidos,
                email,
                rol_principal,
                estado,
                observaciones_internas,
                fecha_alta,
                ultimo_acceso,
                username,
                password_hash,
                nombre_completo,
                rol,
                activo,
                failed_login_attempts,
                bloqueado_hasta,
                ultimo_login,
                updated_at,
                user_id,
            ) = params
            for key, record in list(self.state.items()):
                if record["id"] == user_id:
                    previous_username = str(record.get("username") or "")
                    record.update(
                        {
                            "nombre": str(nombre),
                            "apellidos": str(apellidos),
                            "email": str(email),
                            "rol_principal": str(rol_principal),
                            "estado": str(estado),
                            "observaciones_internas": str(observaciones_internas),
                            "fecha_alta": fecha_alta,
                            "ultimo_acceso": ultimo_acceso,
                            "failed_login_attempts": int(failed_login_attempts),
                            "bloqueado_hasta": bloqueado_hasta,
                            "username": str(username),
                            "password_hash": str(password_hash),
                            "nombre_completo": str(nombre_completo),
                            "rol": str(rol),
                            "activo": bool(activo),
                            "ultimo_login": ultimo_login,
                            "updated_at": updated_at,
                        }
                    )
                    new_username = str(username)
                    if previous_username and previous_username != new_username:
                        self.state.pop(previous_username, None)
                    if key != str(record["id"]):
                        self.state.pop(key, None)
                    self.state[new_username] = record
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_DEACTIVATE_SQL.strip():
            updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["estado"] = "deshabilitado"
                    record["activo"] = False
                    record["failed_login_attempts"] = 0
                    record["bloqueado_hasta"] = None
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_RESET_LOGIN_STATE_SQL.strip():
            updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["estado"] = "activo"
                    record["activo"] = True
                    record["failed_login_attempts"] = 0
                    record["bloqueado_hasta"] = None
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_RECORD_FAILED_LOGIN_SQL.strip():
            estado, activo, failed_login_attempts, bloqueado_hasta, updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["estado"] = str(estado)
                    record["activo"] = bool(activo)
                    record["failed_login_attempts"] = int(failed_login_attempts)
                    record["bloqueado_hasta"] = bloqueado_hasta
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_RECORD_SUCCESSFUL_LOGIN_SQL.strip():
            last_login, last_access, updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["estado"] = "activo"
                    record["activo"] = True
                    record["failed_login_attempts"] = 0
                    record["bloqueado_hasta"] = None
                    record["ultimo_login"] = last_login
                    record["ultimo_acceso"] = last_access
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        raise AssertionError(f"SQL inesperado en prueba auth: {normalized}")

    def fetchone(self) -> dict[str, object] | None:
        return deepcopy(self.row) if self.row is not None else None

    def fetchall(self) -> list[dict[str, object]]:
        return [deepcopy(row) for row in getattr(self, "rows", [])]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeAuthConnection:
    def __init__(self, state: dict[str, dict[str, object]]) -> None:
        self.state = state

    def cursor(self, cursor_factory=None):
        return _FakeAuthCursor(self.state)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _fake_auth_connect(state: dict[str, dict[str, object]]):
    return _FakeAuthConnection(state)


def _build_user_record(
    *,
    user_id: int,
    username: str,
    email: str | None = None,
    password: str,
    nombre_completo: str,
    rol: str = "consultor",
    estado: str | None = None,
    activo: bool = True,
    failed_login_attempts: int = 0,
    bloqueado_hasta: datetime | None = None,
) -> dict[str, object]:
    nombre, _, apellidos = nombre_completo.partition(" ")
    if not apellidos:
        apellidos = "Licican"
    email = email or (username if "@" in username else f"{username}@licican.local")
    current = datetime.now(UTC).replace(microsecond=0)
    state = estado or ("activo" if activo else "deshabilitado")
    if state == "bloqueado":
        activo = False
    return {
        "id": user_id,
        "nombre": nombre,
        "apellidos": apellidos,
        "email": email,
        "rol_principal": rol,
        "estado": state,
        "observaciones_internas": "",
        "fecha_alta": current,
        "ultimo_acceso": None,
        "failed_login_attempts": failed_login_attempts,
        "bloqueado_hasta": bloqueado_hasta,
        "username": username,
        "password_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "nombre_completo": nombre_completo,
        "rol": rol,
        "activo": activo,
        "ultimo_login": None,
        "created_at": current,
        "updated_at": current,
    }


class AuthenticationTests(unittest.TestCase):
    def setUp(self) -> None:
        get_auth_settings.cache_clear()
        rate_limiter._store.attempts.clear()

    def tearDown(self) -> None:
        get_auth_settings.cache_clear()
        rate_limiter._store.attempts.clear()

    def _manual_env(self, **overrides: str):
        env = {
            "BASE_PATH": "/licican",
            "LOGIN_AUTOMATICO": "false",
            "LOGIN_SUPERADMIN_ENABLED": "true",
            "LOGIN_SUPERADMIN_PASS": "admin12345",
            "SESSION_SECRET_KEY": "test-session-secret",
            "SESSION_TIMEOUT_MINUTES": "30",
            "DB_PASSWORD": "test-password",
        }
        env.update(overrides)
        return patch.dict(os.environ, env, clear=False)

    def _extract_csrf(self, html: str) -> str:
        match = re.search(r'name="csrf_token" value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return str(match.group(1))

    def test_login_with_superadmin_enabled_creates_session(self) -> None:
        browser = _BrowserSession()
        auth_state: dict[str, dict[str, object]] = {}
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            status, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            login_status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=superadmin&password=admin12345&csrf_token={csrf_token}",
            )
            page_status, _, page_body = browser.request("/")

        self.assertEqual("200 OK", status)
        self.assertEqual("302 Found", login_status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("Cerrar sesión", page_body.decode("utf-8"))
        self.assertIn("superadmin", auth_state)
        self.assertEqual("activo", auth_state["superadmin"]["estado"])
        self.assertEqual("superadmin", auth_state["superadmin"]["rol_principal"])
        self.assertEqual("superadmin@licitan.local", auth_state["superadmin"]["email"])
        self.assertEqual("Superadministrador", auth_state["superadmin"]["nombre"])
        self.assertEqual("Licican", auth_state["superadmin"]["apellidos"])
        self.assertEqual("Superadministrador Licican", auth_state["superadmin"]["nombre_completo"])
        self.assertTrue(auth_state["superadmin"]["activo"])
        self.assertTrue(bcrypt.checkpw("admin12345".encode("utf-8"), auth_state["superadmin"]["password_hash"].encode("utf-8")))

    def test_login_with_superadmin_works_when_postgresql_sync_fails(self) -> None:
        browser = _BrowserSession()
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(
                patch(
                    "licican.auth.service.psycopg2.connect",
                    side_effect=psycopg2.OperationalError("db down"),
                )
            )
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            login_status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=superadmin&password=admin12345&csrf_token={csrf_token}",
            )

        self.assertEqual("302 Found", login_status)
        self.assertEqual("/licican/", headers["Location"])

    def test_login_with_superadmin_disabled_rejects_superadmin_credentials(self) -> None:
        browser = _BrowserSession()
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="false"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect({})))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, _, response_body = browser.request(
                "/login",
                method="POST",
                body=f"username=superadmin&password=admin12345&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", status)
        self.assertIn("Usuario o contraseña incorrectos.", response_body.decode("utf-8"))

    def test_login_with_database_user_creates_session(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "superadmin": _build_user_record(
                user_id=9,
                username="superadmin",
                email="admin@licican.local",
                password="anterior123",
                nombre_completo="Superadministrador",
                rol="administrador",
                activo=False,
            ),
            "marta": _build_user_record(
                user_id=1,
                username="marta",
                email="marta.garcia@licican.local",
                password="secreto123",
                nombre_completo="Marta Pérez",
                rol="gestor",
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=secreto123&csrf_token={csrf_token}",
            )
            page_status, _, page_body = browser.request("/dashboard")

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("Dashboard", page_body.decode("utf-8"))
        self.assertIsNotNone(auth_state["marta"]["ultimo_login"])
        self.assertEqual("activo", auth_state["superadmin"]["estado"])
        self.assertTrue(auth_state["superadmin"]["activo"])
        self.assertTrue(bcrypt.checkpw("admin12345".encode("utf-8"), auth_state["superadmin"]["password_hash"].encode("utf-8")))

    def test_login_with_database_email_creates_session(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "marta": _build_user_record(
                user_id=1,
                username="marta",
                email="marta.garcia@licican.local",
                password="secreto123",
                nombre_completo="Marta Pérez",
                rol="gestor",
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=marta.garcia@licican.local&password=secreto123&csrf_token={csrf_token}",
            )

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertIsNotNone(auth_state["marta"]["ultimo_login"])

    def test_login_with_superadmin_email_alias_creates_session(self) -> None:
        browser = _BrowserSession()
        auth_state: dict[str, dict[str, object]] = {}
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=superadmin@licitan.local&password=admin12345&csrf_token={csrf_token}",
            )

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertIn("superadmin", auth_state)

    def test_login_with_inactive_user_is_rejected(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "soporte": _build_user_record(
                user_id=2,
                username="soporte",
                password="secreto123",
                nombre_completo="Soporte Interno",
                activo=False,
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, _, response_body = browser.request(
                "/login",
                method="POST",
                body=f"username=soporte&password=secreto123&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", status)
        self.assertIn("Usuario deshabilitado. Contacte al administrador.", response_body.decode("utf-8"))
        self.assertEqual("deshabilitado", auth_state["soporte"]["estado"])

    def test_superadmin_disabled_marks_database_user_inactive(self) -> None:
        auth_state = {
            "superadmin": _build_user_record(
                user_id=7,
                username="superadmin",
                password="admin12345",
                nombre_completo="Superadministrador",
                rol="superadmin",
                activo=True,
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="false", LOGIN_AUTOMATICO="false"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        self.assertFalse(auth_state["superadmin"]["activo"])
        self.assertEqual("deshabilitado", auth_state["superadmin"]["estado"])

    def test_login_blocks_user_after_repeated_failures_and_unlocks_automatically(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "marta": _build_user_record(
                user_id=1,
                username="marta",
                password="secreto123",
                nombre_completo="Marta Pérez",
                rol="gestor",
                estado="activo",
                activo=True,
                failed_login_attempts=0,
                bloqueado_hasta=None,
            )
        }
        unlock_start = datetime(2026, 4, 4, 12, 0, 0)
        with ExitStack() as stack:
            stack.enter_context(
                self._manual_env(
                    LOGIN_SUPERADMIN_ENABLED="false",
                    LOGIN_MAX_FAILED_ATTEMPTS="2",
                    LOGIN_LOCK_MINUTES="1",
                )
            )
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            stack.enter_context(
                patch(
                    "licican.auth.service._now_utc",
                    side_effect=[
                        unlock_start,
                        unlock_start,
                        unlock_start + timedelta(seconds=10),
                        unlock_start + timedelta(seconds=61),
                    ],
                )
            )
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            first_status, _, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=incorrecta&csrf_token={csrf_token}",
            )
            second_status, _, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=incorrecta&csrf_token={csrf_token}",
            )
            blocked_status, _, blocked_body = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=secreto123&csrf_token={csrf_token}",
            )
            final_status, headers, _ = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=secreto123&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", first_status)
        self.assertEqual("401 Unauthorized", second_status)
        self.assertEqual("429 Too Many Requests", blocked_status)
        self.assertIn("Usuario bloqueado temporalmente", blocked_body.decode("utf-8"))
        self.assertEqual("302 Found", final_status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertEqual("activo", auth_state["marta"]["estado"])
        self.assertEqual(0, auth_state["marta"]["failed_login_attempts"])
        self.assertIsNone(auth_state["marta"]["bloqueado_hasta"])

    def test_superadmin_failed_login_does_not_lock_account(self) -> None:
        auth_state = {
            "superadmin": _build_user_record(
                user_id=11,
                username="superadmin",
                password="correcta123",
                nombre_completo="Superadministrador",
                rol="superadmin",
                estado="activo",
                activo=True,
                failed_login_attempts=0,
                bloqueado_hasta=None,
            )
        }
        cursor = _FakeAuthCursor(auth_state)
        row = deepcopy(auth_state["superadmin"])
        settings = get_auth_settings()
        current = datetime(2026, 4, 4, 12, 0, 0)

        auth_service._record_failed_login(cursor, row, current, settings)

        self.assertEqual("activo", auth_state["superadmin"]["estado"])
        self.assertEqual(0, auth_state["superadmin"]["failed_login_attempts"])
        self.assertIsNone(auth_state["superadmin"]["bloqueado_hasta"])

    def test_superadmin_enabled_reactivates_user_and_updates_password(self) -> None:
        auth_state = {
            "superadmin": _build_user_record(
                user_id=7,
                username="superadmin",
                password="vieja12345",
                nombre_completo="Superadministrador",
                rol="superadmin",
                activo=False,
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="true", LOGIN_AUTOMATICO="false", LOGIN_SUPERADMIN_PASS="nueva12345"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        self.assertTrue(auth_state["superadmin"]["activo"])
        self.assertEqual("activo", auth_state["superadmin"]["estado"])
        self.assertEqual("superadmin", auth_state["superadmin"]["rol_principal"])
        self.assertEqual("Superadministrador", auth_state["superadmin"]["nombre"])
        self.assertEqual("Licican", auth_state["superadmin"]["apellidos"])
        self.assertEqual("superadmin@licitan.local", auth_state["superadmin"]["email"])
        self.assertEqual("Superadministrador Licican", auth_state["superadmin"]["nombre_completo"])
        self.assertTrue(bcrypt.checkpw("nueva12345".encode("utf-8"), auth_state["superadmin"]["password_hash"].encode("utf-8")))

    def test_superadmin_sync_keeps_canonical_username_and_clears_conflicts(self) -> None:
        auth_state = {
            "legacy-superadmin": _build_user_record(
                user_id=7,
                username="legacy-superadmin",
                password="vieja12345",
                nombre_completo="Superadministrador",
                rol="superadmin",
                activo=True,
            ),
            "admin-duplicado": _build_user_record(
                user_id=8,
                username="admin-duplicado",
                password="otra12345",
                nombre_completo="Superadministrador",
                rol="superadmin",
                activo=True,
            ),
            "superadmin": _build_user_record(
                user_id=9,
                username="superadmin",
                password="otra12345",
                nombre_completo="Usuario conflictivo",
                rol="gestor",
                activo=True,
            ),
            "marta": _build_user_record(
                user_id=1,
                username="marta",
                password="secreto123",
                nombre_completo="Marta Pérez",
                rol="gestor",
            ),
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_PASS="nueva12345"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        superadmin_rows = [user for user in auth_state.values() if user["rol_principal"] == "superadmin"]
        self.assertEqual(1, len(superadmin_rows))
        self.assertIn("superadmin", auth_state)
        self.assertNotIn("legacy-superadmin", auth_state)
        self.assertNotIn("admin-duplicado", auth_state)
        self.assertEqual("superadmin", auth_state["superadmin"]["username"])
        self.assertEqual("Superadministrador", auth_state["superadmin"]["nombre"])
        self.assertEqual("Licican", auth_state["superadmin"]["apellidos"])
        self.assertEqual("superadmin@licitan.local", auth_state["superadmin"]["email"])
        self.assertEqual("activo", auth_state["superadmin"]["estado"])
        self.assertTrue(bcrypt.checkpw("nueva12345".encode("utf-8"), auth_state["superadmin"]["password_hash"].encode("utf-8")))
        self.assertTrue(any(str(record["id"]) == "9" and record["username"] is None for record in auth_state.values()))

    def test_login_with_invalid_credentials_returns_generic_message(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "marta": _build_user_record(
                user_id=1,
                username="marta",
                password="secreto123",
                nombre_completo="Marta Pérez",
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, _, response_body = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=otro&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", status)
        self.assertIn("Usuario o contraseña incorrectos.", response_body.decode("utf-8"))

    def test_superadmin_sync_creates_visible_user_when_missing(self) -> None:
        auth_state: dict[str, dict[str, object]] = {}
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        self.assertIn("superadmin", auth_state)
        self.assertEqual("Superadministrador", auth_state["superadmin"]["nombre"])
        self.assertEqual("Licican", auth_state["superadmin"]["apellidos"])
        self.assertEqual("superadmin@licitan.local", auth_state["superadmin"]["email"])
        self.assertEqual("Superadministrador Licican", auth_state["superadmin"]["nombre_completo"])
        self.assertEqual("superadmin", auth_state["superadmin"]["rol_principal"])
        self.assertEqual("activo", auth_state["superadmin"]["estado"])

    def test_login_with_database_error_returns_generic_message(self) -> None:
        browser = _BrowserSession()
        with ExitStack() as stack:
            stack.enter_context(self._manual_env())
            stack.enter_context(
                patch(
                    "licican.auth.service.psycopg2.connect",
                    side_effect=psycopg2.OperationalError("db down"),
                )
            )
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            status, _, response_body = browser.request(
                "/login",
                method="POST",
                body=f"username=marta&password=secreto123&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", status)
        self.assertIn("No se pudo validar la autenticacion.", response_body.decode("utf-8"))

    def test_protected_route_without_session_redirects_to_login(self) -> None:
        with self._manual_env():
            status, headers, _ = invoke_app("/", authenticated=False)

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/login", headers["Location"])

    def test_session_timeout_redirects_to_login_with_reason(self) -> None:
        expired_activity = (datetime.now(UTC) - timedelta(minutes=31)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        with self._manual_env():
            status, headers, _ = invoke_app(
                "/",
                authenticated=False,
                cookies=self._expired_cookie(expired_activity),
            )

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/login?reason=timeout", headers["Location"])

    def test_logout_destroys_session_and_redirects_to_login(self) -> None:
        with self._manual_env():
            status, headers, _ = invoke_app("/logout", method="POST", body="csrf_token=csrf-test-token")
            redirected_status, redirected_headers, _ = invoke_app(
                "/",
                authenticated=False,
                cookies=headers["Set-Cookie"].split(";", 1)[0],
            )

        self.assertEqual("302 Found", status)
        self.assertTrue(headers["Location"].startswith("/licican/login"))
        self.assertEqual("302 Found", redirected_status)
        self.assertEqual("/licican/login", redirected_headers["Location"])

    def test_rate_limiting_blocks_after_five_failed_attempts(self) -> None:
        browser = _BrowserSession()
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="false"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect({})))
            _, _, body = browser.request("/login")
            csrf_token = self._extract_csrf(body.decode("utf-8"))
            for _ in range(5):
                status, _, _ = browser.request(
                    "/login",
                    method="POST",
                    body=f"username=admin&password=incorrecta&csrf_token={csrf_token}",
                )
                self.assertEqual("401 Unauthorized", status)
            blocked_status, _, blocked_body = browser.request(
                "/login",
                method="POST",
                body=f"username=admin&password=incorrecta&csrf_token={csrf_token}",
            )

        self.assertEqual("429 Too Many Requests", blocked_status)
        self.assertIn("Demasiados intentos. Espere unos minutos.", blocked_body.decode("utf-8"))

    def _expired_cookie(self, last_activity: str) -> str:
        with patch.dict(
            os.environ,
            {
                "SESSION_SECRET_KEY": "test-session-secret",
            },
            clear=False,
        ):
            get_auth_settings.cache_clear()
            status, headers, _ = invoke_app(
                "/",
                authenticated=False,
                cookies="",
            )
            set_cookie = headers.get("Set-Cookie")
            self.assertEqual("302 Found", status)
            self.assertIsNotNone(set_cookie)
        return self._replace_cookie_last_activity(str(set_cookie).split(";", 1)[0], last_activity)

    def _replace_cookie_last_activity(self, cookie_pair: str, last_activity: str) -> str:
        from itsdangerous import URLSafeSerializer

        _, signed_value = cookie_pair.split("=", 1)
        signer = URLSafeSerializer("test-session-secret", salt="licican.session")
        payload = signer.loads(signed_value)
        payload.update(
            {
                "username": "timeout-user",
                "rol": "administrador",
                "nombre_completo": "Timeout User",
                "is_superadmin": False,
                "last_activity": last_activity,
                "csrf_token": "csrf-test-token",
                "auto_login_active": False,
            }
        )
        return f"licican_session={signer.dumps(payload)}"
