# Manual tecnico

## Publico objetivo
Equipo tecnico que necesita conocer la implementacion actual de `main`, sus rutas verificables y los limites funcionales todavia abiertos.

## Resumen tecnico verificable
`PodencoTI` expone en `main` una aplicacion WSGI minima en Python centrada en dos superficies funcionales previas al catalogo:

- `PB-007`: cobertura inicial visible y verificable de fuentes.
- `PB-006`: regla de clasificacion TI auditable con ejemplos trazables.

## Artefactos tecnicos presentes
- Configuracion de paquete: `pyproject.toml`
- Automatizacion local: `Makefile`
- Aplicacion WSGI: `src/podencoti/app.py`
- Carga de cobertura de fuentes: `src/podencoti/source_coverage.py`
- Carga y evaluacion de reglas TI: `src/podencoti/ti_classification.py`
- Datos versionados: `data/source_coverage.json`, `data/ti_classification_rules.json`
- Suite tecnica: `tests/test_app.py`, `tests/test_source_coverage.py`, `tests/test_ti_classification.py`

## Superficie HTTP vigente
- `/`: vista HTML de cobertura inicial del MVP.
- `/api/fuentes`: JSON con fuentes y resumen por estado.
- `/clasificacion-ti`: vista HTML de la regla TI auditable.
- `/api/clasificacion-ti`: JSON con reglas y ejemplos auditados.

La aplicacion devuelve `404 Not Found` para cualquier otra ruta no declarada.

## Estructura tecnica
- [app.py](/opt/apps/podencoti/src/podencoti/app.py) centraliza el router WSGI, el renderizado HTML y las respuestas JSON.
- [source_coverage.py](/opt/apps/podencoti/src/podencoti/source_coverage.py) valida estados de cobertura permitidos (`MVP`, `Posterior`, `Por definir`) y resume conteos.
- [ti_classification.py](/opt/apps/podencoti/src/podencoti/ti_classification.py) normaliza texto, aplica reglas funcionales y audita ejemplos con tres salidas posibles: `TI`, `No TI` y `Caso frontera`.

## Verificacion reproducible
Desde la raiz del proyecto:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m podencoti.app
```

Resultado verificado en esta revision:
- 15 pruebas automatizadas en verde.
- Servidor local disponible en `http://127.0.0.1:8000`.

## Contradicciones explicitadas
- Parte del historial en `changelog/2026-03-18.md` afirma que `main` no contenia implementacion fuente ni pruebas versionadas; eso contradice el arbol actual.
- Otras entradas del mismo changelog hablan de un catalogo validado con rutas como `/api/oportunidades`; esa superficie no existe en el codigo actual revisado.
- La documentacion funcional de `product-manager/` describe backlog posterior valido, pero no debe leerse como contrato tecnico ya implementado.

## Limitaciones tecnicas actuales
- No existe persistencia de oportunidades ni ingestion real de licitaciones.
- No hay autenticacion, base de datos, tareas programadas ni integracion externa.
- No hay contrato de despliegue productivo versionado, mas alla del arranque local con `wsgiref`.

## Dependencias abiertas
- Implementar `PB-001`, `PB-002` y `PB-003` para pasar de superficies de validacion a un MVP de descubrimiento navegable.
- Resolver documentalmente o administrativamente la contradiccion entre el changelog y el codigo actual cuando corresponda.
