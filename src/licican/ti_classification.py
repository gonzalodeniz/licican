from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_RULES_PATH = BASE_DIR / "data" / "ti_classification_rules.json"
VALID_CLASSIFICATIONS = ("TI", "No TI", "Caso frontera")


@dataclass(frozen=True)
class ClassificationExample:
    id: str
    titulo: str
    descripcion: str
    cpvs: tuple[str, ...]
    clasificacion_esperada: str
    motivo: str


@dataclass(frozen=True)
class ClassificationRuleSet:
    referencia_funcional: str
    inclusion_palabras_clave: tuple[str, ...]
    inclusion_cpv_prefixes: tuple[str, ...]
    inclusion_necesidades_explicitas: tuple[str, ...]
    exclusion_palabras_clave: tuple[str, ...]
    frontera_palabras_clave: tuple[str, ...]
    ejemplos: tuple[ClassificationExample, ...]


@dataclass(frozen=True)
class OpportunityCandidate:
    titulo: str
    descripcion: str
    cpvs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClassificationDecision:
    clasificacion: str
    coincidencias_inclusion: tuple[str, ...]
    coincidencias_exclusion: tuple[str, ...]
    coincidencias_frontera: tuple[str, ...]
    motivo: str


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _matches_terms(text: str, terms: tuple[str, ...]) -> tuple[str, ...]:
    normalized_text = _normalize(text)
    return tuple(term for term in terms if _normalize(term) in normalized_text)


def _matches_cpv_prefixes(cpvs: tuple[str, ...], prefixes: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(prefix for prefix in prefixes if any(cpv.startswith(prefix) for cpv in cpvs))


def load_rule_set(path: Path = DEFAULT_RULES_PATH) -> ClassificationRuleSet:
    payload = json.loads(path.read_text(encoding="utf-8"))
    examples = tuple(
        ClassificationExample(
            id=item["id"],
            titulo=item["titulo"],
            descripcion=item["descripcion"],
            cpvs=tuple(item["cpvs"]),
            clasificacion_esperada=item["clasificacion_esperada"],
            motivo=item["motivo"],
        )
        for item in payload["ejemplos"]
    )

    invalid = sorted(
        {
            example.clasificacion_esperada
            for example in examples
            if example.clasificacion_esperada not in VALID_CLASSIFICATIONS
        }
    )
    if invalid:
        raise ValueError(f"Clasificaciones TI no soportadas: {', '.join(invalid)}")

    return ClassificationRuleSet(
        referencia_funcional=payload["referencia_funcional"],
        inclusion_palabras_clave=tuple(payload["inclusion"]["palabras_clave"]),
        inclusion_cpv_prefixes=tuple(payload["inclusion"]["cpv_prefixes"]),
        inclusion_necesidades_explicitas=tuple(payload["inclusion"]["necesidades_explicitas"]),
        exclusion_palabras_clave=tuple(payload["exclusion"]["palabras_clave"]),
        frontera_palabras_clave=tuple(payload["casos_frontera"]["palabras_clave"]),
        ejemplos=examples,
    )


def classify_opportunity(candidate: OpportunityCandidate, rules: ClassificationRuleSet) -> ClassificationDecision:
    text = f"{candidate.titulo} {candidate.descripcion}".strip()
    inclusion = (
        _matches_terms(text, rules.inclusion_palabras_clave)
        + _matches_terms(text, rules.inclusion_necesidades_explicitas)
        + _matches_cpv_prefixes(candidate.cpvs, rules.inclusion_cpv_prefixes)
    )
    exclusion = _matches_terms(text, rules.exclusion_palabras_clave)
    frontera = _matches_terms(text, rules.frontera_palabras_clave)

    if frontera or (inclusion and exclusion):
        clasificacion = "Caso frontera"
        motivo = "Requiere validación funcional adicional por señales ambiguas, mixtas o fronterizas."
    elif inclusion:
        clasificacion = "TI"
        motivo = "Existe evidencia funcional suficiente de relevancia TI por palabras clave, necesidad explícita o CPV."
    elif exclusion:
        clasificacion = "No TI"
        motivo = "El contenido encaja en exclusiones funcionales no TI y no aporta evidencia tecnológica suficiente."
    else:
        clasificacion = "No TI"
        motivo = "No se ha encontrado evidencia funcional suficiente para clasificar la oportunidad como TI."

    return ClassificationDecision(
        clasificacion=clasificacion,
        coincidencias_inclusion=inclusion,
        coincidencias_exclusion=exclusion,
        coincidencias_frontera=frontera,
        motivo=motivo,
    )


def audit_examples(rules: ClassificationRuleSet) -> list[dict[str, object]]:
    audited = []
    for example in rules.ejemplos:
        candidate = OpportunityCandidate(
            titulo=example.titulo,
            descripcion=example.descripcion,
            cpvs=example.cpvs,
        )
        decision = classify_opportunity(candidate, rules)
        audited.append(
            {
                "id": example.id,
                "titulo": example.titulo,
                "descripcion": example.descripcion,
                "cpvs": list(example.cpvs),
                "clasificacion_esperada": example.clasificacion_esperada,
                "clasificacion_obtenida": decision.clasificacion,
                "coincidencias_inclusion": list(decision.coincidencias_inclusion),
                "coincidencias_exclusion": list(decision.coincidencias_exclusion),
                "coincidencias_frontera": list(decision.coincidencias_frontera),
                "motivo_ejemplo": example.motivo,
                "motivo_regla": decision.motivo,
                "coincide_con_esperado": decision.clasificacion == example.clasificacion_esperada,
            }
        )
    return audited
