# Historias de Usuario de Licican

## Convenciones
- Cada historia enlaza con backlog, caso de uso e issue de GitHub cuando existe.
- Los criterios de aceptacion estan redactados para validacion funcional por `qa-teams`.

## HU-01 Ver oportunidades TI centralizadas
- Backlog relacionado: PB-001
- Caso de uso relacionado: CU-01
- Issue relacionado: #3
- Historia:
  Como empresa o profesional TI,
  quiero ver en un unico catalogo las oportunidades de contratacion publica relevantes en Canarias,
  para detectar licitaciones a tiempo sin revisar manualmente multiples portales.
- Criterios de aceptacion:
  1. El catalogo muestra solo oportunidades clasificadas como TI.
  2. Cada oportunidad muestra titulo, organismo, ubicacion, procedimiento si existe, presupuesto si existe, fecha limite y estado oficial del expediente si la fuente lo informa.
  3. El usuario puede identificar la fuente oficial de cada oportunidad.
  4. Si no hay oportunidades disponibles, se muestra un mensaje claro de estado vacio.
- Dependencias funcionales: PB-007, PB-006
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: validado por `qa-teams` en la issue #3 el 2026-03-18, integrado en `main` y cerrado administrativamente por `product-manager` el 2026-03-19.

## HU-02 Evaluar una licitacion desde su ficha
- Backlog relacionado: PB-002
- Caso de uso relacionado: CU-02
- Issue relacionado: #4
- Historia:
  Como empresa o profesional TI,
  quiero consultar una ficha resumida de cada licitacion,
  para decidir rapido si debo incorporarla a mi proceso comercial o tecnico.
- Criterios de aceptacion:
  1. Desde el catalogo se puede acceder al detalle de una oportunidad.
  2. La ficha muestra como minimo presupuesto, fecha limite, procedimiento, organismo convocante, estado oficial del expediente y enlace a la fuente oficial.
  3. Si hay datos de solvencia tecnica o criterios de adjudicacion, se muestran de forma diferenciada.
  4. Si un dato no esta disponible en la fuente, se indica como no informado.
  5. Si la fuente publica una rectificacion o modificacion del mismo expediente, la ficha refleja el ultimo dato oficial visible.
- Dependencias funcionales: PB-001
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: validado por `qa-teams` en la issue #4 el 2026-03-19, integrado en `main` y cerrado administrativamente por `product-manager` el mismo dia.

## HU-03 Filtrar oportunidades relevantes
- Backlog relacionado: PB-003
- Caso de uso relacionado: CU-03
- Issue relacionado: #5
- Historia:
  Como empresa o profesional TI,
  quiero filtrar las oportunidades por criterios de negocio,
  para quedarme solo con las que encajan con mi capacidad y estrategia.
- Criterios de aceptacion:
  1. El usuario puede filtrar por palabra clave.
  2. El usuario puede filtrar por rango de presupuesto.
  3. El usuario puede filtrar por tipo de procedimiento y ubicacion.
  4. Los filtros activos se ven en pantalla y pueden limpiarse.
  5. Si no hay resultados, se muestra un estado vacio comprensible.
  6. Si el usuario introduce un rango de presupuesto minimo mayor que el maximo, el sistema solicita corregirlo y no presenta ese caso como una busqueda valida sin coincidencias.
- Dependencias funcionales: PB-001
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la reentrega de la issue #5 el 2026-03-20 tras comprobar la correccion del rango de presupuesto invalido en HTML y API. `developer-teams` integro la rama en `main` el 2026-03-21 y `product-manager` cierra administrativamente el trabajo.

## HU-04 Recibir alertas tempranas
- Backlog relacionado: PB-004
- Caso de uso relacionado: CU-04
- Issue relacionado: #6
- Historia:
  Como empresa o profesional TI,
  quiero configurar alertas sobre nuevos contratos relevantes,
  para enterarme antes y preparar mejor una oferta.
