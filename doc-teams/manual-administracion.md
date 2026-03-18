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
- `make test` ejecuta 15 pruebas y termina en verde.
- `make run` publica el mensaje `Servidor disponible en http://127.0.0.1:8000`.
- Mientras el proceso esta levantado, las rutas `/`, `/api/fuentes`, `/clasificacion-ti` y `/api/clasificacion-ti` responden `200 OK`.

## Verificaciones operativas minimas
- Abrir `http://127.0.0.1:8000/` para revisar la cobertura inicial del MVP.
- Abrir `http://127.0.0.1:8000/clasificacion-ti` para revisar la regla TI auditable.
- Consultar las salidas JSON para integracion basica o soporte QA:
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

## Riesgos operativos
- Las superficies actuales son utiles para validacion temprana, pero no para explotacion operativa continua.
- Comunicar que el producto ya ofrece catalogo, filtros o pipeline induciria a error.
- El changelog contiene entradas contradictorias; para soporte operativo debe prevalecer el codigo y las verificaciones reproducibles de esta rama.

## Dependencias abiertas para administracion
- Definir estrategia de despliegue productivo cuando exista una aplicacion mas alla del servidor local de demostracion.
- Incorporar mecanismos de configuracion, supervision y observabilidad cuando el alcance operativo lo requiera.
