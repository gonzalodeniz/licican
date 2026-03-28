# Especificacion Funcional de Producto: Gestion y Seguimiento de Licitaciones

## Objetivo
Definir, en un unico artefacto, la estructura funcional de mayor a menor abstraccion para la aplicacion de gestion y seguimiento de licitaciones publicas de PodencoTI.

## Supuestos de alcance
- Este documento toma como base la vision y el backlog funcional ya vigentes en `product-manager/`.
- Las funcionalidades cubiertas son las actualmente trazadas en `PB-001` a `PB-013`.
- El modelo de permisos se define para tres roles de uso del producto: `Administrador`, `Colaborador` y `Lector/Invitado`.
- Cuando una capacidad ya exista en el backlog como decision funcional cerrada, aqui se consolida sin reabrir su definicion.

## 1. Epicas

### E-01 Descubrimiento y relevancia de oportunidades
Agrupa las capacidades necesarias para localizar, clasificar y consultar licitaciones TI relevantes desde una unica superficie funcional.

- Funcionalidades incluidas:
  - Cobertura inicial de fuentes
  - Reglas auditables de relevancia TI
  - Catalogo de oportunidades
  - Ficha de detalle
  - Filtros funcionales

### E-02 Ingestion operativa y trazabilidad del dato oficial
Agrupa las capacidades necesarias para cargar fuentes oficiales reales, consolidar snapshots versionados y exponer trazabilidad verificable al origen.

- Funcionalidades incluidas:
  - Priorizacion de fuentes oficiales reales
  - Consolidacion de ficheros `.atom`
  - Exposicion de licitaciones, lotes y adjudicaciones
  - Trazabilidad al fichero origen

### E-03 Retencion y seguimiento operativo del usuario
Agrupa las capacidades orientadas a convertir el descubrimiento en trabajo recurrente y gestionable por el usuario.

- Funcionalidades incluidas:
  - Alertas tempranas
  - Pipeline de seguimiento

### E-04 Experiencia transversal y gobierno del producto
Agrupa las capacidades de soporte necesarias para que el producto escale con consistencia y pueda evaluarse con datos.

- Funcionalidades incluidas:
  - Navegacion principal responsive
  - KPIs de producto
  - Modelo de roles y permisos

## 2. Hitos

### Hito 1. Fundacion funcional del catalogo
- Objetivo:
  - Dejar cerradas la cobertura inicial y la logica de relevancia TI para poder descubrir oportunidades con criterio verificable.
- Funcionalidades incluidas:
  - Cobertura inicial de fuentes
  - Reglas auditables de relevancia TI
  - Catalogo de oportunidades
  - Ficha de detalle
  - Filtros funcionales
- Definition of Done de alto nivel:
  - Existe una superficie funcional navegable donde el usuario puede descubrir, revisar y filtrar licitaciones TI.
  - La cobertura inicial esta documentada y no induce a pensar que existe cobertura total.
  - `qa-teams` puede validar relevancia TI, campos visibles y estados vacios de forma observable.

### Hito 2. Base operativa de dato oficial
- Objetivo:
  - Sustituir la dependencia de muestras aisladas por una base operativa consolidada desde fuentes oficiales reales y snapshots `.atom`.
- Funcionalidades incluidas:
  - Priorizacion de fuentes oficiales reales
  - Consolidacion de ficheros `.atom`
  - Exposicion de licitaciones, lotes y adjudicaciones
- Definition of Done de alto nivel:
  - La aplicacion absorbe todos los `.atom` presentes en `data/` sin depender de un nombre fijo.
  - El usuario puede consultar licitaciones, lotes y adjudicaciones con trazabilidad visible al origen.
  - `qa-teams` puede contrastar la salida funcional con el Excel de referencia y con el fichero `.atom` origen.

### Hito 3. Activacion y seguimiento del usuario
- Objetivo:
  - Permitir que el usuario convierta el descubrimiento en rutina y gestione oportunidades de forma persistente.
