# Roadmap de PodencoTI

## Criterios de planificacion
- Se prioriza validar primero la propuesta de valor central: centralizacion y filtrado de oportunidades TI.
- Las fases representan releases funcionales, no decisiones tecnicas de implementacion.
- Cada release debe dejar un resultado verificable por `qa-teams` y trazable a backlog e issues.

## Estado de referencia de la iteracion
- Fecha de corte documental: 2026-03-30.
- Estado confirmado: `PB-007` y `PB-006` ya fueron validados por `qa-teams` y sus entregas estan integradas en `main`.
- Estado actual de trabajo tecnico: `PB-009` ya esta validado, integrado en `main` y cerrado administrativamente en la issue #9.
- `PB-004` ya no esta en preparacion ni pendiente de integracion: `qa-teams` la valido en la issue #6 el 2026-03-25 y `developer-teams` la integro en `main` con borrado de rama el 2026-03-26.
- Siguiente recomendacion para `developer-teams`: integrar en `main` la entrega validada de `PB-012`, dejar evidencia de fusion y borrado de rama en la issue #12 y, solo despues, tomar `PB-010` o `PB-013` segun la capacidad disponible para experiencia y gobierno funcional.
- Las decisiones funcionales sobre expedientes mixtos y sobre oportunidades anuladas, desiertas, desistidas o modificadas quedan ya definidas para evitar bloqueo de backlog posterior.
- En esta revision tambien quedan cerradas cuatro aclaraciones de release para reducir ambiguedad de implementacion:
  - una alerta del MVP requiere al menos un criterio funcional informado
  - el alta inicial en pipeline crea siempre el estado `Nueva`
  - `PB-008` puede refinarse documentalmente antes de disponer de instrumentacion completa
  - la recopilacion desde fuentes reales oficiales nominadas se prioriza antes que alertas y pipeline
- `PB-009` debe ejecutarse por olas y con trazabilidad minima visible al origen oficial
- La validacion y la integracion de `PB-009` confirman la prioridad funcional definida y permiten abrir una nueva iteracion de operativizacion visible del dato real antes de continuar con retencion o con base de interfaz transversal
- Los informes de `quality-auditor` y `security-auditor` del 2026-03-28 introducen una dependencia de priorizacion tecnica: producto debe reservar capacidad para las issues tecnicas que `developer-teams` abra a partir de esos hallazgos antes de ampliar el alcance funcional sin control.

## Release 0: Delimitacion funcional del MVP
- Objetivo: Cerrar ambiguedades criticas antes de la implementacion del catalogo.
- Alcance:
  - PB-007 Cobertura inicial de fuentes prioritarias.
- Criterios de salida:
  - Existe una lista visible y verificable de fuentes `MVP`, `Posterior` y `Por definir`.
  - La interfaz o configuracion no induce a pensar que existe cobertura total.
- Estado actual:
  - `PB-007` completado, validado e integrado en `main`.

## Release 1: Regla de relevancia y descubrimiento
- Objetivo: Permitir descubrir y evaluar oportunidades TI con criterio funcional consistente.
- Alcance:
  - PB-006 Reglas funcionales de clasificacion TI.
  - PB-001 Catalogo inicial de oportunidades TI.
  - PB-002 Ficha de detalle de licitacion.
  - PB-003 Filtros funcionales de busqueda.
- Criterios de salida:
  - El catalogo solo muestra oportunidades alineadas con la cobertura y la regla TI.
  - El usuario puede localizar, revisar y filtrar oportunidades sin recorrer varios portales.
  - El catalogo y la ficha muestran el estado oficial del expediente cuando la fuente lo informe.
  - `qa-teams` puede verificar una muestra de inclusiones, exclusiones y campos visibles.
- Riesgo principal:
  - Que el equipo implemente un catalogo visible pero comunique cobertura o relevancia con mas seguridad de la que la release realmente soporta.
- Estado operativo actual:
  - `PB-006` ya esta validado e integrado en `main` como prerequisito del catalogo.
  - `PB-001` y `PB-002` ya fueron validados por `qa-teams` y estan integrados administrativamente en `main`.
  - `PB-003` ya fue validado por `qa-teams` el 2026-03-20 en la issue #5, integrado por `developer-teams` en `main` el 2026-03-21 y cerrado administrativamente por `product-manager`.

## Release 2: Fuentes reales priorizadas
- Objetivo: Reforzar la credibilidad del producto y la utilidad del catalogo priorizando recopilacion desde fuentes oficiales reales.
- Alcance:
  - PB-009 Priorizacion de recopilacion desde fuentes reales oficiales.
