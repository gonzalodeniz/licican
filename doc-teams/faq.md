# FAQ documental

## Publico objetivo
Personas usuarias internas, equipo tecnico y administracion que necesitan aclarar contradicciones entre vision, historial operativo y comportamiento real de `main`.

## La aplicacion esta disponible para arrancar en `main`?
Si. `make run` levanta un servidor local en `http://127.0.0.1:8000`.

## Entonces que entrega existe realmente hoy?
Existe una entrega minima centrada en cobertura inicial del MVP y clasificacion TI auditable. No existe todavia el catalogo de oportunidades ni el resto de capacidades del MVP de descubrimiento.

## Que rutas estan verificadas?
- `/`
- `/api/fuentes`
- `/clasificacion-ti`
- `/api/clasificacion-ti`

## El producto ya tiene catalogo de oportunidades, filtros, alertas o pipeline?
No en `main`. Esas capacidades siguen en backlog y roadmap de `product-manager/`.

## El historial operativo del 2026-03-18 no dice cosas distintas?
Si. Hay entradas que afirman que no existia implementacion fuente y otras que hablan de un catalogo ya validado. Ninguna de esas afirmaciones coincide con el codigo actual revisado. Como `doc-teams`, la referencia documental valida para comportamiento actual es lo reproducible desde la rama.

## Se puede instalar algo util con `pip install -e .`?
Si. La instalacion editable deja operativa la aplicacion local y permite ejecutar las pruebas.

## Hay pruebas automatizadas disponibles?
Si. `PYTHONPATH=src python3 -m unittest discover -s tests -v` ejecuta 15 pruebas en esta revision.

## Se puede desplegar en produccion con lo que hay ahora?
No hay base documental suficiente para afirmarlo. Solo esta verificado el arranque local con `wsgiref`.

## Que debe tomarse hoy como fuente de verdad?
- Para reglas del repositorio y coordinacion: `AGENTS.md`
- Para vision y alcance funcional esperado: `product-manager/`
- Para el estado tecnico realmente observable en `main`: los manuales actuales de `doc-teams/` y el codigo versionado

## Que dependencias siguen abiertas?
- Implementar `PB-001`, `PB-002` y `PB-003`.
- Definir una estrategia de despliegue real cuando el alcance tecnico lo requiera.
- Resolver administrativamente la contradiccion del changelog historico con el estado actual del codigo.
