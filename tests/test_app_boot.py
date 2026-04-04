from __future__ import annotations

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from licican.app import application, main


class ApplicationBootstrapTests(unittest.TestCase):
    def test_main_handles_keyboard_interrupt_with_controlled_shutdown(self) -> None:
        stdout = io.StringIO()

        with patch.dict(os.environ, {"BASE_PATH": "/licican", "HOST": "127.0.0.1", "PORT": "8123"}, clear=False):
            with patch("licican.app.make_server") as make_server_mock:
                server = make_server_mock.return_value.__enter__.return_value
                server.serve_forever.side_effect = KeyboardInterrupt

                with redirect_stdout(stdout):
                    main()

        output = stdout.getvalue()
        self.assertIn("Servidor disponible en http://127.0.0.1:8123/licican", output)
        self.assertIn("Servidor detenido de forma controlada.", output)
        make_server_mock.assert_called_once_with("127.0.0.1", 8123, application)
        server.server_close.assert_called_once_with()

    def test_main_uses_configured_host_when_present(self) -> None:
        stdout = io.StringIO()

        with patch.dict(os.environ, {"BASE_PATH": "/licican", "HOST": "0.0.0.0", "PORT": "8124"}, clear=False):
            with patch("licican.app.make_server") as make_server_mock:
                server = make_server_mock.return_value.__enter__.return_value
                server.serve_forever.side_effect = KeyboardInterrupt

                with redirect_stdout(stdout):
                    main()

        output = stdout.getvalue()
        self.assertIn("Servidor disponible en http://0.0.0.0:8124/licican", output)
        make_server_mock.assert_called_once_with("0.0.0.0", 8124, application)

    def test_main_rejects_invalid_port_configuration(self) -> None:
        with patch.dict(os.environ, {"BASE_PATH": "/licican", "PORT": "not-a-number"}, clear=False):
            with self.assertRaisesRegex(ValueError, "PORT debe ser un numero entero valido"):
                main()