- Criterios de aceptacion:
  1. El usuario puede crear una alerta con al menos un criterio funcional valido.
  2. El sistema impide guardar una alerta vacia y solicita completar al menos un criterio.
  3. El sistema permite editar y desactivar la alerta.
  4. La alerta queda visible como activa tras guardarse.
  5. Las nuevas oportunidades compatibles quedan asociadas a la alerta para su registro interno en el MVP.
  6. Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no se presentan como nuevas coincidencias accionables.
- Dependencias funcionales: PB-001, PB-003
- Prioridad: P1
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la entrega en la issue #6 el 2026-03-25. `developer-teams` integro la rama en `main` y la elimino el 2026-03-26; `product-manager` cierra administrativamente la issue tras verificar esa integracion.

## HU-05 Hacer seguimiento de oportunidades en pipeline
- Backlog relacionado: PB-005
- Caso de uso relacionado: CU-05
- Issue relacionado: #7
- Historia:
  Como empresa o profesional TI,
  quiero guardar oportunidades y moverlas por estados,
  para gestionar mi trabajo de seguimiento y preparacion de ofertas.
- Alcance funcional acotado:
  - El pipeline del MVP es individual por usuario.
  - La colaboracion por empresa queda fuera de esta historia.
- Criterios de aceptacion:
  1. El usuario puede guardar una oportunidad en su pipeline.
  2. La oportunidad guardada entra en estado inicial `Nueva`.
  3. El usuario puede cambiarla a `Evaluando`, `Preparando oferta`, `Presentada` o `Descartada`.
  4. Una oportunidad no se duplica en el pipeline del mismo usuario.
  5. Si la oportunidad pasa a estado oficial `anulada`, `desierta` o `desistida`, el pipeline mantiene el registro del usuario y muestra una advertencia visible.
- Dependencias funcionales: PB-001, PB-002
- Prioridad: P1
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la issue #7 el 2026-03-31 y la issue fue cerrada administrativamente en GitHub el 2026-04-01.

## HU-06 Disponer de reglas auditables de relevancia TI
- Backlog relacionado: PB-006
- Caso de uso relacionado: CU-08
- Issue relacionado: #2
- Historia:
  Como responsable de producto y validacion,
  quiero tener reglas funcionales explicitas para clasificar oportunidades TI,
  para reducir ambiguedad, falsos positivos y discusiones durante desarrollo y QA.
- Criterios de aceptacion:
  1. Existe un documento funcional con criterios de inclusion y exclusion.
  2. Los criterios incluyen CPVs, palabras clave y casos frontera.
  3. `qa-teams` puede validar una muestra de ejemplos con esos criterios desde una superficie funcional verificable.
  4. El backlog y los issues hacen referencia a estas reglas.
- Dependencias funcionales: PB-007
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la nueva entrega de la issue #2 el 2026-03-18 y la rama `feat/pb-006-clasificacion-ti-auditable` ya se integro en `main`; queda cerrada administrativamente salvo reapertura por cambio de alcance.

## HU-07 Delimitar la cobertura inicial de fuentes
- Backlog relacionado: PB-007
- Caso de uso relacionado: CU-06
- Issue relacionado: #1
- Historia:
  Como responsable de producto,
  quiero definir las fuentes oficiales que entran en la primera release,
  para evitar expectativas no alineadas sobre cobertura y plazos.
- Criterios de aceptacion:
  1. Existe una lista priorizada de fuentes objetivo para MVP.
  2. Cada fuente tiene un estado de inclusion esperado.
  3. La lista esta alineada con backlog y roadmap.
  4. La entrega no comunica cobertura total cuando no existe.
- Dependencias funcionales: ninguna
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: validado previamente por `qa-teams` en la issue #1 e integrado en `main`; queda cerrado administrativamente salvo reapertura por cambio de alcance.

## HU-08 Medir cobertura y uso inicial del producto
- Backlog relacionado: PB-008
- Caso de uso relacionado: CU-07
- Issue relacionado: #8
- Historia:
  Como responsable de producto,
  quiero definir KPIs basicos desde las primeras releases,
  para evaluar si el producto esta aportando valor real.
