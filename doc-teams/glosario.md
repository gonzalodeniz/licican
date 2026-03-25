# Glosario

## Publico objetivo
Usuario interno del proyecto que necesita interpretar de forma consistente la terminologia funcional, tecnica y operativa de `PodencoTI`.

## Terminos del producto
- `PodencoTI`: plataforma orientada a centralizar y detectar oportunidades de contratacion publica TI en Canarias.
- `MVP`: alcance minimo inicial del producto; segun la documentacion funcional vigente, debe comunicarse como cobertura inicial priorizada y no como cobertura total.
- `Oportunidad TI`: licitacion o expediente considerado relevante para tecnologia conforme a las reglas funcionales vigentes de clasificacion.
- `Cobertura funcional`: conjunto de fuentes y capacidades que el producto declara cubrir de forma observable y verificable.
- `Fuente oficial`: portal, perfil del contratante u origen institucional desde el que se obtiene informacion de contratacion publica.
- `Clasificacion TI auditable`: superficie visible que expone reglas, exclusiones, casos frontera y ejemplos verificables antes del catalogo.
- `Filtro funcional`: criterio aplicable sobre el catalogo visible y su API para reducir resultados por palabra clave, presupuesto, procedimiento o ubicacion.
- `Pipeline`: seguimiento del estado de trabajo de una oportunidad por parte del usuario; sigue siendo capacidad planificada, no disponible en `main` revisado. La entrada de `changelog/2026-03-25.md` que lo da por implementado no tiene reflejo tecnico visible en esta revision.
- `Alerta temprana`: mecanismo para registrar o notificar nuevas oportunidades compatibles con criterios del usuario; sigue siendo capacidad planificada, no disponible en `main` revisado. La misma observacion aplica a la nota de `changelog/2026-03-25.md` sobre `PB-004`.

## Terminos operativos del repositorio
- `main`: rama de referencia para trabajo funcional, documental y de coordinacion no tecnica.
- `Estado operativo`: etiqueta comun entre equipos para una issue (`nuevo`, `en desarrollo`, `listo para qa`, `no validado`, `validado`, `cerrado`).
- `Impacto documental`: indicador usado por `developer-teams` para señalar que una entrega validada requiere actualizacion documental.
- `Trazabilidad`: relacion explicita entre vision, backlog, historias, casos de uso, implementacion, validacion y documentacion.

## Terminos de esta revision documental
- `Estado real observable`: comportamiento que puede comprobarse en la rama revisada mediante ficheros versionados y comandos reproducibles.
- `Contradiccion documental`: diferencia entre lo que una fuente del repositorio afirma y lo que puede verificarse realmente en `main`.
- `No disponible en main`: capacidad descrita por vision o backlog que no debe documentarse como funcionalidad utilizable hoy.
- `Entrega minima ejecutable`: estado actual de `main` con servidor local, catalogo inicial, filtros funcionales, ficha de detalle, rutas de cobertura, rutas de priorizacion de fuentes reales y rutas de clasificacion TI auditables, ademas de un despliegue local en contenedor, pero sin alertas, pipeline ni despliegue productivo endurecido.
- `Trabajo validado no integrado`: entrega que puede aparecer en `changelog/` o en una issue como validada por `qa-teams`, pero que aun no forma parte del comportamiento observable de `main` hasta su integracion efectiva; esta expresion ya no aplica a `PB-009`, que si forma parte de `main`.

## Contradicciones clave asociadas al glosario
- `Catalogo validado`: expresion historica que hoy si coincide con las rutas y modulos presentes en `main`, porque el catalogo, la ficha de detalle y la priorizacion de fuentes reales ya forman parte de la rama principal.
- `Validado`: estado que puede referirse a una rama tecnica concreta y no necesariamente a funcionalidad ya integrada en `main`; debe interpretarse junto con la rama y la evidencia observable.
