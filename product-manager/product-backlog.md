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
- Fecha de corte funcional: 2026-03-23.
- `PB-002` queda cerrado administrativamente: `qa-teams` lo valido en la issue #4 y su entrega se integrara en `main` junto con `PB-001` desde la rama tecnica ya validada.
- `PB-001` queda cerrado administrativamente: `qa-teams` lo valido en la issue #3 y su entrega base ya viene incluida en la rama validada de `PB-002`.
- `PB-007` queda cerrado administrativamente: su alcance fue validado por `qa-teams` y esta integrado en `main`.
- `PB-006` queda cerrado administrativamente: `qa-teams` lo revalido en la issue #2 y la rama `feat/pb-006-clasificacion-ti-auditable` ya esta integrada en `main`.
- `PB-003` queda cerrado administrativamente: `qa-teams` valido la reentrega en la issue #5 el 2026-03-20, `developer-teams` integro la rama en `main` el 2026-03-21 y `product-manager` cierra la issue tras verificar esa integracion.
- En esta revision quedan cerradas dos decisiones de producto que ya no deben tratarse como preguntas abiertas:
  - Regla funcional para expedientes mixtos TI.
  - Tratamiento funcional minimo de oportunidades anuladas, desiertas, desistidas o modificadas.
- Se incorpora `PB-009` para priorizar de forma explicita la recopilacion desde fuentes reales oficiales nominadas; esta necesidad no quedaba cubierta por `PB-007`, que solo delimitaba cobertura funcional.
- `PB-009` queda en `no validado`: `qa-teams` reviso la issue #9 el 2026-03-22 y bloqueo su cierre por desincronizacion de la rama `developer-teams/issue-9-pb-009-fuentes-reales` con `main`, con arrastre de borrados ajenos al alcance funcional.

## Backlog priorizado

