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

## Problema 14: el estado visible de la issue queda desfasado respecto al flujo real
### Evidencia
- La issue `#5` mantiene en el cuerpo `Estado operativo: nuevo` aunque ya tiene comentarios estructurados de `developer-teams` y `qa-teams` con `en desarrollo`, `listo para qa` y `no validado`.
- La consulta del backlog abierto en GitHub muestra el cuerpo de la issue, pero no expone de forma inmediata el ultimo comentario operativo.

### Impacto observado
- La lectura rapida del backlog puede inducir a error sobre que trabajo esta realmente nuevo, en curso o bloqueado por QA.
- `developer-teams` y `product-manager` necesitan abrir cada issue o leer comentarios para reconstruir el estado vigente.
- Se debilita la utilidad del campo `Estado operativo:` como referencia comun entre equipos si queda congelado en el alta inicial.

## Problema 15: `doc-teams` puede activarse antes de que la entrega validada exista realmente en `main`
### Evidencia
- `doc-teams` trabaja directamente sobre `main` y debe documentar comportamiento verificable del producto, pero el disparador operativo vigente solo miraba `Estado operativo: validado` e `Impacto documental: si`.
- El `changelog/2026-03-20.md` ya refleja la necesidad de distinguir entre trabajo validado en una rama tecnica y comportamiento realmente integrado en `main`, señal de que el flujo actual permite esa confusion.
- La issue `#5` aparece `validado` en GitHub mientras la rama tecnica `developer-teams/issue-5-pb-003-filtros-catalogo` sigue abierta y aun no se ha fusionado en `main`.

### Impacto observado
- `doc-teams` puede verse obligado a redactar sobre una capacidad aun no disponible en la rama de referencia del repositorio.
- La documentacion oficial corre el riesgo de adelantarse al merge real y generar una fuente de verdad incoherente con `main`.
- El tramo post-QA queda en un limbo operativo: la entrega esta aceptada, pero no queda suficientemente priorizada su integracion antes de activar trabajo dependiente.

## Problema 16: las plantillas de comentarios no fijan de forma visible el prefijo obligatorio `Rol:`
### Evidencia
- Las reglas globales ya exigen que cualquier comentario en una issue comience con `Rol: <nombre-del-rol>`.
- Sin embargo, varias plantillas y ejemplos operativos de arranque, handoff y revision siguen empezando directamente por `Rama:` o `Rama revisada:`, lo que deja al equipo la carga de recordar una regla externa antes de comentar.
- El historial de las issues `#3`, `#4` y `#5` muestra comentarios operativos tempranos sin linea inicial `Rol: ...`, señal de que la plantilla copiable seguia incompleta.

### Impacto observado
- La autoria operativa queda menos visible al leer rapido una issue.
- Se debilita la trazabilidad si mas adelante se quieren auditar handoffs por rol o automatizar metricas sobre comentarios.
- Los equipos pueden cumplir parcialmente la plantilla pero incumplir la norma global sin detectar la incoherencia.

## Problema 17: el cierre administrativo no hacia explicita la sincronizacion final a `Estado operativo: cerrado`
### Evidencia
- Las reglas ya exigian mantener sincronizado el campo `Estado operativo:` del cuerpo de la issue con el estado real, pero el cierre administrativo de `product-manager` no remarcaba de forma suficientemente directa que, al cerrar, el cuerpo debe quedar en `cerrado`.
- El `changelog/2026-03-21.md` ya recoge una correccion posterior en las issues `#3` y `#4` para alinear ese campo con su cierre real, prueba de que la expectativa existia pero no estaba anclada con suficiente fuerza en el ultimo tramo del flujo.

### Impacto observado
- Una issue puede quedar cerrada en GitHub mientras su cuerpo sigue mostrando `validado`, generando una segunda fuente de verdad sobre el estado final.
- El backlog historico pierde consistencia al revisar issues cerradas o al medir tiempos de cierre real.
- `product-manager` asume trabajo correctivo posterior en lugar de cerrar bien a la primera.

## Problema 18: el backlog funcional y la issue activa pueden mostrar estados distintos
### Evidencia
- `product-manager/product-backlog.md` mantiene `PB-009` como `nuevo`, mientras la issue #9 ya refleja `Estado operativo: no validado` tras la revision de `qa-teams`.
- La pagina de issues de GitHub muestra el estado operativo real de la issue, pero el backlog priorizado sigue exponiendo una fotografia de planificacion que no se ha actualizado con la reentrada operativa.

### Impacto observado
- `product-manager` puede interpretar una pieza en re-trabajo como si siguiera pendiente de arrancar.
- `developer-teams` y `qa-teams` ven el estado real en la issue, pero el backlog visible no ayuda a priorizar reentregas ni a detectar de un vistazo trabajo ya iniciado.
- Las metricas de flujo y la lectura del backlog mezclan planificacion y ejecucion si el estado no se sincroniza en cada transicion relevante.

