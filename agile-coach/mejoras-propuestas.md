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
