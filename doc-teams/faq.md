# FAQ documental

## Publico objetivo
Personas usuarias internas, equipo tecnico y administracion que necesitan aclarar contradicciones entre vision, historial operativo y comportamiento real de `main`.

## La aplicacion esta disponible para arrancar en `main`?
Si. `make run` levanta un servidor local en `http://127.0.0.1:8000`.

## Entonces que entrega existe realmente hoy?
Existe una entrega minima de descubrimiento con catalogo inicial de oportunidades TI, filtros funcionales sobre ese catalogo, ficha de detalle, cobertura inicial del MVP y clasificacion TI auditable.

## Que rutas estan verificadas?
- `/`
- `/api/oportunidades`
- `/oportunidades/<id>`
- `/api/oportunidades/<id>`
- `/cobertura-fuentes`
- `/api/fuentes`
- `/clasificacion-ti`
- `/api/clasificacion-ti`

## El producto ya tiene catalogo de oportunidades, filtros, alertas o pipeline?
En `main` ya existen catalogo inicial, filtros funcionales y ficha de detalle. No existen todavia alertas ni pipeline, que siguen en backlog y roadmap de `product-manager/`.

## Que filtros existen hoy?
Se pueden aplicar `palabra_clave`, `presupuesto_min`, `presupuesto_max`, `procedimiento` y `ubicacion` tanto en `/` como en `/api/oportunidades`.

## Como responde el sistema si el rango de presupuesto es invalido?
Si `presupuesto_min` es mayor que `presupuesto_max`, la vista HTML mantiene el catalogo y muestra un mensaje de correccion. La API responde `400 Bad Request` con el campo `error_validacion`.

## Sigue habiendo contradicciones documentales relevantes?
Si. La principal contradiccion vigente es `pyproject.toml`, que sigue describiendo el paquete como si solo cubriera cobertura de fuentes, cuando `main` ya expone catalogo, filtros, detalle y clasificacion TI auditable.

## Existe ya la priorizacion de fuentes reales de `PB-009` en `main`?
No. En la app verificada, `/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias` responden `404 Not Found`.
Si un `changelog` la describe como validada, esa nota debe tratarse como desalineada hasta que exista evidencia reproducible en `main`.

## La ficha de detalle aplica rectificaciones o modificaciones oficiales?
Si. El detalle visible resuelve el ultimo dato oficial publicado cuando el expediente tiene actualizaciones versionadas en `data/opportunities.json`.

## Por que la metadata del paquete no menciona la clasificacion TI?
Porque `pyproject.toml` sigue describiendo el paquete solo como cobertura inicial de fuentes. Esa descripcion ha quedado por detras del estado real de `main`, que ya incluye catalogo inicial, ficha de detalle y la superficie auditable de `PB-006`.

## Se puede instalar algo util con `pip install -e .`?
Si. La instalacion editable deja operativa la aplicacion local y permite ejecutar las pruebas.

## Hay pruebas automatizadas disponibles?
Si. `PYTHONPATH=src python3 -m unittest discover -s tests -v` ejecuta 33 pruebas en esta revision.

## Se puede desplegar en produccion con lo que hay ahora?
No hay base documental suficiente para afirmarlo. Solo esta verificado el arranque local con `wsgiref`.

## Que debe tomarse hoy como fuente de verdad?
- Para reglas del repositorio y coordinacion: `AGENTS.md`
- Para vision y alcance funcional esperado: `product-manager/`
- Para el estado tecnico realmente observable en `main`: los manuales actuales de `doc-teams/` y el codigo versionado

## Que dependencias siguen abiertas?
- Implementar `PB-004`, `PB-005` y `PB-009`.
- Definir una estrategia de despliegue real cuando el alcance tecnico lo requiera.
- Actualizar la metadata del paquete si se quiere alinearla con la superficie visible actual.
