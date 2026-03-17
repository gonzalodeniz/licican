# Definicion de Hecho de PodencoTI

## Objetivo
Establecer cuando un item funcional puede considerarse terminado para pasar a validacion de `qa-teams`.

## Criterios minimos
1. El item implementado esta vinculado a un issue de GitHub abierto y trazado a backlog, historia o caso de uso.
2. El alcance implementado coincide con los criterios de aceptacion acordados en el issue.
3. `developer-teams` ha dejado constancia en el issue de lo realizado, limitaciones conocidas y evidencia tecnica relevante.
4. La funcionalidad es demostrable desde la perspectiva del usuario final prevista en la historia.
5. No quedan ambiguedades funcionales abiertas que bloqueen la validacion.
6. Se han actualizado los artefactos de producto si el alcance funcional ha cambiado.
7. `qa-teams` dispone en el issue de criterios verificables para revisar el comportamiento esperado.

## Regla de cierre
- Un item no se considera definitivamente completado hasta que `qa-teams` indique explicitamente `validado`.
- Si `qa-teams` indica `no validado`, el item vuelve a estado pendiente de correccion o revalidacion.
- `product-manager` no cerrara issues funcionales o de implementacion sin esa validacion explicita.

## Evidencia minima esperada en el issue
- Referencia al item de backlog.
- Referencia a la historia de usuario y, si aplica, al caso de uso.
- Resumen del comportamiento esperado.
- Criterios de aceptacion.
- Notas de dependencias, limitaciones o supuestos.

## Exclusiones
- Una implementacion tecnicamente correcta no equivale a "hecho" si no satisface el valor de negocio definido.
- Una tarea tampoco esta "hecha" por el mero hecho de haber sido fusionada si `qa-teams` no la ha validado.
