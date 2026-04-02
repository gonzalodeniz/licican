# Licican

## Descripcion

`Licican` es una plataforma para centralizar y detectar oportunidades de contratacion publica TI en Canarias. El proyecto busca evitar la busqueda manual en multiples portales oficiales, agregando licitaciones, clasificandolas como relevantes para tecnologia y permitiendo actuar con mas tiempo y mejor informacion.

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
- `quality-auditor`: audita calidad de codigo, cobertura de tests, deuda tecnica, documentacion tecnica y riesgos evidentes de eficiencia
- `security-auditor`: audita seguridad de codigo, secretos, dependencias, validacion de entradas y configuracion de hardening

## Orden de ejecucion recomendado

Este proyecto lo está construyendo de manera autónoma una series de agentes con unos roles bien definidos. Cada agente trabaja en su área de especialización. Para que el flujo de trabajo sea efectivo, se recomienda seguir este orden de ejecución:

1. `product-manager`
   Define o actualiza vision, backlog, historias, casos de uso y issues ejecutables para desarrollo.
2. `developer-teams`
   Lee los issues abiertos, prioriza uno, crea su rama, implementa y deja contexto suficiente para validacion.
3. `qa-teams`
   Revisa la entrega en la rama del issue y deja un resultado explicito de `validado` o `no validado`.
4. `developer-teams`
   Si `qa-teams` ha validado, fusiona la rama tecnica en `main` y la borra antes de iniciar trabajo nuevo, salvo bloqueo operativo documentado.
5. `product-manager`
   Tras la integracion validada, cierra el issue o deja constancia administrativa del motivo por el que sigue abierto.
6. `doc-teams`
   Actualiza la documentacion de usuario, tecnica o de administracion cuando la funcionalidad ya esta validada e integrada en `main`.
7. `quality-auditor`
   Ejecuta auditorias periodicas y entrega un informe estructurado a `product-manager` y `developer-teams`; desarrollo crea las issues tecnicas derivadas y producto las prioriza.
8. `security-auditor`
   Ejecuta auditorias periodicas de seguridad y entrega un informe estructurado a `product-manager` y `developer-teams`; desarrollo crea las issues tecnicas derivadas y producto las prioriza.
9. `agile-coach`
   Actua de forma transversal y preferiblemente al cierre de iteraciones, cuando haya suficiente informacion para analizar el flujo real y proponer mejoras de proceso.

## Uso recomendado de los scripts

Cada rol dispone de un script que carga `.env`, lee su prompt y ejecuta `codex exec`:

