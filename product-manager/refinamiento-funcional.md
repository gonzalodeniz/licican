# Refinamiento Funcional de Licican

## Estado actual
La vision sigue siendo consistente con la propuesta de valor central. No se detectan contradicciones de fondo, pero si una necesidad permanente de acotar el lenguaje de "centralizacion" para no confundir cobertura progresiva con cobertura total.
La prioridad funcional vigente se mantiene en la operativizacion del dato real disponible en `data/`: `PB-011` ya esta validado, integrado en `main` y cerrado administrativamente, y `PB-012` ya quedo validado, integrado en `main` y cerrado administrativamente tras la reconciliacion operativa del 2026-03-30.
`PB-004` deja de formar parte del trabajo abierto: tras la validacion explicita de `qa-teams` en la issue #6 el 2026-03-25, `developer-teams` integro la entrega en `main` y elimino la rama tecnica el 2026-03-26, por lo que producto debe tratarla ya como funcionalidad vigente.

## Huecos de definicion detectados en esta revision
- La inconsistencia principal detectada en esta revision es de trazabilidad operativa: la issue #11 ya figura como `validado` por `qa-teams`, pero varios artefactos de producto seguian tratandola como `nuevo`.
- El siguiente hueco relevante ya no es funcional en `PB-012`, sino de priorizacion: la issue `#14` sustituyo la fuente de datos por PostgreSQL, ya quedo validada por `qa-teams`, se integro en `main` y se cerro administrativamente.
- Aparece una regresion tecnica en el filtrado del catalogo tras la migracion a PostgreSQL que debe corregirse antes de abrir nueva expansion funcional.
- Aparece una necesidad de escalado de consulta: los resultados del catalogo necesitan paginacion una vez el backend PostgreSQL sostiene mas volumen.
- Aparece una necesidad de gobierno de datos: el producto necesita una vista de panel de control para parametrizar la antiguedad de conservacion y archivado de licitaciones.
- Aparece un hueco de trazabilidad de dato: la ficha de licitacion o contrato debe mostrar el nombre del fichero `.atom` origen de la version consolidada.
- Aparece un hueco de validacion funcional: `qa-teams` necesita una correspondencia operativa entre la aplicacion y el Excel `data/licitaciones_ti_canarias.xlsx`, al menos en `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones`.
- Aparece una dependencia de priorizacion tecnica: los informes de auditoria de calidad y seguridad del 2026-03-28 deben convertirse en issues tecnicas por `developer-teams` antes de que producto pueda ordenar su capacidad frente al roadmap funcional.

## Estado funcional confirmado en el repositorio
- `PB-007` dispone de entrega visible en producto y validacion explicita de `qa-teams` en la issue #1.
- La entrega de `PB-007` cubre delimitacion de fuentes, no ingestion real ni catalogo de licitaciones.
- `PB-006` ya quedo validado por `qa-teams` en la issue #2 y deja una superficie funcional auditable previa al catalogo de `PB-001`.
- `PB-001` ya quedo validado por `qa-teams` en la issue #3 y aporta el catalogo visible inicial sobre cobertura MVP y clasificacion TI vigente.
- `PB-002` ya quedo validado por `qa-teams` en la issue #4 y amplia el catalogo con ficha de detalle y tratamiento visible de rectificaciones o modificaciones del expediente.
- `PB-003` ya fue revalidado por `qa-teams` en la issue #5 el 2026-03-20, integrado en `main` por `developer-teams` el 2026-03-21 y cerrado administrativamente por `product-manager`.
- `PB-004` ya fue validado por `qa-teams` en la issue #6 el 2026-03-25, integrado en `main` por `developer-teams` el 2026-03-26 y debe tratarse ya como alcance vigente.
- `PB-011` ya fue validado por `qa-teams` en la issue #11 el 2026-03-27, integrado en `main` por `developer-teams` el 2026-03-28 y cerrado administrativamente por `product-manager` ese mismo dia.

