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

## Paquete minimo para iniciar una issue
Antes de que `developer-teams` abra una rama, la issue debe incluir como minimo y de forma literal:
- `Backlog:`
- `Historia de usuario:`
- `Caso de uso:`
- `Criterios de aceptacion:`
- `Dependencias:`
- `Estado operativo: nuevo`

Si falta alguno de estos campos, la issue no debe considerarse lista para desarrollo y `product-manager` debe completarla antes del inicio tecnico.

## Arranque minimo de `developer-teams`
Cuando `developer-teams` tome una issue debe publicar un comentario de arranque con esta plantilla minima:

```text
Rama: <nombre-rama>
Estado operativo: en desarrollo
```

Este comentario fija que rama esta activa, permite auditar el limite de ramas abiertas y evita que el estado `en desarrollo` quede escondido en texto libre.

## Handoff minimo de `developer-teams` a `qa-teams`
El comentario final de entrega de `developer-teams` debe incluir como minimo:
- `Rama:`
- `Resumen:`
- `Decisiones relevantes:`
- `Limitaciones conocidas:`
- `Verificacion tecnica ejecutada:`
- `Impacto documental: si|no`
- `Estado operativo: listo para qa`

Plantilla minima recomendada:

```text
Rama: <nombre-rama>
Resumen:
- ...
Decisiones relevantes:
- ...
Limitaciones conocidas:
- ...
Verificacion tecnica ejecutada:
- <comando o evidencia>
Impacto documental: si|no
Estado operativo: listo para qa
```

## Handoff minimo de `qa-teams`
El comentario de revision de `qa-teams` debe incluir como minimo:
- `Rama revisada:`
- `Pruebas realizadas:`
- `Resultados observados:`
- `Defectos bloqueantes:`
- `Observaciones:`
- `Riesgos:`
- `Estado operativo: validado|no validado`

Plantilla minima recomendada:

```text
Rama revisada: <nombre-rama>
Pruebas realizadas:
- ...
Resultados observados:
- ...
Defectos bloqueantes:
- ...
Observaciones:
- ...
Riesgos:
- ...
Estado operativo: validado|no validado
```

## Gate previo de `qa-teams`
Antes de ejecutar la validacion funcional, `qa-teams` debe comprobar dos condiciones:
1. La entrega de `developer-teams` usa la plantilla minima de handoff.
2. La rama revisada integra limpia con `main`.

Si alguna de estas condiciones falla, `qa-teams` debe registrar el problema como defecto bloqueante u operativo y cerrar la revision con `Estado operativo: no validado` sin dar por buena la entrega.

## Regla de revalidacion
Si QA deja `Estado operativo: no validado`:
1. La issue sigue abierta.
2. `developer-teams` mantiene la misma rama mientras el alcance siga siendo el mismo.
3. `developer-teams` publica un nuevo comentario de entrega con las correcciones y una nueva evidencia.
4. `qa-teams` vuelve a revisar esa misma issue.

Si el alcance cambia de forma material, `product-manager` debe decidir si corresponde una nueva issue.

## Regla de sincronizacion entre ramas y `main`
- `changelog/` se actualiza solo en `main` y no forma parte de la entrega tecnica del issue.
- Si `developer-teams` o `qa-teams` registran actividad en `changelog/` mientras mantienen una rama abierta, deben sincronizar despues esa rama con `main` antes del siguiente handoff o nueva validacion.
- Antes de declarar `Estado operativo: listo para qa`, `developer-teams` debe comprobar que la rama integra limpia con `main`.

## Disparador operativo de `doc-teams`
`doc-teams` debe priorizar una iteracion cuando concurran estas condiciones:
1. Existe `Estado operativo: validado` en la issue.
2. La entrega de desarrollo indica `Impacto documental: si`.

Si el impacto documental es `no`, la documentacion puede esperar salvo instruccion explicita.

## Checkpoint de cierre de `product-manager`
Tras `Estado operativo: validado`, `product-manager` debe:
1. verificar que la trazabilidad funcional sigue siendo correcta
2. cerrar la issue o dejar constancia explicita del motivo por el que sigue abierta
3. si sigue abierta, indicar bloqueo actual, siguiente responsable y siguiente paso operativo
4. promover el merge segun el flujo del repositorio

Si la issue sigue abierta, usar esta plantilla minima:

```text
Bloqueo actual: <motivo concreto>
Siguiente responsable: product-manager|developer-teams|qa-teams|doc-teams
Siguiente paso operativo: <accion verificable>
Estado de integracion: pendiente|hecho|no aplica
```

## Regla de simplicidad
Estos acuerdos existen para reducir esperas y reprocesos. No deben usarse para introducir estados adicionales ni ceremonias no justificadas.