- Criterios de aceptacion:
  1. Se define al menos un KPI de cobertura, uno de adopcion y uno de uso.
  2. Cada KPI tiene definicion, formula, umbral inicial y decision asociada.
  3. La definicion documental de KPIs puede revisarse aunque la instrumentacion completa aun no exista, siempre que se explicite la limitacion.
  4. El equipo puede revisar estos KPIs sin bloquear el MVP funcional.
- Dependencias funcionales: PB-001, PB-004
- Prioridad: P2
- Estado: `nuevo`

## HU-09 Priorizar recopilacion sobre fuentes reales oficiales
- Backlog relacionado: PB-009
- Caso de uso relacionado: CU-09
- Issue relacionado: #9
- Historia:
  Como responsable de producto,
  quiero priorizar que la recopilacion se haga sobre fuentes oficiales reales y verificables,
  para que el catalogo y las oportunidades futuras se apoyen cuanto antes en origenes creibles y utiles para negocio.
- Criterios de aceptacion:
  1. Existe una lista priorizada y ordenada de fuentes reales oficiales candidatas a integracion temprana.
  2. La prioridad incluye de forma explicita `BOC` (`https://www.gobiernodecanarias.org/boc/`), `BOP Las Palmas` (`https://www.boplaspalmas.net/nbop2/index.php`) y `BOE` (`https://www.boe.es/`) y las clasifica en olas de ejecucion.
  3. Se define el minimo funcional verificable que debe conservar cada oportunidad obtenida desde esas fuentes: origen oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
  4. El backlog, el roadmap y el refinamiento funcional reflejan que esta prioridad adelanta a alertas y pipeline y no implica por si sola ampliar la promesa comercial de cobertura.
  5. Existe una issue de GitHub ejecutable para `developer-teams` con criterios de aceptacion verificables.
- Dependencias funcionales: PB-007, PB-006
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la entrega integrada en `main` en la issue #9 el 2026-03-24. `developer-teams` dejo constancia de fusion y borrado de la rama tecnica ese mismo dia y `product-manager` cerro administrativamente la issue el 2026-03-25.

## HU-10 Navegar por la aplicacion con una estructura comun adaptable
- Backlog relacionado: PB-010
- Caso de uso relacionado: CU-10
- Issue relacionado: #10
- Historia:
  Como usuario de Licican,
  quiero disponer de una navegacion principal clara con menu lateral de iconos y comportamiento responsive,
  para moverme entre las opciones principales de la aplicacion sin perder contexto al cambiar el ancho de la ventana.
- Criterios de aceptacion:
  1. En anchos amplios la aplicacion muestra un menu lateral izquierdo persistente con iconos en vertical para las opciones principales.
  2. La opcion activa queda destacada de forma visible.
  3. El contenido principal se adapta al ancho disponible sin solaparse con la navegacion ni exigir scroll horizontal estructural.
  4. En anchos reducidos el usuario sigue accediendo a las opciones principales mediante una variante responsive coherente.
  5. Las opciones aun no disponibles no se presentan como funcionalidades operativas sin senalizar; si aparecen, quedan marcadas como `proximamente`.
  6. El rediseño no degrada la navegacion hacia catalogo, detalle, filtros ni alertas ya disponibles.
- Dependencias funcionales: PB-001, PB-002, PB-003
- Prioridad: P1
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la navegacion de la issue #10 y la entrega quedo integrada en `main`; `product-manager` la cerro administrativamente el 2026-03-30.

## HU-11 Consolidar licitaciones TI Canarias desde snapshots `.atom` versionados
- Backlog relacionado: PB-011
- Caso de uso relacionado: CU-11
- Issue relacionado: #11
- Historia:
  Como responsable de producto,
  quiero que la aplicacion tome todos los ficheros `.atom` disponibles en `data/` y consolide la version vigente de cada expediente TI de Canarias,
  para trabajar sobre una fuente operativa real aunque los snapshots cambien de nombre por fecha y hora.
