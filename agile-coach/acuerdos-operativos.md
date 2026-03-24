# Acuerdos operativos entre equipos

## Objetivo
Reducir ambiguedades en los handoffs entre `product-manager`, `developer-teams`, `qa-teams` y `doc-teams` sin alterar la separacion de responsabilidades ya definida en el repositorio.

## Referencia canónica de coordinacion
Este documento es la referencia canónica para las reglas compartidas de coordinacion entre equipos. Cuando exista una duda sobre estados operativos, plantillas literales de handoff o checkpoints de cierre, debe tomarse como fuente primaria esta guia y no una copia dispersa en otro documento.

Las demas referencias del proyecto tienen este uso:
- `AGENTS.md` de raiz y de cada rol: instruccion operativa del rol, con las reglas compartidas reflejadas aqui solo en la medida necesaria para cada equipo.
- `README.md`: resumen general del flujo y orientacion inicial para personas o agentes nuevos.
- `changelog/README.md`: referencia canónica del formato del changelog diario.

Si una regla compartida cambia, primero debe actualizarse este documento y despues sincronizarse la redaccion equivalente en los documentos que la consumen.

## Mantenimiento de la fuente canónica
- Cualquier regla compartida nueva o modificada sobre estados operativos, handoffs, sincronizacion o cierres debe redactarse primero en este documento.
- Los `AGENTS.md` de raiz y de rol pueden resumir la regla, pero no deben convertirse en la fuente primaria ni introducir una redaccion distinta sin actualizar esta guia en el mismo cambio.
- Si existe divergencia entre una copia y esta guia, prevalece esta guia hasta que la copia quede sincronizada.

## Estados operativos comunes
Todos los equipos deben reutilizar estos estados operativos en sus comentarios y transiciones de trabajo:

- `nuevo`: issue creada y lista para ser tomada.
- `en desarrollo`: `developer-teams` ha tomado la issue y trabaja sobre una rama dedicada.
- `listo para qa`: desarrollo ha terminado una entrega revisable y ha dejado evidencia suficiente.
- `no validado`: QA ha encontrado defectos o incumplimientos que obligan a nueva entrega.
- `validado`: QA confirma que la entrega cumple el alcance revisado.
- `cerrado`: `product-manager` cierra la issue tras validacion y promueve el siguiente paso de integracion.

Ademas, el campo `Estado operativo:` del cuerpo de la issue debe reflejar siempre el ultimo estado real visible en el flujo. El rol que produzca la transicion debe actualizarlo en GitHub junto con su comentario estructurado.

## Paquete minimo para iniciar una issue
Antes de que `developer-teams` abra una rama, la issue debe incluir como minimo y de forma literal:
- `Backlog:`
- `Historia de usuario:`
- `Caso de uso:`
- `Criterios de aceptacion:`
- `Dependencias:`
- `Estado operativo: nuevo`

Si falta alguno de estos campos, la issue no debe considerarse lista para desarrollo y `product-manager` debe completarla antes del inicio tecnico.

Ademas, `product-manager` debe vigilar que la deuda tecnica relevante detectada en iteraciones previas este trazada en backlog y no quede fuera del sistema de priorizacion.

## Arranque minimo de `developer-teams`
Cuando `developer-teams` tome una issue debe publicar un comentario de arranque con esta plantilla minima:

```text
Rol: developer-teams
Rama: <nombre-rama>
Estado operativo: en desarrollo
```

Este comentario fija que rama esta activa, permite auditar el limite de ramas abiertas y evita que el estado `en desarrollo` quede escondido en texto libre.
Al publicar este arranque, `developer-teams` debe actualizar tambien el `Estado operativo:` del cuerpo de la issue a `en desarrollo`.

## Handoff minimo de `developer-teams` a `qa-teams`
El comentario final de entrega de `developer-teams` debe incluir como minimo:
- `Rama:`
- `Resumen:`
- `Decisiones relevantes:`
- `Refactorizacion aplicada:`
- `Limitaciones conocidas:`
- `Deuda tecnica identificada:`
- `Revision de codigo realizada:`
- `Verificacion tecnica ejecutada:`
- `Impacto documental: si|no`
- `Estado operativo: listo para qa`

Plantilla minima recomendada:

```text
Rol: developer-teams
Rama: <nombre-rama>
Resumen:
- ...
Decisiones relevantes:
- ...
Refactorizacion aplicada:
- ...
Limitaciones conocidas:
- ...
Deuda tecnica identificada:
- ...
Revision de codigo realizada:
- ...
Verificacion tecnica ejecutada:
- <comando o evidencia>
Impacto documental: si|no
Estado operativo: listo para qa
```

Al publicar este handoff, `developer-teams` debe actualizar tambien el `Estado operativo:` del cuerpo de la issue a `listo para qa`.

## Handoff minimo de `qa-teams`
El comentario de revision de `qa-teams` debe incluir como minimo:
- `Rama revisada:`
- `Pruebas realizadas:`
- `Revision de codigo:`
- `Resultados observados:`
- `Defectos bloqueantes:`
- `Observaciones:`
- `Riesgos:`
- `Estado operativo: validado|no validado`

Plantilla minima recomendada:

