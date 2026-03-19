# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion oficial de `PodencoTI` separando con claridad el contenido para usuario final, equipo tecnico y administracion.

## Estado documental de referencia
Fecha de revision: `2026-03-19`.

Esta carpeta documenta el estado real verificable de la rama `main`. En esta revision si existe una entrega minima ejecutable, pero su alcance es acotado:

- Vista HTML de cobertura inicial del MVP (`PB-007`).
- API JSON de cobertura de fuentes.
- Vista HTML de clasificacion TI auditable (`PB-006`).
- API JSON de reglas y ejemplos auditados de clasificacion TI.

No existe todavia un catalogo de oportunidades, ficha de detalle, filtros, alertas ni pipeline de seguimiento.

## Audiencias cubiertas
- Usuario final o stakeholder funcional: [manual-usuario.md](manual-usuario.md)
- Equipo tecnico: [manual-tecnico.md](manual-tecnico.md)
- Administracion u operacion: [manual-administracion.md](manual-administracion.md)
- Preparacion local reproducible: [guia-instalacion.md](guia-instalacion.md)
- Despliegue y limites de publicacion: [guia-despliegue.md](guia-despliegue.md)
- Trazabilidad entre vision, backlog, implementacion y operacion: [matriz-trazabilidad.md](matriz-trazabilidad.md)
- Preguntas frecuentes y contradicciones: [faq.md](faq.md)
- Terminologia transversal del proyecto: [glosario.md](glosario.md)

## Hallazgos principales de esta revision
- `main` contiene implementacion Python versionada en `src/podencoti/`, datos en `data/` y pruebas automatizadas en `tests/`.
- `PYTHONPATH=src python3 -m unittest discover -s tests -v` ejecuta 15 pruebas y finaliza correctamente.
- `make test` tambien funciona en un entorno con `.venv` disponible.
- `make run` arranca un servidor WSGI local en `http://127.0.0.1:8000`.
- Las rutas verificables hoy son `/`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti`.
- Las rutas `/oportunidades` y `/api/oportunidades` responden `404 Not Found` en la revision actual.

## Dependencias y contradicciones abiertas
- La vision y el backlog de `product-manager/` describen capacidades futuras validas como fuente funcional, pero esas capacidades aun no estan implementadas en `main`.
- `pyproject.toml` sigue describiendo el paquete como "Cobertura inicial visible de fuentes del MVP de PodencoTI.", aunque `main` ya expone tambien la superficie auditable de `PB-006`.
- `changelog/2026-03-18.md` y `changelog/2026-03-19.md` contienen entradas que afirman que `main` no tenia implementacion versionada o que ya existian catalogo y fichas de detalle; ninguna de esas afirmaciones coincide con las rutas y modulos revisados en esta rama.

## Criterio documental aplicado
- Se documenta solo lo verificable en `main`.
- Las capacidades futuras se mantienen referenciadas como backlog, no como comportamiento disponible.
- Las contradicciones entre documentacion funcional, historial operativo y estado tecnico actual se dejan explicitas.
