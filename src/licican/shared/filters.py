from __future__ import annotations

from dataclasses import dataclass

from licican.shared.text import clean_text


@dataclass(frozen=True)
class CatalogFilters:
    """Representa los filtros funcionales del catálogo."""

    palabra_clave: str | None = None
    presupuesto_min: int | None = None
    presupuesto_max: int | None = None
    procedimiento: str | None = None
    ubicacion: str | None = None

    def normalized(self) -> "CatalogFilters":
        return CatalogFilters(
            palabra_clave=clean_text(self.palabra_clave),
            presupuesto_min=self.presupuesto_min,
            presupuesto_max=self.presupuesto_max,
            procedimiento=clean_text(self.procedimiento),
            ubicacion=clean_text(self.ubicacion),
        )

    def active_filters(self) -> dict[str, object]:
        return {
            key: value
            for key, value in {
                "palabra_clave": self.palabra_clave,
                "presupuesto_min": self.presupuesto_min,
                "presupuesto_max": self.presupuesto_max,
                "procedimiento": self.procedimiento,
                "ubicacion": self.ubicacion,
            }.items()
            if value not in (None, "")
        }

    def validation_error(self) -> str | None:
        if (
            self.presupuesto_min is not None
            and self.presupuesto_max is not None
            and self.presupuesto_min > self.presupuesto_max
        ):
            return (
                "El presupuesto mínimo no puede ser mayor que el presupuesto máximo. "
                "Revisa el rango antes de aplicar los filtros."
            )
        return None