## Huecos funcionales cerrados en esta revision
- Queda definida la regla funcional para expedientes mixtos donde TI no es el unico componente.
- Queda definido el tratamiento minimo de oportunidades anuladas, desiertas, desistidas o modificadas.
- Queda identificado como deuda de trazabilidad el formato incompleto de varios issues abiertos, que debe corregirse para cumplir las reglas del repositorio.
- Queda despejada la dependencia funcional entre catalogo y ficha: el catalogo base, la ficha, el filtrado, las alertas, la priorizacion de fuentes reales, la consolidacion `.atom` y la validacion funcional de `PB-012` ya estan resueltos; la siguiente capa accionable combina la integracion administrativa de `PB-012`, una base de interfaz comun posterior en `PB-010` y formalizacion operativa de permisos en `PB-013`.
- Queda definido que una alerta del MVP necesita al menos un criterio funcional informado y no puede guardarse vacia.
- Queda definido que el alta inicial en pipeline crea siempre el estado `Nueva`.
- Queda definido que `PB-008` puede avanzar como definicion funcional de KPIs aunque la instrumentacion completa llegue en una iteracion posterior.
- Queda incorporada como prioridad explicita la recopilacion desde fuentes reales oficiales nominadas, ya que `PB-007` solo cerraba cobertura funcional y no orden de implementacion de fuentes reales.
- Queda definido que el rediseño de interfaz solicitado debe materializarse como un item funcional trazable y no como una observacion informal para desarrollo.
- Queda corregida la lectura funcional de `PB-004`: el trabajo ya no esta pendiente ni de desarrollo ni de integracion; pasa a referencia funcional ya entregada.
- Queda definida la siguiente fuente operativa inmediata para desarrollo: todos los `.atom` presentes en `data/`, sin anclar la solucion a un nombre de fichero estable.
- Queda definida la regla estructurada de filtrado para esta iteracion: Canarias por `ES7` o jerarquia territorial, y TI por CPVs con prefijo `72`, `48` o `302`.
- Queda definido que la salida funcional visible debe poder contrastarse con `data/licitaciones_ti_canarias.xlsx`.

## Incidencia operativa abierta prioritaria
- La secuencia de trabajo ya no tiene bloqueos funcionales ni de validacion asociados a `PB-009` ni a `PB-004`.
- `qa-teams` valido la entrega integrada en `main` de `PB-009` el 2026-03-24 y `product-manager` cerro la issue #9 el 2026-03-25.
- `qa-teams` valido `PB-004` el 2026-03-25 y `developer-teams` dejo constancia de integracion y borrado de rama el 2026-03-26.
- `qa-teams` valido `PB-012` el 2026-03-29 sobre la rama `developer-teams/issue-12-pb-012-vistas-excel`, y `developer-teams` ya dejo despues la evidencia requerida de fusion en `main` y borrado de rama.
- Con `PB-011`, `PB-012` y la issue tecnica `#14` ya cerradas, la siguiente prioridad operativa inmediata es reordenar `PB-010` y `PB-013` antes de abrir otra implementacion.
- `T-002` ya quedo validado por `qa-teams`, integrado en `main` por `developer-teams` y cerrado administrativamente por `product-manager`.
- `PB-014` y `PB-015` aparecen como nuevas piezas funcionales para escalado de consulta y gobierno de datos; deben planificarse despues del cierre administrativo de `T-002`.
- `PB-010` permanece como necesidad de experiencia transversal, pero deja de ser la siguiente pieza funcional inmediata.
- `PB-013` aparece como nuevo hueco ejecutable: el modelo de roles y permisos ya esta definido por producto y puede arrancar cuando producto lo priorice sobre `PB-010` u otras piezas posteriores.
- Se detecto y corrige una inconsistencia de alcance: `PB-013` no debe quedar bloqueada por `PB-005`, porque su primera iteracion se aplica a superficies ya disponibles y la extension a pipeline debe heredar la misma matriz mas adelante.
- Los informes de `quality-auditor` y `security-auditor` del 2026-03-28 quedan aceptados como entrada formal de priorizacion; falta que `developer-teams` materialice sus hallazgos accionables en issues tecnicas separadas para poder ordenarlas frente a `PB-010`, `PB-005` y `PB-008`.
- Producto debe reservar capacidad visible para esos hallazgos antes de comprometer nueva expansion funcional posterior a `PB-012`.

