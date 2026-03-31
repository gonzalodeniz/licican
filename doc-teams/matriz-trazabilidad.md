# Matriz de trazabilidad documental

## Publico objetivo
Equipo documental, stakeholders funcionales, equipo tecnico y administracion que necesitan contrastar rapidamente vision, backlog, implementacion real y estado operativo observable.

## Objetivo
Dejar una referencia unica y accionable sobre que capacidades estan disponibles hoy en `main`, que evidencia las respalda y que puntos siguen siendo backlog o contradiccion documental abierta.

## Estado de referencia
- Fecha de revision: `2026-03-29`
- Rama revisada: `main`
- Verificacion ejecutada:
  - `PYTHONPATH=src python3 -m pytest -v`
  - comprobacion directa de rutas `/`, `/api/oportunidades`, `/oportunidades/pcsp-cabildo-licencias-2026`, `/api/oportunidades/pcsp-cabildo-licencias-2026`, `/alertas`, `/api/alertas`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti`
  - comprobacion de que los snapshots Atom del repositorio viven en `data/atom/*.atom` y de que el cargador actual todavia busca `data/*.atom`, lo que deja abierta la reproduccion automatizada de `PB-011`

## Matriz actual

| Elemento | Fuente funcional | Evidencia tecnica en `main` | Estado real observable | Publico principal | Notas |
|---|---|---|---|---|---|
| Catalogo de oportunidades TI | `PB-001`, `HU-01`, `CU-01` | `src/licican/atom_consolidation.py`, `src/licican/opportunity_catalog.py`, `src/licican/app.py`, `data/licitacionesPerfilesContratanteCompleto3_20260323_190607*.atom`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico | Visible en `/` y `/api/oportunidades`; publica solo oportunidades TI dentro de la cobertura vigente y conserva trazabilidad al fichero `.atom` origen en el detalle. |
| Filtros funcionales del catalogo | `PB-003`, `HU-03`, `CU-03` | `src/licican/opportunity_catalog.py`, `src/licican/app.py`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico, QA | Soporta `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`; la API devuelve `400` si el rango de presupuesto es invalido. |
| Ficha de detalle de licitacion | `PB-002`, `HU-02`, `CU-02` | `src/licican/atom_consolidation.py`, `src/licican/opportunity_catalog.py`, `src/licican/app.py`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico | Visible en `/oportunidades/<id>` y `/api/oportunidades/<id>`; aplica el ultimo dato oficial visible cuando hay rectificacion o modificacion y expone `fichero_origen_atom`. |
| Alertas tempranas | `PB-004`, `HU-04`, `CU-04` | `data/alerts.json`, `src/licican/alerts.py`, `src/licican/app.py`, `tests/test_alerts.py`, `tests/test_app.py` | Disponible | Usuario, producto, tecnico, QA | Visible en `/alertas` y `/api/alertas`; reutiliza los filtros del catalogo, permite crear, editar y desactivar alertas e informa solo coincidencias internas accionables. |
| Cobertura inicial de fuentes | `PB-007`, `HU-07`, `CU-06`, `product-manager/refinamiento-funcional.md` | `data/source_coverage.json`, `src/licican/source_coverage.py`, `src/licican/app.py`, `tests/test_source_coverage.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, administracion | Visible en `/cobertura-fuentes` y `/api/fuentes`. |
| Clasificacion TI auditable | `PB-006`, `HU-06`, `CU-08`, `product-manager/refinamiento-funcional.md` | `data/ti_classification_rules.json`, `src/licican/ti_classification.py`, `src/licican/app.py`, `tests/test_ti_classification.py`, `tests/test_app.py` | Disponible | Usuario, tecnico, QA, producto | Visible en `/clasificacion-ti` y `/api/clasificacion-ti`. |
| Priorizacion de recopilacion desde fuentes reales oficiales | `PB-009`, `HU-09`, `CU-09`, `product-manager/refinamiento-funcional.md` | `data/real_source_prioritization.json`, `src/licican/real_source_prioritization.py`, `src/licican/app.py`, `tests/test_real_source_prioritization.py`, `tests/test_app.py` | Disponible | Producto, tecnico, QA, administracion | Visible en `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`; ordena `BOC`, `BOP Las Palmas` y `BOE` por olas y explicita lo que queda fuera de alcance en esta iteracion. |
| Consolidacion de snapshots `.atom` | `PB-011`, `HU-11`, `CU-11`, `product-manager/product-backlog.md` | `src/licican/atom_consolidation.py`, `src/licican/opportunity_catalog.py`, `src/licican/app.py`, `data/atom/*.atom`, `tests/test_opportunity_catalog.py`, `tests/test_app.py` | No verificable completamente en esta checkout | Producto, tecnico, QA | Los snapshots Atom residen en `data/atom/`, pero el cargador vigente sigue buscando `data/*.atom`. La trazabilidad funcional sigue documentada, aunque la reproduccion automatizada de `PB-011` queda condicionada a resolver esa discrepancia. |
| Exposicion funcional del dataset consolidado | `PB-012`, `HU-12`, `CU-12`, `product-manager/product-backlog.md` | `changelog/2026-03-29.md` registra una validacion funcional; en `src/licican/app.py` y `tests/test_app.py` no aparecen rutas, vistas ni pruebas de `/datos-consolidados`, `Licitaciones TI Canarias`, `Detalle Lotes` o `Adjudicaciones` | No disponible en `main` | Usuario, producto, tecnico, QA | Existe una contradiccion documental abierta: el changelog la trata como validada, pero la rama `main` revisada no expone esa superficie. |
| Pipeline de seguimiento | `PB-005`, `HU-05`, `CU-05` | No existe soporte visible en vistas, API, datos o pruebas | No disponible en `main` | Usuario, producto | Sigue como backlog de Release 2 y no presenta evidencia tecnica visible en esta revision. |
| Instalacion local reproducible | `README.md`, `Makefile`, `pyproject.toml` | `pyproject.toml`, `Makefile`, paquete `src/licican/`, suite `tests/` | Disponible | Tecnico, administracion, QA | Requiere `python3 >= 3.12`; no hay dependencias externas adicionales versionadas. |
| Despliegue local en contenedor | Necesidad operativa de validacion reproducible | `Dockerfile`, `docker-compose.yml`, `src/licican/app.py`, `Makefile`, `tests/test_app.py` | Disponible | Administracion, tecnico | Publica la app con `HOST=0.0.0.0`, monta `data/` y excluye artefactos operativos de la imagen. |
| Despliegue productivo | Vision general y necesidad operativa futura | Solo existe `wsgiref.simple_server` y un contenedor local reproducible | No soportado documentalmente | Administracion, tecnico | El repositorio no incluye `systemd`, proxy ni healthcheck de produccion. |

## Contradicciones documentales abiertas
- `pyproject.toml` solo menciona cobertura de fuentes en la descripcion del paquete, aunque el codigo actual tambien incluye catalogo inicial, filtros funcionales, ficha de detalle, alertas internas, clasificacion TI auditable y consolidacion trazable de snapshots `.atom`.
- La documentacion funcional mantiene capacidades futuras validas como `PB-012`, pipeline y ampliaciones de cobertura, pero no hay evidencia tecnica visible de esas capacidades en `main`.
- La documentacion de `product-manager/` sigue mostrando algunos textos anteriores a la integracion de `PB-011` y al estado ya visible de `PB-004`; cuando contradiga la evidencia tecnica de `main`, debe actualizarse.
- El changelog de `2026-03-29` registra `PB-012` como validada, pero la rama `main` revisada no expone esa superficie en el codigo ni en las pruebas; la matriz la considera, por tanto, una contradiccion documental abierta.
- La entrada de `changelog/2026-03-24.md` confirma la integracion de `PB-009` en `main` y debe usarse como referencia operativa frente a descripciones antiguas de estado pendiente.
- La entrada de `changelog/2026-03-25.md` ya coincide con la evidencia tecnica de alertas visibles; la contradiccion residual queda en textos de producto que todavia no reflejan ese estado.
- La entrada de `changelog/2026-03-28.md` confirma la integracion de `PB-011` en `main`; la contradiccion actual añade ademas una discrepancia de rutas entre `data/atom/` y el cargador que sigue esperando `data/*.atom`.

## Dependencias abiertas para siguiente revision documental
- Revisar de nuevo esta matriz cuando `developer-teams` entregue una implementacion observable de `PB-012` o `PB-005` y su validacion quede integrada en `main`.
- Sincronizar la metadata tecnica del paquete si se quiere reducir la brecha entre descripcion y comportamiento observable.