## Problema 19: las reglas compartidas siguen duplicadas en varios documentos y facilitan la deriva
### Evidencia
- Las mismas reglas operativas aparecen repetidas en `AGENTS.md`, en los `AGENTS.md` de cada rol y en `agile-coach/acuerdos-operativos.md`, con el mismo contenido literal en varios puntos.
- `changelog/README.md` tuvo que nacer precisamente para sustituir una referencia historica desfasada que seguia apareciendo en varios documentos, lo que confirma el coste de mantener texto repetido.
- La guia principal del proyecto tambien resume parte del flujo, pero no explicita con suficiente claridad que los estados, plantillas y checkpoints compartidos deben tomar su redaccion canónica de un unico sitio.

### Impacto observado
- Cada ajuste de proceso exige editar varias fuentes a la vez y aumenta el riesgo de que una quede desalineada.
- Los equipos pueden leer una version distinta de la misma regla segun el documento que consulten primero.
- La trazabilidad de cambios de proceso se vuelve mas costosa porque no queda claro cual es la referencia primaria y cuales son solo copias de apoyo.

## Problema 20: la sincronizacion documental tras el merge no tiene un checkpoint operativo unico
### Evidencia
- `doc-teams/README.md` ya describe `PB-009` como integrado en `main`.
- `product-manager/product-backlog.md` y `product-manager/refinamiento-funcional.md` siguen reflejando que `PB-009` queda pendiente de integracion o cierre administrativo.
- La secuencia de trabajo obliga a cerrar o dejar constancia administrativa tras `validado`, pero no fija expresamente que el bloque de producto afectado deba reconciliarse antes de abrir la siguiente pieza funcional.

### Impacto observado
- La documentacion de producto puede quedar una iteracion atrasada respecto a la rama principal.
- `product-manager` y `doc-teams` leen fuentes distintas sobre el mismo estado operativo.
- Se dificulta decidir si el siguiente bloqueo es de cierre administrativo o de sincronizacion documental.

## Problema 21: una issue puede quedar `validado` sin evidencia visible de merge y borrado de rama
### Evidencia
- La issue `#6` esta en `Estado operativo: validado`, pero sigue abierta en GitHub y no existe un comentario operativo de cierre de integracion que deje visible si la fusion en `main` y el borrado de la rama ya se completaron.
- El listado de ramas remotas sigue mostrando `origin/developer-teams/issue-6-pb-004-alertas-tempranas`, lo que impide saber de un vistazo si el cierre tecnico ya se ejecuto o solo quedo pendiente de limpieza.
- El backlog y la issue no exponen por separado la validacion funcional y la evidencia de integracion final.

### Impacto observado
- `product-manager` puede cerrar o dejar abierta una issue sin una señal clara de que la entrega ya no depende de la rama tecnica.
- `developer-teams` y `agile-coach` no pueden distinguir con rapidez entre "validado pero pendiente de merge" y "validado e integrado pero pendiente de cierre administrativo".
- La revision del flujo post-QA se vuelve manual y propensa a olvidar la limpieza de rama.

## Problema 22: la documentacion de estado vigente puede quedar alineada con `main` mientras el backlog sigue desfasado
### Evidencia
- `product-manager/product-backlog.md` mantiene `PB-011` como `validado`, pero sigue marcando pendiente la integracion administrativa de la issue, mientras `doc-teams/README.md` ya describe esa entrega como parte de `main`.
- La discrepancia no afecta al funcionamiento tecnico de la aplicacion, pero si a la lectura de que documento refleja el estado vigente y cual se quedo como fotografia anterior.
- El propio flujo de coordinacion ya obliga a reconciliar backlog, refinamiento y roadmap tras cada merge, pero esa regla no nombraba de forma explicita la documentacion de estado mantenida por `doc-teams` como segundo detector de deriva.

### Impacto observado
- `product-manager` puede seguir leyendo el backlog como si fuera la fuente mas actual aunque la documentacion de estado de `main` ya refleje la entrega integrada.
- `doc-teams` puede quedar alineado con `main` mientras el backlog conserva un estado previo, generando una falsa impresion de que el problema de sincronizacion aun esta en documentacion.
- Se retrasa la deteccion de quien tiene que corregir primero y se mezcla el cierre administrativo con la lectura documental de la integracion.

## Conclusion
El flujo base es correcto y la separacion de responsabilidades esta bien planteada. El principal problema ya no esta en definir mas roles o estados, sino en asegurar que las plantillas realmente incorporan las reglas globales que deben cumplir y que el ultimo tramo del flujo deja un cierre visible sin contradicciones. La mejora prioritaria ahora consiste en hacer copiable el prefijo `Rol:` en todos los comentarios estructurados, en fijar de forma explicita que el cierre administrativo actualiza tambien el cuerpo de la issue a `Estado operativo: cerrado` y en sincronizar el estado del backlog con la issue activa para no mezclar planificacion con ejecucion, reduciendo incumplimientos por memoria, facilitando auditoria ligera y evitando estados historicos desalineados.
