# Matriz de trazabilidad documental

## Publico objetivo
Equipo documental, stakeholders funcionales, equipo tecnico y administracion que necesitan contrastar rapidamente vision, backlog, implementacion real y estado operativo observable.

## Objetivo
Dejar una referencia unica y accionable sobre que capacidades estan disponibles hoy en `main`, que evidencia las respalda y que puntos siguen siendo backlog o contradiccion documental abierta.

## Estado de referencia
- Fecha de revision: `2026-03-23`
- Rama revisada: `main`
- Verificacion ejecutada:
  - `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  - comprobacion directa de rutas `/`, `/api/oportunidades`, `/oportunidades/pcsp-cabildo-licencias-2026`, `/api/oportunidades/pcsp-cabildo-licencias-2026`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti`

## Matriz actual

| Elemento | Fuente funcional | Evidencia tecnica en `main` | Estado real observable | Publico principal | Notas |
|---|---|---|---|---|---|
| Catalogo de oportunidades TI | `PB-001`, `HU-01`, `CU-01` | `data/opportunities.json`, `src/podencoti/opportunity_catalog.py`, `src/podencoti/app.py`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico | Visible en `/` y `/api/oportunidades`; publica solo oportunidades TI dentro de la cobertura MVP. |
| Filtros funcionales del catalogo | `PB-003`, `HU-03`, `CU-03` | `src/podencoti/opportunity_catalog.py`, `src/podencoti/app.py`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico, QA | Soporta `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`; la API devuelve `400` si el rango de presupuesto es invalido. |
| Ficha de detalle de licitacion | `PB-002`, `HU-02`, `CU-02` | `data/opportunities.json`, `src/podencoti/opportunity_catalog.py`, `src/podencoti/app.py`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico | Visible en `/oportunidades/<id>` y `/api/oportunidades/<id>`; aplica el ultimo dato oficial visible cuando hay rectificacion o modificacion. |
| Cobertura inicial de fuentes | `PB-007`, `HU-07`, `CU-06`, `product-manager/refinamiento-funcional.md` | `data/source_coverage.json`, `src/podencoti/source_coverage.py`, `src/podencoti/app.py`, `tests/test_source_coverage.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, administracion | Visible en `/cobertura-fuentes` y `/api/fuentes`. |
| Clasificacion TI auditable | `PB-006`, `HU-06`, `CU-08`, `product-manager/refinamiento-funcional.md` | `data/ti_classification_rules.json`, `src/podencoti/ti_classification.py`, `src/podencoti/app.py`, `tests/test_ti_classification.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, QA, producto | Visible en `/clasificacion-ti` y `/api/clasificacion-ti`. |
| Priorizacion de recopilacion desde fuentes reales oficiales | `PB-009`, `HU-09`, `CU-09`, `product-manager/refinamiento-funcional.md` | No hay evidencia integrada en `main`; `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `404 Not Found` | No disponible en `main` | Producto, tecnico, QA | La prioridad existe en backlog, pero su reentrega sigue sin formar parte de la rama principal. La entrada de `changelog/2026-03-23.md` que la declara validada no coincide con la evidencia tecnica actual y debe resolverse antes de documentarla como comportamiento vigente. |
| Alertas tempranas | `PB-004`, `HU-04`, `CU-04` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog de Release 2. |
| Pipeline de seguimiento | `PB-005`, `HU-05`, `CU-05` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog de Release 2. |
| Instalacion local reproducible | `README.md`, `Makefile`, `pyproject.toml` | `pyproject.toml`, `Makefile`, paquete `src/podencoti/`, suite `tests/` | Disponible | Tecnico, administracion, QA | Requiere `python3 >= 3.12`; no hay dependencias externas adicionales versionadas. |
| Despliegue productivo | Vision general y necesidad operativa futura | Solo existe `wsgiref.simple_server` en `src/podencoti/app.py` | No soportado documentalmente | Administracion, tecnico | El repositorio no incluye `Dockerfile`, `systemd`, proxy ni healthcheck. |

## Contradicciones documentales abiertas
- `pyproject.toml` solo menciona cobertura de fuentes en la descripcion del paquete, aunque el codigo actual tambien incluye catalogo inicial, filtros funcionales, ficha de detalle y clasificacion TI auditable.
- La documentacion funcional mantiene capacidades futuras validas como alertas, pipeline y recopilacion real desde nuevas fuentes oficiales, pero no hay evidencia tecnica visible de esas capacidades en `main`.
- La entrada de `changelog/2026-03-23.md` que presenta `PB-009` como validado no coincide con la evidencia tecnica de `main`; hasta que se alinee, esta matriz trata `PB-009` como no disponible en la rama principal.

## Dependencias abiertas para siguiente revision documental
- Revisar de nuevo esta matriz cuando `developer-teams` entregue una implementacion observable de `PB-004`, `PB-005` o `PB-009` y su validacion quede integrada en `main`.
- Sincronizar la metadata tecnica del paquete si se quiere reducir la brecha entre descripcion y comportamiento observable.
