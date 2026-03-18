# Mejoras de proceso propuestas

## Mejora 1: introducir estados operativos comunes en la issue
### Problema detectado
No existe un lenguaje operativo unico para saber en que punto exacto del flujo esta cada issue.

### Propuesta
Estandarizar estos estados operativos en comentarios y handoffs:
- `nuevo`
- `en desarrollo`
- `listo para qa`
- `no validado`
- `validado`
- `cerrado`

### Impacto esperado
- Reduce ambiguedad sobre el siguiente responsable de actuar.
- Facilita la priorizacion de `developer-teams` sobre trabajo ya empezado.
- Hace mas auditable el flujo real entre equipos.

### Tradeoffs
- Añade una pequena disciplina documental por iteracion.

### Riesgos y dependencias
- Requiere que todos los roles reutilicen la misma nomenclatura.
- Conviene mantenerlo simple y no convertirlo en burocracia adicional.

## Mejora 2: fijar un paquete minimo de handoff a QA
### Problema detectado
El contexto entregado por desarrollo a QA no tiene un contrato minimo comun.

### Propuesta
Obligar a que el comentario final de `developer-teams` antes de QA incluya:
- rama revisable
- resumen de lo realizado
- decisiones relevantes
- limitaciones conocidas
- comandos de verificacion ejecutados
- impacto documental: `si` o `no`
- estado operativo: `listo para qa`

### Impacto esperado
- QA reduce tiempo de reconstruccion del contexto.
- Mejora la calidad y repetibilidad de las revisiones.
- `doc-teams` recibe una senal temprana y verificable de impacto documental.

### Tradeoffs
- Desarrollo debe ser mas explicito al cerrar cada entrega.

### Riesgos y dependencias
- Si se convierte en texto largo no estructurado, se pierde el beneficio.
- Debe mantenerse como checklist breve.

## Mejora 3: explicitar el ciclo de revalidacion
### Problema detectado
No hay una regla clara para volver de `no validado` a una nueva revision.

### Propuesta
Mantener la misma issue y la misma rama del trabajo mientras siga siendo el mismo alcance. Tras un `no validado`:
1. `developer-teams` corrige en la misma rama.
2. Publica un nuevo comentario de entrega con cambios realizados y evidencias nuevas.
3. Marca de nuevo `estado operativo: listo para qa`.
4. `qa-teams` realiza una nueva revision sobre esa misma issue.

### Impacto esperado
- Conserva trazabilidad completa del ciclo de correccion.
- Reduce dispersion de contexto entre ramas o issues duplicadas.

### Tradeoffs
- La issue puede acumular varios comentarios de iteraciones.

### Riesgos y dependencias
- Si el alcance cambia materialmente, `product-manager` debe decidir si sigue siendo la misma issue o si hace falta una nueva.

## Mejora 4: fijar el disparador de `doc-teams`
### Problema detectado
La documentacion depende de interpretacion y puede desalinearse respecto al estado real de la entrega.

### Propuesta
Activar a `doc-teams` cuando se cumplan ambas condiciones:
1. `qa-teams` ha dejado `validado`.
2. La entrega indica `impacto documental: si`.

Si el impacto documental es `no`, `doc-teams` no necesita intervenir en esa iteracion salvo solicitud expresa.

### Impacto esperado
- Se evita documentar funcionalidades aun inestables.
- Se reduce trabajo documental innecesario.
- Mejora la sincronizacion entre entrega validada y documentacion oficial.

### Tradeoffs
- Desarrollo debe evaluar con criterio si existe impacto documental.

### Riesgos y dependencias
- Si `developer-teams` marca mal el impacto documental, el flujo puede omitir documentacion necesaria.
- Conviene que QA senale el riesgo si detecta impacto documental no declarado.

## Mejora 5: introducir metricas ligeras de flujo
### Problema detectado
El repositorio no define como medir si los cambios de proceso mejoran realmente la coordinacion.

