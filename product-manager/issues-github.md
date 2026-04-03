# Borradores de issues de GitHub

## Estado actual
- La unica issue funcional que debe permanecer abierta tras la reconciliacion del 2026-04-03 es `#8`.
- La issue de `PB-005` ya no esta abierta: fue validada por `qa-teams` el 2026-03-31 en la issue #7 y cerrada en GitHub el 2026-04-01.
- La issue de `PB-010` ya fue creada en GitHub como issue #10 el 2026-03-26 y ya quedo cerrada administrativamente el 2026-03-30 tras validacion, integracion en `main` y borrado de rama.
- La issue de `PB-011` ya fue creada en GitHub como issue #11 el 2026-03-26, validada por `qa-teams` el 2026-03-27, integrada en `main` por `developer-teams` el 2026-03-28 y cerrada administrativamente por `product-manager` el mismo dia.
- La issue de `PB-012` ya fue creada en GitHub como issue #12 el 2026-03-26, `qa-teams` la valido el 2026-03-29, `developer-teams` la integro en `main` el 2026-03-30 y ya no debe tratarse como issue abierta.
- La issue de `PB-013` ya fue creada en GitHub como issue #13 el 2026-03-28 y fue cerrada en GitHub el 2026-04-01.
- La issue tecnica #14 ya fue validada por `qa-teams` el 2026-03-30, integrada en `main` por `developer-teams` y cerrada administrativamente por `product-manager` el mismo dia.
- La issue de `PB-014` ya fue creada en GitHub como issue #15 para introducir paginacion en el catalogo y la API.
- La issue de `PB-015` ya fue creada en GitHub como issue #16 para introducir un panel de control de conservacion y archivado de licitaciones; fue validada por `qa-teams`, integrada en `main` por `developer-teams` y cerrada administrativamente por `product-manager` el 2026-04-03.
- La issue de `PB-016` ya fue creada en GitHub como issue #28, validada por `qa-teams` el 2026-04-02, integrada en `main` y cerrada administrativamente por `product-manager` el 2026-04-03 dejando `Estado operativo: cerrado`.
- La issue tecnica `T-002` ya fue creada en GitHub como issue #17 para corregir el filtrado de licitaciones tras la migracion a PostgreSQL, fue validada por `qa-teams` el 2026-03-30, integrada en `main` por `developer-teams` y cerrada administrativamente por `product-manager` el mismo dia.
- La issue tecnica `T-003` ya fue creada en GitHub como issue #18 para unificar utilidades de texto compartidas.
- La issue tecnica `T-004` ya fue creada en GitHub como issue #19 para centralizar constantes de dominio compartidas.
- La issue tecnica `T-005` ya fue creada en GitHub como issue #20 para endurecer la configuracion de credenciales PostgreSQL.
- La issue tecnica `T-006` ya fue creada en GitHub como issue #21 para extraer la resolucion de configuracion a `licican/config.py`.
- La issue tecnica `T-007` ya fue creada en GitHub como issue #22 para extraer helpers HTTP a `licican/web/responses.py`.
- La issue tecnica `T-008` ya fue creada en GitHub como issue #23 para servir el CSS como recurso estatico.
- La issue tecnica `T-009` ya fue creada en GitHub como issue #24 para separar plantillas HTML por vistas.
- La issue tecnica `T-010` ya fue creada en GitHub como issue #26 para introducir un router declarativo en la aplicacion WSGI.
- La issue tecnica `T-011` ya fue creada en GitHub como issue #27 para desacoplar `CatalogFilters` hacia `licican/shared/filters.py`.
- La issue tecnica `T-012` ya fue creada en GitHub como issue #25 para extraer helpers de navegacion XML compartidos.
- En la revision del 2026-03-29 se detecta una inconsistencia de alcance en `PB-013`: no debe quedar bloqueada por `PB-005`, porque su primer corte funcional gobierna superficies ya disponibles y deja pipeline como extension posterior.
- Los hallazgos de `quality-auditor` y `security-auditor` del 2026-03-28 quedan pendientes de que `developer-teams` los traduzca en issues tecnicas separadas para su priorizacion posterior por producto.

