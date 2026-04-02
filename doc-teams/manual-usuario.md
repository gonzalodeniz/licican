# Manual de usuario

## Publico objetivo
Stakeholder funcional, producto o persona usuaria interna que necesita entender que se puede consultar hoy en la rama `main`.

## Estado actual para usuario
La rama `main` expone una entrega minima navegable orientada a descubrimiento inicial y validacion funcional temprana, no un producto de uso final completo.

## Que si existe hoy
- Un catalogo de oportunidades TI servido desde PostgreSQL por defecto y visible en `/`.
- Un respaldo `file` que usa `data/opportunities.json` cuando no hay snapshots Atom versionados en `data/`.
- Una API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales en el catalogo y en `/api/oportunidades` por palabra clave, presupuesto, procedimiento y ubicacion.
- Una ficha HTML de detalle por oportunidad en `/oportunidades/<id>`, con trazabilidad al origen funcional vigente de cada registro cuando la fuente lo permite.
- Una API JSON del detalle en `/api/oportunidades/<id>`.
- Una gestion HTML de alertas tempranas en `/alertas`.
- Una API JSON de alertas persistidas y coincidencias internas en `/api/alertas`.
- Una gestion administrativa de usuarios en `/usuarios`.
- Una API JSON de usuarios en `/api/usuarios`.
- Una vista HTML de cobertura inicial del MVP en `/cobertura-fuentes`.
- Una salida JSON de esa cobertura en `/api/fuentes`.
- Una vista HTML de priorizacion de fuentes reales oficiales en `/priorizacion-fuentes-reales`.
- Una salida JSON de esa priorizacion en `/api/fuentes-prioritarias`.
- Una vista HTML de clasificacion TI auditable en `/clasificacion-ti`.
- Una salida JSON de reglas y ejemplos auditados en `/api/clasificacion-ti`.

## Que permite validar esta entrega
- Que el catalogo visible solo publica oportunidades clasificadas como TI y dentro de la cobertura vigente.
- Que el usuario puede filtrar el catalogo, ver los filtros activos y limpiar la busqueda.
- Que si el rango de presupuesto es invalido, la interfaz solicita corregirlo y no lo presenta como ausencia de resultados.
- Que cada oportunidad mantiene organismo, ubicacion, estado oficial, fecha limite y referencia a su fuente oficial cuando esa informacion existe en el origen.
- Que la ficha de detalle refleja el ultimo dato oficial visible cuando existe una rectificacion o modificacion publicada.
- Que la cobertura inicial del MVP esta acotada a fuentes `MVP`, `Posterior` y `Por definir`.
- Que la priorizacion de fuentes reales oficiales para recopilacion ya esta visible y ordenada por `Ola 1`, `Ola 2` y `Ola 3`.
- Que las alertas tempranas reutilizan los mismos filtros que el catalogo, se pueden crear, editar y desactivar, y registran coincidencias internas accionables.
- Que la regla de relevancia TI muestra inclusiones, exclusiones y casos frontera auditables.
- Que la gestion administrativa de usuarios permite listar cuentas, aplicar filtros, crear usuarios, ver detalle y ejecutar acciones de alta, edicion, activacion, desactivacion, baja logica, reenvio de invitacion y reinicio de acceso segun el rol activo.

