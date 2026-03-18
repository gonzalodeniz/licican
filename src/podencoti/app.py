from __future__ import annotations

import json
from html import escape
from wsgiref.simple_server import make_server

from podencoti.source_coverage import load_source_coverage, summary_by_status


def _html_response() -> str:
    sources = load_source_coverage()
    summary = summary_by_status(sources)
    rows = "\n".join(
        (
            "<tr>"
            f'<td data-label="Fuente oficial">{escape(source.nombre)}</td>'
            f'<td data-label="Categoría">{escape(source.categoria)}</td>'
            f'<td data-label="Estado">{escape(source.estado)}</td>'
            f'<td data-label="Alcance">{escape(source.alcance)}</td>'
            f'<td data-label="Justificación funcional">{escape(source.descripcion)}</td>'
            f'<td data-label="Trazabilidad">{escape(source.referencia_funcional)}</td>'
            "</tr>"
        )
        for source in sources
    )

    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>PodencoTI | Cobertura inicial del MVP</title>
    <style>
      :root {{
        color-scheme: light;
        --bg: #f4efe6;
        --card: #fffdf9;
        --ink: #1c2733;
        --muted: #5f6b76;
        --line: #d7c7af;
        --accent: #a7502b;
        --accent-soft: #f4d8c7;
      }}
      body {{
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background:
          radial-gradient(circle at top right, #f8dfca 0, transparent 22rem),
          linear-gradient(180deg, #f9f4ec 0%, var(--bg) 100%);
        color: var(--ink);
      }}
      main {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 3rem 1.5rem 4rem;
      }}
      .hero, .panel {{
        background: color-mix(in srgb, var(--card) 94%, white);
        border: 1px solid var(--line);
        border-radius: 20px;
        box-shadow: 0 18px 40px rgb(28 39 51 / 0.08);
      }}
      .hero {{
        padding: 2rem;
        margin-bottom: 1.5rem;
      }}
      h1, h2 {{
        margin-top: 0;
      }}
      p {{
        line-height: 1.6;
      }}
      .muted {{
        color: var(--muted);
      }}
      .summary {{
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        margin: 1.5rem 0;
      }}
      .metric {{
        background: var(--accent-soft);
        border-radius: 16px;
        padding: 1rem;
      }}
      .metric strong {{
        display: block;
        font-size: 2rem;
        color: var(--accent);
      }}
      .panel {{
        overflow: hidden;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        text-align: left;
        padding: 0.9rem 1rem;
        border-bottom: 1px solid var(--line);
        vertical-align: top;
      }}
      th {{
        background: #f6ebdf;
      }}
      tr:last-child td {{
        border-bottom: 0;
      }}
      .note {{
        margin-top: 1rem;
        padding: 1rem 1.25rem;
        border-left: 4px solid var(--accent);
        background: #fff4ea;
      }}
      @media (max-width: 720px) {{
        table, thead, tbody, th, td, tr {{
          display: block;
        }}
        thead {{
          display: none;
        }}
        td {{
          padding-top: 0.35rem;
          padding-bottom: 0.35rem;
        }}
        td::before {{
          content: attr(data-label);
          display: block;
          color: var(--muted);
          font-size: 0.85rem;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          margin-bottom: 0.2rem;
        }}
      }}
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <p class="muted">Release 0 · PB-007 · Cobertura visible y verificable</p>
        <h1>Cobertura inicial de fuentes oficiales del MVP</h1>
        <p>
          PodencoTI no comunica cobertura total del ecosistema canario en esta entrega.
          Esta vista delimita qué fuentes oficiales entran en el MVP, cuáles quedan para una fase posterior
          y cuáles siguen pendientes de decisión funcional.
        </p>
        <div class="summary">
          <article class="metric"><strong>{summary["MVP"]}</strong>Fuentes objetivo en MVP</article>
          <article class="metric"><strong>{summary["Posterior"]}</strong>Fuentes planificadas después del MVP</article>
          <article class="metric"><strong>{summary["Por definir"]}</strong>Fuentes pendientes de decisión</article>
        </div>
        <p class="muted">Los datos se cargan desde una configuración versionada en <code>data/source_coverage.json</code>.</p>
      </section>

      <section class="panel">
        <table>
          <thead>
            <tr>
              <th>Fuente oficial</th>
              <th>Categoría</th>
              <th>Estado</th>
              <th>Alcance</th>
              <th>Justificación funcional</th>
              <th>Trazabilidad</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </section>

      <p class="note">
        Referencia funcional alineada con <code>product-manager/refinamiento-funcional.md</code> y <code>product-manager/roadmap.md</code>.
        Esta cobertura sirve de base para el catálogo inicial del MVP sin inducir una expectativa de exhaustividad.
      </p>
    </main>
  </body>
</html>"""


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path == "/api/fuentes":
        sources = load_source_coverage()
        payload = {
            "sources": [source.__dict__ for source in sources],
            "summary": summary_by_status(sources),
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ]
        start_response("200 OK", headers)
        return [body]

    if path == "/":
        body = _html_response().encode("utf-8")
        headers = [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ]
        start_response("200 OK", headers)
        return [body]

    body = b"No encontrado"
    start_response(
        "404 Not Found",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


def main() -> None:
    host = "127.0.0.1"
    port = 8000
    with make_server(host, port, application) as httpd:
        print(f"Servidor disponible en http://{host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("\nServidor detenido de forma controlada.")


if __name__ == "__main__":
    main()
