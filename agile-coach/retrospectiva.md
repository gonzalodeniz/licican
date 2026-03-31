# Retrospectiva del flujo operativo

## Fecha de revision
`2026-03-31`

## Lectura actual
- La secuencia entre `product-manager`, `developer-teams`, `qa-teams` y `doc-teams` ya esta suficientemente definida para operar sin ambiguedades graves.
- El punto de friccion residual no esta en el orden del flujo, sino en el coste de mantener varias copias de reglas compartidas en distintos documentos.

## Impacto observado
- Cada cambio de proceso sigue obligando a revisar mas de una superficie documental.
- Mientras una copia queda pendiente de actualizacion, existe una ventana pequena pero real de deriva entre la referencia canónica y los documentos de apoyo.
- Si nadie mide ese retraso, el coste de mantenimiento se percibe tarde y la friccion queda invisible.

## Mejora prioritaria
- Mantener `agile-coach/acuerdos-operativos.md` como referencia primaria.
- Dejar en los `AGENTS.md` de rol solo la referencia breve o la plantilla literal minima imprescindible.
- Medir el tiempo de propagacion de cada regla compartida con la nueva metrica 15.

## Tradeoffs
- Menos duplicacion significa menos autosuficiencia en cada documento de rol.
- A cambio, baja el riesgo de deriva y se reduce el coste de mantener sincronizadas las reglas comunes.

## Riesgos
- Si se actualiza una copia sin pasar por la guia canónica, la mejora pierde efecto.
- Si la metrica no se revisa en iteraciones posteriores, el coste de mantenimiento seguira oculto.

## Seguimiento
- Usar esta retrospectiva como referencia ligera cuando se vuelva a tocar una regla compartida.
- Revisar la metrica 15 en cualquier iteracion donde cambien estados operativos, handoffs o plantillas literales.
