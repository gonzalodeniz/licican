# Acuerdos operativos entre equipos

## Objetivo
Reducir ambiguedades en los handoffs entre `product-manager`, `developer-teams`, `qa-teams` y `doc-teams` sin alterar la separacion de responsabilidades ya definida en el repositorio.

## Estados operativos comunes
Todos los equipos deben reutilizar estos estados operativos en sus comentarios y transiciones de trabajo:

- `nuevo`: issue creada y lista para ser tomada.
- `en desarrollo`: `developer-teams` ha tomado la issue y trabaja sobre una rama dedicada.
- `listo para qa`: desarrollo ha terminado una entrega revisable y ha dejado evidencia suficiente.
- `no validado`: QA ha encontrado defectos o incumplimientos que obligan a nueva entrega.
- `validado`: QA confirma que la entrega cumple el alcance revisado.
- `cerrado`: `product-manager` cierra la issue tras validacion y promueve el siguiente paso de integracion.

## Handoff minimo de `developer-teams` a `qa-teams`
El comentario final de entrega de `developer-teams` debe incluir como minimo:
- `Rama:`
- `Resumen:`
- `Decisiones relevantes:`
- `Limitaciones conocidas:`
- `Verificacion tecnica ejecutada:`
- `Impacto documental: si|no`
- `Estado operativo: listo para qa`

## Handoff minimo de `qa-teams`
El comentario de revision de `qa-teams` debe incluir como minimo:
- `Rama revisada:`
- `Pruebas realizadas:`
- `Resultados observados:`
- `Defectos bloqueantes:`
- `Observaciones:`
- `Riesgos:`
- `Estado operativo: validado|no validado`

## Regla de revalidacion
Si QA deja `Estado operativo: no validado`:
1. La issue sigue abierta.
2. `developer-teams` mantiene la misma rama mientras el alcance siga siendo el mismo.
3. `developer-teams` publica un nuevo comentario de entrega con las correcciones y una nueva evidencia.
4. `qa-teams` vuelve a revisar esa misma issue.

Si el alcance cambia de forma material, `product-manager` debe decidir si corresponde una nueva issue.

## Disparador operativo de `doc-teams`
`doc-teams` debe priorizar una iteracion cuando concurran estas condiciones:
1. Existe `Estado operativo: validado` en la issue.
2. La entrega de desarrollo indica `Impacto documental: si`.

Si el impacto documental es `no`, la documentacion puede esperar salvo instruccion explicita.

## Checkpoint de cierre de `product-manager`
Tras `Estado operativo: validado`, `product-manager` debe:
1. verificar que la trazabilidad funcional sigue siendo correcta
2. cerrar la issue o dejar constancia explicita del motivo por el que sigue abierta
3. promover el merge segun el flujo del repositorio

## Regla de simplicidad
Estos acuerdos existen para reducir esperas y reprocesos. No deben usarse para introducir estados adicionales ni ceremonias no justificadas.
