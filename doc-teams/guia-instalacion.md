# Guia de instalacion de PodencoTI

## Publico objetivo
Equipo tecnico o persona responsable de ejecutar el proyecto en local para revision funcional o tecnica.

## Estado de la entrega documentada
Esta guia instala y ejecuta la entrega actual del repositorio: un servidor WSGI minimo que publica la cobertura inicial de fuentes oficiales del MVP definida en `PB-007`.

## Prerequisitos
- Sistema con `python3` disponible.
- Version de Python compatible: `3.12` o superior, segun [pyproject.toml](/opt/apps/podencoti/pyproject.toml).
- Acceso al repositorio local en `/opt/apps/podencoti`.

## Estructura relevante
- Codigo de aplicacion: [src/podencoti/app.py](/opt/apps/podencoti/src/podencoti/app.py)
- Datos versionados de cobertura: [data/source_coverage.json](/opt/apps/podencoti/data/source_coverage.json)
- Pruebas tecnicas: [tests/test_app.py](/opt/apps/podencoti/tests/test_app.py) y [tests/test_source_coverage.py](/opt/apps/podencoti/tests/test_source_coverage.py)

## Instalacion recomendada
1. Situa la terminal en la raiz del proyecto:

```bash
cd /opt/apps/podencoti
```

2. Crea un entorno virtual si quieres aislar la ejecucion:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala el paquete en modo editable:

```bash
python3 -m pip install -e .
```

## Ejecucion sin instalacion editable
Si no deseas instalar el paquete, la aplicacion tambien puede ejecutarse con `PYTHONPATH=src`.

## Verificacion tecnica minima
Ejecuta la suite de pruebas incluida:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Resultado esperado en esta version:
- `6` pruebas superadas.
- Sin errores ni fallos.

## Arranque local
Inicia el servidor HTTP local:

```bash
PYTHONPATH=src python3 -m podencoti.app
```

Resultado esperado:
- Mensaje de consola indicando `Servidor disponible en http://127.0.0.1:8000`

## Verificacion funcional manual
Con el servidor en marcha:
- Abre `http://127.0.0.1:8000/` para ver la pagina HTML de cobertura.
- Abre `http://127.0.0.1:8000/api/fuentes` para obtener la salida JSON.

## Limitaciones conocidas
- No existe comando CLI propio, servicio de sistema ni contenedor documentado en la version actual.
- No hay fichero de requisitos separado ni dependencias de runtime adicionales declaradas fuera del propio paquete.
- La guia no cubre despliegue productivo porque el repositorio no incluye aun una topologia de despliegue implementada.