## Recorrido recomendado para una revision funcional
1. Abre `/` y revisa el listado de oportunidades visibles.
2. Aplica filtros por palabra clave, procedimiento, ubicacion o presupuesto para comprobar el refinamiento del catalogo.
3. Prueba un rango invalido con `presupuesto_min` mayor que `presupuesto_max` y verifica que el sistema pide correccion.
4. Entra en una ficha desde el titulo de una oportunidad para comprobar presupuesto, fecha limite, estado oficial y enlace a la fuente cuando existan.
5. Abre `/usuarios` para revisar el listado, el alta, el detalle y las acciones administrativas de cuentas.
6. Abre `/alertas` para revisar como se guardan, editan y desactivan alertas con los mismos filtros del catalogo.
7. Abre `/cobertura-fuentes` para confirmar que la cobertura comunicada sigue siendo parcial y priorizada.
8. Abre `/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen oficial.
9. Abre `/clasificacion-ti` para entender por que una oportunidad entra, se excluye o queda como caso frontera.

## Que no esta disponible hoy en `main`
- Pipeline de seguimiento.
- Autenticacion real, SSO o MFA.
- La superficie funcional de `PB-012` con las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
- Aunque el changelog de `2026-03-29` la menciona como validada, esa superficie de `PB-012` no aparece todavia en las rutas ni en las pruebas visibles de `main`; no debe comunicarse como disponible para usuario final hasta que el codigo la refleje.
- Aunque el changelog de `2026-03-31` menciona `pipeline` como validado, esa superficie tampoco aparece todavia en las rutas ni en las pruebas visibles de `main`; no debe comunicarse como disponible para usuario final hasta que el codigo la refleje.
- Snapshots Atom versionados en `data/`; la reproduccion completa de `PB-011` necesita muestras temporales o externas.

## Como interpretar la documentacion funcional
Los documentos de `product-manager/` siguen siendo la fuente funcional para vision, backlog, historias y casos de uso. Deben leerse como alcance esperado del producto, no como evidencia de que esas funcionalidades ya esten disponibles en esta entrega. Cuando contradigan a `main`, prevalece la evidencia reproducible de la rama actual.

## Limitaciones relevantes para usuario
- Las superficies actuales permiten descubrimiento inicial, filtrado funcional, revision de detalle y gestion interna de alertas, pero no cubren todavia seguimiento operativo ni pipeline.
- La gestion administrativa de usuarios esta disponible para roles con permisos, pero no existe todavia autenticacion real contra proveedor externo, SSO ni MFA.
- La priorizacion de fuentes reales oficiales ya es accesible en una superficie propia, pero solo ordena la recopilacion; no activa pipeline.
- Los filtros actuales actuan solo sobre el catalogo visible y su API; no existe todavia una persistencia de preferencias separada del registro de alertas internas.
- La cobertura visible sigue siendo parcial y no debe interpretarse como rastreo exhaustivo de todo el ecosistema canario.
- El backend PostgreSQL es el modo operativo por defecto y el modo `file` queda como apoyo de pruebas; cuando no hay Atom versionado en `data/`, ese respaldo se apoya en `data/opportunities.json`.
- La consolidacion de `PB-011` sigue siendo la referencia funcional, pero su reproduccion automatizada depende de aportar muestras Atom al arbol o de usar las pruebas temporales del proyecto.
- La metadata tecnica del paquete sigue describiendo una release anterior mas limitada que la visible hoy en `main`.
- `product-manager/` sigue arrastrando algunos textos anteriores a la integracion de `PB-011`; la evidencia reproducible de `main` y el changelog de `2026-03-29` deben tomarse como referencia para el estado vigente, salvo en `PB-012`, donde el changelog entra en contradiccion con el codigo y prevalece `main`.
- Las alertas visibles en `main` son internas: registran coincidencias accionables, pero todavia no envian notificaciones salientes.
- La superficie de `PB-012` sigue pendiente: no aparecen todavia las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` ni `Adjudicaciones`.
- El changelog de `2026-03-29` contradice parcialmente ese estado al registrar `PB-012` como validada; mientras esa desalineacion no se resuelva con evidencia en `main`, la referencia valida para usuario es la ausencia de la superficie.
- El changelog de `2026-03-31` contradice ademas la ausencia de `pipeline`, pero la interfaz y la API siguen sin exponerla; la referencia valida para usuario sigue siendo que no esta disponible.

## Recomendacion de uso
Para demos o revision funcional temprana, utiliza el catalogo en `/`, la ficha de detalle de una oportunidad visible, la gestion de alertas en `/alertas` y, como apoyo, las vistas de cobertura y clasificacion TI. Para capacidades de negocio pendientes, toma como referencia `product-manager/roadmap.md` y `product-manager/product-backlog.md`.
