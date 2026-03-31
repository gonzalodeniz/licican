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

## Mejora 9: fijar un paquete minimo para que una issue sea ejecutable
### Problema detectado
Una issue puede pasar a desarrollo sin dejar trazado de forma literal su origen funcional ni sus dependencias, obligando a reinterpretar documentos antes de empezar.

### Propuesta
Exigir que toda issue lista para `developer-teams` incluya y mantenga en este orden:
- `Backlog:`
- `Historia de usuario:`
- `Caso de uso:`
- `Criterios de aceptacion:`
- `Dependencias:`
- `Estado operativo: nuevo`

Ademas, `developer-teams` no debe iniciar implementacion si ese paquete minimo falta.

### Impacto esperado
- Reduce arranques en falso y preguntas repetidas antes de abrir rama.
- Hace mas visible si el bloqueo esta en refinamiento funcional y no en capacidad tecnica.
- Mejora la trazabilidad entre producto, desarrollo y QA desde el inicio del ciclo.

### Tradeoffs
- `product-manager` debe invertir algo mas de disciplina al abrir o refrescar issues.

### Riesgos y dependencias
- Si los campos se rellenan con texto ambiguo, el beneficio baja aunque el formato exista.
- Requiere que `developer-teams` frene el inicio cuando la issue no sea realmente operable.

## Mejora 10: sustituir la referencia historica de `changelog/` por una guia vigente
### Problema detectado
La referencia usada por los roles para el `changelog/` ya no refleja todas las reglas actuales, en especial la hora obligatoria por entrada.

### Propuesta
Crear `changelog/README.md` como referencia estable de formato, con plantilla minima y nota explicita de que los ficheros historicos anteriores pueden no cumplir reglas introducidas despues.

### Impacto esperado
- Reduce contradicciones entre ejemplo historico y norma vigente.
- Facilita que todos los roles registren entradas homogoneas sin reinterpretar excepciones.
- Mejora la utilidad del `changelog/` como evidencia operativa y fuente de auditoria ligera.

### Tradeoffs
- Introduce un fichero documental adicional de mantenimiento sencillo.

### Riesgos y dependencias
- Si los roles siguen copiando formatos antiguos por inercia, la mejora tardara en consolidarse.
- Conviene actualizar tambien las referencias en todos los `AGENTS.md` afectados.

## Mejora 11: activar documentacion solo tras integracion real en `main`
### Problema detectado
`doc-teams` trabaja sobre `main`, pero podia activarse con una entrega `validado` todavia no fusionada, lo que fuerza a distinguir manualmente entre trabajo aceptado y comportamiento realmente disponible.

### Propuesta
- Cambiar el disparador de `doc-teams` para exigir simultaneamente `Estado operativo: validado`, `Impacto documental: si` y rama tecnica ya fusionada en `main`.
- Reforzar que `developer-teams` priorice el merge y el borrado de rama tras QA antes de iniciar una nueva issue, salvo bloqueo operativo documentado.

### Impacto esperado
- Evita que la documentacion oficial se adelante a la realidad integrada del producto.
- Reduce el tiempo en que una issue queda `validado` pero sin cierre operativo claro.
- Hace mas lineal la secuencia `validado -> merge -> documentacion -> cierre administrativo`.

### Tradeoffs
- `doc-teams` puede entrar un poco mas tarde en algunas iteraciones si el merge no se ejecuta con disciplina.

### Riesgos y dependencias
- Si `developer-teams` retrasa el merge sin dejar bloqueo explicito, la cola documental seguira esperando aunque QA ya haya aceptado la entrega.
- Requiere que `product-manager` mantenga visible el bloqueo cuando una issue validada no pueda cerrarse aun.

## Mejora 12: fijar un comentario minimo de arranque para `developer-teams`
### Problema detectado
El inicio de una issue exige informar rama y estado, pero no quedaba anclado a una plantilla literal unica.

### Propuesta
Obligar a que el arranque de una issue use al menos:
- `Rama:`
- `Estado operativo: en desarrollo`

### Impacto esperado
- Hace visible de inmediato que rama esta activa en cada issue.
- Facilita vigilar el limite de dos ramas tecnicas abiertas.
- Mejora la lectura del tiempo real hasta inicio de desarrollo.

