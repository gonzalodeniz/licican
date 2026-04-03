# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion oficial de `Licican` separando con claridad el contenido para usuario final, equipo tecnico y administracion.

## Estado documental de referencia
Fecha de revision: `2026-04-03`.

Esta carpeta documenta el estado real verificable de la rama `main`. En esta revision la entrega minima ejecutable ya incorpora PostgreSQL como backend operativo por defecto para catalogo y detalle, la gestion administrativa de usuarios con persistencia en PostgreSQL, la superficie consolidada de datos de `PB-012`, el pipeline operativo de `PB-005`, la matriz de permisos y los KPIs visibles para administracion.
La consolidacion de `PB-011` sigue soportada por el codigo y por las pruebas, pero esta checkout no versiona snapshots `.atom` en `data/`; por eso, la carga reproducible desde el arbol actual cae en el respaldo `data/opportunities.json` salvo que se aporten ficheros Atom temporales o externos.

- Vista HTML del catalogo inicial de oportunidades TI (`PB-001`) en `/`.
- API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales (`PB-003`) en la vista HTML del catalogo y en la API JSON de `/api/oportunidades`.
- Vista HTML de ficha de detalle (`PB-002`) en `/oportunidades/<id>`.
- API JSON del detalle trazable en `/api/oportunidades/<id>`.
- Vista HTML de datos consolidados (`PB-012`) en `/datos-consolidados`.
- API JSON de datos consolidados en `/api/datos-consolidados`.
- Vista HTML de pipeline de seguimiento (`PB-005`) en `/pipeline`.
- API JSON del pipeline en `/api/pipeline`.
- Vista HTML de alertas tempranas (`PB-004`) en `/alertas`.
- API JSON de alertas persistidas y coincidencias internas en `/api/alertas`.
- Vista HTML de gestion administrativa de usuarios (`PB-016`) en `/usuarios`.
- API JSON de gestion administrativa de usuarios en `/api/usuarios`.
- Vista HTML de cobertura inicial del MVP (`PB-007`) en `/cobertura-fuentes`.
- API JSON de cobertura de fuentes en `/api/fuentes`.
- Vista HTML de clasificacion TI auditable (`PB-006`) en `/clasificacion-ti`.
- API JSON de reglas y ejemplos auditados de clasificacion TI en `/api/clasificacion-ti`.
- Vista HTML de priorizacion de fuentes reales oficiales (`PB-009`) en `/priorizacion-fuentes-reales`.
- API JSON de priorizacion de fuentes reales oficiales en `/api/fuentes-prioritarias`.
- Vista HTML de KPIs (`PB-013`) en `/kpis`.
- Vista HTML de la matriz de permisos (`PB-013`) en `/permisos`.
- El backend operativo por defecto para catalogo y detalle es PostgreSQL; `LICICAN_CATALOG_BACKEND=file` sigue disponible para aislamiento de pruebas y usa `data/opportunities.json` cuando no hay snapshots Atom versionados disponibles.
- `PB-009` ya forma parte de `main` y su trazabilidad visible cubre `BOC`, `BOP Las Palmas` y `BOE` por olas.
- `PB-011` sigue siendo la referencia funcional del catalogo consolidado, pero en esta checkout no hay snapshots `.atom` versionados en `data/`; la reproduccion automatizada solo puede demostrarse con muestras temporales o externas.
- La issue tecnica #14 ya esta cerrada administrativamente en GitHub tras la validacion funcional y la integracion en `main`.
- La issue tecnica #17 ya esta integrada en `main` y corrige la resolucion de ubicacion en PostgreSQL para no degradar etiquetas geograficas especificas.
- Existe un despliegue local en contenedor con `Dockerfile` y `docker-compose.yml`, con persistencia de `data/`, configuracion de `PORT` via `.env`, variables `DB_*` para PostgreSQL y una BBDD integrada con volumen persistente.

