# Guia de instalacion

## Publico objetivo
Equipo tecnico, QA o soporte que necesita preparar el proyecto en local de forma reproducible.

## Objetivo real de esta guia
Instalar la entrega minima actual de `PodencoTI`, dejar operativo el entorno local o contenedorizado y verificar sus rutas visibles y su suite tecnica.

## Prerequisitos
- Sistema con `python3`.
- Version compatible: `3.12` o superior.
- Acceso local al repositorio en `/opt/apps/podencoti`.
- Para la ruta en contenedor, disponer de `docker` y `docker compose`.

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

4. Prepara la configuracion local:

```bash
cp .env.example .env
```

Edita `.env` y ajusta al menos `PORT` si quieres usar un puerto distinto del valor por defecto.
Si vas a ejecutar el contenedor, `PORT` sigue siendo el puerto publicado y la aplicacion usa `HOST=0.0.0.0` dentro de Compose.

## Verificaciones posteriores
1. Ejecuta la suite tecnica:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Resultado esperado en esta revision:
- 41 pruebas en verde

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
- mensaje `Servidor disponible en http://127.0.0.1:<PORT>` segun el valor definido en `.env`

4. Arranca la aplicacion en contenedor:

```bash
docker compose up -d --build
docker compose logs -f
```

Resultado esperado en esta revision:
- el contenedor publica la app en `http://127.0.0.1:<PORT>/`
- `data/` queda montado como volumen persistente
- la aplicacion escucha dentro del contenedor en `HOST=0.0.0.0`

5. Verifica las rutas principales:

```bash
curl -i http://127.0.0.1:<PORT>/
curl -i http://127.0.0.1:<PORT>/api/oportunidades
curl -i "http://127.0.0.1:<PORT>/?palabra_clave=licencias"
curl -i "http://127.0.0.1:<PORT>/api/oportunidades?procedimiento=Abierto"
curl -i "http://127.0.0.1:<PORT>/api/oportunidades?presupuesto_min=120000&presupuesto_max=90000"
curl -i http://127.0.0.1:<PORT>/oportunidades/pcsp-cabildo-licencias-2026
curl -i http://127.0.0.1:<PORT>/api/oportunidades/pcsp-cabildo-licencias-2026
curl -i http://127.0.0.1:<PORT>/cobertura-fuentes
curl -i http://127.0.0.1:<PORT>/api/fuentes
curl -i http://127.0.0.1:<PORT>/priorizacion-fuentes-reales
curl -i http://127.0.0.1:<PORT>/api/fuentes-prioritarias
curl -i http://127.0.0.1:<PORT>/clasificacion-ti
curl -i http://127.0.0.1:<PORT>/api/clasificacion-ti
```

## Que queda instalado realmente
- Paquete `podencoti` en modo editable.
- Aplicacion WSGI local para catalogo inicial, filtros funcionales, ficha de detalle, cobertura, priorizacion de fuentes reales y clasificacion TI auditables.
- Acceso a datos versionados en `data/` y a la suite automatizada en `tests/`.
- Imagen Docker minima con la misma superficie funcional, apta para despliegue local en contenedor.

## Que no queda disponible
- Alertas o pipeline.
- Despliegue productivo endurecido.

## Limitaciones y dependencias abiertas
- La instalacion deja operativa una entrega minima de descubrimiento, no el MVP completo descrito en backlog.
- Los datos del catalogo son versionados y estaticos; no existe todavia rastreo automatizado en ejecucion local.
- `pyproject.toml` sigue describiendo una release mas limitada que la realmente visible; verifica siempre contra esta guia, el codigo y las pruebas.
- La priorizacion de fuentes reales ya forma parte de la instalacion utilizable, pero no activa alertas ni pipeline.