## Issue creada: Medicion basica de cobertura, adopcion y uso inicial del producto

Titulo sugerido: `[product-manager] PB-008 Definir medicion basica de cobertura, adopcion y uso`

Backlog: PB-008 Medicion basica de valor del producto
Historia de usuario: HU-08 Medir cobertura y uso inicial del producto
Caso de uso: CU-07 Revisar indicadores iniciales de producto
Criterios de aceptacion:
1. Existe al menos un KPI de cobertura, uno de adopcion y uno de uso.
2. Cada KPI incluye definicion, formula, umbral inicial y decision asociada.
3. La bateria minima puede arrancar con medicion manual temporal si la instrumentacion completa aun no existe, siempre que la limitacion quede explicitada.
4. La documentacion resultante permite revisar los KPIs sin bloquear el MVP funcional.
5. La propuesta deja claro que la primera medicion puede ser operativa y documental, no necesariamente automatizada desde el primer dia.
Dependencias: PB-001, PB-004
Estado operativo: nuevo

Contexto funcional:
- Producto necesita una base objetiva para decidir si ampliar cobertura, profundizar en relevancia o invertir antes en retencion.
- La definicion de KPIs debe ser util para la priorizacion posterior, no solo para reporting descriptivo.
- La primera iteracion no debe quedar bloqueada por la ausencia de instrumentacion avanzada si la definicion funcional ya es clara.

KPIs sugeridos para la primera iteracion:
- Cobertura: porcentaje de fuentes MVP priorizadas que producen datos visibles y trazables en la ventana de evaluacion.
- Adopcion: porcentaje de usuarios activos semanales que disponen de al menos una alerta activa.
- Uso: frecuencia semanal de consultas de catalogo o detalle por usuario activo.

Umbrales iniciales y decisiones asociadas:
- Cobertura: umbral inicial provisional del 90 por ciento; si baja de ese nivel, la decision es frenar expansion y estabilizar trazabilidad e ingestion.
- Adopcion: umbral inicial provisional del 30 por ciento de usuarios activos semanales con al menos una alerta; si baja de ese nivel, la decision es simplificar onboarding y configuracion de alertas.
- Uso: umbral inicial provisional de una interaccion semanal de catalogo o detalle por usuario activo; si baja de ese nivel, la decision es revisar relevancia, navegacion y encaje funcional antes de ampliar cobertura.

Tareas sugeridas:
- Definir la formula exacta de cada KPI y su unidad de medida.
- Fijar un umbral inicial provisional para cada indicador y la decision de producto asociada.
- Indicar claramente si la primera captura sera manual, automatizada o mixta.
- Alinear la definicion con las capacidades ya disponibles en catalogo, alertas y detalle.
- Preparar criterios verificables para que `qa-teams` contraste la documentacion.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Si el primer corte funcional de medicion se apoyara en datos manuales de seguimiento mientras se habilita la instrumentacion automatica.
- Si el KPI de uso debe centrarse en catalogo, detalle, alertas o una combinacion simple de las tres superficies.

## Issue creada: Consolidar fuentes `.atom` versionadas de `/data` para licitaciones TI Canarias

Titulo sugerido: `[product-manager] PB-011 Consolidar fuentes .atom versionadas de /data para licitaciones TI Canarias`

Backlog: PB-011 Consolidacion funcional de fuentes `.atom` versionadas para oportunidades TI Canarias
Historia de usuario: HU-11 Consolidar licitaciones TI Canarias desde snapshots `.atom` versionados
Caso de uso: CU-11 Consolidar snapshots `.atom` en un dataset funcional trazable
Criterios de aceptacion:
1. La aplicacion toma como fuentes de entrada todos los ficheros con extension `.atom` disponibles en la carpeta `data/`, sin depender de un nombre fijo.
2. La consolidacion funcional recorre cada `<entry>` y solo considera candidatas las oportunidades que cumplan simultaneamente criterio geografico Canarias y criterio TI por CPV.
3. El criterio geografico se considera valido si existe algun `CountrySubentityCode` que empiece por `ES7`, o si en `ParentLocatedParty` o en `CountrySubentity` aparece `Canarias` o una isla canaria relevante.
4. El criterio TI se considera valido si algun `ItemClassificationCode` empieza por `72`, `48` o `302`.
5. Si un mismo expediente aparece en varios `.atom`, la aplicacion conserva una unica version funcional por expediente usando la version mas reciente disponible.
6. Cada registro consolidado conserva el nombre del fichero `.atom` del que procede la version vigente.
Dependencias: PB-009 y PB-006
Estado operativo: cerrado

