# E-02 Ingestion y trazabilidad del dato oficial

## Objetivo
Convertir fuentes oficiales reales y snapshots versionados en una base operativa consolidada y visible para usuario y QA.

## Alcance
- PB-009 Priorizacion de recopilacion desde fuentes reales oficiales
- PB-011 Consolidacion funcional de fuentes `.atom` versionadas para oportunidades TI Canarias
- PB-012 Exposicion funcional en la aplicacion del dataset de licitaciones TI Canarias

## Historias relacionadas
- HU-09 Priorizar recopilacion desde fuentes oficiales reales
- HU-11 Consolidar snapshots `.atom`
- HU-12 Consultar licitaciones, lotes y adjudicaciones

## Casos de uso relacionados
- CU-07 Consolidar snapshots `.atom`
- CU-08 Consultar licitaciones, lotes y adjudicaciones consolidadas
- CU-09 Priorizar fuentes reales oficiales para recopilacion
- CU-11 Consolidar snapshots `.atom` en un dataset funcional trazable
- CU-12 Revisar la informacion consolidada en pestañas y detalle con fichero origen visible

## Definition of Done de epica
- La aplicacion absorbe todos los `.atom` presentes en `data/`.
- Los expedientes visibles conservan trazabilidad al origen oficial y al fichero `.atom` vigente.
- La salida funcional es contrastable con `data/licitaciones_ti_canarias.xlsx` para la muestra actual.

## Riesgo principal
- Que el dato consolidado exista internamente pero no sea verificable ni trazable desde la aplicacion.