| ID | Titulo | Descripcion | Prioridad | Valor de negocio | Criterios de aceptacion | Dependencias | Estado | Trazabilidad |
|---|---|---|---|---|---|---|---|---|
| PB-001 | Catalogo inicial de oportunidades TI de Canarias | El usuario debe poder consultar en un unico listado las licitaciones TI detectadas dentro de la cobertura MVP ya delimitada. | P0 | Permite validar la propuesta central de centralizacion y descubrimiento temprano. | 1. Existe un listado consultable de oportunidades TI. 2. Cada oportunidad muestra al menos titulo, organismo, ubicacion, presupuesto si existe, fecha limite y estado oficial del expediente si la fuente lo informa. 3. Solo se muestran oportunidades etiquetadas como TI segun reglas funcionales vigentes. 4. El usuario puede distinguir la fuente oficial de cada registro. 5. Si no hay oportunidades disponibles, se muestra un estado vacio claro. | PB-007, PB-006 | `cerrado` | HU-01, CU-01, issue #3 |
| PB-002 | Ficha de detalle de licitacion | El usuario debe acceder a una vista con la informacion critica de cada oportunidad para decidir si merece seguimiento. | P0 | Reduce tiempo de analisis y evita revisar manualmente el pliego completo para un primer filtro. | 1. Desde el catalogo se accede al detalle. 2. La ficha muestra presupuesto, plazo, procedimiento, criterios de adjudicacion, solvencia tecnica si esta disponible y enlace a la fuente oficial. 3. El usuario puede identificar la fecha limite, el organismo convocante y el estado oficial del expediente sin ambiguedad. 4. Si un dato no esta disponible en origen, se muestra como no informado. 5. Si la oportunidad fue modificada y la fuente publica nueva fecha limite u otra variable critica, la ficha muestra el ultimo dato oficial disponible. | PB-001 | `cerrado` | HU-02, CU-02, issue #4 |
| PB-003 | Filtros funcionales de busqueda | El usuario debe poder filtrar oportunidades por palabras clave, presupuesto, procedimiento y ubicacion. | P0 | Aumenta relevancia y hace util el volumen de datos agregado. | 1. El usuario puede aplicar filtros por palabra clave, rango de presupuesto, procedimiento y ubicacion. 2. El listado refleja los filtros activos. 3. El usuario puede limpiar los filtros. 4. Si no hay resultados, se muestra un estado vacio comprensible. 5. Si el usuario introduce un rango de presupuesto invalido, el sistema solicita corregirlo y no lo interpreta como una busqueda valida sin resultados. | PB-001 | `cerrado` | HU-03, CU-03, issue #5 |
| PB-006 | Reglas funcionales de clasificacion TI | El producto debe establecer reglas verificables para decidir si una oportunidad es relevante para tecnologia antes de ampliar el catalogo. | P0 | Reduce falsos positivos, evita debates posteriores con QA y protege la utilidad del catalogo. | 1. Existe un criterio funcional documentado de inclusion TI. 2. El criterio contempla CPVs, palabras clave y casos frontera. 3. Las exclusiones relevantes quedan explicitadas. 4. `qa-teams` puede contrastar una muestra representativa con estas reglas desde una superficie funcional verificable. | PB-007 | `cerrado` | HU-06, CU-08, issue #2 |
| PB-007 | Cobertura inicial de fuentes prioritarias | El MVP debe delimitar que fuentes oficiales entran en la primera entrega para evitar ambiguedad de alcance y expectativas incorrectas. | P0 | Permite planificar entrega incremental y medir cobertura real. | 1. Existe una lista priorizada de fuentes objetivo para la primera release. 2. Cada fuente tiene estado de inclusion objetivo: `MVP`, `Posterior` o `Por definir`. 3. La definicion queda alineada con roadmap y backlog. 4. La entrega no induce a pensar que existe cobertura total del ecosistema canario. | Ninguna | `cerrado` | HU-07, CU-06, issue #1 |
| PB-009 | Priorizacion de recopilacion desde fuentes reales oficiales | El producto debe priorizar que la recopilacion de contratos y concursos se haga sobre fuentes oficiales reales y verificables, empezando por boletines y portales con valor temprano para Canarias. | P0 | Refuerza la credibilidad del catalogo, reduce riesgo de datos irreales o desactualizados y acerca antes el producto a la propuesta de valor comercial. | 1. Existe una lista priorizada y ordenada de fuentes reales oficiales para recopilacion temprana. 2. La prioridad nombra de forma explicita `BOC` (`https://www.gobiernodecanarias.org/boc/`), `BOP Las Palmas` (`https://www.boplaspalmas.net/nbop2/index.php`) y `BOE` (`https://www.boe.es/`) y las clasifica como `Ola 1`, `Ola 2` o `Ola 3`. 3. La primera entrega de esta prioridad deja visible en una superficie verificable que cada oportunidad recopilada conserva, como minimo, fuente oficial, fecha de publicacion o equivalente, enlace oficial y estado oficial si la fuente lo informa. 4. La documentacion funcional deja explicito que alertas, pipeline y ampliacion de cobertura a nuevas administraciones quedan fuera de esta iteracion. 5. Existe al menos una issue ejecutable en GitHub para que `developer-teams` implemente esta prioridad con trazabilidad a `PB-007` y `PB-006`. | PB-007, PB-006 | `no validado` | HU-09, CU-09, issue #9 |
| PB-004 | Configuracion de alertas tempranas | El usuario debe poder definir alertas para recibir nuevas oportunidades relevantes sin busqueda manual recurrente. | P1 | Materializa la promesa diferencial de anticipacion y refuerza la recurrencia de uso. | 1. El usuario puede crear al menos una alerta con un criterio funcional valido entre palabra clave, presupuesto, procedimiento o ubicacion. 2. El sistema impide guardar una alerta vacia y solicita completar al menos un criterio. 3. El sistema deja visible que la alerta esta activa. 4. Cuando aparece una oportunidad que cumple los criterios, queda registrada para notificacion o consumo interno del MVP. 5. El usuario puede editar o desactivar la alerta. 6. Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no deben registrarse como nuevas coincidencias accionables. | PB-001, PB-003 | `nuevo` | HU-04, CU-04, issue #6 |
| PB-005 | Pipeline de seguimiento de oportunidades | El usuario debe poder guardar oportunidades y moverlas por estados de trabajo para coordinar su respuesta comercial o tecnica. | P1 | Favorece retencion y gestion del trabajo sobre oportunidades detectadas. | 1. El usuario puede guardar una oportunidad en su pipeline desde una superficie visible del catalogo o del detalle. 2. La oportunidad guardada entra por defecto en estado `Nueva`. 3. El usuario puede cambiarla a `Evaluando`, `Preparando oferta`, `Presentada` o `Descartada`. 4. Puede consultar su pipeline con el estado actual de cada oportunidad. 5. El cambio de estado queda reflejado de forma consistente y sin duplicados. 6. Si la fuente oficial marca la oportunidad como `anulada`, `desierta` o `desistida`, el pipeline conserva el registro del usuario y muestra una advertencia visible de estado oficial. | PB-001, PB-002 | `nuevo` | HU-05, CU-05, issue #7 |
| PB-008 | Medicion basica de valor del producto | El producto debe definir como medir cobertura, adopcion y uso de alertas desde las primeras releases. | P2 | Permite evaluar si el producto confirma la vision y orientar iteraciones posteriores. | 1. Existen KPIs basicos definidos por release. 2. Cada KPI tiene definicion, formula, umbral inicial y decision asociada. 3. La definicion documental de KPIs puede prepararse antes de que toda la instrumentacion este disponible. 4. Los KPIs no bloquean el MVP funcional. | PB-001, PB-004 | `nuevo` | HU-08, CU-07, issue #8 |

