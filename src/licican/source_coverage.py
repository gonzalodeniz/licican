from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = BASE_DIR / "data" / "source_coverage.json"
VALID_STATUSES = ("MVP", "Posterior", "Por definir")


@dataclass(frozen=True)
class SourceCoverage:
    nombre: str
    categoria: str
    estado: str
    descripcion: str
    alcance: str
    referencia_funcional: str


def load_source_coverage(path: Path = DEFAULT_DATA_PATH) -> list[SourceCoverage]:
    raw_data = json.loads(path.read_text(encoding="utf-8"))
    sources = [SourceCoverage(**item) for item in raw_data["sources"]]

    invalid_statuses = sorted({source.estado for source in sources if source.estado not in VALID_STATUSES})
    if invalid_statuses:
        raise ValueError(f"Estados de cobertura no soportados: {', '.join(invalid_statuses)}")

    return sources


def summary_by_status(sources: list[SourceCoverage]) -> dict[str, int]:
    summary = {status: 0 for status in VALID_STATUSES}
    for source in sources:
        summary[source.estado] += 1
    return summary