## Decisiones funcionales vigentes
- El MVP de negocio se compone de dos escalones:
  - escalon 1: cobertura acotada, regla de relevancia TI, catalogo, detalle y filtros
  - escalon 2: recopilacion prioritaria desde fuentes reales oficiales
  - escalon 3: alertas y pipeline
- La comunicacion del producto debe hablar de cobertura inicial priorizada, no de cobertura total.
- La recopilacion de contratos y concursos debe priorizar fuentes reales oficiales y verificables antes de invertir en capacidades de retencion no esenciales.
- La ejecucion funcional de esa prioridad se ordena por olas para reducir dispersion:
  - `Ola 1`: `BOC`
  - `Ola 2`: `BOP Las Palmas`
  - `Ola 3`: `BOE`
- La relevancia TI debe poder explicarse y auditarse sin depender de interpretaciones tecnicas implicitas.
- La regla TI ya puede validarse de forma observable antes de construir el catalogo, pero su casuistica seguira refinandose con ejemplos reales.
- El pipeline minimo sigue limitado a los estados `Nueva`, `Evaluando`, `Preparando oferta`, `Presentada` y `Descartada`.
- La primera iteracion de permisos de `PB-013` debe gobernar catalogo, detalle, filtros, vistas consolidadas, alertas y administracion visible; pipeline se incorpora despues sin redefinir la matriz funcional.
- La primera iteracion de alertas queda limitada a registrar coincidencias internas; la notificacion saliente se evaluara en una fase posterior.
- Una alerta vacia no es valida: debe incluir al menos un criterio funcional entre palabra clave, presupuesto, procedimiento o ubicacion.
- El pipeline MVP queda limitado a gestion individual por usuario; la colaboracion por empresa no forma parte del alcance actual.
- La primera vez que una oportunidad entra en pipeline debe hacerlo en estado `Nueva`.
- La definicion de KPIs de `PB-008` no exige disponer desde el primer dia de toda la instrumentacion automatizada, pero si exige dejar explicita cualquier limitacion de medicion.
- La primera entrega de `PB-009` debe conservar, como minimo por oportunidad recopilada, referencia a la fuente oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando la fuente lo publique.
- `PB-009` no cambia por si solo la promesa comercial de cobertura ni adelanta funcionalidades de alertas o pipeline.
- La siguiente iteracion operativa debe tomar todos los `.atom` presentes en `data/` aunque cambien fecha y hora en su nombre.
- El filtro geografico principal para Canarias en esta iteracion es `CountrySubentityCode` con prefijo `ES7`; si no basta, deben usarse `ParentLocatedParty` y `CountrySubentity` como apoyo.
- La siguiente iteracion operativa considera TI por CPVs con prefijo `72`, `48` o `302`.
- Si un expediente aparece repetido entre snapshots `.atom`, la aplicacion debe conservar una unica version funcional con el dato oficial mas reciente disponible.
- El detalle de licitacion o contrato debe hacer visible el nombre del fichero `.atom` origen de la version vigente.
- La superficie visible de la iteracion debe alinearse funcionalmente con las pestañas `Licitaciones TI Canarias`, `Detalle Lotes` y `Adjudicaciones` del Excel `data/licitaciones_ti_canarias.xlsx`.
- La navegacion principal de la aplicacion debe resolverse desde una estructura comun con menu lateral izquierdo de iconos cuando el ancho disponible lo permita.
- La adaptacion responsive es un requisito funcional de producto: la interfaz debe conservar acceso a opciones principales y legibilidad del contenido al cambiar el ancho de la ventana.
- Las opciones principales aun no operativas no deben aparecer como rutas plenamente disponibles sin senalizacion explicita.