### Tradeoffs
- Introduce un comentario adicional muy corto al comienzo del trabajo tecnico.

### Riesgos y dependencias
- Si el comentario se publica tarde, la metrica de arranque seguira distorsionada.
- Requiere que `developer-teams` mantenga actualizada la referencia si cambia de rama.

## Mejora 13: mantener sincronizado el `Estado operativo:` visible en la issue
### Problema detectado
El cuerpo de la issue puede seguir mostrando `Estado operativo: nuevo` aunque el trabajo real ya este en desarrollo, en QA o incluso `no validado`.

### Propuesta
Exigir que el rol que produzca cada transicion operativa actualice tambien el campo `Estado operativo:` del cuerpo de la issue en GitHub, ademas de dejar su comentario estructurado.

### Impacto esperado
- Mejora la lectura rapida del backlog abierto sin obligar a inspeccionar comentarios.
- Reduce errores de priorizacion sobre issues aparentemente `nuevo` que en realidad ya estan en curso o devueltas por QA.
- Hace mas util el estado operativo como fuente de verdad compartida.

### Tradeoffs
- Introduce una accion adicional de mantenimiento en GitHub para los roles que ya comentan la issue.

### Riesgos y dependencias
- Si la actualizacion del cuerpo se olvida, reaparece la divergencia entre backlog visible y flujo real.
- Conviene limitar la edicion al campo `Estado operativo:` para no reescribir contexto funcional por error.

## Mejora 14: reforzar la reentrega tras `no validado`
### Problema detectado
La regla de revalidacion existe, pero `developer-teams` aun podia interpretar que bastaba con corregir codigo sin reemitir un handoff completo ni reflejar el nuevo estado visible en la issue.

### Propuesta
Tras un `no validado`, exigir a `developer-teams` que:
- priorice esa misma issue frente a nuevas issues
- mantenga la misma rama mientras el alcance no cambie
- publique un nuevo comentario de entrega con la plantilla completa
- vuelva a actualizar el `Estado operativo:` del cuerpo de la issue a `listo para qa`

### Impacto esperado
- Reduce revalidaciones ambiguas o sin contexto incremental claro.
- Mantiene trazabilidad comparable entre la primera entrega y las reentregas.
- Evita que QA tenga que deducir si ya existe una nueva entrega realmente revisable.

### Tradeoffs
- La iteracion de correccion gana algo de disciplina documental.

### Riesgos y dependencias
- Si el alcance cambia materialmente y se mantiene la misma issue, la reentrega seguira siendo confusa.
- Requiere que `product-manager` abra una nueva issue cuando la correccion deje de ser el mismo alcance.

## Mejora 15: convertir el paquete minimo de handoff en gate explicito de QA
### Problema detectado
La plantilla de entrega existia, pero QA no tenia una regla suficientemente clara para rechazar desde el inicio una entrega incompleta o desalineada con `main`.

### Propuesta
Antes de validar funcionalmente, `qa-teams` debe comprobar que:
- el comentario de `developer-teams` incluye la plantilla minima de handoff
- la rama integra limpia con `main`

Si alguna condicion falla, QA debe cerrar la revision como `Estado operativo: no validado`.

### Impacto esperado
- Evita que QA asuma trabajo de reconstruccion del contexto.
- Separa defectos de proceso de defectos funcionales.
- Refuerza el cumplimiento real de las reglas de handoff.

### Tradeoffs
- Puede aumentar el numero de `no validado` por causas operativas en el corto plazo.

### Riesgos y dependencias
- Si QA aplica la regla de forma mecanica sin describir bien el bloqueo, desarrollo no tendra feedback accionable.
- Requiere que `developer-teams` siga tratando la sincronizacion con `main` como paso previo real y no solo declarado.

## Mejora 16: incorporar `Rol:` dentro de todas las plantillas operativas de issue
### Problema detectado
Las reglas globales exigen que cualquier comentario en una issue empiece con `Rol: <nombre-del-rol>`, pero varias plantillas de arranque, entrega y revision seguian empezando directamente por los campos funcionales.

### Propuesta
- Hacer que todas las plantillas minimas copien la linea `Rol: ...` como primer campo.
- Ajustar los `AGENTS.md` de raiz y de los roles que usan esas plantillas para que la regla no quede separada del ejemplo.

