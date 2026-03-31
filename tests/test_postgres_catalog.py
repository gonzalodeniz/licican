from __future__ import annotations

import unittest
from datetime import datetime, timezone
from unittest.mock import patch

import psycopg2

from licican.opportunity_catalog import build_catalog, build_opportunity_detail, load_opportunity_records
from licican.shared.filters import CatalogFilters
from licican.postgres_catalog import PostgresCatalogError, load_postgres_opportunity_records


class _FakeCursor:
    def __init__(self, rows):
        self.rows = rows
        self.executed_sql = None
        self.executed_params = None

    def execute(self, sql, params=None):
        self.executed_sql = sql
        self.executed_params = params

    def fetchall(self):
        return self.rows

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConnection:
    def __init__(self, rows):
        self.rows = rows

    def cursor(self, cursor_factory=None):
        return _FakeCursor(self.rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class PostgresCatalogTests(unittest.TestCase):
    def test_load_opportunity_records_can_read_from_postgresql(self) -> None:
        rows = [
            {
                "expediente_id": "SUM/2026/0000004663",
                "id_plataforma": "https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/19207228",
                "titulo": "Suscripción de ocho licencias software",
                "resumen": "Licencias para plataforma corporativa.",
                "organo_contratacion": "Secretaría General Técnica de Hacienda",
                "ubicacion_comunidad": "Canarias",
                "ubicacion_nuts": "ES70",
                "procedimiento": "9",
                "presupuesto_base": 26750,
                "updated_at": datetime(2026, 3, 28, 20, 2, 34, tzinfo=timezone.utc),
                "fecha_limite_presentacion": datetime(2026, 3, 25, 14, 0, 0, tzinfo=timezone.utc),
                "estado": "EV",
                "organo_perfil_url": "https://www.gobiernodecanarias.org/perfil_del_contratante/",
                "link_detalle": "https://contrataciondelestado.es/detalle/19207228",
                "cpv_codes": ["48600000"],
                "fichero_origen": "licitacionesPerfilesContratanteCompleto3_20260328_200234.atom",
                "jerarquia_org": ["Canarias"],
            }
        ]

        with patch.dict("os.environ", {"DB_PASSWORD": "secreto"}, clear=False):
            with patch("licican.postgres_catalog.psycopg2.connect", return_value=_FakeConnection(rows)):
                reference, records = load_opportunity_records(backend="postgres")

        self.assertIn("T-001", reference)
        self.assertEqual(1, len(records))
        self.assertEqual("sum-2026-0000004663", records[0].id)
        self.assertEqual("Abierto simplificado", records[0].procedimiento)
        self.assertEqual("En evaluacion", records[0].estado)
        self.assertEqual("Canarias", records[0].ubicacion)
        self.assertEqual("licitacionesPerfilesContratanteCompleto3_20260328_200234.atom", records[0].fichero_origen_atom)

    def test_build_catalog_applies_filters_over_postgresql_records(self) -> None:
        rows = [
            {
                "expediente_id": "A-2026",
                "id_plataforma": "1",
                "titulo": "Servicio cloud de backup",
                "resumen": "Backup y continuidad",
                "organo_contratacion": "Gobierno de Canarias",
                "ubicacion_comunidad": "Canarias",
                "ubicacion_nuts": "ES70",
                "procedimiento": "1",
                "presupuesto_base": 100000,
                "updated_at": datetime(2026, 3, 28, 10, 0, 0, tzinfo=timezone.utc),
                "fecha_limite_presentacion": datetime(2026, 4, 10, 10, 0, 0, tzinfo=timezone.utc),
                "estado": "PUB",
                "organo_perfil_url": None,
                "link_detalle": "https://contrataciondelestado.es/detalle/1",
                "cpv_codes": ["72222300"],
                "fichero_origen": "snapshot.atom",
                "jerarquia_org": ["Canarias"],
            },
            {
                "expediente_id": "B-2026",
                "id_plataforma": "2",
                "titulo": "Suministro de licencias",
                "resumen": "Licencias de plataforma",
                "organo_contratacion": "Cabildo de Tenerife",
                "ubicacion_comunidad": "Canarias",
                "ubicacion_nuts": "ES70",
                "procedimiento": "9",
                "presupuesto_base": 26000,
                "updated_at": datetime(2026, 3, 27, 10, 0, 0, tzinfo=timezone.utc),
                "fecha_limite_presentacion": datetime(2026, 4, 12, 10, 0, 0, tzinfo=timezone.utc),
                "estado": "EV",
                "organo_perfil_url": None,
                "link_detalle": "https://contrataciondelestado.es/detalle/2",
                "cpv_codes": ["48600000"],
                "fichero_origen": "snapshot.atom",
                "jerarquia_org": ["Canarias"],
            },
        ]

        with patch.dict("os.environ", {"DB_PASSWORD": "secreto"}, clear=False):
            with patch("licican.postgres_catalog.psycopg2.connect", return_value=_FakeConnection(rows)):
                payload = build_catalog(
                    filters=CatalogFilters(procedimiento="Abierto"),
                    backend="postgres",
                )

        self.assertEqual(2, payload["total_registros_origen"])
        self.assertEqual(2, payload["total_oportunidades_visibles"])
        self.assertEqual(1, payload["total_oportunidades_catalogo"])
        self.assertEqual(["a-2026"], [item["id"] for item in payload["oportunidades"]])

    def test_build_catalog_preserves_specific_location_for_combined_postgresql_filters(self) -> None:
        rows = [
            {
                "expediente_id": "EXP-001",
                "id_plataforma": "1",
                "titulo": "Suministro de licencias corporativas",
                "resumen": "Licencias y soporte de plataforma",
                "organo_contratacion": "Cabildo de Tenerife",
                "ubicacion_comunidad": "Canarias",
                "ubicacion_nuts": "ES70",
                "procedimiento": "9",
                "presupuesto_base": 97000,
                "updated_at": datetime(2026, 3, 28, 10, 0, 0, tzinfo=timezone.utc),
                "fecha_limite_presentacion": datetime(2026, 4, 10, 10, 0, 0, tzinfo=timezone.utc),
                "estado": "PUB",
                "organo_perfil_url": None,
                "link_detalle": "https://contrataciondelestado.es/detalle/1",
                "cpv_codes": ["48600000"],
                "fichero_origen": "snapshot.atom",
                "jerarquia_org": [
                    "Cabildo Insular de Tenerife",
                    "Santa Cruz de Tenerife",
                    "Canarias",
                    "ENTIDADES LOCALES",
                    "Sector Publico",
                ],
            }
        ]

        with patch.dict("os.environ", {"DB_PASSWORD": "secreto"}, clear=False):
            with patch("licican.postgres_catalog.psycopg2.connect", return_value=_FakeConnection(rows)):
                payload = build_catalog(
                    filters=CatalogFilters(
                        palabra_clave="licencias",
                        presupuesto_min=90000,
                        presupuesto_max=120000,
                        procedimiento="Abierto simplificado",
                        ubicacion="Santa Cruz de Tenerife",
                    ),
                    backend="postgres",
                )

        self.assertEqual(["exp-001"], [item["id"] for item in payload["oportunidades"]])
        self.assertEqual("Santa Cruz de Tenerife", payload["oportunidades"][0]["ubicacion"])

    def test_build_opportunity_detail_returns_none_when_record_is_not_visible(self) -> None:
        rows = []
        with patch.dict("os.environ", {"DB_PASSWORD": "secreto"}, clear=False):
            with patch("licican.postgres_catalog.psycopg2.connect", return_value=_FakeConnection(rows)):
                detail = build_opportunity_detail("inexistente", backend="postgres")

        self.assertIsNone(detail)

    def test_build_catalog_raises_controlled_error_when_postgresql_fails(self) -> None:
        with patch.dict("os.environ", {"DB_PASSWORD": "secreto"}, clear=False):
            with patch(
                "licican.postgres_catalog.psycopg2.connect",
                side_effect=psycopg2.OperationalError("db down"),
            ):
                with self.assertRaisesRegex(Exception, "No se pudo cargar el catalogo desde PostgreSQL"):
                    build_catalog(backend="postgres")

    def test_build_catalog_requires_postgresql_credentials_when_no_url_is_configured(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "LICICAN_CATALOG_BACKEND": "postgres",
                "LICICAN_DATABASE_URL": "",
                "DATABASE_URL": "",
                "DB_HOST": "",
                "DB_PORT": "",
                "DB_NAME": "",
                "DB_USER": "",
                "DB_PASSWORD": "",
            },
            clear=False,
        ):
            with self.assertRaisesRegex(
                PostgresCatalogError,
                "No se ha configurado conexión a PostgreSQL. Define LICICAN_DATABASE_URL o las variables DB_\\*.",
            ):
                load_postgres_opportunity_records()
