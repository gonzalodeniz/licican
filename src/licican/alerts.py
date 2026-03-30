from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from licican.opportunity_catalog import CatalogFilters, DEFAULT_DATA_PATH, build_catalog


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ALERTS_PATH = BASE_DIR / "data" / "alerts.json"
DEFAULT_REFERENCE = "PB-004 · HU-04 · CU-04 · Registro interno de alertas tempranas del MVP"
NON_ACTIONABLE_STATES = {"anulada", "desierta", "desistida"}


@dataclass(frozen=True)
class AlertMatch:
    id: str
    titulo: str
    organismo: str
    ubicacion: str
    procedimiento: str | None
    presupuesto: int | None
    fecha_publicacion_oficial: str
    fecha_limite: str
    estado: str
    fuente_oficial: str
    url_fuente_oficial: str


@dataclass(frozen=True)
class SavedAlert:
    id: str
    activa: bool
    creada_en: str
    actualizada_en: str
    filtros: CatalogFilters
    coincidencias: tuple[AlertMatch, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "id": self.id,
            "activa": self.activa,
            "creada_en": self.creada_en,
            "actualizada_en": self.actualizada_en,
            "filtros": self.filtros.active_filters(),
            "coincidencias": [match.__dict__ for match in self.coincidencias],
        }


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _filters_from_payload(payload: dict[str, object]) -> CatalogFilters:
    return CatalogFilters(
        palabra_clave=payload.get("palabra_clave"),
        presupuesto_min=payload.get("presupuesto_min"),
        presupuesto_max=payload.get("presupuesto_max"),
        procedimiento=payload.get("procedimiento"),
        ubicacion=payload.get("ubicacion"),
    ).normalized()


def _matches_from_payload(items: list[dict[str, object]]) -> tuple[AlertMatch, ...]:
    return tuple(
        AlertMatch(
            id=item["id"],
            titulo=item["titulo"],
            organismo=item["organismo"],
            ubicacion=item["ubicacion"],
            procedimiento=item.get("procedimiento"),
            presupuesto=item.get("presupuesto"),
            fecha_publicacion_oficial=item["fecha_publicacion_oficial"],
            fecha_limite=item["fecha_limite"],
            estado=item["estado"],
            fuente_oficial=item["fuente_oficial"],
            url_fuente_oficial=item["url_fuente_oficial"],
        )
        for item in items
    )


def load_alerts(path: Path = DEFAULT_ALERTS_PATH) -> tuple[str, list[SavedAlert]]:
    if not path.is_file():
        return DEFAULT_REFERENCE, []

    payload = json.loads(path.read_text(encoding="utf-8"))
    reference = payload.get("referencia_funcional", DEFAULT_REFERENCE)
    alerts = [
        SavedAlert(
            id=item["id"],
            activa=bool(item.get("activa", True)),
            creada_en=item["creada_en"],
            actualizada_en=item.get("actualizada_en", item["creada_en"]),
            filtros=_filters_from_payload(item.get("filtros", {})),
            coincidencias=_matches_from_payload(item.get("coincidencias", [])),
        )
        for item in payload.get("alerts", [])
    ]
    return reference, alerts


def summarize_alerts(alerts: list[SavedAlert]) -> dict[str, int]:
    return {
        "total_alertas": len(alerts),
        "alertas_activas": sum(1 for alert in alerts if alert.activa),
        "alertas_inactivas": sum(1 for alert in alerts if not alert.activa),
        "coincidencias_activas": sum(len(alert.coincidencias) for alert in alerts if alert.activa),
    }


def validate_alert_filters(filters: CatalogFilters) -> str | None:
    normalized_filters = filters.normalized()
    validation_error = normalized_filters.validation_error()
    if validation_error is not None:
        return validation_error
    if not normalized_filters.active_filters():
        return (
            "La alerta necesita al menos un criterio funcional entre palabra clave, "
            "presupuesto, procedimiento o ubicacion."
        )
    return None