- Funcionalidades incluidas:
  - Alertas tempranas
  - Pipeline de seguimiento
- Definition of Done de alto nivel:
  - El usuario puede guardar criterios de interes persistentes sin crear alertas vacias.
  - El usuario puede guardar oportunidades en pipeline sin duplicados y moverlas por estados definidos.
  - Los estados oficiales no rompen la trazabilidad ni generan falsas oportunidades nuevas.

### Hito 4. Escalabilidad de experiencia y medicion
- Objetivo:
  - Asegurar una base de navegacion comun, un control minimo de permisos y una medicion funcional inicial.
- Funcionalidades incluidas:
  - Navegacion principal responsive
  - KPIs de producto
  - Modelo de roles y permisos
- Definition of Done de alto nivel:
  - La aplicacion mantiene una estructura comun usable en escritorio y movil.
  - Las acciones del sistema estan acotadas por rol de forma consistente.
  - Producto dispone de KPIs definidos para tomar decisiones posteriores sin bloquear las releases funcionales previas.

## 3. Historias de usuario

### HU-01 Delimitar cobertura inicial de fuentes
Como Product Manager, quiero definir las fuentes oficiales incluidas en la primera release para evitar expectativas de cobertura no alineadas.

- Criterios de aceptacion:
  - Given que existe un inventario preliminar de fuentes oficiales, When se revisa el alcance del MVP, Then cada fuente queda clasificada como `MVP`, `Posterior` o `Por definir`.
  - Given que una fuente no esta dentro del alcance del MVP, When se consulta la documentacion funcional, Then la fuente aparece como excluida o pendiente sin presentarse como disponible.
  - Given que se comunica la cobertura del producto, When se describe el alcance inicial, Then no se afirma cobertura total del ecosistema canario.

### HU-02 Definir reglas auditables de relevancia TI
Como Product Manager o QA, quiero disponer de reglas funcionales auditables de relevancia TI para reducir falsos positivos y validar el catalogo con criterios consistentes.

- Criterios de aceptacion:
  - Given que se revisa la clasificacion de oportunidades, When se consulta la definicion funcional, Then existen criterios de inclusion, exclusion y casos frontera.
  - Given una oportunidad con CPV o descripcion ambigua, When se evalua con la regla vigente, Then el resultado queda identificado como inclusion, exclusion o caso frontera.
  - Given que `qa-teams` necesita validar la relevancia, When accede a la superficie funcional definida, Then puede contrastar ejemplos representativos con la clasificacion esperada.

### HU-03 Consultar catalogo de licitaciones TI
Como empresa o profesional TI, quiero ver en un catalogo unificado las oportunidades relevantes para detectar licitaciones a tiempo sin revisar multiples portales.

- Criterios de aceptacion:
  - Given que existen oportunidades TI disponibles, When el usuario accede al catalogo, Then el sistema muestra solo oportunidades clasificadas como TI dentro de la cobertura vigente.
  - Given que una oportunidad tiene datos basicos disponibles, When se muestra en el listado, Then se ven al menos titulo, organismo, ubicacion, presupuesto si existe, fecha limite y estado oficial si la fuente lo informa.
  - Given que no hay resultados disponibles, When el usuario entra al catalogo, Then el sistema muestra un estado vacio claro y comprensible.

### HU-04 Revisar el detalle de una licitacion
Como empresa o profesional TI, quiero consultar la ficha resumida de una licitacion para decidir rapidamente si merece seguimiento.

- Criterios de aceptacion:
  - Given que el usuario selecciona una oportunidad del catalogo, When accede al detalle, Then el sistema muestra presupuesto, procedimiento, fecha limite, organismo convocante y enlace a la fuente oficial cuando existan.
  - Given que algun dato no esta disponible en origen, When se carga la ficha, Then el sistema lo muestra como `no informado` o equivalente claro.
  - Given que el expediente ha sido rectificado o modificado, When se consulta la ficha, Then se muestra el ultimo dato oficial visible del mismo expediente.