### Impacto esperado
- Reduce incumplimientos por olvido de una regla que hoy esta fuera de la plantilla.
- Mejora la lectura rapida de las issues y la trazabilidad por rol.
- Facilita automatizar o auditar comentarios estructurados sin inferencias adicionales.

### Tradeoffs
- Anade una linea fija mas a cada comentario estructurado.

### Riesgos y dependencias
- Si algun equipo sigue reutilizando ejemplos historicos antiguos, la mejora tardara unas iteraciones en consolidarse.
- Conviene actualizar a la vez acuerdos operativos y `AGENTS.md` para no dejar dos plantillas competidoras.

## Mejora 17: hacer explicito que el cierre administrativo sincroniza la issue a `cerrado`
### Problema detectado
El repositorio ya exige que el cuerpo de la issue refleje el ultimo estado real, pero el cierre administrativo no remarcaba con suficiente claridad que esa sincronizacion final debe dejar `Estado operativo: cerrado`.

### Propuesta
- Exigir de forma literal que `product-manager`, al cerrar una issue, actualice tambien su cuerpo a `Estado operativo: cerrado`.
- Reflejar la misma regla en acuerdos operativos y en las instrucciones del propio rol.

### Impacto esperado
- Evita que una issue cerrada siga mostrando `validado` en el cuerpo.
- Mejora la consistencia historica del backlog y de las metricas de flujo.
- Reduce trabajo correctivo posterior sobre issues ya cerradas.

### Tradeoffs
- Introduce un ultimo paso administrativo mas en el cierre, aunque de bajo coste.

### Riesgos y dependencias
- Si el cierre se hace con prisa y sin editar el cuerpo, el problema seguira existiendo aunque la regla sea clara.
- Requiere disciplina de `product-manager` en el mismo momento del cierre, no en una correccion posterior.

## Mejora 18: sincronizar el estado del backlog con la issue activa
### Problema detectado
El backlog funcional puede conservar un estado de planificacion que ya no coincide con el estado operativo visible de la issue asociada.

### Propuesta
Cuando un item tenga issue activa, el campo `Estado` del backlog debe reflejar el mismo estado operativo que la issue o, como minimo, no puede quedarse en `nuevo` si la issue ya paso por `en desarrollo`, `listo para qa`, `no validado`, `validado` o `cerrado`.

### Impacto esperado
- Evita que `product-manager` lea una pieza en re-trabajo como si estuviera todavia sin arrancar.
- Mejora la lectura rapida del backlog y la priorizacion de reentregas.
- Reduce la divergencia entre documento de producto, issue de GitHub y flujo real del equipo.

### Tradeoffs
- Obliga a que `product-manager` actualice un artefacto mas en cada transicion relevante.

### Riesgos y dependencias
- Si se actualiza solo la issue y no el backlog, la mejora pierde valor.
- Conviene que la regla quede anclada tambien en el `AGENTS.md` de `product-manager` para que no dependa de memoria.

## Mejora 19: definir una referencia canónica para las reglas compartidas de coordinacion
### Problema detectado
Las reglas comunes de estados, handoffs y cierre estan repartidas entre varios `AGENTS.md`, `README.md` y `changelog/README.md`, lo que obliga a mantener varias copias del mismo criterio y abre la puerta a versiones divergentes.

### Propuesta
Declarar `agile-coach/acuerdos-operativos.md` como referencia canónica para:
- estados operativos comunes
- plantillas literales de handoff
- checkpoints de sincronizacion entre equipos
- reglas de cierre administrativo y revalidacion

Mantener `AGENTS.md` y `README.md` como superficies de consulta y resumen, pero indicando de forma explicita que cualquier cambio de redaccion compartida debe nacer primero en `agile-coach/acuerdos-operativos.md` y luego propagarse a las copias necesarias.

### Impacto esperado
- Reduce el coste de mantenimiento de las reglas de coordinacion.
- Disminuye el riesgo de que dos equipos trabajen con una version distinta de la misma norma.
- Hace mas claro donde revisar la redaccion vigente antes de modificar una plantilla o un estado.

### Tradeoffs
- Introduce una capa mas de referencia documental que hay que conocer al principio.
- Requiere disciplina para actualizar la fuente canónica antes que las copias derivadas.

