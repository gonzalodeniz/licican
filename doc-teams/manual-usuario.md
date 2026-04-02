# Manual de usuario

## Publico objetivo
Stakeholder funcional, producto o persona usuaria interna que necesita entender que se puede consultar hoy en la rama `main`.

## Estado actual para usuario
La rama `main` expone una entrega minima navegable orientada a descubrimiento inicial, seguimiento operativo y validacion funcional temprana, no un producto de uso final completo.

## Que si existe hoy
- Un catalogo de oportunidades TI servido desde PostgreSQL por defecto y visible en `/`.
- Un respaldo `file` que usa `data/opportunities.json` cuando no hay snapshots Atom versionados en `data/`.
- Una API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales en el catalogo y en `/api/oportunidades` por palabra clave, presupuesto, procedimiento y ubicacion.
- Una ficha HTML de detalle por oportunidad en `/oportunidades/<id>`, con trazabilidad al origen funcional vigente de cada registro cuando la fuente lo permite.
- Una API JSON del detalle en `/api/oportunidades/<id>`.
- Una vista HTML de datos consolidados en `/datos-consolidados`, con pestañas para `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
- Una API JSON de datos consolidados en `/api/datos-consolidados`.
- Una vista HTML de pipeline de seguimiento en `/pipeline`.
- Una API JSON de pipeline en `/api/pipeline`.
- Una gestion HTML de alertas tempranas en `/alertas`.
- Una API JSON de alertas persistidas y coincidencias internas en `/api/alertas`.
- Una gestion administrativa de usuarios en `/usuarios`, persistida en PostgreSQL.
- Una API JSON de usuarios en `/api/usuarios`.
- Una vista HTML de cobertura inicial del MVP en `/cobertura-fuentes`.
- Una salida JSON de esa cobertura en `/api/fuentes`.
- Una vista HTML de priorizacion de fuentes reales oficiales en `/priorizacion-fuentes-reales`.
- Una salida JSON de esa priorizacion en `/api/fuentes-prioritarias`.
- Una vista HTML de clasificacion TI auditable en `/clasificacion-ti`.
- Una salida JSON de reglas y ejemplos auditados en `/api/clasificacion-ti`.
- Una vista HTML de KPIs en `/kpis`.
- Una vista HTML de la matriz de permisos en `/permisos`.

## Que ve cada rol
- Administrador: puede consultar catalogo, datos consolidados, alertas, pipeline, KPIs, permisos y usuarios.
- Colaborador: puede consultar catalogo, datos consolidados, alertas, pipeline y KPIs dentro de su alcance.
- Lector/Invitado: puede consultar catalogo, detalle, datos consolidados y clasificacion TI.

## Que permite validar esta entrega
- Que el catalogo visible solo publica oportunidades clasificadas como TI y dentro de la cobertura vigente.
- Que el usuario puede filtrar el catalogo, ver los filtros activos y limpiar la busqueda.
- Que si el rango de presupuesto es invalido, la interfaz solicita corregirlo y no lo presenta como ausencia de resultados.
- Que cada oportunidad mantiene organismo, ubicacion, estado oficial, fecha limite y referencia a su fuente oficial cuando esa informacion existe en el origen.
- Que la ficha de detalle refleja el ultimo dato oficial visible cuando existe una rectificacion o modificacion publicada.
- Que los datos consolidados muestran `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones` con trazabilidad al Excel versionado.
- Que el pipeline permite guardar oportunidades, evita duplicados y conserva el estado de seguimiento del usuario.
- Que la cobertura inicial del MVP esta acotada a fuentes `MVP`, `Posterior` y `Por definir`.
- Que la priorizacion de fuentes reales oficiales para recopilacion ya esta visible y ordenada por `Ola 1`, `Ola 2` y `Ola 3`.
- Que las alertas tempranas reutilizan los mismos filtros que el catalogo, se pueden crear, editar y desactivar, y registran coincidencias internas accionables.
- Que la regla de relevancia TI muestra inclusiones, exclusiones y casos frontera auditables.
- Que la gestion administrativa de usuarios permite listar cuentas, aplicar filtros, crear usuarios, ver detalle y ejecutar acciones de alta, edicion, activacion, desactivacion, baja logica, reenvio de invitacion y reinicio de acceso segun el rol activo, con persistencia en PostgreSQL.
- Que la matriz de permisos y los KPIs reflejan el alcance operativo de cada rol sin introducir autenticacion real.

## Recorrido recomendado para una revision funcional
1. Abre `/` y revisa el listado de oportunidades visibles.
2. Aplica filtros por palabra clave, procedimiento, ubicacion o presupuesto para comprobar el refinamiento del catalogo.
3. Prueba un rango invalido con `presupuesto_min` mayor que `presupuesto_max` y verifica que el sistema pide correccion.
4. Entra en una ficha desde el titulo de una oportunidad para comprobar presupuesto, fecha limite, estado oficial y enlace a la fuente cuando existan.
5. Abre `/datos-consolidados` para revisar las tres pestañas del Excel versionado y su trazabilidad al fichero de origen.
6. Abre `/pipeline` para guardar una oportunidad, comprobar que no se duplica y mover su estado de seguimiento.
7. Abre `/usuarios` para revisar el listado, el alta, el detalle y las acciones administrativas de cuentas.
8. Abre `/alertas` para revisar como se guardan, editan y desactivan alertas con los mismos filtros del catalogo.
9. Abre `/cobertura-fuentes` para confirmar que la cobertura comunicada sigue siendo parcial y priorizada.
10. Abre `/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen oficial.
11. Abre `/clasificacion-ti` para entender por que una oportunidad entra, se excluye o queda como caso frontera.
12. Abre `/kpis` y `/permisos` para comprobar el alcance visible por rol.

