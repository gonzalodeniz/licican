# Casos de Uso de Licican

## Convenciones de trazabilidad
- Cada caso de uso referencia backlog e historias relacionadas.
- Las reglas de negocio `RB-*` sirven como base de verificacion funcional para `qa-teams`.

## CU-01 Consultar catalogo de oportunidades TI
- Backlog relacionado: PB-001
- Historias relacionadas: HU-01
- Actor principal: Usuario registrado de Licican.
- Objetivo: Descubrir en un solo lugar oportunidades de contratacion publica TI relevantes en Canarias.
- Disparador: El usuario accede al modulo principal de oportunidades.
- Precondiciones:
  - Existen oportunidades disponibles en el catalogo.
  - Las oportunidades han sido clasificadas como TI segun las reglas funcionales vigentes.
  - La cobertura funcional MVP ya ha sido delimitada.
- Flujo principal:
  1. El usuario abre el catalogo de oportunidades.
  2. El sistema muestra un listado de oportunidades TI ordenadas por actualidad o relevancia.
  3. El usuario visualiza informacion basica de cada oportunidad.
  4. El usuario selecciona una oportunidad para ver mas detalle.
- Flujos alternativos:
  - A1. Si no hay oportunidades disponibles, el sistema muestra un estado vacio explicando la situacion.
  - A2. Si una oportunidad carece de algun dato no obligatorio, el sistema lo indica sin ocultar el resto de informacion disponible.
  - A3. Si la fuente informa que la oportunidad esta anulada, desierta o desistida, el sistema mantiene la referencia visible con su estado oficial y no la presenta como nueva activa.
- Postcondiciones:
  - El usuario ha identificado una o varias oportunidades potencialmente relevantes.
- Reglas de negocio relacionadas:
  - RB-01 Solo deben mostrarse oportunidades clasificadas como TI.
  - RB-02 Cada oportunidad debe conservar referencia a la fuente oficial.
  - RB-03 Solo deben aparecer oportunidades cuya fuente este dentro del alcance funcional vigente.
  - RB-20 El estado oficial del expediente debe mostrarse cuando la fuente lo informe.

## CU-02 Revisar el detalle de una licitacion
- Backlog relacionado: PB-002
- Historias relacionadas: HU-02
- Actor principal: Usuario registrado de Licican.
- Objetivo: Evaluar rapidamente si una licitacion merece seguimiento.
- Disparador: El usuario selecciona una oportunidad desde el listado o una alerta.
- Precondiciones:
  - La oportunidad existe en el catalogo.
- Flujo principal:
  1. El usuario accede al detalle de la oportunidad.
  2. El sistema muestra los datos criticos disponibles.
  3. El usuario revisa presupuesto, fecha limite, procedimiento y requisitos relevantes.
  4. El usuario decide si guardar o descartar la oportunidad.
- Flujos alternativos:
  - A1. Si algun dato critico no esta disponible en origen, el sistema lo marca como no informado.
  - A2. Si la fuente oficial no es accesible temporalmente, el sistema mantiene el ultimo resumen estructurado disponible e informa de ello.
  - A3. Si la fuente publica una modificacion o rectificacion del mismo expediente, el sistema mantiene la referencia funcional y muestra el ultimo dato oficial disponible.
- Postcondiciones:
  - El usuario dispone de informacion suficiente para una decision inicial.
- Reglas de negocio relacionadas:
  - RB-04 La fecha limite debe ser visible de forma prioritaria.
  - RB-05 El enlace a la fuente oficial debe estar disponible siempre que exista.
  - RB-21 La ficha debe reflejar el ultimo estado y la ultima fecha oficial visible del expediente cuando existan rectificaciones.

## CU-03 Filtrar oportunidades
- Backlog relacionado: PB-003
- Historias relacionadas: HU-03
- Actor principal: Usuario registrado de Licican.
- Objetivo: Reducir el ruido y quedarse con oportunidades que encajan con su perfil comercial o tecnico.
- Disparador: El usuario aplica uno o varios filtros sobre el catalogo.
- Precondiciones:
  - El catalogo de oportunidades esta disponible.
- Flujo principal:
  1. El usuario selecciona criterios de filtrado.
  2. El sistema actualiza el listado segun los criterios activos.
  3. El usuario revisa los resultados filtrados.
  4. El usuario modifica o limpia filtros cuando lo necesita.
