# Manual de administracion y operacion

## Publico objetivo
Persona responsable de preparar el entorno local, arrancar la entrega minima actual y verificar que las superficies visibles responden como se espera.

## Alcance operativo actual
En `main` existe un servicio HTTP local arrancable con `wsgiref.simple_server`. Su alcance operativo es de validacion local y demostracion funcional temprana; no equivale a una operacion productiva completa.

## Prerequisitos
- Acceso al arbol del proyecto en `/opt/apps/podencoti`.
- `python3` compatible con `>=3.12`.
- Entorno virtual activo o directorio `.venv/` disponible si se va a usar `make`.
- `make` para usar los objetivos definidos en `Makefile`.
- Un fichero `.env` con `PORT` definido. Si no existe, puede copiarse desde [`.env.example`](/opt/apps/podencoti/.env.example).
- Para el despliegue en contenedor, disponer de `docker` y `docker compose`.

## Arranque local reproducible
Desde la raiz del proyecto:

```bash
cd /opt/apps/podencoti
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
make test
make run
```

## Arranque en contenedor
Desde la raiz del proyecto:

```bash
cd /opt/apps/podencoti
docker compose up -d --build
docker compose logs -f
```

Resultado esperado:
- la aplicacion responde en `http://127.0.0.1:<PORT>/`
- `data/` persiste fuera de la imagen porque se monta como volumen
- dentro del contenedor la aplicacion escucha en `HOST=0.0.0.0`

## Resultado esperado en esta revision
- `make test` ejecuta 41 pruebas y termina en verde.
- `make run` publica el mensaje `Servidor disponible en http://127.0.0.1:<PORT>` segun el valor configurado en `.env`.
- `docker compose up -d --build` publica la misma aplicacion con el puerto definido por `PORT`.
- Mientras el proceso esta levantado, las rutas `/`, `/api/oportunidades`, `/oportunidades/pcsp-cabildo-licencias-2026`, `/api/oportunidades/pcsp-cabildo-licencias-2026`, `/cobertura-fuentes`, `/api/fuentes`, `/priorizacion-fuentes-reales`, `/api/fuentes-prioritarias`, `/clasificacion-ti` y `/api/clasificacion-ti` responden `200 OK`.

## Verificaciones operativas minimas
- Abrir `http://127.0.0.1:<PORT>/` para revisar el catalogo inicial de oportunidades TI.
- Abrir `http://127.0.0.1:<PORT>/?palabra_clave=licencias` para verificar filtrado funcional en HTML.
- Consultar `http://127.0.0.1:<PORT>/api/oportunidades?procedimiento=Abierto` para verificar filtrado funcional en API.
- Consultar `http://127.0.0.1:<PORT>/api/oportunidades?presupuesto_min=120000&presupuesto_max=90000` para verificar que la API devuelve `400` con validacion explicita de rango.
- Abrir `http://127.0.0.1:<PORT>/oportunidades/pcsp-cabildo-licencias-2026` para revisar una ficha de detalle con rectificacion visible.
- Abrir `http://127.0.0.1:<PORT>/cobertura-fuentes` para revisar la cobertura inicial del MVP.
- Abrir `http://127.0.0.1:<PORT>/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen.
- Abrir `http://127.0.0.1:<PORT>/clasificacion-ti` para revisar la regla TI auditable.
- Consultar las salidas JSON para integracion basica o soporte QA:
  - `http://127.0.0.1:<PORT>/api/oportunidades`
  - `http://127.0.0.1:<PORT>/api/oportunidades/pcsp-cabildo-licencias-2026`
  - `http://127.0.0.1:<PORT>/api/fuentes`
  - `http://127.0.0.1:<PORT>/api/fuentes-prioritarias`
  - `http://127.0.0.1:<PORT>/api/clasificacion-ti`

## Parada controlada
- Interrumpe el proceso con `Ctrl+C`.
- La aplicacion imprime `Servidor detenido de forma controlada.`.

## Operacion no disponible
No existe en `main`:
- servicio gestionado con `systemd`
- proxy inverso documentado
- observabilidad o healthcheck dedicado
- procedimiento de backup o rollback
- despliegue productivo endurecido
- alertas tempranas
- pipeline de seguimiento

## Riesgos operativos
- Las superficies actuales son utiles para validacion temprana, pero no para explotacion operativa continua.
- Comunicar que el producto ya ofrece alertas o pipeline induciria a error.
- `pyproject.toml` sigue describiendo una superficie mas estrecha que la observable hoy; para soporte operativo debe prevalecer el codigo, las rutas verificadas y esta documentacion.
- La priorizacion funcional de nuevas fuentes reales oficiales ya esta visible en `main`, pero no debe confundirse con alertas, pipeline ni otras capacidades de seguimiento.
- Aunque algunos documentos de `product-manager/` sigan arrastrando estado anterior, la operacion revisada en `main` ya expone superficies funcionales para esa priorizacion.
- La entrada de `changelog/2026-03-25.md` que atribuye `PB-004` a `main` no se corresponde con la superficie revisada; mientras no aparezcan rutas o pruebas, esta guia no debe usar esa nota como base operativa.

## Dependencias abiertas para administracion
- Definir estrategia de despliegue productivo cuando exista una aplicacion mas alla del servidor local de demostracion.
- Incorporar mecanismos de configuracion, supervision y observabilidad cuando el alcance operativo lo requiera.
