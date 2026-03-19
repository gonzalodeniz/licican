from __future__ import annotations

import json
from html import escape
from urllib.parse import parse_qs, quote
from wsgiref.simple_server import make_server

from podencoti.opportunity_catalog import CatalogFilters, build_catalog, build_opportunity_detail
from podencoti.source_coverage import load_source_coverage, summary_by_status
from podencoti.ti_classification import audit_examples, load_rule_set


def _page_template(
    document_title: str,
    page_heading: str,
    hero_label: str,
    hero_body: str,
    content: str,
) -> str:
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>{escape(document_title)}</title>
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
        --ok: #2f6b45;
        --warn: #946200;
        --risk: #9c3b2f;
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
      .hero, .panel, .metric, .note {{
        background: color-mix(in srgb, var(--card) 94%, white);
        border: 1px solid var(--line);
        border-radius: 20px;
        box-shadow: 0 18px 40px rgb(28 39 51 / 0.08);
      }}
      .hero {{
        padding: 2rem;
        margin-bottom: 1.5rem;
      }}
      .panel {{
        overflow: hidden;
        margin-bottom: 1.5rem;
      }}
      .panel-body {{
        padding: 1.5rem;
      }}
      h1, h2, h3 {{
        margin-top: 0;
      }}
      p, li {{
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
        padding: 1rem;
      }}
      .metric strong {{
        display: block;
        font-size: 2rem;
        color: var(--accent);
      }}
      .rule-grid {{
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      }}
      .rule-list {{
        margin: 0;
        padding-left: 1.1rem;
      }}
      .badge {{
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.4rem;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: var(--accent-soft);
        font-size: 0.95rem;
      }}
      .badge.ok {{
        background: #dceedd;
        color: var(--ok);
      }}
      .badge.warn {{
        background: #f5eac6;
        color: var(--warn);
      }}
      .badge.risk {{
        background: #f8ddd7;
        color: var(--risk);
      }}
      .filters {{
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        align-items: end;
      }}
      .filters label {{
        display: block;
        font-size: 0.95rem;
        color: var(--muted);
        margin-bottom: 0.35rem;
      }}
      .filters input, .filters select {{
        width: 100%;
        box-sizing: border-box;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
        font: inherit;
        background: white;
        color: var(--ink);
      }}
      .filter-actions {{
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
      }}
      .button-link, button {{
        display: inline-block;
        border: 0;
        border-radius: 999px;
        padding: 0.8rem 1.2rem;
        font: inherit;
        text-decoration: none;
        cursor: pointer;
      }}
      button {{
        background: var(--accent);
        color: white;
      }}
      .button-link {{
        background: #efe4d4;
        color: var(--ink);
      }}
      .active-filters {{
        margin-top: 1rem;
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
      code {{
        font-size: 0.95em;
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
        <p class="muted">{escape(hero_label)}</p>
        <h1>{escape(page_heading)}</h1>
        <p>{hero_body}</p>
      </section>
      {content}
    </main>
  </body>
</html>"""


def _coverage_html_response() -> str:
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

    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{summary["MVP"]}</strong>Fuentes objetivo en MVP</article>
            <article class="metric"><strong>{summary["Posterior"]}</strong>Fuentes planificadas después del MVP</article>
            <article class="metric"><strong>{summary["Por definir"]}</strong>Fuentes pendientes de decisión</article>
          </div>
          <p class="muted">Los datos se cargan desde una configuración versionada en <code>data/source_coverage.json</code>.</p>
        </div>
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
    """
    return _page_template(
        "PodencoTI | Cobertura inicial del MVP",
        "Cobertura inicial de fuentes oficiales del MVP",
        "Release 0 · PB-007 · Cobertura visible y verificable",
        (
            "PodencoTI no comunica cobertura total del ecosistema canario en esta entrega. "
            "Esta vista delimita qué fuentes oficiales entran en el MVP, cuáles quedan para una fase posterior "
            "y cuáles siguen pendientes de decisión funcional."
        ),
        content,
    )


def _format_budget(amount: int | None) -> str:
    if amount is None:
        return "Presupuesto no informado"
    formatted = f"{amount:,.0f}".replace(",", ".")
    return f"{formatted} EUR"


def _detail_url(opportunity_id: str) -> str:
    return f"/oportunidades/{quote(opportunity_id)}"


def _parse_catalog_filters(environ) -> CatalogFilters:
    query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)

    def first(name: str) -> str | None:
        values = query.get(name)
        if not values:
            return None
        value = values[0].strip()
        return value or None

    def integer(name: str) -> int | None:
        value = first(name)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    return CatalogFilters(
        palabra_clave=first("palabra_clave"),
        presupuesto_min=integer("presupuesto_min"),
        presupuesto_max=integer("presupuesto_max"),
        procedimiento=first("procedimiento"),
        ubicacion=first("ubicacion"),
    )


def _active_filter_badges(filters: dict[str, object]) -> str:
    labels = {
        "palabra_clave": "Palabra clave",
        "presupuesto_min": "Presupuesto mínimo",
        "presupuesto_max": "Presupuesto máximo",
        "procedimiento": "Procedimiento",
        "ubicacion": "Ubicación",
    }
    if not filters:
        return ""

    badges = "".join(
        f'<span class="badge">{escape(labels[key])}: {escape(str(value))}</span>'
        for key, value in filters.items()
    )
    return f"""
      <div class="active-filters">
        <p><strong>Filtros activos</strong></p>
        <div>{badges}</div>
      </div>
    """


def _catalog_html_response(filters: CatalogFilters | None = None) -> str:
    catalog = build_catalog(filters=filters)
    opportunities = catalog["oportunidades"]
    active_filters = catalog["filtros_activos"]
    available_filters = catalog["filtros_disponibles"]
    filter_form = f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Filtros funcionales</h2>
          <form method="get" action="/">
            <div class="filters">
              <div>
                <label for="palabra_clave">Palabra clave</label>
                <input id="palabra_clave" name="palabra_clave" type="text" value="{escape(str(active_filters.get("palabra_clave", "")))}" placeholder="backup, licencias, redes..." />
              </div>
              <div>
                <label for="presupuesto_min">Presupuesto mínimo</label>
                <input id="presupuesto_min" name="presupuesto_min" type="number" min="0" step="1" value="{escape(str(active_filters.get("presupuesto_min", "")))}" />
              </div>
              <div>
                <label for="presupuesto_max">Presupuesto máximo</label>
                <input id="presupuesto_max" name="presupuesto_max" type="number" min="0" step="1" value="{escape(str(active_filters.get("presupuesto_max", "")))}" />
              </div>
              <div>
                <label for="procedimiento">Procedimiento</label>
                <select id="procedimiento" name="procedimiento">
                  <option value="">Todos</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if active_filters.get("procedimiento") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["procedimientos"]
                  )}
                </select>
              </div>
              <div>
                <label for="ubicacion">Ubicación</label>
                <select id="ubicacion" name="ubicacion">
                  <option value="">Todas</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if active_filters.get("ubicacion") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["ubicaciones"]
                  )}
                </select>
              </div>
            </div>
            <div class="filter-actions">
              <button type="submit">Aplicar filtros</button>
              <a class="button-link" href="/">Limpiar filtros</a>
            </div>
          </form>
          {_active_filter_badges(active_filters)}
        </div>
      </section>
    """

    if opportunities:
        rows = "\n".join(
            (
                "<tr>"
                f'<td data-label="Oportunidad"><a href="{escape(_detail_url(item["id"]))}">{escape(item["titulo"])}</a></td>'
                f'<td data-label="Organismo">{escape(item["organismo"])}</td>'
                f'<td data-label="Ubicación">{escape(item["ubicacion"])}</td>'
                f'<td data-label="Procedimiento">{escape(item["procedimiento"] or "No informado")}</td>'
                f'<td data-label="Presupuesto">{escape(_format_budget(item["presupuesto"]))}</td>'
                f'<td data-label="Fecha límite">{escape(item["fecha_limite"])}</td>'
                f'<td data-label="Estado">{escape(item["estado"])}</td>'
                f'<td data-label="Fuente oficial"><a href="{escape(item["url_fuente_oficial"])}">{escape(item["fuente_oficial"])}</a></td>'
                "</tr>"
            )
            for item in opportunities
        )
        catalog_panel = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{catalog["total_oportunidades_catalogo"]}</strong>Oportunidades TI visibles</article>
            <article class="metric"><strong>{len(catalog["cobertura_aplicada"])}</strong>Fuentes oficiales MVP aplicadas</article>
            <article class="metric"><strong>{catalog["total_oportunidades_visibles"]}</strong>Oportunidades TI antes de filtrar</article>
          </div>
          <p class="muted">
            El catálogo reutiliza la cobertura MVP de <code>PB-007</code> y la clasificación auditable de <code>PB-006</code>.
            No representa todavía cobertura total del ecosistema canario.
          </p>
        </div>
        <table>
          <thead>
            <tr>
              <th>Oportunidad</th>
              <th>Organismo</th>
              <th>Ubicación</th>
              <th>Procedimiento</th>
              <th>Presupuesto</th>
              <th>Fecha límite</th>
              <th>Estado</th>
              <th>Fuente oficial</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </section>
        """
    else:
        message = (
            "No hay resultados con los filtros activos."
            if active_filters
            else "No hay oportunidades TI disponibles dentro de la cobertura MVP en este momento."
        )
        catalog_panel = f"""
      <section class="note">
        {escape(message)}
      </section>
        """

    content = f"""
      {filter_form}
      {catalog_panel}

      <p class="note">
        Referencia funcional activa: <code>{escape(catalog["referencia_funcional"])}</code>.
        Cada registro mantiene visible su fuente oficial para facilitar verificación por <code>qa-teams</code>.
      </p>
    """
    return _page_template(
        "PodencoTI | Catálogo inicial de oportunidades TI",
        "Catálogo inicial de oportunidades TI de Canarias",
        "Release 1 · PB-001 · Descubrimiento inicial verificable",
        (
            "PodencoTI muestra aquí un primer catálogo consultable de oportunidades TI dentro de la cobertura MVP ya delimitada. "
            "Solo se publican registros clasificados como TI y con fuente oficial visible."
        ),
        content,
    )


