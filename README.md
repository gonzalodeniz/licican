# PodencoTI

## Descripcion

`PodencoTI` es una plataforma para centralizar y detectar oportunidades de contratacion publica TI en Canarias. El proyecto busca evitar la busqueda manual en multiples portales oficiales, agregando licitaciones, clasificandolas como relevantes para tecnologia y permitiendo actuar con mas tiempo y mejor informacion.

## Objetivo

El objetivo del proyecto es ayudar a pymes, startups, consultoras, integradores y profesionales autonomos del sector tecnologico a descubrir antes las licitaciones publicas relevantes en Canarias, filtrarlas mejor y preparar ofertas con mayor antelacion.

Para ello, el producto persigue estas capacidades:

- rastreo automatizado de fuentes oficiales de contratacion en Canarias
- clasificacion inteligente de oportunidades TI
- filtros por palabras clave, presupuesto, procedimiento y ubicacion
- extraccion de datos criticos de cada licitacion
- alertas y seguimiento de oportunidades en un pipeline de trabajo

## Roles del repositorio

El repositorio trabaja con roles explicitamente activados mediante prompt:

- `product-manager`: define vision, backlog, historias, casos de uso e issues funcionales
- `developer-teams`: implementa los issues abiertos definidos por producto
- `qa-teams`: valida funcionalmente el trabajo entregado por desarrollo
- `doc-teams`: mantiene manuales de usuario, documentacion tecnica y documentacion de administracion
- `agile-coach`: analiza procesos, propone mejoras y puede actualizar `AGENTS.md` para mejorar la coordinacion

## Orden de ejecucion recomendado

Este proyecto lo está construyendo de manera autónoma una series de agentes con unos roles bien definidos. Cada agente trabaja en su área de especialización. Para que el flujo de trabajo sea efectivo, se recomienda seguir este orden de ejecución:

1. `product-manager`
   Define o actualiza vision, backlog, historias, casos de uso y issues ejecutables para desarrollo.
2. `developer-teams`
   Lee los issues abiertos, prioriza uno, crea su rama, implementa y deja contexto suficiente para validacion.
3. `qa-teams`
   Revisa la entrega en la rama del issue y deja un resultado explicito de `validado` o `no validado`.
4. `product-manager`
   Si `qa-teams` ha validado, cierra el issue y promueve el merge a `main`.
5. `doc-teams`
   Actualiza la documentacion de usuario, tecnica o de administracion cuando la funcionalidad ya este suficientemente estable o validada.
6. `agile-coach`
   Actua de forma transversal y preferiblemente al cierre de iteraciones, cuando haya suficiente informacion para analizar el flujo real y proponer mejoras de proceso.

## Uso recomendado de los scripts

Cada rol dispone de un script que carga `.env`, lee su prompt y ejecuta `codex exec`:

```bash
./1_rol-product-manager.sh
./2_rol-developer-teams.sh
./3_rol-qa-teams.sh
./4_rol-doc-teams.sh
./5_rol-agile-coach.sh
```

Tambien pueden recibir opciones adicionales de `codex exec`, por ejemplo:

```bash
./2_rol-developer-teams.sh --full-auto
```

## Reglas importantes

- Ningun rol se activa por contexto implicito; debe activarse de forma explicita en el prompt.
- `developer-teams` trabaja en un unico issue cada vez.
- `qa-teams` no cierra issues ni hace merge.
- `product-manager` no debe cerrar issues sin validacion explicita de `qa-teams`.
- `doc-teams` mantiene la documentacion del proyecto sin sustituir a otros equipos.
- `agile-coach` puede actualizar `AGENTS.md` para mejorar la coordinacion y los procesos, siempre con cambios justificados.

## Fuente de verdad

- Vision y artefactos funcionales: `product-manager/`
- Reglas globales y activacion de roles: `AGENTS.md`
- Documentacion de usuario, tecnica y administracion: `doc-teams/`
- Mejora continua y coordinacion de procesos: `agile-coach/`

## Entrega tecnica actual

La entrega tecnica vigente en `main` cubre dos piezas previas al catalogo del MVP:

- `PB-007`: cobertura inicial visible y verificable de fuentes del MVP.
- `PB-006`: regla de clasificacion TI auditable con ejemplos verificables.

### Como ejecutar la vista de cobertura

```bash
PYTHONPATH=src python3 -m podencoti.app
```

Luego se puede abrir:

- `http://127.0.0.1:8000/` para la vista HTML de cobertura
- `http://127.0.0.1:8000/api/fuentes` para la salida JSON trazable a la configuracion
- `http://127.0.0.1:8000/clasificacion-ti` para la vista HTML de clasificacion TI auditable
- `http://127.0.0.1:8000/api/clasificacion-ti` para la salida JSON de reglas y ejemplos auditados

## Capacidades aun no implementadas en `main`

Aunque formen parte de la vision y del backlog, todavia no existen en esta rama:

- catalogo de oportunidades TI
- ficha de detalle de licitacion
- filtros funcionales
- alertas tempranas
- pipeline de seguimiento

### Como ejecutar las pruebas tecnicas

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
