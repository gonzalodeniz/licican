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