- Criterios de aceptacion:
  1. La carga de datos toma todos los ficheros `.atom` presentes en `data/` sin depender de un nombre fijo.
  2. Solo se incluyen expedientes que cumplan simultaneamente filtro geografico Canarias y filtro TI por CPV segun las reglas estructuradas definidas.
  3. El filtro geografico usa como criterio principal `CountrySubentityCode` con prefijo `ES7` y como criterios complementarios `ParentLocatedParty` o `CountrySubentity` con `Canarias` o nombres de islas canarias.
  4. El filtro TI usa CPVs que empiecen por `72`, `48` o `302`.
  5. Si un expediente aparece repetido en varios `.atom`, la aplicacion conserva una unica version funcional con la informacion mas reciente disponible.
  6. Cada expediente consolidado conserva el nombre del fichero `.atom` origen de la version vigente.
- Dependencias funcionales: PB-009, PB-006
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la entrega en la issue #11 el 2026-03-27. `developer-teams` integro la rama en `main` y la elimino el 2026-03-28; `product-manager` cerro administrativamente la issue el mismo dia.

## HU-12 Consultar licitaciones, lotes y adjudicaciones con trazabilidad al fichero origen
- Backlog relacionado: PB-012
- Caso de uso relacionado: CU-12
- Issue relacionado: #12
- Historia:
  Como empresa o profesional TI,
  quiero consultar en la aplicacion las licitaciones, sus lotes y sus adjudicaciones con el mismo marco funcional del Excel de referencia y con visibilidad del fichero origen,
  para revisar la oportunidad sin perder trazabilidad del dato.
- Criterios de aceptacion:
  1. La aplicacion muestra una pestaña `Licitaciones TI Canarias`.
  2. La aplicacion muestra una pestaña `Detalle Lotes`.
  3. La aplicacion muestra una pestaña `Adjudicaciones`.
  4. El detalle de una licitacion o contrato muestra el nombre del fichero `.atom` de origen.
  5. La informacion visible para la muestra actual se corresponde funcionalmente con `data/licitaciones_ti_canarias.xlsx` en esas tres pestañas.
  6. Si un dato no viene informado en origen, la interfaz lo muestra como no informado o equivalente claro.
- Dependencias funcionales: PB-011, PB-002
- Prioridad: P0
- Estado: `cerrado`
- Nota de estado: `qa-teams` valido la reentrega de la issue #12 el 2026-03-29. `developer-teams` integro la rama en `main` y la elimino el 2026-03-30; `product-manager` reconcilia la historia como cerrada.

## HU-13 Gestionar acceso por rol a las acciones del sistema
- Backlog relacionado: PB-013
- Caso de uso relacionado: CU-13
- Issue relacionado: #13
- Historia:
  Como responsable de producto y operacion,
  quiero que las acciones del sistema se habiliten segun el rol del usuario,
  para proteger la gestion de alertas, pipeline y administracion sin degradar la experiencia de consulta.
- Criterios de aceptacion:
  1. Given un usuario con rol `Administrador`, When accede a la aplicacion, Then puede consultar licitaciones, gestionar alertas, consultar KPIs y administrar roles o permisos sobre las superficies ya disponibles.
  2. Given un usuario con rol `Manager`, When accede a la aplicacion, Then puede gestionar sus alertas propias y su pipeline propio dentro de las superficies ya disponibles.
  3. Given un usuario con rol `Colaborador`, When navega por catalogo, detalle, filtros o vistas consolidadas, Then puede consultar la informacion pero no crear ni editar entidades.
  4. Given un usuario con rol `Invitado`, When navega por catalogo, detalle, filtros o vistas consolidadas, Then puede consultar la informacion pero no crear ni editar entidades.
  5. Given que una superficie futura como pipeline aun no esta disponible, When se implementa esta primera iteracion de permisos, Then la matriz funcional deja preparada su extension sin bloquear la entrega actual.
  6. Given que un usuario intenta ejecutar una accion no permitida para su rol, When el sistema procesa la solicitud, Then la accion queda bloqueada de forma consistente y el control no se presenta como operativo.
