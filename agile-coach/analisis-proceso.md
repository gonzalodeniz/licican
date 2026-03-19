# Analisis del proceso actual

## Alcance del analisis
Este analisis revisa la coordinacion definida entre `product-manager`, `developer-teams`, `qa-teams`, `doc-teams` y `agile-coach` a partir de los `AGENTS.md`, la documentacion funcional y el uso actual de issues del repositorio.

## Flujo actual observado
1. `product-manager` mantiene backlog, historias, casos de uso e issues ejecutables.
2. `developer-teams` toma un unico issue, crea una rama, implementa y deja contexto para QA en la issue.
3. `qa-teams` revisa la rama y deja `validado` o `no validado`.
4. `product-manager` cierra la issue y promueve merge tras validacion.
5. `doc-teams` actualiza documentacion cuando la funcionalidad esta estable.

## Problema 1: falta un estado operativo comun entre equipos
### Evidencia
- Los roles describen responsabilidades, pero no comparten un vocabulario operativo minimo para distinguir `nuevo`, `en desarrollo`, `listo para QA`, `no validado`, `validado` y `cerrado`.
- En las issues abiertas aparece el texto "Pendiente de validacion por `qa-teams`", pero no una regla comun que todos deban seguir o reutilizar.

### Impacto observado
- Aumenta la necesidad de reinterpretar comentarios para saber quien debe actuar.
- Se debilita la priorizacion de `developer-teams` cuando existen issues empezados pero no cerrados.
- Se dificulta automatizar o auditar el flujo mas adelante.

## Problema 2: el handoff a QA no tiene un paquete minimo obligatorio
### Evidencia
- `developer-teams` debe dejar contexto tecnico en la issue, pero no existe una plantilla minima transversal.
- `qa-teams` debe documentar pruebas y resultado, pero no se fija un conjunto minimo comun de datos para cada revision.

### Impacto observado
- La calidad del handoff depende del criterio individual de cada iteracion.
- QA puede perder tiempo reconstruyendo comandos, alcance real, limitaciones o evidencias.
- El feedback no es igual de reutilizable para revalidaciones o retrospectivas.

## Problema 3: no esta definido el circuito de reentrada tras `no validado`
### Evidencia
- El repositorio obliga a terminar con `validado` o `no validado`, pero no define explicitamente como vuelve la tarea a desarrollo ni que debe actualizarse para reabrir la revision.

### Impacto observado
- Puede haber dudas sobre si se mantiene la misma rama, la misma issue o una nueva.
- Puede repetirse contexto ya conocido o perderse trazabilidad entre entregas sucesivas del mismo issue.

## Problema 4: `doc-teams` no tiene un disparador operativo claro
### Evidencia
- `doc-teams` debe documentar la realidad implementada, pero no existe una regla comun para indicar si una entrega tiene impacto documental y cuando debe entrar este equipo.
- El README recomienda que `doc-teams` actue cuando la funcionalidad este estable o validada, pero no lo convierte en criterio operativo reusable por el resto de roles.

### Impacto observado
- La documentacion puede llegar tarde o adelantarse a cambios aun no validados.
- El equipo de documentacion depende de interpretar el contexto del issue en lugar de recibir una señal explicita.

## Problema 5: falta una expectativa de cierre tras `validado`
### Evidencia
- El flujo indica que `product-manager` cierra y promueve merge despues de QA.
- Existe al menos una issue ya `validado` que sigue abierta, lo que muestra que la regla existe pero no tiene un checkpoint operativo suficientemente visible.

### Impacto observado
- Se acumulan issues que tecnicamente ya han pasado QA pero siguen aparentando trabajo en curso.
- Se distorsiona la lectura del backlog y la priorizacion de nuevas iteraciones.

## Problema 6: el uso del `changelog/` genera conflictos evitables con las ramas tecnicas
### Evidencia
- El repositorio obliga a registrar actividad diaria en `changelog/` sobre `main`, pero no fijaba una regla explicita para resincronizar despues las ramas tecnicas abiertas.
- En la issue `#2`, `qa-teams` documento el 2026-03-18 un conflicto de integracion en `changelog/2026-03-18.md` al intentar validar la rama `feat/pb-006-clasificacion-ti-auditable`.

### Impacto observado
- QA recibe entregas que funcionalmente ya estan en revision pero operativamente no integran limpias con `main`.
- Se invierte tiempo de validacion en resolver o diagnosticar conflictos administrativos en lugar de revisar comportamiento.
- El propio `changelog/` pasa de ser un mecanismo de trazabilidad a convertirse en una fuente de friccion entre equipos.

## Problema 7: falta un checkpoint explicito de sincronizacion antes del handoff a QA
### Evidencia
- `developer-teams` debe dejar contexto para QA, pero no existia una regla comun que obligara a comprobar integracion limpia con `main` antes de declarar `listo para qa`.
- La revision de `qa-teams` en la issue `#2` detecto a la vez una entrega funcional incompleta y una rama desalineada con `main`, mezclando dos tipos de problemas en el mismo handoff.

