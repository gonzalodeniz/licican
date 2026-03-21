# Refinamiento Funcional de PodencoTI

## Estado actual
La vision sigue siendo consistente con la propuesta de valor central. No se detectan contradicciones de fondo, pero si una necesidad permanente de acotar el lenguaje de "centralizacion" para no confundir cobertura progresiva con cobertura total.

## Estado funcional confirmado en el repositorio
- `PB-007` dispone de entrega visible en producto y validacion explicita de `qa-teams` en la issue #1.
- La entrega de `PB-007` cubre delimitacion de fuentes, no ingestion real ni catalogo de licitaciones.
- `PB-006` ya quedo validado por `qa-teams` en la issue #2 y deja una superficie funcional auditable previa al catalogo de `PB-001`.
- `PB-001` ya quedo validado por `qa-teams` en la issue #3 y aporta el catalogo visible inicial sobre cobertura MVP y clasificacion TI vigente.
- `PB-002` ya quedo validado por `qa-teams` en la issue #4 y amplia el catalogo con ficha de detalle y tratamiento visible de rectificaciones o modificaciones del expediente.
- `PB-003` ya fue revalidado por `qa-teams` en la issue #5 el 2026-03-20 y queda pendiente solo de merge en `main`, borrado de rama tecnica y cierre administrativo.

## Huecos funcionales cerrados en esta revision
- Queda definida la regla funcional para expedientes mixtos donde TI no es el unico componente.
- Queda definido el tratamiento minimo de oportunidades anuladas, desiertas, desistidas o modificadas.
- Queda identificado como deuda de trazabilidad el formato incompleto de varios issues abiertos, que debe corregirse para cumplir las reglas del repositorio.
- Queda despejada la dependencia funcional entre catalogo y ficha: el catalogo base y la ficha ya estan validados y la siguiente pieza accionable pasa a ser el filtrado funcional.

## Incidencia operativa abierta prioritaria
- La issue #5 de `PB-003` ya esta `validado`, pero sigue abierta porque la rama `developer-teams/issue-5-pb-003-filtros-catalogo` aun no se ha fusionado en `main` ni se ha borrado.
- El siguiente paso exigible a `developer-teams` es completar esa integracion antes de abrir una nueva implementacion.
- Mientras la rama validada siga abierta, no debe arrancarse `PB-004` ni `PB-005`.

## Decisiones funcionales vigentes
- El MVP de negocio se compone de dos escalones:
  - escalon 1: cobertura acotada, regla de relevancia TI, catalogo, detalle y filtros
  - escalon 2: alertas y pipeline
- La comunicacion del producto debe hablar de cobertura inicial priorizada, no de cobertura total.
- La relevancia TI debe poder explicarse y auditarse sin depender de interpretaciones tecnicas implicitas.
- La regla TI ya puede validarse de forma observable antes de construir el catalogo, pero su casuistica seguira refinandose con ejemplos reales.
- El pipeline minimo sigue limitado a los estados `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
- La primera iteracion de alertas queda limitada a registrar coincidencias internas; la notificacion saliente se evaluara en una fase posterior.
- El pipeline MVP queda limitado a gestion individual por usuario; la colaboracion por empresa no forma parte del alcance actual.

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

## Dependencias abiertas
- Confirmar con negocio si el MVP debe cubrir tambien ayuntamientos desde la primera promesa comercial o si permanecen fuera de la comunicacion inicial.
- Definir mas adelante si las modificaciones oficiales del expediente requieren un historial visible de cambios en lugar de mostrar solo el ultimo dato disponible.

## Riesgos de producto
- Riesgo de falsa expectativa si se comunica "todas las licitaciones canarias" sin matizar la cobertura inicial real.
- Riesgo de falsos positivos si desarrollo interpreta de forma laxa que una parte TI es "sustancial" en expedientes mixtos.
- Riesgo de baja adopcion si el MVP entrega solo agregacion pero no relevancia util.
- Riesgo de frustracion si faltan datos criticos en fichas sin indicarse claramente su ausencia.
- Riesgo operativo si desarrollo declara rutas o superficies de validacion no expuestas realmente en la entrega revisable.
- Riesgo operativo si una rama tecnica ya validada permanece abierta y retrasa el paso ordenado hacia `PB-004`.

## Supuestos explicitos
- El primer objetivo es demostrar que la centralizacion y el filtrado ahorran tiempo al usuario.
- La cobertura total del ecosistema canario se abordara de forma incremental.
- `qa-teams` validara primero comportamiento funcional observable, no exhaustividad total de fuentes.

## Preguntas abiertas para siguiente refinamiento
- Que umbral comercial debe exigirse para considerar suficiente la cobertura MVP antes de ampliar a ayuntamientos.
- Que datos minimos deben gobernar una futura decision de monetizacion o plan de pago.

## Recomendacion operativa para `developer-teams`
- Completar merge a `main` y borrado de rama de la issue #5 correspondiente a `PB-003`, ya validada por `qa-teams`.
- Tras esa integracion, tomar `PB-004` como siguiente pieza funcional prioritaria.
- Reutilizar la cobertura validada de `PB-007`, la regla auditable de `PB-006` y la superficie ya validada de `PB-001`, `PB-002` y `PB-003` sin reabrirlas salvo cambio de alcance.
- Mantener visible en el catalogo la fuente oficial y evitar mensajes que sugieran cobertura total del ecosistema canario.
- Aplicar el filtrado solo sobre oportunidades ya visibles dentro de cobertura MVP y clasificacion final `TI`.
- Tratar los expedientes mixtos dudosos como caso frontera fuera del catalogo hasta que exista evidencia funcional suficiente.

## Trazabilidad operativa
- `PB-007` y `HU-07` quedan cubiertos por la issue #1 y su validacion ya registrada.
- `PB-006`, `HU-06` y `CU-08` resuelven la definicion de relevancia TI antes del catalogo.
- `PB-001`, `PB-002` y `PB-003` ya quedaron validados por `qa-teams`; Release 1 queda funcionalmente completa y pendiente solo de la integracion operativa final de la issue #5.
- `PB-004` y `PB-005` quedan listos para Release 2 tras validar el MVP de descubrimiento.
- `PB-008` prepara la base de decision para evolucion posterior sin bloquear el MVP.