- Secuencia funcional de esta release:
  - Ola 1: `BOC`
  - Ola 2: `BOP Las Palmas`
  - Ola 3: `BOE`
- Criterios de salida:
  - Existe una prioridad trazable y ejecutable de fuentes reales oficiales para recopilacion.
  - `BOC`, `BOP Las Palmas` y `BOE` quedan identificadas de forma explicita como fuentes reales prioritarias y ordenadas por olas.
  - La entrega deja visible, para cada oportunidad obtenida desde estas fuentes, la trazabilidad minima al origen oficial.
  - La secuencia de entregas deja claro que esta prioridad adelanta a nuevas capacidades de retencion y no amplía por si misma la promesa comercial de cobertura.
- Riesgo principal:
  - Que el producto invierta antes en engagement que en reforzar la calidad y credibilidad de las oportunidades visibles.
- Estado operativo actual:
  - `PB-009` quedo validado por `qa-teams` sobre la entrega integrada en `main` el 2026-03-24.
  - `developer-teams` dejo trazabilidad explicita de integracion y borrado de rama en la issue #9 el 2026-03-24.
  - `product-manager` cerro administrativamente la issue #9 el 2026-03-25 tras reconciliar backlog, historia, caso de uso y roadmap.

## Release 3: Consolidacion de snapshots `.atom` y trazabilidad de origen
- Objetivo: Convertir los `.atom` versionados ya presentes en `data/` en una fuente operativa consolidada de oportunidades TI Canarias con trazabilidad al fichero origen.
- Alcance:
  - PB-011 Consolidacion funcional de fuentes `.atom` versionadas para oportunidades TI Canarias.
- Criterios de salida:
  - La aplicacion procesa todos los `.atom` presentes en `data/` sin depender de un nombre de fichero fijo.
  - El filtrado funcional usa criterios estructurados de Canarias y CPV TI.
  - Si un expediente aparece en varios snapshots, queda una unica version funcional vigente.
  - Cada registro consolidado conserva el nombre del fichero `.atom` origen de la version vigente.
- Riesgo principal:
  - Que la aplicacion siga dependiendo de un snapshot puntual, no absorba actualizaciones de nombre y rompa la trazabilidad del dato.
- Estado operativo actual:
  - `qa-teams` valido `PB-011` en la issue #11 el 2026-03-27.
  - `developer-teams` integro la rama en `main` y la elimino el 2026-03-28.
  - `product-manager` cerro administrativamente la issue #11 el 2026-03-28.

## Release 4: Vistas verificables de licitaciones, lotes y adjudicaciones
- Objetivo: Hacer visible en la aplicacion la informacion consolidada derivada de los `.atom` en una superficie contrastable con el Excel funcional de referencia.
- Alcance:
  - PB-012 Exposicion funcional en la aplicacion del dataset de licitaciones TI Canarias.
- Criterios de salida:
  - Existen las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
  - La informacion visible se corresponde funcionalmente con `data/licitaciones_ti_canarias.xlsx` para la muestra actual.
  - El detalle de la licitacion o contrato muestra el fichero `.atom` origen.
  - Los datos no informados y los estados vacios se muestran de forma clara.
- Riesgo principal:
  - Que el dato consolidado exista tecnicamente pero siga sin una superficie funcional verificable por usuario y QA.
- Dependencia operativa:
  - La release ya esta `validada` por `qa-teams` en la issue #12, pero sigue pendiente de integracion administrativa en `main` hasta que `developer-teams` deje constancia explicita de fusion y borrado de rama.

## Release 5: Base de navegacion y control de acceso
- Objetivo: Establecer una estructura comun de interfaz y un modelo minimo de permisos para sostener el crecimiento de modulos con una experiencia coherente y controlada.
- Alcance:
  - PB-010 Navegacion principal responsive con menu lateral de iconos.
  - PB-013 Modelo funcional de roles y permisos.
- Criterios de salida:
  - La aplicacion muestra una navegacion principal comun y persistente en el lateral izquierdo cuando el ancho disponible lo permite.
  - La opcion activa queda visible y el contenido principal no se solapa con la navegacion.
  - En anchos reducidos la aplicacion conserva acceso util a las opciones principales mediante una variante responsive.
  - Las opciones no disponibles no se presentan como modulos operativos sin senalizacion explicita.
  - Las acciones visibles de consulta y gestion se ajustan al rol del usuario sin exponer controles no autorizados.
- Riesgo principal:
  - Que el producto siga creciendo por modulos sin una base comun de interfaz y permisos y se vuelva mas dificil de usar, gobernar y evolucionar.
