#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

if [ ! -f "${ENV_FILE}" ]; then
  echo "No existe .env en el directorio actual"
  exit 1
fi

set -a
source "${ENV_FILE}"
set +a

if [ -z "${GITHUB_PAT:-}" ]; then
  echo "GITHUB_PAT no está definido tras cargar .env"
  exit 1
fi

exec codex --dangerously-bypass-approvals-and-sandbox "$@"
