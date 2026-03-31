# Manual tecnico

## Publico objetivo
Equipo tecnico que necesita conocer la implementacion actual de `main`, sus rutas verificables y los limites funcionales todavia abiertos.

## Resumen tecnico verificable
`Licican` expone en `main` una aplicacion WSGI minima en Python con un conjunto funcional verificable y un despliegue local en contenedor:

- `PB-001`: catalogo inicial de oportunidades TI.
- `PB-003`: filtros funcionales aplicados sobre el catalogo HTML y la API JSON.
- `PB-002`: ficha resumida de detalle por oportunidad visible.
- `PB-004`: alertas tempranas con alta, edicion y desactivacion, y registro interno de coincidencias accionables.
- `PB-007`: cobertura inicial visible y verificable de fuentes.
- `PB-006`: regla de clasificacion TI auditable con ejemplos trazables.
- `PB-009`: priorizacion visible de fuentes reales oficiales por olas.
- `PB-011`: consolidacion funcional trazable de snapshots `.atom` con detalle de fichero origen.
- `Issue #14`: backend PostgreSQL operativo por defecto para catalogo y detalle, con modo `file` disponible para pruebas aisladas.
- Despliegue local en contenedor con `Dockerfile` y `docker-compose.yml`, incluyendo PostgreSQL integrada.

La version actual de `main` sirve catalogo y detalle desde PostgreSQL por defecto mediante la issue tecnica #14. El modo `file` sigue disponible para pruebas aisladas y la documentacion de `PB-011` conserva valor historico sobre la consolidacion de snapshots `.atom`, pero esa evidencia no es reproducible todavia en esta checkout porque los snapshots estan en `data/atom/` mientras el cargador sigue buscando `data/*.atom`. La descripcion de paquete en `pyproject.toml` sigue mencionando solo cobertura de fuentes. Esa metadata ya no resume por completo el comportamiento observable de la rama.
La issue tecnica #17 ya esta validada en su rama de trabajo y corrige la resolucion de ubicacion en PostgreSQL para no degradar etiquetas geograficas especificas a `Canarias`, pero hasta su merge en `main` esta mejora sigue siendo una expectativa validada y no un comportamiento vigente documentable como parte estable de la rama principal.

## Artefactos tecnicos presentes
- Configuracion de paquete: `pyproject.toml`
- Automatizacion local: `Makefile`
- Aplicacion WSGI: `src/licican/app.py`
- Alertas tempranas: `src/licican/alerts.py`
- Catalogo y detalle de oportunidades: `src/licican/opportunity_catalog.py`
- Carga de cobertura de fuentes: `src/licican/source_coverage.py`
- Priorizacion de fuentes reales oficiales: `src/licican/real_source_prioritization.py`
- Carga y evaluacion de reglas TI: `src/licican/ti_classification.py`
- Datos versionados: `data/opportunities.json`, `data/source_coverage.json`, `data/real_source_prioritization.json`, `data/ti_classification_rules.json`
- Snapshots `.atom` presentes en el repositorio: `data/atom/*.atom`
- Datos de alertas: `data/alerts.json`
- Suite tecnica: `tests/test_app.py`, `tests/test_alerts.py`, `tests/test_opportunity_catalog.py`, `tests/test_real_source_prioritization.py`, `tests/test_source_coverage.py`, `tests/test_ti_classification.py`
- Contenedorizacion local: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

## Superficie HTTP vigente
- `/`: vista HTML del catalogo inicial de oportunidades TI con formulario de filtros funcionales.
- `/api/oportunidades`: JSON del catalogo filtrado por cobertura MVP y clasificacion TI.
- `/oportunidades/<id>`: ficha HTML de detalle de una oportunidad visible.
- `/api/oportunidades/<id>`: JSON trazable de la ficha de detalle.
- `/alertas`: vista HTML para crear, editar y desactivar alertas reutilizando los mismos filtros del catalogo.
- `/api/alertas`: JSON con la referencia funcional, el resumen de alertas persistidas y sus coincidencias internas.
- `/cobertura-fuentes`: vista HTML de cobertura inicial del MVP.
- `/api/fuentes`: JSON con fuentes y resumen por estado.
- `/priorizacion-fuentes-reales`: vista HTML de priorizacion de fuentes reales oficiales.
- `/api/fuentes-prioritarias`: JSON con fuentes priorizadas, resumen por olas y elementos fuera de alcance de esta iteracion.
- `/clasificacion-ti`: vista HTML de la regla TI auditable.
- `/api/clasificacion-ti`: JSON con reglas y ejemplos auditados.

