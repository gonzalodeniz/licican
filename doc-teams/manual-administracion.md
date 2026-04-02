# Manual de administracion y operacion

## Publico objetivo
Persona responsable de preparar el entorno local, arrancar la entrega minima actual y verificar que las superficies visibles responden como se espera.

## Alcance operativo actual
En `main` existe un servicio HTTP local arrancable con `wsgiref.simple_server`. Su alcance operativo es de validacion local y demostracion funcional temprana; no equivale a una operacion productiva completa, aunque ya expone catalogo, detalle, datos consolidados, pipeline, alertas, usuarios, KPIs y permisos.

## Prerequisitos
- Acceso al arbol del proyecto en `/opt/apps/licican`.
- `python3` compatible con `>=3.12`.
- Entorno virtual activo o directorio `.venv/` disponible si se va a usar `make`.
- `make` para usar los objetivos definidos en `Makefile`.
- Un fichero `.env` con `PORT` definido. Si no existe, puede copiarse desde [`.env.example`](/opt/apps/licican/.env.example).
- Un fichero `.env` con `DB_PORT` definido si se quiere exponer la BBDD integrada en un puerto distinto; por defecto se usa `15432`.
- Un fichero `.env` con `LICICAN_CATALOG_BACKEND` definido si se quiere forzar `file`; por defecto se usa PostgreSQL.
- Un fichero `.env` con `LICICAN_DATABASE_URL` o con las variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` definido si se quiere personalizar la conexion a PostgreSQL.
- Si se quieren guardar alertas en una ruta alternativa, configurar `LICICAN_ALERTS_PATH`; por defecto se usa `data/alerts.json`.
- Si se quieren guardar oportunidades de seguimiento en una ruta alternativa, configurar `LICICAN_PIPELINE_PATH`; por defecto se usa `data/pipeline.json`.
- Para el despliegue en contenedor, disponer de `docker` y `docker compose`.

## Arranque local reproducible
Desde la raiz del proyecto:

```bash
cd /opt/apps/licican
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
make test
make run
```

## Arranque en contenedor
Desde la raiz del proyecto:

```bash
cd /opt/apps/licican
docker compose up -d --build
# En otra terminal, si quieres ver logs:
# docker compose logs -f
make docker-psql
```

Resultado esperado:
- la aplicacion responde en `http://127.0.0.1:<PORT>/`
- `data/` persiste fuera de la imagen porque se monta como volumen
- dentro del contenedor la aplicacion escucha en `HOST=0.0.0.0`
- la gestion de usuarios responde en `http://127.0.0.1:<PORT>/usuarios` y la API en `http://127.0.0.1:<PORT>/api/usuarios`
- el pipeline responde en `http://127.0.0.1:<PORT>/pipeline` y la API en `http://127.0.0.1:<PORT>/api/pipeline`
- los datos consolidados responden en `http://127.0.0.1:<PORT>/datos-consolidados` y la API en `http://127.0.0.1:<PORT>/api/datos-consolidados`
- los KPIs y la matriz de permisos responden en `http://127.0.0.1:<PORT>/kpis` y `http://127.0.0.1:<PORT>/permisos`

## Resultado esperado en esta revision
- `make test` ejecuta 131 pruebas en verde con `pytest`.
- `make run` publica el mensaje `Servidor disponible en http://127.0.0.1:<PORT>` segun el valor configurado en `.env`, o el siguiente puerto libre si el solicitado esta ocupado.
- `docker compose up -d --build` publica la misma aplicacion con el puerto definido por `PORT` y levanta la BBDD integrada.
- `make docker-psql` abre una terminal `psql` contra `postgres-licitaciones`.
- La aplicacion usa PostgreSQL como backend por defecto; el modo `file` queda reservado para pruebas aisladas o escenarios de respaldo.
- Mientras el proceso esta levantado, las rutas `/`, `/api/oportunidades`, `/oportunidades/pcsp-cabildo-licencias-2026`, `/api/oportunidades/pcsp-cabildo-licencias-2026`, `/datos-consolidados`, `/api/datos-consolidados`, `/datos-consolidados/licitaciones/114-2025`, `/datos-consolidados/adjudicaciones/2565-2024-pt1-pccntr-4934579`, `/pipeline`, `/api/pipeline`, `/alertas`, `/api/alertas`, `/cobertura-fuentes`, `/api/fuentes`, `/priorizacion-fuentes-reales`, `/api/fuentes-prioritarias`, `/clasificacion-ti`, `/api/clasificacion-ti`, `/kpis` y `/permisos` responden `200 OK`.
- Mientras el proceso esta levantado, las rutas `/usuarios`, `/usuarios/usr-003`, `/api/usuarios` y `/api/usuarios/usr-003` tambien responden segun el rol de acceso y el estado de los datos de ejemplo.
- La ficha de detalle muestra el fichero `.atom` origen cuando la consolidacion de `PB-011` recibe snapshots Atom de entrada; si no hay ficheros Atom en `data/`, el respaldo visible es `data/opportunities.json`.

