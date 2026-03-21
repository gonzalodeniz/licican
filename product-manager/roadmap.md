# Roadmap de PodencoTI

## Criterios de planificacion
- Se prioriza validar primero la propuesta de valor central: centralizacion y filtrado de oportunidades TI.
- Las fases representan releases funcionales, no decisiones tecnicas de implementacion.
- Cada release debe dejar un resultado verificable por `qa-teams` y trazable a backlog e issues.

## Estado de referencia de la iteracion
- Fecha de corte documental: 2026-03-21.
- Estado confirmado: `PB-007` y `PB-006` ya fueron validados por `qa-teams` y sus entregas estan integradas en `main`.
- Estado actual de trabajo tecnico: solo permanece abierta en remoto la rama `developer-teams/issue-5-pb-003-filtros-catalogo`.
- Siguiente recomendacion para `developer-teams`: fusionar en `main` la rama validada de `PB-003`, borrar la rama tecnica y cerrar la issue #5 antes de tomar una nueva implementacion.
- Las decisiones funcionales sobre expedientes mixtos y sobre oportunidades anuladas, desiertas, desistidas o modificadas quedan ya definidas para evitar bloqueo de backlog posterior.
- En esta revision tambien quedan cerradas tres aclaraciones de release para reducir ambiguedad de implementacion:
  - una alerta del MVP requiere al menos un criterio funcional informado
  - el alta inicial en pipeline crea siempre el estado `Nueva`
  - `PB-008` puede refinarse documentalmente antes de disponer de instrumentacion completa

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
  - `PB-003` ya fue validado por `qa-teams` el 2026-03-20 en la issue #5. Release 1 queda funcionalmente completada y pendiente solo de integracion final en `main` por `developer-teams`.

## Release 2: Alertas y seguimiento operativo
- Objetivo: Convertir el descubrimiento en uso recurrente y gestion operativa.
- Alcance:
  - PB-004 Configuracion de alertas tempranas.
  - PB-005 Pipeline de seguimiento de oportunidades.
- Criterios de salida:
  - El usuario puede dejar configurados criterios persistentes de interes.
  - El usuario puede seguir oportunidades guardadas sin duplicados y con estados consistentes.
  - Las oportunidades con estado oficial `anulada`, `desierta` o `desistida` no se presentan como nuevas alertas accionables y siguen siendo visibles en pipeline con advertencia.
- Dependencia clave:
  - Requiere que Release 1 haya validado e integrado en `main` el valor del catalogo y de los filtros.
- Decision funcional vigente:
  - Las alertas del MVP registran coincidencias de forma interna; la notificacion saliente queda fuera de esta release.
  - Una alerta del MVP solo es valida si contiene al menos un criterio funcional; no se permiten alertas vacias.
  - El pipeline del MVP es individual por usuario; la colaboracion por empresa queda para una release posterior.
  - El alta inicial de una oportunidad en pipeline debe crear el estado `Nueva`.

## Release 3: Medicion y aprendizaje
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
- El siguiente paso operativo de `developer-teams` es completar merge y borrado de rama de la issue #5, asociada a `PB-003`.
- Tras esa integracion, la siguiente issue recomendada para iniciar es la #6, asociada a `PB-004`.
- `PB-004` debe reutilizar la cobertura validada de `PB-007`, la regla auditable validada de `PB-006` y la superficie ya validada de catalogo, detalle y filtros.
- No se recomienda iniciar `PB-004` ni `PB-005` mientras la rama validada de `PB-003` siga abierta sin integrar.
