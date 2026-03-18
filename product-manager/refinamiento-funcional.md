# Refinamiento Funcional de PodencoTI

## Estado actual
La vision sigue siendo consistente con la propuesta de valor central. No se detectan contradicciones de fondo, pero si una necesidad de acotar mejor el lenguaje de "centralizacion" para no confundir cobertura progresiva con cobertura total.

## Estado funcional confirmado en el repositorio
- `PB-007` dispone de entrega visible en producto y validacion explicita de `qa-teams` en la issue #1.
- La entrega actual cubre delimitacion de fuentes, no ingestion real ni catalogo de licitaciones.
- El siguiente trabajo funcional recomendado es `PB-006` para fijar reglas auditables de relevancia TI.

## Huecos funcionales detectados en esta revision
- El backlog no reflejaba el estado real de `PB-007` ni su validacion por QA.
- Faltaban casos de uso para la delimitacion de cobertura y para la revision de KPIs.
- No existian issues remotas para `PB-004`, `PB-005` y `PB-008`.
- Seguian abiertas decisiones funcionales sobre casos frontera TI, alertas y alcance del pipeline.

## Decisiones funcionales vigentes
- El MVP de negocio se compone de dos escalones:
  - escalon 1: cobertura acotada, regla de relevancia TI, catalogo, detalle y filtros
  - escalon 2: alertas y pipeline
- La comunicacion del producto debe hablar de cobertura inicial priorizada, no de cobertura total.
- La relevancia TI debe poder explicarse y auditarse sin depender de interpretaciones tecnicas implícitas.
- El pipeline minimo sigue limitado a los estados `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.

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
- Confirmar con negocio si el MVP debe cubrir tambien ayuntamientos desde la primera release o si permanecen fuera de la promesa comercial inicial.
- Confirmar si la primera version de alertas debe contemplar solo registro interno o tambien envio externo inmediato.
- Confirmar si el pipeline sera individual por usuario o compartido por empresa en fases posteriores.

## Riesgos de producto
- Riesgo de falsa expectativa si se comunica "todas las licitaciones canarias" sin matizar la cobertura inicial real.
- Riesgo de falsos positivos si la clasificacion TI no queda suficientemente definida antes del catalogo.
- Riesgo de baja adopcion si el MVP entrega solo agregacion pero no relevancia util.
- Riesgo de frustracion si faltan datos criticos en fichas sin indicarse claramente su ausencia.

## Supuestos explicitos
- El primer objetivo es demostrar que la centralizacion y el filtrado ahorran tiempo al usuario.
- La cobertura total del ecosistema canario se abordara de forma incremental.
- `qa-teams` validara primero comportamiento funcional observable, no exhaustividad total de fuentes.

## Preguntas abiertas para siguiente refinamiento
- Que umbral funcional convierte un expediente mixto en oportunidad TI relevante.
- Que se considerara "alerta temprana" en el MVP: deteccion registrada, aviso en producto o notificacion saliente.
- Como debe tratarse una oportunidad anulada, desierta o modificada dentro del pipeline del usuario.

## Recomendacion operativa para `developer-teams`
- Tomar la issue #2 correspondiente a `PB-006` como siguiente trabajo.
- No iniciar implementacion de catalogo visible de `PB-001` sin incorporar una regla TI validable por QA.

## Trazabilidad operativa
- `PB-007` y `HU-07` quedan cubiertos por la issue #1 y su validacion ya registrada.
- `PB-006` y `HU-06` resuelven la definicion de relevancia TI antes del catalogo.
- `PB-001`, `PB-002` y `PB-003` forman el MVP de descubrimiento de Release 1.
- `PB-004` y `PB-005` quedan listos para Release 2 tras validar el MVP de descubrimiento.
- `PB-008` prepara la base de decision para evolucion posterior sin bloquear el MVP.
