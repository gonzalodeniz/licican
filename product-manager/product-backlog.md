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

## Estado de referencia de backlog
- Fecha de corte funcional: 2026-03-21.
- `PB-002` queda cerrado administrativamente: `qa-teams` lo valido en la issue #4 y su entrega se integrara en `main` junto con `PB-001` desde la rama tecnica ya validada.
- `PB-001` queda cerrado administrativamente: `qa-teams` lo valido en la issue #3 y su entrega base ya viene incluida en la rama validada de `PB-002`.
- `PB-007` queda cerrado administrativamente: su alcance fue validado por `qa-teams` y esta integrado en `main`.
- `PB-006` queda cerrado administrativamente: `qa-teams` lo revalido en la issue #2 y la rama `feat/pb-006-clasificacion-ti-auditable` ya esta integrada en `main`.
- `PB-003` queda en `validado`: `qa-teams` valido la reentrega en la issue #5 el 2026-03-20 y no quedan defectos bloqueantes funcionales abiertos para su alcance.
- La issue #5 sigue abierta solo por cierre operativo pendiente: `developer-teams` debe fusionar en `main` la rama `developer-teams/issue-5-pb-003-filtros-catalogo` y borrarla antes de iniciar una nueva implementacion.
- En esta revision quedan cerradas dos decisiones de producto que ya no deben tratarse como preguntas abiertas:
  - Regla funcional para expedientes mixtos TI.
  - Tratamiento funcional minimo de oportunidades anuladas, desiertas, desistidas o modificadas.

## Backlog priorizado

| ID | Titulo | Descripcion | Prioridad | Valor de negocio | Criterios de aceptacion | Dependencias | Estado | Trazabilidad |
|---|---|---|---|---|---|---|---|---|
| PB-001 | Catalogo inicial de oportunidades TI de Canarias | El usuario debe poder consultar en un unico listado las licitaciones TI detectadas dentro de la cobertura MVP ya delimitada. | P0 | Permite validar la propuesta central de centralizacion y descubrimiento temprano. | 1. Existe un listado consultable de oportunidades TI. 2. Cada oportunidad muestra al menos titulo, organismo, ubicacion, presupuesto si existe, fecha limite y estado oficial del expediente si la fuente lo informa. 3. Solo se muestran oportunidades etiquetadas como TI segun reglas funcionales vigentes. 4. El usuario puede distinguir la fuente oficial de cada registro. 5. Si no hay oportunidades disponibles, se muestra un estado vacio claro. | PB-007, PB-006 | `cerrado` | HU-01, CU-01, issue #3 |
| PB-002 | Ficha de detalle de licitacion | El usuario debe acceder a una vista con la informacion critica de cada oportunidad para decidir si merece seguimiento. | P0 | Reduce tiempo de analisis y evita revisar manualmente el pliego completo para un primer filtro. | 1. Desde el catalogo se accede al detalle. 2. La ficha muestra presupuesto, plazo, procedimiento, criterios de adjudicacion, solvencia tecnica si esta disponible y enlace a la fuente oficial. 3. El usuario puede identificar la fecha limite, el organismo convocante y el estado oficial del expediente sin ambiguedad. 4. Si un dato no esta disponible en origen, se muestra como no informado. 5. Si la oportunidad fue modificada y la fuente publica nueva fecha limite u otra variable critica, la ficha muestra el ultimo dato oficial disponible. | PB-001 | `cerrado` | HU-02, CU-02, issue #4 |
| PB-003 | Filtros funcionales de busqueda | El usuario debe poder filtrar oportunidades por palabras clave, presupuesto, procedimiento y ubicacion. | P0 | Aumenta relevancia y hace util el volumen de datos agregado. | 1. El usuario puede aplicar filtros por palabra clave, rango de presupuesto, procedimiento y ubicacion. 2. El listado refleja los filtros activos. 3. El usuario puede limpiar los filtros. 4. Si no hay resultados, se muestra un estado vacio comprensible. 5. Si el usuario introduce un rango de presupuesto invalido, el sistema solicita corregirlo y no lo interpreta como una busqueda valida sin resultados. | PB-001 | `validado` | HU-03, CU-03, issue #5 |
| PB-006 | Reglas funcionales de clasificacion TI | El producto debe establecer reglas verificables para decidir si una oportunidad es relevante para tecnologia antes de ampliar el catalogo. | P0 | Reduce falsos positivos, evita debates posteriores con QA y protege la utilidad del catalogo. | 1. Existe un criterio funcional documentado de inclusion TI. 2. El criterio contempla CPVs, palabras clave y casos frontera. 3. Las exclusiones relevantes quedan explicitadas. 4. `qa-teams` puede contrastar una muestra representativa con estas reglas desde una superficie funcional verificable. | PB-007 | `cerrado` | HU-06, CU-08, issue #2 |
| PB-007 | Cobertura inicial de fuentes prioritarias | El MVP debe delimitar que fuentes oficiales entran en la primera entrega para evitar ambiguedad de alcance y expectativas incorrectas. | P0 | Permite planificar entrega incremental y medir cobertura real. | 1. Existe una lista priorizada de fuentes objetivo para la primera release. 2. Cada fuente tiene estado de inclusion objetivo: `MVP`, `Posterior` o `Por definir`. 3. La definicion queda alineada con roadmap y backlog. 4. La entrega no induce a pensar que existe cobertura total del ecosistema canario. | Ninguna | `cerrado` | HU-07, CU-06, issue #1 |
| PB-004 | Configuracion de alertas tempranas | El usuario debe poder definir alertas para recibir nuevas oportunidades relevantes sin busqueda manual recurrente. | P1 | Materializa la promesa diferencial de anticipacion y refuerza la recurrencia de uso. | 1. El usuario puede crear al menos una alerta con criterios de palabra clave, presupuesto, procedimiento y ubicacion. 2. El sistema deja visible que la alerta esta activa. 3. Cuando aparece una oportunidad que cumple los criterios, queda registrada para notificacion. 4. El usuario puede editar o desactivar la alerta. 5. Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no deben registrarse como nuevas coincidencias accionables. | PB-001, PB-003 | `nuevo` | HU-04, CU-04, issue #6 |
| PB-005 | Pipeline de seguimiento de oportunidades | El usuario debe poder guardar oportunidades y moverlas por estados de trabajo para coordinar su respuesta comercial o tecnica. | P1 | Favorece retencion y gestion del trabajo sobre oportunidades detectadas. | 1. El usuario puede guardar una oportunidad en su pipeline. 2. Puede asignar un estado entre `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`. 3. Puede consultar su pipeline con el estado actual de cada oportunidad. 4. El cambio de estado queda reflejado de forma consistente y sin duplicados. 5. Si la fuente oficial marca la oportunidad como `anulada`, `desierta` o `desistida`, el pipeline conserva el registro del usuario y muestra una advertencia visible de estado oficial. | PB-001, PB-002 | `nuevo` | HU-05, CU-05, issue #7 |
| PB-008 | Medicion basica de valor del producto | El producto debe definir como medir cobertura, adopcion y uso de alertas desde las primeras releases. | P2 | Permite evaluar si el producto confirma la vision y orientar iteraciones posteriores. | 1. Existen KPIs basicos definidos por release. 2. Cada KPI tiene definicion, formula y decision asociada. 3. Los KPIs no bloquean el MVP funcional. | PB-001, PB-004 | `nuevo` | HU-08, CU-07, issue #8 |

