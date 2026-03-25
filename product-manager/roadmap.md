# Roadmap de PodencoTI

## Criterios de planificacion
- Se prioriza validar primero la propuesta de valor central: centralizacion y filtrado de oportunidades TI.
- Las fases representan releases funcionales, no decisiones tecnicas de implementacion.
- Cada release debe dejar un resultado verificable por `qa-teams` y trazable a backlog e issues.

## Estado de referencia de la iteracion
- Fecha de corte documental: 2026-03-25.
- Estado confirmado: `PB-007` y `PB-006` ya fueron validados por `qa-teams` y sus entregas estan integradas en `main`.
- Estado actual de trabajo tecnico: `PB-009` ya esta validado, integrado en `main` y cerrado administrativamente en la issue #9.
- Siguiente recomendacion para `developer-teams`: tomar la issue #6, asociada a `PB-004`, como siguiente iteracion funcional prioritaria.
- Las decisiones funcionales sobre expedientes mixtos y sobre oportunidades anuladas, desiertas, desistidas o modificadas quedan ya definidas para evitar bloqueo de backlog posterior.
- En esta revision tambien quedan cerradas cuatro aclaraciones de release para reducir ambiguedad de implementacion:
  - una alerta del MVP requiere al menos un criterio funcional informado
  - el alta inicial en pipeline crea siempre el estado `Nueva`
  - `PB-008` puede refinarse documentalmente antes de disponer de instrumentacion completa
  - la recopilacion desde fuentes reales oficiales nominadas se prioriza antes que alertas y pipeline
- `PB-009` debe ejecutarse por olas y con trazabilidad minima visible al origen oficial
- La validacion y la integracion de `PB-009` confirman la prioridad funcional definida y liberan la siguiente iteracion de retencion

## Release 0: Delimitacion funcional del MVP
- Objetivo: Cerrar ambiguedades criticas antes de la implementacion del catalogo.
- Alcance:
  - PB-007 Cobertura inicial de fuentes prioritarias.
- Criterios de salida:
  - Existe una lista visible y verificable de fuentes `MVP`, `Posterior` y `Por definir`.
  - La interfaz o configuracion no induce a pensar que existe cobertura total.
- Estado actual:
  - `PB-007` completado, validado e integrado en `main`.

## Release 1: Regla de relevancia y descubrimiento
- Objetivo: Permitir descubrir y evaluar oportunidades TI con criterio funcional consistente.
- Alcance:
  - PB-006 Reglas funcionales de clasificacion TI.
  - PB-001 Catalogo inicial de oportunidades TI.
  - PB-002 Ficha de detalle de licitacion.
  - PB-003 Filtros funcionales de busqueda.
- Criterios de salida:
  - El catalogo solo muestra oportunidades alineadas con la cobertura y la regla TI.
  - El usuario puede localizar, revisar y filtrar oportunidades sin recorrer varios portales.
  - El catalogo y la ficha muestran el estado oficial del expediente cuando la fuente lo informe.
  - `qa-teams` puede verificar una muestra de inclusiones, exclusiones y campos visibles.
- Riesgo principal:
  - Que el equipo implemente un catalogo visible pero comunique cobertura o relevancia con mas seguridad de la que la release realmente soporta.
- Estado operativo actual:
  - `PB-006` ya esta validado e integrado en `main` como prerequisito del catalogo.
  - `PB-001` y `PB-002` ya fueron validados por `qa-teams` y estan integrados administrativamente en `main`.
  - `PB-003` ya fue validado por `qa-teams` el 2026-03-20 en la issue #5, integrado por `developer-teams` en `main` el 2026-03-21 y cerrado administrativamente por `product-manager`.

## Release 2: Fuentes reales priorizadas
- Objetivo: Reforzar la credibilidad del producto y la utilidad del catalogo priorizando recopilacion desde fuentes oficiales reales.
- Alcance:
  - PB-009 Priorizacion de recopilacion desde fuentes reales oficiales.
