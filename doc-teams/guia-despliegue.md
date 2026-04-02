# Guia de despliegue

## Publico objetivo
Persona responsable de publicar o exponer `Licican` fuera de un entorno local de desarrollo.

## Estado actual del despliegue
La rama `main` contiene una aplicacion arrancable en local con PostgreSQL como backend operativo por defecto, modo `file` disponible para pruebas aisladas, gestion administrativa de usuarios persistida en JSON y una ruta reproducible de contenedor con `Dockerfile` y `docker-compose.yml` que levanta la aplicacion y la BBDD PostgreSQL integrada. Esto cubre despliegue local reproducible, pero no implica aun una publicacion productiva endurecida.

## Verificacion previa obligatoria
Antes de plantear cualquier publicacion, confirma desde la raiz del proyecto:

```bash
cd /opt/apps/licican
source .venv/bin/activate
python3 -m pip install -e .
make test
timeout 2s make run
docker compose up -d --build
```

Si no existe `.env`, copia antes `.env.example` a `.env` y define `PORT`. En contenedor, la app usa `HOST=0.0.0.0` para aceptar conexiones externas al puerto publicado.

## Resultado esperado en esta revision
- `python3 -m pip install -e .` termina correctamente.
- `make test` ejecuta 131 pruebas en verde con `pytest`.
- `make run` arranca el servidor local usando `PORT` desde `.env` y, si el puerto esta ocupado, avanza al siguiente libre.
- `docker compose up -d --build` publica la misma aplicacion en un contenedor, levanta la BBDD integrada y monta `data/` como volumen persistente.
- En la superficie desplegada responden tambien `/alertas` y `/api/alertas`, que almacenan alertas internas sin notificaciones salientes.
- En la superficie desplegada responden tambien `/usuarios` y `/api/usuarios`, que gestionan cuentas de usuario con almacenamiento versionado en `data/users.json`.
- El detalle de oportunidad muestra el origen funcional vigente y, en modo `file`, el respaldo `data/opportunities.json` cuando no hay snapshots Atom versionados.

## Conclusion operativa
Solo debe considerarse soportado el arranque local de validacion y el despliegue local en contenedor con Compose. No hay base documental suficiente para prometer despliegue en servidor, orquestador o plataforma gestionada.

## Elementos de despliegue no disponibles
- servidor WSGI de produccion endurecido
- fichero de configuracion de entorno versionado para produccion
- servicio `systemd`
- proxy inverso documentado
- healthcheck dedicado
- procedimiento de rollback

## Dependencias abiertas para habilitar despliegue real
- Definir la topologia de publicacion objetivo.
- Externalizar configuracion si aparecen credenciales o integraciones adicionales.
- Incorporar operativa de proceso, observabilidad y recuperacion.
- Revisar de nuevo esta guia cuando el alcance supere la demo local actual.
- Si se quiere pasar de contenedor local a produccion, endurecer la imagen, definir usuario/volumenes finales y documentar supervision, observabilidad y rollback.
- La priorizacion de fuentes reales ya puede desplegarse junto con el resto de la entrega minima, pero sigue siendo una funcionalidad de recopilacion, no una capa operativa completa.
- Las alertas visibles son internas y no sustituyen una capa de notificacion o automatizacion de seguimiento.
- La gestion de usuarios disponible en `main` no incluye autenticacion real, SSO ni MFA; el control sigue siendo por rol simulado y por la semilla JSON versionada.
- La entrega documentada aqui usa PostgreSQL por defecto; `LICICAN_CATALOG_BACKEND=file` y `data/opportunities.json` quedan como respaldo operativo cuando se fuerza ese modo.
- La consolidacion Atom sigue sujeta a la disponibilidad de snapshots `.atom`; si no hay ficheros Atom en `data/`, la ruta `file` usa el respaldo JSON.

## Riesgos
- Documentar hoy un despliegue real seria inventar decisiones tecnicas no presentes en el repositorio.
- Comunicar la entrega actual como lista para produccion desalinearia a documentacion, QA y producto.