## Regla funcional vigente para expedientes mixtos
- Un expediente mixto debe considerarse TI en el MVP cuando se cumpla al menos una de estas condiciones:
  - el objeto principal o entregable dominante menciona de forma explicita software, sistemas, ciberseguridad, redes, cloud, datos, licencias o infraestructura TIC
  - el CPV principal es tecnologico
  - la parte TI es sustancial para el valor esperado del contrato y resulta indispensable para cumplir su objeto
- Un expediente mixto no debe considerarse TI cuando:
  - la parte tecnologica es accesoria o secundaria respecto al objeto principal
  - la evidencia funcional disponible no permite afirmar que la necesidad TI sea sustancial
- Si la informacion de origen no permite decidir con seguridad, el expediente debe tratarse como caso frontera y quedar fuera del catalogo visible del MVP hasta nuevo refinamiento.

## Tratamiento funcional vigente del ciclo de vida de oportunidades
- Si una oportunidad pasa a estado oficial `anulada`, `desierta` o `desistida`, debe seguir siendo visible con ese estado para preservar contexto historico.
- Una oportunidad con esos estados oficiales no debe presentarse como nueva oportunidad accionable ni generar nuevas alertas accionables.
- Si la oportunidad ya estaba guardada en pipeline, el sistema debe conservar el estado de trabajo del usuario y mostrar el estado oficial como advertencia visible.
- Si la fuente publica una modificacion o rectificacion del mismo expediente, el producto debe mantener la misma referencia funcional y mostrar el ultimo dato oficial disponible en campos criticos como fecha limite o presupuesto.
- El historial detallado de cambios oficiales queda fuera del MVP; por ahora basta con exponer el ultimo dato oficial visible.

## Reglas funcionales vigentes de clasificacion TI
- Se considera candidata TI una oportunidad que cumpla al menos uno de estos criterios:
  - menciona software, desarrollo, sistemas, soporte TI, ciberseguridad, redes, licencias, cloud, datos o hardware tecnologico
  - incluye CPVs alineados con servicios o suministros tecnologicos
  - describe una necesidad de digitalizacion, mantenimiento de sistemas o infraestructura TIC
- Se considera no TI, salvo evidencia contraria:
  - obra civil sin componente tecnologico relevante
  - suministros generales de mobiliario o material no tecnologico
  - servicios administrativos o de consultoria no vinculados a tecnologia
- Casos frontera que requieren criterio verificable adicional:
  - contratos mixtos donde TI sea una parte menor
  - servicios de telecomunicaciones no claramente ligados a sistemas o redes
  - expedientes de digitalizacion formulados con lenguaje demasiado generico

## Cobertura funcional vigente para MVP
- Estado `MVP`:
  - Plataforma de Contratacion del Sector Publico filtrada por organos de contratacion de Canarias
  - Gobierno de Canarias
  - Cabildos insulares
- Estado `Posterior`:
  - Ayuntamientos con perfiles del contratante propios
  - Empresas publicas y consorcios
- Estado `Por definir`:
  - Fuentes con acceso inconsistente, formatos no estandar o baja frecuencia de oportunidades TI

## Fuentes reales oficiales priorizadas para recopilacion
- `Ola 1`:
  - `BOC` (`https://www.gobiernodecanarias.org/boc/`)
- `Ola 2`:
  - `BOP Las Palmas` (`https://www.boplaspalmas.net/nbop2/index.php`)
- `Ola 3`:
  - `BOE` (`https://www.boe.es/`)
- Prioridad alta posterior o dependiente de validacion adicional:
  - perfiles del contratante y boletines oficiales adicionales que aporten oportunidades TI relevantes para Canarias, incluidos cabildos y otros boletines provinciales o locales