- Flujos alternativos:
  - A1. Si ningun resultado cumple los criterios, el sistema muestra un estado vacio y permite limpiar filtros.
  - A2. Si el usuario aplica un rango de presupuesto invalido, el sistema solicita corregirlo.
- Postcondiciones:
  - El usuario dispone de un subconjunto relevante de oportunidades.
- Reglas de negocio relacionadas:
  - RB-06 Los filtros activos deben quedar visibles.
  - RB-07 La limpieza de filtros debe restaurar el listado completo disponible.

## CU-04 Configurar alertas tempranas
- Backlog relacionado: PB-004
- Historias relacionadas: HU-04
- Actor principal: Usuario registrado de Licican.
- Objetivo: Recibir nuevas oportunidades sin tener que revisar manualmente todas las fuentes.
- Disparador: El usuario decide crear una alerta.
- Precondiciones:
  - El usuario tiene acceso a la gestion de alertas.
  - El catalogo y los criterios de filtrado ya estan disponibles.
- Flujo principal:
  1. El usuario crea una alerta con criterios funcionales.
  2. El sistema confirma que la alerta queda activa.
  3. Cuando aparecen nuevas oportunidades compatibles, el sistema registra la coincidencia y la asocia a la alerta.
  4. El usuario consulta o modifica la alerta cuando lo necesita.
- Flujos alternativos:
  - A1. Si el usuario intenta guardar una alerta sin criterios minimos, el sistema solicita completarlos y no guarda una alerta vacia.
  - A2. Si existen varias alertas solapadas, el sistema permite mantenerlas sin duplicar el mensaje de configuracion.
  - A3. Si una oportunidad compatible pasa a estado oficial `anulada`, `desierta` o `desistida`, deja de tratarse como coincidencia nueva accionable.
- Postcondiciones:
  - El usuario dispone de al menos una alerta activa.
- Reglas de negocio relacionadas:
  - RB-08 Una alerta puede activarse, editarse o desactivarse.
  - RB-09 La configuracion de alertas debe reutilizar los mismos criterios funcionales que el filtrado del catalogo.
  - RB-16 En el MVP la alerta debe registrar coincidencias funcionales aunque no exista todavia notificacion saliente.
  - RB-22 Una oportunidad cerrada oficialmente no debe generar una nueva alerta accionable.
  - RB-24 Una alerta no puede guardarse vacia; debe incluir al menos un criterio funcional informado.

## CU-05 Gestionar pipeline de oportunidades
- Backlog relacionado: PB-005
- Historias relacionadas: HU-05
- Actor principal: Usuario registrado de Licican.
- Objetivo: Hacer seguimiento del estado de trabajo de cada licitacion relevante.
- Disparador: El usuario decide guardar una oportunidad en su pipeline.
- Precondiciones:
  - La oportunidad existe y es visible para el usuario.
  - El alcance del pipeline MVP es individual por usuario.
- Flujo principal:
  1. El usuario guarda una oportunidad en su pipeline.
  2. El sistema la asigna al estado inicial `Nueva`.
  3. El usuario cambia el estado segun avanza su proceso interno.
  4. El usuario consulta el pipeline para conocer el estado de sus oportunidades.
- Flujos alternativos:
  - A1. Si la oportunidad ya estaba guardada, el sistema evita duplicados y permite actualizar su estado.
  - A2. Si el usuario decide descartarla, el sistema conserva el registro en estado `Descartada`.
  - A3. Si la oportunidad pasa a `anulada`, `desierta` o `desistida`, el sistema conserva el estado de trabajo del usuario y muestra el estado oficial como advertencia visible.
- Postcondiciones:
  - La oportunidad queda gestionada en el pipeline del usuario.
