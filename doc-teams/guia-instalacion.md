# Guia de instalacion

## Publico objetivo
Equipo tecnico, QA o soporte que necesita preparar el proyecto en local de forma reproducible.

## Objetivo real de esta guia
Instalar la entrega minima actual de `PodencoTI`, dejar operativo el entorno local y verificar sus rutas visibles y su suite tecnica.

## Prerequisitos
- Sistema con `python3`.
- Version compatible: `3.12` o superior.
- Acceso local al repositorio en `/opt/apps/podencoti`.

## Preparacion local
1. Situate en la raiz del proyecto:

```bash
cd /opt/apps/podencoti
```

2. Crea el entorno virtual recomendado:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala el paquete en modo editable:

```bash
python3 -m pip install -e .
```

## Verificaciones posteriores
1. Ejecuta la suite tecnica:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Resultado esperado en esta revision:
- 15 pruebas en verde

2. Comprueba el objetivo de pruebas del `Makefile`:

```bash
make test
```

Resultado esperado en esta revision:
- ejecucion correcta de la misma suite automatizada

3. Arranca la aplicacion local:

```bash
make run
```

Resultado esperado en esta revision:
- mensaje `Servidor disponible en http://127.0.0.1:8000`

4. Verifica las rutas principales:

```bash
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/api/fuentes
curl -i http://127.0.0.1:8000/clasificacion-ti
curl -i http://127.0.0.1:8000/api/clasificacion-ti
```

## Que queda instalado realmente
- Paquete `podencoti` en modo editable.
- Aplicacion WSGI local para cobertura y clasificacion TI auditables.
- Acceso a datos versionados en `data/` y a la suite automatizada en `tests/`.

## Que no queda disponible
- Catalogo real de oportunidades.
- Detalle de licitaciones.
- Filtros, alertas o pipeline.
- Componentes de despliegue productivo.

## Limitaciones y dependencias abiertas
- La instalacion deja operativa una entrega minima de validacion, no el MVP completo descrito en backlog.
- Algunas entradas del historial operativo del repositorio no reflejan el estado actual del codigo; verifica siempre contra esta guia y contra las pruebas.