### HU-05 Filtrar oportunidades relevantes
Como empresa o profesional TI, quiero filtrar las licitaciones por criterios de negocio para quedarme solo con las que encajan con mi capacidad y estrategia.

- Criterios de aceptacion:
  - Given que el usuario introduce una palabra clave o selecciona filtros, When aplica la busqueda, Then el listado se actualiza segun los criterios activos.
  - Given que existen filtros activos, When el usuario visualiza el resultado, Then el sistema muestra de forma visible los filtros aplicados y permite limpiarlos.
  - Given que el usuario informa un rango de presupuesto invalido, When intenta aplicar el filtro, Then el sistema solicita corregirlo y no interpreta ese caso como una busqueda valida sin resultados.

### HU-06 Priorizar recopilacion desde fuentes oficiales reales
Como Product Manager, quiero priorizar la recopilacion sobre fuentes oficiales reales y verificables para reforzar la credibilidad del dato visible en producto.

- Criterios de aceptacion:
  - Given que se revisa la prioridad de recopilacion, When se documenta la siguiente iteracion, Then `BOC`, `BOP Las Palmas` y `BOE` quedan identificadas de forma explicita y ordenadas por olas.
  - Given que una oportunidad procede de una fuente real priorizada, When se expone funcionalmente, Then conserva como minimo fuente oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
  - Given que se priorizan estas fuentes, When se actualiza roadmap y backlog, Then queda claro que esta prioridad antecede a nuevas capacidades de retencion no esenciales.

### HU-07 Consolidar snapshots `.atom`
Como responsable de producto, quiero que la aplicacion consolide todos los ficheros `.atom` presentes en `data/` para trabajar sobre una base operativa vigente aunque cambie el nombre de los snapshots.

- Criterios de aceptacion:
  - Given que existen varios ficheros `.atom` en `data/`, When se ejecuta la carga funcional, Then se toman todos los ficheros presentes sin depender de un nombre fijo.
  - Given que un mismo expediente aparece en varios snapshots, When el sistema consolida la informacion, Then conserva una unica version funcional con el dato mas reciente disponible.
  - Given que un expediente consolidado queda visible, When se consulta su informacion, Then se conserva el nombre del fichero `.atom` origen de la version vigente.

### HU-08 Consultar licitaciones, lotes y adjudicaciones
Como empresa o profesional TI, quiero consultar licitaciones, lotes y adjudicaciones con trazabilidad al origen para revisar la oportunidad sin perder contexto del dato oficial.

- Criterios de aceptacion:
  - Given que el usuario entra en la aplicacion, When navega al modulo de datos consolidados, Then existen las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
  - Given que se consulta una licitacion o contrato, When se abre su detalle, Then se muestra el nombre del fichero `.atom` origen.
  - Given que la muestra funcional esta disponible, When `qa-teams` la contrasta, Then la informacion visible se corresponde funcionalmente con `data/licitaciones_ti_canarias.xlsx` para las tres pestañas definidas.

### HU-09 Configurar alertas tempranas
Como empresa o profesional TI, quiero crear alertas con criterios de interes para enterarme antes de nuevas oportunidades relevantes.

- Criterios de aceptacion:
  - Given que el usuario informa al menos un criterio funcional, When guarda una alerta, Then el sistema la registra como activa.
  - Given que el usuario intenta guardar una alerta vacia, When confirma el alta, Then el sistema bloquea el guardado y solicita completar al menos un criterio.
  - Given que aparecen nuevas oportunidades compatibles, When el sistema las evalua, Then las asocia a la alerta y no trata como nuevas accionables las oportunidades con estado oficial `anulada`, `desierta` o `desistida`.

### HU-10 Gestionar pipeline de seguimiento
Como empresa o profesional TI, quiero guardar oportunidades y moverlas por estados para gestionar mi proceso comercial y de preparacion de oferta.

