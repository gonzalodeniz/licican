# Roadmap de Licican

## Criterios de planificacion
- Se prioriza validar primero la propuesta de valor central: centralizacion y filtrado de oportunidades TI.
- Las fases representan releases funcionales, no decisiones tecnicas de implementacion.
- Cada release debe dejar un resultado verificable por `qa-teams` y trazable a backlog e issues.

## Estado de referencia de la iteracion
- Fecha de corte documental: 2026-04-03.
- Estado confirmado: `PB-007` y `PB-006` ya fueron validados por `qa-teams` y sus entregas estan integradas en `main`.
- Estado actual de trabajo tecnico: `PB-009` ya esta validado, integrado en `main` y cerrado administrativamente en la issue #9.
- `PB-004` ya no esta en preparacion ni pendiente de integracion: `qa-teams` la valido en la issue #6 el 2026-03-25 y `developer-teams` la integro en `main` con borrado de rama el 2026-03-26.
- `PB-010` ya no forma parte del trabajo pendiente: quedo validada, integrada en `main` y cerrada administrativamente.
- `PB-005` ya no esta pendiente de integracion ni de cierre administrativo: la issue #7 fue cerrada en GitHub el 2026-04-01.
- `PB-013` ya no forma parte del trabajo pendiente: la issue #13 fue cerrada en GitHub el 2026-04-01 y su capacidad queda absorbida en el estado vigente del producto.
- `PB-016` ya no forma parte del trabajo pendiente: `qa-teams` lo valido en la issue #28 el 2026-04-02, la entrega ya esta integrada en `main` y `product-manager` reconcilia su cierre administrativo el 2026-04-03.
- `PB-015` ya no forma parte del trabajo pendiente: la issue #16 fue validada por `qa-teams`, integrada en `main` por `developer-teams` y cerrada administrativamente por `product-manager` el 2026-04-03.
- Siguiente recomendacion para `developer-teams`: priorizar las issues tecnicas derivadas de auditoria y dejar `PB-008` como trabajo ya integrado y pendiente solo de cierre administrativo.
- `PB-008` queda validado funcionalmente, integrado en `main` y listo para cierre administrativo; su bateria minima de KPI de cobertura, adopcion y uso ya esta definida y puede apoyarse en medicion manual temporal si hace falta.
- Las decisiones funcionales sobre expedientes mixtos y sobre oportunidades anuladas, desiertas, desistidas o modificadas quedan ya definidas para evitar bloqueo de backlog posterior.
- En esta revision tambien quedan cerradas cuatro aclaraciones de release para reducir ambiguedad de implementacion:
  - una alerta del MVP requiere al menos un criterio funcional informado
  - el alta inicial en pipeline crea siempre el estado `Nueva`
  - `PB-008` ya esta validado funcionalmente, integrado en `main` y listo para cierre administrativo sin depender de una instrumentacion completa
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
- Esta release se conserva solo como referencia historica; la superficie fue retirada de `main`.
- Objetivo: Conservar la trazabilidad historica de la entrega consolidada retirada, sin presentar la superficie como funcional en `main`.
- Alcance:
  - PB-012 Exposicion funcional en la aplicacion del dataset de licitaciones TI Canarias.
- Criterios de salida:
  - La referencia historica queda documentada sin exponer rutas activas en `main`.
  - Las menciones a la entrega consolidada se conservan solo como trazabilidad.
- Riesgo principal:
  - Que la documentacion siga sugiriendo una superficie retirada como si continuara operativa.
- Estado operativo actual:
  - `qa-teams` valido `PB-012` en la issue #12 el 2026-03-29.
  - `developer-teams` integro la rama validada en `main` y elimino la rama tecnica el 2026-03-30.
  - `product-manager` reconcilia esta release como ya integrada en `main` y cerrada administrativamente.

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
- Restriccion operativa vigente:
  - La issue tecnica `#14` ya no bloquea la siguiente secuencia documental y tecnica del producto.
  - `PB-010` y `PB-013` ya quedaron cerradas administrativamente; la siguiente prioridad funcional/documental elegible pasa a ser `PB-008` ya integrado y pendiente de cierre administrativo.
  - `PB-015` ya quedo cerrada administrativamente y deja de competir como trabajo abierto.

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
  - `PB-005` ya fue validado por `qa-teams` en la issue #7 el 2026-03-31 y quedo cerrado administrativamente en GitHub el 2026-04-01.
  - El riesgo abierto de esta release ya no es de cierre operativo, sino de reutilizar correctamente el seguimiento activo como base de la politica de retencion.

## Release 7: Medicion y aprendizaje
- Objetivo: Mejorar precision, cobertura y priorizacion apoyandose en indicadores.
- Alcance:
  - PB-008 Medicion basica de valor del producto.
  - Ajustes de priorizacion segun feedback y resultados de QA.