## Verificaciones operativas minimas
- Abrir `http://127.0.0.1:<PORT>/` para revisar el catalogo inicial de oportunidades TI.
- Abrir `http://127.0.0.1:<PORT>/?palabra_clave=licencias` para verificar filtrado funcional en HTML.
- Consultar `http://127.0.0.1:<PORT>/api/oportunidades?procedimiento=Abierto` para verificar filtrado funcional en API.
- Consultar `http://127.0.0.1:<PORT>/api/oportunidades?presupuesto_min=120000&presupuesto_max=90000` para verificar que la API devuelve `400` con validacion explicita de rango.
- Abrir `http://127.0.0.1:<PORT>/oportunidades/pcsp-cabildo-licencias-2026` para revisar una ficha de detalle con rectificacion visible.
- Abrir `http://127.0.0.1:<PORT>/oportunidades/pcsp-cabildo-licencias-2026` para revisar una ficha de detalle con rectificacion visible y fichero de origen cuando exista consolidacion Atom.
- Abrir `http://127.0.0.1:<PORT>/datos-consolidados` para revisar las tres pestañas del Excel versionado.
- Abrir `http://127.0.0.1:<PORT>/pipeline` para guardar una oportunidad y comprobar que el seguimiento evita duplicados.
- Abrir `http://127.0.0.1:<PORT>/alertas` para crear una alerta interna, comprobar que no admite formularios vacios y verificar su edicion o desactivacion.
- Abrir `http://127.0.0.1:<PORT>/usuarios` para revisar el listado, la creacion y el detalle de cuentas de usuario.
- Abrir `http://127.0.0.1:<PORT>/kpis` para revisar el resumen de cobertura, adopcion y uso.
- Abrir `http://127.0.0.1:<PORT>/permisos` para revisar la matriz funcional por rol.
- Abrir `http://127.0.0.1:<PORT>/cobertura-fuentes` para revisar la cobertura inicial del MVP.
- Abrir `http://127.0.0.1:<PORT>/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen.
- Abrir `http://127.0.0.1:<PORT>/clasificacion-ti` para revisar la regla TI auditable.
- Consultar las salidas JSON para integracion basica o soporte QA:
  - `http://127.0.0.1:<PORT>/api/oportunidades`
  - `http://127.0.0.1:<PORT>/api/oportunidades/pcsp-cabildo-licencias-2026`
  - `http://127.0.0.1:<PORT>/api/alertas`
  - `http://127.0.0.1:<PORT>/api/fuentes`
  - `http://127.0.0.1:<PORT>/api/fuentes-prioritarias`
  - `http://127.0.0.1:<PORT>/api/clasificacion-ti`

## Parada controlada
- Interrumpe el proceso con `Ctrl+C`.
- La aplicacion imprime `Servidor detenido de forma controlada.`

## Operacion no disponible
No existe en `main`:
- servicio gestionado con `systemd`
- proxy inverso documentado
- observabilidad o healthcheck dedicado
- procedimiento de backup o rollback
- despliegue productivo endurecido
- gestion externa real de identidades, SSO o MFA
- notificaciones salientes de alertas

## Riesgos operativos
- Las superficies actuales son utiles para validacion temprana, pero no para explotacion operativa continua.
- Comunicar que el producto ya ofrece notificaciones salientes induciria a error; las alertas visibles son internas y no envian notificaciones salientes.
- La gestion de usuarios se apoya en PostgreSQL, con las tablas `usuario`, `usuario_superficie` y `usuario_historial`; si la base no responde, la aplicacion devuelve un error controlado.
- `pyproject.toml` sigue describiendo una superficie mas estrecha que la observable hoy; para soporte operativo debe prevalecer el codigo, las rutas verificadas y esta documentacion.
- La priorizacion funcional de nuevas fuentes reales oficiales ya esta visible en `main`, y el pipeline ya puede operarse desde `/pipeline` y `/api/pipeline`.
- Aunque algunos documentos de `product-manager/` sigan arrastrando estado anterior, la operacion revisada en `main` ya expone superficies funcionales para esa priorizacion.
- Las alertas de `PB-004` ya se pueden operar localmente desde `/alertas` y `/api/alertas`.
- La entrega administrable revisada ya opera sobre PostgreSQL por defecto; `LICICAN_CATALOG_BACKEND=file` conserva la ruta de apoyo basada en fichero.
- La carga Atom sigue condicionada por la disponibilidad de snapshots `.atom`; si no hay ficheros Atom en `data/`, el respaldo operativo es `data/opportunities.json`.
- La BBDD integrada se publica en `DB_PORT` y puede abrirse por terminal con `make docker-psql`.

## Dependencias abiertas para administracion
- Definir estrategia de despliegue productivo cuando exista una aplicacion mas alla del servidor local de demostracion.
- Incorporar mecanismos de configuracion, supervision y observabilidad cuando el alcance operativo lo requiera.
