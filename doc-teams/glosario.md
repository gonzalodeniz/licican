# Glosario

## Publico objetivo
Usuario interno del proyecto que necesita interpretar de forma consistente la terminologia funcional, tecnica y operativa de `Licican`.

## Terminos del producto
- `Licican`: plataforma orientada a centralizar y detectar oportunidades de contratacion publica TI en Canarias.
- `MVP`: alcance minimo inicial del producto; segun la documentacion funcional vigente, debe comunicarse como cobertura inicial priorizada y no como cobertura total.
- `Oportunidad TI`: licitacion o expediente considerado relevante para tecnologia conforme a las reglas funcionales vigentes de clasificacion.
- `Cobertura funcional`: conjunto de fuentes y capacidades que el producto declara cubrir de forma observable y verificable.
- `Fuente oficial`: portal, perfil del contratante u origen institucional desde el que se obtiene informacion de contratacion publica.
- `Clasificacion TI auditable`: superficie visible que expone reglas, exclusiones, casos frontera y ejemplos verificables antes del catalogo.
- `Filtro funcional`: criterio aplicable sobre el catalogo visible y su API para reducir resultados por palabra clave, presupuesto, procedimiento o ubicacion.
- `Snapshot .atom`: fichero Atom utilizado por `PB-011`; esta definicion aplica a muestras temporales o externas, porque el repositorio actual no versiona snapshots `.atom` en `data/`.
- `Gestion de usuarios`: modulo administrativo disponible en `main` para listar, filtrar, crear, editar y cambiar de estado cuentas de usuario, con detalle y trazabilidad basica en `data/users.json`.
- `Pipeline`: seguimiento del estado de trabajo de una oportunidad por parte del usuario; sigue siendo capacidad planificada y no esta disponible en `main` revisado, aunque el changelog de `2026-03-31` la menciona como validada.
- `Alerta temprana`: capacidad disponible en `main` para crear, editar y desactivar alertas internas reutilizando los filtros del catalogo y registrando coincidencias accionables; no incluye notificaciones salientes.

## Terminos operativos del repositorio
- `main`: rama de referencia para trabajo funcional, documental y de coordinacion no tecnica.
- `Estado operativo`: etiqueta comun entre equipos para una issue (`nuevo`, `en desarrollo`, `listo para qa`, `no validado`, `validado`, `cerrado`).
- `Impacto documental`: indicador usado por `developer-teams` para señalar que una entrega validada requiere actualizacion documental.
- `Trazabilidad`: relacion explicita entre vision, backlog, historias, casos de uso, implementacion, validacion y documentacion.

## Terminos de esta revision documental
- `Estado real observable`: comportamiento que puede comprobarse en la rama revisada mediante ficheros versionados y comandos reproducibles.
- `Contradiccion documental`: diferencia entre lo que una fuente del repositorio afirma y lo que puede verificarse realmente en `main`.
- `No disponible en main`: capacidad descrita por vision o backlog que no debe documentarse como funcionalidad utilizable hoy.
- `Entrega minima ejecutable`: estado actual de `main` con servidor local, catalogo servido por PostgreSQL por defecto, respaldo `file` sobre `data/opportunities.json` cuando no hay Atom versionado, filtros funcionales, ficha de detalle con fichero origen cuando exista, alertas internas, gestion administrativa de usuarios, rutas de cobertura, rutas de priorizacion de fuentes reales y rutas de clasificacion TI auditables, ademas de un despliegue local en contenedor, pero sin pipeline ni despliegue productivo endurecido.
- `Trabajo validado no integrado`: entrega que puede aparecer en `changelog/` o en una issue como validada por `qa-teams`, pero que aun no forma parte del comportamiento observable de `main` hasta su integracion efectiva; esta expresion ya no aplica a `PB-009` ni a `PB-011`, que ya forman parte de `main`, y vuelve a ser util para leer `PB-012` o `pipeline` mientras el changelog las cite como validadas sin que el codigo visible las exponga.

## Contradicciones clave asociadas al glosario
- `Catalogo validado`: expresion historica que hoy si coincide con las rutas y modulos presentes en `main`, porque el catalogo consolidado, la ficha de detalle, las alertas internas y la priorizacion de fuentes reales ya forman parte de la rama principal.
- `Validado`: estado que puede referirse a una rama tecnica concreta y no necesariamente a funcionalidad ya integrada en `main`; debe interpretarse junto con la rama y la evidencia observable.
