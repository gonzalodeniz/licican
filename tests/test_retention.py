from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from licican import retention as retention_module


def _ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class _RetentionState:
    def __init__(self) -> None:
        self.policy = {
            "antiguedad_dias": 30,
            "modo": "cerradas",
            "actualizada_en": _ts("2026-04-03T09:00:00Z"),
        }
        self.rows = [
            {
                "id_plataforma": "https://example.test/1",
                "expediente": "EXP-001",
                "titulo": "Servicio cloud activo",
                "organo_contratacion": "Gobierno de Canarias",
                "estado": "PUB",
                "fecha_importacion": _ts("2026-02-01T10:00:00Z"),
                "updated_at": _ts("2026-04-01T10:00:00Z"),
            },
            {
                "id_plataforma": "https://example.test/2",
                "expediente": "EXP-002",
                "titulo": "Licitacion cerrada para archivar",
                "organo_contratacion": "Cabildo de Tenerife",
                "estado": "RES",
                "fecha_importacion": _ts("2026-01-01T10:00:00Z"),
                "updated_at": _ts("2026-02-15T10:00:00Z"),
            },
            {
                "id_plataforma": "https://example.test/3",
                "expediente": "EXP-003",
                "titulo": "Licitacion cerrada reciente",
                "organo_contratacion": "Cabildo de Gran Canaria",
                "estado": "ADJ",
                "fecha_importacion": _ts("2026-03-15T10:00:00Z"),
                "updated_at": _ts("2026-03-25T10:00:00Z"),
            },
        ]
        self.archived_rows: list[dict[str, object]] = []


class _FakeCursor:
    def __init__(self, state: _RetentionState):
        self.state = state
        self.rows: list[dict[str, object]] = []
        self.rowcount = 0

    def execute(self, sql, params=None):
        normalized = str(sql).strip()
        self.rowcount = 0
        if normalized == retention_module.RETENTION_SCHEMA_BOOTSTRAP_SQL.strip():
            self.rows = []
            return
        if normalized == retention_module.RETENTION_POLICY_SELECT_SQL.strip():
            self.rows = [dict(self.state.policy)]
            return
        if normalized == retention_module.RETENTION_POLICY_UPSERT_SQL.strip():
            antiguedad_dias, modo = params
            self.state.policy = {
                "antiguedad_dias": int(antiguedad_dias),
                "modo": str(modo),
                "actualizada_en": _ts("2026-04-03T10:00:00Z"),
            }
            self.rows = [dict(self.state.policy)]
            self.rowcount = 1
            return
        if normalized == retention_module.RETENTION_RECORDS_SELECT_SQL.strip():
            self.rows = [dict(row) for row in self.state.rows]
            return
        if normalized == retention_module.ARCHIVED_COUNT_SQL.strip():
            self.rows = [{"total": len(self.state.archived_rows)}]
            return
        if normalized == retention_module.ARCHIVE_RECORDS_INSERT_SQL.strip():
            _, modo, antiguedad_dias, ids = params
            selected = [dict(row) for row in self.state.rows if row["id_plataforma"] in set(ids)]
            for row in selected:
                archived = dict(row)
                archived["politica_modo"] = modo
                archived["politica_antiguedad_dias"] = antiguedad_dias
                self.state.archived_rows.append(archived)
            self.rowcount = len(selected)
            self.rows = []
            return
        if normalized == retention_module.ARCHIVE_RECORDS_DELETE_SQL.strip():
            ids = set(params[0])
            before = len(self.state.rows)
            self.state.rows = [row for row in self.state.rows if row["id_plataforma"] not in ids]
            self.rowcount = before - len(self.state.rows)
            self.rows = []
            return
        raise AssertionError(f"SQL no controlado en pruebas: {normalized}")

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return list(self.rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConnection:
    def __init__(self, state: _RetentionState):
        self.state = state

    def cursor(self, cursor_factory=None):
        return _FakeCursor(self.state)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class RetentionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.previous_bootstrap = retention_module._SCHEMA_BOOTSTRAPPED
        retention_module._SCHEMA_BOOTSTRAPPED = False

    def tearDown(self) -> None:
        retention_module._SCHEMA_BOOTSTRAPPED = self.previous_bootstrap

    def test_build_retention_payload_classifies_operational_records(self) -> None:
        state = _RetentionState()
        pipeline_payload = {
            "referencia_funcional": "PB-005",
            "pipeline": [
                {
                    "opportunity_id": "exp-001",
                    "usuario_id": "usr-001",
                    "estado_seguimiento": "Evaluando",
                    "creada_en": "2026-03-01T10:00:00Z",
                    "actualizada_en": "2026-04-01T10:00:00Z",
                    "oportunidad": {
                        "id": "exp-001",
                        "titulo": "Servicio cloud activo",
                        "organismo": "Gobierno de Canarias",
                        "ubicacion": "Canarias",
                        "procedimiento": "Abierto",
                        "presupuesto": 120000,
                        "fecha_publicacion_oficial": "2026-03-01",
                        "fecha_limite": "2026-04-10",
                        "estado_oficial": "Publicada",
                        "fuente_oficial": "PCSP",
                        "url_fuente_oficial": "https://example.test/1",
                    },
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            pipeline_path.write_text(json.dumps(pipeline_payload), encoding="utf-8")
            with patch("licican.retention.psycopg2.connect", return_value=_FakeConnection(state)):
                payload = retention_module.build_retention_payload(
                    pipeline_path=pipeline_path,
                    now=_ts("2026-04-03T10:00:00Z"),
                )

        self.assertEqual(1, payload["resumen"]["mantener_activas"])
        self.assertEqual(1, payload["resumen"]["archivar"])
        self.assertEqual(1, payload["resumen"]["conservar"])
        self.assertEqual("exp-002", payload["grupos"]["archivar"][0]["slug"])

    def test_update_retention_policy_persists_new_values(self) -> None:
        state = _RetentionState()

        with patch("licican.retention.psycopg2.connect", return_value=_FakeConnection(state)):
            updated = retention_module.update_retention_policy(antiguedad_dias=45, modo="desde_creacion")

        self.assertEqual(45, updated.antiguedad_dias)
        self.assertEqual("desde_creacion", updated.modo)
        self.assertEqual(45, state.policy["antiguedad_dias"])

    def test_apply_retention_policy_moves_archivable_rows_to_archive(self) -> None:
        state = _RetentionState()
        pipeline_payload = {"referencia_funcional": "PB-005", "pipeline": []}

        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            pipeline_path.write_text(json.dumps(pipeline_payload), encoding="utf-8")
            with patch("licican.retention.psycopg2.connect", return_value=_FakeConnection(state)):
                result = retention_module.apply_retention_policy(
                    pipeline_path=pipeline_path,
                    now=_ts("2026-04-03T10:00:00Z"),
                )

        self.assertEqual(1, result["archivadas"])
        self.assertEqual(1, len(state.archived_rows))
        self.assertEqual(["EXP-001", "EXP-003"], [row["expediente"] for row in state.rows])
