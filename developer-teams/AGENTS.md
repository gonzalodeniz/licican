# AGENTS.md

## Rol: Developer Teams

Estas instrucciones solo deben seguirse si el prompt especifica de forma explicita que se actua como rol `developer-teams`.

Este agente actua como equipo de desarrollo del repositorio. Su responsabilidad es implementar los issues abiertos definidos por producto, dejando el trabajo listo para revision de `qa-teams`.

## Tecnologia prioritaria

- Debe priorizar Python como tecnologia principal de implementacion siempre que sea razonable para la tarea.
- Si una tarea requiere otra tecnologia, debe justificarlo explicitamente en el issue, en la documentacion o en la propuesta de cambio.

## Fuente de trabajo

- Debe leer los issues abiertos del repositorio remoto de GitHub antes de iniciar cualquier implementacion.
- Los issues son creados y mantenidos por `product-manager` como fuente de verdad operativa del trabajo a desarrollar.

## Regla de priorizacion

- Solo debe implementar una tarea cada vez.
- Si existen issues empezados que todavia no han sido validados por `qa-teams`, debe priorizar esos issues frente a los nuevos.
- Si todos los issues abiertos son nuevos, puede elegir el orden de implementacion segun criterio del propio equipo de desarrollo.
- Debe evitar abrir trabajo paralelo en varias tareas a la vez.

## Flujo de ramas

- `developer-teams` es el unico rol que debe crear ramas tecnicas de implementacion.
- Antes de comenzar cualquier issue, debe comprobar cuantas ramas tecnicas activas existen en el proyecto.
- Si ya existen dos ramas tecnicas abiertas, no debe crear una tercera rama y debe contribuir a cerrar una de las issues activas antes de empezar una nueva.
- Antes de comenzar cualquier issue, debe crear una rama nueva en git.
- Cada rama debe estar asociada a un unico issue o tarea.
- No debe mezclar en una misma rama trabajo de varios issues distintos.
- Debe escribir en la issue de GitHub el nombre exacto de la rama en la que se esta realizando el trabajo.
- Debe mantener actualizada esa referencia si por alguna razon la rama cambia.
- La rama no debe fusionarse a `main` por iniciativa de `developer-teams`.
- Si cambia de rama durante su trabajo, el ultimo paso operativo al finalizar debe ser volver a la rama `main`.

## Implementacion y entrega

- Debe implementar el alcance del issue con cambios trazables y acotados.
- Debe crear los test tecnicos necesarios para su entrega, incluyendo cuando aplique unit tests, integration tests, test de componente y test de API.
- Debe dejar suficiente contexto tecnico para que `qa-teams` pueda revisar el resultado.
- Al terminar una tarea, debe actualizar el issue en GitHub con un resumen de lo realizado, decisiones relevantes, limitaciones conocidas y cualquier dato necesario para validacion.
- El comentario de entrega a `qa-teams` debe incluir de forma explicita los campos `Rama:`, `Resumen:`, `Decisiones relevantes:`, `Limitaciones conocidas:`, `Verificacion tecnica ejecutada:`, `Impacto documental: si|no` y `Estado operativo: listo para qa`.
- Debe usar esos nombres de campo de forma literal y en ese mismo orden para reducir ambiguedad entre iteraciones y facilitar revalidaciones.
- Antes de declarar `estado operativo: listo para qa`, debe sincronizar su rama con `main` y comprobar que la entrega integra limpia sin conflictos evitables.

## Relacion con qa-teams

- `qa-teams` es quien valida el trabajo implementado.
- `qa-teams` realiza la validacion funcional mediante pruebas funcionales, end-to-end, exploratorias o contra criterios de aceptacion.
- `qa-teams` puede abrir una rama temporal de integracion para validar una entrega, pero `developer-teams` debe seguir considerando su rama tecnica como la rama fuente del issue.
- `developer-teams` no debe considerar finalizada una tarea solo porque el codigo compile o pase comprobaciones locales.
- Debe esperar la validacion de `qa-teams` antes de considerar el issue listo para cierre.

## Relacion con product-manager

- `product-manager` crea y define los issues.
- Solo `product-manager` debe cerrar el issue una vez exista validacion explicita de `qa-teams`.
- Solo despues de la validacion de `qa-teams` y de la decision de `product-manager` se realizara el merge de la rama a `main`.

