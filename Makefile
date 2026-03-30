.PHONY: help run test docker-build docker-up docker-down docker-logs docker-restart docker-psql

SHELL := /bin/bash
PYTHON ?= python3
PYTHONPATH := src
VENV_ACTIVATE := .venv/bin/activate
DOCKER ?= docker
COMPOSE ?= docker compose
IMAGE_NAME ?= podencoti:latest

define ENSURE_VENV
	if [[ -z "$$VIRTUAL_ENV" ]]; then \
		if [[ -f "$(VENV_ACTIVATE)" ]]; then \
			source "$(VENV_ACTIVATE)"; \
		else \
			echo "No se encontro $(VENV_ACTIVATE)"; \
			exit 1; \
		fi; \
	fi
endef

help:
	@printf "%s\n" \
		"Objetivos disponibles:" \
		"  make run   - Ejecuta la aplicacion local usando PORT desde .env" \
		"  make test  - Ejecuta la suite tecnica con unittest" \
		"  make docker-build  - Construye la imagen Docker minima" \
		"  make docker-up     - Levanta el despliegue con docker compose" \
		"  make docker-down   - Detiene el despliegue con docker compose" \
		"  make docker-logs   - Muestra los logs del contenedor" \
		"  make docker-restart - Recrea el despliegue Docker" \
		"  make docker-psql   - Abre una terminal psql en la base de datos" \
		"Los objetivos activan .venv automaticamente si no hay un entorno virtual ya activo."

run:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m podencoti.app

test:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -v

docker-build:
	@$(DOCKER) build -t $(IMAGE_NAME) .

docker-up:
	@$(COMPOSE) up -d --build

docker-down:
	@$(COMPOSE) down

docker-logs:
	@$(COMPOSE) logs -f

docker-restart:
	@$(COMPOSE) down && $(COMPOSE) up -d --build

docker-psql:
	@set -a; \
	if [[ -f .env ]]; then source .env; fi; \
	set +a; \
	$(COMPOSE) up -d postgres-licitaciones >/dev/null && \
	$(COMPOSE) exec -it postgres-licitaciones psql -U "$${DB_USER:-licitaciones_admin}" -d "$${DB_NAME:-licitaciones}"
