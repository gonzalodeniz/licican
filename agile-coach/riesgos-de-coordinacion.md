# Riesgos actuales de coordinacion

## Objetivo
Registrar los riesgos de coordinacion que siguen activos tras los ajustes de proceso ya aplicados y dejar visible que senales deben vigilar los equipos.

## Riesgo 1: issues `validado` que permanecen abiertas sin cierre administrativo claro
- Senal observable: issue abierta con validacion de QA pero sin comentario estructurado de bloqueo, responsable siguiente y paso operativo.
- Impacto: distorsiona la lectura del backlog abierto y oculta si el atasco es real o solo administrativo.
- Mitigacion acordada: comentario obligatorio de `product-manager` con `Bloqueo actual:`, `Siguiente responsable:`, `Siguiente paso operativo:` y `Estado de integracion:`.

## Riesgo 2: deriva en el formato de handoff entre iteraciones
- Senal observable: comentarios de entrega o revision con el estado operativo incrustado en texto libre o con claves distintas entre issues.
- Impacto: aumenta el tiempo de lectura, complica revalidaciones y reduce la calidad de metricas ligeras.
- Mitigacion acordada: plantillas literales minimas para `developer-teams`, `qa-teams` y seguimiento administrativo de `product-manager`.

## Riesgo 3: reaparicion de conflictos por `changelog/` en ramas tecnicas largas
- Senal observable: una rama tecnica permanece abierta mientras `main` sigue recibiendo entradas nuevas en `changelog/`.
- Impacto: QA vuelve a asumir conflictos administrativos antes de validar funcionalmente.
- Mitigacion acordada: resincronizar la rama con `main` antes de cada nuevo handoff a QA.

## Riesgo 4: activacion tardia de `doc-teams`
- Senal observable: entrega con `Impacto documental: si` y `Estado operativo: validado` sin movimiento posterior en documentacion.
- Impacto: el producto validado queda operativamente desalineado de su documentacion oficial.
- Mitigacion acordada: usar `Impacto documental: si` como disparador y revisar esta cola al cierre de cada entrega validada.

## Riesgo 5: arranque de desarrollo sobre issues aun no operables
- Senal observable: la issue se mueve a `en desarrollo` sin incluir `Backlog:`, `Historia de usuario:`, `Caso de uso:`, `Criterios de aceptacion:` o `Dependencias:`.
- Impacto: se trasladan ambiguedades funcionales al trabajo tecnico y se desperdicia capacidad de desarrollo en aclaraciones tardias.
- Mitigacion acordada: paquete minimo obligatorio de issue antes de abrir rama y bloqueo explicito de inicio si falta ese contexto.

## Riesgo 6: deriva en el formato del `changelog/` por seguir ejemplos historicos
- Senal observable: nuevas entradas sin hora exacta o con estructura copiada de ficheros anteriores a la regla vigente.
- Impacto: baja la calidad de la trazabilidad diaria y aumenta la interpretacion manual entre roles.
- Mitigacion acordada: usar `changelog/README.md` como referencia vigente de formato y tratar los ficheros historicos solo como contexto del nivel de detalle.

## Riesgo 7: arranque ambiguo de issues en desarrollo
- Senal observable: la issue pasa a trabajo activo sin comentario minimo con `Rama:` y `Estado operativo: en desarrollo`.
- Impacto: se pierde visibilidad rapida sobre que rama esta activa y se debilita el control del limite de ramas tecnicas.
- Mitigacion acordada: comentario de arranque obligatorio y literal al tomar la issue.

## Riesgo 8: QA consume tiempo en entregas sin gate previo superado
- Senal observable: la revision funcional empieza aunque falte la plantilla minima de handoff o existan conflictos evitables con `main`.
- Impacto: QA invierte capacidad en reconstruir contexto o diagnosticar integracion antes de validar comportamiento.
- Mitigacion acordada: comprobacion previa obligatoria y cierre con `Estado operativo: no validado` cuando el handoff no sea operable.

## Riesgo 9: backlog visible con estados operativos desfasados
- Senal observable: el cuerpo de la issue sigue mostrando `Estado operativo: nuevo` aunque existan comentarios posteriores con `en desarrollo`, `listo para qa`, `no validado` o `validado`.
- Impacto: la priorizacion y la lectura rapida del backlog se apoyan en un estado engañoso o incompleto.
- Mitigacion acordada: actualizar el `Estado operativo:` del cuerpo de la issue en cada transicion operativa relevante.

## Riesgo 10: documentacion adelantada respecto a la integracion real
- Senal observable: una issue queda `validado` con `Impacto documental: si`, pero la rama tecnica sigue abierta o la capacidad aun no existe en `main`.
- Impacto: la documentacion oficial puede describir un comportamiento todavia no integrado y crear incoherencia entre manuales, backlog visible y producto real.
- Mitigacion acordada: activar a `doc-teams` solo cuando la entrega validada ya este fusionada en `main` y reforzar la prioridad de merge tras QA.

## Riesgo 11: comentarios estructurados sin `Rol:` al inicio
- Senal observable: un comentario de arranque, handoff o validacion empieza directamente por `Rama:` o `Rama revisada:`.
- Impacto: baja la visibilidad de autoria, se incumple la norma global del repositorio y se complica la auditoria ligera por rol.
- Mitigacion acordada: incluir `Rol: <nombre-del-rol>` como primera linea de todas las plantillas operativas de issue.