## Decisiones funcionales vigentes que impactan backlog
- Un expediente mixto se considera TI para el MVP cuando cumple al menos una de estas condiciones:
  - el objeto principal o el entregable dominante menciona de forma explicita software, sistemas, ciberseguridad, redes, cloud, datos, licencias o infraestructura TIC
  - el CPV principal es tecnologico
  - la parte TI representa una porcion sustancial del valor esperado y es indispensable para cumplir el objeto del contrato
- Si un expediente mixto solo contiene TI accesoria o secundaria y la fuente no aporta evidencia suficiente para considerarla sustancial, debe quedar fuera del catalogo del MVP o tratarse como caso frontera pendiente de refinamiento.
- Cuando una oportunidad pase a `anulada`, `desierta` o `desistida`, el producto debe conservar la referencia historica y mostrar el estado oficial visible; no debe seguir tratandola como oportunidad nueva activa.
- Cuando una oportunidad sea modificada o rectificada, el producto debe mantener la misma referencia funcional si el expediente sigue siendo el mismo y exponer el ultimo dato oficial disponible en variables criticas.

## Orden recomendado para `developer-teams`
1. Completar merge a `main` y borrado de rama de PB-003 en la issue #5.
2. PB-004
3. PB-005
4. PB-008

## Notas de priorizacion
- `PB-007` y `PB-006` ya cumplieron su objetivo y quedan cerrados administrativamente tras validacion e integracion en `main`.
- `PB-001`, `PB-002` y `PB-003` ya quedaron validados por `qa-teams`; Release 1 queda funcionalmente validada y solo resta cerrar la integracion operativa de la issue #5 antes de abrir nuevo trabajo tecnico.
- `PB-004` y `PB-005` extienden el valor diferencial y la retencion tras validar descubrimiento.
- `PB-008` queda fuera del camino critico del MVP, pero debe prepararse antes de una ampliacion comercial o de cobertura.

## Riesgos y dependencias abiertas
- Sigue abierta la dependencia de negocio sobre si los ayuntamientos deben entrar en la promesa comercial de primera release o mantenerse en fase posterior.
- Existe riesgo de falsa expectativa si la comunicacion comercial usa lenguaje de cobertura total en lugar de cobertura inicial priorizada.
- Existe riesgo de falsos positivos si desarrollo interpreta de forma demasiado laxa el criterio de "porcion sustancial" en expedientes mixtos.
- Existe riesgo operativo si `developer-teams` inicia `PB-004` antes de fusionar y borrar la rama validada de `PB-003`, porque incumpliria la secuencia acordada entre roles.

## Preguntas abiertas para siguiente iteracion
- Que umbral comercial debe exigirse para considerar suficiente la cobertura MVP antes de ampliar a ayuntamientos.
- Que indicadores minimos deben fijarse como puerta de inversion posterior en alertas salientes y monetizacion.
