# FAQ documental

## Publico objetivo
Personas usuarias internas, equipo tecnico y administracion que necesitan aclarar contradicciones entre vision, historial operativo y comportamiento real de `main`.

## La aplicacion esta disponible para arrancar en `main`?
Si. `make run` levanta un servidor local usando `PORT` desde `.env` y, por defecto, `8000` si no se define. Tambien existe una ruta de contenedor local con `docker compose up -d --build`, que publica el mismo servicio, levanta la BBDD integrada y monta `data/` como volumen persistente.

## Entonces que entrega existe realmente hoy?
Existe una entrega minima de descubrimiento con catalogo servido desde PostgreSQL por defecto, filtros funcionales sobre ese catalogo, ficha de detalle con origen funcional visible, gestion interna de alertas, cobertura inicial del MVP, priorizacion de fuentes reales oficiales por olas y clasificacion TI auditable.

## Que rutas estan verificadas?
- `/`
- `/api/oportunidades`
- `/oportunidades/<id>`
- `/api/oportunidades/<id>`
- `/alertas`
- `/api/alertas`
- `/cobertura-fuentes`
- `/api/fuentes`
- `/priorizacion-fuentes-reales`
- `/api/fuentes-prioritarias`
- `/clasificacion-ti`
- `/api/clasificacion-ti`

## El producto ya tiene catalogo de oportunidades, filtros, alertas o pipeline?
En `main` ya existen catalogo consolidado, filtros funcionales, ficha de detalle, alertas internas y priorizacion de fuentes reales oficiales por olas. No existe todavia pipeline en la superficie tecnica revisada.

## PB-011 ya esta operativo en `main`?
La intencion funcional sigue documentada, pero en esta checkout la evidencia automatizada no se reproduce completa: los snapshots viven en `data/atom/` y el cargador actual sigue buscando `data/*.atom`. Hasta que esa discrepancia se resuelva, la trazabilidad de `PB-011` debe tratarse como condicionada y no como validacion cerrada.

## La aplicacion ya usa PostgreSQL por defecto?
Si. La issue tecnica #14 ya quedo validada, integrada en `main` y cerrada administrativamente, de modo que PostgreSQL es el backend operativo por defecto para catalogo y detalle. `LICICAN_CATALOG_BACKEND=file` sigue disponible para pruebas aisladas o respaldo.

## PB-012 ya esta operativo en `main`?
No segun la evidencia tecnica revisada en esta documentacion. El changelog de `2026-03-29` la registra como validada, pero en `main` no aparecen rutas, vistas ni pruebas para `/datos-consolidados` ni para las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
Mientras esa desalineacion siga abierta, debe tratarse como trabajo validado no integrado o como evidencia documental contradictoria, no como funcionalidad disponible para usuario o administracion.

## Que filtros existen hoy?
Se pueden aplicar `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion` tanto en `/` como en `/api/oportunidades`.

## Como responde el sistema si el rango de presupuesto es invalido?
Si `presupuesto_min` es mayor que `presupuesto_max`, la vista HTML mantiene el catalogo y muestra un mensaje de correccion. La API responde `400 Bad Request` con el campo `error_validacion`.

## Sigue habiendo contradicciones documentales relevantes?
Si. La principal contradiccion vigente es doble: `pyproject.toml` sigue describiendo el paquete como si solo cubriera cobertura de fuentes, y algunos documentos de `product-manager/` todavia conservan textos previos a la integracion de `PB-011` o al estado ya visible de `PB-004`.
Ademas, el changelog de `2026-03-29` registra `PB-012` como validada sin que la superficie correspondiente aparezca en `main`, asi que esa entrada debe leerse con cautela hasta que el codigo la respalde.

## Por que algunos textos de producto no coinciden con esta documentacion?
Porque esta FAQ toma como referencia el codigo, las rutas y las pruebas ejecutables en `main`. En esta revision, las alertas si se observan en `src/` y `tests/`, y la consolidacion `.atom` ya esta integrada, asi que la contradiccion residual queda en algunos textos funcionales de producto que todavia no se han sincronizado.

## Existe ya la priorizacion de fuentes reales de `PB-009` en `main`?
Si. En la app verificada, `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `200 OK` y muestran `BOC`, `BOP Las Palmas` y `BOE` agrupadas por olas.
Si algun documento de producto sigue describiendo `PB-009` como pendiente de fusion, esa nota debe considerarse desactualizada frente a `main`.

## La ficha de detalle aplica rectificaciones o modificaciones oficiales?
Si. El detalle visible resuelve el ultimo dato oficial publicado cuando el expediente tiene actualizaciones versionadas, y ademas expone el fichero `.atom` de origen cuando procede de la consolidacion.

## Por que la metadata del paquete no menciona la clasificacion TI?
Porque `pyproject.toml` sigue describiendo el paquete solo como cobertura inicial de fuentes. Esa descripcion ha quedado por detras del estado real de `main`, que ya incluye catalogo inicial, ficha de detalle y la superficie auditable de `PB-006`.

## Se puede instalar algo util con `pip install -e .`?
Si. La instalacion editable deja operativa la aplicacion local y permite ejecutar las pruebas.

## Como abro una terminal psql contra la BBDD integrada?
Desde la raiz del proyecto, `make docker-psql` abre una sesion interactiva `psql` contra `postgres-licitaciones`.

## Hay pruebas automatizadas disponibles?
Si. `PYTHONPATH=src python3 -m pytest -v` ejecuta 104 pruebas en verde en esta revision.

## Se puede desplegar en produccion con lo que hay ahora?
No hay base documental suficiente para afirmarlo. Solo esta verificado el arranque local con `wsgiref` y el despliegue local en contenedor.

## Que debe tomarse hoy como fuente de verdad?
- Para reglas del repositorio y coordinacion: `AGENTS.md`
- Para vision y alcance funcional esperado: `product-manager/`
- Para el estado tecnico realmente observable en `main`: los manuales actuales de `doc-teams/` y el codigo versionado
- Si un changelog reciente contradice el codigo visible, debe prevalecer la evidencia reproducible de `main` hasta que se sincronice la documentacion implicada.

## Que dependencias siguen abiertas?
- Exponer `PB-012` en la interfaz para las vistas funcionales del Excel de referencia.
- Implementar `PB-005`.
- Definir una estrategia de despliegue real cuando el alcance tecnico lo requiera.
- Actualizar la metadata del paquete si se quiere alinearla con la superficie visible actual.