- Decision de alcance:
  - La primera iteracion de `PB-013` debe aplicarse sobre las superficies ya disponibles en producto y no quedar bloqueada por la futura existencia de `PB-005`; la extension de permisos a pipeline se aplicara cuando esa superficie exista.

## Release 6: Alertas y seguimiento operativo
- Objetivo: Convertir el descubrimiento en uso recurrente y gestion operativa.
- Alcance:
  - PB-004 Configuracion de alertas tempranas.
  - PB-005 Pipeline de seguimiento de oportunidades.
- Criterios de salida:
  - El usuario puede dejar configurados criterios persistentes de interes.
  - El usuario puede seguir oportunidades guardadas sin duplicados y con estados consistentes.
  - Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no se presentan como nuevas alertas accionables y siguen siendo visibles en pipeline con advertencia.
- Dependencia clave:
  - Requiere que Release 1 haya validado el valor del catalogo y de los filtros, que Release 2 haya fijado la prioridad de recopilacion real y que Release 3 y Release 4 hayan hecho visible la base operativa derivada de `.atom`.
- Decision funcional vigente:
  - Las alertas del MVP registran coincidencias de forma interna; la notificacion saliente queda fuera de esta release.
  - Una alerta del MVP solo es valida si contiene al menos un criterio funcional; no se permiten alertas vacias.
  - El pipeline del MVP es individual por usuario; la colaboracion por empresa queda para una release posterior.
  - El alta inicial de una oportunidad en pipeline debe crear el estado `Nueva`.
- Estado operativo actual:
  - `PB-004` ya fue validado por `qa-teams` en la issue #6 el 2026-03-25, integrado en `main` por `developer-teams` el 2026-03-26 y queda cerrado administrativamente por `product-manager`.
  - `PB-005` permanece en `nuevo` y no debe iniciarse antes de `PB-011` y `PB-012`, ni antes de decidir si la base de navegacion `PB-010` entra antes o despues de esta exposicion funcional.
  - `PB-013` queda preparado en la issue #13 para convertir el modelo de roles y permisos en comportamiento observable sobre las superficies ya disponibles antes de ampliar mas gestion multiusuario.

## Release 7: Medicion y aprendizaje
- Objetivo: Mejorar precision, cobertura y priorizacion apoyandose en indicadores.
- Alcance:
  - PB-008 Medicion basica de valor del producto.
  - Ajustes de priorizacion segun feedback y resultados de QA.
- Criterios de salida:
  - Existen definiciones de KPI utilizables para decidir siguientes inversiones funcionales.
  - El roadmap posterior puede justificarse con evidencia y no solo con intuicion.

## Dependencias abiertas de roadmap
- Confirmar con negocio cuando la cobertura de ayuntamientos pasa de `Posterior` a promesa comercial del producto.
- Definir en una iteracion posterior si las oportunidades modificadas deben generar historial visible de cambios, no solo el ultimo dato oficial.
- Decidir en una iteracion posterior si los KPIs de alertas deben exigirse ya con dato real o pueden arrancar con definicion documental y recogida manual temporal.
- Confirmar que modulos deben formar parte de la navegacion principal visible desde la primera entrega de `PB-010` y cuales deben quedar ocultos o marcados como `proximamente`.
- Confirmar si la referencia funcional al Excel debe cubrir en una iteracion posterior tambien la hoja `Modificaciones` cuando existan datos disponibles.

## Decision operativa para la siguiente iteracion
- El siguiente paso operativo de producto es mantener sincronizados backlog, historias, roadmap e issues abiertos con la nueva prioridad funcional.
- El siguiente paso operativo recomendado para `developer-teams` es fusionar en `main` la entrega ya validada de `PB-012` y dejar trazabilidad de esa integracion en la issue #12; despues, tomar `PB-010` o `PB-013`.
- `PB-009` ya reutiliza la cobertura validada de `PB-007`, la regla auditable validada de `PB-006` y la superficie ya validada de catalogo, detalle y filtros.
- No se recomienda iniciar `PB-005` antes de completar la integracion administrativa de `PB-012`; la base de navegacion `PB-010` y el control de acceso `PB-013` deben reevaluarse despues de dejar esa entrega fusionada en `main`.
- Antes de abrir una nueva expansion funcional, producto debe recibir de `developer-teams` la traduccion a issues tecnicas de los hallazgos accionables de auditoria del 2026-03-28 para poder priorizarlos frente al roadmap vigente.
- A fecha 2026-03-30 la rama `developer-teams/issue-12-pb-012-vistas-excel` sigue siendo la referencia de una entrega ya validada; el siguiente cuello de botella es integrar esa rama y ordenar despues la siguiente implementacion funcional.