```text
Rol: qa-teams
Rama revisada: <nombre-rama>
Pruebas realizadas:
- ...
Revision de codigo:
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

Al publicar este resultado, `qa-teams` debe actualizar tambien el `Estado operativo:` del cuerpo de la issue a `validado` o `no validado` segun corresponda.

## Gate previo de `qa-teams`
Antes de ejecutar la validacion funcional, `qa-teams` debe comprobar dos condiciones:
1. La entrega de `developer-teams` usa la plantilla minima de handoff.
2. La rama revisada integra limpia con `main`.
3. Existe evidencia suficiente de revision de codigo y de como se ha tratado la deuda tecnica o la refactorizacion necesaria.

Si alguna de estas condiciones falla, `qa-teams` debe registrar el problema como defecto bloqueante u operativo y cerrar la revision con `Estado operativo: no validado` sin dar por buena la entrega.

## Regla de revalidacion
Si QA deja `Estado operativo: no validado`:
1. La issue sigue abierta.
2. `developer-teams` mantiene la misma rama mientras el alcance siga siendo el mismo.
3. `developer-teams` prioriza esa misma issue frente a nuevas issues.
4. `developer-teams` publica un nuevo comentario de entrega con la plantilla completa, las correcciones y una nueva evidencia.
5. `developer-teams` vuelve a actualizar el `Estado operativo:` del cuerpo de la issue a `listo para qa`.
6. `qa-teams` vuelve a revisar esa misma issue.

Si el alcance cambia de forma material, `product-manager` debe decidir si corresponde una nueva issue.

## Regla de integracion tras `validado`
- Tras `Estado operativo: validado`, `developer-teams` debe priorizar la fusion de la rama tecnica en `main` y su borrado antes de iniciar una nueva issue, salvo bloqueo operativo documentado en la propia issue.
- Si la integracion no puede hacerse de inmediato, `product-manager` debe dejar visible el motivo en su comentario administrativo usando `Bloqueo actual:` y `Estado de integracion: pendiente`.
- Hasta que la fusion no exista, la funcionalidad aceptada por QA no debe tratarse como comportamiento vigente en la documentacion oficial mantenida sobre `main`.

## Regla de sincronizacion entre ramas y `main`
- `changelog/` se actualiza solo en `main` y no forma parte de la entrega tecnica del issue.
- Si `developer-teams` o `qa-teams` registran actividad en `changelog/` mientras mantienen una rama abierta, deben sincronizar despues esa rama con `main` antes del siguiente handoff o nueva validacion.
- Antes de declarar `Estado operativo: listo para qa`, `developer-teams` debe comprobar que la rama integra limpia con `main`.

## Sincronizacion entre backlog y issue activa
Cuando un item del backlog tenga issue GitHub activa, el campo `Estado` del backlog debe reflejar el mismo estado operativo visible de esa issue. Mientras la issue avance por `en desarrollo`, `listo para qa`, `no validado`, `validado` o `cerrado`, el backlog no debe conservar `nuevo` por inercia.

Esta sincronizacion debe ejecutarse junto con la transicion operativa que la provoca, para que el backlog siga siendo una fotografia util del trabajo real y no solo un registro de planificacion inicial.

## Disparador operativo de `doc-teams`
`doc-teams` debe priorizar una iteracion cuando concurran estas condiciones:
1. Existe `Estado operativo: validado` en la issue.
2. La entrega de desarrollo indica `Impacto documental: si`.
3. La rama tecnica correspondiente ya ha sido fusionada en `main`.

Si el impacto documental es `no`, o si la entrega sigue validada pero todavia no integrada en `main`, la documentacion puede esperar salvo instruccion explicita.

## Checkpoint de cierre de `product-manager`
Tras `Estado operativo: validado`, `product-manager` debe:
1. verificar que la trazabilidad funcional sigue siendo correcta
2. cerrar la issue o dejar constancia explicita del motivo por el que sigue abierta
3. si sigue abierta, indicar bloqueo actual, siguiente responsable y siguiente paso operativo
4. promover el merge segun el flujo del repositorio

Si la issue sigue abierta, usar esta plantilla minima:

```text
Rol: product-manager
Bloqueo actual: <motivo concreto>
Siguiente responsable: product-manager|developer-teams|qa-teams|doc-teams
Siguiente paso operativo: <accion verificable>
Estado de integracion: pendiente|hecho|no aplica
```

Al cerrar definitivamente la issue, `product-manager` debe actualizar tambien el cuerpo de la issue a `Estado operativo: cerrado` para que el estado visible coincida con el cierre real en GitHub.

## Sincronizacion documental tras integracion
- Cuando una issue validada se fusiona en `main`, `product-manager` debe reconciliar el backlog, el refinamiento funcional y el roadmap afectados antes de iniciar una nueva issue funcional.
- Si la issue sigue abierta por cierre administrativo o seguimiento, el comentario debe indicar tambien si la documentacion de producto ya quedo sincronizada o sigue pendiente.
- No debe permanecer una version de backlog que sugiera `nuevo` o pendiente de trabajo cuando la entrega ya esta integrada en `main`.

## Regla de simplicidad
Estos acuerdos existen para reducir esperas y reprocesos. No deben usarse para introducir estados adicionales ni ceremonias no justificadas.

## Regla de prevencion de deuda tecnica
- `developer-teams` debe revisar y sanear el codigo dentro del alcance razonable de cada issue, no solo implementar el cambio minimo que haga pasar pruebas.
- `qa-teams` debe comprobar que esa revision existe y que no se esta trasladando deuda tecnica evitable a iteraciones futuras sin dejarla trazada.
- `product-manager` debe convertir la deuda tecnica relevante diferida en backlog o issues separadas antes del cierre administrativo de una entrega.