### Riesgos y dependencias
- Si el equipo ignora la referencia canónica y edita solo las copias, la deriva reaparecera.
- Conviene mantener esta regla visible tambien en `AGENTS.md` de raiz y en la guia principal del proyecto.

## Mejora 20: introducir un checkpoint de sincronizacion documental despues del merge
### Problema detectado
La issue validada puede quedar integrada en `main` mientras backlog, refinamiento o roadmap siguen mostrando un estado previo.

### Propuesta
Tras cada merge de una entrega validada, `product-manager` debe reconciliar el backlog, el refinamiento funcional y el roadmap afectados antes de iniciar una nueva issue funcional. Si la issue sigue abierta por cierre administrativo, el comentario debe indicar tambien si la documentacion de producto ya quedo sincronizada o sigue pendiente.

### Impacto esperado
- Reduce desfase entre `main` y los artefactos funcionales.
- Hace visible si el bloqueo restante es solo administrativo.
- Evita que el siguiente arranque use un mapa de producto desactualizado.

### Tradeoffs
- Añade un paso documental mas al cierre de iteracion.

### Riesgos y dependencias
- Si `product-manager` no actualiza los artefactos en el mismo ciclo, reaparece el desfase.
- Requiere que la regla quede reflejada tambien en `AGENTS.md` de `product-manager` y en los acuerdos operativos.

## Mejora 21: hacer visible el cierre tecnico de una issue validada
### Problema detectado
Una issue puede permanecer `validado` y abierta sin dejar una huella operativa clara de que la rama tecnica ya fue fusionada y borrada.

### Propuesta
- Exigir que, una vez completado el merge y el borrado de la rama, `developer-teams` deje un comentario adicional de cierre de integracion con `Rama:`, `Merge en main:` y `Rama eliminada:`.
- Exigir que `product-manager` no cierre definitivamente la issue hasta ver ese comentario o dejar constancia explicita de que la integracion sigue pendiente.

### Impacto esperado
- El backlog distingue mejor entre validacion funcional y cierre tecnico-administrativo.
- Se reduce la posibilidad de que una issue aceptada siga pareciendo trabajo en curso por falta de limpieza visible.
- `product-manager` puede cerrar con una evidencia breve y comparable, en vez de inferirla a partir de varias fuentes.

### Tradeoffs
- Añade un comentario operativo corto mas al final del flujo.

### Riesgos y dependencias
- Si el comentario se rellena de forma mecanica y sin evidencia real, el valor de la regla baja.
- Requiere disciplina de `developer-teams` para ejecutar el borrado de rama inmediatamente despues del merge.

## Mejora 22: separar la trazabilidad historica del `changelog/` de la evidencia de integracion en `main`
### Problema detectado
Una entrada de `changelog/` puede mencionar una validacion o un avance operativo aunque la evidencia tecnica vigente en `main` siga sin mostrar la integracion completa de la entrega.

### Propuesta
Dejar explicitamente en los acuerdos operativos y en `AGENTS.md` que:
- `main` es la referencia para saber si una entrega ya esta realmente integrada.
- El comentario de cierre de integracion de `developer-teams` y el comentario administrativo de `product-manager` son la evidencia operativa del cierre.
- `changelog/` solo conserva trazabilidad historica y no sustituye ni al merge ni al borrado de rama ni al cierre administrativo.

### Impacto esperado
- Evita leer una entrega como integrada solo porque aparezca asi en el `changelog/`.
- Reduce contradicciones entre la evidencia tecnica, el estado visible de la issue y la documentacion de proceso.
- Hace mas fiable la revision documental de `doc-teams` y la lectura de backlog por `product-manager`.

### Tradeoffs
- Obliga a revisar una fuente mas antes de dar por cerrado un trabajo validado.
- Requiere mantener muy clara la diferencia entre historia operativa y estado vigente.

### Riesgos y dependencias
- Si los equipos siguen usando el `changelog/` como prueba de estado actual, la ambiguedad reaparecera.
- La mejora depende de que `developer-teams` deje el comentario de cierre de integracion y de que `product-manager` no cierre la issue sin esa evidencia.

## Mejora 23: usar la documentacion de estado vigente como segundo detector de deriva post-merge
### Problema detectado
Tras integrar una entrega validada, el backlog puede seguir mostrando un estado anterior aunque la documentacion de estado vigente mantenida por `doc-teams` ya refleje la realidad de `main`.