def _build_alert_matches(
    filters: CatalogFilters,
    catalog_path: Path = DEFAULT_DATA_PATH,
) -> tuple[AlertMatch, ...]:
    payload = build_catalog(path=catalog_path, filters=filters.normalized())
    matches = []
    for item in payload["oportunidades"]:
        if str(item["estado"]).strip().lower() in NON_ACTIONABLE_STATES:
            continue
        matches.append(
            AlertMatch(
                id=item["id"],
                titulo=item["titulo"],
                organismo=item["organismo"],
                ubicacion=item["ubicacion"],
                procedimiento=item.get("procedimiento"),
                presupuesto=item.get("presupuesto"),
                fecha_publicacion_oficial=item["fecha_publicacion_oficial"],
                fecha_limite=item["fecha_limite"],
                estado=item["estado"],
                fuente_oficial=item["fuente_oficial"],
                url_fuente_oficial=item["url_fuente_oficial"],
            )
        )
    return tuple(matches)


def _next_alert_id(alerts: list[SavedAlert]) -> str:
    next_number = len(alerts) + 1
    existing_ids = {alert.id for alert in alerts}
    while True:
        candidate = f"alerta-{next_number:03d}"
        if candidate not in existing_ids:
            return candidate
        next_number += 1


def _save_alerts(reference: str, alerts: list[SavedAlert], path: Path) -> None:
    payload = {
        "referencia_funcional": reference,
        "alerts": [alert.to_payload() for alert in alerts],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_alert(
    filters: CatalogFilters,
    path: Path = DEFAULT_ALERTS_PATH,
    catalog_path: Path = DEFAULT_DATA_PATH,
    now: str | None = None,
) -> SavedAlert:
    validation_error = validate_alert_filters(filters)
    if validation_error is not None:
        raise ValueError(validation_error)

    reference, alerts = load_alerts(path)
    timestamp = now or _current_timestamp()
    saved_alert = SavedAlert(
        id=_next_alert_id(alerts),
        activa=True,
        creada_en=timestamp,
        actualizada_en=timestamp,
        filtros=filters.normalized(),
        coincidencias=_build_alert_matches(filters, catalog_path),
    )
    alerts.append(saved_alert)
    _save_alerts(reference, alerts, path)
    return saved_alert


def update_alert(
    alert_id: str,
    filters: CatalogFilters,
    path: Path = DEFAULT_ALERTS_PATH,
    catalog_path: Path = DEFAULT_DATA_PATH,
    now: str | None = None,
) -> SavedAlert:
    validation_error = validate_alert_filters(filters)
    if validation_error is not None:
        raise ValueError(validation_error)

    reference, alerts = load_alerts(path)
    timestamp = now or _current_timestamp()
    for index, current_alert in enumerate(alerts):
        if current_alert.id != alert_id:
            continue
        updated_alert = SavedAlert(
            id=current_alert.id,
            activa=current_alert.activa,
            creada_en=current_alert.creada_en,
            actualizada_en=timestamp,
            filtros=filters.normalized(),
            coincidencias=_build_alert_matches(filters, catalog_path),
        )
        alerts[index] = updated_alert
        _save_alerts(reference, alerts, path)
        return updated_alert
    raise KeyError(alert_id)


def deactivate_alert(
    alert_id: str,
    path: Path = DEFAULT_ALERTS_PATH,
    now: str | None = None,
) -> SavedAlert:
    reference, alerts = load_alerts(path)
    timestamp = now or _current_timestamp()
    for index, current_alert in enumerate(alerts):
        if current_alert.id != alert_id:
            continue
        updated_alert = SavedAlert(
            id=current_alert.id,
            activa=False,
            creada_en=current_alert.creada_en,
            actualizada_en=timestamp,
            filtros=current_alert.filtros,
            coincidencias=current_alert.coincidencias,
        )
        alerts[index] = updated_alert
        _save_alerts(reference, alerts, path)
        return updated_alert
    raise KeyError(alert_id)
