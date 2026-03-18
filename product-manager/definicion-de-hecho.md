# Definicion de Hecho de PodencoTI

## Objetivo
Establecer cuando un item funcional puede considerarse terminado para pasar a validacion de `qa-teams` y cuando puede cerrarse administrativamente por `product-manager`.

## Criterios minimos para pasar a QA
1. El item implementado esta vinculado a un issue de GitHub abierto y trazado a backlog, historia y caso de uso cuando aplique.
2. El alcance implementado coincide con los criterios de aceptacion acordados en el issue.
3. `developer-teams` ha dejado constancia en el issue de lo realizado, decisiones relevantes, limitaciones conocidas, verificacion tecnica ejecutada e impacto documental.
4. La funcionalidad es demostrable desde la perspectiva del usuario final prevista en la historia.
5. No quedan ambiguedades funcionales abiertas que bloqueen la validacion.
6. Se han actualizado los artefactos de producto si el alcance funcional ha cambiado.
7. `qa-teams` dispone en el issue de criterios verificables para revisar el comportamiento esperado.
8. El issue queda en estado operativo `listo para qa`.

## Criterios para considerarlo validado
1. `qa-teams` deja en la issue el resultado explicito `validado` o `no validado`.
2. Si el resultado es `validado`, el comportamiento observado cumple los criterios de aceptacion.
3. Si el resultado es `no validado`, el item vuelve a flujo de correccion sin cerrarse.

## Criterios para cierre administrativo por `product-manager`
1. Existe validacion explicita de `qa-teams`.
2. El issue no mantiene dependencias abiertas que impidan su cierre administrativo.
3. Si la rama o integracion final sigue pendiente, `product-manager` debe dejar constancia explicita del motivo por el que el issue continua abierto.
4. Solo tras esa comprobacion el item puede pasar a estado `cerrado`.

## Regla de cierre
- Un item no se considera definitivamente completado hasta que `qa-teams` indique explicitamente `validado`.
- Una implementacion tecnicamente correcta no equivale a "hecho" si no satisface el valor de negocio definido.
- Una tarea tampoco esta "hecha" por el mero hecho de haber sido fusionada si `qa-teams` no la ha validado.

## Evidencia minima esperada en el issue
- Referencia al item de backlog.
- Referencia a la historia de usuario y, si aplica, al caso de uso.
- Estado operativo actualizado.
- Resumen del comportamiento esperado.
- Criterios de aceptacion.
- Notas de dependencias, limitaciones o supuestos.
- Resultado de validacion de `qa-teams`.
