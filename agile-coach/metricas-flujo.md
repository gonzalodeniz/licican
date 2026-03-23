# Metricas ligeras de flujo

## Objetivo
Medir si el proceso entre equipos mejora en velocidad, claridad y estabilidad sin crear una carga operativa innecesaria.

## Metricas recomendadas

## 1. Tiempo hasta inicio de desarrollo
- Definicion: tiempo desde la creacion de la issue hasta el primer comentario o evidencia de `Estado operativo: en desarrollo`.
- Senal que aporta: detecta espera excesiva antes de empezar trabajo comprometido.

## 2. Tiempo de espera en QA
- Definicion: tiempo desde `Estado operativo: listo para qa` hasta el comentario de QA con `validado` o `no validado`.
- Senal que aporta: detecta cuello de botella en validacion.

## 3. Tasa de revalidacion
- Definicion: porcentaje de issues que pasan al menos una vez por `Estado operativo: no validado`.
- Senal que aporta: detecta calidad insuficiente del handoff o criterios poco claros antes de desarrollo.

## 4. Tiempo de cierre tras validacion
- Definicion: tiempo desde `Estado operativo: validado` hasta cierre de la issue por `product-manager`.
- Senal que aporta: detecta acumulacion de trabajo ya aceptado pero no cerrado.

## 4 bis. Tiempo de integracion tras validacion
- Definicion: tiempo desde `Estado operativo: validado` hasta que la rama tecnica queda fusionada en `main`.
- Senal que aporta: detecta limbo post-QA antes de merge, borrado de rama y activacion de documentacion dependiente.

## 5. Tasa de impacto documental declarado
- Definicion: porcentaje de entregas de desarrollo que marcan `Impacto documental: si`.
- Senal que aporta: ayuda a dimensionar la carga real de `doc-teams`.

## 6. Entregas que llegan a QA con conflicto contra `main`
- Definicion: numero o porcentaje de entregas revisadas por QA que presentan conflictos de integracion con `main`.
- Senal que aporta: detecta fallos de sincronizacion entre la rama tecnica y la rama de referencia del repositorio.

## 7. Issues devueltas por falta de contexto minimo
- Definicion: numero o porcentaje de issues que `developer-teams` no puede iniciar porque faltan campos obligatorios de contexto operativo.
- Senal que aporta: detecta si el cuello de botella real esta en refinamiento funcional antes de abrir trabajo tecnico.

## 8. Entregas rechazadas por handoff incompleto o sin integracion limpia
- Definicion: numero o porcentaje de revisiones que QA cierra en `no validado` porque falta la plantilla minima de entrega o porque la rama no integra limpia con `main`.
- Senal que aporta: detecta si el problema esta en la preparacion operativa del handoff antes de revisar funcionalidad.

## 9. Issues con estado visible desalineado
- Definicion: numero o porcentaje de issues abiertas cuyo cuerpo no refleja el mismo `Estado operativo:` que la ultima transicion operativa registrada en comentarios.
- Senal que aporta: detecta perdida de fiabilidad del backlog visible y deriva entre fuente resumida y flujo real.

## 10. Items de backlog desalineados con la issue activa
- Definicion: numero o porcentaje de items con issue activa cuyo `Estado` en `product-manager/product-backlog.md` no coincide con el ultimo `Estado operativo:` visible en la issue asociada.
- Senal que aporta: detecta cuando el documento de producto se queda como fotografia de planificacion y deja de representar el trabajo real que ya esta en curso o en revalidacion.

## 11. Documentos operativos sin referencia canónica explicita
- Definicion: numero de documentos de proceso consultados en una iteracion que reproducen una regla compartida sin enlazar o remitir a `agile-coach/acuerdos-operativos.md` o `changelog/README.md` como fuente primaria.
- Senal que aporta: detecta riesgo de deriva documental y mide si la referencia canónica de las reglas comunes se esta adoptando de forma consistente.

## Regla de uso
- Revisar estas metricas al cierre de cada iteracion relevante o cuando se acumulen varias issues cerradas.
- Si una metrica empeora de forma sostenida, revisar primero el handoff asociado antes de cambiar responsabilidades entre equipos.
