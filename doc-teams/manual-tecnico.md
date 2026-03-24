# Manual tecnico

## Publico objetivo
Equipo tecnico que necesita conocer la implementacion actual de `main`, sus rutas verificables y los limites funcionales todavia abiertos.

## Resumen tecnico verificable
`PodencoTI` expone en `main` una aplicacion WSGI minima en Python con seis piezas funcionales verificables y un despliegue local en contenedor:

- `PB-001`: catalogo inicial de oportunidades TI.
- `PB-003`: filtros funcionales aplicados sobre el catalogo HTML y la API JSON.
- `PB-002`: ficha resumida de detalle por oportunidad visible.
- `PB-007`: cobertura inicial visible y verificable de fuentes.
- `PB-006`: regla de clasificacion TI auditable con ejemplos trazables.
- `PB-009`: priorizacion visible de fuentes reales oficiales por olas.
- Despliegue local en contenedor con `Dockerfile` y `docker-compose.yml`.

La descripcion de paquete en `pyproject.toml` sigue mencionando solo cobertura de fuentes. Esa metadata ya no resume por completo el comportamiento observable de la rama.

## Artefactos tecnicos presentes
- Configuracion de paquete: `pyproject.toml`
- Automatizacion local: `Makefile`
- Aplicacion WSGI: `src/podencoti/app.py`
- Catalogo y detalle de oportunidades: `src/podencoti/opportunity_catalog.py`
- Carga de cobertura de fuentes: `src/podencoti/source_coverage.py`
- Priorizacion de fuentes reales oficiales: `src/podencoti/real_source_prioritization.py`
- Carga y evaluacion de reglas TI: `src/podencoti/ti_classification.py`
- Datos versionados: `data/opportunities.json`, `data/source_coverage.json`, `data/real_source_prioritization.json`, `data/ti_classification_rules.json`
- Suite tecnica: `tests/test_app.py`, `tests/test_opportunity_catalog.py`, `tests/test_real_source_prioritization.py`, `tests/test_source_coverage.py`, `tests/test_ti_classification.py`
- Contenedorizacion local: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

## Superficie HTTP vigente
- `/`: vista HTML del catalogo inicial de oportunidades TI con formulario de filtros funcionales.
- `/api/oportunidades`: JSON del catalogo filtrado por cobertura MVP y clasificacion TI.
- `/oportunidades/<id>`: ficha HTML de detalle de una oportunidad visible.
- `/api/oportunidades/<id>`: JSON trazable de la ficha de detalle.
- `/cobertura-fuentes`: vista HTML de cobertura inicial del MVP.
- `/api/fuentes`: JSON con fuentes y resumen por estado.
- `/priorizacion-fuentes-reales`: vista HTML de priorizacion de fuentes reales oficiales.
- `/api/fuentes-prioritarias`: JSON con fuentes priorizadas, resumen por olas y elementos fuera de alcance de esta iteracion.
- `/clasificacion-ti`: vista HTML de la regla TI auditable.
- `/api/clasificacion-ti`: JSON con reglas y ejemplos auditados.

La aplicacion devuelve `404 Not Found` para cualquier otra ruta no declarada.
Los parametros funcionales visibles hoy para `/` y `/api/oportunidades` son `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
Si `presupuesto_min` es mayor que `presupuesto_max`, la API responde `400 Bad Request` y la vista HTML mantiene el catalogo base junto con un mensaje de correccion.

### Campos visibles por superficie
- `/api/oportunidades`: devuelve `referencia_funcional`, `cobertura_aplicada`, `total_registros_origen`, `total_oportunidades_visibles`, `total_oportunidades_catalogo`, `filtros_activos`, `error_validacion`, `filtros_disponibles` y `oportunidades`.
- `/api/oportunidades/<id>`: devuelve datos criticos visibles, `actualizacion_oficial_mas_reciente` y `historial_actualizaciones`.
- `/api/fuentes`: devuelve `sources` y `summary`.
- `/priorizacion-fuentes-reales`: devuelve una tabla HTML con `Ola`, `Fuente real oficial`, `Categoria`, `Alcance`, `Justificacion` y `Trazabilidad`.
- `/api/fuentes-prioritarias`: devuelve `referencia_funcional`, `sources`, `summary` y `fuera_de_alcance`.
- `/api/clasificacion-ti`: devuelve `referencia_funcional`, `reglas` y `ejemplos_auditados`.

## Estructura tecnica
- [app.py](/opt/apps/podencoti/src/podencoti/app.py) centraliza el router WSGI, el renderizado HTML y las respuestas JSON.
- [opportunity_catalog.py](/opt/apps/podencoti/src/podencoti/opportunity_catalog.py) carga registros versionados, filtra por cobertura MVP, aplica la clasificacion TI y resuelve el ultimo dato oficial visible para ficha y catalogo.
- [source_coverage.py](/opt/apps/podencoti/src/podencoti/source_coverage.py) valida estados de cobertura permitidos (`MVP`, `Posterior`, `Por definir`) y resume conteos.
- [real_source_prioritization.py](/opt/apps/podencoti/src/podencoti/real_source_prioritization.py) valida las olas permitidas (`Ola 1`, `Ola 2`, `Ola 3`), ordena las fuentes por prioridad y resume la distribucion por ola.
- [ti_classification.py](/opt/apps/podencoti/src/podencoti/ti_classification.py) normaliza texto, aplica reglas funcionales y audita ejemplos con tres salidas posibles: `TI`, `No TI` y `Caso frontera`.

## Verificacion reproducible
Desde la raiz del proyecto:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m podencoti.app
docker compose up -d --build
```

Resultado verificado en esta revision:
- 41 pruebas automatizadas en verde.
- Servidor local disponible en `http://127.0.0.1:<PORT>`, usando `PORT` desde `.env` y, por defecto, `8000` si no se define.
- Contenedor accesible en `http://127.0.0.1:<PORT>` cuando `docker-compose.yml` publica la aplicacion con `HOST=0.0.0.0`.

## Contradicciones explicitadas
- `pyproject.toml` sigue describiendo el paquete como una release centrada solo en cobertura de fuentes, aunque la rama ya expone catalogo, filtros, detalle y clasificacion TI auditable.
- La documentacion funcional de `product-manager/` describe backlog posterior valido, pero no debe leerse como contrato tecnico ya implementado para alertas, pipeline o recopilacion real desde nuevas fuentes oficiales.
- La documentacion funcional de `product-manager/` sigue mostrando algunos textos anteriores a la fusion de `PB-009`; cuando contradiga a `main`, la evidencia tecnica vigente debe prevalecer y esa fuente debe corregirse.

## Limitaciones tecnicas actuales
- No existe persistencia de usuario ni ingestion automatizada real de licitaciones; el catalogo se alimenta desde `data/opportunities.json`.
- No hay autenticacion, base de datos, tareas programadas ni integracion externa.
- No hay contrato de despliegue productivo versionado, mas alla del arranque local con `wsgiref` y la publicacion local en contenedor.
- La priorizacion de fuentes reales de `PB-009` ya esta expuesta en la app verificada con `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`.
- La entrega de `PB-009` no habilita alertas ni pipeline; solo refuerza origen, trazabilidad y orden de recopilacion.

## Dependencias abiertas
- Implementar `PB-004` y `PB-005` para evolucionar desde el descubrimiento inicial filtrable a un MVP mas operativo.
- Actualizar la metadata de paquete si se quiere que describa fielmente la superficie observable de `main`.
