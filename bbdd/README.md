# Base de Datos de Licican

Este directorio contiene el contrato de esquema y utilidades de inicializacion de la base de datos.

## Esquema base

El fichero `initdb/01-schema.sql` define la estructura inicial de PostgreSQL para una instalación limpia.

## Seed opcional del superadmin

Para entornos de desarrollo puede ejecutarse manualmente el seed del superadmin sin depender del primer login:

```bash
PYTHONPATH=src python3 bbdd/seed_superadmin.py
```

El script usa la configuración del `.env`:

- si `LOGIN_SUPERADMIN_ENABLED=true` o `LOGIN_AUTOMATICO=true`, crea o reactiva el superadmin y actualiza su contraseña
- si `LOGIN_SUPERADMIN_ENABLED=false`, desactiva el superadmin existente

Este seed no forma parte del `initdb` automático para no mezclar el contrato base con una acción operativa opcional.