- Criterio funcional:
  - si una fuente es oficial, real y aporta señal temprana de contratos o concursos aprovechables por el usuario objetivo, debe evaluarse antes que nuevas capacidades de engagement no esenciales
- Minimo funcional verificable por oportunidad recopilada en `PB-009`:
  - identificacion visible de la fuente oficial
  - enlace oficial clicable o accesible
  - fecha de publicacion o equivalente oficial visible
  - estado oficial del expediente cuando la fuente lo informe
- Fuera de alcance de esta iteracion:
  - notificaciones salientes al usuario
  - automatizacion completa de pipeline
  - ampliacion de promesa comercial a cobertura total o a ayuntamientos no confirmados

## Dependencias abiertas
- Confirmar con negocio si el MVP debe cubrir tambien ayuntamientos desde la primera promesa comercial o si permanecen fuera de la comunicacion inicial.
- Definir mas adelante si las modificaciones oficiales del expediente requieren un historial visible de cambios en lugar de mostrar solo el ultimo dato disponible.
- Decidir si la primera captura operativa de KPIs de alertas se resolvera con medicion manual temporal o se aplazara hasta disponer de mas instrumentacion.
- Confirmar con negocio si la siguiente evolucion de alertas debe seguir centrada en registro interno de coincidencias o exigir ya una primera salida visible adicional para el usuario sin llegar todavia a notificacion externa.
- Recibir de `developer-teams` las issues tecnicas derivadas de los hallazgos de `quality-auditor` y `security-auditor` del 2026-03-28 para reservar y ordenar capacidad.

## Riesgos de producto
- Riesgo de falsa expectativa si se comunica "todas las licitaciones canarias" sin matizar la cobertura inicial real.
- Riesgo de falsos positivos si desarrollo interpreta de forma laxa que una parte TI es "sustancial" en expedientes mixtos.
- Riesgo de baja adopcion si el MVP entrega solo agregacion pero no relevancia util.
- Riesgo de frustracion si faltan datos criticos en fichas sin indicarse claramente su ausencia.
- Riesgo operativo si desarrollo declara rutas o superficies de validacion no expuestas realmente en la entrega revisable.
- Riesgo de credibilidad si el producto retrasa la recopilacion real y prioriza antes capacidades de retencion sobre fuentes oficiales verificables.
- Riesgo de dispersion si `developer-teams` intenta abordar simultaneamente las tres fuentes prioritarias sin un orden de entrega ni un minimo comun verificable.
- Riesgo de carga incompleta si desarrollo ata la ingesta a un nombre fijo de fichero `.atom` y no a la presencia dinamica de todos los `.atom` en `data/`.
- Riesgo de falsos positivos o falsos negativos si la extraccion no aplica de forma combinada los criterios estructurados de Canarias y CPV TI ya definidos para esta iteracion.
- Riesgo de opacidad si el detalle no expone el fichero origen y `qa-teams` no puede reconciliar aplicacion con Excel y snapshots.
- Riesgo de inconsistencia de experiencia si cada nueva vista incorpora navegacion propia en lugar de una estructura principal comun y responsive.
- Riesgo operativo si la documentacion de producto no refleja con rapidez las integraciones ya realizadas en `main` y sigue guiando al equipo con prioridades desfasadas.
- Riesgo operativo si producto no reordena con suficiente claridad `PB-010` y `PB-013` tras cerrar la issue tecnica `#14`, porque la siguiente implementacion activa debe seguir siendo inequoca.
- Riesgo funcional si el crecimiento de alertas, pipeline o futuras vistas no aplica de forma consistente el modelo de roles y permisos ya definido.
- Riesgo de roadmap sesgado si los hallazgos tecnicos y de seguridad del 2026-03-28 no se convierten pronto en trabajo trazable y compiten de forma invisible con nuevas funcionalidades.
- Riesgo de planificacion irreal si `PB-013` se mantiene ligada a dependencias aun no visibles y se retrasa un control de acceso que ya puede acotarse sobre superficies existentes.

