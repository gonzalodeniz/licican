# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion oficial de `PodencoTI` separando con claridad el contenido para usuario final, equipo tecnico y administracion.

## Estado documental de referencia
Fecha de revision: `2026-03-23`.

Esta carpeta documenta el estado real verificable de la rama `main`. En esta revision existe una entrega minima ejecutable de descubrimiento, pero su alcance sigue siendo acotado:

- Vista HTML del catalogo inicial de oportunidades TI (`PB-001`) en `/`.
- API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales (`PB-003`) en la vista HTML del catalogo y en la API JSON de `/api/oportunidades`.
- Vista HTML de ficha de detalle (`PB-002`) en `/oportunidades/<id>`.
- API JSON del detalle trazable en `/api/oportunidades/<id>`.
- Vista HTML de cobertura inicial del MVP (`PB-007`) en `/cobertura-fuentes`.
- API JSON de cobertura de fuentes en `/api/fuentes`.
- Vista HTML de clasificacion TI auditable (`PB-006`) en `/clasificacion-ti`.
- API JSON de reglas y ejemplos auditados de clasificacion TI en `/api/clasificacion-ti`.
- `PB-009` sigue priorizado en backlog e issue #9, pero su reentrega todavia no forma parte de `main`.

No existen todavia alertas tempranas, pipeline de seguimiento, autenticacion ni componentes de despliegue productivo.

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
- `PYTHONPATH=src python3 -m unittest discover -s tests -v` ejecuta 33 pruebas y finaliza correctamente.
- `make test` tambien funciona en un entorno con `.venv` disponible.
- `make run` arranca un servidor WSGI local en `http://127.0.0.1:8000`.
- Las rutas verificables hoy son `/`, `/api/oportunidades`, `/oportunidades/<id>`, `/api/oportunidades/<id>`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti`.
- El catalogo visible publica 3 oportunidades TI a partir de 5 registros de origen dentro de la cobertura MVP actual.
- El catalogo permite filtrar por `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
- Si el usuario informa un rango de presupuesto invalido, la vista HTML muestra una correccion explicita y la API responde `400 Bad Request` con `error_validacion`.
- La priorizacion de fuentes reales de `PB-009` sigue sin estar expuesta como superficie navegable en `main`; las rutas `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `404 Not Found`.
- Existe una contradiccion documental abierta: `changelog/2026-03-23.md` describe `PB-009` como validado, pero la evidencia tecnica actual de `main` no expone esa superficie.

## Dependencias y contradicciones abiertas
- La vision y el backlog de `product-manager/` describen capacidades futuras validas como fuente funcional, pero esas capacidades aun no estan implementadas en `main`.
- `pyproject.toml` sigue describiendo el paquete como "Cobertura inicial visible de fuentes del MVP de PodencoTI.", aunque `main` ya expone tambien catalogo inicial (`PB-001`), filtros funcionales (`PB-003`), ficha de detalle (`PB-002`) y superficie auditable de `PB-006`.
- Alertas (`PB-004`) y pipeline (`PB-005`) siguen definidos funcionalmente, pero no tienen evidencia tecnica visible en `main`.
- `PB-009` ya existe como prioridad funcional en `product-manager/`, pero aun no hay implementacion integrada y validada en la rama principal.
- La entrada de `changelog/2026-03-23.md` que presenta `PB-009` como validado no coincide con la evidencia tecnica revisada en `main`; esta discrepancia debe resolverse antes de documentar la priorizacion de fuentes como comportamiento vigente.

## Criterio documental aplicado
- Se documenta solo lo verificable en `main`.
- Las capacidades futuras se mantienen referenciadas como backlog, no como comportamiento disponible.
- Las contradicciones entre documentacion funcional, metadata tecnica y estado observable actual se dejan explicitas.
