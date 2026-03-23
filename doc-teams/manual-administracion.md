# Manual de administracion y operacion

## Publico objetivo
Persona responsable de preparar el entorno local, arrancar la entrega minima actual y verificar que las superficies visibles responden como se espera.

## Alcance operativo actual
En `main` existe un servicio HTTP local arrancable con `wsgiref.simple_server`. Su alcance operativo es de validacion local y demostracion funcional temprana; no equivale a una operacion productiva completa.

## Prerequisitos
- Acceso al arbol del proyecto en `/opt/apps/podencoti`.
- `python3` compatible con `>=3.12`.
- Entorno virtual activo o directorio `.venv/` disponible si se va a usar `make`.
- `make` para usar los objetivos definidos en `Makefile`.

## Arranque local reproducible
Desde la raiz del proyecto:

```bash
cd /opt/apps/podencoti
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
make test
make run
```

## Resultado esperado en esta revision
- `make test` ejecuta 33 pruebas y termina en verde.
- `make run` publica el mensaje `Servidor disponible en http://127.0.0.1:8000`.
- Mientras el proceso esta levantado, las rutas `/`, `/api/oportunidades`, `/oportunidades/pcsp-cabildo-licencias-2026`, `/api/oportunidades/pcsp-cabildo-licencias-2026`, `/cobertura-fuentes`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti` responden `200 OK`.

## Verificaciones operativas minimas
- Abrir `http://127.0.0.1:8000/` para revisar el catalogo inicial de oportunidades TI.
- Abrir `http://127.0.0.1:8000/?palabra_clave=licencias` para verificar filtrado funcional en HTML.
- Consultar `http://127.0.0.1:8000/api/oportunidades?procedimiento=Abierto` para verificar filtrado funcional en API.
- Consultar `http://127.0.0.1:8000/api/oportunidades?presupuesto_min=120000&presupuesto_max=90000` para verificar que la API devuelve `400` con validacion explicita de rango.
- Abrir `http://127.0.0.1:8000/oportunidades/pcsp-cabildo-licencias-2026` para revisar una ficha de detalle con rectificacion visible.
- Abrir `http://127.0.0.1:8000/cobertura-fuentes` para revisar la cobertura inicial del MVP.
- Abrir `http://127.0.0.1:8000/clasificacion-ti` para revisar la regla TI auditable.
- Consultar las salidas JSON para integracion basica o soporte QA:
  - `http://127.0.0.1:8000/api/oportunidades`
  - `http://127.0.0.1:8000/api/oportunidades/pcsp-cabildo-licencias-2026`
  - `http://127.0.0.1:8000/api/fuentes`
  - `http://127.0.0.1:8000/api/clasificacion-ti`

## Parada controlada
- Interrumpe el proceso con `Ctrl+C`.
- La aplicacion imprime `Servidor detenido de forma controlada.`.

## Operacion no disponible
No existe en `main`:
- servicio gestionado con `systemd`
- contenedor o `Dockerfile`
- proxy inverso documentado
- observabilidad o healthcheck dedicado
- procedimiento de backup o rollback
- despliegue productivo validado
- superficies operativas de priorizacion de fuentes reales (`/priorizacion-fuentes-reales` y `/api/fuentes-prioritarias`)

## Riesgos operativos
- Las superficies actuales son utiles para validacion temprana, pero no para explotacion operativa continua.
- Comunicar que el producto ya ofrece alertas o pipeline induciria a error.
- `pyproject.toml` sigue describiendo una superficie mas estrecha que la observable hoy; para soporte operativo debe prevalecer el codigo, las rutas verificadas y esta documentacion.
- La priorizacion funcional de nuevas fuentes reales oficiales ya existe en `product-manager/`, pero no debe confundirse con una ingestión ya disponible en la operacion actual.
- Aunque un changelog reciente pueda describir `PB-009` como validado, la operacion revisada en `main` no expone todavia superficies funcionales para esa priorizacion.

## Dependencias abiertas para administracion
- Definir estrategia de despliegue productivo cuando exista una aplicacion mas alla del servidor local de demostracion.
- Incorporar mecanismos de configuracion, supervision y observabilidad cuando el alcance operativo lo requiera.