Contexto funcional:
- La carpeta `data/` ya contiene snapshots `.atom` que se iran actualizando con nuevas fechas y horas en el nombre del fichero.
- Producto fija como regla funcional que la carga debe apoyarse en la presencia dinamica de todos los `.atom` y no en un nombre estatico.
- La consolidacion debe ser auditable para que QA pueda contrastar entradas, filtros y trazabilidad.

Tareas sugeridas:
- Inventariar y cargar todos los `.atom` disponibles en `data/`.
- Definir la clave funcional de consolidacion por expediente y la regla de version vigente.
- Implementar el filtrado conjunto Canarias + TI con trazabilidad verificable.
- Persistir o exponer el nombre del fichero origen asociado a la version vigente.
- Dejar evidencia tecnica de la muestra consolidada obtenida desde los `.atom` actuales.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Que campo o combinacion de campos garantiza mejor la unicidad funcional del expediente cuando falte `ContractFolderID`.
- Si la fecha oficial mas fiable para priorizar versiones es `atom:updated` o si debe existir criterio complementario en caso de empate.

## Issue creada: Exponer en la aplicacion las vistas del Excel de licitaciones TI Canarias

Titulo sugerido: `[product-manager] PB-012 Exponer en la aplicacion las vistas del Excel de licitaciones TI Canarias`

Backlog: PB-012 Exposicion funcional en la aplicacion del dataset de licitaciones TI Canarias
Historia de usuario: HU-12 Consultar licitaciones, lotes y adjudicaciones con trazabilidad al fichero origen
Caso de uso: CU-12 Revisar la informacion consolidada en pestañas y detalle con fichero origen visible
Criterios de aceptacion:
1. La aplicacion muestra una pestaña `Licitaciones TI Canarias`.
2. La aplicacion muestra una pestaña `Detalle Lotes`.
3. La aplicacion muestra una pestaña `Adjudicaciones`.
4. El detalle de una licitacion o contrato muestra de forma visible el nombre del fichero `.atom` origen.
5. La informacion visible en la aplicacion para la muestra actual corresponde funcionalmente con `data/licitaciones_ti_canarias.xlsx` en esas tres pestañas.
6. Si algun campo esperado no viene informado en origen, la aplicacion lo muestra como dato no informado o equivalente claro.
Dependencias: PB-011 y PB-002
Estado operativo: cerrado

Contexto funcional:
- El Excel `data/licitaciones_ti_canarias.xlsx` actua como referencia funcional de salida para esta iteracion.
- QA debe poder comparar una muestra representativa entre aplicacion y Excel.
- La trazabilidad del dato exige que el detalle muestre el fichero `.atom` origen de la version consolidada.

Tareas sugeridas:
- Mapear a la interfaz las columnas y agrupaciones funcionales relevantes del Excel de referencia.
- Definir la navegacion o segmentacion adecuada entre licitaciones, lotes y adjudicaciones.
- Exponer en el detalle de expediente o contrato el nombre del fichero `.atom` origen.
- Preparar una muestra verificable para QA sobre los datos actuales de `data/`.
- Documentar limitaciones funcionales si alguna columna del Excel no entra en esta iteracion.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Si la primera iteracion debe cubrir solo las tres pestañas indicadas o dejar preparada tambien la extension posterior a `Modificaciones`.
- Que subconjunto minimo de columnas del Excel debe priorizarse primero si la interfaz no puede absorberlas todas en una unica pantalla sin degradar legibilidad.

Estado administrativo actual:
- La issue #12 ya fue reconciliada como cerrada tras validacion, merge en `main` y borrado de rama.

