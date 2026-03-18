# Guia de despliegue

## Publico objetivo
Persona responsable de publicar o exponer `PodencoTI` fuera de un entorno local de desarrollo.

## Estado actual del despliegue
La rama `main` si contiene una aplicacion arrancable, pero solo existe un mecanismo de ejecucion local con `wsgiref.simple_server`. No hay artefactos suficientes para documentar un despliegue productivo reproducible sin caer en especulacion.

## Verificacion previa obligatoria
Antes de plantear cualquier publicacion, confirma desde la raiz del proyecto:

```bash
cd /opt/apps/podencoti
source .venv/bin/activate
python3 -m pip install -e .
make test
timeout 2s make run
```

## Resultado esperado en esta revision
- `python3 -m pip install -e .` termina correctamente.
- `make test` ejecuta 15 pruebas en verde.
- `make run` arranca el servidor local y queda a la escucha hasta que se interrumpe el proceso.

## Conclusion operativa
Solo debe considerarse soportado el arranque local de validacion. No hay base documental suficiente para prometer despliegue en servidor, contenedor o plataforma gestionada.

## Elementos de despliegue no disponibles
- servidor WSGI de produccion
- fichero de configuracion de entorno
- servicio `systemd`
- definicion de contenedor
- proxy inverso documentado
- healthcheck dedicado
- procedimiento de rollback

## Dependencias abiertas para habilitar despliegue real
- Definir la topologia de publicacion objetivo.
- Externalizar configuracion si aparecen puertos, credenciales o integraciones.
- Incorporar operativa de proceso, observabilidad y recuperacion.
- Revisar de nuevo esta guia cuando el alcance supere la demo local actual.

## Riesgos
- Documentar hoy un despliegue real seria inventar decisiones tecnicas no presentes en el repositorio.
- Comunicar la entrega actual como lista para produccion desalinearia a documentacion, QA y producto.
