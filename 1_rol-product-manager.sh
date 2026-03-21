#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="${SCRIPT_DIR}/product-manager/prompt-product-manager.md"
RUN_CODEX="${SCRIPT_DIR}/run-codex.sh"

if [ ! -f "${PROMPT_FILE}" ]; then
  echo "No existe ${PROMPT_FILE}"
  exit 1
fi

if [ ! -x "${RUN_CODEX}" ]; then
  chmod +x "${RUN_CODEX}"
fi

PROMPT_CONTENT="$(cat "${PROMPT_FILE}")"

exec "${RUN_CODEX}" exec -m "gpt-5.4" -C "${SCRIPT_DIR}" "${PROMPT_CONTENT}" "$@"