## Riesgo 12: issue cerrada con cuerpo todavia en `validado`
- Senal observable: la issue aparece cerrada en GitHub pero el cuerpo sigue mostrando `Estado operativo: validado`.
- Impacto: el historico mezcla dos estados finales distintos y degrada la fiabilidad del backlog ya cerrado.
- Mitigacion acordada: exigir que `product-manager` actualice el cuerpo a `Estado operativo: cerrado` en el mismo cierre administrativo.

## Riesgo 13: backlog visible desalineado respecto a la issue activa
- Senal observable: el item del backlog sigue en `nuevo` mientras la issue asociada ya figura como `en desarrollo`, `listo para qa`, `no validado`, `validado` o `cerrado`.
- Impacto: la lectura rapida del backlog oculta re-trabajo, dificulta priorizar reentregas y puede hacer que `product-manager` interprete mal la carga real del equipo.
- Mitigacion acordada: sincronizar el campo `Estado` del backlog con la transicion operativa de la issue en la misma actualizacion documental.

## Riesgo 14: deriva por duplicacion de reglas compartidas en varios documentos
- Senal observable: una misma regla de handoff, cierre o estado operativo aparece redactada en varios documentos sin indicar cual es la referencia primaria.
- Impacto: cada cambio de proceso debe replicarse manualmente, aumenta la probabilidad de que una copia quede desactualizada y se multiplican las interpretaciones de una misma norma.
- Mitigacion acordada: tomar `agile-coach/acuerdos-operativos.md` como referencia canónica para las reglas compartidas y usar `changelog/README.md` como referencia canónica del formato de registro diario.

## Riesgo 15: el backlog y el refinamiento de producto se quedan atras tras un merge validado
- Senal observable: una entrega ya integrada en `main` convive con documentos de producto que siguen describiendo el estado previo.
- Impacto: `product-manager` puede planificar la siguiente iteracion sobre una fotografia desfasada y `doc-teams` puede mantener una version distinta del producto.
- Mitigacion acordada: reconciliar backlog, refinamiento y roadmap afectados antes de abrir la siguiente issue funcional y, si la issue sigue abierta, dejar visible si la documentacion ya quedo sincronizada.

## Riesgo 16: una issue validada queda abierta sin evidencia de cierre de integracion
- Senal observable: la issue sigue abierta en `validado` sin comentario de cierre de integracion de `developer-teams` o sin comentario administrativo de `product-manager` que explique la integracion pendiente.
- Impacto: el equipo no distingue de un vistazo entre validacion funcional completada y cierre tecnico-administrativo aun pendiente.
- Mitigacion acordada: exigir comentario de cierre con `Merge en main:` y `Rama eliminada:` antes del cierre administrativo definitivo.

## Riesgo 17: tomar el `changelog/` como evidencia suficiente de integracion
- Senal observable: el `changelog/` describe una entrega como validada o sincronizada, pero la rama `main` o los comentarios de cierre no muestran aun la integracion completa.
- Impacto: `product-manager` o `doc-teams` pueden documentar como vigente una capacidad que todavia no esta realmente integrada, o dar por cerrada una issue sin evidencia tecnica suficiente.
- Mitigacion acordada: tratar `main` y los comentarios de cierre como evidencia vigente de integracion; el `changelog/` solo tiene valor historico y nunca debe sustituir esa comprobacion.

## Riesgo 18: backlog desfasado frente a la documentacion de estado vigente
- Senal observable: `doc-teams/README.md` o la documentacion de estado vigente ya describen una entrega como parte de `main`, pero `product-manager/product-backlog.md` sigue marcandola con un estado anterior.
- Impacto: el backlog pierde fiabilidad como fotografia operativa y puede hacer que la siguiente planificacion se base en una version atrasada del estado real del producto.
- Mitigacion acordada: en el checkpoint post-merge, `product-manager` debe contrastar backlog y documentacion de estado vigente y corregir primero el artefacto que siga desfasado antes de abrir nueva planificacion funcional.

## Riesgo 19: backlog que rebaja o no actualiza una issue ya validada
- Senal observable: la issue `#12` figura en `Estado operativo: validado` en GitHub, pero `product-manager/product-backlog.md` sigue mostrando `PB-012` como `no validado`.
- Impacto: la entrega aceptada puede seguir pareciendo bloqueada, se retrasa el cierre administrativo y se confunde a quien consulta el backlog para decidir la siguiente accion.
- Mitigacion acordada: cuando `qa-teams` cambie el estado de una issue a `validado`, `product-manager` debe sincronizar el backlog en el mismo ciclo operativo y no dejarlo en un estado anterior por inercia; si la issue sigue abierta, el backlog debe permanecer en `validado` hasta el cierre real.

## Riesgo 20: reaparicion de duplicidad en reglas compartidas por copiar en lugar de remitir
- Senal observable: una regla comun cambia en la guia canónica, pero una o varias copias derivadas siguen repitiendo el bloque completo en vez de limitarse a una remision breve.
- Impacto: se multiplican las superficies que hay que revisar, aumenta la probabilidad de deriva y se pierde parte del beneficio de tener una fuente de verdad unica.
- Mitigacion acordada: mantener las reglas compartidas solo en `agile-coach/acuerdos-operativos.md` y reducir los `AGENTS.md` de rol a remisiones cortas mas la plantilla literal minima necesaria.