## Issue creada: Navegacion principal responsive con menu lateral de iconos

Titulo sugerido: `[product-manager] PB-010 Navegacion principal responsive con menu lateral de iconos`

Backlog: PB-010 Navegacion principal responsive con menu lateral de iconos
Historia de usuario: HU-10 Navegar por los modulos principales desde una estructura comun adaptable al ancho de la ventana
Caso de uso: CU-10 Navegar por los modulos principales con una estructura responsive
Criterios de aceptacion:
1. En resoluciones amplias la aplicacion muestra un menu lateral izquierdo persistente con iconos en disposicion vertical para las opciones principales.
2. La opcion activa de navegacion queda resaltada de forma visible y consistente entre vistas.
3. La interfaz adapta la navegacion y el contenido al ancho disponible sin solapamientos ni necesidad de scroll horizontal estructural.
4. En anchos reducidos la navegacion principal sigue siendo accesible mediante una variante responsive coherente con la estructura general de la aplicacion.
5. Las opciones aun no disponibles no deben presentarse como rutas plenamente operativas; si se muestran, deben quedar marcadas de forma explicita como `proximamente`.
6. La entrega no debe degradar las superficies ya validadas de catalogo, detalle, filtros y alertas.
Dependencias: PB-001, PB-002, PB-003 y coordinacion de visibilidad con PB-004 y PB-005 segun estado real de implementacion
Estado operativo: cerrado

Contexto funcional:
- El producto necesita una base de navegacion comun para sostener el crecimiento de catalogo, alertas, pipeline y futuras vistas sin obligar al usuario a reaprender la estructura en cada pantalla.
- El patron deseado es una navegacion principal situada a la izquierda con iconos en vertical, priorizando claridad, ubicacion rapida y escalabilidad de modulos.
- La adaptacion al ancho de ventana es un requisito de producto, no una mejora cosmetica opcional.

Alcance esperado para `developer-teams`:
- Definir una estructura de layout comun reutilizable para las pantallas principales.
- Incorporar el menu lateral izquierdo de iconos en vistas donde aplique.
- Resolver el comportamiento responsive de la navegacion y del contenedor principal.
- Mantener coherencia visual de estado activo, foco y jerarquia de contenido.
- Evitar exponer como disponibles modulos que aun no tengan una superficie funcional utilizable.

Tareas sugeridas:
- Inventariar las opciones principales reales que ya existen en la aplicacion y distinguirlas de las previstas.
- Proponer la estructura base de navegacion y su correspondencia con las vistas actuales.
- Implementar el layout comun y aplicar la navegacion a las pantallas principales existentes.
- Definir y aplicar el comportamiento responsive para anchos reducidos.
- Revisar regresiones visuales y funcionales sobre catalogo, detalle, filtros y alertas.
- Añadir evidencia de verificacion tecnica y capturas o descripcion verificable para `qa-teams`.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Que opciones deben aparecer desde el primer dia como modulos principales visibles y cuales deben quedar ocultas o marcadas como `proximamente`.
- Si alguna vista actual requiere ajuste de contenido adicional para encajar en el nuevo layout sin perder legibilidad.

## Issue creada: Implementar modelo funcional de roles y permisos

Titulo sugerido: `[product-manager] PB-013 Implementar modelo funcional de roles y permisos`

Backlog: PB-013 Modelo funcional de roles y permisos
Historia de usuario: HU-13 Gestionar acceso por rol a las acciones del sistema
Caso de uso: CU-13 Aplicar permisos segun rol en consulta y gestion
Criterios de aceptacion:
1. El sistema distingue al menos los roles `Administrador`, `Manager`, `Colaborador` e `Invitado`.
2. `Administrador` puede consultar licitaciones, gestionar alertas, consultar KPIs y administrar roles o permisos sobre las superficies ya disponibles, ademas de cualquier accion visible para los demas roles.
3. `Manager` puede consultar licitaciones, crear y editar sus alertas propias, operar su pipeline propio y consultar KPIs solo si la vista no expone informacion sensible de negocio o de otros usuarios.
4. `Colaborador` puede consultar catalogo, detalle, filtros y vistas consolidadas, pero no puede crear ni modificar alertas, roles ni configuraciones de producto.
5. `Invitado` puede consultar catalogo, detalle, filtros y vistas consolidadas, pero no puede crear ni modificar alertas, roles ni configuraciones de producto.
6. Si una superficie futura como pipeline aun no esta disponible, la primera iteracion de permisos no queda bloqueada por ello y deja preparada la extension de la misma matriz de permisos.
7. Si un usuario intenta ejecutar una accion no permitida para su rol, el sistema bloquea la accion de forma consistente y no expone controles operativos como si estuvieran disponibles.
8. La navegacion y las superficies del producto muestran u ocultan acciones segun rol sin degradar la experiencia de consulta.
Dependencias: PB-010 y PB-004
Estado operativo: cerrado