- Reglas de negocio relacionadas:
  - RB-10 Los estados minimos del pipeline son `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
  - RB-11 Una misma oportunidad no debe duplicarse en el pipeline del mismo usuario.
  - RB-17 La primera release del pipeline no incluye colaboracion compartida por empresa.
  - RB-23 El estado oficial del expediente no elimina el historico del pipeline del usuario.
  - RB-25 El alta inicial de una oportunidad en pipeline debe crearla en estado `Nueva`.

## CU-06 Delimitar cobertura funcional inicial
- Backlog relacionado: PB-007
- Historias relacionadas: HU-07
- Actor principal: Responsable de producto.
- Objetivo: Definir que fuentes oficiales entran en el MVP y cuales quedan fuera o pendientes.
- Disparador: Se prepara la release funcional inicial del producto.
- Precondiciones:
  - La vision del producto esta vigente.
  - Existe un inventario preliminar de fuentes oficiales canarias.
- Flujo principal:
  1. El responsable de producto revisa las fuentes oficiales candidatas.
  2. Clasifica cada fuente como `MVP`, `Posterior` o `Por definir`.
  3. Registra la decision y su justificacion funcional.
  4. La cobertura resultante se refleja de forma visible y verificable en producto y documentacion.
- Flujos alternativos:
  - A1. Si una fuente tiene acceso inconsistente o formato no estandar, se clasifica como `Por definir` hasta nuevo refinamiento.
  - A2. Si una fuente no aporta oportunidades TI con frecuencia razonable, puede quedar para una fase posterior.
- Postcondiciones:
  - La cobertura MVP queda acotada y verificable por desarrollo y QA.
- Reglas de negocio relacionadas:
  - RB-12 La primera release no debe presentarse como cobertura total del ecosistema canario.
  - RB-13 Toda fuente incluida debe conservar justificacion funcional y trazabilidad.

## CU-07 Revisar indicadores iniciales de producto
- Backlog relacionado: PB-008
- Historias relacionadas: HU-08
- Actor principal: Responsable de producto.
- Objetivo: Medir si el MVP esta aportando valor real y orientar priorizacion posterior.
- Disparador: Se prepara la evolucion posterior al MVP de descubrimiento.
- Precondiciones:
  - Existe al menos una entrega funcional evaluable del producto.
- Flujo principal:
  1. El responsable de producto revisa cobertura, adopcion y uso sobre los indicadores definidos.
  2. Contrasta el resultado con los umbrales acordados.
  3. Registra una conclusion de continuidad, ajuste o ampliacion.
- Flujos alternativos:
  - A1. Si un indicador no puede medirse todavia, se deja constancia de la limitacion y de la accion necesaria para habilitarlo.
  - A2. Si la cobertura crece mas rapido que la calidad percibida, se priorizan ajustes de relevancia sobre nuevas fuentes.
- Postcondiciones:
  - Existe una base objetiva para decidir la siguiente priorizacion funcional.
- Reglas de negocio relacionadas:
  - RB-14 Ningun KPI debe bloquear por si solo la salida del MVP de descubrimiento.
  - RB-15 Los KPIs deben servir para decidir, no solo para informar.
  - RB-26 La definicion funcional de KPIs puede adelantarse a la instrumentacion completa siempre que deje explicita la limitacion de medicion.

## CU-08 Revisar reglas auditables de relevancia TI
- Backlog relacionado: PB-006
- Historias relacionadas: HU-06
- Actor principal: Responsable de producto o `qa-teams`.
- Objetivo: Verificar de forma observable que la regla funcional de relevancia TI distingue inclusiones, exclusiones y casos frontera antes de construir el catalogo.
- Disparador: Se necesita validar o revisar la regla TI vigente del MVP.
- Precondiciones:
  - Existe una definicion funcional vigente de inclusion, exclusion y casos frontera.
  - La aplicacion expone una superficie verificable para revisar reglas y ejemplos auditados.
- Flujo principal:
  1. El actor accede a la vista o salida verificable de clasificacion TI.
  2. El sistema muestra criterios de inclusion, exclusion y casos frontera.
  3. El actor revisa ejemplos representativos con clasificacion esperada y obtenida.
  4. El actor confirma si la regla funcional es suficiente para habilitar el catalogo.
- Flujos alternativos:
  - A1. Si un ejemplo no coincide con la clasificacion esperada, el sistema deja visible la discrepancia para su correccion.
  - A2. Si un caso sigue siendo ambiguo, se mantiene identificado como frontera y se eleva a refinamiento funcional posterior.
- Postcondiciones:
  - La regla TI queda validable o sujeta a ajustes antes de aplicarse sobre el catalogo.
- Reglas de negocio relacionadas:
  - RB-18 La regla TI debe ser auditable por producto y `qa-teams` antes de depender de ella en el catalogo.
  - RB-19 Los casos frontera no deben presentarse como inclusion inequivoca si requieren criterio adicional.

## CU-09 Priorizar fuentes reales oficiales para recopilacion
- Backlog relacionado: PB-009
- Historias relacionadas: HU-09
- Actor principal: Responsable de producto.
- Objetivo: Definir que fuentes reales oficiales deben entrar antes en la recopilacion para acercar el producto a datos utilizables en produccion.
- Disparador: Se revisa la priorizacion posterior al MVP inicial de descubrimiento.
- Precondiciones:
  - Existe una cobertura funcional inicial ya delimitada.
  - Existen fuentes oficiales reales identificables con valor potencial para contratos y concursos TI.
- Flujo principal:
  1. El responsable de producto revisa fuentes reales oficiales candidatas.
  2. Prioriza las fuentes segun valor para Canarias, credibilidad del dato y capacidad de alimentar recopilacion util, distinguiendo `Ola 1`, `Ola 2` y `Ola 3`.
  3. Define el minimo funcional verificable que debe conservar cada oportunidad recopilada desde fuente real oficial.
  4. Registra fuentes concretas, su prioridad y las exclusiones de iteracion en backlog, roadmap y refinamiento funcional.
  5. Crea o actualiza una issue ejecutable para que `developer-teams` implemente la nueva prioridad.
- Flujos alternativos:
  - A1. Si una fuente oficial es real pero su formato o acceso exige analisis adicional, puede quedar priorizada con alcance incremental en lugar de descartarse.
  - A2. Si una fuente tiene cobertura estatal pero aporta contratos relevantes para Canarias, puede quedar incluida como prioridad complementaria.
  - A3. Si una fuente prioritaria no puede aportar de momento todos los campos enriquecidos del catalogo, la entrega sigue siendo valida si conserva al menos referencia oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
- Postcondiciones:
  - El proyecto dispone de una prioridad trazable y ejecutable para reforzar la recopilacion con fuentes reales.
- Reglas de negocio relacionadas:
  - RB-27 La recopilacion prioritaria debe apoyarse en fuentes oficiales reales y verificables antes que en nuevas capacidades de retencion no esenciales.
  - RB-28 La lista prioritaria debe nombrar de forma explicita al menos `BOC`, `BOP Las Palmas` y `BOE`.
  - RB-29 La primera iteracion de recopilacion priorizada debe ordenar las fuentes por olas para evitar una implementacion simultanea difusa.
  - RB-30 Toda oportunidad recopilada desde una fuente real priorizada debe conservar trazabilidad minima al origen oficial.
  - RB-31 `PB-009` no amplía por si mismo el alcance comercial prometido ni habilita alertas o pipeline.

## CU-10 Navegar por los modulos principales con una estructura responsive
- Backlog relacionado: PB-010
- Historias relacionadas: HU-10
- Actor principal: Usuario registrado de Licican.
- Objetivo: Moverse entre las opciones principales de la aplicacion desde una navegacion clara, estable y adaptable al ancho disponible.
- Disparador: El usuario accede a cualquier pantalla principal de la aplicacion.
- Precondiciones:
  - Existe al menos un modulo principal disponible para el usuario.
  - La aplicacion expone una estructura comun de navegacion entre sus vistas principales.
- Flujo principal:
  1. El usuario abre la aplicacion.
  2. El sistema muestra una navegacion principal persistente con iconos dispuestos verticalmente en el lateral izquierdo cuando el ancho disponible lo permite.
  3. El usuario identifica la opcion activa y selecciona otra opcion principal.
  4. El sistema actualiza el contenido principal manteniendo visible el contexto de navegacion.
  5. El usuario sigue trabajando sin perder acceso a las opciones principales de la aplicacion.
- Flujos alternativos:
  - A1. Si el ancho disponible no permite mantener el menu lateral completo, el sistema conserva el acceso a las opciones principales mediante una variante responsive sin solapamientos ni perdida de navegacion.
  - A2. Si una opcion principal prevista aun no esta disponible funcionalmente, el sistema no la presenta como accion lista para uso o la marca de forma explicita como `proximamente`.
  - A3. Si el usuario vuelve a una vista ya visitada, el sistema mantiene resaltada la seccion activa correspondiente.
- Postcondiciones:
  - El usuario puede recorrer los modulos principales desde una estructura comun y entendible.
- Reglas de negocio relacionadas:
  - RB-32 La aplicacion debe ofrecer una navegacion principal consistente entre modulos con una opcion activa visible.
  - RB-33 En anchos amplios, la navegacion principal debe mostrarse en el lateral izquierdo con disposicion vertical por iconos.
  - RB-34 La adaptacion responsive no debe provocar perdida de acceso a opciones principales ni solapamiento del contenido.
  - RB-35 Ninguna opcion no disponible debe inducir al usuario a pensar que ya esta operativa si aun no lo esta.

## CU-11 Consolidar snapshots `.atom` en un dataset funcional trazable
- Backlog relacionado: PB-011
- Historias relacionadas: HU-11
- Actor principal: Responsable de producto o proceso de recopilacion del sistema.
- Objetivo: Transformar los snapshots `.atom` versionados de `data/` en un conjunto consolidado de oportunidades TI Canarias listo para uso funcional.
- Disparador: La aplicacion necesita actualizar su base visible a partir de los `.atom` disponibles.
- Precondiciones:
  - Existen ficheros `.atom` en la carpeta `data/`.
  - Las reglas funcionales de relevancia TI siguen vigentes.
- Flujo principal:
  1. El sistema localiza todos los ficheros `.atom` disponibles en `data/`.
  2. Recorre cada `<entry>` y evalua el filtro geografico Canarias y el filtro TI por CPV.
  3. Agrupa los registros por expediente para evitar duplicados funcionales entre snapshots.
  4. Conserva como version vigente la entrada mas reciente disponible para cada expediente.
  5. Guarda o expone el nombre del fichero `.atom` del que procede esa version vigente.
- Flujos alternativos:
  - A1. Si un `.atom` no aporta entradas validas, el sistema lo ignora sin bloquear el resto de la consolidacion.
  - A2. Si falta `CountrySubentityCode`, el sistema puede apoyarse en `ParentLocatedParty` o `CountrySubentity` para decidir el criterio geografico.
  - A3. Si un expediente aparece en varios snapshots con distinta fecha oficial, el sistema conserva solo la version mas reciente.
- Postcondiciones:
  - Existe un dataset funcional consolidado de oportunidades TI Canarias con trazabilidad al fichero origen.
- Reglas de negocio relacionadas:
  - RB-36 La aplicacion debe procesar todos los `.atom` presentes en `data/`, no un unico nombre de fichero fijo.
  - RB-37 El filtro geografico prioritario para Canarias es `CountrySubentityCode` con prefijo `ES7`.
  - RB-38 El filtro geografico complementario puede usar `ParentLocatedParty` y `CountrySubentity` con referencias a Canarias o islas canarias.
  - RB-39 La relevancia TI estructurada en esta iteracion se determina por CPVs con prefijo `72`, `48` o `302`.
  - RB-40 La consolidacion debe conservar una unica version funcional por expediente y mantener trazabilidad al fichero origen vigente.

## CU-12 Revisar la informacion consolidada en pestañas y detalle con fichero origen visible
- Backlog relacionado: PB-012
- Historias relacionadas: HU-12
- Actor principal: Usuario registrado de Licican.
- Objetivo: Consultar la informacion consolidada de licitaciones, lotes y adjudicaciones desde una superficie verificable y con trazabilidad al snapshot origen.
- Disparador: El usuario accede al modulo de oportunidades consolidado desde fuentes `.atom`.
- Precondiciones:
  - El dataset consolidado de `PB-011` esta disponible.
  - Existe una referencia funcional de salida en `data/licitaciones_ti_canarias.xlsx`.
- Flujo principal:
  1. El usuario abre la vista principal de licitaciones TI Canarias.
  2. El sistema muestra la pestaña `Licitaciones TI Canarias` con la informacion principal de los expedientes.
  3. El usuario navega a `Detalle Lotes` o `Adjudicaciones` segun su necesidad.
  4. El usuario abre el detalle de una licitacion o contrato.
  5. El sistema muestra el nombre del fichero `.atom` origen de la version consolidada del dato.
- Flujos alternativos:
  - A1. Si una licitacion no tiene lotes o adjudicaciones, la superficie correspondiente muestra un estado vacio claro.
  - A2. Si algun campo esperado no viene informado en origen, la aplicacion lo marca como no informado sin ocultar el resto del registro.
  - A3. Si `qa-teams` compara una muestra con el Excel de referencia, puede localizar la correspondencia funcional en las tres pestañas principales.
- Postcondiciones:
  - El usuario ha revisado informacion estructurada y trazable sobre licitaciones, lotes y adjudicaciones.
- Reglas de negocio relacionadas:
  - RB-41 La aplicacion debe ofrecer las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
  - RB-42 El detalle de licitacion o contrato debe mostrar el nombre del fichero `.atom` origen de la version consolidada.
  - RB-43 La salida visible debe ser funcionalmente contrastable con `data/licitaciones_ti_canarias.xlsx` para la muestra de datos vigente.
  - RB-44 Los datos no informados en origen deben quedar senalizados de forma clara.

## CU-13 Aplicar permisos segun rol en consulta y gestion
- Backlog relacionado: PB-013
- Historias relacionadas: HU-13
- Actor principal: Usuario autenticado o invitado segun el rol asignado.
- Objetivo: Garantizar que cada rol ve y ejecuta solo las acciones que le corresponden.
- Disparador: El usuario accede a una accion de consulta o de gestion en la aplicacion.
- Precondiciones:
  - Existe un rol funcional asignado o inferido para el usuario actual.
  - El producto ya dispone de acciones visibles de consulta, alertas o administracion.
- Flujo principal:
  1. El usuario accede a una vista o accion del producto.
  2. El sistema identifica su rol: `Administrador`, `Colaborador` o `Lector/Invitado`.
  3. El sistema muestra las acciones permitidas para ese rol.
  4. El usuario ejecuta una accion autorizada.
  5. El sistema procesa la accion manteniendo la trazabilidad de permisos aplicada.
- Flujos alternativos:
  - A1. Si el usuario intenta ejecutar una accion no permitida, el sistema la bloquea y no la presenta como operativa.
  - A2. Si el rol es `Lector/Invitado`, el sistema permite consulta de catalogo, detalle, filtros y vistas consolidadas, pero no muestra acciones de alta o edicion.
  - A3. Si el rol es `Colaborador`, el sistema limita la gestion a sus elementos propios en las superficies ya disponibles y excluye administracion global.
  - A4. Si una superficie futura como pipeline aun no esta expuesta, la aplicacion conserva la regla funcional definida sin bloquear la iteracion de permisos sobre las superficies vigentes.
- Postcondiciones:
  - El usuario ha operado dentro del alcance permitido para su rol.
- Reglas de negocio relacionadas:
  - RB-45 El sistema debe distinguir al menos los roles `Administrador`, `Colaborador` y `Lector/Invitado`.
  - RB-46 `Administrador` puede administrar acciones transversales de consulta y gestion.
  - RB-47 `Colaborador` solo puede gestionar sus propios elementos salvo permiso adicional explicitado.
  - RB-48 `Lector/Invitado` no puede crear ni modificar entidades.
  - RB-49 La interfaz no debe mostrar como disponibles acciones bloqueadas por permisos.
  - RB-50 La primera iteracion de permisos debe ser ejecutable sobre las superficies ya disponibles y extenderse a pipeline cuando `PB-005` exista sin redefinir la matriz base.

## CU-14 Navegar resultados del catalogo en paginas
- Backlog relacionado: PB-014
- Historias relacionadas: HU-14
- Actor principal: Usuario registrado de Licican.
- Objetivo: Consultar resultados amplios del catalogo sin perder contexto ni rendimiento.
- Disparador: El usuario solicita avanzar, retroceder o cambiar de pagina en el catalogo o su API.
- Precondiciones:
  - El catalogo dispone de mas resultados de los que una sola vista muestra por defecto.
  - Los filtros funcionales de catalogo siguen disponibles.
- Flujo principal:
  1. El usuario abre el catalogo o consulta la API.
  2. El sistema muestra los resultados en paginas y expone el rango visible actual.
  3. El usuario cambia de pagina o salta a una concreta.
  4. El sistema mantiene filtros y orden mientras actualiza la pagina visible.
- Flujos alternativos:
  - A1. Si la pagina solicitada no existe o es invalida, el sistema responde con un comportamiento controlado y consistente.
  - A2. Si los filtros activos reducen mucho el resultado, el sistema sigue mostrando la paginacion disponible de forma clara.
- Postcondiciones:
  - El usuario sigue trabajando con un subconjunto manejable de resultados.
- Reglas de negocio relacionadas:
  - RB-51 La navegacion paginada debe preservar filtros activos y orden visible.
  - RB-52 El sistema debe mostrar total de resultados y rango actualmente visible.

## CU-15 Configurar conservacion y archivado de licitaciones
- Backlog relacionado: PB-015
- Historias relacionadas: HU-15
- Actor principal: Administradora u operador de datos.
- Objetivo: Definir cuanto tiempo se conservan las licitaciones activas y cuando deben archivarse las cerradas.
- Disparador: El responsable de operacion abre el panel de control de retencion.
- Precondiciones:
  - Existe configuracion operativa de retencion disponible.
  - La fuente de datos y la gestion de seguimiento activo ya estan disponibles en `main`.
- Flujo principal:
  1. El responsable abre el panel de control.
  2. El sistema muestra el umbral de conservacion configurado.
  3. El responsable ajusta si la politica se mide desde la creacion o desde el cierre de la licitacion.
  4. El sistema aplica la politica sobre licitaciones cerradas y conserva las activas con seguimiento.
  5. Las licitaciones archivadas se trasladan a una tabla homologa con la misma estructura de datos.
- Flujos alternativos:
  - A1. Si una licitacion mantiene seguimiento activo, el sistema no la borra aunque supere el umbral.
  - A2. Si la politica no puede ejecutarse todavia sobre la base de datos, el panel sigue mostrando la configuracion sin aplicar borrado automatico.
- Postcondiciones:
  - La politica de conservacion y archivado queda visible y alineada con la operacion.
- Reglas de negocio relacionadas:
  - RB-53 Las licitaciones con seguimiento activo no se eliminan.
  - RB-54 Las licitaciones cerradas y archivables se trasladan a una tabla de archivadas con la misma estructura de datos.
  - RB-55 La configuracion puede expresarse en dias totales desde la creacion o en antiguedad de las cerradas.

## CU-16 Administrar cuentas de usuario
- Backlog relacionado: PB-016
- Historias relacionadas: HU-16
- Actor principal: Administrador de plataforma, administrador funcional o responsable con permisos de gestion de usuarios.
- Objetivo: Gestionar cuentas, roles, permisos y estados de acceso de los usuarios de Licican desde un modulo centralizado y trazable.
- Disparador: El responsable abre el modulo `Gestion de usuarios`.
- Precondiciones:
  - Existe un contexto de sesion con permisos suficientes para la gestion de usuarios.
  - El sistema dispone de persistencia para cuentas, estados y trazabilidad.
- Flujo principal:
  1. El responsable abre el modulo de gestion de usuarios.
  2. El sistema muestra un listado paginado con filtros, KPIs y acciones por fila.
  3. El responsable crea o edita una cuenta segun necesidad.
  4. El sistema valida datos, roles, superficies y restricciones de acceso.
  5. El responsable activa, desactiva, reactiva, reenvia invitaciones o reinicia acceso segun el estado de la cuenta.
  6. El sistema deja trazabilidad del cambio y actualiza el detalle del usuario.
- Flujos alternativos:
  - A1. Si el email ya existe, el sistema bloquea la alta o la edicion y muestra un error claro.
  - A2. Si se intenta desactivar al ultimo administrador activo, el sistema bloquea la accion.
  - A3. Si la cuenta esta pendiente de activacion, el sistema permite reenviar la invitacion pero no permite acceso operativo.
  - A4. Si el responsable no tiene permisos suficientes para asignar un rol o superficie restringida, la accion se impide.
  - A5. Si se solicita una baja logica, el sistema conserva el historico y retira la cuenta del uso activo.
- Postcondiciones:
  - La cuenta queda actualizada y la accion relevante permanece auditada.
- Reglas de negocio relacionadas:
  - RB-56 El email debe ser unico y valido.
  - RB-57 La alta, edicion, activacion, desactivacion, reactivacion y baja logica deben quedar auditadas.
  - RB-58 Un usuario inactivo, bloqueado o pendiente no debe poder acceder hasta que su estado lo permita.
  - RB-59 El sistema no puede quedar sin ningun administrador activo.
  - RB-60 La baja logica debe preferirse a la eliminacion fisica.
  - RB-61 Los roles o superficies sensibles solo pueden asignarse con permisos suficientes.
  - RB-62 El ultimo acceso debe ser visible o quedar como no disponible si nunca ha iniciado sesion.
  - RB-63 Las acciones sensibles requieren confirmacion previa antes de ejecutarse.
