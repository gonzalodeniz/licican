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

## Conclusion
El flujo base es correcto y la separacion de responsabilidades esta bien planteada. El principal problema no es de definicion de roles, sino de contrato operativo entre handoffs. La mejora prioritaria consiste en estandarizar estados, contenido minimo de entrega, sincronizacion con `main` y reglas de reentrada para reducir esperas, reprocesos y ambiguedad.