Contexto funcional:
- La especificacion funcional consolidada ya define una matriz de permisos para `Administrador`, `Manager`, `Colaborador` e `Invitado`, pero ese alcance no estaba todavia trazado como issue ejecutable.
- Producto necesita convertir esa definicion en trabajo observable antes de ampliar gestion multiusuario o administracion operativa.
- Esta primera iteracion debe gobernar superficies ya visibles del producto; `PB-005` no bloquea este corte y heredara despues la misma matriz funcional.

Tareas sugeridas:
- Inventariar las acciones visibles y mutables del producto actual.
- Mapear cada accion a la matriz de permisos aprobada por producto.
- Aplicar restricciones coherentes en interfaz y backend donde corresponda.
- Ajustar navegacion y llamadas a la accion para que no sugieran capacidades inexistentes al rol actual.
- Dejar preparada la extension a pipeline sin exigir que esa superficie exista ya en esta entrega.
- Dejar evidencia verificable para `qa-teams` con escenarios por rol.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Si el primer corte funcional debe resolver autenticacion real o puede apoyarse inicialmente en roles simulados para validar el comportamiento visible.
- Que vistas de KPI pueden exponerse a `Colaborador` sin abrir informacion sensible de negocio o de otros usuarios.

Estado administrativo actual:
- La issue #13 ya fue reconciliada como cerrada en GitHub el 2026-04-01.

## Issue creada: Paginacion de resultados del catalogo

Titulo sugerido: `[product-manager] PB-014 Paginacion de resultados del catalogo`

Backlog: PB-014 Paginacion de resultados del catalogo
Historia de usuario: HU-14 Paginacion de resultados del catalogo
Caso de uso: CU-14 Navegar resultados del catalogo en paginas
Criterios de aceptacion:
1. El catalogo HTML y la API JSON permiten navegar por paginas.
2. El sistema muestra el total de resultados y el rango actualmente visible.
3. El usuario puede avanzar, retroceder y saltar a una pagina concreta.
4. La paginacion conserva los filtros activos y el orden de listado.
5. Si la pagina solicitada es inexistente o invalida, el sistema responde con un comportamiento controlado y consistente.
Dependencias: PB-001, PB-003, issue #14 integrada en `main`
Estado operativo: cerrado

Contexto funcional:
- El catalogo necesita manejar mejor volumentes mayores de resultados sin perder filtros ni contexto.
- La paginacion debe ser visible tanto en HTML como en la API para que QA pueda verificarla con la misma muestra.

## Issue creada: Panel de control de conservacion y archivado de licitaciones

Titulo sugerido: `[product-manager] PB-015 Panel de control de conservacion y archivado de licitaciones`

Backlog: PB-015 Panel de control de conservacion y archivado de licitaciones
Historia de usuario: HU-15 Configurar conservacion y archivado de licitaciones
Caso de uso: CU-15 Configurar conservacion y archivado de licitaciones
Criterios de aceptacion:
1. La vista de panel de control muestra la antiguedad configurada en dias.
2. La politica puede expresarse como dias desde la creacion o como antiguedad de las licitaciones cerradas.
3. Las licitaciones con seguimiento activo no se borran nunca.
4. Las licitaciones cerradas que estuvieron activas se trasladan a una tabla `licitaciones archivadas`.
5. La tabla archivada conserva los mismos datos que la tabla principal.
6. El panel deja visible que registros se conservaran, archivaran o mantendran activos.
Dependencias: issue #14 integrada en `main`, PB-005 cerrada administrativamente
Estado operativo: nuevo