### Impacto observado
- QA asume parte del coste de descubrir si el problema esta en el comportamiento entregado o en la sincronizacion de ramas.
- Aumenta el riesgo de ciclos de `no validado` por causas evitables antes de empezar la validacion funcional real.

## Problema 8: la issue puede quedar `validado` y abierta con contexto administrativo insuficiente
### Evidencia
- La issue `#1` permanece abierta tras `Estado operativo: validado`.
- El comentario administrativo explica por que sigue abierta, pero no deja de forma estructurada el siguiente responsable, el siguiente paso operativo ni el estado real de integracion.

### Impacto observado
- Una issue aceptada por QA sigue pareciendo trabajo en curso si no queda claro si falta merge, cierre administrativo o borrado de rama.
- `developer-teams` y `agile-coach` pierden visibilidad sobre si el bloqueo es real o solo una tarea administrativa pendiente.
- El backlog abierto mezcla trabajo no validado con trabajo ya aceptado pero no cerrado.

## Problema 9: las plantillas de handoff siguen siendo interpretables en lugar de literales
### Evidencia
- Los comentarios historicos de desarrollo y QA en las issues `#1` y `#2` contienen la informacion esencial, pero no siempre reutilizan las mismas claves ni el mismo orden.
- Esto obliga a re-interpretar comentarios para localizar el estado operativo, la rama revisada o el contexto minimo de entrega.

### Impacto observado
- La trazabilidad entre iteraciones del mismo issue depende de lectura manual.
- Se dificulta revisar metricas de flujo o auditar el cumplimiento de handoffs minimos.
- La revalidacion es mas costosa porque la informacion no queda siempre en un formato comparable.

## Problema 10: una issue puede parecer lista para desarrollo sin tener contexto minimo estable
### Evidencia
- `product-manager` debe crear issues ejecutables, pero hasta ahora no existia un paquete literal minimo comun que fijara backlog origen, historia, caso de uso, criterios de aceptacion y dependencias.
- `developer-teams` debe leer los issues abiertos antes de empezar, pero no tenia una regla explicita para frenar el inicio cuando faltara ese contexto minimo.

### Impacto observado
- Desarrollo puede invertir tiempo en reinterpretar artefactos de producto antes de abrir una rama.
- Aumenta el riesgo de empezar trabajo sobre una issue aun insuficientemente refinada.
- QA recibe mas tarde la ambiguedad inicial, porque el hueco de definicion se descubre ya dentro del ciclo tecnico.

## Problema 11: la referencia historica de `changelog/` ya no coincide con la norma vigente
### Evidencia
- Los roles seguian usando `changelog/2026-03-17.md` como referencia de formato.
- Ese fichero no incluye la hora obligatoria por entrada que ahora exigen las propias reglas del repositorio y de cada rol.

### Impacto observado
- La instruccion mezcla una referencia historica util con un formato ya desfasado.
- Cada rol debe decidir por interpretacion propia si prioriza la norma actual o el ejemplo antiguo.
- La calidad del registro diario queda expuesta a deriva incluso cuando la regla de fondo ya esta clara.

## Problema 12: el inicio de una issue no deja una huella operativa suficientemente estable
### Evidencia
- El flujo exige que `developer-teams` indique la rama y deje constancia de `estado operativo: en desarrollo`, pero no fijaba una plantilla literal minima para ese arranque.
- Sin una forma comun, la informacion puede quedar repartida entre comentarios libres y actualizaciones parciales de la issue.

### Impacto observado
- Cuesta localizar rapidamente que rama esta activa en cada issue.
- Se debilita la comprobacion del limite de dos ramas tecnicas abiertas.
- La metrica de tiempo hasta inicio de desarrollo depende de interpretacion manual en lugar de un comentario comparable.

## Problema 13: QA no tenia una puerta de entrada explicita para rechazar handoffs incompletos
### Evidencia
- `developer-teams` debe usar una plantilla minima para entregar a QA, pero `qa-teams` no tenia una regla igual de explicita para detener la revision cuando faltaba ese paquete o la rama no integraba limpia con `main`.
- La norma permitia registrar el riesgo, pero no convertia ese defecto de handoff en un criterio operativo claro de `no validado`.

### Impacto observado
- QA puede perder tiempo reconstruyendo contexto antes de empezar la validacion funcional.
- Se mezclan defectos funcionales con fallos de preparacion de entrega en la misma revision.
- La disciplina del handoff depende de buena voluntad y no de un control verificable entre equipos.

## Conclusion
El flujo base es correcto y la separacion de responsabilidades esta bien planteada. El principal problema no es de definicion de roles, sino de contrato operativo entre handoffs, de preparacion minima antes de iniciar desarrollo, de control de entrada en QA y de cierre administrativo tras validacion. La mejora prioritaria consiste en estandarizar estados, arranque de issue, contenido minimo de issue, contenido minimo de entrega, sincronizacion con `main`, puerta previa de QA, cierre post-validacion y una referencia vigente de `changelog/` para reducir esperas, reprocesos y ambiguedad.