### Propuesta
Seguir de forma ligera estas metricas:
- tiempo desde issue abierta hasta `en desarrollo`
- tiempo desde `listo para qa` hasta resultado de QA
- porcentaje de issues que requieren revalidacion
- tiempo desde `validado` hasta cierre por `product-manager`

### Impacto esperado
- Permite detectar cuellos de botella reales.
- Da criterio para decidir si el bloqueo esta en desarrollo, QA o cierre.

### Tradeoffs
- Requiere disciplina minima en comentarios y fechas.

### Riesgos y dependencias
- Sin estados operativos comunes, estas metricas pierden calidad.

## Mejora 6: separar la trazabilidad del `changelog/` de la entrega tecnica del issue
### Problema detectado
El `changelog/` debe actualizarse en `main`, pero no existia una regla operativa suficiente para evitar que esa actividad contaminara ramas tecnicas o generara conflictos de integracion.

### Propuesta
- Mantener el `changelog/` solo en `main` y dejar explicito que nunca forma parte de la entrega tecnica a QA.
- Si `developer-teams` o `qa-teams` actualizan `changelog/` mientras mantienen una rama abierta, deben sincronizar despues esa rama con `main` antes del siguiente handoff.

### Impacto esperado
- Reduce conflictos evitables en validacion e integracion.
- Evita que QA invierta tiempo en incidencias administrativas derivadas del registro diario.
- Mantiene la trazabilidad diaria sin mezclarla con el alcance tecnico del issue.

### Tradeoffs
- Obliga a un paso adicional de sincronizacion cuando una rama permanece abierta mas de un bloque de trabajo.

### Riesgos y dependencias
- Si los equipos olvidan resincronizar la rama tras actualizar `main`, el conflicto reaparecera.
- Requiere que la secuencia operativa de `developer-teams` explicite esa comprobacion antes de QA.

## Mejora 7: reforzar el checkpoint posterior a `validado`
### Problema detectado
Una issue puede quedar abierta tras `validado` sin dejar claro si el bloqueo es integracion, cierre administrativo o dependencia documental.

### Propuesta
Si `product-manager` mantiene abierta una issue ya `validado`, debe dejar en la propia issue:
- bloqueo actual
- siguiente responsable
- siguiente paso operativo

### Impacto esperado
- Evita que una issue validada siga abierta sin contexto accionable.
- Mejora la lectura real del backlog y del trabajo pendiente.
- Facilita a `agile-coach` y al resto de equipos detectar bloqueos de cierre en lugar de confundirlos con trabajo aun no aceptado.

### Tradeoffs
- Introduce una pequena disciplina administrativa adicional en el cierre.

### Riesgos y dependencias
- Si el comentario se vuelve ambiguo, reaparecera el mismo problema con mas texto pero sin mas claridad.

## Mejora 8: fijar una plantilla literal para comentarios de handoff
### Problema detectado
Los equipos ya comparten que informacion debe aparecer en las issues, pero no una plantilla literal estable que facilite localizarla y compararla entre iteraciones.

### Propuesta
- Exigir a `developer-teams` y `qa-teams` que reutilicen siempre las mismas claves literales y en el mismo orden para sus comentarios de handoff.
- Exigir a `product-manager` una plantilla administrativa minima cuando una issue siga abierta tras `validado`.

### Impacto esperado
- Reduce tiempo de lectura y reinterpretacion entre equipos.
- Mejora la trazabilidad de revalidaciones y cierres administrativos.
- Hace mas viable medir cumplimiento de handoffs y tiempos de espera por estado.

### Tradeoffs
- Introduce mas disciplina formal en los comentarios de issue.

### Riesgos y dependencias
- Si las plantillas se vuelven demasiado largas, los equipos pueden tender a rellenarlas de forma mecanica.
- Conviene mantener solo los campos necesarios para decidir el siguiente paso operativo.
