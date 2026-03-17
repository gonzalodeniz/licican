# Refinamiento Funcional de PodencoTI

## Estado actual
La vision es consistente con la propuesta de valor general, pero faltaban definiciones operativas para que `developer-teams` pueda implementar sin ambiguedad innecesaria.

## Huecos funcionales detectados
- No estaba delimitada la cobertura inicial de fuentes oficiales para el MVP.
- No existia una regla funcional verificable para clasificar una licitacion como TI.
- No estaban definidos los estados minimos del pipeline.
- No estaba aclarado el conjunto minimo de campos obligatorios en listado y detalle.
- No existia una traduccion directa de la vision a backlog, historias, casos de uso y roadmap.
- No habia issues ejecutables para comenzar trabajo en `developer-teams`.

## Decisiones funcionales adoptadas en esta iteracion
- El MVP se centra primero en descubrimiento: catalogo, detalle y filtros.
- Alertas y pipeline pasan a una segunda release funcional, manteniendo coherencia con la vision.
- Se define un conjunto minimo de estados del pipeline: `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada`, `Descartada`.
- Se establece que cada oportunidad debe preservar trazabilidad a su fuente oficial.
- Se separa explicitamente la definicion funcional de la implementacion tecnica.

## Reglas funcionales iniciales de clasificacion TI
- Se considera candidata TI una oportunidad que cumpla al menos uno de estos criterios:
  - menciona software, desarrollo, sistemas, soporte TI, ciberseguridad, redes, licencias, cloud, datos o hardware tecnologico
  - incluye CPVs alineados con servicios o suministros tecnologicos
  - describe una necesidad de digitalizacion, mantenimiento de sistemas o infraestructura TIC
- Se considera no TI, salvo evidencia contraria:
  - obra civil sin componente tecnologico relevante
  - suministros generales de mobiliario o material no tecnologico
  - servicios administrativos o de consultoria no vinculados a tecnologia
- Casos frontera que requieren validacion de negocio o QA:
  - contratos mixtos donde TI sea una parte menor
  - servicios de telecomunicaciones no claramente ligados a sistemas o redes
  - expedientes de digitalizacion formulados con lenguaje demasiado generico

## Cobertura funcional inicial propuesta para MVP
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
- Confirmar con negocio si el MVP debe cubrir tambien ayuntamientos desde la primera release.
- Confirmar si la primera version de alertas debe contemplar solo registro interno o tambien envio externo inmediato.
- Confirmar si el pipeline sera individual por usuario o compartido por empresa en fases posteriores.

## Riesgos de producto
- Riesgo de falsa expectativa si se comunica "todas las licitaciones canarias" sin matizar la cobertura inicial real.
- Riesgo de falsos positivos si la clasificacion TI no queda suficientemente definida.
- Riesgo de baja adopcion si el MVP entrega solo agregacion pero no relevancia util.
- Riesgo de frustracion si faltan datos criticos en fichas sin indicarse claramente su ausencia.

## Supuestos explicitos
- El primer objetivo es demostrar que la centralizacion y el filtrado ahorran tiempo al usuario.
- La cobertura total del ecosistema canario se abordara de forma incremental.
- `qa-teams` validara primero comportamiento funcional observable, no exhaustividad total de fuentes.

## Preguntas abiertas
- Que criterio comercial definira "alerta temprana" en el MVP: inmediatez, frecuencia o mera deteccion antes de fecha limite.
- Que nivel minimo de detalle debe exigirse cuando la fuente oficial no publica claramente solvencia o criterios de adjudicacion.
- Como debe tratarse una oportunidad anulada, desierta o modificada dentro del pipeline del usuario.

## Trazabilidad operativa
- PB-007 y HU-07 resuelven cobertura inicial de fuentes.
- PB-006 y HU-06 resuelven definicion de relevancia TI.
- PB-001, PB-002 y PB-003 forman el MVP de Release 1.
- PB-004 y PB-005 quedan listos para Release 2 tras validacion del MVP de descubrimiento.
