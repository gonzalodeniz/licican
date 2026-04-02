# FAQ documental

## Publico objetivo
Personas usuarias internas, equipo tecnico y administracion que necesitan aclarar contradicciones entre vision, historial operativo y comportamiento real de `main`.

## La aplicacion esta disponible para arrancar en `main`?
Si. `make run` levanta un servidor local usando `PORT` desde `.env` y, por defecto, `8000` si no se define. Tambien existe una ruta de contenedor local con `docker compose up -d --build`, que publica el mismo servicio, levanta la BBDD integrada y monta `data/` como volumen persistente.

## Entonces que entrega existe realmente hoy?
Existe una entrega minima de descubrimiento y seguimiento con catalogo servido desde PostgreSQL por defecto, filtros funcionales sobre ese catalogo, ficha de detalle con origen funcional visible cuando la fuente lo aporta, datos consolidados, pipeline, gestion interna de alertas, gestion administrativa de usuarios, cobertura inicial del MVP, priorizacion de fuentes reales oficiales por olas, clasificacion TI auditable, KPIs y matriz de permisos.

## Que rutas estan verificadas?
- `/`
- `/api/oportunidades`
- `/oportunidades/<id>`
- `/api/oportunidades/<id>`
- `/alertas`
- `/api/alertas`
- `/datos-consolidados`
- `/api/datos-consolidados`
- `/datos-consolidados/licitaciones/<id>`
- `/datos-consolidados/adjudicaciones/<id>`
- `/pipeline`
- `/api/pipeline`
- `/usuarios`
- `/usuarios/<id>`
- `/api/usuarios`
- `/api/usuarios/<id>`
- `/cobertura-fuentes`
- `/api/fuentes`
- `/priorizacion-fuentes-reales`
- `/api/fuentes-prioritarias`
- `/clasificacion-ti`
- `/api/clasificacion-ti`
- `/kpis`
- `/permisos`

## El producto ya tiene catalogo de oportunidades, filtros, alertas, usuarios o pipeline?
En `main` ya existen catalogo consolidado, filtros funcionales, ficha de detalle, datos consolidados, pipeline, alertas internas, gestion administrativa de usuarios, KPIs, permisos y priorizacion de fuentes reales oficiales por olas.

## PB-011 ya esta operativo en `main`?
La intencion funcional sigue documentada y el codigo soporta la consolidacion Atom, pero en esta checkout no hay snapshots `.atom` versionados en `data/`. La reproducibilidad completa depende de aportar muestras temporales o externas; el respaldo versionado visible para el modo `file` es `data/opportunities.json`.

## La aplicacion ya usa PostgreSQL por defecto?
Si. La issue tecnica #14 ya quedo validada, integrada en `main` y cerrada administrativamente, de modo que PostgreSQL es el backend operativo por defecto para catalogo y detalle. `LICICAN_CATALOG_BACKEND=file` sigue disponible para pruebas aisladas o respaldo.

## Ya existe gestion de usuarios en `main`?
Si. La issue #28 ya quedo validada e integrada en `main`. La superficie `/usuarios` permite listar, filtrar, crear, editar y cambiar de estado cuentas, y la API `/api/usuarios` expone el listado y el detalle seleccionable. La persistencia se hace en PostgreSQL. Lo que no existe aun es autenticacion real contra un proveedor externo, SSO o MFA.

## PB-012 ya esta operativo en `main`?
Si. La superficie `/datos-consolidados` expone las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`, con detalle trazable al Excel versionado y a las vistas de fila correspondientes.

## Que filtros existen hoy?
Se pueden aplicar `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion` tanto en `/` como en `/api/oportunidades`.

## Como responde el sistema si el rango de presupuesto es invalido?
Si `presupuesto_min` es mayor que `presupuesto_max`, la vista HTML mantiene el catalogo y muestra un mensaje de correccion. La API responde `400 Bad Request` con el campo `error_validacion`.

## Sigue habiendo contradicciones documentales relevantes?
Si. La principal contradiccion vigente es que `pyproject.toml` sigue describiendo el paquete como si solo cubriera cobertura de fuentes. Ademas, algunos documentos de `product-manager/` todavia arrastran formulaciones anteriores a la consolidacion de `PB-011` o al estado ya visible de `PB-004`.

## Por que algunos textos de producto no coinciden con esta documentacion?
Porque esta FAQ toma como referencia el codigo, las rutas y las pruebas ejecutables en `main`. En esta revision, las alertas, el pipeline y los datos consolidados ya se observan en `src/` y `tests/`, asi que la contradiccion residual queda en algunos textos funcionales de producto que todavia no se han sincronizado.

## Existe ya la priorizacion de fuentes reales de `PB-009` en `main`?
Si. En la app verificada, `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `200 OK` y muestran `BOC`, `BOP Las Palmas` y `BOE` agrupadas por olas.
Si algun documento de producto sigue describiendo `PB-009` como pendiente de fusion, esa nota debe considerarse desactualizada frente a `main`.

## La ficha de detalle aplica rectificaciones o modificaciones oficiales?
Si. El detalle visible resuelve el ultimo dato oficial publicado cuando el expediente tiene actualizaciones versionadas, y ademas expone el fichero de origen cuando procede de la consolidacion o de una fuente que lo incluya.

## Por que la metadata del paquete no menciona la clasificacion TI?
Porque `pyproject.toml` sigue describiendo el paquete solo como cobertura inicial de fuentes. Esa descripcion ha quedado por detras del estado real de `main`, que ya incluye catalogo inicial, ficha de detalle y la superficie auditable de `PB-006`.

## Se puede instalar algo util con `pip install -e .`?
Si. La instalacion editable deja operativa la aplicacion local y permite ejecutar las pruebas.

## Como abro una terminal psql contra la BBDD integrada?
Desde la raiz del proyecto, `make docker-psql` abre una sesion interactiva `psql` contra `postgres-licitaciones`.

## Hay pruebas automatizadas disponibles?
Si. `PYTHONPATH=src python3 -m pytest -v` ejecuta la suite automatizada del proyecto en esta revision.

## Se puede desplegar en produccion con lo que hay ahora?
No hay base documental suficiente para afirmarlo. Solo esta verificado el arranque local con `wsgiref` y el despliegue local en contenedor.

## Que debe tomarse hoy como fuente de verdad?
- Para reglas del repositorio y coordinacion: `AGENTS.md`
- Para vision y alcance funcional esperado: `product-manager/`
- Para el estado tecnico realmente observable en `main`: los manuales actuales de `doc-teams/` y el codigo versionado
- Si un changelog reciente contradice el codigo visible, debe prevalecer la evidencia reproducible de `main` hasta que se sincronice la documentacion implicada.

## Que dependencias siguen abiertas?
- Mantener sincronizada la metadata del paquete con la superficie visible actual.
- Definir una estrategia de despliegue real cuando el alcance tecnico lo requiera.