## Decisiones funcionales vigentes que impactan backlog
- Una alerta del MVP solo es valida si contiene al menos un criterio funcional informado; no deben existir alertas vacias.
- La primera vez que un usuario guarda una oportunidad en pipeline, el estado inicial obligatorio es `Nueva`.
- Un expediente mixto se considera TI para el MVP cuando cumple al menos una de estas condiciones:
  - el objeto principal o el entregable dominante menciona de forma explicita software, sistemas, ciberseguridad, redes, cloud, datos, licencias o infraestructura TIC
  - el CPV principal es tecnologico
  - la parte TI representa una porcion sustancial del valor esperado y es indispensable para cumplir el objeto del contrato
- Si un expediente mixto solo contiene TI accesoria o secundaria y la fuente no aporta evidencia suficiente para considerarla sustancial, debe quedar fuera del catalogo del MVP o tratarse como caso frontera pendiente de refinamiento.
- Cuando una oportunidad pase a `anulada`, `desierta` o `desistida`, el producto debe conservar la referencia historica y mostrar el estado oficial visible; no debe seguir tratandola como oportunidad nueva activa.
- Cuando una oportunidad sea modificada o rectificada, el producto debe mantener la misma referencia funcional si el expediente sigue siendo el mismo y exponer el ultimo dato oficial disponible en variables criticas.
- La priorizacion de fuentes reales oficiales para recopilacion se ordena asi:
  - `Ola 1`: `BOC`.
  - `Ola 2`: `BOP Las Palmas`.
  - `Ola 3`: `BOE`.
- La iteracion de `PB-009` debe reforzar origen y trazabilidad del dato, no abrir todavia alertas, pipeline ni expansion comercial de cobertura.

## Orden recomendado para `developer-teams`
1. PB-009
2. PB-004
3. PB-005
4. PB-008

## Notas de priorizacion
- `PB-007` y `PB-006` ya cumplieron su objetivo y quedan cerrados administrativamente tras validacion e integracion en `main`.
- `PB-001`, `PB-002` y `PB-003` ya quedaron validados por `qa-teams`; la siguiente prioridad funcional deja de ser retencion y pasa a ser reforzar recopilacion real sobre fuentes oficiales verificables.
- `PB-009` entra como `P0` por su impacto directo en la credibilidad del producto y en la calidad del valor entregado por el catalogo.
- `PB-009` debe seguir en la misma issue #9 y en la misma rama `developer-teams/issue-9-pb-009-fuentes-reales` mientras no cambie el alcance; no procede abrir una tercera linea de implementacion.
- `PB-004` y `PB-005` siguen siendo valiosos, pero pasan por detras de la incorporacion de fuentes reales prioritarias.
- `PB-008` queda fuera del camino critico del MVP, pero debe prepararse antes de una ampliacion comercial o de cobertura.

## Riesgos y dependencias abiertas
- Sigue abierta la dependencia de negocio sobre si los ayuntamientos deben entrar en la promesa comercial de primera release o mantenerse en fase posterior.
- Existe riesgo de falsa expectativa si la comunicacion comercial usa lenguaje de cobertura total en lugar de cobertura inicial priorizada.
- Existe riesgo de falsos positivos si desarrollo interpreta de forma demasiado laxa el criterio de "porcion sustancial" en expedientes mixtos.
- Existe riesgo de credibilidad si el producto prioriza alertas o pipeline antes de reforzar la recopilacion con fuentes reales oficiales visibles y verificables.
- Existe riesgo de entrega funcionalmente ambigua si `PB-009` no distingue prioridad por olas ni deja claro el minimo de metadatos oficiales exigible por oportunidad recopilada.
- Existe riesgo operativo de reentregas bloqueadas si la rama `developer-teams/issue-9-pb-009-fuentes-reales` no se resincroniza con `main` antes del siguiente handoff a `qa-teams`.

## Preguntas abiertas para siguiente iteracion
- Que umbral comercial debe exigirse para considerar suficiente la cobertura MVP antes de ampliar a ayuntamientos.
- Que indicadores minimos deben fijarse como puerta de inversion posterior en alertas salientes y monetizacion.
