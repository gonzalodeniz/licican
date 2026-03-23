# Refinamiento Funcional de PodencoTI

## Estado actual
La vision sigue siendo consistente con la propuesta de valor central. No se detectan contradicciones de fondo, pero si una necesidad permanente de acotar el lenguaje de "centralizacion" para no confundir cobertura progresiva con cobertura total.
La prioridad funcional vigente sigue siendo `PB-009`, aunque su issue activa (#9) esta en `no validado` por una incidencia operativa de rama que debe corregirse sin cambiar el alcance de producto.

## Huecos de definicion detectados en esta revision
- La prioridad funcional de `PB-009` ya existia, pero faltaba fijar el orden de ejecucion entre fuentes reales oficiales para evitar una implementacion demasiado amplia en un solo salto.
- Faltaba dejar explicito el minimo de trazabilidad al origen oficial que debe conservar cada oportunidad recopilada en esta iteracion.
- Faltaba remarcar de forma mas dura que `PB-009` no abre por si mismo alertas, pipeline ni ampliacion comercial de cobertura.

## Estado funcional confirmado en el repositorio
- `PB-007` dispone de entrega visible en producto y validacion explicita de `qa-teams` en la issue #1.
- La entrega de `PB-007` cubre delimitacion de fuentes, no ingestion real ni catalogo de licitaciones.
- `PB-006` ya quedo validado por `qa-teams` en la issue #2 y deja una superficie funcional auditable previa al catalogo de `PB-001`.
- `PB-001` ya quedo validado por `qa-teams` en la issue #3 y aporta el catalogo visible inicial sobre cobertura MVP y clasificacion TI vigente.
- `PB-002` ya quedo validado por `qa-teams` en la issue #4 y amplia el catalogo con ficha de detalle y tratamiento visible de rectificaciones o modificaciones del expediente.
- `PB-003` ya fue revalidado por `qa-teams` en la issue #5 el 2026-03-20, integrado en `main` por `developer-teams` el 2026-03-21 y cerrado administrativamente por `product-manager`.

## Huecos funcionales cerrados en esta revision
- Queda definida la regla funcional para expedientes mixtos donde TI no es el unico componente.
- Queda definido el tratamiento minimo de oportunidades anuladas, desiertas, desistidas o modificadas.
- Queda identificado como deuda de trazabilidad el formato incompleto de varios issues abiertos, que debe corregirse para cumplir las reglas del repositorio.
- Queda despejada la dependencia funcional entre catalogo y ficha: el catalogo base, la ficha y el filtrado ya estan validados y la siguiente pieza accionable pasa a ser `PB-009`.
- Queda definido que una alerta del MVP necesita al menos un criterio funcional informado y no puede guardarse vacia.
- Queda definido que el alta inicial en pipeline crea siempre el estado `Nueva`.
- Queda definido que `PB-008` puede avanzar como definicion funcional de KPIs aunque la instrumentacion completa llegue en una iteracion posterior.
- Queda incorporada como prioridad explicita la recopilacion desde fuentes reales oficiales nominadas, ya que `PB-007` solo cerraba cobertura funcional y no orden de implementacion de fuentes reales.

## Incidencia operativa abierta prioritaria
- La nueva prioridad abierta para `developer-teams` pasa a ser `PB-009`.
- La secuencia de trabajo ya no tiene bloqueos administrativos previos asociados a `PB-003`.
- La validacion e integracion previas permiten reordenar la siguiente iteracion sin reabrir entregas ya aceptadas.
- `qa-teams` no cuestiona el alcance funcional de `PB-009`, pero si bloquea la entrega actual porque la rama `developer-teams/issue-9-pb-009-fuentes-reales` arrastra borrados de archivos de gobierno del repositorio ajenos a la issue.
- Mientras el alcance siga siendo el mismo, la correccion debe hacerse en la misma issue #9 y en la misma rama tecnica, tras resincronizar con `main`.

## Decisiones funcionales vigentes
- El MVP de negocio se compone de dos escalones:
  - escalon 1: cobertura acotada, regla de relevancia TI, catalogo, detalle y filtros
  - escalon 2: recopilacion prioritaria desde fuentes reales oficiales
  - escalon 3: alertas y pipeline
- La comunicacion del producto debe hablar de cobertura inicial priorizada, no de cobertura total.
- La recopilacion de contratos y concursos debe priorizar fuentes reales oficiales y verificables antes de invertir en capacidades de retencion no esenciales.
- La ejecucion funcional de esa prioridad se ordena por olas para reducir dispersion:
  - `Ola 1`: `BOC`
  - `Ola 2`: `BOP Las Palmas`
  - `Ola 3`: `BOE`
- La relevancia TI debe poder explicarse y auditarse sin depender de interpretaciones tecnicas implicitas.
- La regla TI ya puede validarse de forma observable antes de construir el catalogo, pero su casuistica seguira refinandose con ejemplos reales.
- El pipeline minimo sigue limitado a los estados `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
- La primera iteracion de alertas queda limitada a registrar coincidencias internas; la notificacion saliente se evaluara en una fase posterior.
- Una alerta vacia no es valida: debe incluir al menos un criterio funcional entre palabra clave, presupuesto, procedimiento o ubicacion.
- El pipeline MVP queda limitado a gestion individual por usuario; la colaboracion por empresa no forma parte del alcance actual.
- La primera vez que una oportunidad entra en pipeline debe hacerlo en estado `Nueva`.
- La definicion de KPIs de `PB-008` no exige disponer desde el primer dia de toda la instrumentacion automatizada, pero si exige dejar explicita cualquier limitacion de medicion.
- La primera entrega de `PB-009` debe conservar, como minimo por oportunidad recopilada, referencia a la fuente oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando la fuente lo publique.
- `PB-009` no cambia por si solo la promesa comercial de cobertura ni adelanta funcionalidades de alertas o pipeline.

## Regla funcional vigente para expedientes mixtos
- Un expediente mixto debe considerarse TI en el MVP cuando se cumpla al menos una de estas condiciones:
  - el objeto principal o entregable dominante menciona de forma explicita software, sistemas, ciberseguridad, redes, cloud, datos, licencias o infraestructura TIC
  - el CPV principal es tecnologico
  - la parte TI es sustancial para el valor esperado del contrato y resulta indispensable para cumplir su objeto
- Un expediente mixto no debe considerarse TI cuando:
  - la parte tecnologica es accesoria o secundaria respecto al objeto principal
  - la evidencia funcional disponible no permite afirmar que la necesidad TI sea sustancial
- Si la informacion de origen no permite decidir con seguridad, el expediente debe tratarse como caso frontera y quedar fuera del catalogo visible del MVP hasta nuevo refinamiento.

## Tratamiento funcional vigente del ciclo de vida de oportunidades
- Si una oportunidad pasa a estado oficial `anulada`, `desierta` o `desistida`, debe seguir siendo visible con ese estado para preservar contexto historico.
- Una oportunidad con esos estados oficiales no debe presentarse como nueva oportunidad accionable ni generar nuevas alertas accionables.
- Si la oportunidad ya estaba guardada en pipeline, el sistema debe conservar el estado de trabajo del usuario y mostrar el estado oficial como advertencia visible.
- Si la fuente publica una modificacion o rectificacion del mismo expediente, el producto debe mantener la misma referencia funcional y mostrar el ultimo dato oficial disponible en campos criticos como fecha limite o presupuesto.
- El historial detallado de cambios oficiales queda fuera del MVP; por ahora basta con exponer el ultimo dato oficial visible.

## Reglas funcionales vigentes de clasificacion TI
- Se considera candidata TI una oportunidad que cumpla al menos uno de estos criterios:
  - menciona software, desarrollo, sistemas, soporte TI, ciberseguridad, redes, licencias, cloud, datos o hardware tecnologico
  - incluye CPVs alineados con servicios o suministros tecnologicos
  - describe una necesidad de digitalizacion, mantenimiento de sistemas o infraestructura TIC
- Se considera no TI, salvo evidencia contraria:
  - obra civil sin componente tecnologico relevante
  - suministros generales de mobiliario o material no tecnologico
  - servicios administrativos o de consultoria no vinculados a tecnologia
- Casos frontera que requieren criterio verificable adicional:
  - contratos mixtos donde TI sea una parte menor
  - servicios de telecomunicaciones no claramente ligados a sistemas o redes
  - expedientes de digitalizacion formulados con lenguaje demasiado generico

## Cobertura funcional vigente para MVP
- Estado `MVP`:
  - Plataforma de Contratacion del Sector Publico filtrada por organos de contratacion de Canarias
  - Gobierno de Canarias
  - Cabildos insulares
- Estado `Posterior`:
  - Ayuntamientos con perfiles del contratante propios
  - Empresas publicas y consorcios
- Estado `Por definir`:
  - Fuentes con acceso inconsistente, formatos no estandar o baja frecuencia de oportunidades TI

## Fuentes reales oficiales priorizadas para recopilacion
- `Ola 1`:
  - `BOC` (`https://www.gobiernodecanarias.org/boc/`)
- `Ola 2`:
  - `BOP Las Palmas` (`https://www.boplaspalmas.net/nbop2/index.php`)
- `Ola 3`:
  - `BOE` (`https://www.boe.es/`)
- Prioridad alta posterior o dependiente de validacion adicional:
  - perfiles del contratante y boletines oficiales adicionales que aporten oportunidades TI relevantes para Canarias, incluidos cabildos y otros boletines provinciales o locales
- Criterio funcional:
  - si una fuente es oficial, real y aporta señal temprana de contratos o concursos aprovechables por el usuario objetivo, debe evaluarse antes que nuevas capacidades de engagement no esenciales
- Minimo funcional verificable por oportunidad recopilada en `PB-009`:
  - identificacion visible de la fuente oficial
  - enlace oficial clicable o accesible
  - fecha de publicacion o equivalente oficial visible
  - estado oficial del expediente cuando la fuente lo informe
- Fuera de alcance de esta iteracion:
  - notificaciones salientes al usuario
  - automatizacion completa de pipeline
  - ampliacion de promesa comercial a cobertura total o a ayuntamientos no confirmados

## Dependencias abiertas
- Confirmar con negocio si el MVP debe cubrir tambien ayuntamientos desde la primera promesa comercial o si permanecen fuera de la comunicacion inicial.
- Definir mas adelante si las modificaciones oficiales del expediente requieren un historial visible de cambios en lugar de mostrar solo el ultimo dato disponible.
- Decidir si la primera captura operativa de KPIs de alertas se resolvera con medicion manual temporal o se aplazara hasta disponer de mas instrumentacion.
- Confirmar tras la siguiente reentrega de `PB-009` que la rama tecnica elimina los borrados ajenos al alcance y vuelve a integrar limpia con `main` antes del nuevo handoff a `qa-teams`.

## Riesgos de producto
- Riesgo de falsa expectativa si se comunica "todas las licitaciones canarias" sin matizar la cobertura inicial real.
- Riesgo de falsos positivos si desarrollo interpreta de forma laxa que una parte TI es "sustancial" en expedientes mixtos.
- Riesgo de baja adopcion si el MVP entrega solo agregacion pero no relevancia util.
- Riesgo de frustracion si faltan datos criticos en fichas sin indicarse claramente su ausencia.
- Riesgo operativo si desarrollo declara rutas o superficies de validacion no expuestas realmente en la entrega revisable.
- Riesgo de credibilidad si el producto retrasa la recopilacion real y prioriza antes capacidades de retencion sobre fuentes oficiales verificables.
- Riesgo de dispersion si `developer-teams` intenta abordar simultaneamente las tres fuentes prioritarias sin un orden de entrega ni un minimo comun verificable.

## Supuestos explicitos
- El primer objetivo es demostrar que la centralizacion y el filtrado ahorran tiempo al usuario.
- La cobertura total del ecosistema canario se abordara de forma incremental.
- `qa-teams` validara primero comportamiento funcional observable, no exhaustividad total de fuentes.

## Preguntas abiertas para siguiente refinamiento
- Que umbral comercial debe exigirse para considerar suficiente la cobertura MVP antes de ampliar a ayuntamientos.
- Que datos minimos deben gobernar una futura decision de monetizacion o plan de pago.

## Recomendacion operativa para `developer-teams`
- Tomar `PB-009` como siguiente pieza funcional prioritaria para reforzar recopilacion sobre fuentes reales oficiales nominadas.
- Corregir `PB-009` sobre la issue #9 ya abierta y sobre la rama `developer-teams/issue-9-pb-009-fuentes-reales`, sin abrir una nueva issue funcional mientras el alcance no cambie.
- Reutilizar la cobertura validada de `PB-007`, la regla auditable de `PB-006` y la superficie ya validada de `PB-001`, `PB-002` y `PB-003` sin reabrirlas salvo cambio de alcance.
- Tratar `BOC`, `BOP Las Palmas` y `BOE` como fuentes reales de referencia para la siguiente iteracion, en ese orden por olas.
- Mantener visible en el catalogo la fuente oficial y evitar mensajes que sugieran cobertura total del ecosistema canario.
- Garantizar como minimo por oportunidad recopilada la visibilidad de origen oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
- Aplicar el filtrado solo sobre oportunidades ya visibles dentro de cobertura MVP y clasificacion final `TI`.
- Tratar los expedientes mixtos dudosos como caso frontera fuera del catalogo hasta que exista evidencia funcional suficiente.
- Resincronizar la rama con `main` antes de volver a pedir revision a `qa-teams` para evitar un segundo rechazo por arrastre de cambios ajenos.

## Trazabilidad operativa
- `PB-007` y `HU-07` quedan cubiertos por la issue #1 y su validacion ya registrada.
- `PB-006`, `HU-06` y `CU-08` resuelven la definicion de relevancia TI antes del catalogo.
- `PB-001`, `PB-002` y `PB-003` ya quedaron validados por `qa-teams` y cerrados administrativamente; Release 1 queda funcionalmente completa.
- `PB-009` sigue siendo la siguiente pieza prioritaria tras el MVP de descubrimiento para reforzar recopilacion real, pero su estado actual es `no validado` en la issue #9 por incidencia operativa de rama.
- `PB-004` y `PB-005` quedan desplazados a la release posterior de retencion.
- `PB-008` prepara la base de decision para evolucion posterior sin bloquear el MVP.
