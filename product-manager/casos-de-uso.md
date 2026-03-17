# Casos de Uso de PodencoTI

## CU-01 Consultar catalogo de oportunidades TI
- Actor principal: Usuario registrado de PodencoTI.
- Objetivo: Descubrir en un solo lugar oportunidades de contratacion publica TI relevantes en Canarias.
- Disparador: El usuario accede al modulo principal de oportunidades.
- Precondiciones:
  - Existen oportunidades disponibles en el catalogo.
  - Las oportunidades han sido clasificadas como TI segun las reglas funcionales vigentes.
- Flujo principal:
  1. El usuario abre el catalogo de oportunidades.
  2. El sistema muestra un listado de oportunidades TI ordenadas por relevancia o actualidad.
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

## CU-02 Revisar el detalle de una licitacion
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
  - RB-03 La fecha limite debe ser visible de forma prioritaria.
  - RB-04 El enlace a la fuente oficial debe estar disponible siempre que exista.

## CU-03 Filtrar oportunidades
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
  - RB-05 Los filtros activos deben quedar visibles.
  - RB-06 La limpieza de filtros debe restaurar el listado completo disponible.

## CU-04 Configurar alertas tempranas
- Actor principal: Usuario registrado de PodencoTI.
- Objetivo: Recibir nuevas oportunidades sin tener que revisar manualmente todas las fuentes.
- Disparador: El usuario decide crear una alerta.
- Precondiciones:
  - El usuario tiene acceso a la gestion de alertas.
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
  - RB-07 Una alerta puede activarse, editarse o desactivarse.
  - RB-08 La configuracion de alertas debe reutilizar los mismos criterios funcionales que el filtrado del catalogo.

## CU-05 Gestionar pipeline de oportunidades
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
  - RB-09 Los estados minimos del pipeline son `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
  - RB-10 Una misma oportunidad no debe duplicarse en el pipeline del mismo usuario.
