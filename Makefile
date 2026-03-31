.DEFAULT_GOAL := help

.PHONY: help run test coverage docker-build docker-up docker-down docker-logs docker-restart docker-psql

SHELL := /bin/bash
PYTHON ?= python3
PYTHONPATH := src
VENV_ACTIVATE := .venv/bin/activate
DOCKER ?= docker
COMPOSE ?= docker compose
IMAGE_NAME ?= licican:latest

define ENSURE_VENV
	if [[ -n "$$VIRTUAL_ENV" && -x "$$VIRTUAL_ENV/bin/python3" ]]; then \
		:; \
	elif [[ -f "$(VENV_ACTIVATE)" ]]; then \
		source "$(VENV_ACTIVATE)"; \
	else \
		echo "No se encontro $(VENV_ACTIVATE)"; \
		exit 1; \
	fi
endef

run:
	@$(ENSURE_VENV); \
	requested_port="$${PORT:-8000}"; \
	resolved_port=""; \
	for candidate_port in $$(seq "$$requested_port" 8100); do \
		if ! ( : < /dev/tcp/127.0.0.1/$$candidate_port ) 2>/dev/null; then \
			resolved_port="$$candidate_port"; \
			break; \
		fi; \
	done; \
	if [[ -z "$$resolved_port" ]]; then \
		echo "No se encontraron puertos libres entre $$requested_port y 8100"; \
		exit 1; \
	fi; \
	if [[ "$$resolved_port" != "$$requested_port" ]]; then \
		echo "Puerto $$requested_port ocupado, usando $$resolved_port"; \
	fi; \
	BASE_PATH=/licican PORT="$$resolved_port" PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m licican.app

test:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest -v

coverage:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m coverage run --source=src -m pytest -v && \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m coverage report -m

help:
	@printf "%s\n" \
		"Objetivos disponibles:" \
		"  make run   - Ejecuta la aplicacion local usando PORT o el siguiente puerto libre" \
		"  make test  - Ejecuta la suite tecnica con pytest" \
		"  make coverage - Ejecuta la suite y muestra el informe de cobertura" \
		"  make docker-build  - Construye la imagen Docker minima" \
		"  make docker-up     - Levanta el despliegue con docker compose" \
		"  make docker-down   - Detiene el despliegue con docker compose" \
		"  make docker-logs   - Muestra los logs del contenedor" \
		"  make docker-restart - Recrea el despliegue Docker" \
		"  make docker-psql   - Abre una terminal psql en la base de datos" \
		"Los objetivos activan .venv automaticamente si no hay un entorno virtual ya activo."

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