- Criterios de aceptacion:
  - Given que el usuario guarda una oportunidad por primera vez, When se anade al pipeline, Then entra en estado inicial `Nueva`.
  - Given que la oportunidad ya estaba guardada en el pipeline del mismo usuario, When intenta volver a guardarla, Then el sistema evita duplicados.
  - Given que la oportunidad cambia a estado oficial `anulada`, `desierta` o `desistida`, When el usuario la consulta en su pipeline, Then el sistema conserva el registro y muestra una advertencia visible.

### HU-11 Navegar por la aplicacion con estructura comun
Como usuario de PodencoTI, quiero disponer de una navegacion principal clara y responsive para moverme entre modulos sin perder contexto.

- Criterios de aceptacion:
  - Given que el usuario accede desde un ancho amplio, When se carga la aplicacion, Then se muestra una navegacion lateral persistente con la opcion activa destacada.
  - Given que el usuario accede desde un ancho reducido, When navega por la aplicacion, Then mantiene acceso util a las opciones principales mediante una variante responsive coherente.
  - Given que existen modulos no disponibles, When aparecen en navegacion, Then quedan claramente marcados como `proximamente` y no como funcionalidad operativa.

### HU-12 Medir valor inicial del producto
Como Product Manager, quiero definir KPIs de cobertura, adopcion y uso para tomar decisiones de priorizacion posteriores con evidencia.

- Criterios de aceptacion:
  - Given que se revisa el rendimiento inicial del producto, When se consulta la documentacion de metricas, Then existe al menos un KPI de cobertura, uno de adopcion y uno de uso.
  - Given que cada KPI esta definido, When producto lo revisa, Then dispone de formula, umbral inicial y decision asociada.
  - Given que aun no existe toda la instrumentacion tecnica, When se documentan los KPIs, Then la limitacion queda explicita sin bloquear la salida funcional del MVP.

### HU-13 Gestionar acceso por rol a las acciones del sistema
Como responsable de producto y operacion, quiero que las acciones del sistema se habiliten segun el rol del usuario para proteger la gestion y mantener una experiencia coherente de consulta.

- Criterios de aceptacion:
  - Given un usuario con rol `Administrador`, When accede a la aplicacion, Then puede consultar licitaciones, gestionar alertas, gestionar pipeline, consultar KPIs y administrar roles o permisos.
  - Given un usuario con rol `Colaborador`, When accede a sus superficies de trabajo, Then puede gestionar solo sus alertas y su pipeline propio sin acceder a administracion global.
  - Given un usuario con rol `Lector/Invitado`, When navega por catalogo, detalle, filtros o vistas consolidadas, Then puede consultar la informacion pero no crear ni editar entidades.
  - Given que un usuario intenta ejecutar una accion no permitida para su rol, When el sistema procesa la solicitud, Then la accion queda bloqueada de forma consistente y el control no se presenta como operativo.

## 4. Casos de uso

### CU-01 Descubrir licitaciones TI en el catalogo
- Actor principal:
  - Usuario registrado o lector con acceso a consulta.
- Objetivo:
  - Identificar oportunidades TI relevantes desde una unica vista.
- Precondiciones:
  - Existe cobertura funcional vigente.
  - Las oportunidades ya han sido clasificadas segun las reglas TI.
- Disparador:
  - El usuario accede al catalogo principal.
- Happy path:
  1. El usuario abre el modulo de catalogo.
  2. El sistema muestra las licitaciones TI visibles.
  3. El usuario revisa los datos basicos del listado.
  4. El usuario selecciona una oportunidad para profundizar.
- Flujo alternativo o error:
  - Si no existen oportunidades disponibles, el sistema muestra un estado vacio explicativo y no presenta un error tecnico como si fuera ausencia de permisos.
- Postcondiciones:
  - El usuario identifica una o varias oportunidades candidatas.

