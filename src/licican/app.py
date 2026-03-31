from __future__ import annotations

from html import escape
from urllib.parse import parse_qs, quote, urlencode
from wsgiref.simple_server import make_server

from licican.alerts import create_alert, deactivate_alert, load_alerts, summarize_alerts, update_alert
from licican.canarias_dataset import build_adjudicacion_detail, build_licitacion_detail, load_canarias_dataset
from licican.config import (
    normalize_base_path,
    resolve_alerts_path,
    resolve_base_path,
    resolve_host,
    resolve_port,
)
from licican.opportunity_catalog import (
    CatalogDataSourceError,
    CatalogFilters,
    build_catalog,
    build_opportunity_detail,
)
from licican.real_source_prioritization import load_real_source_prioritization, summarize_prioritization
from licican.source_coverage import load_source_coverage, summary_by_status
from licican.ti_classification import audit_examples, load_rule_set
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response


def _page_template(
    document_title: str,
    page_heading: str,
    hero_label: str,
    hero_body: str,
    content: str,
    current_path: str = "/",
    base_path: str = "",
) -> str:
    navigation = _navigation_html(base_path, current_path)
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>{escape(document_title)}</title>
    <style>
      :root {{
        color-scheme: light;
        --bg: #ece5db;
        --card: #fffdf8;
        --ink: #121a23;
        --muted: #58646f;
        --line: #cdbfae;
        --accent: #0f4c5c;
        --accent-strong: #16384d;
        --accent-soft: #d9e4e6;
        --ok: #1d5b3a;
        --warn: #8a5b00;
        --risk: #8a2f2a;
      }}
      body {{
        margin: 0;
        font-family: "IBM Plex Serif", Georgia, "Times New Roman", serif;
        background:
          radial-gradient(circle at top left, rgb(15 76 92 / 0.16) 0, transparent 28rem),
          linear-gradient(180deg, #f4eee5 0%, var(--bg) 100%);
        color: var(--ink);
      }}
      .app-shell {{
        width: 100%;
        max-width: none;
        margin: 0 auto;
        box-sizing: border-box;
        padding: 1.35rem 1.5rem;
      }}
      .app-frame {{
        display: grid;
        grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
        gap: 1.35rem;
        align-items: start;
      }}
      .side-nav,
      .mobile-nav {{
        background: color-mix(in srgb, var(--card) 94%, white);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: 0 18px 40px rgb(18 26 35 / 0.08);
      }}
      .side-nav {{
        position: sticky;
        top: 1.35rem;
        padding: 1.3rem 1rem;
      }}
      .nav-kicker {{
        margin: 0 0 0.35rem;
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      .nav-title {{
        margin: 0 0 1rem;
        font-size: 1.45rem;
      }}
      .nav-copy {{
        margin: 0 0 1.25rem;
        color: var(--muted);
      }}
      .nav-section {{
        margin-top: 1.2rem;
      }}
      .nav-section-title {{
        margin: 0 0 0.55rem;
        color: var(--muted);
        font-size: 0.85rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }}
      .nav-list {{
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        gap: 0.45rem;
      }}
      .nav-link,
      .nav-link-static {{
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        gap: 0.75rem;
        align-items: center;
        text-decoration: none;
        border-radius: 18px;
        padding: 0.8rem 0.9rem;
        border: 1px solid transparent;
      }}
      .nav-link {{
        color: var(--ink);
      }}
      .nav-link:hover {{
        background: rgb(15 76 92 / 0.06);
        border-color: rgb(15 76 92 / 0.1);
      }}
      .nav-link.active {{
        background: linear-gradient(135deg, rgb(15 76 92 / 0.16), rgb(15 76 92 / 0.07));
        border-color: rgb(15 76 92 / 0.28);
      }}
      .nav-link-static {{
        color: var(--muted);
        background: rgb(88 100 111 / 0.05);
        border-color: rgb(88 100 111 / 0.12);
      }}
      .nav-icon {{
        width: 2.2rem;
        height: 2.2rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: rgb(15 76 92 / 0.1);
        color: var(--accent-strong);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
      }}
      .nav-link.active .nav-icon {{
        background: var(--accent);
        color: white;
      }}
      .nav-copy-block {{
        min-width: 0;
      }}
      .nav-label {{
        display: block;
        font-weight: 700;
      }}
      .nav-help {{
        display: block;
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.35;
      }}
      .nav-tag {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        font-size: 0.78rem;
        background: #f5eac6;
        color: var(--warn);
      }}
      .nav-note {{
        margin-top: 1.2rem;
        padding: 0.95rem 1rem;
        border-radius: 18px;
        background: rgb(15 76 92 / 0.06);
        color: var(--muted);
        line-height: 1.45;
      }}
      .content-shell {{
        min-width: 0;
      }}
      .mobile-nav {{
        display: none;
        margin-bottom: 1rem;
        overflow: hidden;
      }}
      .mobile-nav summary {{
        list-style: none;
        cursor: pointer;
        padding: 1rem 1.1rem;
        font-weight: 700;
      }}
      .mobile-nav summary::-webkit-details-marker {{
        display: none;
      }}
      .mobile-nav[open] summary {{
        border-bottom: 1px solid var(--line);
      }}
      .mobile-nav-body {{
        padding: 0.45rem 0.8rem 0.9rem;
      }}
      main {{
        min-width: 0;
        padding: 1.15rem 0 3rem;
      }}
      .hero, .panel, .metric, .note {{
        background: color-mix(in srgb, var(--card) 94%, white);
        border: 1px solid var(--line);
        border-radius: 22px;
        box-shadow: 0 18px 40px rgb(18 26 35 / 0.08);
      }}
      .hero {{
        padding: 2rem 2.1rem;
        margin-bottom: 1.35rem;
        background:
          linear-gradient(135deg, rgb(15 76 92 / 0.08), rgb(255 255 255 / 0.96) 52%),
          var(--card);
        border-left: 6px solid var(--accent);
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
        line-height: 1.05;
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
        gap: 1.15rem;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        align-items: end;
      }}
      .filters label {{
        display: block;
        font-size: 0.95rem;
        color: var(--muted);
        margin-bottom: 0.4rem;
      }}
      .filters input, .filters select {{
        width: 100%;
        box-sizing: border-box;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.85rem 0.95rem;
        font: inherit;
        background: #fff;
        color: var(--ink);
        box-shadow: inset 0 1px 0 rgb(18 26 35 / 0.03);
      }}
      .filter-actions {{
        display: flex;
        gap: 0.85rem;
        flex-wrap: wrap;
        justify-content: flex-end;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
      }}
      .button-link, button {{
        display: inline-block;
        border: 0;
        border-radius: 999px;
        padding: 0.86rem 1.25rem;
        font: inherit;
        text-decoration: none;
        cursor: pointer;
        transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease, color 160ms ease, border-color 160ms ease;
      }}
      button {{
        background: var(--accent);
        color: white;
        box-shadow: 0 10px 24px rgb(15 76 92 / 0.22);
      }}
      .button-link {{
        background: transparent;
        color: var(--accent);
        border: 1px solid var(--accent);
      }}
      .button-link:hover, button:hover {{
        transform: translateY(-1px);
      }}
      .button-link:hover {{
        background: rgb(15 76 92 / 0.06);
      }}
      button:hover {{
        background: var(--accent-strong);
      }}
      .active-filters {{
        margin-top: 1rem;
      }}
      .pagination-bar {{
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        margin: 1rem 0 1.25rem;
        padding: 1rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: #f8f4ed;
      }}
      .pagination-status {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
      }}
      .pagination-actions {{
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
      }}
      .pagination-jump {{
        display: flex;
        gap: 0.65rem;
        align-items: center;
        flex-wrap: wrap;
      }}
      .pagination-jump label {{
        color: var(--muted);
      }}
      .pagination-jump input {{
        width: 6rem;
        box-sizing: border-box;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 0.65rem 0.8rem;
        font: inherit;
      }}
      .table-wrap {{
        overflow-x: auto;
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
        background: #eef2f0;
      }}
      tr:last-child td {{
        border-bottom: 0;
      }}
      .offer-cell {{
        display: flex;
        flex-direction: column;
        gap: 0.45rem;
      }}
      .offer-link {{
        color: var(--accent-strong);
        font-weight: 700;
        text-decoration-thickness: 2px;
        text-underline-offset: 0.18em;
      }}
      .offer-action {{
        align-self: flex-start;
        padding: 0.38rem 0.75rem;
        border-radius: 999px;
        border: 1px solid var(--accent);
        color: var(--accent);
        text-decoration: none;
        font-size: 0.92rem;
        background: rgb(15 76 92 / 0.04);
      }}
      .offer-action:hover {{
        background: rgb(15 76 92 / 0.09);
      }}
      .source-link {{
        color: var(--muted);
        text-decoration-thickness: 1px;
        text-underline-offset: 0.16em;
      }}
      .tab-nav {{
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 1rem 0 1.25rem;
      }}
      .tab-link {{
        display: inline-block;
        padding: 0.7rem 1rem;
        border-radius: 999px;
        text-decoration: none;
        border: 1px solid var(--line);
        color: var(--accent-strong);
        background: #fffaf3;
      }}
      .tab-link.active {{
        background: var(--accent);
        color: white;
        border-color: var(--accent);
        box-shadow: 0 10px 24px rgb(15 76 92 / 0.18);
      }}
      .note {{
        margin-top: 1rem;
        padding: 1rem 1.25rem;
        border-left: 4px solid var(--accent);
        background: #f8f6f1;
      }}
      .note-warning {{
        border-left-color: var(--warn);
        background: #fbf4e2;
      }}
      code {{
        font-size: 0.95em;
      }}
      @media (max-width: 720px) {{
        .app-shell {{
          padding: 0.85rem;
        }}
        .app-frame {{
          grid-template-columns: 1fr;
        }}
        .side-nav {{
          display: none;
        }}
        .mobile-nav {{
          display: block;
        }}
        main {{
          padding-top: 0;
        }}
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
        .offer-cell {{
          gap: 0.35rem;
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
    <div class="app-shell">
      <div class="app-frame">
        {navigation}
        <div class="content-shell">
          <main>
            <section class="hero">
              <p class="muted">{escape(hero_label)}</p>
              <h1>{escape(page_heading)}</h1>
              <p>{hero_body}</p>
            </section>
            {content}
          </main>
        </div>
      </div>
    </div>
  </body>
</html>"""


def _resolve_request_path(environ, base_path: str) -> str:
    raw_path = environ.get("PATH_INFO", "/") or "/"
    script_name = normalize_base_path(environ.get("SCRIPT_NAME")) or base_path

    if script_name and raw_path.startswith(script_name):
        raw_path = raw_path[len(script_name) :] or "/"

    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"

    return raw_path or "/"


def _navigation_items() -> list[dict[str, str | bool]]:
    return [
        {
            "label": "Catalogo",
            "description": "Oportunidades, filtros y paginacion",
            "icon": "CT",
            "path": "/",
            "upcoming": False,
        },
        {
            "label": "Datos consolidados",
            "description": "Excel funcional, lotes y adjudicaciones",
            "icon": "DC",
            "path": "/datos-consolidados",
            "upcoming": False,
        },
        {
            "label": "Alertas",
            "description": "Criterios guardados y coincidencias activas",
            "icon": "AL",
            "path": "/alertas",
            "upcoming": False,
        },
        {
            "label": "Clasificacion TI",
            "description": "Reglas auditables y casos frontera",
            "icon": "TI",
            "path": "/clasificacion-ti",
            "upcoming": False,
        },
        {
            "label": "Pipeline",
            "description": "Seguimiento operativo de oportunidades",
            "icon": "PL",
            "path": "",
            "upcoming": True,
        },
        {
            "label": "Permisos",
            "description": "Roles y restricciones por superficie",
            "icon": "PM",
            "path": "",
            "upcoming": True,
        },
    ]


def _path_matches_navigation(current_path: str, item_path: str) -> bool:
    if item_path == "/":
        return current_path == "/" or current_path.startswith("/oportunidades/")
    if item_path == "/datos-consolidados":
        return current_path == item_path or current_path.startswith(f"{item_path}/")
    return current_path == item_path or current_path.startswith(f"{item_path}/")


def _navigation_item_html(base_path: str, current_path: str, item: dict[str, str | bool]) -> str:
    label = str(item["label"])
    description = str(item["description"])
    icon = str(item["icon"])
    path = str(item["path"])
    upcoming = bool(item["upcoming"])

    if upcoming:
        return f"""
          <li>
            <div class="nav-link-static">
              <span class="nav-icon" aria-hidden="true">{escape(icon)}</span>
              <span class="nav-copy-block">
                <span class="nav-label">{escape(label)}</span>
                <span class="nav-help">{escape(description)}</span>
              </span>
              <span class="nav-tag">proximamente</span>
            </div>
          </li>
        """

    class_name = "nav-link active" if _path_matches_navigation(current_path, path) else "nav-link"
    return f"""
      <li>
        <a class="{class_name}" href="{escape(build_url(base_path, path))}">
          <span class="nav-icon" aria-hidden="true">{escape(icon)}</span>
          <span class="nav-copy-block">
            <span class="nav-label">{escape(label)}</span>
            <span class="nav-help">{escape(description)}</span>
          </span>
          <span class="nav-tag">activo</span>
        </a>
      </li>
    """


def _navigation_list_html(base_path: str, current_path: str) -> str:
    items = "".join(_navigation_item_html(base_path, current_path, item) for item in _navigation_items())
    return f'<ul class="nav-list">{items}</ul>'


def _navigation_html(base_path: str, current_path: str) -> str:
    list_html = _navigation_list_html(base_path, current_path)
    return f"""
      <aside class="side-nav" aria-label="Navegacion principal">
        <p class="nav-kicker">PB-010</p>
        <h2 class="nav-title">Licican</h2>
        <p class="nav-copy">Base de navegacion comun para catalogo, alertas y crecimiento de modulos sin rutas huerfanas.</p>
        <div class="nav-section">
          <p class="nav-section-title">Modulos</p>
          {list_html}
        </div>
        <p class="nav-note">
          La navegacion prioriza superficies ya operativas y deja marcadas como <strong>proximamente</strong> las piezas que todavia no tienen una vista utilizable.
        </p>
      </aside>
      <details class="mobile-nav">
        <summary>Menu principal</summary>
        <div class="mobile-nav-body">
          {list_html}
        </div>
      </details>
    """


def _coverage_html_response(base_path: str = "") -> str:
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
        "Licican | Cobertura inicial del MVP",
        "Cobertura inicial de fuentes oficiales del MVP",
        "Release 0 · PB-007 · Cobertura visible y verificable",
        (
            "Licican no comunica cobertura total del ecosistema canario en esta entrega. "
            "Esta vista delimita qué fuentes oficiales entran en el MVP, cuáles quedan para una fase posterior "
            "y cuáles siguen pendientes de decisión funcional."
        ),
        content,
        current_path="/cobertura-fuentes",
        base_path=base_path,
    )


def _real_source_prioritization_html_response(base_path: str = "") -> str:
    reference, sources, out_of_scope = load_real_source_prioritization()
    summary = summarize_prioritization(sources)
    rows = "\n".join(
        (
            "<tr>"
            f'<td data-label="Ola">{escape(source.ola)}</td>'
            f'<td data-label="Fuente real oficial"><a href="{escape(source.url_oficial)}">{escape(source.nombre)}</a></td>'
            f'<td data-label="Categoría">{escape(source.categoria)}</td>'
            f'<td data-label="Alcance">{escape(source.alcance)}</td>'
            f'<td data-label="Justificación">{escape(source.justificacion)}</td>'
            f'<td data-label="Trazabilidad">{escape(source.trazabilidad)}</td>'
            "</tr>"
        )
        for source in sources
    )
    out_of_scope_html = "".join(f"<li>{escape(item)}</li>" for item in out_of_scope)

    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{summary["Ola 1"]}</strong>Fuentes en Ola 1</article>
            <article class="metric"><strong>{summary["Ola 2"]}</strong>Fuentes en Ola 2</article>
            <article class="metric"><strong>{summary["Ola 3"]}</strong>Fuentes en Ola 3</article>
          </div>
          <p class="muted">
            Esta priorización reutiliza la cobertura visible de <code>PB-007</code> y la clasificación auditable de <code>PB-006</code>
            para reforzar la recopilación con fuentes reales oficiales antes de abrir alertas o pipeline.
          </p>
        </div>
        <table>
          <thead>
            <tr>
              <th>Ola</th>
              <th>Fuente real oficial</th>
              <th>Categoría</th>
              <th>Alcance</th>
              <th>Justificación</th>
              <th>Trazabilidad</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </section>

      <section class="note">
        <strong>Fuera de alcance en esta iteración</strong>
        <ul>
          {out_of_scope_html}
        </ul>
      </section>

      <p class="note">
        Referencia funcional activa: <code>{escape(reference)}</code>.
        La lista priorizada nombra de forma explícita <code>BOC</code>, <code>BOP Las Palmas</code> y <code>BOE</code> con orden por olas verificable por <code>qa-teams</code>.
      </p>
    """
    return _page_template(
        "Licican | Priorización de fuentes reales oficiales",
        "Priorización de fuentes reales oficiales para recopilación",
        "Release 2 · PB-009 · Recopilación priorizada por olas",
        (
            "Licican deja aquí visible qué fuentes oficiales reales deben entrar antes en la recopilación temprana. "
            "La entrega refuerza credibilidad y trazabilidad sin ampliar todavía cobertura comercial, alertas ni pipeline."
        ),
        content,
        current_path="/priorizacion-fuentes-reales",
        base_path=base_path,
    )


def _format_budget(amount: int | None) -> str:
    if amount is None:
        return "Presupuesto no informado"
    formatted = f"{amount:,.0f}".replace(",", ".")
    return f"{formatted} EUR"


def _detail_url(opportunity_id: str) -> str:
    return f"/oportunidades/{quote(opportunity_id)}"


def _parse_filters_from_multidict(values: dict[str, list[str]]) -> CatalogFilters:
    def first(name: str) -> str | None:
        candidates = values.get(name)
        if not candidates:
            return None
        value = candidates[0].strip()
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


def _parse_catalog_filters(environ) -> CatalogFilters:
    return _parse_filters_from_multidict(parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False))


def _parse_catalog_page(environ) -> int:
    values = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)
    candidates = values.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def _alert_filters_query(filters: dict[str, object]) -> str:
    return urlencode({key: value for key, value in filters.items() if value not in (None, "")})


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


def _catalog_query_string(filters: dict[str, object], page: int | None = None) -> str:
    params = {key: value for key, value in filters.items() if value not in (None, "")}
    if page is not None:
        params["page"] = page
    if not params:
        return ""
    return urlencode(params)


def _catalog_page_url(base_path: str, filters: dict[str, object], page: int) -> str:
    query = _catalog_query_string(filters, page)
    path = build_url(base_path, "/")
    if not query:
        return path
    return f"{path}?{query}"


def _pagination_adjustment_message(pagination: dict[str, object]) -> str | None:
    if not pagination.get("ajustada"):
        return None
    requested_page = pagination["pagina_solicitada"]
    current_page = pagination["pagina_actual"]
    if pagination.get("motivo_ajuste") == "invalida":
        return (
            f"La pagina solicitada ({requested_page}) no es valida. "
            f"Se muestra la pagina {current_page}."
        )
    return (
        f"La pagina solicitada ({requested_page}) no existe. "
        f"Se muestra la pagina {current_page}."
    )


def _pagination_jump_form(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    if int(pagination["total_paginas"]) <= 1:
        return ""

    hidden_fields = "".join(
        f'<input type="hidden" name="{escape(str(key))}" value="{escape(str(value))}" />'
        for key, value in filters.items()
        if value not in (None, "")
    )
    return f"""
      <form class="pagination-jump" method="get" action="{escape(build_url(base_path, '/'))}">
        {hidden_fields}
        <label for="catalog-page">Ir a la pagina</label>
        <input id="catalog-page" name="page" type="number" min="1" max="{pagination["total_paginas"]}" value="{pagination["pagina_actual"]}" />
        <button type="submit">Ir</button>
      </form>
    """


def _pagination_controls_html(base_path: str, filters: dict[str, object], pagination: dict[str, object]) -> str:
    if int(pagination["total_paginas"]) <= 1:
        return ""

    prev_link = ""
    if pagination["pagina_anterior"] is not None:
        prev_link = (
            f'<a class="button-link" href="{escape(_catalog_page_url(base_path, filters, int(pagination["pagina_anterior"])))}">'
            "Pagina anterior"
            "</a>"
        )

    next_link = ""
    if pagination["pagina_siguiente"] is not None:
        next_link = (
            f'<a class="button-link" href="{escape(_catalog_page_url(base_path, filters, int(pagination["pagina_siguiente"])))}">'
            "Pagina siguiente"
            "</a>"
        )

    return f"""
      <div class="pagination-bar">
        <div class="pagination-status">
          <strong>Pagina {pagination["pagina_actual"]} de {pagination["total_paginas"]}</strong>
          <span class="muted">Mostrando {pagination["resultado_desde"]}-{pagination["resultado_hasta"]} de {pagination["total_resultados"]}</span>
        </div>
        <div class="pagination-actions">
          {prev_link}
          {next_link}
        </div>
        {_pagination_jump_form(base_path, filters, pagination)}
      </div>
    """


def _status_note_html(message: str | None, tone: str = "ok") -> str:
    if message is None:
        return ""

    class_name = "note"
    if tone == "warn":
        class_name = "note note-warning"
    return f"""
      <section class="{class_name}">
        {escape(message)}
      </section>
    """


def _validation_note_html(message: str | None) -> str:
    if message is None:
        return ""
    return _status_note_html(f"Corrige el rango de presupuesto. {message}", "warn")


def _display_value(value: object | None) -> str:
    if value in (None, ""):
        return "No informado"
    return str(value)


def _tab_link(base_path: str, current_view: str, view: str, label: str) -> str:
    class_name = "tab-link active" if current_view == view else "tab-link"
    return (
        f'<a class="{class_name}" href="{escape(build_url(base_path, f"/datos-consolidados?vista={view}"))}">'
        f"{escape(label)}</a>"
    )


def _data_tabs_html(base_path: str, current_view: str) -> str:
    return f"""
      <nav class="tab-nav" aria-label="Pestañas de datos consolidados">
        {_tab_link(base_path, current_view, "licitaciones", "Licitaciones TI Canarias")}
        {_tab_link(base_path, current_view, "lotes", "Detalle Lotes")}
        {_tab_link(base_path, current_view, "adjudicaciones", "Adjudicaciones")}
      </nav>
    """


def _dataset_table_html(rows: list[dict[str, object]], columns: list[tuple[str, str]], actions: list[str] | None = None) -> str:
    if not rows:
        return """
      <section class="note">
        No hay filas disponibles en la hoja seleccionada para la muestra actual del Excel.
      </section>
        """

    headers = "".join(f"<th>{escape(label)}</th>" for _, label in columns)
    if actions is not None:
        headers += "<th>Detalle</th>"

    body_rows = []
    for index, row in enumerate(rows):
        cells = "".join(
            f'<td data-label="{escape(label)}">{escape(_display_value(row.get(key)))}</td>'
            for key, label in columns
        )
        if actions is not None:
            cells += f'<td data-label="Detalle">{actions[index]}</td>'
        body_rows.append(f"<tr>{cells}</tr>")

    return f"""
      <div class="table-wrap">
        <table>
          <thead>
            <tr>{headers}</tr>
          </thead>
          <tbody>
            {"".join(body_rows)}
          </tbody>
        </table>
      </div>
    """


def _datos_consolidados_html_response(view: str, base_path: str = "") -> str:
    dataset = load_canarias_dataset()
    selected_view = view if view in {"licitaciones", "lotes", "adjudicaciones"} else "licitaciones"
    tabs = _data_tabs_html(base_path, selected_view)

    if selected_view == "licitaciones":
        rows = dataset["licitaciones"]
        columns = [
            ("id_expediente", "ID Expediente"),
            ("titulo", "Título"),
            ("estado", "Estado"),
            ("organo_contratacion", "Órgano Contratación"),
            ("importe_sin_iva", "Importe sin IVA"),
            ("procedimiento", "Procedimiento"),
            ("plazo_presentacion", "Plazo Presentación"),
            ("numero_lotes", "Nº Lotes"),
            ("numero_adjudicaciones", "Nº Adjudicaciones"),
            ("fichero_origen_atom", "Fichero Origen"),
        ]
        actions = [
            f'<a class="offer-action" href="{escape(build_url(base_path, f"/datos-consolidados/licitaciones/{item["slug"]}"))}">Ver detalle</a>'
            for item in rows
        ]
        heading = "Licitaciones TI Canarias"
        description = (
            "La vista replica la hoja principal del Excel versionado y expone el expediente, su estado, "
            "el órgano contratante, los importes clave y el fichero `.atom` consolidado visible para trazabilidad."
        )
    elif selected_view == "lotes":
        rows = dataset["lotes"]
        columns = [
            ("id_expediente", "ID Expediente"),
            ("titulo_licitacion", "Título Licitación"),
            ("numero_lote", "Nº Lote"),
            ("nombre_lote", "Nombre Lote"),
            ("importe_sin_iva", "Importe sin IVA (€)"),
            ("importe_con_iva", "Importe con IVA (€)"),
            ("cpvs", "CPVs"),
            ("ubicacion", "Ubicación"),
            ("criterios_adjudicacion", "Criterios Adjudicación"),
        ]
        actions = [
            f'<a class="offer-action" href="{escape(build_url(base_path, f"/datos-consolidados/licitaciones/{item["licitacion_slug"]}"))}">Ver licitación</a>'
            for item in rows
        ]
        heading = "Detalle Lotes"
        description = (
            "La hoja de lotes permite revisar el desglose funcional de cada expediente por lote, "
            "manteniendo importes, ubicación, CPVs y criterios de adjudicación."
        )
    else:
        rows = dataset["adjudicaciones"]
        columns = [
            ("id_expediente", "ID Expediente"),
            ("titulo", "Título"),
            ("fecha_adjudicacion", "Fecha Adjudicación"),
            ("lote", "Lote"),
            ("ganador", "Ganador"),
            ("importe_adjudicacion_sin_iva", "Importe Adj. sin IVA"),
            ("importe_adjudicacion_total", "Importe Adj. Total"),
            ("id_contrato", "ID Contrato"),
            ("fichero_origen_atom", "Fichero Origen"),
        ]
        actions = [
            f'<a class="offer-action" href="{escape(build_url(base_path, f"/datos-consolidados/adjudicaciones/{item["slug"]}"))}">Ver contrato</a>'
            for item in rows
        ]
        heading = "Adjudicaciones"
        description = (
            "La hoja de adjudicaciones expone el resultado contractual visible para la muestra actual, "
            "incluyendo adjudicatario, importes, lote y trazabilidad al origen cuando la licitación asociada la aporta."
        )

    table_html = _dataset_table_html(rows, columns, actions)
    summary = dataset["resumen"]
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{summary["licitaciones"]}</strong>Licitaciones en la muestra</article>
            <article class="metric"><strong>{summary["lotes"]}</strong>Lotes visibles</article>
            <article class="metric"><strong>{summary["adjudicaciones"]}</strong>Adjudicaciones visibles</article>
          </div>
          <p class="muted">
            La fuente visible de esta entrega es <code>{escape(dataset["archivo_origen"])}</code>, alineada con <code>{escape(dataset["referencia_funcional"])}</code>.
          </p>
          {tabs}
          <p>{description}</p>
        </div>
        {table_html}
      </section>
    """
    return _page_template(
        "Licican | Datos consolidados TI Canarias",
        heading,
        "Release 7 · PB-012 · Excel funcional visible en la aplicación",
        (
            "Licican expone aquí la misma estructura funcional que el Excel versionado de licitaciones TI Canarias, "
            "con pestañas separadas para licitaciones, lotes y adjudicaciones."
        ),
        content,
        current_path="/datos-consolidados",
        base_path=base_path,
    )


def _licitacion_excel_detail_html_response(slug: str, base_path: str = "") -> str | None:
    detail = build_licitacion_detail(slug)
    if detail is None:
        return None

    rows = [
        ("ID Expediente", detail["id_expediente"]),
        ("Estado", detail["estado"]),
        ("Órgano Contratación", detail["organo_contratacion"]),
        ("Importe estimado", detail["importe_estimado"]),
        ("Importe con IVA", detail["importe_con_iva"]),
        ("Importe sin IVA", detail["importe_sin_iva"]),
        ("CPVs Informáticos", detail["cpvs_informaticos"]),
        ("Ubicación", detail["ubicacion"]),
        ("Procedimiento", detail["procedimiento"]),
        ("Plazo Presentación", detail["plazo_presentacion"]),
        ("Nº Lotes", detail["numero_lotes"]),
        ("Nº Adjudicaciones", detail["numero_adjudicaciones"]),
        ("Fecha Actualización", detail["fecha_actualizacion"]),
        ("Fichero .atom origen", detail["fichero_origen_atom"]),
    ]
    table_rows = "".join(
        f"<tr><th>{escape(label)}</th><td>{escape(_display_value(value))}</td></tr>" for label, value in rows
    )
    placsp_link = detail["enlace_placsp"]
    extra_link = (
        f'<p><a class="offer-action" href="{escape(str(placsp_link))}" target="_blank" rel="noopener noreferrer">Abrir expediente en PLACSP</a></p>'
        if placsp_link
        else ""
    )
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <p><a href="{escape(build_url(base_path, '/datos-consolidados?vista=licitaciones'))}">Volver a Licitaciones TI Canarias</a></p>
          <div class="table-wrap">
            <table>
              <tbody>
                {table_rows}
              </tbody>
            </table>
          </div>
          {extra_link}
        </div>
      </section>
    """
    return _page_template(
        "Licican | Detalle de licitación consolidada",
        str(detail["titulo"]),
        "PB-012 · Detalle trazable del expediente",
        (
            "La ficha mantiene visible la correspondencia funcional con el Excel de referencia y deja explícito el fichero `.atom` "
            "que alimenta la versión consolidada mostrada al usuario."
        ),
        content,
        current_path="/datos-consolidados",
        base_path=base_path,
    )


def _adjudicacion_excel_detail_html_response(slug: str, base_path: str = "") -> str | None:
    detail = build_adjudicacion_detail(slug)
    if detail is None:
        return None

    rows = [
        ("ID Expediente", detail["id_expediente"]),
        ("Resultado", detail["resultado"]),
        ("Fecha Adjudicación", detail["fecha_adjudicacion"]),
        ("Lote", detail["lote"]),
        ("Ganador", detail["ganador"]),
        ("NIF Ganador", detail["nif_ganador"]),
        ("Ciudad Ganador", detail["ciudad_ganador"]),
        ("País", detail["pais"]),
        ("Importe Adj. sin IVA", detail["importe_adjudicacion_sin_iva"]),
        ("Importe Adj. Total", detail["importe_adjudicacion_total"]),
        ("Ofertas Recibidas", detail["ofertas_recibidas"]),
        ("Ofertas PYME", detail["ofertas_pyme"]),
        ("PYME Adjudicatario", detail["pyme_adjudicatario"]),
        ("ID Contrato", detail["id_contrato"]),
        ("Fecha Contrato", detail["fecha_contrato"]),
        ("Fichero .atom origen", detail["fichero_origen_atom"]),
    ]
    table_rows = "".join(
        f"<tr><th>{escape(label)}</th><td>{escape(_display_value(value))}</td></tr>" for label, value in rows
    )
    licitacion_link = ""
    if detail["licitacion_slug"] is not None:
        licitacion_link = (
            f'<p><a class="offer-action" href="{escape(build_url(base_path, f"/datos-consolidados/licitaciones/{detail["licitacion_slug"]}"))}">'
            "Ver licitación asociada</a></p>"
        )
    content = f"""
      <section class="panel">
        <div class="panel-body">
          <p><a href="{escape(build_url(base_path, '/datos-consolidados?vista=adjudicaciones'))}">Volver a Adjudicaciones</a></p>
          <p>{escape(_display_value(detail["descripcion"]))}</p>
          <div class="table-wrap">
            <table>
              <tbody>
                {table_rows}
              </tbody>
            </table>
          </div>
          {licitacion_link}
        </div>
      </section>
    """
    return _page_template(
        "Licican | Detalle de adjudicación consolidada",
        str(detail["titulo"]),
        "PB-012 · Contrato adjudicado con trazabilidad",
        (
            "Esta ficha deja visible el resultado contractual de la muestra actual y, cuando existe correspondencia con la licitación, "
            "hereda la trazabilidad del fichero `.atom` origen."
        ),
        content,
        current_path="/datos-consolidados",
        base_path=base_path,
    )


def _catalog_html_response(filters: CatalogFilters | None = None, page: int = 1, base_path: str = "") -> str:
    catalog = build_catalog(filters=filters, page=page)
    opportunities = catalog["oportunidades"]
    active_filters = catalog["filtros_activos"]
    available_filters = catalog["filtros_disponibles"]
    validation_error = catalog.get("error_validacion")
    pagination = catalog["paginacion"]
    uses_atom_consolidation = catalog["referencia_funcional"] == "PB-011"
    coverage_label = "Snapshots .atom consolidados" if uses_atom_consolidation else "Fuentes oficiales MVP aplicadas"
    coverage_note = (
        "El catálogo consolida todos los snapshots `.atom` versionados presentes en `data/`, "
        "aplica el criterio conjunto Canarias + CPV TI de <code>PB-011</code> y conserva trazabilidad al fichero origen vigente."
        if uses_atom_consolidation
        else (
            "El catálogo reutiliza la cobertura MVP de <code>PB-007</code>, la clasificación auditable de <code>PB-006</code> "
            "y la prioridad de fuentes reales oficiales de <code>PB-009</code>. "
            "No representa todavía cobertura total del ecosistema canario ni habilita alertas o pipeline."
        )
    )
    filter_form = f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Filtros funcionales</h2>
          <form method="get" action="{escape(build_url(base_path, '/'))}">
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
              <a class="button-link" href="{escape(build_url(base_path, '/'))}">Limpiar filtros</a>
            </div>
          </form>
          {_active_filter_badges(active_filters)}
          {_validation_note_html(validation_error)}
          {_status_note_html(_pagination_adjustment_message(pagination), "warn")}
        </div>
      </section>
    """

    if opportunities:
        rows = "\n".join(
            (
                "<tr>"
                f'<td data-label="Oferta"><div class="offer-cell"><a class="offer-link" href="{escape(build_url(base_path, _detail_url(item["id"])))}">{escape(item["titulo"])}</a><a class="offer-action" href="{escape(build_url(base_path, _detail_url(item["id"])))}">Ver oferta concreta</a></div></td>'
                f'<td data-label="Organismo">{escape(item["organismo"])}</td>'
                f'<td data-label="Ubicación">{escape(item["ubicacion"])}</td>'
                f'<td data-label="Procedimiento">{escape(item["procedimiento"] or "No informado")}</td>'
                f'<td data-label="Presupuesto">{escape(_format_budget(item["presupuesto"]))}</td>'
                f'<td data-label="Publicación oficial">{escape(item["fecha_publicacion_oficial"])}</td>'
                f'<td data-label="Fecha límite">{escape(item["fecha_limite"])}</td>'
                f'<td data-label="Estado">{escape(item["estado"])}</td>'
                f'<td data-label="Fuente oficial"><a class="source-link" href="{escape(item["url_fuente_oficial"])}" target="_blank" rel="noopener noreferrer">{escape(item["fuente_oficial"])}</a></td>'
                "</tr>"
            )
            for item in opportunities
        )
        catalog_panel = f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{catalog["total_oportunidades_catalogo"]}</strong>Oportunidades TI visibles</article>
            <article class="metric"><strong>{len(catalog["cobertura_aplicada"])}</strong>{coverage_label}</article>
            <article class="metric"><strong>{catalog["total_oportunidades_visibles"]}</strong>Oportunidades TI antes de filtrar</article>
          </div>
          {_pagination_controls_html(base_path, active_filters, pagination)}
          <p class="muted">
            {coverage_note}
          </p>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Oferta</th>
                <th>Organismo</th>
                <th>Ubicación</th>
                <th>Procedimiento</th>
                <th>Presupuesto</th>
                <th>Publicación oficial</th>
                <th>Fecha límite</th>
                <th>Estado</th>
                <th>Fuente oficial</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
        <div class="panel-body">
          {_pagination_controls_html(base_path, active_filters, pagination)}
        </div>
      </section>
        """
    else:
        message = (
            "No hay resultados con los filtros activos."
            if active_filters and validation_error is None
            else (
                "No hay oportunidades TI disponibles en los snapshots `.atom` consolidados en este momento."
                if uses_atom_consolidation
                else "No hay oportunidades TI disponibles dentro de la cobertura MVP en este momento."
            )
        )
        catalog_panel = f"""
      <section class="note">
        {escape(message)}
      </section>
        """

    content = f"""
      <section class="note">
        <strong>Datos consolidados visibles del Excel</strong><br />
        La aplicación incorpora una superficie funcional alineada con <code>data/licitaciones_ti_canarias.xlsx</code> en las pestañas
        <strong>Licitaciones TI Canarias</strong>, <strong>Detalle Lotes</strong> y <strong>Adjudicaciones</strong>.
        <a class="button-link" href="{escape(build_url(base_path, '/datos-consolidados'))}">Abrir datos consolidados</a>
      </section>
      {filter_form}
      <section class="note">
        <strong>Alertas tempranas del MVP</strong><br />
        Puedes guardar una alerta con estos mismos criterios desde <a href="{escape(build_url(base_path, '/alertas'))}">la gestión de alertas</a>.
        {"<a class=\"button-link\" href=\"" + escape(build_url(base_path, '/alertas')) + ("?" + escape(_alert_filters_query(active_filters)) if active_filters else "") + "\">Guardar estos criterios como alerta</a>" if active_filters else ""}
      </section>
      {catalog_panel}

      <p class="note">
        Referencia funcional activa: <code>{escape(catalog["referencia_funcional"])}</code>.
        Cada registro mantiene visible su fuente oficial, enlace oficial, fecha de publicación y estado oficial para facilitar verificación por <code>qa-teams</code>.
      </p>
    """
    return _page_template(
        "Licican | Catálogo inicial de oportunidades TI",
        "Catálogo inicial de oportunidades TI de Canarias",
        "Release 6 · PB-011 · Consolidacion funcional trazable",
        (
            "Licican muestra aquí un catálogo consultable obtenido a partir de todos los snapshots `.atom` versionados presentes en `data/`. "
            "Solo se publican registros que cumplen simultáneamente criterio geográfico Canarias y criterio TI por CPV, con fuente oficial visible."
        ),
        content,
        current_path="/",
        base_path=base_path,
    )


def _alert_summary_text(filters: dict[str, object]) -> str:
    labels = {
        "palabra_clave": "Palabra clave",
        "presupuesto_min": "Presupuesto mínimo",
        "presupuesto_max": "Presupuesto máximo",
        "procedimiento": "Procedimiento",
        "ubicacion": "Ubicación",
    }
    if not filters:
        return "Sin criterios informados"
    return " · ".join(f"{labels[key]}: {value}" for key, value in filters.items())


def _alerts_html_response(
    base_path: str = "",
    form_filters: CatalogFilters | None = None,
    form_error: str | None = None,
    status_message: str | None = None,
) -> str:
    reference, alerts = load_alerts(resolve_alerts_path())
    catalog = build_catalog()
    available_filters = catalog["filtros_disponibles"]
    summary = summarize_alerts(alerts)
    form_active_filters = (form_filters or CatalogFilters()).normalized().active_filters()

    create_form = f"""
      <section class="panel">
        <div class="panel-body">
          <h2>Crear alerta</h2>
          <p class="muted">
            La alerta reutiliza exactamente los mismos criterios funcionales del catálogo.
            En este MVP registra coincidencias internas visibles, sin notificación saliente.
          </p>
          {_status_note_html(status_message, "ok")}
          {_status_note_html(form_error, "warn")}
          <form method="post" action="{escape(build_url(base_path, '/alertas'))}">
            <div class="filters">
              <div>
                <label for="alerta_palabra_clave">Palabra clave</label>
                <input id="alerta_palabra_clave" name="palabra_clave" type="text" value="{escape(str(form_active_filters.get("palabra_clave", "")))}" placeholder="backup, licencias, redes..." />
              </div>
              <div>
                <label for="alerta_presupuesto_min">Presupuesto mínimo</label>
                <input id="alerta_presupuesto_min" name="presupuesto_min" type="number" min="0" step="1" value="{escape(str(form_active_filters.get("presupuesto_min", "")))}" />
              </div>
              <div>
                <label for="alerta_presupuesto_max">Presupuesto máximo</label>
                <input id="alerta_presupuesto_max" name="presupuesto_max" type="number" min="0" step="1" value="{escape(str(form_active_filters.get("presupuesto_max", "")))}" />
              </div>
              <div>
                <label for="alerta_procedimiento">Procedimiento</label>
                <select id="alerta_procedimiento" name="procedimiento">
                  <option value="">Todos</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if form_active_filters.get("procedimiento") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["procedimientos"]
                  )}
                </select>
              </div>
              <div>
                <label for="alerta_ubicacion">Ubicación</label>
                <select id="alerta_ubicacion" name="ubicacion">
                  <option value="">Todas</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if form_active_filters.get("ubicacion") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["ubicaciones"]
                  )}
                </select>
              </div>
            </div>
            <div class="filter-actions">
              <button type="submit">Guardar alerta</button>
              <a class="button-link" href="{escape(build_url(base_path, '/alertas'))}">Limpiar formulario</a>
            </div>
          </form>
        </div>
      </section>
    """

    if alerts:
        alert_sections = []
        for alert in alerts:
            alert_filters = alert.filtros.active_filters()
            coincidence_items = "".join(
                (
                    "<li>"
                    f'<a class="offer-link" href="{escape(build_url(base_path, _detail_url(match.id)))}">{escape(match.titulo)}</a>'
                    f" · {escape(match.organismo)} · {escape(match.estado)}"
                    "</li>"
                )
                for match in alert.coincidencias
            ) or "<li>Sin coincidencias accionables registradas en este momento.</li>"
            alert_sections.append(
                f"""
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{'Activa' if alert.activa else 'Inactiva'}</strong>Estado actual</article>
            <article class="metric"><strong>{len(alert.coincidencias)}</strong>Coincidencias accionables</article>
            <article class="metric"><strong>{escape(alert.id)}</strong>Identificador interno</article>
          </div>
          <p><strong>Criterios actuales:</strong> {escape(_alert_summary_text(alert_filters))}</p>
          <p class="muted">Creada: {escape(alert.creada_en)} · Última actualización: {escape(alert.actualizada_en)}</p>
          {_active_filter_badges(alert_filters)}
          <h3>Editar alerta</h3>
          <form method="post" action="{escape(build_url(base_path, f'/alertas/{alert.id}/editar'))}">
            <div class="filters">
              <div>
                <label for="{escape(alert.id)}-palabra_clave">Palabra clave</label>
                <input id="{escape(alert.id)}-palabra_clave" name="palabra_clave" type="text" value="{escape(str(alert_filters.get("palabra_clave", "")))}" />
              </div>
              <div>
                <label for="{escape(alert.id)}-presupuesto_min">Presupuesto mínimo</label>
                <input id="{escape(alert.id)}-presupuesto_min" name="presupuesto_min" type="number" min="0" step="1" value="{escape(str(alert_filters.get("presupuesto_min", "")))}" />
              </div>
              <div>
                <label for="{escape(alert.id)}-presupuesto_max">Presupuesto máximo</label>
                <input id="{escape(alert.id)}-presupuesto_max" name="presupuesto_max" type="number" min="0" step="1" value="{escape(str(alert_filters.get("presupuesto_max", "")))}" />
              </div>
              <div>
                <label for="{escape(alert.id)}-procedimiento">Procedimiento</label>
                <select id="{escape(alert.id)}-procedimiento" name="procedimiento">
                  <option value="">Todos</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if alert_filters.get("procedimiento") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["procedimientos"]
                  )}
                </select>
              </div>
              <div>
                <label for="{escape(alert.id)}-ubicacion">Ubicación</label>
                <select id="{escape(alert.id)}-ubicacion" name="ubicacion">
                  <option value="">Todas</option>
                  {"".join(
                      f'<option value="{escape(item)}"' + (' selected' if alert_filters.get("ubicacion") == item else '') + f'>{escape(item)}</option>'
                      for item in available_filters["ubicaciones"]
                  )}
                </select>
              </div>
            </div>
            <div class="filter-actions">
              <button type="submit">Actualizar alerta</button>
            </div>
          </form>
          {f'<form method="post" action="{escape(build_url(base_path, f"/alertas/{alert.id}/desactivar"))}"><div class="filter-actions"><button type="submit">Desactivar alerta</button></div></form>' if alert.activa else '<p class="muted">La alerta está desactivada y se conserva solo para trazabilidad del MVP.</p>'}
          <h3>Coincidencias internas registradas</h3>
          <ul>{coincidence_items}</ul>
        </div>
      </section>
                """
            )
        alert_list = "".join(alert_sections)
    else:
        alert_list = """
      <section class="note">
        Todavía no hay alertas registradas. Guarda la primera para dejar visible el criterio activo del MVP.
      </section>
        """

    content = f"""
      {create_form}
      <section class="panel">
        <div class="panel-body">
          <div class="summary">
            <article class="metric"><strong>{summary["total_alertas"]}</strong>Alertas totales</article>
            <article class="metric"><strong>{summary["alertas_activas"]}</strong>Alertas activas</article>
            <article class="metric"><strong>{summary["coincidencias_activas"]}</strong>Coincidencias accionables activas</article>
          </div>
          <p class="muted">
            Referencia funcional activa: <code>{escape(reference)}</code>.
            Esta vista no envía notificaciones; solo registra coincidencias internas accionables del MVP.
          </p>
        </div>
      </section>
      {alert_list}
    """
    return _page_template(
        "Licican | Alertas tempranas del MVP",
        "Gestión de alertas tempranas",
        "Release 2 · PB-004 · Registro interno de anticipación",
        (
            "Licican permite guardar criterios persistentes para dejar visible qué oportunidades TI deben seguirse sin búsqueda manual recurrente. "
            "En esta primera entrega las coincidencias quedan registradas en la propia aplicación como soporte interno del MVP."
        ),
        content,
        current_path="/alertas",
        base_path=base_path,
    )


def _catalog_data_error_html_response(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Fuente temporalmente no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>
            La aplicacion no ha podido consultar la fuente de datos operativa configurada para el catalogo.
            Revisa la conexion a PostgreSQL o la configuracion del backend antes de reintentar.
          </p>
          <p>
            Ruta afectada del catalogo: <code>{escape(build_url(base_path, '/api/oportunidades'))}</code>
          </p>
        </div>
      </section>
    """
    return _page_template(
        "Licican | Catalogo temporalmente no disponible",
        "Catalogo temporalmente no disponible",
        "Servicio de datos no disponible",
        "El catalogo y el detalle requieren acceso a la fuente de datos configurada para la aplicacion.",
        content,
        current_path="/",
        base_path=base_path,
    )


def _detail_html_response(opportunity_id: str, base_path: str = "") -> str | None:
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
          <p><a href="{escape(build_url(base_path, '/'))}">Volver al catalogo</a></p>
          <div class="summary">
            <article class="metric"><strong>{escape(str(detail["estado"]))}</strong>Estado oficial visible</article>
            <article class="metric"><strong>{escape(str(detail["fecha_limite"]))}</strong>Fecha limite visible</article>
            <article class="metric"><strong>{escape(_format_budget(detail["presupuesto"]))}</strong>Presupuesto visible</article>
          </div>
          <div class="table-wrap">
            <table>
              <tbody>
                <tr><th>Organismo convocante</th><td>{escape(str(detail["organismo"]))}</td></tr>
                <tr><th>Ubicacion</th><td>{escape(str(detail["ubicacion"]))}</td></tr>
                <tr><th>Procedimiento</th><td>{escape(str(detail["procedimiento"] or "No informado"))}</td></tr>
                <tr><th>Presupuesto</th><td>{escape(_format_budget(detail["presupuesto"]))}</td></tr>
                <tr><th>Publicación oficial</th><td>{escape(str(detail["fecha_publicacion_oficial"]))}</td></tr>
                <tr><th>Fecha limite</th><td>{escape(str(detail["fecha_limite"]))}</td></tr>
                <tr><th>Estado oficial del expediente</th><td>{escape(str(detail["estado"]))}</td></tr>
                <tr><th>Fuente oficial</th><td><a class="source-link" href="{escape(str(detail["url_fuente_oficial"]))}" target="_blank" rel="noopener noreferrer">{escape(str(detail["fuente_oficial"]))}</a></td></tr>
                <tr><th>Fichero .atom origen</th><td>{escape(str(detail["fichero_origen_atom"] or "No informado"))}</td></tr>
              </tbody>
            </table>
          </div>
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
        "Licican | Ficha de detalle de licitacion",
        str(detail["titulo"]),
        "Release 1 · PB-002 · Ficha resumida verificable",
        (
            "La ficha resume los datos criticos del expediente y mantiene visible la fuente oficial, la fecha de publicación y el estado oficial. "
            "Cuando existe una rectificacion o modificacion publicada por el origen, se muestra el ultimo dato oficial visible."
        ),
        update_panel + latest_fields,
        current_path=f"/oportunidades/{quote(opportunity_id)}",
        base_path=base_path,
    )


def _classification_html_response(base_path: str = "") -> str:
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
        "Licican | Clasificación TI auditable",
        "Clasificación TI auditable",
        "Release 0 · PB-006 · Regla TI verificable",
        (
            "Licican fija aquí la regla funcional mínima para decidir qué oportunidades son TI, "
            "cuáles deben excluirse y qué expedientes requieren revisión adicional antes de aparecer en el catálogo."
        ),
        content,
        current_path="/clasificacion-ti",
        base_path=base_path,
    )
def application(environ, start_response):
    base_path = resolve_base_path()
    path = _resolve_request_path(environ, base_path)
    method = (environ.get("REQUEST_METHOD", "GET") or "GET").upper()
    filters = _parse_catalog_filters(environ)
    page = _parse_catalog_page(environ)

    if path == "/api/datos-consolidados":
        body = b"".join(json_body(load_canarias_dataset()))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/alertas":
        reference, alerts = load_alerts(resolve_alerts_path())
        payload = {
            "referencia_funcional": reference,
            "summary": summarize_alerts(alerts),
            "alerts": [alert.to_payload() for alert in alerts],
        }
        body = b"".join(json_body(payload))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/alertas" and method == "POST":
        form_filters = _parse_filters_from_multidict(read_form_data(environ))
        try:
            create_alert(form_filters, path=resolve_alerts_path())
        except ValueError as exc:
            body = b"".join(html_body(_alerts_html_response(base_path, form_filters, str(exc))))
            return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", body)
        except CatalogDataSourceError as exc:
            body = b"".join(html_body(_catalog_data_error_html_response(base_path, str(exc))))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", body)
        return send_redirect(start_response, build_url(base_path, "/alertas") + "?mensaje=Alerta+creada+y+activa")

    if path.startswith("/alertas/") and method == "POST":
        segments = path.strip("/").split("/")
        if len(segments) == 3 and segments[2] == "editar":
            alert_id = segments[1]
            form_filters = _parse_filters_from_multidict(read_form_data(environ))
            try:
                update_alert(alert_id, form_filters, path=resolve_alerts_path())
            except ValueError as exc:
                body = b"".join(html_body(_alerts_html_response(base_path, None, f"No se ha actualizado {alert_id}. {exc}")))
                return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", body)
            except CatalogDataSourceError as exc:
                body = b"".join(html_body(_catalog_data_error_html_response(base_path, str(exc))))
                return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", body)
            except KeyError:
                body = b"No encontrado"
                return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
            return send_redirect(start_response, build_url(base_path, "/alertas") + "?mensaje=Alerta+actualizada")
        if len(segments) == 3 and segments[2] == "desactivar":
            alert_id = segments[1]
            try:
                deactivate_alert(alert_id, path=resolve_alerts_path())
            except KeyError:
                body = b"No encontrado"
                return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
            return send_redirect(start_response, build_url(base_path, "/alertas") + "?mensaje=Alerta+desactivada")

    if path.startswith("/api/oportunidades/"):
        opportunity_id = path.removeprefix("/api/oportunidades/")
        try:
            detail = build_opportunity_detail(opportunity_id)
        except CatalogDataSourceError as exc:
            body = b"".join(json_body({"error": str(exc)}))
            return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", body)
        if detail is None:
            body = b"No encontrado"
            return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(json_body(detail))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/oportunidades":
        try:
            payload = build_catalog(filters=filters, page=page)
        except CatalogDataSourceError as exc:
            body = b"".join(json_body({"error": str(exc)}))
            return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", body)
        status = "400 Bad Request" if payload["error_validacion"] else "200 OK"
        body = b"".join(json_body(payload))
        return send_response(start_response, status, "application/json; charset=utf-8", body)

    if path == "/api/fuentes":
        sources = load_source_coverage()
        payload = {
            "sources": [source.__dict__ for source in sources],
            "summary": summary_by_status(sources),
        }
        body = b"".join(json_body(payload))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/api/fuentes-prioritarias":
        reference, sources, out_of_scope = load_real_source_prioritization()
        payload = {
            "referencia_funcional": reference,
            "sources": [source.__dict__ for source in sources],
            "summary": summarize_prioritization(sources),
            "fuera_de_alcance": list(out_of_scope),
        }
        body = b"".join(json_body(payload))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

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
        body = b"".join(json_body(payload))
        return send_response(start_response, "200 OK", "application/json; charset=utf-8", body)

    if path == "/clasificacion-ti":
        body = b"".join(html_body(_classification_html_response(base_path)))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/cobertura-fuentes":
        body = b"".join(html_body(_coverage_html_response(base_path)))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/priorizacion-fuentes-reales":
        body = b"".join(html_body(_real_source_prioritization_html_response(base_path)))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/alertas":
        query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)
        status_message = (query.get("mensaje") or [None])[0]
        try:
            content = _alerts_html_response(base_path, filters, status_message=status_message)
        except CatalogDataSourceError as exc:
            body = b"".join(html_body(_catalog_data_error_html_response(base_path, str(exc))))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", body)
        body = b"".join(html_body(content))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/datos-consolidados":
        query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)
        current_view = (query.get("vista") or ["licitaciones"])[0]
        body = b"".join(html_body(_datos_consolidados_html_response(current_view, base_path)))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path.startswith("/datos-consolidados/licitaciones/"):
        slug = path.removeprefix("/datos-consolidados/licitaciones/")
        content = _licitacion_excel_detail_html_response(slug, base_path)
        if content is None:
            body = b"No encontrado"
            return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(html_body(content))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path.startswith("/datos-consolidados/adjudicaciones/"):
        slug = path.removeprefix("/datos-consolidados/adjudicaciones/")
        content = _adjudicacion_excel_detail_html_response(slug, base_path)
        if content is None:
            body = b"No encontrado"
            return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(html_body(content))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path.startswith("/oportunidades/"):
        opportunity_id = path.removeprefix("/oportunidades/")
        try:
            content = _detail_html_response(opportunity_id, base_path)
        except CatalogDataSourceError as exc:
            body = b"".join(html_body(_catalog_data_error_html_response(base_path, str(exc))))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", body)
        if content is None:
            body = b"No encontrado"
            return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)
        body = b"".join(html_body(content))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    if path == "/":
        try:
            content = _catalog_html_response(filters, page, base_path)
        except CatalogDataSourceError as exc:
            body = b"".join(html_body(_catalog_data_error_html_response(base_path, str(exc))))
            return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", body)
        body = b"".join(html_body(content))
        return send_response(start_response, "200 OK", "text/html; charset=utf-8", body)

    body = b"No encontrado"
    return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", body)


def main() -> None:
    base_path = resolve_base_path()
    host = resolve_host()
    port = resolve_port()
    with make_server(host, port, application) as httpd:
        print(f"Servidor disponible en http://{host}:{port}{base_path or '/'}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("\nServidor detenido de forma controlada.")


if __name__ == "__main__":
    main()
