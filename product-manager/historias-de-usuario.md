# Historias de Usuario de PodencoTI

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
- Estado: `validado`
- Nota de estado: `qa-teams` valido la entrega en la issue #6 el 2026-03-25 sobre la rama `developer-teams/issue-6-pb-004-alertas-tempranas`. Queda pendiente de integracion en `main`, borrado de rama tecnica y cierre administrativo posterior por `product-manager`.

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
- Estado: `nuevo`

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
  Como usuario de PodencoTI,
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
- Estado: `nuevo`

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
- Estado: `nuevo`

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
- Estado: `nuevo`