Las alertas tempranas, el pipeline, la gestion administrativa de usuarios, los datos consolidados, los KPIs y la matriz de permisos ya estan implementados y verificables en `main`; la documentacion funcional de `product-manager/` sigue siendo la fuente de alcance esperado, pero cuando contradiga a `main` debe leerse como especificacion, no como evidencia de ausencia. Tampoco hay autenticacion real, SSO ni MFA, y el despliegue productivo endurecido sigue fuera de alcance.

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
- `PYTHONPATH=src python3 -m pytest -v` ejecuta la suite automatizada del proyecto en esta checkout, que en esta revision termina en 149 pruebas en verde.
- `make test` tambien funciona en un entorno con `.venv` disponible.
- `make run` arranca un servidor WSGI local usando `PORT` desde `.env` y, si ese puerto ya esta ocupado, avanza al siguiente libre.
- `docker compose up -d --build` levanta la misma aplicacion en contenedor, publica el puerto configurado en `PORT` y monta `data/` como volumen persistente.
- Las rutas verificables hoy son `/`, `/api/oportunidades`, `/oportunidades/<id>`, `/api/oportunidades/<id>`, `/datos-consolidados`, `/api/datos-consolidados`, `/pipeline`, `/api/pipeline`, `/alertas`, `/api/alertas`, `/usuarios`, `/usuarios/<id>`, `/api/usuarios`, `/api/usuarios/<id>`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti`, `/api/clasificacion-ti`, `/priorizacion-fuentes-reales`, `/api/fuentes-prioritarias`, `/kpis` y `/permisos`.
- El catalogo visible publica oportunidades TI desde PostgreSQL por defecto y, si se fuerza `LICICAN_CATALOG_BACKEND=file`, usa el respaldo `data/opportunities.json` cuando no hay snapshots Atom versionados disponibles en `data/`.
- El catalogo permite filtrar por `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
- Si el usuario informa un rango de presupuesto invalido, la vista HTML muestra una correccion explicita y la API responde `400 Bad Request` con `error_validacion`.
- La gestion de usuarios permite listar, filtrar, crear, editar y cambiar de estado cuentas de usuario, ademas de abrir detalle y consultar la trazabilidad basica del registro seleccionado.
- La superficie de `PB-012` ya esta integrada en `main` y se reproduce desde el Excel versionado con las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
- El pipeline de `PB-005` ya esta integrado en `main` y permite guardar oportunidades, evitar duplicados y mover cada registro por estados de seguimiento.
- Existe una contradiccion documental residual en `pyproject.toml`, que sigue describiendo el paquete como si solo cubriera la cobertura de fuentes.

## Dependencias y contradicciones abiertas
- La vision y el backlog de `product-manager/` describen capacidades futuras validas como fuente funcional, pero no deben leerse como evidencia de que `PB-012`, `PB-005` o el resto de ampliaciones planificadas ya esten disponibles en `main`.
- `pyproject.toml` sigue describiendo el paquete como "Cobertura inicial visible de fuentes del MVP de Licican.", aunque `main` ya expone tambien catalogo inicial (`PB-001`), filtros funcionales (`PB-003`), ficha de detalle (`PB-002`), superficie auditable de `PB-006`, priorizacion de fuentes reales oficiales (`PB-009`) y consolidacion trazable de `PB-011` con respaldo JSON cuando no hay Atom versionado.
- `PB-009` ya tiene evidencia integrada en `main`; `PB-011` conserva trazabilidad funcional en la documentacion, pero su reproduccion completa desde el arbol actual requiere aportar muestras Atom.
- `PB-012` ya forma parte de `main` y debe documentarse como superficie vigente, no como trabajo pendiente.

## Criterio documental aplicado
- Se documenta solo lo verificable en `main`.
- Las capacidades futuras se mantienen referenciadas como backlog, no como comportamiento disponible.
- Las contradicciones entre documentacion funcional, metadata tecnica y estado observable actual se dejan explicitas.