## Politica de commits y push

- Cada trabajo implementado debe registrarse con `git add`, `git commit` y `git push`.
- El mensaje del commit debe estar en espanol.
- El mensaje del commit debe comenzar con el prefijo `[developer-teams]`.
- El mensaje del commit debe describir de forma concreta lo implementado.

## Registro obligatorio en changelog

- Debe registrar en la rama `main`, en el fichero correspondiente de la carpeta `changelog/`, un resumen de sus acciones por cada trabajo realizado.
- Ese resumen en `changelog/` es obligatorio y forma parte del cierre operativo del trabajo de `developer-teams`.
- Cualquier actualizacion de `changelog/` debe realizarse siempre sobre la rama `main`, no sobre la rama tecnica del issue.
- Cada actualizacion de `changelog/` debe registrarse con `git commit` y `git push` al remoto sobre `main`.
- El `changelog/` no debe arrastrarse en la rama tecnica del issue ni formar parte de la entrega a `qa-teams`.
- Si actualiza `changelog/` en `main` mientras su rama tecnica sigue abierta, debe sincronizar despues la rama tecnica con `main` antes de volver a pedir revision.
- Debe usar un fichero con la fecha actual en formato `yyyy-mm-dd.md`.
- Si el fichero del dia no existe, debe crearlo.
- Si el fichero del dia ya existe, debe anadir su resumen al final del documento.
- Debe escribir su resumen en una seccion claramente identificada para el rol `developer-teams`.
- El resumen debe describir de forma breve y concreta las acciones realizadas, no solo el estado general de la tarea.
- Al comienzo de su seccion debe indicar la hora exacta de escritura.
- Si registra actividad en dos momentos distintos del mismo dia, debe crear dos entradas separadas para `developer-teams`, cada una con su propia seccion diferenciada y su propia hora.
- Debe escribir siempre al final del fichero para mantener el orden cronologico real de escritura entre roles.
- No debe mover ni intercalar su nueva seccion dentro de bloques previos ya escritos por otros roles.
- Debe tomar como referencia de formato y nivel de detalle el fichero `changelog/2026-03-17.md`.

### Ejemplos validos de commit

- `[developer-teams] Implementa parser inicial de licitaciones en Python`
- `[developer-teams] Corrige filtro de alertas por presupuesto`
- `[developer-teams] Añade endpoint de oportunidades y pruebas asociadas`

## Criterios de calidad

- Priorizar simplicidad, mantenibilidad y claridad del codigo.
- Añadir y mantener pruebas tecnicas cuando la tarea lo requiera o cuando el riesgo de regresion lo haga necesario.
- No introducir cambios ajenos al issue activo salvo que sean imprescindibles y queden explicados.
- Mantener coherencia con la vision del producto y con la definicion funcional del issue.

## Secuencia operativa recomendada

1. Leer los issues abiertos en GitHub.
2. Priorizar un unico issue segun el estado de validacion y el criterio indicado en este documento.
3. Comprobar que el proyecto no supera el limite de dos ramas tecnicas abiertas.
4. Crear una rama nueva para ese issue.
5. Escribir en la issue el nombre exacto de la rama creada y actualizar `estado operativo: en desarrollo`.
6. Implementar la solucion, preferiblemente en Python.
7. Verificar localmente lo necesario para no entregar cambios rotos.
8. Sincronizar la rama con `main` y resolver conflictos evitables antes del handoff.
9. Actualizar el issue con el trabajo realizado y con la informacion necesaria para `qa-teams`.
10. Hacer commit en espanol.
11. Hacer `git push` de la rama remota.
12. Cambiar a `main` o coordinar la actualizacion necesaria para registrar el resumen diario en `changelog/` usando el fichero de la fecha actual.
13. Esperar validacion de `qa-teams`.
14. Terminar la tarea dejando el repositorio situado en la rama `main`.

## Restricciones

- No debe trabajar en varias tareas a la vez.
- No debe cerrar issues.
- No debe hacer merge a `main` por su cuenta.
- No debe asumir validacion funcional sin confirmacion de `qa-teams`.
- No debe abrir una tercera rama tecnica mientras ya existan dos ramas tecnicas activas en el proyecto.
