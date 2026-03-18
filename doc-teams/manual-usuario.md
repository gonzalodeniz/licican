# Manual de usuario

## Publico objetivo
Stakeholder funcional, producto o persona usuaria interna que necesita entender que se puede consultar hoy en la rama `main`.

## Estado actual para usuario
La rama `main` expone una entrega minima navegable orientada a validacion funcional temprana, no un producto de uso final completo.

## Que si existe hoy
- Una vista HTML de cobertura inicial del MVP en `/`.
- Una salida JSON de esa cobertura en `/api/fuentes`.
- Una vista HTML de clasificacion TI auditable en `/clasificacion-ti`.
- Una salida JSON de reglas y ejemplos auditados en `/api/clasificacion-ti`.

## Que permite validar esta entrega
- Que la cobertura inicial del MVP esta acotada a fuentes `MVP`, `Posterior` y `Por definir`.
- Que la comunicacion del producto no presenta cobertura total del ecosistema canario.
- Que la regla de relevancia TI muestra inclusiones, exclusiones y casos frontera auditables antes del catalogo.

## Que no esta disponible hoy en `main`
- Catalogo de oportunidades TI.
- Ficha de detalle de licitacion.
- Filtros por palabra clave, presupuesto, procedimiento o ubicacion.
- Alertas tempranas.
- Pipeline de seguimiento.
- Gestion de usuarios o autenticacion.

## Como interpretar la documentacion funcional
Los documentos de `product-manager/` siguen siendo la fuente funcional para vision, backlog, historias y casos de uso. Deben leerse como alcance esperado del producto, no como evidencia de que esas funcionalidades ya esten disponibles en esta entrega.

## Limitaciones relevantes para usuario
- Las superficies actuales estan pensadas para validacion de cobertura y de regla TI, no para operar licitaciones reales extremo a extremo.
- Algunas entradas historicas del repositorio hablan de un catalogo ya validado, pero ese comportamiento no aparece en el codigo actual de `main`.

## Recomendacion de uso
Para demos o revision funcional temprana, utiliza las dos vistas HTML actuales. Para capacidades de negocio pendientes, toma como referencia `product-manager/roadmap.md` y `product-manager/product-backlog.md`.