La aplicacion devuelve `404 Not Found` para cualquier otra ruta no declarada.
Los parametros funcionales visibles hoy para `/` y `/api/oportunidades` son `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
Si `presupuesto_min` es mayor que `presupuesto_max`, la API responde `400 Bad Request` y la vista HTML mantiene el catalogo base junto con un mensaje de correccion.
Cuando la aplicacion opera con `LICICAN_CATALOG_BACKEND=file`, el catalogo y el detalle se alimentan de la consolidacion funcional de `PB-011`; en ese caso, cada ficha muestra tambien `fichero_origen_atom`. En esta checkout la carga Atom no es completamente reproducible porque los ficheros estan en `data/atom/` y el cargador aun busca `data/*.atom`. Con el backend PostgreSQL por defecto, la carga procede de la tabla `licitacion` y mantiene error controlado si la base no esta disponible.

### Campos visibles por superficie
- `/api/oportunidades`: devuelve `referencia_funcional`, `cobertura_aplicada`, `total_registros_origen`, `total_oportunidades_visibles`, `total_oportunidades_catalogo`, `filtros_activos`, `error_validacion`, `filtros_disponibles` y `oportunidades`.
- `/api/oportunidades/<id>`: devuelve datos criticos visibles, `actualizacion_oficial_mas_reciente`, `historial_actualizaciones` y `fichero_origen_atom`.
- `/api/alertas`: devuelve `referencia_funcional`, `summary` y `alerts`.
- `/api/fuentes`: devuelve `sources` y `summary`.
- `/priorizacion-fuentes-reales`: devuelve una tabla HTML con `Ola`, `Fuente real oficial`, `Categoria`, `Alcance`, `Justificacion` y `Trazabilidad`.
- `/api/fuentes-prioritarias`: devuelve `referencia_funcional`, `sources`, `summary` y `fuera_de_alcance`.
- `/api/clasificacion-ti`: devuelve `referencia_funcional`, `reglas` y `ejemplos_auditados`.

## Estructura tecnica
- [app.py](/opt/apps/licican/src/licican/app.py) centraliza el router WSGI, el renderizado HTML y las respuestas JSON.
- [atom_consolidation.py](/opt/apps/licican/src/licican/atom_consolidation.py) consolida snapshots `.atom`, resuelve la version vigente por expediente y conserva el fichero origen.
- [alerts.py](/opt/apps/licican/src/licican/alerts.py) persiste alertas internas, valida criterios funcionales y recalcula coincidencias accionables.
- [opportunity_catalog.py](/opt/apps/licican/src/licican/opportunity_catalog.py) carga registros versionados desde la consolidacion Atom cuando existe, filtra por cobertura MVP, aplica la clasificacion TI y resuelve el ultimo dato oficial visible para ficha y catalogo.
- [postgres_catalog.py](/opt/apps/licican/src/licican/postgres_catalog.py) centraliza la carga desde PostgreSQL para el backend operativo por defecto y conserva el modo `file` como alternativa de apoyo.
- [source_coverage.py](/opt/apps/licican/src/licican/source_coverage.py) valida estados de cobertura permitidos (`MVP`, `Posterior`, `Por definir`) y resume conteos.
- [real_source_prioritization.py](/opt/apps/licican/src/licican/real_source_prioritization.py) valida las olas permitidas (`Ola 1`, `Ola 2`, `Ola 3`), ordena las fuentes por prioridad y resume la distribucion por ola.
- [ti_classification.py](/opt/apps/licican/src/licican/ti_classification.py) normaliza texto, aplica reglas funcionales y audita ejemplos con tres salidas posibles: `TI`, `No TI` y `Caso frontera`.

## Verificacion reproducible
Desde la raiz del proyecto:

```bash
PYTHONPATH=src python3 -m pytest -v
PYTHONPATH=src python3 -m licican.app
docker compose up -d --build
```

Resultado verificado en esta revision:
- 104 pruebas automatizadas ejecutadas en verde con `pytest`.
- Servidor local disponible en `http://127.0.0.1:<PORT>`, usando `PORT` desde `.env` y, por defecto, `8000` si no se define.
- Contenedor accesible en `http://127.0.0.1:<PORT>` cuando `docker-compose.yml` publica la aplicacion con `HOST=0.0.0.0`.
- La BBDD PostgreSQL integrada responde en `localhost:15432` por defecto y se puede abrir con `make docker-psql`.
- Las rutas `http://127.0.0.1:<PORT>/alertas` y `http://127.0.0.1:<PORT>/api/alertas` responden con la gestion interna de alertas tempranas del MVP.
- Las rutas `http://127.0.0.1:<PORT>/priorizacion-fuentes-reales` y `http://127.0.0.1:<PORT>/api/fuentes-prioritarias` siguen disponibles para la priorizacion de fuentes reales.
- La ruta `http://127.0.0.1:<PORT>/oportunidades/<id>` expone el fichero `.atom` origen de la oportunidad cuando la consolidacion Atom es reproducible.
- El backend PostgreSQL por defecto devuelve error controlado si la base no esta disponible y el modo `file` sigue accesible para verificacion aislada.

## Contradicciones explicitadas
- `pyproject.toml` sigue describiendo el paquete como una release centrada solo en cobertura de fuentes, aunque la rama ya expone catalogo, filtros, detalle y clasificacion TI auditable.
- La documentacion funcional de `product-manager/` describe backlog posterior valido, pero no debe leerse como contrato tecnico ya implementado para `PB-012`, pipeline o nuevas ampliaciones de cobertura.
- Parte de `product-manager/` sigue mostrando el estado anterior de `PB-004`; la evidencia tecnica vigente en `main` ya expone alertas, asi que esa fuente debe leerse con cautela hasta que se sincronice.
- La documentacion funcional de `product-manager/` sigue mostrando algunos textos anteriores a la integracion de `PB-011`; cuando contradiga a `main`, la evidencia tecnica vigente debe prevalecer y esa fuente debe corregirse.
- El changelog de `2026-03-29` registra `PB-012` como validada, pero en `main` no hay rutas, vistas ni pruebas que expongan `/datos-consolidados` ni las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`; esa entrega sigue siendo una contradiccion documental abierta hasta que el codigo la materialice.

## Limitaciones tecnicas actuales
- No existe persistencia de usuario ni ingestion automatizada fuera de los snapshots `.atom` versionados disponibles; el catalogo se alimenta de la consolidacion funcional de `PB-011` cuando hay `.atom` en `data/` y cae a `data/opportunities.json` solo como respaldo.
- `PB-012` no esta expuesto en la superficie tecnica revisada, asi que no debe documentarse como disponible aunque el changelog la haya citado como validada.
- No hay autenticacion, base de datos, tareas programadas ni integracion externa.
- No hay contrato de despliegue productivo versionado, mas alla del arranque local con `wsgiref` y la publicacion local en contenedor.
- La priorizacion de fuentes reales de `PB-009` ya esta expuesta en la app verificada con `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`.
- La entrega de `PB-009` no habilita pipeline; solo refuerza origen, trazabilidad y orden de recopilacion.
- Las alertas de `PB-004` solo registran coincidencias internas y no envian notificaciones salientes.
- La consolidacion de `PB-011` sigue siendo la referencia funcional, pero su carga automatizada requiere corregir la discrepancia entre `data/atom/` y el patron que usa el cargador.
- La issue `#17` ya tiene validacion funcional, pero la documentacion de `main` debe seguir tratandola como pendiente de integracion hasta que exista el merge y el borrado de la rama tecnica.

## Dependencias abiertas
- Implementar `PB-012` para exponer en interfaz las vistas funcionales equivalentes al Excel de referencia y ampliar la trazabilidad visible al usuario final.
- Implementar `PB-005` para evolucionar desde el descubrimiento inicial filtrable y la gestion interna de alertas a un MVP mas operativo.
- Actualizar la metadata de paquete si se quiere que describa fielmente la superficie observable de `main`.
