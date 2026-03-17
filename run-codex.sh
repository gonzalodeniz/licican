#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "No existe .env en el directorio actual"
  exit 1
fi

set -a
source .env
set +a

if [ -z "${GITHUB_PAT:-}" ]; then
  echo "GITHUB_PAT no está definido tras cargar .env"
  exit 1
fi

exec codex