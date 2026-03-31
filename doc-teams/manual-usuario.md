# Manual de usuario

## Publico objetivo
Stakeholder funcional, producto o persona usuaria interna que necesita entender que se puede consultar hoy en la rama `main`.

## Estado actual para usuario
La rama `main` expone una entrega minima navegable orientada a descubrimiento inicial y validacion funcional temprana, no un producto de uso final completo.

## Que si existe hoy
- Un catalogo de oportunidades TI servido desde PostgreSQL por defecto y visible en `/`, con modo `file` disponible como respaldo para pruebas aisladas.
- Una API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales en el catalogo y en `/api/oportunidades` por palabra clave, presupuesto, procedimiento y ubicacion.
- Una ficha HTML de detalle por oportunidad en `/oportunidades/<id>`, con trazabilidad al origen funcional vigente de cada registro.
- Una API JSON del detalle en `/api/oportunidades/<id>`.
- Una gestion HTML de alertas tempranas en `/alertas`.
- Una API JSON de alertas persistidas y coincidencias internas en `/api/alertas`.
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
- Que cada oportunidad mantiene organismo, ubicacion, estado oficial, fecha limite y referencia a su fuente oficial.
- Que la ficha de detalle refleja el ultimo dato oficial visible cuando existe una rectificacion o modificacion publicada.
- Que cada detalle muestra el origen funcional vigente cuando el backend lo permite y, en modo `file`, el nombre del fichero `.atom` origen de la version consolidada.
- Que la cobertura inicial del MVP esta acotada a fuentes `MVP`, `Posterior` y `Por definir`.
- Que la priorizacion de fuentes reales oficiales para recopilacion ya esta visible y ordenada por `Ola 1`, `Ola 2` y `Ola 3`.
- Que las alertas tempranas reutilizan los mismos filtros que el catalogo, se pueden crear, editar y desactivar, y registran coincidencias internas accionables.
- Que la regla de relevancia TI muestra inclusiones, exclusiones y casos frontera auditables.

## Recorrido recomendado para una revision funcional
1. Abre `/` y revisa el listado de oportunidades visibles.
2. Aplica filtros por palabra clave, procedimiento, ubicacion o presupuesto para comprobar el refinamiento del catalogo.
3. Prueba un rango invalido con `presupuesto_min` mayor que `presupuesto_max` y verifica que el sistema pide correccion.
4. Entra en una ficha desde el titulo de una oportunidad para comprobar presupuesto, fecha limite, estado oficial, enlace a la fuente y fichero `.atom` de origen.
5. Abre `/alertas` para revisar como se guardan, editan y desactivan alertas con los mismos filtros del catalogo.
6. Abre `/cobertura-fuentes` para confirmar que la cobertura comunicada sigue siendo parcial y priorizada.
7. Abre `/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen oficial.
8. Abre `/clasificacion-ti` para entender por que una oportunidad entra, se excluye o queda como caso frontera.

## Que no esta disponible hoy en `main`
- Pipeline de seguimiento.
- Gestion de usuarios o autenticacion.
- La superficie funcional de `PB-012` con las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
- Aunque el changelog de `2026-03-29` la menciona como validada, esa superficie de `PB-012` no aparece todavia en las rutas ni en las pruebas visibles de `main`; no debe comunicarse como disponible para usuario final hasta que el codigo la refleje.
- Aunque el changelog de `2026-03-31` menciona `pipeline` como validado, esa superficie tampoco aparece todavia en las rutas ni en las pruebas visibles de `main`; no debe comunicarse como disponible para usuario final hasta que el codigo la refleje.

## Como interpretar la documentacion funcional
Los documentos de `product-manager/` siguen siendo la fuente funcional para vision, backlog, historias y casos de uso. Deben leerse como alcance esperado del producto, no como evidencia de que esas funcionalidades ya esten disponibles en esta entrega. Cuando contradigan a `main`, prevalece la evidencia reproducible de la rama actual.

## Limitaciones relevantes para usuario
- Las superficies actuales permiten descubrimiento inicial, filtrado funcional, revision de detalle y gestion interna de alertas, pero no cubren todavia seguimiento operativo ni pipeline.
- La priorizacion de fuentes reales oficiales ya es accesible en una superficie propia, pero solo ordena la recopilacion; no activa pipeline.
- Los filtros actuales actuan solo sobre el catalogo visible y su API; no existe todavia una persistencia de preferencias separada del registro de alertas internas.
- La cobertura visible sigue siendo parcial y no debe interpretarse como rastreo exhaustivo de todo el ecosistema canario.
- El backend PostgreSQL es el modo operativo por defecto y el modo `file` queda como apoyo de pruebas; eso no implica cobertura total ni pipeline.
- La consolidacion de `PB-011` sigue siendo la referencia funcional, pero su reproduccion automatizada queda condicionada por la discrepancia entre `data/atom/` y el cargador que busca `data/*.atom`.
- La metadata tecnica del paquete sigue describiendo una release anterior mas limitada que la visible hoy en `main`.
- `product-manager/` sigue arrastrando algunos textos anteriores a la integracion de `PB-011`; la evidencia reproducible de `main` y el changelog de `2026-03-29` deben tomarse como referencia para el estado vigente, salvo en `PB-012`, donde el changelog entra en contradiccion con el codigo y prevalece `main`.
- Las alertas visibles en `main` son internas: registran coincidencias accionables, pero todavia no envian notificaciones salientes.
- La superficie de `PB-012` sigue pendiente: no aparecen todavia las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` ni `Adjudicaciones`.
- El changelog de `2026-03-29` contradice parcialmente ese estado al registrar `PB-012` como validada; mientras esa desalineacion no se resuelva con evidencia en `main`, la referencia valida para usuario es la ausencia de la superficie.
- El changelog de `2026-03-31` contradice ademas la ausencia de `pipeline`, pero la interfaz y la API siguen sin exponerla; la referencia valida para usuario sigue siendo que no esta disponible.

## Recomendacion de uso
Para demos o revision funcional temprana, utiliza el catalogo en `/`, la ficha de detalle de una oportunidad visible, la gestion de alertas en `/alertas` y, como apoyo, las vistas de cobertura y clasificacion TI. Para capacidades de negocio pendientes, toma como referencia `product-manager/roadmap.md` y `product-manager/product-backlog.md`.
