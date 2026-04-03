#!/usr/bin/env python3
"""Seed manual del superadmin para entornos de desarrollo.

Este script sincroniza el usuario superadmin con la configuracion de
entorno sin depender del primer login de la aplicacion.

Comportamiento:
- Si `LOGIN_SUPERADMIN_ENABLED=true` o `LOGIN_AUTOMATICO=true`, crea o
  reactiva el superadmin y actualiza su `password_hash` con la contraseña
  actual del `.env`.
- Si `LOGIN_SUPERADMIN_ENABLED=false`, desactiva el superadmin existente.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from licican.auth.config import get_auth_settings  # noqa: E402
from licican.auth.service import synchronize_superadmin_account  # noqa: E402
from licican.config import load_env_file  # noqa: E402


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
LOGGER = logging.getLogger("seed-superadmin")


def main() -> None:
    """Ejecuta la sincronizacion manual del superadmin."""
    load_env_file(ROOT_DIR / ".env")
    settings = get_auth_settings()
    synchronize_superadmin_account(settings)
    LOGGER.info("Superadmin sincronizado correctamente.")


if __name__ == "__main__":
    main()