### CU-02 Revisar detalle de una licitacion
- Actor principal:
  - Usuario registrado o lector con acceso a consulta.
- Objetivo:
  - Evaluar si la licitacion merece seguimiento.
- Precondiciones:
  - La oportunidad existe y es accesible desde catalogo, alerta o vista consolidada.
- Disparador:
  - El usuario pulsa sobre una oportunidad.
- Happy path:
  1. El usuario accede al detalle.
  2. El sistema muestra datos criticos, estado oficial y enlace a la fuente.
  3. El usuario revisa informacion relevante para decidir si continuar.
- Flujo alternativo o error:
  - Si un dato critico no esta informado por la fuente, el sistema mantiene el detalle disponible y marca ese dato como no informado.
- Postcondiciones:
  - El usuario dispone de informacion suficiente para una decision inicial.

### CU-03 Filtrar licitaciones por criterios de negocio
- Actor principal:
  - Usuario registrado o lector con acceso a consulta.
- Objetivo:
  - Reducir ruido en el listado de oportunidades.
- Precondiciones:
  - El catalogo esta disponible.
- Disparador:
  - El usuario aplica filtros desde la interfaz.
- Happy path:
  1. El usuario informa palabra clave, rango de presupuesto, procedimiento o ubicacion.
  2. El sistema recalcula el listado.
  3. El usuario revisa el subconjunto resultante.
  4. El usuario limpia o ajusta filtros segun necesidad.
- Flujo alternativo o error:
  - Si el rango de presupuesto es invalido, el sistema lo rechaza y pide correccion antes de ejecutar la busqueda.
- Postcondiciones:
  - El usuario obtiene una vista filtrada consistente.

### CU-04 Configurar y mantener alertas
- Actor principal:
  - Administrador o colaborador.
- Objetivo:
  - Guardar criterios persistentes de interes para detectar nuevas oportunidades.
- Precondiciones:
  - El usuario tiene sesion iniciada y permisos de gestion.
  - Existen criterios funcionales reutilizables desde el catalogo.
- Disparador:
  - El usuario decide crear o editar una alerta.
- Happy path:
  1. El usuario abre la gestion de alertas.
  2. Introduce uno o varios criterios.
  3. Guarda la alerta.
  4. El sistema la deja activa y visible.
  5. Cuando aparecen coincidencias nuevas, el sistema las asocia internamente a la alerta.
- Flujo alternativo o error:
  - Si el usuario intenta guardar la alerta sin criterios, el sistema bloquea la accion e informa que debe completar al menos un criterio.
- Postcondiciones:
  - Existe una alerta activa, editable o desactivable.

### CU-05 Gestionar pipeline de oportunidades
- Actor principal:
  - Administrador o colaborador.
- Objetivo:
  - Hacer seguimiento individual de oportunidades guardadas.
- Precondiciones:
  - La oportunidad existe y es visible.
- Disparador:
  - El usuario decide guardar o actualizar una oportunidad en su pipeline.
- Happy path:
  1. El usuario guarda una oportunidad.
  2. El sistema la crea en estado `Nueva`.
  3. El usuario cambia el estado segun su proceso.
  4. El sistema conserva el historico operativo visible.
- Flujo alternativo o error:
  - Si la oportunidad ya existe en el pipeline del mismo usuario, el sistema evita duplicarla y redirige al registro existente.
- Postcondiciones:
  - La oportunidad queda gestionada en el pipeline del usuario.

### CU-06 Priorizar y gobernar fuentes oficiales reales
- Actor principal:
  - Product Manager o administrador funcional.
- Objetivo:
  - Decidir que fuentes reales deben entrar primero en recopilacion.
- Precondiciones:
  - Existe cobertura funcional inicial.
- Disparador:
  - Se abre una nueva iteracion de priorizacion de dato oficial.
- Happy path:
  1. El actor revisa fuentes oficiales candidatas.
  2. Las ordena por olas segun valor de negocio y verificabilidad.
  3. Registra la prioridad y el minimo funcional exigible por oportunidad.
  4. El backlog y roadmap se actualizan con esa prioridad.
