# AGENTS.md

## Proposito

Este archivo define las reglas globales del repositorio `podencoti` y aclara como deben activarse las instrucciones especificas de cada rol.

## Regla de activacion por rol

Las instrucciones de subdirectorios solo se aplicaran si el prompt lo indica de forma explicita.

- Solo se seguiran las instrucciones de `product-manager/AGENTS.md` si en el prompt se especifica que se actua como rol `product-manager`.
- Solo se seguiran las instrucciones de `developer-teams/AGENTS.md` si en el prompt se especifica que se actua como rol `developer-teams`.
- Solo se seguiran las instrucciones de `qa-teams/AGENTS.md` si en el prompt se especifica que se actua como rol `qa-teams`.
- Solo se seguiran las instrucciones de `doc-teams/AGENTS.md` si en el prompt se especifica que se actua como rol `doc-teams`.
- Solo se seguiran las instrucciones de `agile-coach/AGENTS.md` si en el prompt se especifica que se actua como rol `agile-coach`.

Si el prompt no activa uno de esos roles de forma explicita, no deben asumirse ni heredarse automaticamente sus instrucciones.

## Jerarquia de instrucciones del proyecto

1. Este `AGENTS.md` de raiz define las reglas generales del repositorio.
2. Los archivos `AGENTS.md` de cada area definen instrucciones especificas de ese rol.
3. Las instrucciones de area solo complementan a las de raiz cuando el rol ha sido activado expresamente en el prompt.

## Estructura actual del proyecto

```text
/
|-- AGENTS.md
|-- Makefile
|-- README.md
|-- pyproject.toml
|-- changelog/
|-- data/
|-- src/
|   `-- podencoti/
|-- tests/
|-- product-manager/
|-- developer-teams/
|-- qa-teams/
|-- doc-teams/
|-- agile-coach/
|-- rol-product-manager.sh
|-- rol-developer-teams.sh
|-- rol-qa-teams.sh
|-- rol-doc-teams.sh
|-- rol-agile-coach.sh
`-- run-codex.sh
```

### Descripcion de carpetas

- `src/`: codigo fuente Python de la aplicacion.
- `tests/`: pruebas tecnicas automatizadas del proyecto.
- `data/`: datos versionados que utiliza la aplicacion.
- `changelog/`: registro diario de actividad por rol.
- `product-manager/`: documentacion de producto, vision, backlog y artefactos funcionales.
- `developer-teams/`: instrucciones, entregables y documentacion del equipo de desarrollo.
- `qa-teams/`: instrucciones, criterios y evidencia del equipo de validacion funcional y de calidad.
- `doc-teams/`: instrucciones y artefactos de documentacion funcional, tecnica y de administracion del proyecto.
- `agile-coach/`: instrucciones y artefactos para mejora continua, coordinacion entre equipos y optimizacion de procesos.

### Otros ficheros relevantes en raiz

- `Makefile`: comandos de ejecucion local y pruebas.
- `README.md`: descripcion general del proyecto y forma de uso.
- `pyproject.toml`: metadatos y configuracion base del paquete Python.
- `rol-*.sh`: scripts de entrada para ejecutar cada rol con su prompt correspondiente.
- `run-codex.sh`: script auxiliar de ejecucion de Codex.

## Vision del producto

`PodencoTI` es una plataforma para centralizar y detectar oportunidades de contratacion publica TI en Canarias. El producto busca evitar la busqueda manual en multiples portales, agregando licitaciones, clasificandolas como relevantes para tecnologia y enviando alertas tempranas para que empresas y profesionales puedan preparar ofertas con mas tiempo y mejor informacion.

### Problema que resuelve

- La contratacion publica canaria esta fragmentada en muchos portales y perfiles del contratante.
- La identificacion manual de licitaciones TI consume tiempo y produce errores u oportunidades perdidas.
- Los equipos comerciales y tecnicos llegan tarde a pliegos relevantes por falta de centralizacion y filtrado.

### Usuarios objetivo