Contexto funcional:
- El panel debe servir de control operativo para conservar datos y prevenir borrados no deseados de oportunidades activas.
- La tabla archivada debe mantener la misma estructura de datos para no romper trazabilidad ni consultas futuras.

Dependencia operativa vigente:
- Esta issue ya no permanece abierta; su cierre administrativo queda reconciliado con la validacion de `qa-teams` y la integracion en `main`.

## Issue creada: Gestion de usuarios de plataforma

Titulo sugerido: `[product-manager] PB-016 Gestion de usuarios de plataforma`

Backlog: PB-016 Gestion de usuarios y accesos de plataforma
Historia de usuario: HU-16 Gestionar usuarios de plataforma
Caso de uso: CU-16 Administrar cuentas de usuario
Criterios de aceptacion:
1. Dado un administrador con permisos suficientes, cuando accede al modulo, entonces ve un listado paginado de usuarios con nombre completo, email, rol principal, superficies asignadas, estado, ultimo acceso y acciones por fila.
2. Dado un administrador con permisos suficientes, cuando crea un usuario con datos validos, entonces el sistema guarda la cuenta, la muestra en el listado y deja trazabilidad de la alta.
3. Dado un email ya existente, cuando se intenta crear o editar una cuenta con ese email, entonces el sistema bloquea la operacion con un mensaje de error claro.
4. Dado un usuario activo, cuando se desactiva o se da de baja logica, entonces deja de poder acceder y la accion queda confirmada antes de ejecutarse.
5. Dado un usuario pendiente de activacion, cuando se reenvia la invitacion, entonces el sistema confirma el reenvio y mantiene el estado pendiente hasta que acceda.
6. Dado un usuario con acceso ya iniciado, cuando se reinicia el acceso o la contraseña, entonces el sistema ejecuta la accion y la deja auditada.
7. Dado un administrador sin permisos suficientes, cuando intenta asignar un rol o superficie restringida, entonces el sistema lo impide.
8. Dado que el sistema tiene un unico administrador activo, cuando se intenta desactivar ese ultimo administrador, entonces la operacion se bloquea.
Dependencias: PB-013, contexto de sesion y trazabilidad de cambios disponibles en `main`
Estado operativo: cerrado

Contexto funcional:
- El modulo de usuarios ya se encuentra visible y validado sobre la superficie actual del producto.
- La entrega base resuelve listado, alta, detalle, cambio de estado, reenvio de invitacion, reinicio de acceso y guardia del ultimo administrador activo.
- Las futuras necesidades de autenticacion real, proveedor de identidad y auditoria centralizada deben tratarse como evoluciones posteriores y no reabrir esta issue ya validada.

Estado administrativo actual:
- `qa-teams` valido la issue #28 el 2026-04-02.
- La capacidad ya esta integrada en `main`.
- `product-manager` reconcilia su cierre administrativo el 2026-04-03 actualizando backlog, historias, casos de uso, roadmap y cuerpo de la issue.

## Issue creada: Corregir el filtrado de licitaciones tras PostgreSQL

Titulo sugerido: `[product-manager] T-002 Corregir el filtrado de licitaciones tras PostgreSQL`

Backlog: T-002 Corregir el filtrado de licitaciones tras PostgreSQL
Historia de usuario: HU-03 Filtrar oportunidades relevantes
Caso de uso: CU-03 Filtrar oportunidades
Criterios de aceptacion:
1. Los filtros por palabra clave, presupuesto, procedimiento y ubicacion funcionan en HTML y API sobre PostgreSQL.
2. Los rangos de presupuesto invalidos siguen devolviendo una respuesta controlada.
3. Los filtros combinados devuelven resultados coherentes con el backend `file` cuando se comparan sobre la misma muestra.
4. El filtrado no depende de datos embebidos obsoletos ni de rutas internas de la implementacion anterior.
5. Existen pruebas de regresion especificas sobre PostgreSQL para la combinacion de filtros mas usada.
Dependencias: PB-003, issue #14 integrada en `main`
Estado operativo: cerrado

