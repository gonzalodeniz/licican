# Product Backlog de PodencoTI

## Objetivo
Traducir la vision de PodencoTI en trabajo priorizado, trazable y ejecutable para `developer-teams`, manteniendo alineacion con la validacion posterior de `qa-teams`.

## Escala de prioridad
- `P0`: imprescindible para validar el MVP de descubrimiento.
- `P1`: alto valor tras validar el MVP de descubrimiento.
- `P2`: mejora relevante, util para aprendizaje o escalado, pero no bloqueante.

## Estado operativo comun
- `nuevo`: item preparado por producto y disponible para que `developer-teams` lo tome.
- `en desarrollo`: item tomado por `developer-teams`.
- `listo para qa`: item implementado y pendiente de validacion funcional.
- `no validado`: item revisado por `qa-teams` con hallazgos bloqueantes o incumplimientos.
- `validado`: item aceptado por `qa-teams`.
- `cerrado`: item validado, integrado y cerrado administrativamente por `product-manager`.

## Backlog priorizado

| ID | Titulo | Descripcion | Prioridad | Valor de negocio | Criterios de aceptacion | Dependencias | Estado | Trazabilidad |
|---|---|---|---|---|---|---|---|---|
| PB-006 | Reglas funcionales de clasificacion TI | El producto debe establecer reglas verificables para decidir si una oportunidad es relevante para tecnologia antes de ampliar el catalogo. | P0 | Reduce falsos positivos, evita debates posteriores con QA y protege la utilidad del catalogo. | 1. Existe un criterio funcional documentado de inclusion TI. 2. El criterio contempla CPVs, palabras clave y casos frontera. 3. Las exclusiones relevantes quedan explicitadas. 4. `qa-teams` puede contrastar una muestra representativa con estas reglas. | PB-007 | `nuevo` | HU-06, CU-01, issue #2 |
| PB-001 | Catalogo inicial de oportunidades TI de Canarias | El usuario debe poder consultar en un unico listado las licitaciones TI detectadas dentro de la cobertura MVP ya delimitada. | P0 | Permite validar la propuesta central de centralizacion y descubrimiento temprano. | 1. Existe un listado consultable de oportunidades TI. 2. Cada oportunidad muestra al menos titulo, organismo, ubicacion, presupuesto si existe, fecha limite y estado. 3. Solo se muestran oportunidades etiquetadas como TI segun reglas funcionales vigentes. 4. El usuario puede distinguir la fuente oficial de cada registro. 5. Si no hay oportunidades disponibles, se muestra un estado vacio claro. | PB-007, PB-006 | `nuevo` | HU-01, CU-01, issue #3 |
| PB-002 | Ficha de detalle de licitacion | El usuario debe acceder a una vista con la informacion critica de cada oportunidad para decidir si merece seguimiento. | P0 | Reduce tiempo de analisis y evita revisar manualmente el pliego completo para un primer filtro. | 1. Desde el catalogo se accede al detalle. 2. La ficha muestra presupuesto, plazo, procedimiento, criterios de adjudicacion, solvencia tecnica si esta disponible y enlace a la fuente oficial. 3. El usuario puede identificar la fecha limite y el organismo convocante sin ambiguedad. 4. Si un dato no esta disponible en origen, se muestra como no informado. | PB-001 | `nuevo` | HU-02, CU-02, issue #4 |
| PB-003 | Filtros funcionales de busqueda | El usuario debe poder filtrar oportunidades por palabras clave, presupuesto, procedimiento y ubicacion. | P0 | Aumenta relevancia y hace util el volumen de datos agregado. | 1. El usuario puede aplicar filtros por palabra clave, rango de presupuesto, procedimiento y ubicacion. 2. El listado refleja los filtros activos. 3. El usuario puede limpiar los filtros. 4. Si no hay resultados, se muestra un estado vacio comprensible. | PB-001 | `nuevo` | HU-03, CU-03, issue #5 |
| PB-007 | Cobertura inicial de fuentes prioritarias | El MVP debe delimitar que fuentes oficiales entran en la primera entrega para evitar ambiguedad de alcance y expectativas incorrectas. | P0 | Permite planificar entrega incremental y medir cobertura real. | 1. Existe una lista priorizada de fuentes objetivo para la primera release. 2. Cada fuente tiene estado de inclusion objetivo: `MVP`, `Posterior` o `Por definir`. 3. La definicion queda alineada con roadmap y backlog. 4. La entrega no induce a pensar que existe cobertura total del ecosistema canario. | Ninguna | `validado` | HU-07, CU-06, issue #1 |
| PB-004 | Configuracion de alertas tempranas | El usuario debe poder definir alertas para recibir nuevas oportunidades relevantes sin busqueda manual recurrente. | P1 | Materializa la promesa diferencial de anticipacion y refuerza la recurrencia de uso. | 1. El usuario puede crear al menos una alerta con criterios de palabra clave, presupuesto, procedimiento y ubicacion. 2. El sistema deja visible que la alerta esta activa. 3. Cuando aparece una oportunidad que cumple los criterios, queda registrada para notificacion. 4. El usuario puede editar o desactivar la alerta. | PB-001, PB-003 | `nuevo` | HU-04, CU-04, issue #6 |
| PB-005 | Pipeline de seguimiento de oportunidades | El usuario debe poder guardar oportunidades y moverlas por estados de trabajo para coordinar su respuesta comercial o tecnica. | P1 | Favorece retencion y gestion del trabajo sobre oportunidades detectadas. | 1. El usuario puede guardar una oportunidad en su pipeline. 2. Puede asignar un estado entre `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`. 3. Puede consultar su pipeline con el estado actual de cada oportunidad. 4. El cambio de estado queda reflejado de forma consistente y sin duplicados. | PB-001, PB-002 | `nuevo` | HU-05, CU-05, issue #7 |
| PB-008 | Medicion basica de valor del producto | El producto debe definir como medir cobertura, adopcion y uso de alertas desde las primeras releases. | P2 | Permite evaluar si el producto confirma la vision y orientar iteraciones posteriores. | 1. Existen KPIs basicos definidos por release. 2. Cada KPI tiene definicion, formula y decision asociada. 3. Los KPIs no bloquean el MVP funcional. | PB-001, PB-004 | `nuevo` | HU-08, CU-07, issue #8 |

## Orden recomendado para `developer-teams`
1. PB-006
2. PB-001
3. PB-002
4. PB-003
5. PB-004
6. PB-005
7. PB-008

## Notas de priorizacion
- `PB-007` ya esta validado por `qa-teams`; permanece trazado como base funcional del MVP y no debe reabrirse salvo cambio de alcance.
- `PB-006` es el siguiente item recomendado porque reduce ambiguedad antes de construir el catalogo visible de oportunidades.
- `PB-001`, `PB-002` y `PB-003` conforman el MVP navegable minimo para validar descubrimiento y primera evaluacion.
- `PB-004` y `PB-005` extienden el valor diferencial y la retencion tras validar descubrimiento.
- `PB-008` queda fuera del camino critico del MVP, pero debe prepararse antes de una ampliacion comercial o de cobertura.

## Huecos funcionales pendientes de cerrar
- Aun no esta fijada la definicion operativa de caso frontera para expedientes mixtos donde TI sea minoritaria.
- Falta decidir si la primera iteracion de alertas registra coincidencias de forma interna o si ya incluye notificacion saliente.
- Falta decidir si el pipeline es individual por usuario desde el inicio o si se reserva la colaboracion por empresa para una release posterior.