```bash
./1_rol-product-manager.sh
./2_rol-developer-teams.sh
./3_rol-qa-teams.sh
./4_rol-doc-teams.sh
./5_rol-agile-coach.sh
./6_rol-quality-auditor.sh
./7_rol-security-auditor.sh
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
- `quality-auditor` trabaja sobre `main`, entrega informes estructurados con severidad y evidencia, y registra sus acciones en `changelog/`.
- `security-auditor` trabaja sobre `main`, entrega informes estructurados con severidad y evidencia, y registra sus acciones en `changelog/`.

## Fuente de verdad

- Vision y artefactos funcionales: `product-manager/`
- Reglas globales y activacion de roles: `AGENTS.md`
- Acuerdos operativos compartidos, estados comunes y plantillas de handoff: `agile-coach/acuerdos-operativos.md`
- Formato vigente del changelog diario: `changelog/README.md`
- Documentacion de usuario, tecnica y administracion: `doc-teams/`
- Mejora continua y coordinacion de procesos: `agile-coach/`
- Auditoria de calidad de codigo y evidencias: `quality-auditor/`
- Auditoria de seguridad de codigo y evidencias: `security-auditor/`

## Entrega tecnica actual

La rama `main` ya integra ocho piezas funcionales y operativas verificables del MVP inicial:

- `PB-007`: cobertura inicial visible y verificable de fuentes del MVP.
- `PB-006`: regla de clasificacion TI auditable con ejemplos verificables.
- `PB-001`: catalogo inicial de oportunidades TI consultable desde una app WSGI minima en Python.
- `PB-002`: ficha de detalle navegable desde el catalogo, con tratamiento explicito de campos no informados y aplicacion del ultimo dato oficial visible cuando el expediente publica una rectificacion o modificacion.
- `PB-003`: filtros funcionales sobre el catalogo y su API por palabra clave, rango de presupuesto, procedimiento y ubicacion, incluyendo validacion explicita de rangos invalidos.
- `PB-004`: gestion de alertas tempranas con alta, edicion y desactivacion, reutilizando los filtros del catalogo y registrando coincidencias internas accionables.
- `PB-009`: priorizacion visible de fuentes reales oficiales por olas (`BOC`, `BOP Las Palmas`, `BOE`) y refuerzo de la trazabilidad minima al origen oficial en cada oportunidad publicada.
- Despliegue local en contenedor Docker con `Dockerfile`, `docker-compose.yml` y persistencia de `data/`.

### Como ejecutar las vistas actuales

Si no existe `.env`, copia `.env.example` y ajusta al menos `PORT` antes de arrancar.

El arranque local usa el puerto definido en `.env` mediante `PORT`. Si no se define, la aplicacion cae al valor por defecto `8000`.
El servidor local escucha en `HOST`, con `127.0.0.1` por defecto. Si necesitas exponerlo fuera de la maquina local, usa `HOST=0.0.0.0`.
La carga del catalogo y del detalle usa PostgreSQL por defecto. Si necesitas forzar temporalmente la fuente historica basada en ficheros para pruebas locales, exporta `LICICAN_CATALOG_BACKEND=file`.

Configuracion local por defecto del backend PostgreSQL:

- `DB_HOST=localhost`
- `DB_PORT=15432`
- `DB_NAME=licitaciones`
- `DB_USER=licitaciones_admin`
- `DB_PASSWORD=Lic1t4c10n3s_2026!`

```bash
PYTHONPATH=src python3 -m licican.app
```

Luego se puede abrir:

- `http://127.0.0.1:<PORT>/` para la vista HTML del catalogo inicial de oportunidades TI, con formulario de filtros funcionales
- `http://127.0.0.1:<PORT>/api/oportunidades` para la salida JSON del catalogo filtrado por cobertura MVP y clasificacion TI
- `http://127.0.0.1:<PORT>/oportunidades/<id>` para la ficha HTML de detalle de una oportunidad visible
- `http://127.0.0.1:<PORT>/api/oportunidades/<id>` para la salida JSON trazable de la ficha de detalle
- `http://127.0.0.1:<PORT>/alertas` para la gestion HTML de alertas tempranas del MVP
- `http://127.0.0.1:<PORT>/api/alertas` para la salida JSON de alertas persistidas y sus coincidencias internas
- `http://127.0.0.1:<PORT>/cobertura-fuentes` para la vista HTML de cobertura MVP
- `http://127.0.0.1:<PORT>/api/fuentes` para la salida JSON trazable a la configuracion
- `http://127.0.0.1:<PORT>/priorizacion-fuentes-reales` para la vista HTML de priorizacion de fuentes reales oficiales por olas
- `http://127.0.0.1:<PORT>/api/fuentes-prioritarias` para la salida JSON de la priorizacion de fuentes reales oficiales
- `http://127.0.0.1:<PORT>/clasificacion-ti` para la vista HTML de la regla TI auditable
- `http://127.0.0.1:<PORT>/api/clasificacion-ti` para la salida JSON de reglas y ejemplos auditados

Ejemplos de filtros ya soportados:

- `http://127.0.0.1:<PORT>/?palabra_clave=licencias`
- `http://127.0.0.1:<PORT>/api/oportunidades?procedimiento=Abierto`
- `http://127.0.0.1:<PORT>/api/oportunidades?presupuesto_min=90000&presupuesto_max=120000`

### Despliegue con Docker

El `docker-compose.yml` raiz levanta la aplicacion y la base de datos PostgreSQL integrada.

- `licican` publica el puerto definido por `PORT` y monta `./data:/app/data` para persistencia.
- `licican` arranca con `LICICAN_CATALOG_BACKEND=postgres` y conecta con `postgres-licitaciones` usando la configuracion `DB_*` del compose.
- `postgres-licitaciones` publica la base de datos en `DB_PORT` y persiste los datos en `pgdata_licitaciones`.
- La aplicacion en contenedor escucha con `HOST=0.0.0.0`, mientras que en local mantiene `127.0.0.1`.

1. Revisa `.env` y ajusta `PORT` o `DB_PORT` si necesitas puertos distintos.
2. Levanta la pila completa con `docker compose up -d --build`.
3. Usa `make docker-psql` para abrir una terminal `psql` sobre la BBDD integrada.

Objetivos de `Makefile` disponibles:

```bash
make docker-build
make docker-up
make docker-down
make docker-logs
make docker-restart
make docker-psql
```

## Capacidades aun no implementadas en esta rama

Aunque formen parte de la vision y del backlog, todavia no existen en esta rama:

- pipeline de seguimiento

### Como ejecutar las pruebas tecnicas

```bash
PYTHONPATH=src python3 -m pytest -v
```
