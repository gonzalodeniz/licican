# Historias de Usuario de PodencoTI

## Convenciones
- Cada historia enlaza con backlog, caso de uso e issue de GitHub cuando existe.
- Los criterios de aceptacion estan redactados para validacion funcional por `qa-teams`.

## HU-01 Ver oportunidades TI centralizadas
- Backlog relacionado: PB-001
- Caso de uso relacionado: CU-01
- Issue relacionado: #3
- Historia:
  Como empresa o profesional TI,
  quiero ver en un unico catalogo las oportunidades de contratacion publica relevantes en Canarias,
  para detectar licitaciones a tiempo sin revisar manualmente multiples portales.
- Criterios de aceptacion:
  1. El catalogo muestra solo oportunidades clasificadas como TI.
  2. Cada oportunidad muestra titulo, organismo, ubicacion, procedimiento si existe, presupuesto si existe y fecha limite.
  3. El usuario puede identificar la fuente oficial de cada oportunidad.
  4. Si no hay oportunidades disponibles, se muestra un mensaje claro de estado vacio.
- Dependencias funcionales: PB-007, PB-006
- Prioridad: P0
- Estado: `nuevo`

## HU-02 Evaluar una licitacion desde su ficha
- Backlog relacionado: PB-002
- Caso de uso relacionado: CU-02
- Issue relacionado: #4
- Historia:
  Como empresa o profesional TI,
  quiero consultar una ficha resumida de cada licitacion,
  para decidir rapido si debo incorporarla a mi proceso comercial o tecnico.
- Criterios de aceptacion:
  1. Desde el catalogo se puede acceder al detalle de una oportunidad.
  2. La ficha muestra como minimo presupuesto, fecha limite, procedimiento, organismo convocante y enlace a la fuente oficial.
  3. Si hay datos de solvencia tecnica o criterios de adjudicacion, se muestran de forma diferenciada.
  4. Si un dato no esta disponible en la fuente, se indica como no informado.
- Dependencias funcionales: PB-001
- Prioridad: P0
- Estado: `nuevo`

## HU-03 Filtrar oportunidades relevantes
- Backlog relacionado: PB-003
- Caso de uso relacionado: CU-03
- Issue relacionado: #5
- Historia:
  Como empresa o profesional TI,
  quiero filtrar las oportunidades por criterios de negocio,
  para quedarme solo con las que encajan con mi capacidad y estrategia.
- Criterios de aceptacion:
  1. El usuario puede filtrar por palabra clave.
  2. El usuario puede filtrar por rango de presupuesto.
  3. El usuario puede filtrar por tipo de procedimiento y ubicacion.
  4. Los filtros activos se ven en pantalla y pueden limpiarse.
  5. Si no hay resultados, se muestra un estado vacio comprensible.
- Dependencias funcionales: PB-001
- Prioridad: P0
- Estado: `nuevo`

## HU-04 Recibir alertas tempranas
- Backlog relacionado: PB-004
- Caso de uso relacionado: CU-04
- Issue relacionado: #6
- Historia:
  Como empresa o profesional TI,
  quiero configurar alertas sobre nuevos contratos relevantes,
  para enterarme antes y preparar mejor una oferta.
- Criterios de aceptacion:
  1. El usuario puede crear una alerta con al menos un criterio funcional.
  2. El sistema permite editar y desactivar la alerta.
  3. La alerta queda visible como activa tras guardarse.
  4. Las nuevas oportunidades compatibles quedan asociadas a la alerta para su futura notificacion.
- Dependencias funcionales: PB-001, PB-003
- Prioridad: P1
- Estado: `nuevo`

## HU-05 Hacer seguimiento de oportunidades en pipeline
- Backlog relacionado: PB-005
- Caso de uso relacionado: CU-05
- Issue relacionado: #7
- Historia:
  Como empresa o profesional TI,
  quiero guardar oportunidades y moverlas por estados,
  para gestionar mi trabajo de seguimiento y preparacion de ofertas.
- Criterios de aceptacion:
  1. El usuario puede guardar una oportunidad en su pipeline.
  2. La oportunidad guardada recibe un estado inicial.
  3. El usuario puede cambiarla a `Evaluando`, `Preparando oferta`, `Presentada` o `Descartada`.
  4. Una oportunidad no se duplica en el pipeline del mismo usuario.
- Dependencias funcionales: PB-001, PB-002
- Prioridad: P1
- Estado: `nuevo`

## HU-06 Disponer de reglas auditables de relevancia TI
- Backlog relacionado: PB-006
- Caso de uso relacionado: CU-01
- Issue relacionado: #2
- Historia:
  Como responsable de producto y validacion,
  quiero tener reglas funcionales explicitas para clasificar oportunidades TI,
  para reducir ambiguedad, falsos positivos y discusiones durante desarrollo y QA.
- Criterios de aceptacion:
  1. Existe un documento funcional con criterios de inclusion y exclusion.
  2. Los criterios incluyen CPVs, palabras clave y casos frontera.
  3. `qa-teams` puede validar una muestra de ejemplos con esos criterios.
  4. El backlog y los issues hacen referencia a estas reglas.
- Dependencias funcionales: PB-007
- Prioridad: P0
- Estado: `nuevo`

## HU-07 Delimitar la cobertura inicial de fuentes
- Backlog relacionado: PB-007
- Caso de uso relacionado: CU-06
- Issue relacionado: #1
- Historia:
  Como responsable de producto,
  quiero definir las fuentes oficiales que entran en la primera release,
  para evitar expectativas no alineadas sobre cobertura y plazos.
- Criterios de aceptacion:
  1. Existe una lista priorizada de fuentes objetivo para MVP.
  2. Cada fuente tiene un estado de inclusion esperado.
  3. La lista esta alineada con backlog y roadmap.
  4. La entrega no comunica cobertura total cuando no existe.
- Dependencias funcionales: ninguna
- Prioridad: P0
- Estado: `validado`
- Nota de estado: validado por `qa-teams` en la issue #1; pendiente de cierre administrativo cuando se resuelva su integracion final.

## HU-08 Medir cobertura y uso inicial del producto
- Backlog relacionado: PB-008
- Caso de uso relacionado: CU-07
- Issue relacionado: #8
- Historia:
  Como responsable de producto,
  quiero definir KPIs basicos desde las primeras releases,
  para evaluar si el producto esta aportando valor real.
- Criterios de aceptacion:
  1. Se define al menos un KPI de cobertura, uno de adopcion y uno de uso.
  2. Cada KPI tiene formula, umbral inicial y decision asociada.
  3. El equipo puede revisar estos KPIs sin bloquear el MVP funcional.
- Dependencias funcionales: PB-001, PB-004
- Prioridad: P2
- Estado: `nuevo`
