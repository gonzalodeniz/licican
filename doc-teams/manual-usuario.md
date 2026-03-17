# Manual de usuario

## Publico objetivo
Usuario interno, stakeholder funcional o persona de negocio que necesita consultar la delimitacion visible de la cobertura inicial de fuentes del MVP.

## Que permite hacer el producto hoy
La entrega actual no ofrece todavia un catalogo completo de licitaciones TI, filtros, alertas ni pipeline. El comportamiento implementado permite:
- Consultar una vista HTML con las fuentes oficiales incluidas o planificadas para el MVP.
- Revisar un resumen por estado de cobertura.
- Obtener la misma informacion en formato JSON para trazabilidad tecnica o validacion.

## Requisito previo
La aplicacion debe estar arrancada en local siguiendo [guia-instalacion.md](/opt/apps/podencoti/doc-teams/guia-instalacion.md).

## Acceso
- Vista HTML: `http://127.0.0.1:8000/`
- API JSON: `http://127.0.0.1:8000/api/fuentes`

## Lectura de la vista principal
La pantalla principal muestra:
- Un encabezado que identifica la entrega como `Release 0 · PB-007`.
- Tres metricas de resumen:
  - `MVP`: fuentes objetivo para la primera release.
  - `Posterior`: fuentes previstas para una fase posterior.
  - `Por definir`: fuentes pendientes de decision funcional o tecnica.
- Una tabla con seis columnas:
  - `Fuente oficial`
  - `Categoria`
  - `Estado`
  - `Alcance`
  - `Justificacion funcional`
  - `Trazabilidad`

## Interpretacion de estados
- `MVP`: la fuente forma parte de la cobertura objetivo de la primera entrega funcional.
- `Posterior`: la fuente no entra en la entrega actual y queda planificada para una iteracion posterior.
- `Por definir`: la fuente requiere decision adicional antes de comprometer su inclusion.

## Fuentes reflejadas en la version actual
- Plataforma de Contratacion del Sector Publico filtrada por organos de Canarias.
- Gobierno de Canarias.
- Cabildos insulares.
- Ayuntamientos con perfiles del contratante propios.
- Empresas publicas y consorcios.
- Fuentes con acceso inconsistente o formato no estandar.

## Que no debe asumirse
- La vista no representa aun un inventario exhaustivo de todas las licitaciones canarias.
- La pagina no muestra expedientes individuales ni permite buscar, filtrar o guardar oportunidades.
- La presencia de una fuente en estado `MVP` no implica que exista ya una integracion automatizada visible en este repositorio; solo refleja la cobertura funcional versionada para esta entrega.

## Incidencias esperables
- Si se accede a una ruta distinta de `/` o `/api/fuentes`, el sistema responde `404 No encontrado`.
- Si el servidor no esta levantado, el navegador no podra cargar la pagina ni la API.
