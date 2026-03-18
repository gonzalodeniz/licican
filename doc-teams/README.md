# Documentacion de `doc-teams`

## Objetivo
Centralizar la documentacion operativa y de referencia del proyecto `PodencoTI` con separacion explicita por audiencia.

## Audiencias cubiertas
- Usuario final o stakeholder funcional: [manual-usuario.md](/opt/apps/podencoti/doc-teams/manual-usuario.md)
- Equipo tecnico: [manual-tecnico.md](/opt/apps/podencoti/doc-teams/manual-tecnico.md)
- Administracion u operacion: [manual-administracion.md](/opt/apps/podencoti/doc-teams/manual-administracion.md)
- Puesta en marcha local: [guia-instalacion.md](/opt/apps/podencoti/doc-teams/guia-instalacion.md)

## Alcance documental actual
La implementacion disponible en el repositorio cubre una entrega minima de `PB-007`: una vista HTML y una API JSON para hacer visible la cobertura inicial de fuentes oficiales del MVP.

## Huecos y dependencias abiertas detectadas
- La vision del producto describe un catalogo de oportunidades TI, detalle de licitacion, filtros, alertas y pipeline, pero esas capacidades no estan implementadas todavia en el codigo actual.
- El `README.md` de raiz describe correctamente la entrega tecnica actual, pero convive con artefactos funcionales que representan alcance futuro. La documentacion de `doc-teams` diferencia ambos planos para evitar ambiguedad.
- No existe automatizacion de despliegue, servicio persistente, contenedorizacion ni configuracion de observabilidad. Cualquier instruccion operativa queda limitada al arranque local con `python3`.
- La cobertura funcional inicial de fuentes mantiene dependencias abiertas ya registradas en `product-manager/refinamiento-funcional.md`: inclusion de ayuntamientos en MVP, criterio operativo de alerta temprana y futura naturaleza del pipeline.

## Criterio documental aplicado
- No se documenta comportamiento no implementado como si estuviera disponible.
- Cuando una capacidad pertenece a la vision o al backlog pero no al producto actual, se marca como pendiente.
- Los procedimientos tecnicos y operativos incluidos en esta carpeta han sido redactados para ser reproducibles con la estructura actual del repositorio.
