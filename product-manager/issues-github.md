# Borradores de issues de GitHub

## Estado actual
- La issue de `PB-010` ya fue creada en GitHub como issue #10 el 2026-03-26.
- La issue de `PB-011` ya fue creada en GitHub como issue #11 el 2026-03-26, validada por `qa-teams` el 2026-03-27, integrada en `main` por `developer-teams` el 2026-03-28 y cerrada administrativamente por `product-manager` el mismo dia.
- La issue de `PB-012` ya fue creada en GitHub como issue #12 el 2026-03-26 y actualmente esta en `Estado operativo: no validado`.
- La issue de `PB-013` ya fue creada en GitHub como issue #13 el 2026-03-28 para convertir en trabajo ejecutable el modelo de roles y permisos.
- Los hallazgos de `quality-auditor` y `security-auditor` del 2026-03-28 quedan pendientes de que `developer-teams` los traduzca en issues tecnicas separadas para su priorizacion posterior por producto.

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
Estado operativo: no validado

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
Estado operativo: nuevo

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
1. El sistema distingue al menos los roles `Administrador`, `Colaborador` y `Lector/Invitado`.
2. `Administrador` puede consultar licitaciones, gestionar alertas, gestionar pipeline propio y ajeno cuando aplique, consultar KPIs y administrar roles o permisos.
3. `Colaborador` puede consultar licitaciones, crear y editar sus alertas, gestionar su pipeline propio y consultar KPIs solo si la vista no expone informacion sensible de negocio o de otros usuarios.
4. `Lector/Invitado` puede consultar catalogo, detalle, filtros y vistas consolidadas, pero no puede crear ni modificar alertas, pipeline, roles ni configuraciones de producto.
5. Si un usuario intenta ejecutar una accion no permitida para su rol, el sistema bloquea la accion de forma consistente y no expone controles operativos como si estuvieran disponibles.
6. La navegacion y las superficies del producto muestran u ocultan acciones segun rol sin degradar la experiencia de consulta.
Dependencias: PB-010, PB-004 y PB-005
Estado operativo: nuevo

Contexto funcional:
- La especificacion funcional consolidada ya define una matriz de permisos para `Administrador`, `Colaborador` y `Lector/Invitado`, pero ese alcance no estaba todavia trazado como issue ejecutable.
- Producto necesita convertir esa definicion en trabajo observable antes de ampliar gestion multiusuario o administracion operativa.

Tareas sugeridas:
- Inventariar las acciones visibles y mutables del producto actual.
- Mapear cada accion a la matriz de permisos aprobada por producto.
- Aplicar restricciones coherentes en interfaz y backend donde corresponda.
- Ajustar navegacion y llamadas a la accion para que no sugieran capacidades inexistentes al rol actual.
- Dejar evidencia verificable para `qa-teams` con escenarios por rol.

Preguntas abiertas que `developer-teams` debe aclarar si bloquean:
- Si el primer corte funcional debe resolver autenticacion real o puede apoyarse inicialmente en roles simulados para validar el comportamiento visible.
- Que vistas de KPI pueden exponerse a `Colaborador` sin abrir informacion sensible de negocio o de otros usuarios.
