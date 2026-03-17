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
|-- product-manager/
|   |-- AGENTS.md
|   `-- vision-product.md
|-- developer-teams/
|-- qa-teams/
|-- doc-teams/
`-- agile-coach/
```

### Descripcion de carpetas

- `product-manager/`: documentacion de producto, vision, backlog y artefactos funcionales.
- `developer-teams/`: instrucciones, entregables y documentacion del equipo de desarrollo.
- `qa-teams/`: instrucciones, criterios y evidencia del equipo de validacion funcional y de calidad.
- `doc-teams/`: instrucciones y artefactos de documentacion funcional, tecnica y de administracion del proyecto.
- `agile-coach/`: instrucciones y artefactos para mejora continua, coordinacion entre equipos y optimizacion de procesos.

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
- Limitar lectura y escritura al directorio del proyecto `/opt/apps/podencoti`.

## Flujo de trabajo entre equipos

- El equipo `product-manager` es quien crea y mantiene los issues funcionales en el repositorio remoto de GitHub.
- El equipo `developer-teams` debe leer los issues abiertos antes de empezar a implementar.
- `developer-teams` debe trabajar solo en una tarea cada vez para facilitar la revision de `qa-teams`.
- Si existen issues ya empezados y todavia no validados por `qa-teams`, `developer-teams` debe priorizarlos frente a issues completamente nuevos.
- Si todos los issues abiertos son nuevos, `developer-teams` puede decidir el orden de implementacion segun su propio criterio tecnico y de desbloqueo.
- Antes de comenzar cualquier issue, `developer-teams` debe crear una rama nueva en git dedicada a ese trabajo.
- `developer-teams` es responsable de los test tecnicos, como unit tests, integration tests, test de componente y test de API.
- Una vez implementada la tarea, `developer-teams` debe actualizar el issue correspondiente con el trabajo realizado para que `qa-teams` pueda revisarlo.
- Cada cambio implementado por `developer-teams` debe terminar con `git commit` en espanol y `git push` de la rama remota.
- `qa-teams` revisa y valida el trabajo sobre la rama de la tarea desde la perspectiva del usuario y de los criterios de aceptacion.
- `qa-teams` es responsable de los tests de validacion, como pruebas funcionales, end-to-end, exploratorias y contra criterios de aceptacion.
- `qa-teams` debe dejar en la issue el resultado de la revision y finalizar con un estado explicito de `validado` o `no validado`.
- Si el resultado es `no validado`, `qa-teams` debe explicar la razon para que `developer-teams` pueda resolverla.
- Solo tras la validacion de `qa-teams`, `product-manager` debe cerrar el issue y promover el merge de la rama a `main`.

## Recomendaciones para evolucionar el repositorio

- Mantener en `product-manager/` la fuente de verdad funcional y de negocio.
- Añadir documentacion transversal si el proyecto crece, por ejemplo `README.md`, decision records y convenciones de versionado.
- Evitar que un rol modifique artefactos propios de otro sin dejar constancia clara del motivo.

## Regla de seguridad organizativa

Ningun rol debe darse por activado por contexto implicito, por nombre de carpeta o por historial previo del chat. La activacion debe venir indicada expresamente en el prompt actual del usuario.