- Flujo alternativo o error:
  - Si una fuente es oficial pero su formato o acceso no es estable, queda priorizada para analisis incremental en lugar de tratarse como fuente operativa inmediata.
- Postcondiciones:
  - Existe una prioridad ejecutable y trazable de fuentes reales.

### CU-07 Consolidar snapshots `.atom`
- Actor principal:
  - Sistema.
- Objetivo:
  - Construir una base vigente y no duplicada de expedientes TI Canarias.
- Precondiciones:
  - Existen varios ficheros `.atom` en `data/`.
  - La regla geografica y la regla TI estan definidas.
- Disparador:
  - Se ejecuta la carga o actualizacion de datos.
- Happy path:
  1. El sistema detecta todos los `.atom` presentes.
  2. Aplica los filtros geograficos y TI definidos.
  3. Identifica duplicados funcionales del mismo expediente.
  4. Conserva la version mas reciente.
  5. Registra el fichero `.atom` origen de la version vigente.
- Flujo alternativo o error:
  - Si un snapshot no aporta campos suficientes para reemplazar otro mas reciente, el sistema conserva la mejor version disponible sin duplicar el expediente.
- Postcondiciones:
  - Existe una base consolidada y trazable de expedientes.

### CU-08 Consultar licitaciones, lotes y adjudicaciones consolidadas
- Actor principal:
  - Usuario registrado o lector con acceso a consulta.
- Objetivo:
  - Revisar la informacion consolidada en vistas funcionales contrastables.
- Precondiciones:
  - La base consolidada ya esta disponible.
- Disparador:
  - El usuario entra en el modulo de datos consolidados.
- Happy path:
  1. El usuario accede a las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
  2. El sistema muestra la informacion correspondiente.
  3. El usuario abre el detalle de una licitacion o contrato.
  4. El sistema muestra el fichero origen.
- Flujo alternativo o error:
  - Si un campo no viene informado en origen, el sistema mantiene la fila o detalle y lo marca como no informado en lugar de ocultarlo.
- Postcondiciones:
  - El usuario puede revisar el dato consolidado con trazabilidad funcional.

### CU-09 Navegar entre modulos principales
- Actor principal:
  - Cualquier usuario con acceso al producto.
- Objetivo:
  - Moverse por los modulos principales sin perdida de contexto.
- Precondiciones:
  - Existe una estructura comun de navegacion.
- Disparador:
  - El usuario carga cualquier pantalla principal.
- Happy path:
  1. El sistema muestra la navegacion principal.
  2. El usuario selecciona un modulo.
  3. La opcion activa queda destacada.
  4. El contenido principal se adapta al espacio disponible.
- Flujo alternativo o error:
  - Si el ancho de pantalla es reducido, el sistema cambia a una variante responsive sin ocultar el acceso a los modulos principales.
- Postcondiciones:
  - El usuario mantiene navegacion consistente en diferentes anchos de pantalla.

### CU-10 Revisar indicadores de producto
- Actor principal:
  - Product Manager o administrador.
- Objetivo:
  - Tomar decisiones posteriores apoyadas en indicadores.
- Precondiciones:
  - Existen KPIs definidos y al menos una release evaluable.
- Disparador:
  - Se revisa el avance de producto.
- Happy path:
  1. El actor consulta los KPIs definidos.
  2. Revisa valores, umbrales y decisiones asociadas.
  3. Ajusta roadmap o backlog segun el resultado.
- Flujo alternativo o error:
  - Si un KPI todavia no puede medirse, el sistema o la documentacion explicita la limitacion y la accion necesaria para habilitarlo.
- Postcondiciones:
  - Existe una decision trazable basada en indicadores o en la ausencia justificada de medicion.

