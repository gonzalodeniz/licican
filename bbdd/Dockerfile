FROM postgres:16-bookworm

LABEL maintainer="Gonzalo - Licitaciones BBDD"
LABEL description="PostgreSQL 16 con locale es_ES.UTF-8 para licitaciones del Sector Público"

# Instalar locale español
RUN apt-get update \
    && apt-get install -y --no-install-recommends locales \
    && sed -i '/es_ES.UTF-8/s/^# //' /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=es_ES.UTF-8
ENV LC_ALL=es_ES.UTF-8

# Copiar scripts de inicialización
# PostgreSQL ejecuta automáticamente los .sql y .sh de /docker-entrypoint-initdb.d/
# en orden alfabético la primera vez que arranca el contenedor
COPY initdb/ /docker-entrypoint-initdb.d/

EXPOSE 5432
