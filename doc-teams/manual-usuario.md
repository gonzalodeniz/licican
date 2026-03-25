# Manual de usuario

## Publico objetivo
Stakeholder funcional, producto o persona usuaria interna que necesita entender que se puede consultar hoy en la rama `main`.

## Estado actual para usuario
La rama `main` expone una entrega minima navegable orientada a descubrimiento inicial y validacion funcional temprana, no un producto de uso final completo.

## Que si existe hoy
- Un catalogo inicial de oportunidades TI en `/`.
- Una API JSON del catalogo en `/api/oportunidades`.
- Filtros funcionales en el catalogo y en `/api/oportunidades` por palabra clave, presupuesto, procedimiento y ubicacion.
- Una ficha HTML de detalle por oportunidad en `/oportunidades/<id>`.
- Una API JSON del detalle en `/api/oportunidades/<id>`.
- Una vista HTML de cobertura inicial del MVP en `/cobertura-fuentes`.
- Una salida JSON de esa cobertura en `/api/fuentes`.
- Una vista HTML de priorizacion de fuentes reales oficiales en `/priorizacion-fuentes-reales`.
- Una salida JSON de esa priorizacion en `/api/fuentes-prioritarias`.
- Una vista HTML de clasificacion TI auditable en `/clasificacion-ti`.
- Una salida JSON de reglas y ejemplos auditados en `/api/clasificacion-ti`.

## Que permite validar esta entrega
- Que el catalogo visible solo publica oportunidades clasificadas como TI y dentro de la cobertura MVP.
- Que el usuario puede filtrar el catalogo, ver los filtros activos y limpiar la busqueda.
- Que si el rango de presupuesto es invalido, la interfaz solicita corregirlo y no lo presenta como ausencia de resultados.
- Que cada oportunidad mantiene organismo, ubicacion, estado oficial, fecha limite y referencia a su fuente oficial.
- Que la ficha de detalle refleja el ultimo dato oficial visible cuando existe una rectificacion o modificacion publicada.
- Que la cobertura inicial del MVP esta acotada a fuentes `MVP`, `Posterior` y `Por definir`.
- Que la priorizacion de fuentes reales oficiales para recopilacion ya esta visible y ordenada por `Ola 1`, `Ola 2` y `Ola 3`.
- Que la regla de relevancia TI muestra inclusiones, exclusiones y casos frontera auditables.

## Recorrido recomendado para una revision funcional
1. Abre `/` y revisa el listado de oportunidades visibles.
2. Aplica filtros por palabra clave, procedimiento, ubicacion o presupuesto para comprobar el refinamiento del catalogo.
3. Prueba un rango invalido con `presupuesto_min` mayor que `presupuesto_max` y verifica que el sistema pide correccion.
4. Entra en una ficha desde el titulo de una oportunidad para comprobar presupuesto, fecha limite, estado oficial y enlace a la fuente.
5. Abre `/cobertura-fuentes` para confirmar que la cobertura comunicada sigue siendo parcial y priorizada.
6. Abre `/priorizacion-fuentes-reales` para revisar la secuencia de recopilacion por olas y la trazabilidad minima al origen oficial.
7. Abre `/clasificacion-ti` para entender por que una oportunidad entra, se excluye o queda como caso frontera.

## Que no esta disponible hoy en `main`
- Alertas tempranas.
- Pipeline de seguimiento.
- Gestion de usuarios o autenticacion.
- La entrada de `changelog/2026-03-25.md` describe `PB-004` como entregado, pero en esta revision no hay rutas, datos ni pruebas visibles de esas capacidades en `main`.

## Como interpretar la documentacion funcional
Los documentos de `product-manager/` siguen siendo la fuente funcional para vision, backlog, historias y casos de uso. Deben leerse como alcance esperado del producto, no como evidencia de que esas funcionalidades ya esten disponibles en esta entrega.

## Limitaciones relevantes para usuario
- Las superficies actuales permiten descubrimiento inicial, filtrado funcional y revision de detalle, pero no cubren todavia seguimiento operativo ni alertas.
- La priorizacion de fuentes reales oficiales ya es accesible en una superficie propia, pero solo ordena la recopilacion; no activa alertas ni pipeline.
- Los filtros actuales actuan solo sobre el catalogo visible y su API; no existe todavia persistencia de preferencias ni alertas asociadas a esos criterios.
- La cobertura visible sigue siendo parcial y no debe interpretarse como rastreo exhaustivo de todo el ecosistema canario.
- La metadata tecnica del paquete sigue describiendo una release anterior mas limitada que la visible hoy en `main`.
- `product-manager/` sigue arrastrando algunos textos anteriores sobre `PB-009`; la evidencia reproducible de `main` y el changelog de `2026-03-24` deben tomarse como referencia para el estado vigente.
- La nota de `changelog/2026-03-25.md` sobre `PB-004` no se corresponde todavia con la superficie visible de `main`; hasta que se sincronicen codigo, pruebas y documentacion, esta guia solo reconoce lo que puede verificarse directamente.

## Recomendacion de uso
Para demos o revision funcional temprana, utiliza el catalogo en `/`, la ficha de detalle de una oportunidad visible y, como apoyo, las vistas de cobertura y clasificacion TI. Para capacidades de negocio pendientes, toma como referencia `product-manager/roadmap.md` y `product-manager/product-backlog.md`.
