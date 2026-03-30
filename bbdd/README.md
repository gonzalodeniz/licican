# Licitaciones del Sector Público - Base de Datos

Sistema para almacenar licitaciones de la [Plataforma de Contratación del Sector Público](https://contrataciondelestado.es) en PostgreSQL, a partir de los feeds ATOM.

**Solo se importan licitaciones que cumplan AMBOS filtros:**
- **Geográfico**: Canarias (código NUTS `ES7*`, o "Canarias" en la jerarquía `ParentLocatedParty` o `CountrySubentity`).
- **Tipo de contrato informático**: Al menos un CPV que empiece por `72` (Servicios TI), `48` (Software) o `302` (Equipos informáticos), buscando tanto en el proyecto principal como en todos los lotes.

## Estructura del proyecto

```
licitaciones-db/
├── Dockerfile                  # Imagen PostgreSQL 16 con locale es_ES
├── docker-compose-bbdd.yml     # Compose para levantar la BBDD
├── .env.example                # Variables de entorno (copiar a .env)
├── initdb/
│   └── 01-schema.sql           # DDL: base de datos, tabla e índices
├── importar_licitaciones.py    # Script de importación de ficheros ATOM
├── requirements.txt            # Dependencias Python
└── README.md
```

## 1. Levantar la base de datos

```bash
# Copiar y ajustar variables de entorno
cp .env.example .env

# Construir y arrancar
docker compose -f docker-compose-bbdd.yml up -d --build

# Verificar que está sano
docker compose -f docker-compose-bbdd.yml ps
```

Desde la raiz del proyecto, la pila completa ya integra esta BBDD en `docker-compose.yml`:

```bash
cd /opt/apps/podencoti
docker compose up -d --build
make docker-psql
```

Al arrancar por primera vez, el contenedor ejecuta automáticamente `initdb/01-schema.sql`, que crea la base de datos `licitaciones` y la tabla con todos sus índices.

Los datos se persisten en el volumen Docker `pgdata_licitaciones`.

## 2. Importar ficheros ATOM

```bash
# Instalar dependencias
pip install -r requirements.txt

# Importar: apuntar al directorio que contiene los .atom
# El script lee automáticamente la cadena de ficheros
python3 importar_licitaciones.py /ruta/a/los/atom/

# Forzar reprocesamiento completo de toda la cadena
python3 importar_licitaciones.py --force /ruta/a/los/atom/
```

### Flujo de lectura (cadena `rel="next"`)

El script no procesa los ficheros en orden alfabético ni de forma arbitraria. Sigue la cadena definida dentro de los propios ficheros ATOM:

1. **Siempre** lee `licitacionesPerfilesContratanteCompleto3.atom` (el fichero principal, que contiene las licitaciones más recientes). Este fichero nunca se registra como procesado.
2. Dentro del fichero, lee el `<link rel="next">` para saber cuál es el siguiente.
3. Si ese siguiente fichero **ya está** en la tabla `fichero_procesado`, **se detiene** (los ficheros más antiguos de la cadena no han cambiado).
4. Si **no está**, lo procesa, lo registra, y continúa al siguiente `rel="next"`.

Esto significa que en una descarga típica con 314 ficheros donde solo los primeros 7 son nuevos, el script procesa exactamente esos 7 y para.

### Control de ficheros procesados

```sql
-- Ver ficheros procesados
SELECT nombre_fichero, fecha_procesado, entries_filtradas, entries_insertadas
FROM fichero_procesado
ORDER BY fecha_procesado DESC;

-- Limpiar historial para reprocesar toda la cadena
TRUNCATE fichero_procesado;
```

### Lógica de importación

| Situación | Acción |
|---|---|
| Licitación **no es de Canarias** o **no tiene CPV informático** | Se **descarta** (no se importa) |
| Licitación **pasa filtros** y **no existe** en BBDD | Se **inserta** |
| Licitación **pasa filtros**, **existe** y fichero es **más reciente** | Se **actualiza** |
| Licitación **pasa filtros**, **existe** y fichero es **más antiguo o igual** | **No se modifica** |
| Entry de tipo `deleted-entry` | Se **marca como anulada** (solo si ya está en BBDD) |

La clave primaria es `id_plataforma` (la URL de sindicación del entry ATOM).

## 3. Conexión directa

```bash
# Desde el host
psql -h localhost -p 15432 -U licitaciones_admin -d licitaciones

# Desde otro contenedor en la misma red
psql -h postgres-licitaciones -U licitaciones_admin -d licitaciones
```

### Consultas de ejemplo

```sql
-- Licitaciones abiertas (en evaluación)
SELECT expediente, titulo, importe_total, estado, cpv_codes
FROM licitacion
WHERE estado = 'EV'
ORDER BY updated_at DESC;

-- Búsqueda por texto en título
SELECT expediente, titulo, organo_contratacion
FROM licitacion
WHERE to_tsvector('spanish', titulo) @@ plainto_tsquery('spanish', 'servicios informáticos');

-- Licitaciones de servicios TI (CPV 72*)
SELECT expediente, titulo, importe_total
FROM licitacion
WHERE EXISTS (SELECT 1 FROM unnest(cpv_codes) AS c WHERE c LIKE '72%')
ORDER BY updated_at DESC;

-- Licitaciones adjudicadas con adjudicatario
SELECT expediente, titulo, adjudicatario_nombre, contrato_importe_total
FROM licitacion
WHERE resultado_codigo IS NOT NULL
  AND adjudicatario_nombre IS NOT NULL
ORDER BY fecha_adjudicacion DESC
LIMIT 20;
```

## Variables de entorno

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `POSTGRES_PASSWORD` | `Lic1t4c10n3s_2026!` | Contraseña del usuario admin |
| `POSTGRES_PORT` | `5432` | Puerto externo para el compose standalone |
| `DB_HOST` | `localhost` | Host de la BBDD (para el importador) |
| `DB_PORT` | `15432` | Puerto de la BBDD integrado en el compose raiz |
| `DB_NAME` | `licitaciones` | Nombre de la BBDD |
| `DB_USER` | `licitaciones_admin` | Usuario de la BBDD |
| `DB_PASSWORD` | `Lic1t4c10n3s_2026!` | Contraseña (para el importador) |
