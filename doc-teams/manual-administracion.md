# Manual de administracion y operacion

## Publico objetivo
Persona responsable de arrancar, detener, verificar y mantener la entrega actual del proyecto en un entorno local o controlado.

## Alcance operativo actual
Este manual cubre solo la operacion de la version implementada en el repositorio: servidor local para visualizar y exponer la cobertura inicial de fuentes del MVP.

## Prerequisitos operativos
- Acceso al arbol del proyecto en `/opt/apps/podencoti`.
- `python3` compatible con la version declarada en [pyproject.toml](/opt/apps/podencoti/pyproject.toml).
- Puerto local `8000` disponible si se usa la configuracion por defecto.

## Arranque del servicio
Desde la raiz del proyecto:

```bash
cd /opt/apps/podencoti
PYTHONPATH=src python3 -m podencoti.app
```

Validacion inmediata esperada:
- Mensaje `Servidor disponible en http://127.0.0.1:8000`

## Verificacion operativa
Comprobaciones manuales recomendadas tras el arranque:
- Abrir `http://127.0.0.1:8000/` y confirmar que aparece el titulo `Cobertura inicial de fuentes oficiales del MVP`.
- Abrir `http://127.0.0.1:8000/api/fuentes` y confirmar que devuelve `sources` y `summary`.
- Confirmar que el resumen actual es:
  - `MVP`: `3`
  - `Posterior`: `2`
  - `Por definir`: `1`

## Parada del servicio
- Si el proceso se ejecuta en primer plano, detener con `Ctrl+C`.
- No existe por ahora unidad `systemd`, supervisor ni mecanismo de daemonizacion mantenido en el repositorio.

## Mantenimiento de datos de cobertura
La fuente de verdad operativa del contenido publicado es [data/source_coverage.json](/opt/apps/podencoti/data/source_coverage.json).

Antes de modificarla:
- Verifica alineacion con `product-manager/refinamiento-funcional.md` y `product-manager/roadmap.md`.
- Mantén los estados dentro del conjunto soportado: `MVP`, `Posterior`, `Por definir`.
- Conserva la trazabilidad funcional en `referencia_funcional`.

Despues de modificarla:
1. Ejecuta las pruebas:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

2. Arranca el servidor y revisa HTML y JSON.

## Incidencias y diagnostico basico
### El servidor no arranca
Posibles causas:
- `python3` no disponible o version insuficiente.
- Puerto `8000` ocupado.
- Error de importacion por no usar `PYTHONPATH=src` ni instalacion editable.

### La API devuelve error al cargar datos
Posibles causas:
- JSON mal formado en `data/source_coverage.json`.
- Uso de un valor de `estado` no soportado.

### La pagina no refleja lo esperado
Posibles causas:
- Se modifico el JSON sin reiniciar el proceso.
- La fuente funcional de referencia en `product-manager/` no esta alineada con el dato operativo cargado.

## Riesgos y limitaciones
- No hay autenticacion, control de acceso ni endurecimiento de seguridad visible para exponer este servicio fuera de un entorno controlado.
- No existe persistencia historica ni auditoria de cambios en runtime fuera del versionado Git.
- No hay mecanismos implementados de healthcheck, metricas o alertado tecnico.
- La documentacion funcional del producto supera el alcance operativo de la implementacion actual; cualquier uso externo debe comunicar expresamente que esta entrega solo cubre visualizacion de cobertura de fuentes.