## Que no esta disponible hoy en `main`
- Autenticacion real, SSO o MFA.
- Snapshots Atom versionados en `data/`; la reproduccion completa de `PB-011` necesita muestras temporales o externas.
- Notificaciones salientes de alertas.
- Despliegue productivo endurecido.

## Como interpretar la documentacion funcional
Los documentos de `product-manager/` siguen siendo la fuente funcional para vision, backlog, historias y casos de uso. Deben leerse como alcance esperado del producto, no como evidencia de que esas funcionalidades ya esten disponibles en esta entrega. Cuando contradigan a `main`, prevalece la evidencia reproducible de la rama actual.

## Limitaciones relevantes para usuario
- Las superficies actuales permiten descubrimiento inicial, filtrado funcional, revision de detalle y gestion interna de alertas, pero no cubren todavia seguimiento operativo ni pipeline.
- Las superficies actuales permiten descubrimiento inicial, filtrado funcional, revision de detalle, seguimiento operativo, datos consolidados y gestion interna de alertas.
- La gestion administrativa de usuarios esta disponible para roles con permisos y persiste en PostgreSQL, pero no existe todavia autenticacion real contra proveedor externo, SSO ni MFA.
- La priorizacion de fuentes reales oficiales ya es accesible en una superficie propia y el pipeline ya esta disponible; las alertas siguen siendo internas y no envian notificaciones salientes.
- Los filtros actuales actuan solo sobre el catalogo visible y su API; no existe todavia una persistencia de preferencias separada del registro de alertas internas.
- La cobertura visible sigue siendo parcial y no debe interpretarse como rastreo exhaustivo de todo el ecosistema canario.
- El backend PostgreSQL es el modo operativo por defecto y el modo `file` queda como apoyo de pruebas; cuando no hay Atom versionado en `data/`, ese respaldo se apoya en `data/opportunities.json`.
- La consolidacion de `PB-011` sigue siendo la referencia funcional, pero su reproduccion automatizada depende de aportar muestras Atom al arbol o de usar las pruebas temporales del proyecto.
- La metadata tecnica del paquete sigue describiendo una release anterior mas limitada que la visible hoy en `main`.
- `product-manager/` sigue siendo la fuente funcional de alcance esperado, pero la evidencia reproducible de `main` ya incluye `PB-005` y `PB-012`.
- Las alertas visibles en `main` son internas: registran coincidencias accionables, pero todavia no envian notificaciones salientes.
- La superficie de datos consolidados ya esta presente, pero su reproducibilidad completa sigue dependiendo del Excel versionado y de la trazabilidad del fichero de origen.
- El pipeline conserva su estado por usuario y por oportunidad, pero no equivale a notificaciones ni a automatizaciones externas.

## Recomendacion de uso
Para demos o revision funcional temprana, utiliza el catalogo en `/`, la ficha de detalle de una oportunidad visible, `datos-consolidados`, `pipeline`, la gestion de alertas y, como apoyo, las vistas de cobertura, priorizacion, clasificacion TI, KPIs y permisos. Para capacidades de negocio pendientes, toma como referencia `product-manager/roadmap.md` y `product-manager/product-backlog.md`.