Contexto funcional:
- La migracion a PostgreSQL ha dejado una regresion visible en el filtrado que debe corregirse antes de abrir nueva expansion funcional.
- Esta issue debe tratarse como correccion prioritaria porque afecta a una capacidad central ya disponible del producto.

## Issues creadas: Secuencia tecnica de refactorizacion sin cambio funcional externo

### issue #18
Titulo sugerido: `[product-manager] T-003 Unificar utilidades de texto compartidas`

Resumen:
- Crea `licican/shared/text.py` y elimina duplicados de normalizacion, slugificado y limpieza de texto en cuatro modulos.
- Exige mantener type hints y crear cobertura basica si la existente no basta.
- Abre la secuencia tecnica y no tiene dependencias previas.

### issue #19
Titulo sugerido: `[product-manager] T-004 Centralizar constantes de dominio compartidas`

Resumen:
- Crea `licican/shared/domain_constants.py` para compartir constantes y mapeos de dominio entre `atom_consolidation.py` y `postgres_catalog.py`.
- Mantiene fuera del modulo comun las heuristicas especificas de ubicacion de PostgreSQL.
- Depende de `T-003`.

### issue #20
Titulo sugerido: `[product-manager] T-005 Endurecer configuracion de credenciales PostgreSQL`

Resumen:
- Elimina passwords hardcodeados y exige configuracion explicita por entorno.
- Mantiene defaults no sensibles permitidos para host, puerto, base de datos y usuario.
- Depende de `T-004`.

### issue #21
Titulo sugerido: `[product-manager] T-006 Extraer resolucion de configuracion a licican/config.py`

Resumen:
- Saca de `app.py` la carga de `.env`, la resolucion de `BASE_PATH`, host, puerto y rutas auxiliares.
- Exige que `load_env_file()` solo cargue una vez por proceso.
- Depende de `T-005`.

### issue #22
Titulo sugerido: `[product-manager] T-007 Extraer helpers HTTP a licican/web/responses.py`

Resumen:
- Mueve respuestas HTTP, redirecciones, construccion de cuerpos HTML/JSON, lectura de formularios y construccion de URLs a un modulo web comun.
- Mantiene la interfaz WSGI y las URLs existentes.
- Depende de `T-006`.

### issue #23
Titulo sugerido: `[product-manager] T-008 Servir el CSS como recurso estatico`

Resumen:
- Extrae el CSS embebido a `licican/web/static/style.css`.
- Exige una ruta `/static/<filename>` con `content-type` adecuado y sin cambios visuales.
- Depende de `T-007`.

### issue #24
Titulo sugerido: `[product-manager] T-009 Separar plantillas HTML por vistas`

Resumen:
- Crea `licican/web/templates/` y distribuye renders por vista y componentes.
- Mantiene el HTML visible sin cambios externos.
- Depende de `T-008`.

### issue #26
Titulo sugerido: `[product-manager] T-010 Crear un router declarativo para la aplicacion WSGI`

Resumen:
- Introduce `licican/web/router.py`, handlers desacoplados y un `Request` simple o equivalente.
- Fija como objetivo dejar `app.py` por debajo de 100 lineas o documentar bloqueo tecnico objetivo.
- Depende de `T-009`.

### issue #27
Titulo sugerido: `[product-manager] T-011 Desacoplar CatalogFilters hacia licican/shared/filters.py`

Resumen:
- Mueve `CatalogFilters` a un modulo compartido para romper la dependencia de `alerts.py` respecto a `opportunity_catalog.py`.
- Mantiene filtros y alertas sin cambios funcionales.
- Depende de `T-010`.

### issue #25
Titulo sugerido: `[product-manager] T-012 Extraer helpers de navegacion XML compartidos`

Resumen:
- Crea `licican/shared/xml_helpers.py` y mueve ahi los helpers XML de `atom_consolidation.py`.
- Cierra la secuencia tecnica y exige prueba unitaria basica o cobertura equivalente del modulo nuevo.
- Depende de `T-011`.