## Supuestos explicitos
- El primer objetivo es demostrar que la centralizacion y el filtrado ahorran tiempo al usuario.
- La cobertura total del ecosistema canario se abordara de forma incremental.
- `qa-teams` validara primero comportamiento funcional observable, no exhaustividad total de fuentes.

## Preguntas abiertas para siguiente refinamiento
- Que umbral comercial debe exigirse para considerar suficiente la cobertura MVP antes de ampliar a ayuntamientos.
- Que datos minimos deben gobernar una futura decision de monetizacion o plan de pago.

## Recomendacion operativa para `developer-teams`
- Completar la integracion administrativa de la issue tecnica `#14`, ya validada por `qa-teams`, y dejar evidencia de merge en `main` y borrado de rama antes de iniciar nueva implementacion funcional.
- A continuacion, tomar `PB-010` o `PB-013` segun el orden que mejor reduzca deuda de experiencia y de control de acceso.
- Mantener `PB-005` como siguiente pieza de negocio posterior a `PB-010` o coordinar su arranque cuando `PB-011` y `PB-012` ya hayan dejado visible la nueva base de dato consolidado.
- Mantener `PB-005` y `PB-008` por detras de `PB-012`, y reevaluar `PB-010` y `PB-013` como siguiente capa de experiencia y gobierno funcional.
- Crear las issues tecnicas separadas derivadas de los informes de `quality-auditor` y `security-auditor` del 2026-03-28 para que producto pueda priorizarlas de forma explicita.
- No tratar la issue tecnica `#14` como permiso automatico para abrir `PB-013` en paralelo: primero debe resolverse o bloquearse de forma explicita la implementacion activa actual y dejar constancia de integracion o bloqueo administrativo.
- Mantener visible en el catalogo la fuente oficial y evitar mensajes que sugieran cobertura total del ecosistema canario.
- Garantizar como minimo por oportunidad recopilada la visibilidad de origen oficial, enlace oficial, fecha de publicacion o equivalente y estado oficial cuando exista.
- Garantizar en detalle la visibilidad del fichero `.atom` origen de la version consolidada.
- Aplicar el filtrado solo sobre oportunidades ya visibles dentro de cobertura MVP y clasificacion final `TI`.
- Tratar los expedientes mixtos dudosos como caso frontera fuera del catalogo hasta que exista evidencia funcional suficiente.

## Trazabilidad operativa
- `PB-007` y `HU-07` quedan cubiertos por la issue #1 y su validacion ya registrada.
- `PB-006`, `HU-06` y `CU-08` resuelven la definicion de relevancia TI antes del catalogo.
- `PB-001`, `PB-002` y `PB-003` ya quedaron validados por `qa-teams` y cerrados administrativamente; Release 1 queda funcionalmente completa.
- `PB-009` ya quedo validado por `qa-teams` sobre la entrega integrada en `main` y queda cerrado administrativamente en la issue #9 para mantener sincronizados backlog e historial operativo.
- `PB-004` queda validado por `qa-teams`, integrado en `main` y cerrado administrativamente.
- `PB-011` queda validado por `qa-teams`, integrado en `main` y cerrado administrativamente.
- `PB-012` completa esa iteracion haciendo visible en aplicacion la salida alineada con el Excel y la trazabilidad al fichero origen.
- `PB-010` queda como iteracion de base de interfaz posterior a la consolidacion visible del dato.
- `PB-013` convierte en trabajo ejecutable la matriz de permisos definida en la especificacion consolidada sobre las superficies ya disponibles, dejando pipeline como extension posterior.
- `PB-005` queda como modulo posterior que debe apoyarse en esa base de navegacion comun.
- `PB-008` prepara la base de decision para evolucion posterior sin bloquear el MVP.