def _detail_html_response(opportunity_id: str) -> str | None:
    detail = build_opportunity_detail(opportunity_id)
    if detail is None:
        return None

    update = detail["actualizacion_oficial_mas_reciente"]
    update_panel = ""
    if update is not None:
        update_panel = f"""
      <section class="note">
        La ficha refleja el ultimo dato oficial visible publicado el <strong>{escape(str(update["fecha_publicacion"]))}</strong>
        mediante <strong>{escape(str(update["tipo"]))}</strong>.
        {escape(str(update["resumen"]))}
      </section>
        """

    criteria_items = detail["criterios_adjudicacion"]
    if criteria_items:
        criteria_html = "<ul>" + "".join(
            f"<li>{escape(str(item))}</li>" for item in criteria_items
        ) + "</ul>"
    else:
        criteria_html = "<p>No informado</p>"

    solvency_html = escape(str(detail["solvencia_tecnica"] or "No informado"))
    latest_fields = f"""
      <section class="panel">
        <div class="panel-body">
          <p><a href="/">Volver al catalogo</a></p>
          <div class="summary">
            <article class="metric"><strong>{escape(str(detail["estado"]))}</strong>Estado oficial visible</article>
            <article class="metric"><strong>{escape(str(detail["fecha_limite"]))}</strong>Fecha limite visible</article>
            <article class="metric"><strong>{escape(_format_budget(detail["presupuesto"]))}</strong>Presupuesto visible</article>
          </div>
          <table>
            <tbody>
              <tr><th>Organismo convocante</th><td>{escape(str(detail["organismo"]))}</td></tr>
              <tr><th>Ubicacion</th><td>{escape(str(detail["ubicacion"]))}</td></tr>
              <tr><th>Procedimiento</th><td>{escape(str(detail["procedimiento"] or "No informado"))}</td></tr>
              <tr><th>Presupuesto</th><td>{escape(_format_budget(detail["presupuesto"]))}</td></tr>
              <tr><th>Fecha limite</th><td>{escape(str(detail["fecha_limite"]))}</td></tr>
              <tr><th>Estado oficial del expediente</th><td>{escape(str(detail["estado"]))}</td></tr>
              <tr><th>Fuente oficial</th><td><a href="{escape(str(detail["url_fuente_oficial"]))}">{escape(str(detail["fuente_oficial"]))}</a></td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel">
        <div class="panel-body">
          <h2>Contexto resumido</h2>
          <p>{escape(str(detail["descripcion"]))}</p>
        </div>
      </section>

      <section class="panel">
        <div class="panel-body">
          <h2>Solvencia tecnica</h2>
          <p>{solvency_html}</p>
        </div>
      </section>

      <section class="panel">
        <div class="panel-body">
          <h2>Criterios de adjudicacion</h2>
          {criteria_html}
        </div>
      </section>
    """

    return _page_template(
        "PodencoTI | Ficha de detalle de licitacion",
        str(detail["titulo"]),
        "Release 1 · PB-002 · Ficha resumida verificable",
        (
            "La ficha resume los datos criticos del expediente y mantiene visible la fuente oficial. "
            "Cuando existe una rectificacion o modificacion publicada por el origen, se muestra el ultimo dato oficial visible."
        ),
        update_panel + latest_fields,
    )


