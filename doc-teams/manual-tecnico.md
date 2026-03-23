# Manual tecnico

## Publico objetivo
Equipo tecnico que necesita conocer la implementacion actual de `main`, sus rutas verificables y los limites funcionales todavia abiertos.

## Resumen tecnico verificable
`PodencoTI` expone en `main` una aplicacion WSGI minima en Python con cinco piezas funcionales verificables:

- `PB-001`: catalogo inicial de oportunidades TI.
- `PB-003`: filtros funcionales aplicados sobre el catalogo HTML y la API JSON.
- `PB-002`: ficha resumida de detalle por oportunidad visible.
- `PB-007`: cobertura inicial visible y verificable de fuentes.
- `PB-006`: regla de clasificacion TI auditable con ejemplos trazables.

La descripcion de paquete en `pyproject.toml` sigue mencionando solo cobertura de fuentes. Esa metadata ya no resume por completo el comportamiento observable de la rama.

## Artefactos tecnicos presentes
- Configuracion de paquete: `pyproject.toml`
- Automatizacion local: `Makefile`
- Aplicacion WSGI: `src/podencoti/app.py`
- Catalogo y detalle de oportunidades: `src/podencoti/opportunity_catalog.py`
- Carga de cobertura de fuentes: `src/podencoti/source_coverage.py`
- Carga y evaluacion de reglas TI: `src/podencoti/ti_classification.py`
- Datos versionados: `data/opportunities.json`, `data/source_coverage.json`, `data/ti_classification_rules.json`
- Suite tecnica: `tests/test_app.py`, `tests/test_opportunity_catalog.py`, `tests/test_source_coverage.py`, `tests/test_ti_classification.py`

## Superficie HTTP vigente
- `/`: vista HTML del catalogo inicial de oportunidades TI con formulario de filtros funcionales.
- `/api/oportunidades`: JSON del catalogo filtrado por cobertura MVP y clasificacion TI.
- `/oportunidades/<id>`: ficha HTML de detalle de una oportunidad visible.
- `/api/oportunidades/<id>`: JSON trazable de la ficha de detalle.
- `/cobertura-fuentes`: vista HTML de cobertura inicial del MVP.
- `/api/fuentes`: JSON con fuentes y resumen por estado.
- `/clasificacion-ti`: vista HTML de la regla TI auditable.
- `/api/clasificacion-ti`: JSON con reglas y ejemplos auditados.

La aplicacion devuelve `404 Not Found` para cualquier otra ruta no declarada.
Los parametros funcionales visibles hoy para `/` y `/api/oportunidades` son `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion`.
Si `presupuesto_min` es mayor que `presupuesto_max`, la API responde `400 Bad Request` y la vista HTML mantiene el catalogo base junto con un mensaje de correccion.

### Campos visibles por superficie
- `/api/oportunidades`: devuelve `referencia_funcional`, `cobertura_aplicada`, `total_registros_origen`, `total_oportunidades_visibles`, `total_oportunidades_catalogo`, `filtros_activos`, `error_validacion`, `filtros_disponibles` y `oportunidades`.
- `/api/oportunidades/<id>`: devuelve datos criticos visibles, `actualizacion_oficial_mas_reciente` y `historial_actualizaciones`.
- `/api/fuentes`: devuelve `sources` y `summary`.
- `/api/clasificacion-ti`: devuelve `referencia_funcional`, `reglas` y `ejemplos_auditados`.

## Estructura tecnica
- [app.py](/opt/apps/podencoti/src/podencoti/app.py) centraliza el router WSGI, el renderizado HTML y las respuestas JSON.
- [opportunity_catalog.py](/opt/apps/podencoti/src/podencoti/opportunity_catalog.py) carga registros versionados, filtra por cobertura MVP, aplica la clasificacion TI y resuelve el ultimo dato oficial visible para ficha y catalogo.
- [source_coverage.py](/opt/apps/podencoti/src/podencoti/source_coverage.py) valida estados de cobertura permitidos (`MVP`, `Posterior`, `Por definir`) y resume conteos.
- [ti_classification.py](/opt/apps/podencoti/src/podencoti/ti_classification.py) normaliza texto, aplica reglas funcionales y audita ejemplos con tres salidas posibles: `TI`, `No TI` y `Caso frontera`.

## Verificacion reproducible
Desde la raiz del proyecto:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m podencoti.app
```

Resultado verificado en esta revision:
- 33 pruebas automatizadas en verde.
- Servidor local disponible en `http://127.0.0.1:8000`.

## Contradicciones explicitadas
- `pyproject.toml` sigue describiendo el paquete como una release centrada solo en cobertura de fuentes, aunque la rama ya expone catalogo, filtros, detalle y clasificacion TI auditable.
- La documentacion funcional de `product-manager/` describe backlog posterior valido, pero no debe leerse como contrato tecnico ya implementado para alertas, pipeline o recopilacion real desde nuevas fuentes oficiales.

## Limitaciones tecnicas actuales
- No existe persistencia de usuario ni ingestion automatizada real de licitaciones; el catalogo se alimenta desde `data/opportunities.json`.
- No hay autenticacion, base de datos, tareas programadas ni integracion externa.
- No hay contrato de despliegue productivo versionado, mas alla del arranque local con `wsgiref`.
- La priorizacion de fuentes reales de `PB-009` no esta expuesta en la app verificada: `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `404 Not Found`.
- Si una entrada de `changelog/` afirma que `PB-009` ya esta validada, esa afirmacion no debe tomarse como evidencia tecnica hasta que la ruta sea reproducible en `main`.

## Dependencias abiertas
- Implementar `PB-004`, `PB-005` y `PB-009` para evolucionar desde el descubrimiento inicial filtrable a un MVP mas operativo y con fuentes reales adicionales.
- Actualizar la metadata de paquete si se quiere que describa fielmente la superficie observable de `main`.