- Pymes y startups tecnologicas.
- Consultoras e integradores TI.
- Profesionales autonomos del sector tecnologico.

### Capacidades clave esperadas

- Rastreo automatizado de fuentes oficiales de contratacion en Canarias.
- Clasificacion inteligente de oportunidades TI.
- Filtros por palabras clave, presupuesto, procedimiento y ubicacion.
- Extraccion de datos criticos de cada licitacion.
- Alertas y seguimiento de oportunidades en un pipeline de trabajo.

## Principios operativos recomendados

- Escribir en espanol salvo que el prompt indique lo contrario.
- Mantener trazabilidad entre vision, requisitos, desarrollo y validacion.
- No mezclar decisiones de producto con decisiones tecnicas sin dejar claras las dependencias.
- Priorizar documentos y entregables accionables frente a texto ambiguo o decorativo.
- Hacer explicitos supuestos, riesgos, dependencias y preguntas abiertas.
- Mantener `main` como rama de referencia para trabajo funcional, documental y de coordinacion no tecnica.
- Mantener `main` como rama obligatoria para cualquier actualizacion de ficheros dentro de `changelog/`, independientemente del rol que la realice.
- En cualquier actualizacion de `changelog/`, cada rol debe iniciar su bloque o seccion con la hora exacta de escritura.
- Si un mismo rol registra actividad en dos momentos distintos del mismo dia, debe crear dos entradas separadas, cada una con su propia seccion diferenciada y su propia hora de escritura.
- Cada actualizacion de `changelog/` debe terminar con `git commit` y `git push` al repositorio remoto sobre la rama `main`.
- Los cambios de `changelog/` no forman parte de la entrega tecnica de una issue y no deben permanecer en ramas tecnicas ni en ramas temporales de integracion.
- Si un rol mantiene una rama abierta y registra actividad en `changelog/` sobre `main`, debe sincronizar despues su rama abierta con `main` antes del siguiente handoff a QA o integracion.
- Limitar el numero de ramas abiertas para facilitar el seguimiento operativo del proyecto.
- Todos los commits del repositorio deben comenzar con el prefijo del rol que los ejecuta en formato `[rol]`, por ejemplo `[developer-teams] Implementa clasificacion TI`.
- Si para ejecutar o desarrollar el proyecto en Python fuese necesaria la instalacion de librerias adicionales en el sistema o en el entorno de trabajo, debe existir y mantenerse un fichero `requirements.txt` en la raiz del repositorio con dichas dependencias.
- Limitar lectura y escritura al directorio del proyecto `/opt/apps/podencoti`.

## Flujo de trabajo entre equipos