- Secuencia funcional de esta release:
  - Ola 1: `BOC`
  - Ola 2: `BOP Las Palmas`
  - Ola 3: `BOE`
- Criterios de salida:
  - Existe una prioridad trazable y ejecutable de fuentes reales oficiales para recopilacion.
  - `BOC`, `BOP Las Palmas` y `BOE` quedan identificadas de forma explicita como fuentes reales prioritarias y ordenadas por olas.
  - La entrega deja visible, para cada oportunidad obtenida desde estas fuentes, la trazabilidad minima al origen oficial.
  - La secuencia de entregas deja claro que esta prioridad adelanta a nuevas capacidades de retencion y no amplía por si misma la promesa comercial de cobertura.
- Riesgo principal:
  - Que el producto invierta antes en engagement que en reforzar la calidad y credibilidad de las oportunidades visibles.
- Estado operativo actual:
  - `PB-009` quedo validado por `qa-teams` sobre la entrega integrada en `main` el 2026-03-24.
  - `developer-teams` dejo trazabilidad explicita de integracion y borrado de rama en la issue #9 el 2026-03-24.
  - `product-manager` cerro administrativamente la issue #9 el 2026-03-25 tras reconciliar backlog, historia, caso de uso y roadmap.

## Release 3: Alertas y seguimiento operativo
- Objetivo: Convertir el descubrimiento en uso recurrente y gestion operativa.
- Alcance:
  - PB-004 Configuracion de alertas tempranas.
  - PB-005 Pipeline de seguimiento de oportunidades.
- Criterios de salida:
  - El usuario puede dejar configurados criterios persistentes de interes.
  - El usuario puede seguir oportunidades guardadas sin duplicados y con estados consistentes.
  - Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no se presentan como nuevas alertas accionables y siguen siendo visibles en pipeline con advertencia.
- Dependencia clave:
  - Requiere que Release 1 haya validado el valor del catalogo y de los filtros, y que Release 2 haya fijado la prioridad de recopilacion real.
- Decision funcional vigente:
  - Las alertas del MVP registran coincidencias de forma interna; la notificacion saliente queda fuera de esta release.
  - Una alerta del MVP solo es valida si contiene al menos un criterio funcional; no se permiten alertas vacias.
  - El pipeline del MVP es individual por usuario; la colaboracion por empresa queda para una release posterior.
  - El alta inicial de una oportunidad en pipeline debe crear el estado `Nueva`.

## Release 4: Medicion y aprendizaje
- Objetivo: Mejorar precision, cobertura y priorizacion apoyandose en indicadores.
- Alcance:
  - PB-008 Medicion basica de valor del producto.
  - Ajustes de priorizacion segun feedback y resultados de QA.
- Criterios de salida:
  - Existen definiciones de KPI utilizables para decidir siguientes inversiones funcionales.
  - El roadmap posterior puede justificarse con evidencia y no solo con intuicion.

## Dependencias abiertas de roadmap
- Confirmar con negocio cuando la cobertura de ayuntamientos pasa de `Posterior` a promesa comercial del producto.
- Definir en una iteracion posterior si las oportunidades modificadas deben generar historial visible de cambios, no solo el ultimo dato oficial.
- Decidir en una iteracion posterior si los KPIs de alertas deben exigirse ya con dato real o pueden arrancar con definicion documental y recogida manual temporal.

## Decision operativa para la siguiente iteracion
- El siguiente paso operativo de producto es mantener sincronizados backlog, historias, roadmap e issues abiertos con la nueva prioridad funcional.
- La siguiente issue recomendada para iniciar es la #6, asociada a `PB-004`.
- `PB-009` ya reutiliza la cobertura validada de `PB-007`, la regla auditable validada de `PB-006` y la superficie ya validada de catalogo, detalle y filtros.
- No se recomienda iniciar `PB-005` antes de `PB-004`, salvo bloqueo funcional explicito documentado.
