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