- El equipo `product-manager` es quien crea y mantiene los issues funcionales en el repositorio remoto de GitHub.
- Los issues deben usar un estado operativo comun entre equipos para reducir ambiguedad: `nuevo`, `en desarrollo`, `listo para qa`, `no validado`, `validado` y `cerrado`.
- Los roles `product-manager`, `doc-teams` y `agile-coach` trabajan directamente sobre `main` y no deben crear ramas de trabajo propias.
- El equipo `developer-teams` debe leer los issues abiertos antes de empezar a implementar.
- `developer-teams` debe trabajar solo en una tarea cada vez para facilitar la revision de `qa-teams`.
- Si existen issues ya empezados y todavia no validados por `qa-teams`, `developer-teams` debe priorizarlos frente a issues completamente nuevos.
- Si todos los issues abiertos son nuevos, `developer-teams` puede decidir el orden de implementacion segun su propio criterio tecnico y de desbloqueo.
- Solo `developer-teams` debe crear ramas tecnicas para implementar issues.
- Antes de comenzar cualquier issue tecnico, `developer-teams` debe comprobar cuantas ramas tecnicas activas existen y no debe abrir una nueva si ya hay dos ramas tecnicas abiertas en el proyecto.
- Cada issue tecnico debe indicar explicitamente la rama donde se esta realizando el trabajo para que el resto de equipos pueda localizarla sin ambiguedad.
- Cuando `developer-teams` tome una issue debe dejar constancia de `estado operativo: en desarrollo`.
- `developer-teams` es responsable de los test tecnicos, como unit tests, integration tests, test de componente y test de API.
- Una vez implementada la tarea, `developer-teams` debe actualizar el issue correspondiente con el trabajo realizado para que `qa-teams` pueda revisarlo, incluyendo como minimo rama, resumen, decisiones relevantes, limitaciones conocidas, verificacion tecnica ejecutada, impacto documental y `estado operativo: listo para qa`.
- En ese handoff a `qa-teams`, `developer-teams` debe usar de forma literal los campos `Rama:`, `Resumen:`, `Decisiones relevantes:`, `Limitaciones conocidas:`, `Verificacion tecnica ejecutada:`, `Impacto documental:` y `Estado operativo: listo para qa`.
- Antes de pedir revision a `qa-teams`, `developer-teams` debe comprobar que su rama integra limpia con `main` y resolver los conflictos evitables de sincronizacion.
- Cada cambio implementado por `developer-teams` debe terminar con `git commit` en espanol y `git push` de la rama remota.
- `qa-teams` revisa y valida el trabajo sobre la rama de la tarea desde la perspectiva del usuario y de los criterios de aceptacion.
- `qa-teams` puede crear una rama temporal de integracion para ejecutar pruebas o preparar la validacion cuando lo necesite. Esa rama de integracion es adicional a las dos ramas tecnicas permitidas, debe usarse solo para validacion y debe borrarse al terminar la revision.
- `qa-teams` es responsable de los tests de validacion, como pruebas funcionales, end-to-end, exploratorias y contra criterios de aceptacion.
- `qa-teams` debe dejar en la issue el resultado de la revision, incluyendo como minimo rama revisada, pruebas realizadas, resultados observados, defectos bloqueantes, observaciones, riesgos y `estado operativo: validado` o `estado operativo: no validado`.
- En ese comentario de revision, `qa-teams` debe usar de forma literal los campos `Rama revisada:`, `Pruebas realizadas:`, `Resultados observados:`, `Defectos bloqueantes:`, `Observaciones:`, `Riesgos:` y `Estado operativo: validado|no validado`.
- `qa-teams` debe verificar que la issue ha concluido realmente segun sus criterios de aceptacion y revisar si existe deuda tecnica relevante o si procede abrir una tarea tecnica de refactorizacion o mejora de codigo.
- Si el resultado es `no validado`, `qa-teams` debe explicar la razon para que `developer-teams` pueda resolverla en la misma issue y, mientras el alcance sea el mismo, en la misma rama.
- Solo tras la validacion de `qa-teams`, `product-manager` debe fusionar en `main` la rama tecnica correspondiente, cerrar el issue o dejar constancia explicita del motivo por el que sigue abierta, y borrar la rama tecnica una vez completado el merge si ya no existe una razon clara para conservarla.
- Si una issue permanece abierta tras `estado operativo: validado`, `product-manager` debe dejar un comentario administrativo con los campos literales `Bloqueo actual:`, `Siguiente responsable:`, `Siguiente paso operativo:` y `Estado de integracion: pendiente|hecho|no aplica` para evitar que siga abierta sin contexto.
- `doc-teams` debe intervenir cuando una entrega validada tenga `impacto documental: si`, salvo que se indique expresamente otra prioridad.
- Si existen ya dos ramas tecnicas abiertas, el proyecto debe concluir o desbloquear al menos una issue antes de iniciar una nueva implementacion tecnica.

## Recomendaciones para evolucionar el repositorio

- Mantener en `product-manager/` la fuente de verdad funcional y de negocio.
- Añadir documentacion transversal si el proyecto crece, por ejemplo `README.md`, decision records y convenciones de versionado.
- Evitar que un rol modifique artefactos propios de otro sin dejar constancia clara del motivo.

## Regla de seguridad organizativa

Ningun rol debe darse por activado por contexto implicito, por nombre de carpeta o por historial previo del chat. La activacion debe venir indicada expresamente en el prompt actual del usuario.
