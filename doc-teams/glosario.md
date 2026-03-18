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
- `Pipeline`: seguimiento del estado de trabajo de una oportunidad por parte del usuario; sigue siendo capacidad planificada, no disponible en `main`.
- `Alerta temprana`: mecanismo para registrar o notificar nuevas oportunidades compatibles con criterios del usuario; sigue siendo capacidad planificada, no disponible en `main`.

## Terminos operativos del repositorio
- `main`: rama de referencia para trabajo funcional, documental y de coordinacion no tecnica.
- `Estado operativo`: etiqueta comun entre equipos para una issue (`nuevo`, `en desarrollo`, `listo para qa`, `no validado`, `validado`, `cerrado`).
- `Impacto documental`: indicador usado por `developer-teams` para señalar que una entrega validada requiere actualizacion documental.
- `Trazabilidad`: relacion explicita entre vision, backlog, historias, casos de uso, implementacion, validacion y documentacion.

## Terminos de esta revision documental
- `Estado real observable`: comportamiento que puede comprobarse en la rama revisada mediante ficheros versionados y comandos reproducibles.
- `Contradiccion documental`: diferencia entre lo que una fuente del repositorio afirma y lo que puede verificarse realmente en `main`.
- `No disponible en main`: capacidad descrita por vision o backlog que no debe documentarse como funcionalidad utilizable hoy.
- `Entrega minima ejecutable`: estado actual de `main` con servidor local, rutas de cobertura y rutas de clasificacion TI, pero sin catalogo ni flujos de usuario finales.

## Contradicciones clave asociadas al glosario
- `Catalogo validado`: expresion sugerida en parte del historial operativo del 2026-03-18 que no coincide con las rutas ni con los modulos presentes hoy en `main`.
- `Validado`: estado que aparece en el historial operativo y que debe leerse con cuidado cuando el propio changelog entra en contradiccion con el codigo vigente de la rama.