- Criterios de salida:
  - Existen definiciones de KPI utilizables para decidir siguientes inversiones funcionales.
  - La bateria minima cubre cobertura de fuentes priorizadas, adopcion temprana y uso recurrente.
  - La primera medicion puede ser manual si la instrumentacion completa aun no existe, siempre que la limitacion quede explicitada.
  - El roadmap posterior puede justificarse con evidencia y no solo con intuicion.

## Release 8: Escalado de consulta y gobierno de retencion
- Objetivo: Mejorar la consulta de listados amplios y definir una politica clara de conservacion y archivado de licitaciones.
- Alcance:
  - PB-014 Paginacion de resultados del catalogo.
  - PB-015 Panel de control de conservacion y archivado de licitaciones.
- Criterios de salida:
  - El catalogo y la API permiten recorrer resultados por paginas sin perder filtros ni orden.
  - El panel de control deja visible el umbral de conservacion y la politica de archivado.
  - Las licitaciones con seguimiento activo no se eliminan.
  - Las licitaciones cerradas se archivan en una tabla homologa cuando corresponde.
- Riesgo principal:
  - Que el volumen de resultados o la retencion de datos generen friccion operativa si no se acotan con una politica clara.
- Estado operativo actual:
  - `PB-014` ya quedo cerrado tras su integracion.
  - `PB-015` ya no es una prioridad funcional abierta tras su cierre administrativo el 2026-04-03.

## Release 9: Gobierno de usuarios y accesos
- Objetivo: Administrar cuentas de usuario, roles y permisos desde un modulo institucional y trazable.
- Alcance:
  - PB-016 Gestion de usuarios y accesos de plataforma.
- Criterios de salida:
  - El usuario con permisos suficientes puede listar, crear, editar y controlar cuentas desde un unico modulo.
  - Los cambios de rol, estado y permisos quedan auditados.
  - El sistema impide dejar la plataforma sin administradores activos.
  - La interfaz mantiene una lectura sobria y coherente con el resto del backoffice.
- Riesgo principal:
  - Que el producto crezca en volumen de cuentas sin una herramienta administrativa interna que evite gestion manual y errores de acceso.
- Estado operativo actual:
  - `qa-teams` valido `PB-016` en la issue #28 el 2026-04-02.
  - La capacidad ya esta integrada en `main` y queda cerrada administrativamente por `product-manager` el 2026-04-03.

## Dependencias abiertas de roadmap
- Confirmar con negocio cuando la cobertura de ayuntamientos pasa de `Posterior` a promesa comercial del producto.
- Definir en una iteracion posterior si las oportunidades modificadas deben generar historial visible de cambios, no solo el ultimo dato oficial.
- Decidir en una iteracion posterior si los KPIs de alertas deben exigirse ya con dato real o pueden arrancar con definicion documental y recogida manual temporal.
- Confirmar que modulos deben formar parte de la navegacion principal visible desde la primera entrega de `PB-010` y cuales deben quedar ocultos o marcados como `proximamente`.
- Confirmar si la referencia funcional al Excel debe cubrir en una iteracion posterior tambien la hoja `Modificaciones` cuando existan datos disponibles.
- Convertir en trabajo trazable las evoluciones posteriores del modulo de usuarios: autenticacion real, proveedor de identidad y auditoria centralizada.

## Decision operativa para la siguiente iteracion
- El siguiente paso operativo de producto es mantener sincronizados backlog, historias, roadmap e issues abiertos con la nueva prioridad funcional.
- La issue tecnica `T-002` ya quedo cerrada administrativamente el 2026-03-30 tras validacion, merge en `main` y borrado de rama.
- A partir de esta reconciliacion, el orden funcional/documental recomendado abierto pasa a `PB-008` ya integrado y a las issues tecnicas derivadas de auditoria.
- `PB-009` ya reutiliza la cobertura validada de `PB-007`, la regla auditable validada de `PB-006` y la superficie ya validada de catalogo, detalle y filtros.
- `PB-005` ya no debe tratarse como trabajo abierto: queda cerrado administrativamente y absorbido en la base funcional vigente.
- Antes de abrir una nueva expansion funcional, producto debe recibir de `developer-teams` la traduccion a issues tecnicas de los hallazgos accionables de auditoria del 2026-03-28 para poder priorizarlos frente al roadmap vigente.
- A fecha 2026-04-03 la integracion de `PB-012`, `PB-015`, `PB-016`, el cierre administrativo de la issue tecnica `#14`, el cierre de la issue #7 y el cierre de la issue #13 ya estan resueltos en `main` y en GitHub; el siguiente cuello de botella operativo pasa a ser cerrar administrativamente `PB-008` sin perder de vista las issues tecnicas derivadas de auditoria.
