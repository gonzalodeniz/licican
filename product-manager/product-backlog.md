# Product Backlog de PodencoTI

## Objetivo
Traducir la vision de PodencoTI en trabajo priorizado, trazable y ejecutable para `developer-teams`.

## Escala de prioridad
- `P0`: imprescindible para validar el MVP.
- `P1`: alto valor tras el MVP inicial.
- `P2`: mejora relevante pero no bloqueante.

## Backlog priorizado

| ID | Titulo | Descripcion | Prioridad | Valor de negocio | Criterios de aceptacion | Dependencias | Estado | Trazabilidad |
|---|---|---|---|---|---|---|---|---|
| PB-001 | Catalogo inicial de oportunidades TI de Canarias | Como base del producto, el usuario debe poder consultar en un unico listado las licitaciones TI detectadas en fuentes oficiales canarias. | P0 | Permite validar la propuesta central de centralizacion y descubrimiento temprano. | 1. Existe un listado consultable de oportunidades TI. 2. Cada oportunidad muestra al menos titulo, organismo, ubicacion, presupuesto si existe, fecha limite y estado. 3. Solo se muestran oportunidades etiquetadas como TI segun reglas funcionales definidas. 4. El usuario puede distinguir la fuente oficial de cada registro. | Ninguna | Pendiente | CU-01, HU-01 |
| PB-002 | Ficha de detalle de licitacion | El usuario debe acceder a una vista con la informacion critica de cada oportunidad para decidir si merece seguimiento. | P0 | Reduce tiempo de analisis y evita revisar manualmente el pliego completo para un primer filtro. | 1. Desde el listado se accede al detalle. 2. La ficha muestra presupuesto, plazo, procedimiento, criterios de adjudicacion, solvencia tecnica si esta disponible y enlace a la fuente oficial. 3. El usuario puede identificar la fecha limite y el organismo convocante sin ambiguedad. | PB-001 | Pendiente | CU-02, HU-02 |
| PB-003 | Filtros funcionales de busqueda | El usuario debe poder filtrar oportunidades por palabras clave, presupuesto, procedimiento y ubicacion. | P0 | Aumenta relevancia y hace util el volumen de datos agregado. | 1. El usuario puede aplicar filtros por palabra clave, rango de presupuesto, procedimiento y ubicacion. 2. El listado refleja los filtros activos. 3. El usuario puede limpiar los filtros. 4. Si no hay resultados, se muestra estado vacio comprensible. | PB-001 | Pendiente | CU-03, HU-03 |
| PB-004 | Configuracion de alertas tempranas | El usuario debe poder definir alertas para recibir nuevas oportunidades relevantes sin busqueda manual recurrente. | P1 | Materializa la promesa diferencial de anticipacion y recurrencia de uso. | 1. El usuario puede crear al menos una alerta con criterios de palabra clave, presupuesto, procedimiento y ubicacion. 2. El sistema deja visible que la alerta esta activa. 3. Cuando aparece una oportunidad que cumple los criterios, queda registrada para notificacion. 4. El usuario puede editar o desactivar la alerta. | PB-001, PB-003 | Pendiente | CU-04, HU-04 |
| PB-005 | Pipeline de seguimiento de oportunidades | El usuario debe poder guardar oportunidades y moverlas por estados de trabajo para coordinar su respuesta comercial o tecnica. | P1 | Favorece retencion y gestion del trabajo sobre oportunidades detectadas. | 1. El usuario puede guardar una oportunidad en su pipeline. 2. Puede asignar un estado entre `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`. 3. Puede consultar su pipeline con el estado actual de cada oportunidad. 4. El cambio de estado queda reflejado de forma consistente. | PB-001, PB-002 | Pendiente | CU-05, HU-05 |
| PB-006 | Reglas funcionales de clasificacion TI | El producto debe establecer reglas verificables para decidir si una oportunidad es relevante para tecnologia. | P0 | Reduce falsos positivos y da coherencia al catalogo inicial. | 1. Existe un criterio funcional documentado de inclusion TI. 2. El criterio contempla CPVs, palabras clave y casos frontera. 3. Las exclusiones relevantes quedan explicitadas. 4. Las reglas pueden ser auditadas por negocio y QA. | Ninguna | Pendiente | CU-01, HU-06 |
| PB-007 | Cobertura inicial de fuentes prioritarias | El MVP debe delimitar que fuentes oficiales entran en la primera entrega para evitar ambiguedad de alcance. | P0 | Permite planificar entrega incremental y medir cobertura real. | 1. Existe una lista priorizada de fuentes objetivo para la primera release. 2. Cada fuente tiene estado de inclusion objetivo: MVP, posterior o por definir. 3. La definicion queda alineada con roadmap y backlog. | Ninguna | Pendiente | HU-07 |
| PB-008 | Medicion basica de valor del producto | El producto debe definir como medir cobertura, adopcion y uso de alertas desde las primeras releases. | P2 | Permite evaluar si el producto confirma la vision y orientar iteraciones posteriores. | 1. Existen KPIs basicos definidos por release. 2. Cada KPI tiene definicion, formula y decision asociada. 3. Los KPIs no bloquean el MVP funcional. | PB-001, PB-004 | Pendiente | HU-08 |

## Orden recomendado para `developer-teams`
1. PB-007
2. PB-006
3. PB-001
4. PB-002
5. PB-003
6. PB-004
7. PB-005
8. PB-008

## Notas de priorizacion
- PB-007 y PB-006 reducen ambiguedad funcional antes de construir experiencia de usuario.
- PB-001, PB-002 y PB-003 conforman el MVP navegable minimo.
- PB-004 y PB-005 extienden el valor diferencial y la retencion.
- PB-008 se mantiene fuera del camino critico del primer MVP.
