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

from licican.auth.config import get_auth_settings
from licican.auth.rate_limiter import rate_limiter
from licican.auth.service import (
    AUTH_USER_BOOTSTRAP_SQL,
    AUTH_USER_DEACTIVATE_SQL,
    AUTH_USER_INSERT_SQL,
    AUTH_USER_LAST_LOGIN_SQL,
    AUTH_USER_SELECT_SQL,
    AUTH_USER_UPDATE_SUPERADMIN_SQL,
    synchronize_superadmin_account,
)
from tests.test_app import invoke_app


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
        if normalized == AUTH_USER_SELECT_SQL.strip():
            login_name = str(params[0])
            email = str(params[1]) if params and len(params) > 1 else login_name
            record = self.state.get(login_name)
            if record is None:
                record = next((row for row in self.state.values() if row.get("email") == email), None)
            self.row = deepcopy(record) if record is not None else None
            return
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
                invitacion_pendiente,
                username,
                password_hash,
                nombre_completo,
                rol,
                activo,
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
                "invitacion_pendiente": bool(invitacion_pendiente),
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
                invitacion_pendiente,
                username,
                password_hash,
                nombre_completo,
                rol,
                activo,
                ultimo_login,
                updated_at,
                user_id,
            ) = params
            for record in self.state.values():
                if record["id"] == user_id:
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
                            "invitacion_pendiente": bool(invitacion_pendiente),
                            "username": str(username),
                            "password_hash": str(password_hash),
                            "nombre_completo": str(nombre_completo),
                            "rol": str(rol),
                            "activo": bool(activo),
                            "ultimo_login": ultimo_login,
                            "updated_at": updated_at,
                        }
                    )
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        if normalized == AUTH_USER_DEACTIVATE_SQL.strip():
            updated_at, user_id = params
            for record in self.state.values():
                if record["id"] == user_id:
                    record["estado"] = "inactivo"
                    record["activo"] = False
                    record["invitacion_pendiente"] = False
                    record["updated_at"] = updated_at
                    return
            raise AssertionError(f"Usuario no encontrado en test auth: {user_id}")
        raise AssertionError(f"SQL inesperado en prueba auth: {normalized}")

    def fetchone(self) -> dict[str, object] | None:
        return deepcopy(self.row) if self.row is not None else None

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
    activo: bool = True,
) -> dict[str, object]:
    nombre, _, apellidos = nombre_completo.partition(" ")
    if not apellidos:
        apellidos = "Licican"
    email = email or (username if "@" in username else f"{username}@licican.local")
    current = datetime.now(UTC).replace(microsecond=0)
    return {
        "id": user_id,
        "nombre": nombre,
        "apellidos": apellidos,
        "email": email,
        "rol_principal": rol,
        "estado": "activo" if activo else "inactivo",
        "observaciones_internas": "",
        "fecha_alta": current,
        "ultimo_acceso": None,
        "invitacion_pendiente": False,
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
            "LOGIN_SUPERADMIN_NAME": "admin",
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
                body=f"username=admin&password=admin12345&csrf_token={csrf_token}",
            )
            page_status, _, page_body = browser.request("/")

        self.assertEqual("200 OK", status)
        self.assertEqual("302 Found", login_status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("Cerrar sesión", page_body.decode("utf-8"))
        self.assertIn("admin", auth_state)
        self.assertEqual("activo", auth_state["admin"]["estado"])
        self.assertEqual("administrador", auth_state["admin"]["rol_principal"])
        self.assertEqual("superadmin@licitan.local", auth_state["admin"]["email"])
        self.assertEqual("Superadministrador", auth_state["admin"]["nombre"])
        self.assertEqual("Licican", auth_state["admin"]["apellidos"])
        self.assertTrue(auth_state["admin"]["activo"])
        self.assertTrue(bcrypt.checkpw("admin12345".encode("utf-8"), auth_state["admin"]["password_hash"].encode("utf-8")))

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
                body=f"username=admin&password=admin12345&csrf_token={csrf_token}",
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
                body=f"username=admin&password=admin12345&csrf_token={csrf_token}",
            )

        self.assertEqual("401 Unauthorized", status)
        self.assertIn("Usuario o contraseña incorrectos.", response_body.decode("utf-8"))

    def test_login_with_database_user_creates_session(self) -> None:
        browser = _BrowserSession()
        auth_state = {
            "admin": _build_user_record(
                user_id=9,
                username="admin",
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
            page_status, _, page_body = browser.request("/kpis")

        self.assertEqual("302 Found", status)
        self.assertEqual("/licican/", headers["Location"])
        self.assertEqual("200 OK", page_status)
        self.assertIn("KPIs iniciales de cobertura, adopción y uso", page_body.decode("utf-8"))
        self.assertIsNotNone(auth_state["marta"]["ultimo_login"])
        self.assertEqual("activo", auth_state["admin"]["estado"])
        self.assertTrue(auth_state["admin"]["activo"])
        self.assertTrue(bcrypt.checkpw("admin12345".encode("utf-8"), auth_state["admin"]["password_hash"].encode("utf-8")))

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
        self.assertIn("admin", auth_state)

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
        self.assertIn("Usuario desactivado. Contacte al administrador.", response_body.decode("utf-8"))
        self.assertEqual("inactivo", auth_state["soporte"]["estado"])

    def test_superadmin_disabled_marks_database_user_inactive(self) -> None:
        auth_state = {
            "admin": _build_user_record(
                user_id=7,
                username="admin",
                password="admin12345",
                nombre_completo="Superadministrador",
                rol="administrador",
                activo=True,
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="false", LOGIN_AUTOMATICO="false"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        self.assertFalse(auth_state["admin"]["activo"])
        self.assertEqual("inactivo", auth_state["admin"]["estado"])

    def test_superadmin_enabled_reactivates_user_and_updates_password(self) -> None:
        auth_state = {
            "admin": _build_user_record(
                user_id=7,
                username="admin",
                password="vieja12345",
                nombre_completo="Superadministrador",
                rol="administrador",
                activo=False,
            )
        }
        with ExitStack() as stack:
            stack.enter_context(self._manual_env(LOGIN_SUPERADMIN_ENABLED="true", LOGIN_AUTOMATICO="false", LOGIN_SUPERADMIN_PASS="nueva12345"))
            stack.enter_context(patch("licican.auth.service.psycopg2.connect", side_effect=lambda *args, **kwargs: _fake_auth_connect(auth_state)))
            synchronize_superadmin_account(get_auth_settings())

        self.assertTrue(auth_state["admin"]["activo"])
        self.assertEqual("activo", auth_state["admin"]["estado"])
        self.assertEqual("administrador", auth_state["admin"]["rol_principal"])
        self.assertTrue(bcrypt.checkpw("nueva12345".encode("utf-8"), auth_state["admin"]["password_hash"].encode("utf-8")))

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

        self.assertIn("admin", auth_state)
        self.assertEqual("Superadministrador", auth_state["admin"]["nombre"])
        self.assertEqual("Licican", auth_state["admin"]["apellidos"])
        self.assertEqual("superadmin@licitan.local", auth_state["admin"]["email"])
        self.assertEqual("administrador", auth_state["admin"]["rol_principal"])
        self.assertEqual("activo", auth_state["admin"]["estado"])

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
        self.assertEqual("/licican/login?reason=logout", headers["Location"])
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
