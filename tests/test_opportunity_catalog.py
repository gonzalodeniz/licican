from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from licican.opportunity_catalog import build_catalog, build_opportunity_detail, load_opportunity_records
from licican.shared.filters import CatalogFilters


def _atom_entry(
    *,
    contract_folder_id: str,
    updated: str,
    title: str,
    summary: str,
    organization: str,
    cpv: str,
    country_subentity_code: str,
    country_subentity: str,
    amount: str,
    deadline: str,
    status: str = "PUB",
    procedure: str = "1",
) -> str:
    return f"""
  <entry xmlns="http://www.w3.org/2005/Atom"
         xmlns:cac="urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2"
         xmlns:cac-place-ext="urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc-place-ext="urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2">
    <id>{contract_folder_id}</id>
    <link href="https://contrataciondelestado.es/detalle/{contract_folder_id}" />
    <summary>{summary}</summary>
    <title>{title}</title>
    <updated>{updated}</updated>
    <cac-place-ext:ContractFolderStatus>
      <cbc:ContractFolderID>{contract_folder_id}</cbc:ContractFolderID>
      <cbc-place-ext:ContractFolderStatusCode>{status}</cbc-place-ext:ContractFolderStatusCode>
      <cac-place-ext:LocatedContractingParty>
        <cac:Party>
          <cac:PartyName>
            <cbc:Name>{organization}</cbc:Name>
          </cac:PartyName>
        </cac:Party>
        <cac-place-ext:ParentLocatedParty>
          <cac:PartyName>
            <cbc:Name>Canarias</cbc:Name>
          </cac:PartyName>
        </cac-place-ext:ParentLocatedParty>
      </cac-place-ext:LocatedContractingParty>
      <cac:ProcurementProject>
        <cbc:Name>{title}</cbc:Name>
        <cac:BudgetAmount>
          <cbc:TotalAmount>{amount}</cbc:TotalAmount>
        </cac:BudgetAmount>
        <cac:RequiredCommodityClassification>
          <cbc:ItemClassificationCode>{cpv}</cbc:ItemClassificationCode>
        </cac:RequiredCommodityClassification>
        <cac:RealizedLocation>
          <cbc:CountrySubentity>{country_subentity}</cbc:CountrySubentity>
          <cbc:CountrySubentityCode>{country_subentity_code}</cbc:CountrySubentityCode>
        </cac:RealizedLocation>
      </cac:ProcurementProject>
      <cac:TenderingProcess>
        <cbc:ProcedureCode>{procedure}</cbc:ProcedureCode>
        <cac:TenderSubmissionDeadlinePeriod>
          <cbc:EndDate>{deadline}</cbc:EndDate>
        </cac:TenderSubmissionDeadlinePeriod>
      </cac:TenderingProcess>
    </cac-place-ext:ContractFolderStatus>
  </entry>
"""


def _atom_feed(*entries: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        + "".join(entries)
        + "</feed>\n"
    )