### CU-13 Aplicar permisos segun rol en consulta y gestion
- Actor principal:
  - Usuario autenticado o invitado segun el rol asignado.
- Objetivo:
  - Garantizar que cada rol ve y ejecuta solo las acciones que le corresponden.
- Precondiciones:
  - Existe un rol funcional asignado o inferido para el usuario actual.
  - El producto ya dispone de acciones visibles de consulta, alertas, pipeline o administracion.
- Disparador:
  - El usuario accede a una vista o accion del producto.
- Happy path:
  1. El usuario accede a una vista o accion del producto.
  2. El sistema identifica su rol.
  3. El sistema muestra solo las acciones permitidas.
  4. El usuario ejecuta una accion autorizada.
  5. El sistema procesa la accion manteniendo la restriccion de permisos.
- Flujo alternativo o error:
  - Si el usuario intenta ejecutar una accion no permitida, el sistema la bloquea y no la presenta como operativa.
- Postcondiciones:
  - El usuario opera dentro del alcance permitido para su rol.

## 5. Reglas de negocio

### Reglas de cobertura y relevancia
- RB-01 Solo deben mostrarse oportunidades clasificadas como TI segun la regla funcional vigente.
- RB-02 La cobertura inicial debe comunicarse como cobertura priorizada, no como cobertura total.
- RB-03 Toda fuente incluida en el MVP debe quedar clasificada como `MVP`, `Posterior` o `Por definir`.
- RB-04 Los expedientes mixtos solo se consideran TI cuando la parte tecnologica es sustancial o indispensable para el objeto del contrato.
- RB-05 Los casos frontera deben permanecer identificados como tales y no tratarse como inclusion inequivoca.

### Reglas de dato oficial y trazabilidad
- RB-06 Toda oportunidad visible debe conservar referencia a la fuente oficial.
- RB-07 Toda oportunidad recopilada desde fuentes reales priorizadas debe conservar enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
- RB-08 La consolidacion de `.atom` debe tomar todos los ficheros presentes en `data/` sin depender de un nombre fijo.
- RB-09 Si un expediente aparece repetido en varios snapshots, debe existir una unica version funcional vigente.
- RB-10 El detalle de una licitacion o contrato debe mostrar el nombre del fichero `.atom` origen de la version consolidada.
- RB-11 La salida funcional visible de licitaciones, lotes y adjudicaciones debe poder contrastarse con `data/licitaciones_ti_canarias.xlsx`.

### Reglas de consulta y filtrado
- RB-12 Si un dato no existe en origen, el sistema debe mostrarlo como no informado o equivalente claro.
- RB-13 La fecha limite debe mostrarse con prioridad en la ficha de detalle cuando exista.
- RB-14 Los filtros activos deben permanecer visibles y poder limpiarse.
- RB-15 Un rango de presupuesto invalido debe rechazarse como error de validacion, no como busqueda sin resultados.

### Reglas de alertas y pipeline
- RB-16 Una alerta no puede guardarse vacia; debe contener al menos un criterio funcional.
- RB-17 Las alertas del MVP pueden registrar coincidencias internas aunque la notificacion saliente quede fuera de alcance.
- RB-18 Una oportunidad con estado oficial `anulada`, `desierta` o `desistida` no debe tratarse como nueva coincidencia accionable.
- RB-19 El pipeline MVP es individual por usuario; la colaboracion compartida queda fuera de alcance.
- RB-20 El alta inicial en pipeline crea obligatoriamente el estado `Nueva`.
- RB-21 Una misma oportunidad no puede duplicarse en el pipeline del mismo usuario.
- RB-22 Si el estado oficial del expediente cambia a `anulada`, `desierta` o `desistida`, el pipeline conserva el historico del usuario y muestra advertencia visible.

