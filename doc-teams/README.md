# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion oficial de `PodencoTI` separando con claridad el contenido para usuario final, equipo tecnico y administracion.

## Estado documental de referencia
Fecha de revision: `2026-03-27`.

Esta carpeta documenta el estado real verificable de la rama `main`. En esta revision existe una entrega minima ejecutable de descubrimiento, pero su alcance sigue siendo acotado:

- Vista HTML del catalogo inicial de oportunidades TI (`PB-001`) en `/`.
- API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales (`PB-003`) en la vista HTML del catalogo y en la API JSON de `/api/oportunidades`.
- Vista HTML de ficha de detalle (`PB-002`) en `/oportunidades/<id>`.
- API JSON del detalle trazable en `/api/oportunidades/<id>`.
- Vista HTML de alertas tempranas (`PB-004`) en `/alertas`.
- API JSON de alertas persistidas y coincidencias internas en `/api/alertas`.
- Vista HTML de cobertura inicial del MVP (`PB-007`) en `/cobertura-fuentes`.
- API JSON de cobertura de fuentes en `/api/fuentes`.
- Vista HTML de clasificacion TI auditable (`PB-006`) en `/clasificacion-ti`.
- API JSON de reglas y ejemplos auditados de clasificacion TI en `/api/clasificacion-ti`.
- Vista HTML de priorizacion de fuentes reales oficiales (`PB-009`) en `/priorizacion-fuentes-reales`.
- API JSON de priorizacion de fuentes reales oficiales en `/api/fuentes-prioritarias`.
- `PB-009` ya forma parte de `main` y su trazabilidad visible cubre `BOC`, `BOP Las Palmas` y `BOE` por olas.
- Aunque el changelog de `2026-03-27` menciona `PB-011` como validada, la evidencia tecnica visible en `main` revisada aqui sigue sin mostrar consolidacion de `data/*.atom`; el catalogo continua leyendose desde `data/opportunities.json`.
- No se observan superficies de pipeline de seguimiento en el codigo o en las pruebas de `main`.
- Existe un despliegue local en contenedor con `Dockerfile` y `docker-compose.yml`, con persistencia de `data/` y configuracion de `PORT` via `.env`.

Las alertas tempranas ya estan implementadas y verificables en `main`; lo que sigue sin existir es el pipeline de seguimiento. Parte de la documentacion funcional de `product-manager/` sigue arrastrando descripciones anteriores sobre `PB-004`, asi que esa fuente debe leerse con cautela frente a la evidencia tecnica actual. Tampoco hay autenticacion ni un despliegue productivo endurecido.

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
- `PYTHONPATH=src python3 -m unittest discover -s tests -v` ejecuta 49 pruebas y finaliza correctamente.
- `make test` tambien funciona en un entorno con `.venv` disponible.
- `make run` arranca un servidor WSGI local usando `PORT` desde `.env` y, por defecto, `8000` si no se define.
- `docker compose up -d --build` levanta la misma aplicacion en contenedor, publica el puerto configurado en `PORT` y monta `data/` como volumen persistente.
- Las rutas verificables hoy son `/`, `/api/oportunidades`, `/oportunidades/<id>`, `/api/oportunidades/<id>`, `/alertas`, `/api/alertas`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti`.
- Las rutas verificables de `PB-009` hoy son `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`.
- El catalogo visible publica 3 oportunidades TI a partir de 5 registros de origen dentro de la cobertura MVP actual.
- El catalogo permite filtrar por `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
- Si el usuario informa un rango de presupuesto invalido, la vista HTML muestra una correccion explicita y la API responde `400 Bad Request` con `error_validacion`.
- La entrada de `changelog/2026-03-25.md` que menciona `PB-004` ya coincide con la evidencia tecnica visible en `main`; la contradiccion residual queda en algunos textos de `product-manager/` que todavia conservan estado anterior a la integracion.
- Existe una contradiccion documental residual en `product-manager/`: varios documentos siguen describiendo `PB-009` como pendiente de fusion y borrado de rama, pero la evidencia tecnica y el changelog de `2026-03-24` ya muestran esa entrega integrada en `main`.
- El changelog de `2026-03-27` registra `PB-011` como validada, pero el codigo y las pruebas de `main` revisados en esta pasada no muestran aun ingestion de `data/*.atom` ni una superficie de consolidacion trazable; hasta que se sincronice, esa referencia debe tratarse como contradiccion abierta y no como comportamiento vigente.

## Dependencias y contradicciones abiertas
- La vision y el backlog de `product-manager/` describen capacidades futuras validas como fuente funcional, pero esas capacidades aun no estan implementadas en `main`.
- `pyproject.toml` sigue describiendo el paquete como "Cobertura inicial visible de fuentes del MVP de PodencoTI.", aunque `main` ya expone tambien catalogo inicial (`PB-001`), filtros funcionales (`PB-003`), ficha de detalle (`PB-002`), superficie auditable de `PB-006` y priorizacion de fuentes reales oficiales (`PB-009`).
- Pipeline (`PB-005`) sigue definido funcionalmente, pero no tiene evidencia tecnica visible en `main` revisado.
- `PB-009` ya existe como prioridad funcional en `product-manager/` y ahora tambien tiene evidencia integrada en `main`; lo que sigue desalineado es parte del texto de producto, que todavia conserva el estado operativo previo a la fusion.

## Criterio documental aplicado
- Se documenta solo lo verificable en `main`.
- Las capacidades futuras se mantienen referenciadas como backlog, no como comportamiento disponible.
- Las contradicciones entre documentacion funcional, metadata tecnica y estado observable actual se dejan explicitas.