### Propuesta
- En el checkpoint post-merge, `product-manager` debe contrastar el estado del backlog con la documentacion de estado vigente de `doc-teams`.
- Si ambos documentos divergen, la copia a corregir primero es la que sigue arrastrando el estado anterior, normalmente el backlog.
- El comentario administrativo de cierre debe dejar visible si esa reconciliacion documental ya quedo hecha o sigue pendiente.

### Impacto esperado
- Reduce la probabilidad de que el backlog se convierta en una fotografia antigua mientras la documentacion de estado vigente ya esta actualizada.
- Hace mas claro que documento esta atrasado cuando la discrepancia no es funcional sino de coordinacion.
- Mejora la deteccion temprana de cierre administrativo incompleto sin obligar a revisar varias fuentes por separado.

### Tradeoffs
- Introduce una comprobacion documental adicional en el cierre post-merge.

### Riesgos y dependencias
- Si `doc-teams` y `product-manager` actualizan sus artefactos en momentos distintos, la discrepancia puede reaparecer temporalmente.
- Requiere que el backlog y la documentacion de estado se revisen en el mismo ciclo que el merge, no en una iteracion posterior.

## Secuencia prioritaria de adopcion
Las mejoras anteriores ya cubren la mayor parte de las fricciones detectadas. Para que el cambio de proceso tenga impacto rapido y no genere mas ruido del necesario, la adopcion recomendada es esta:

1. Blindar las plantillas operativas con `Rol:` como primera linea y con el `Estado operativo:` visible en el cuerpo de la issue.
2. Exigir evidencia de cierre tecnico tras `validado`: merge en `main` y borrado de la rama antes del cierre administrativo.
3. Mantener sincronizados backlog, refinamiento funcional y roadmap en el mismo ciclo en que cambia el estado real de la issue.
4. Usar la documentacion de estado vigente como detector adicional de backlog desfasado tras el merge.
5. Reducir duplicidad documental dejando las reglas compartidas en `agile-coach/acuerdos-operativos.md` y reservando a `AGENTS.md` y `README.md` solo las referencias o plantillas minimas.

### Impacto esperado
- Recorta la probabilidad de deriva entre documentos y comentarios operativos.
- Hace que los cambios de estado sean mas visibles y auditablemente comparables.
- Baja el coste de mantenimiento de futuras mejoras de proceso.

### Tradeoffs
- Obliga a editar varios documentos en una misma iteracion si se quiere mantener la coherencia.
- Puede parecer mas estricto al principio, pero evita rehacer trabajo por estados o plantillas ambiguas.

### Riesgos y dependencias
- Si la secuencia se adopta de forma parcial, reapareceran las mismas inconsistencias en distintas fuentes.
- La reduccion de duplicidad documental solo funciona si las copias derivadas dejan de reescribir reglas ya fijadas en la guia canónica.

## Mejora 24: medir el coste de propagar reglas compartidas
### Problema detectado
Aunque las reglas compartidas ya tienen una referencia canónica, cada cambio sigue obligando a revisar varias superficies documentales y eso hace visible solo una parte del coste de mantenimiento.

### Propuesta
Registrar, en cada cambio de proceso relevante, el tiempo que tarda en propagarse la regla desde `agile-coach/acuerdos-operativos.md` hasta las copias derivadas que sigan siendo necesarias. Si la propagacion obliga a editar muchas superficies o se alarga mas de lo razonable dentro del mismo ciclo, revisar si alguna copia sigue aportando valor operativo o si puede reducirse a una remision breve.

### Impacto esperado
- Hace visible el coste real de mantener reglas compartidas en varios documentos.
- Ayuda a detectar temprano cuando la documentacion de proceso esta demasiado fragmentada.
- Reduce el riesgo de que una copia quede atrasada sin que nadie lo note hasta la siguiente iteracion.

### Tradeoffs
- Añade una comprobacion ligera mas cuando se cambie una regla compartida.
- Puede parecer un control extra si la estructura documental ya esta bien sincronizada.

### Riesgos y dependencias
- Si la medicion no se usa en revisiones posteriores, solo añadira registro sin mejorar el proceso.
- Depende de que `agile-coach/acuerdos-operativos.md` siga siendo la referencia primaria y de que las copias deriven de ella, no al reves.