### Reglas de experiencia y gobierno
- RB-23 La navegacion principal debe mantener una variante usable en escritorio y en anchos reducidos.
- RB-24 Las opciones no disponibles no pueden mostrarse como operativas sin senalizacion explicita.
- RB-25 Deben existir KPIs minimos de cobertura, adopcion y uso, aunque su medicion completa se habilite en una iteracion posterior.
- RB-26 El modelo de permisos debe impedir a `Lector/Invitado` crear o modificar entidades.

## 6. Modelo de roles y permisos

| Accion del sistema | Administrador | Colaborador | Lector/Invitado | Nota |
|---|---|---|---|---|
| Acceder al catalogo de licitaciones | ✅ | ✅ | ✅ | Consulta basica permitida para todos los roles definidos. |
| Ver detalle de una licitacion | ✅ | ✅ | ✅ | Incluye consulta de campos visibles y origen oficial expuesto. |
| Filtrar licitaciones | ✅ | ✅ | ✅ | No altera datos del sistema. |
| Consultar licitaciones, lotes y adjudicaciones consolidadas | ✅ | ✅ | ✅ | Consulta de vistas funcionales consolidadas. |
| Ver fichero `.atom` origen en detalle | ✅ | ✅ | ✅ | Visible como metadato de trazabilidad, no como capacidad de administracion tecnica. |
| Crear alerta | ✅ | ✅ | ❌ | Requiere sesion y capacidad de gestion personal. |
| Editar alerta propia | ✅ | ✅ | ❌ | Limitado a alertas del propio usuario para colaboradores. |
| Desactivar alerta propia | ✅ | ✅ | ❌ | Limitado a alertas del propio usuario para colaboradores. |
| Editar alertas de otros usuarios | ✅ | ❌ | ❌ | Solo administracion global. |
| Guardar oportunidad en pipeline | ✅ | ✅ | ❌ | Requiere sesion y espacio personal de trabajo. |
| Cambiar estado de oportunidad en pipeline propio | ✅ | ✅ | ❌ | Limitado a registros propios para colaboradores. |
| Ver pipeline propio | ✅ | ✅ | ❌ | Requiere sesion. |
| Ver pipeline de otros usuarios | ✅ | ❌ | ❌ | Solo administracion global si el producto lo habilita. |
| Configurar fuentes oficiales priorizadas | ✅ | ❌ | ❌ | Capacidad funcional de gobierno del producto. |
| Ajustar reglas de relevancia TI | ✅ | ❌ | ❌ | Cambio de gobierno funcional con impacto transversal. |
| Consultar KPIs de producto | ✅ | ⚠️ | ❌ | Permitido a colaborador solo si se habilita vista operativa sin datos sensibles de negocio. |
| Gestionar roles y permisos | ✅ | ❌ | ❌ | Solo administracion. |
| Ver modulos marcados como `proximamente` | ✅ | ✅ | ✅ | Visibilidad permitida, uso operativo no disponible. |

## 7. Trazabilidad resumida con backlog vigente

| Epica | Historias relacionadas | Backlog relacionado |
|---|---|---|
| E-01 Descubrimiento y relevancia de oportunidades | HU-01, HU-02, HU-03, HU-04, HU-05 | PB-007, PB-006, PB-001, PB-002, PB-003 |
| E-02 Ingestion operativa y trazabilidad del dato oficial | HU-06, HU-07, HU-08 | PB-009, PB-011, PB-012 |
| E-03 Retencion y seguimiento operativo del usuario | HU-09, HU-10 | PB-004, PB-005 |
| E-04 Experiencia transversal y gobierno del producto | HU-10, HU-08, HU-13 | PB-010, PB-008, PB-013 |

## 8. Criterio de uso de este artefacto
- Este documento sirve como referencia ejecutiva para ordenar el alcance de mayor a menor abstraccion.
- Las historias, casos de uso y reglas aqui consolidadas deben mantenerse sincronizadas con `product-backlog.md`, `historias-de-usuario.md`, `casos-de-uso.md` y `roadmap.md`.
- Si una decision de producto cambia, este documento debe actualizarse junto con los artefactos funcionales que referencia.
