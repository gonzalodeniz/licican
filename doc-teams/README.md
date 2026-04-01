# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion oficial de `Licican` separando con claridad el contenido para usuario final, equipo tecnico y administracion.

## Estado documental de referencia
Fecha de revision: `2026-04-01`.

Esta carpeta documenta el estado real verificable de la rama `main`. En esta revision la entrega minima ejecutable ya incorpora la issue tecnica #14, que activa PostgreSQL como backend operativo por defecto para catalogo y detalle, y mantiene el modo `file` como respaldo explicito para pruebas aisladas. La issue tecnica #17 (`T-002`) ya esta integrada en `main` y corrige la resolucion de ubicacion en PostgreSQL para no degradar ubicaciones geograficas especificas a `Canarias`.
La consolidacion de `PB-011` sigue soportada por el codigo y por las pruebas, pero esta checkout no versiona snapshots `.atom` en `data/`; por eso, la carga reproducible desde el arbol actual cae en el respaldo `data/opportunities.json` salvo que se aporten ficheros Atom temporales o externos.

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
- Vista HTML del catalogo consolidado (`PB-011`) en `/`.
- El backend operativo por defecto para catalogo y detalle es PostgreSQL; `LICICAN_CATALOG_BACKEND=file` sigue disponible para aislamiento de pruebas y usa `data/opportunities.json` cuando no hay snapshots Atom versionados disponibles.
- `PB-009` ya forma parte de `main` y su trazabilidad visible cubre `BOC`, `BOP Las Palmas` y `BOE` por olas.
- `PB-011` sigue siendo la referencia funcional del catalogo consolidado, pero en esta checkout no hay snapshots `.atom` versionados en `data/`; la reproduccion automatizada solo puede demostrarse con muestras temporales o externas.
- La issue tecnica #14 ya esta cerrada administrativamente en GitHub tras la validacion funcional y la integracion en `main`.
- No se observan superficies de pipeline de seguimiento ni de `PB-012` en el codigo o en las pruebas de `main`.
- El changelog de `2026-03-31` menciona `pipeline` como validado, pero en `main` no aparecen aun las rutas `/pipeline` ni `/api/pipeline`; esa entrada debe leerse como desalineacion documental hasta que el codigo la respalde.
- El changelog de `2026-03-29` registra `PB-012` como validada, pero la evidencia tecnica visible en `main` no expone todavia esa superficie; esta desalineacion sigue abierta y debe documentarse como tal.
- La issue tecnica `#17` queda documentada como integrada en `main`; este estado ya forma parte de la fotografia vigente de la rama principal.
- Existe un despliegue local en contenedor con `Dockerfile` y `docker-compose.yml`, con persistencia de `data/`, configuracion de `PORT` via `.env`, variables `DB_*` para PostgreSQL y una BBDD integrada con volumen persistente.

Las alertas tempranas ya estan implementadas y verificables en `main`; lo que sigue sin existir es el pipeline de seguimiento. Parte de la documentacion funcional de `product-manager/` sigue arrastrando textos anteriores a la integracion de `PB-011` o al estado ya visible de `PB-004`, asi que esa fuente debe leerse con cautela frente a la evidencia tecnica actual. Tampoco hay autenticacion ni un despliegue productivo endurecido.

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
- `main` contiene implementacion Python versionada en `src/licican/`, datos en `data/` y pruebas automatizadas en `tests/`.
- `PYTHONPATH=src python3 -m pytest -v` ejecuta 111 pruebas en verde en esta checkout.
- `make test` tambien funciona en un entorno con `.venv` disponible.
- `make run` arranca un servidor WSGI local usando `PORT` desde `.env` y, si ese puerto ya esta ocupado, avanza al siguiente libre.
- `docker compose up -d --build` levanta la misma aplicacion en contenedor, publica el puerto configurado en `PORT` y monta `data/` como volumen persistente.
- Las rutas verificables hoy son `/`, `/api/oportunidades`, `/oportunidades/<id>`, `/api/oportunidades/<id>`, `/alertas`, `/api/alertas`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti`, `/api/clasificacion-ti`, `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`.
- Las rutas verificables de `PB-009` hoy son `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`.
- El catalogo visible publica oportunidades TI desde PostgreSQL por defecto y, si se fuerza `LICICAN_CATALOG_BACKEND=file`, usa el respaldo `data/opportunities.json` cuando no hay snapshots Atom versionados disponibles en `data/`.
- El catalogo permite filtrar por `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
- Si el usuario informa un rango de presupuesto invalido, la vista HTML muestra una correccion explicita y la API responde `400 Bad Request` con `error_validacion`.
- La entrega consolidada de `PB-011` sigue soportada por el codigo, pero en esta checkout solo puede reproducirse de forma completa con muestras Atom aportadas externamente o en pruebas temporales; el arbol versionado actual no incluye snapshots `.atom`.
- Existe una contradiccion documental residual en `product-manager/`: varios documentos seguian describiendo `PB-011` como pendiente de integracion antes de esta sincronizacion, por lo que esa fuente debe revisarse frente a `main`.
- Existe otra desalineacion abierta: el changelog de `2026-03-31` registra `pipeline` como validado, pero `main` no expone esa superficie ni tiene pruebas que la demuestren.

## Dependencias y contradicciones abiertas
- La vision y el backlog de `product-manager/` describen capacidades futuras validas como fuente funcional, pero no deben leerse como evidencia de que `PB-012`, `PB-005` o el resto de ampliaciones planificadas ya esten disponibles en `main`.
- `pyproject.toml` sigue describiendo el paquete como "Cobertura inicial visible de fuentes del MVP de Licican.", aunque `main` ya expone tambien catalogo inicial (`PB-001`), filtros funcionales (`PB-003`), ficha de detalle (`PB-002`), superficie auditable de `PB-006`, priorizacion de fuentes reales oficiales (`PB-009`) y consolidacion trazable de `PB-011` con respaldo JSON cuando no hay Atom versionado.
- `PB-009` ya tiene evidencia integrada en `main`; `PB-011` conserva trazabilidad funcional en la documentacion, pero su reproduccion completa desde el arbol actual requiere aportar muestras Atom.
- `PB-012` aparece como validada en el changelog de `2026-03-29`, pero en `main` sigue sin observarse ninguna ruta, vista o prueba que la exponga; hasta que eso cambie, debe tratarse como trabajo validado no integrado o como evidencia documental desalineada.

## Criterio documental aplicado
- Se documenta solo lo verificable en `main`.
- Las capacidades futuras se mantienen referenciadas como backlog, no como comportamiento disponible.
- Las contradicciones entre documentacion funcional, metadata tecnica y estado observable actual se dejan explicitas.
