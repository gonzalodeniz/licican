from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = BASE_DIR / "data" / "real_source_prioritization.json"
VALID_WAVES = ("Ola 1", "Ola 2", "Ola 3")


@dataclass(frozen=True)
class PrioritizedRealSource:
    nombre: str
    ola: str
    url_oficial: str
    categoria: str
    prioridad: int
    alcance: str
    justificacion: str
    trazabilidad: str


def load_real_source_prioritization(
    path: Path = DEFAULT_DATA_PATH,
) -> tuple[str, list[PrioritizedRealSource], tuple[str, ...]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    sources = [PrioritizedRealSource(**item) for item in payload["sources"]]

    invalid_waves = sorted({source.ola for source in sources if source.ola not in VALID_WAVES})
    if invalid_waves:
        raise ValueError(f"Olas de priorizacion no soportadas: {', '.join(invalid_waves)}")

    ordered_sources = sorted(sources, key=lambda source: source.prioridad)
    out_of_scope = tuple(payload.get("fuera_de_alcance", ()))
    return payload["referencia_funcional"], ordered_sources, out_of_scope


def summarize_prioritization(sources: list[PrioritizedRealSource]) -> dict[str, int]:
    summary = {wave: 0 for wave in VALID_WAVES}
    for source in sources:
        summary[source.ola] += 1
    return summary