- Dependencias funcionales: PB-010, PB-004
- Prioridad: P1
- Estado: `cerrado`
- Nota de estado: la issue #13 figura cerrada en GitHub desde el 2026-04-01 y esta historia queda reconciliada como entrega integrada.
- Nota de alcance: la primera iteracion de `PB-013` gobierna las superficies ya disponibles; las reglas de pipeline se aplicaran en la evolucion de `PB-005` sin redefinir la matriz de permisos.

## HU-14 Paginacion de resultados del catalogo
- Backlog relacionado: PB-014
- Caso de uso relacionado: CU-14
- Issue relacionado: #15
- Historia:
  Como empresa o profesional TI,
  quiero navegar el catalogo y la API en paginas,
  para revisar un volumen grande de licitaciones sin perder contexto ni rendimiento.
- Criterios de aceptacion:
  1. El catalogo HTML y la API JSON permiten navegar por paginas.
  2. El sistema muestra el total de resultados y el rango actualmente visible.
  3. El usuario puede avanzar, retroceder y saltar a una pagina concreta.
  4. La paginacion conserva los filtros activos y el orden de listado.
  5. Si la pagina solicitada es inexistente o invalida, el sistema responde con un comportamiento controlado y consistente.
- Dependencias funcionales: PB-001, PB-003
- Prioridad: P1
- Estado: `cerrado`
- Nota de estado: la issue #15 ya fue cerrada en GitHub y esta historia queda reconciliada como entrega integrada.

## HU-15 Configurar conservacion y archivado de licitaciones
- Backlog relacionado: PB-015
- Caso de uso relacionado: CU-15
- Issue relacionado: #16
- Historia:
  Como administrador u operador de datos,
  quiero configurar la antiguedad de conservacion y archivado de las licitaciones,
  para controlar cuanto tiempo permanecen activas en la base de datos antes de moverlas a archivo.
- Criterios de aceptacion:
  1. La vista de panel de control muestra la antiguedad configurada en dias.
  2. La politica puede expresarse como dias desde la creacion o como antiguedad de las licitaciones cerradas.
  3. Las licitaciones con seguimiento activo no se borran nunca.
  4. Las licitaciones cerradas que estuvieron activas se trasladan a una tabla `licitaciones archivadas`.
  5. La tabla archivada conserva los mismos datos que la tabla principal.
  6. El panel deja visible que registros se conservaran, archivaran o mantendran activos.
- Dependencias funcionales: issue #14 integrada en `main`, PB-005 cerrada administrativamente
- Prioridad: P1
- Estado: `nuevo`

## HU-16 Gestionar usuarios de plataforma
- Backlog relacionado: PB-016
- Caso de uso relacionado: CU-16
- Issue relacionado: #28
- Historia:
  Como administrador o manager con permisos suficientes,
  quiero poder gestionar cuentas de usuario, roles, permisos y accesos desde un unico modulo,
  para controlar de forma trazable quien puede operar en Licican y con que alcance.
- Alcance funcional acotado:
  - La gestion es sobre cuentas internas de la plataforma.
  - La baja logica reemplaza a la eliminacion fisica.
  - La gestion masiva queda fuera del MVP.
- Criterios de aceptacion:
  1. El modulo muestra un listado paginado de usuarios con nombre completo, email, rol principal, estado, ultimo acceso y acciones por fila.
  2. El usuario con permisos suficientes puede crear una cuenta con datos validos y verla reflejada en el listado y en el detalle.
  3. El sistema bloquea emails duplicados con un mensaje de error claro.
  4. El usuario con permisos suficientes puede editar datos basicos, cambiar el rol principal y actualizar el estado.
  5. El usuario con permisos suficientes puede activar, desactivar, reactivar o dar baja logica a una cuenta con confirmacion previa en acciones sensibles.
  6. El usuario con permisos suficientes puede reenviar invitacion a cuentas pendientes y reiniciar acceso o contraseña cuando corresponda.
  7. El detalle de usuario muestra estado actual, ultimo acceso e historial o trazabilidad de cambios.
  8. El sistema impide dejar la plataforma sin ningun administrador activo.
- Dependencias funcionales: PB-013, persistencia de usuarios, auditoria de cambios, autenticacion o contexto de sesion
- Prioridad: P2
- Estado: `nuevo`