def _classification_html_response() -> str:
    rules = load_rule_set()
    audited_examples = audit_examples(rules)
    example_rows = "\n".join(
        (
            "<tr>"
            f'<td data-label="Ejemplo">{escape(example["titulo"])}</td>'
            f'<td data-label="Esperada">{escape(example["clasificacion_esperada"])}</td>'
            f'<td data-label="Obtenida">{escape(example["clasificacion_obtenida"])}</td>'
            f'<td data-label="Coincidencias">{escape(", ".join(example["coincidencias_inclusion"] + example["coincidencias_exclusion"] + example["coincidencias_frontera"]) or "Sin coincidencias")}</td>'
            f'<td data-label="Trazabilidad">{escape(example["motivo_ejemplo"])}</td>'
            "</tr>"
        )
        for example in audited_examples
    )
    inclusion_badges = "".join(
        f'<span class="badge ok">{escape(term)}</span>' for term in rules.inclusion_palabras_clave
    )
    cpv_badges = "".join(
        f'<span class="badge ok">{escape(prefix)}</span>' for prefix in rules.inclusion_cpv_prefixes
    )
    exclusion_badges = "".join(
        f'<span class="badge risk">{escape(term)}</span>' for term in rules.exclusion_palabras_clave
    )
    frontier_badges = "".join(
        f'<span class="badge warn">{escape(term)}</span>' for term in rules.frontera_palabras_clave
    )

    content = f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Reglas auditables aplicadas</h2>
          <div class="rule-grid">
            <article>
              <h3>Inclusión por palabras clave</h3>
              <div>{inclusion_badges}</div>
            </article>
            <article>
              <h3>Inclusión por prefijos CPV</h3>
              <div>{cpv_badges}</div>
            </article>
            <article>
              <h3>Exclusiones funcionales</h3>
              <div>{exclusion_badges}</div>
            </article>
            <article>
              <h3>Casos frontera</h3>
              <div>{frontier_badges}</div>
            </article>
          </div>
          <p class="muted">Referencia funcional: <code>{escape(rules.referencia_funcional)}</code></p>
        </div>
      </section>

      <section class="panel">
        <div class="panel-body">
          <h2>Ejemplos auditados para QA</h2>
          <p>
            Esta superficie permite revisar inclusiones, exclusiones y <strong>casos frontera</strong> sin depender todavía del catálogo de <code>PB-001</code>.
            Los expedientes mixtos o de <strong>telecomunicaciones</strong> ambiguas quedan identificados como revisables.
          </p>
        </div>
        <table>
          <thead>
            <tr>
              <th>Ejemplo</th>
              <th>Esperada</th>
              <th>Obtenida</th>
              <th>Coincidencias</th>
              <th>Trazabilidad funcional</th>
            </tr>
          </thead>
          <tbody>
            {example_rows}
          </tbody>
        </table>
      </section>
    """
    return _page_template(
        "PodencoTI | Clasificación TI auditable",
        "Clasificación TI auditable",
        "Release 0 · PB-006 · Regla TI verificable",
        (
            "PodencoTI fija aquí la regla funcional mínima para decidir qué oportunidades son TI, "
            "cuáles deben excluirse y qué expedientes requieren revisión adicional antes de aparecer en el catálogo."
        ),
        content,
    )


def _json_response(payload: dict[str, object]) -> list[bytes]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return [body]


def _html_response(content: str) -> list[bytes]:
    return [content.encode("utf-8")]


def _respond(start_response, status: str, content_type: str, body: bytes) -> list[bytes]:
    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
    ]
    start_response(status, headers)
    return [body]


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    filters = _parse_catalog_filters(environ)

    if path.startswith("/api/oportunidades/"):
        opportunity_id = path.removeprefix("/api/oportunidades/")
        detail = build_opportunity_detail(opportunity_id)
        if detail is None:
            body = b"No encontrado"
            return _respond(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(_json_response(detail))
        return _respond(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/oportunidades":
        body = b"".join(_json_response(build_catalog(filters=filters)))
        return _respond(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/fuentes":
        sources = load_source_coverage()
        payload = {
            "sources": [source.__dict__ for source in sources],
            "summary": summary_by_status(sources),
        }
        body = b"".join(_json_response(payload))
        return _respond(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/clasificacion-ti":
        rules = load_rule_set()
        payload = {
            "referencia_funcional": rules.referencia_funcional,
            "reglas": {
                "inclusion_palabras_clave": list(rules.inclusion_palabras_clave),
                "inclusion_cpv_prefixes": list(rules.inclusion_cpv_prefixes),
                "inclusion_necesidades_explicitas": list(rules.inclusion_necesidades_explicitas),
                "exclusion_palabras_clave": list(rules.exclusion_palabras_clave),
                "casos_frontera": list(rules.frontera_palabras_clave),
            },
            "ejemplos_auditados": audit_examples(rules),
        }
        body = b"".join(_json_response(payload))
        return _respond(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/clasificacion-ti":
        body = b"".join(_html_response(_classification_html_response()))
        return _respond(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/cobertura-fuentes":
        body = b"".join(_html_response(_coverage_html_response()))
        return _respond(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path.startswith("/oportunidades/"):
        opportunity_id = path.removeprefix("/oportunidades/")
        content = _detail_html_response(opportunity_id)
        if content is None:
            body = b"No encontrado"
            return _respond(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(_html_response(content))
        return _respond(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/":
        body = b"".join(_html_response(_catalog_html_response(filters)))
        return _respond(start_response, "200 OK", "text/html; charset=utf-8", body)

    body = b"No encontrado"
    return _respond(start_response, "404 Not Found", "text/plain; charset=utf-8", body)


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