class OpportunityCatalogTests(unittest.TestCase):
    def test_load_opportunity_records_returns_consolidated_atom_seed_data(self) -> None:
        reference, records = load_opportunity_records(backend="file")

        self.assertIn("PB-001", reference)
        self.assertEqual(5, len(records))
        self.assertEqual("govcan-backup-cloud-2026", records[0].id)
        self.assertTrue(all(record.fichero_origen_atom is None for record in records))

    def test_build_catalog_returns_consolidated_canarias_ti_opportunities(self) -> None:
        catalog = build_catalog(backend="file")

        self.assertEqual(5, catalog["total_registros_origen"])
        self.assertEqual(3, catalog["total_oportunidades_catalogo"])
        self.assertEqual(
            [
                "pcsp-cabildo-licencias-2026",
                "govcan-backup-cloud-2026",
                "cabildo-redes-2026",
            ],
            [item["id"] for item in catalog["oportunidades"]],
        )
        self.assertEqual(1, catalog["paginacion"]["pagina_actual"])
        self.assertEqual(10, catalog["paginacion"]["tamano_pagina"])
        self.assertEqual(1, catalog["paginacion"]["total_paginas"])
        self.assertEqual(1, catalog["paginacion"]["resultado_desde"])
        self.assertEqual(3, catalog["paginacion"]["resultado_hasta"])
        self.assertEqual(3, len(catalog["cobertura_aplicada"]))
        self.assertTrue(all(item["clasificacion_ti"] == "TI" for item in catalog["oportunidades"]))

    def test_build_opportunity_detail_includes_atom_source_filename(self) -> None:
        detail = build_opportunity_detail("pcsp-cabildo-licencias-2026", backend="file")

        assert detail is not None
        self.assertEqual("2026-03-22", detail["fecha_publicacion_oficial"])
        self.assertEqual("2026-04-10", detail["fecha_limite"])
        self.assertEqual(97000, detail["presupuesto"])
        self.assertEqual("Abierta", detail["estado"])
        self.assertIsNone(detail["fichero_origen_atom"])

    def test_build_opportunity_detail_returns_none_for_non_visible_record(self) -> None:
        self.assertIsNone(build_opportunity_detail("govcan-teleco-mixto-2026", backend="file"))

    def test_build_catalog_can_return_empty_catalog(self) -> None:
        payload = {
            "referencia_funcional": "PB-001",
            "opportunities": [
                {
                    "id": "solo-no-ti",
                    "titulo": "Compra de mobiliario de oficina",
                    "descripcion": "Mesas, sillas y armarios.",
                    "organismo": "Gobierno de Canarias",
                    "ubicacion": "Canarias",
                    "procedimiento": "Abierto",
                    "presupuesto": 12000,
                    "fecha_publicacion_oficial": "2026-04-01",
                    "fecha_limite": "2026-05-01",
                    "estado": "Abierta",
                    "fuente_oficial": "Gobierno de Canarias",
                    "url_fuente_oficial": "https://www.gobiernodecanarias.org/perfil_del_contratante/",
                    "cpvs": ["39130000"],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "opportunities.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            catalog = build_catalog(path)

        self.assertEqual(1, catalog["total_registros_origen"])
        self.assertEqual(0, catalog["total_oportunidades_catalogo"])
        self.assertEqual([], catalog["oportunidades"])
        self.assertEqual(1, catalog["paginacion"]["pagina_actual"])
        self.assertEqual(0, catalog["paginacion"]["resultado_desde"])
        self.assertEqual(0, catalog["paginacion"]["resultado_hasta"])

    def test_build_catalog_applies_combined_filters(self) -> None:
        catalog = build_catalog(
            filters=CatalogFilters(
                palabra_clave="licencias",
                presupuesto_min=90000,
                presupuesto_max=120000,
                procedimiento="Abierto simplificado",
                ubicacion="Santa Cruz de Tenerife",
            ),
            backend="file",
        )

        self.assertEqual(3, catalog["total_oportunidades_visibles"])
        self.assertEqual(1, catalog["total_oportunidades_catalogo"])
        self.assertEqual(["pcsp-cabildo-licencias-2026"], [item["id"] for item in catalog["oportunidades"]])
        self.assertEqual(
            {
                "palabra_clave": "licencias",
                "presupuesto_min": 90000,
                "presupuesto_max": 120000,
                "procedimiento": "Abierto simplificado",
                "ubicacion": "Santa Cruz de Tenerife",
            },
            catalog["filtros_activos"],
        )
        self.assertEqual(1, catalog["paginacion"]["total_paginas"])

    def test_build_catalog_excludes_records_without_known_budget_when_range_is_requested(self) -> None:
        catalog = build_catalog(filters=CatalogFilters(presupuesto_max=100000), backend="file")

        self.assertEqual(
            ["pcsp-cabildo-licencias-2026"],
            [item["id"] for item in catalog["oportunidades"]],
        )

    def test_build_catalog_flags_invalid_budget_range_without_treating_it_as_empty_result(self) -> None:
        catalog = build_catalog(
            filters=CatalogFilters(presupuesto_min=120000, presupuesto_max=90000),
            backend="file",
        )

        self.assertEqual(
            "El presupuesto mínimo no puede ser mayor que el presupuesto máximo. "
            "Revisa el rango antes de aplicar los filtros.",
            catalog["error_validacion"],
        )
        self.assertEqual(3, catalog["total_oportunidades_catalogo"])
        self.assertEqual(3, len(catalog["oportunidades"]))

    def test_build_catalog_returns_requested_page_slice(self) -> None:
        catalog = build_catalog(page=2, page_size=2, backend="file")

        self.assertEqual(["cabildo-redes-2026"], [item["id"] for item in catalog["oportunidades"]])
        self.assertEqual(2, catalog["paginacion"]["pagina_actual"])
        self.assertEqual(3, catalog["paginacion"]["resultado_desde"])
        self.assertEqual(3, catalog["paginacion"]["resultado_hasta"])
        self.assertFalse(catalog["paginacion"]["hay_siguiente"])

    def test_build_catalog_normalizes_invalid_requested_page(self) -> None:
        catalog = build_catalog(page=0, backend="file")

        self.assertEqual(1, catalog["paginacion"]["pagina_actual"])
        self.assertTrue(catalog["paginacion"]["ajustada"])
        self.assertEqual("invalida", catalog["paginacion"]["motivo_ajuste"])

    def test_build_catalog_clamps_page_out_of_range(self) -> None:
        catalog = build_catalog(page=9, backend="file")

        self.assertEqual(1, catalog["paginacion"]["pagina_actual"])
        self.assertTrue(catalog["paginacion"]["ajustada"])
        self.assertEqual("fuera_de_rango", catalog["paginacion"]["motivo_ajuste"])
        self.assertEqual(
            ["pcsp-cabildo-licencias-2026", "govcan-backup-cloud-2026", "cabildo-redes-2026"],
            [item["id"] for item in catalog["oportunidades"]],
        )

    def test_load_opportunity_records_consolidates_latest_snapshot_from_atom_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_dir = Path(tmp_dir)
            older_feed = _atom_feed(
                _atom_entry(
                    contract_folder_id="EXP-01/2026",
                    updated="2026-03-20T10:00:00+01:00",
                    title="Servicio TI inicial",
                    summary="Version inicial del expediente.",
                    organization="Cabildo de Tenerife",
                    cpv="72222300",
                    country_subentity_code="ES709",
                    country_subentity="Tenerife",
                    amount="100000",
                    deadline="2026-04-10",
                )
            )
            newer_feed = _atom_feed(
                _atom_entry(
                    contract_folder_id="EXP-01/2026",
                    updated="2026-03-22T12:00:00+01:00",
                    title="Servicio TI consolidado",
                    summary="Version mas reciente del expediente.",
                    organization="Cabildo de Tenerife",
                    cpv="72222300",
                    country_subentity_code="ES709",
                    country_subentity="Tenerife",
                    amount="125000",
                    deadline="2026-04-15",
                )
            )
            (data_dir / "snapshot_1.atom").write_text(older_feed, encoding="utf-8")
            (data_dir / "snapshot_2.atom").write_text(newer_feed, encoding="utf-8")

            reference, records = load_opportunity_records(data_dir)

        self.assertIn("PB-011", reference)
        self.assertEqual(1, len(records))
        self.assertEqual("exp-01-2026", records[0].id)
        self.assertEqual("Servicio TI consolidado", records[0].titulo)
        self.assertEqual(125000, records[0].presupuesto)
        self.assertEqual("snapshot_2.atom", records[0].fichero_origen_atom)
