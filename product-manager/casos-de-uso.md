# Casos de Uso de PodencoTI

## Convenciones de trazabilidad
- Cada caso de uso referencia backlog e historias relacionadas.
- Las reglas de negocio `RB-*` sirven como base de verificacion funcional para `qa-teams`.

## CU-01 Consultar catalogo de oportunidades TI
- Backlog relacionado: PB-001, PB-006
- Historias relacionadas: HU-01, HU-06
- Actor principal: Usuario registrado de PodencoTI.
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
- Postcondiciones:
  - El usuario ha identificado una o varias oportunidades potencialmente relevantes.
- Reglas de negocio relacionadas:
  - RB-01 Solo deben mostrarse oportunidades clasificadas como TI.
  - RB-02 Cada oportunidad debe conservar referencia a la fuente oficial.
  - RB-03 Solo deben aparecer oportunidades cuya fuente este dentro del alcance funcional vigente.

## CU-02 Revisar el detalle de una licitacion
- Backlog relacionado: PB-002
- Historias relacionadas: HU-02
- Actor principal: Usuario registrado de PodencoTI.
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
- Postcondiciones:
  - El usuario dispone de informacion suficiente para una decision inicial.
- Reglas de negocio relacionadas:
  - RB-04 La fecha limite debe ser visible de forma prioritaria.
  - RB-05 El enlace a la fuente oficial debe estar disponible siempre que exista.

## CU-03 Filtrar oportunidades
- Backlog relacionado: PB-003
- Historias relacionadas: HU-03
- Actor principal: Usuario registrado de PodencoTI.
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
- Actor principal: Usuario registrado de PodencoTI.
- Objetivo: Recibir nuevas oportunidades sin tener que revisar manualmente todas las fuentes.
- Disparador: El usuario decide crear una alerta.
- Precondiciones:
  - El usuario tiene acceso a la gestion de alertas.
  - El catalogo y los criterios de filtrado ya estan disponibles.
- Flujo principal:
  1. El usuario crea una alerta con criterios funcionales.
  2. El sistema confirma que la alerta queda activa.
  3. Cuando aparecen nuevas oportunidades compatibles, el sistema las asocia a la alerta.
  4. El usuario consulta o modifica la alerta cuando lo necesita.
- Flujos alternativos:
  - A1. Si el usuario intenta guardar una alerta sin criterios minimos, el sistema solicita completarlos.
  - A2. Si existen varias alertas solapadas, el sistema permite mantenerlas sin duplicar el mensaje de configuracion.
- Postcondiciones:
  - El usuario dispone de al menos una alerta activa.
- Reglas de negocio relacionadas:
  - RB-08 Una alerta puede activarse, editarse o desactivarse.
  - RB-09 La configuracion de alertas debe reutilizar los mismos criterios funcionales que el filtrado del catalogo.

## CU-05 Gestionar pipeline de oportunidades
- Backlog relacionado: PB-005
- Historias relacionadas: HU-05
- Actor principal: Usuario registrado de PodencoTI.
- Objetivo: Hacer seguimiento del estado de trabajo de cada licitacion relevante.
- Disparador: El usuario decide guardar una oportunidad en su pipeline.
- Precondiciones:
  - La oportunidad existe y es visible para el usuario.
- Flujo principal:
  1. El usuario guarda una oportunidad en su pipeline.
  2. El sistema la asigna a un estado inicial.
  3. El usuario cambia el estado segun avanza su proceso interno.
  4. El usuario consulta el pipeline para conocer el estado de sus oportunidades.
- Flujos alternativos:
  - A1. Si la oportunidad ya estaba guardada, el sistema evita duplicados y permite actualizar su estado.
  - A2. Si el usuario decide descartarla, el sistema conserva el registro en estado `Descartada`.
- Postcondiciones:
  - La oportunidad queda gestionada en el pipeline del usuario.
- Reglas de negocio relacionadas:
  - RB-10 Los estados minimos del pipeline son `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
  - RB-11 Una misma oportunidad no debe duplicarse en el pipeline del mismo usuario.

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
