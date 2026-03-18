.PHONY: help run test

SHELL := /bin/bash
PYTHON ?= python3
PYTHONPATH := src
VENV_ACTIVATE := .venv/bin/activate

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
		"  make run   - Ejecuta la aplicacion local en http://127.0.0.1:8000" \
		"  make test  - Ejecuta la suite tecnica con unittest" \
		"Los objetivos activan .venv automaticamente si no hay un entorno virtual ya activo."

run:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m podencoti.app

test:
	@$(ENSURE_VENV); \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -v
