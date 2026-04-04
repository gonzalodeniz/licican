from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.shared.app_http import invoke_app


class ApplicationPipelineTests(unittest.TestCase):
    def test_pipeline_page_renders_empty_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            with patch.dict(os.environ, {"LICICAN_PIPELINE_PATH": str(pipeline_path)}, clear=False):
                status, headers, body = invoke_app("/pipeline")

        html = body.decode("utf-8")
        self.assertEqual("200 OK", status)
        self.assertEqual("text/html; charset=utf-8", headers["Content-Type"])
        self.assertIn('id="pipeline-summary-panel"', html)
        self.assertIn("Pipeline de seguimiento de oportunidades", html)
        self.assertIn("Todavía no hay oportunidades guardadas en el pipeline.", html)
        self.assertIn('class="nav-link active" href="/licican/pipeline"', html)

    def test_pipeline_lifecycle_is_visible_from_html_and_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_path = Path(tmp_dir) / "pipeline.json"
            with patch.dict(os.environ, {"LICICAN_PIPELINE_PATH": str(pipeline_path)}, clear=False):
                created_status, created_headers, _ = invoke_app(
                    "/pipeline",
                    method="POST",
                    body="opportunity_id=pcsp-cabildo-licencias-2026",
                )
                self.assertEqual("303 See Other", created_status)
                self.assertEqual("/licican/pipeline?mensaje=Oportunidad+guardada+en+el+pipeline", created_headers["Location"])

                duplicate_status, duplicate_headers, _ = invoke_app(
                    "/pipeline",
                    method="POST",
                    body="opportunity_id=pcsp-cabildo-licencias-2026",
                )
                self.assertEqual("303 See Other", duplicate_status)
                self.assertEqual(
                    "/licican/pipeline?mensaje=La+oportunidad+ya+estaba+guardada+en+el+pipeline",
                    duplicate_headers["Location"],
                )

                update_status, update_headers, _ = invoke_app(
                    "/pipeline/pcsp-cabildo-licencias-2026/estado",
                    method="POST",
                    body="estado_seguimiento=Evaluando",
                )
                self.assertEqual("303 See Other", update_status)
                self.assertEqual("/licican/pipeline?mensaje=Estado+de+pipeline+actualizado", update_headers["Location"])

                page_status, page_headers, page_body = invoke_app("/pipeline")
                api_status, api_headers, api_body = invoke_app("/api/pipeline")

        html = page_body.decode("utf-8")
        api_payload = json.loads(api_body)

        self.assertEqual("200 OK", page_status)
        self.assertEqual("text/html; charset=utf-8", page_headers["Content-Type"])
        self.assertIn('id="pipeline-summary-panel"', html)
        self.assertIn("pcsp-cabildo-licencias-2026", html)
        self.assertIn("Evaluando", html)
        self.assertIn("Fuente oficial", html)

        self.assertEqual("200 OK", api_status)
        self.assertEqual("application/json; charset=utf-8", api_headers["Content-Type"])
        self.assertEqual(1, api_payload["summary"]["total_oportunidades"])
        self.assertEqual(0, api_payload["summary"]["con_advertencia_oficial"])
        self.assertEqual("Evaluando", api_payload["pipeline"][0]["estado_seguimiento"])
