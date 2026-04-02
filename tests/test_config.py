from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import licican.config as config


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self._previous_loaded = config._ENV_LOADED
        config._ENV_LOADED = False

    def tearDown(self) -> None:
        config._ENV_LOADED = self._previous_loaded

    def test_normalize_base_path_normalizes_empty_and_prefixed_values(self) -> None:
        self.assertEqual("", config.normalize_base_path(None))
        self.assertEqual("", config.normalize_base_path("/"))
        self.assertEqual("/licican", config.normalize_base_path("licican/"))

    def test_load_env_file_only_loads_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("BASE_PATH=/primero\nHOST=0.0.0.0\n", encoding="utf-8")

            with patch.dict(os.environ, {}, clear=True):
                config.load_env_file(env_path)
                env_path.write_text("BASE_PATH=/segundo\nHOST=127.0.0.1\n", encoding="utf-8")
                config.load_env_file(env_path)

                self.assertEqual("/primero", os.environ["BASE_PATH"])
                self.assertEqual("0.0.0.0", os.environ["HOST"])

    def test_resolve_functions_use_loaded_environment_values(self) -> None:
        with patch.dict(
            os.environ,
            {
                "BASE_PATH": "licican",
                "HOST": "0.0.0.0",
                "PORT": "8080",
                "LICICAN_ALERTS_PATH": "/tmp/alerts.json",
            },
            clear=True,
        ):
            config._ENV_LOADED = True
            self.assertEqual("/licican", config.resolve_base_path())
            self.assertEqual("0.0.0.0", config.resolve_host())
            self.assertEqual(8080, config.resolve_port())
            self.assertEqual(Path("/tmp/alerts.json"), config.resolve_alerts_path())

    def test_resolve_host_defaults_to_loopback_when_missing(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config._ENV_LOADED = True
            self.assertEqual("127.0.0.1", config.resolve_host())
