# Matriz de trazabilidad documental

## Publico objetivo
Equipo documental, stakeholders funcionales, equipo tecnico y administracion que necesitan contrastar rapidamente vision, backlog, implementacion real y estado operativo observable.

## Objetivo
Dejar una referencia unica y accionable sobre que capacidades estan disponibles hoy en `main`, que evidencia las respalda y que puntos siguen siendo backlog o contradiccion documental abierta.

## Estado de referencia
- Fecha de revision: `2026-03-19`
- Rama revisada: `main`
- Verificacion ejecutada:
  - `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  - comprobacion directa de rutas `/`, `/api/fuentes`, `/clasificacion-ti`, `/api/clasificacion-ti`, `/oportunidades` y `/api/oportunidades`

## Matriz actual

| Elemento | Fuente funcional | Evidencia tecnica en `main` | Estado real observable | Publico principal | Notas |
|---|---|---|---|---|---|
| Cobertura inicial de fuentes | `PB-007`, `HU-07`, `CU-06`, `product-manager/refinamiento-funcional.md` | `data/source_coverage.json`, `src/podencoti/source_coverage.py`, `src/podencoti/app.py`, `tests/test_source_coverage.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, administracion | Visible en `/` y `/api/fuentes`. |
| Clasificacion TI auditable | `PB-006`, `HU-06`, `CU-08`, `product-manager/refinamiento-funcional.md` | `data/ti_classification_rules.json`, `src/podencoti/ti_classification.py`, `src/podencoti/app.py`, `tests/test_ti_classification.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, QA, producto | Visible en `/clasificacion-ti` y `/api/clasificacion-ti`. |
| Catalogo de oportunidades TI | `PB-001`, `HU-01`, `CU-01` | No existe modulo, ruta ni datos versionados de catalogo en `src/` o `data/` | No disponible en `main` | Usuario, producto | `/oportunidades` y `/api/oportunidades` responden `404 Not Found`. |
| Ficha de detalle de licitacion | `PB-002`, `HU-02`, `CU-02` | No existe modulo, ruta ni pruebas especificas de detalle en `src/` o `tests/` | No disponible en `main` | Usuario, producto | La narrativa del `changelog` no coincide con el codigo actual revisado. |
| Filtros funcionales | `PB-003`, `HU-03`, `CU-03` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog dependiente del catalogo. |
| Alertas tempranas | `PB-004`, `HU-04`, `CU-04` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog de Release 2. |
| Pipeline de seguimiento | `PB-005`, `HU-05`, `CU-05` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog de Release 2. |
| Instalacion local reproducible | `README.md`, `Makefile`, `pyproject.toml` | `pyproject.toml`, `Makefile`, paquete `src/podencoti/`, suite `tests/` | Disponible | Tecnico, administracion, QA | Requiere `python3 >= 3.12`; no hay dependencias externas adicionales versionadas. |
| Despliegue productivo | Vision general y necesidad operativa futura | Solo existe `wsgiref.simple_server` en `src/podencoti/app.py` | No soportado documentalmente | Administracion, tecnico | El repositorio no incluye `Dockerfile`, `systemd`, proxy ni healthcheck. |

## Contradicciones documentales abiertas
- `changelog/2026-03-18.md` contiene afirmaciones incompatibles entre si y con el arbol actual: unas entradas dicen que no habia implementacion versionada y otras hablan de rutas de catalogo ya validadas.
- `changelog/2026-03-19.md` afirma que `PB-002` fue implementado y validado con navegacion a fichas de detalle, pero esa superficie no existe hoy en `src/podencoti/` ni en `tests/`.
- `pyproject.toml` solo menciona cobertura de fuentes en la descripcion del paquete, aunque el codigo actual tambien incluye la superficie de clasificacion TI auditable.

## Dependencias abiertas para siguiente revision documental
- Sincronizar documentalmente el estado operativo historico con el estado real de `main` para reducir ambiguedad entre roles.
- Revisar de nuevo esta matriz cuando `developer-teams` entregue una implementacion observable de `PB-001`, `PB-002` o `PB-003`.
