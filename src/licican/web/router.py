from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import parse_qs

from licican.access import AccessContext, has_capability, resolve_access_context
from licican.alerts import create_alert, deactivate_alert, filter_alerts_by_user, load_alerts, summarize_alerts, update_alert
from licican.canarias_dataset import build_adjudicacion_detail, build_licitacion_detail, load_canarias_dataset
from licican.config import normalize_base_path, resolve_alerts_path, resolve_base_path, resolve_pipeline_path
from licican.opportunity_catalog import CatalogDataSourceError, build_catalog, build_opportunity_detail
from licican.pipeline import add_opportunity_to_pipeline, build_pipeline_payload, update_pipeline_entry_status
from licican.real_source_prioritization import load_real_source_prioritization, summarize_prioritization
from licican.shared.filters import CatalogFilters
from licican.source_coverage import load_source_coverage, summary_by_status
from licican.ti_classification import audit_examples, load_rule_set
from licican.users import UsersDatabaseError, UserFilters, build_users_payload, change_user_state, create_user, resend_invitation, reset_access, update_user
from licican.web.responses import build_url, html_body, json_body, read_form_data, send_redirect, send_response
from licican.web.templates.alerts import render_alerts
from licican.web.templates.base import page_template
from licican.web.templates.catalog import render_catalog
from licican.web.templates.classification import render_classification
from licican.web.templates.coverage import render_coverage
from licican.web.templates.dataset import render_datos_consolidados
from licican.web.templates.detail import render_adjudicacion_detail, render_licitacion_detail, render_opportunity_detail
from licican.web.templates.kpis import render_kpis
from licican.web.templates.permissions import render_permissions_matrix
from licican.web.templates.pipeline import render_pipeline
from licican.web.templates.prioritization import render_prioritization
from licican.web.templates.users import render_users

STATIC_DIR = Path(__file__).resolve().parent / "static"
Route = namedtuple("Route", ["method", "pattern", "handler"])


@dataclass(frozen=True)
class Request:
    environ: dict[str, object]
    method: str
    path: str
    base_path: str
    query: dict[str, list[str]]
    access_context: AccessContext


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


def _parse_catalog_filters(request: Request) -> CatalogFilters:
    return _parse_filters_from_multidict(request.query)


def _parse_catalog_page(request: Request) -> int:
    candidates = request.query.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def _parse_catalog_page_size(request: Request) -> int:
    candidates = request.query.get("page_size")
    if not candidates:
        return 10
    try:
        page_size = int(candidates[0])
    except ValueError:
        return 10
    return page_size if page_size in {5, 10, 25, 50} else 10


def _parse_user_filters(request: Request) -> UserFilters:
    query = request.query
    return UserFilters(
        busqueda=(query.get("busqueda") or [None])[0],
        estado=(query.get("estado") or [None])[0],
        rol=(query.get("rol") or [None])[0],
        superficie=(query.get("superficie") or [None])[0],
    )


def _parse_users_page(request: Request) -> int:
    candidates = request.query.get("page")
    if not candidates:
        return 1
    try:
        return int(candidates[0])
    except ValueError:
        return 1


def _parse_users_page_size(request: Request) -> int:
    candidates = request.query.get("page_size")
    if not candidates:
        return 10
    try:
        page_size = int(candidates[0])
    except ValueError:
        return 10
    return page_size if page_size in {5, 10, 25, 50} else 10


def _resolve_request_path(environ: dict[str, object], base_path: str) -> str:
    raw_path = str(environ.get("PATH_INFO", "/") or "/")
    script_name = normalize_base_path(str(environ.get("SCRIPT_NAME") or "")) or base_path
    if script_name and raw_path.startswith(script_name):
        raw_path = raw_path[len(script_name):] or "/"
    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"
    return raw_path or "/"


def _not_found(start_response) -> list[bytes]:
    return send_response(start_response, "404 Not Found", "text/plain; charset=utf-8", b"No encontrado")


def _catalog_data_error_html(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Fuente temporalmente no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La aplicacion no ha podido consultar la fuente de datos operativa configurada para el catalogo. Revisa la conexion a PostgreSQL o la configuracion del backend antes de reintentar.</p>
          <p>Ruta afectada del catalogo: <code>{escape(build_url(base_path, '/api/oportunidades'))}</code></p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Catalogo temporalmente no disponible",
        "Catalogo temporalmente no disponible",
        "Servicio de datos no disponible",
        "El catalogo y el detalle requieren acceso a la fuente de datos configurada para la aplicacion.",
        content,
        current_path="/",
        base_path=base_path,
    )


def _access_denied_html(request: Request, capability: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Acceso bloqueado por permisos</strong><br />
        El rol activo <strong>{escape(request.access_context.role_label)}</strong> no puede ejecutar la accion requerida para <code>{escape(capability)}</code>.
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La aplicacion mantiene visibles solo las superficies compatibles con el rol actual y bloquea de forma consistente los intentos de gestion no autorizados.</p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Acceso restringido",
        "Acceso restringido por rol",
        "PB-013 · Restriccion consistente de acciones",
        "La accion solicitada no esta disponible para el rol funcional activo.",
        content,
        current_path=request.path,
        base_path=request.base_path,
        access_context=request.access_context,
    )


def _deny_html(request: Request, start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "text/html; charset=utf-8",
        b"".join(html_body(_access_denied_html(request, capability))),
    )


def _deny_json(start_response, capability: str) -> list[bytes]:
    return send_response(
        start_response,
        "403 Forbidden",
        "application/json; charset=utf-8",
        b"".join(json_body({"error": f"Acceso restringido por permisos para {capability}."})),
    )


def _visible_alerts(request: Request, alerts):
    return alerts if request.access_context.is_admin else filter_alerts_by_user(alerts, request.access_context.user_id)


def _visible_pipeline_payload(request: Request) -> dict[str, object]:
    return build_pipeline_payload(
        path=resolve_pipeline_path(),
        usuario_id=None if request.access_context.is_admin else request.access_context.user_id,
    )


def _visible_users_payload(request: Request, selected_user_id: str | None = None) -> dict[str, object]:
    return build_users_payload(
        filters=_parse_user_filters(request),
        page=_parse_users_page(request),
        page_size=_parse_users_page_size(request),
        selected_user_id=selected_user_id,
    )


def _users_data_error_html(base_path: str, message: str) -> str:
    content = f"""
      <section class="note note-warning">
        <strong>Base de datos de usuarios no disponible</strong><br />
        {escape(message)}
      </section>
      <section class="panel">
        <div class="panel-body">
          <p>La gestion de usuarios depende de PostgreSQL y no puede renderizarse mientras la conexion no responda.</p>
        </div>
      </section>
    """
    return page_template(
        "Licican | Usuarios temporalmente no disponibles",
        "Usuarios temporalmente no disponibles",
        "Servicio de datos no disponible",
        "El modulo de gestion de usuarios requiere acceso a la base de datos configurada.",
        content,
        current_path="/usuarios",
        base_path=base_path,
    )


def handle_static(request: Request, start_response, filename: str) -> list[bytes]:
    relative_path = filename
    static_path = (STATIC_DIR / relative_path).resolve()
    if not str(static_path).startswith(str(STATIC_DIR.resolve())) or not static_path.is_file():
        return _not_found(start_response)
    content_type = "text/css; charset=utf-8" if static_path.suffix == ".css" else "application/octet-stream"
    return send_response(start_response, "200 OK", content_type, static_path.read_bytes())


def handle_api_dataset(request: Request, start_response) -> list[bytes]:
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(load_canarias_dataset())))


def handle_api_alerts(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return _deny_json(start_response, "view_alerts")
    reference, alerts = load_alerts(resolve_alerts_path())
    visible_alerts = _visible_alerts(request, alerts)
    payload = {"referencia_funcional": reference, "summary": summarize_alerts(visible_alerts), "alerts": [alert.to_payload() for alert in visible_alerts]}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_pipeline(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return _deny_json(start_response, "view_pipeline")
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(_visible_pipeline_payload(request))))


def handle_alerts_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_alerts"):
        return _deny_html(request, start_response, "view_alerts")
    filters = _parse_catalog_filters(request)
    status_message = (request.query.get("mensaje") or [None])[0]
    try:
        reference, alerts = load_alerts(resolve_alerts_path())
        visible_alerts = _visible_alerts(request, alerts)
        available_filters = build_catalog()["filtros_disponibles"]
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, filters.normalized().active_filters(), None, status_message, request.access_context)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_pipeline_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_pipeline"):
        return _deny_html(request, start_response, "view_pipeline")
    status_message = (request.query.get("mensaje") or [None])[0]
    content = render_pipeline(_visible_pipeline_payload(request), request.base_path, None, status_message, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_users_page(request: Request, start_response, id: str | None = None) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_html(request, start_response, "view_users")
    status_message = (request.query.get("mensaje") or [None])[0]
    selected_user_id = id
    try:
        if selected_user_id is None and request.path != "/usuarios":
            selected_user_id = request.path.rsplit("/", 1)[-1]
        payload = _visible_users_payload(request, selected_user_id=selected_user_id)
        content = render_users(payload, request.base_path, None, status_message, request.access_context)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except Exception as exc:
        content = render_users(_visible_users_payload(request), request.base_path, str(exc), status_message, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def _user_form_values(form_data: dict[str, list[str]]) -> dict[str, object]:
    return {
        "nombre": (form_data.get("nombre") or [""])[0],
        "apellidos": (form_data.get("apellidos") or [""])[0],
        "email": (form_data.get("email") or [""])[0],
        "rol_principal": (form_data.get("rol_principal") or [""])[0],
        "estado": (form_data.get("estado") or ["pendiente"])[0],
        "superficies": (form_data.get("superficies") or [""])[0],
        "observaciones_internas": (form_data.get("observaciones_internas") or [""])[0],
    }


def _users_error_response(request: Request, start_response, message: str, status: str = "400 Bad Request", selected_user_id: str | None = None) -> list[bytes]:
    content = render_users(_visible_users_payload(request, selected_user_id=selected_user_id), request.base_path, message, None, request.access_context)
    return send_response(start_response, status, "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_create_user(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    form_data = _user_form_values(read_form_data(request.environ))
    try:
        create_user(
            nombre=str(form_data["nombre"]),
            apellidos=str(form_data["apellidos"]),
            email=str(form_data["email"]),
            rol_principal=str(form_data["rol_principal"]),
            superficies=str(form_data["superficies"]),
            estado=str(form_data["estado"]),
            observaciones_internas=str(form_data["observaciones_internas"]),
        )
    except ValueError as exc:
        return _users_error_response(request, start_response, str(exc))
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/usuarios") + "?mensaje=Usuario+creado+y+registrado")


def handle_update_user(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    form_data = _user_form_values(read_form_data(request.environ))
    try:
        update_user(
            id,
            nombre=str(form_data["nombre"]),
            apellidos=str(form_data["apellidos"]),
            email=str(form_data["email"]),
            rol_principal=str(form_data["rol_principal"]),
            superficies=str(form_data["superficies"]),
            estado=str(form_data["estado"]),
            observaciones_internas=str(form_data["observaciones_internas"]),
        )
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha actualizado {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, f"/usuarios/{id}") + "?mensaje=Usuario+actualizado")


def handle_change_user_state(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado") or [""])[0]
    try:
        change_user_state(id, state)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha actualizado el estado de {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, f"/usuarios/{id}") + "?mensaje=Estado+de+usuario+actualizado")


def handle_resend_user_invitation(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    try:
        resend_invitation(id)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha reenviado la invitacion de {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, f"/usuarios/{id}") + "?mensaje=Invitacion+reenviada")


def handle_reset_user_access(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_users"):
        return _deny_html(request, start_response, "manage_users")
    try:
        reset_access(id)
    except ValueError as exc:
        return _users_error_response(request, start_response, f"No se ha reiniciado el acceso de {id}. {exc}", selected_user_id=id)
    except KeyError:
        return _not_found(start_response)
    except UsersDatabaseError as exc:
        content = _users_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, f"/usuarios/{id}") + "?mensaje=Acceso+reiniciado")



def handle_create_alert(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        create_alert(form_filters, path=resolve_alerts_path(), user_id=request.access_context.user_id)
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        visible_alerts = _visible_alerts(request, alerts)
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, form_filters.normalized().active_filters(), str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+creada+y+activa")


def handle_update_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    form_filters = _parse_filters_from_multidict(read_form_data(request.environ))
    try:
        update_alert(
            id,
            form_filters,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except ValueError as exc:
        reference, alerts = load_alerts(resolve_alerts_path())
        available_filters = build_catalog()["filtros_disponibles"]
        visible_alerts = _visible_alerts(request, alerts)
        summary = summarize_alerts(visible_alerts)
        content = render_alerts(reference, visible_alerts, summary, available_filters, request.base_path, {}, f"No se ha actualizado {id}. {exc}", None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except PermissionError:
        return _deny_html(request, start_response, "manage_alerts")
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+actualizada")


def handle_deactivate_alert(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_alerts"):
        return _deny_html(request, start_response, "manage_alerts")
    try:
        deactivate_alert(
            id,
            path=resolve_alerts_path(),
            user_id=request.access_context.user_id,
            allow_any_owner=request.access_context.is_admin,
        )
    except PermissionError:
        return _deny_html(request, start_response, "manage_alerts")
    except KeyError:
        return _not_found(start_response)
    return send_redirect(start_response, build_url(request.base_path, "/alertas") + "?mensaje=Alerta+desactivada")


def handle_create_pipeline_entry(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return _deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    opportunity_id = (form_data.get("opportunity_id") or [""])[0].strip()
    try:
        _, created = add_opportunity_to_pipeline(opportunity_id, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(_visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _not_found(start_response)

    message = "Oportunidad guardada en el pipeline" if created else "La oportunidad ya estaba guardada en el pipeline"
    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + f"?mensaje={message.replace(' ', '+')}")


def handle_update_pipeline_entry(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "manage_pipeline"):
        return _deny_html(request, start_response, "manage_pipeline")
    form_data = read_form_data(request.environ)
    state = (form_data.get("estado_seguimiento") or [""])[0]
    try:
        update_pipeline_entry_status(id, state, path=resolve_pipeline_path(), usuario_id=request.access_context.user_id)
    except ValueError as exc:
        content = render_pipeline(_visible_pipeline_payload(request), request.base_path, str(exc), None, request.access_context)
        return send_response(start_response, "400 Bad Request", "text/html; charset=utf-8", b"".join(html_body(content)))
    except KeyError:
        return _deny_html(request, start_response, "manage_pipeline")

    return send_redirect(start_response, build_url(request.base_path, "/pipeline") + "?mensaje=Estado+de+pipeline+actualizado")


def handle_api_opportunities(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=_parse_catalog_filters(request),
            page=_parse_catalog_page(request),
            page_size=_parse_catalog_page_size(request),
        )
    except CatalogDataSourceError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    status = "400 Bad Request" if payload["error_validacion"] else "200 OK"
    return send_response(start_response, status, "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_opportunity_detail(request: Request, start_response, id: str) -> list[bytes]:
    try:
        detail = build_opportunity_detail(id)
    except CatalogDataSourceError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    if detail is None:
        return _not_found(start_response)
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(detail)))


def handle_api_sources(request: Request, start_response) -> list[bytes]:
    sources = load_source_coverage()
    payload = {"sources": [source.__dict__ for source in sources], "summary": summary_by_status(sources)}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_prioritized_sources(request: Request, start_response) -> list[bytes]:
    reference, sources, out_of_scope = load_real_source_prioritization()
    payload = {"referencia_funcional": reference, "sources": [source.__dict__ for source in sources], "summary": summarize_prioritization(sources), "fuera_de_alcance": list(out_of_scope)}
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_classification(request: Request, start_response) -> list[bytes]:
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
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_classification_page(request: Request, start_response) -> list[bytes]:
    rules = load_rule_set()
    content = render_classification(rules.referencia_funcional, rules, audit_examples(rules), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_coverage_page(request: Request, start_response) -> list[bytes]:
    sources = load_source_coverage()
    content = render_coverage(sources, summary_by_status(sources), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_prioritization_page(request: Request, start_response) -> list[bytes]:
    reference, sources, out_of_scope = load_real_source_prioritization()
    content = render_prioritization(reference, sources, out_of_scope, summarize_prioritization(sources), request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_dataset_page(request: Request, start_response) -> list[bytes]:
    dataset = load_canarias_dataset()
    selected_view = (request.query.get("vista") or ["licitaciones"])[0]
    selected_view = selected_view if selected_view in {"licitaciones", "lotes", "adjudicaciones"} else "licitaciones"
    if selected_view == "licitaciones":
        rows = dataset["licitaciones"]
        columns = [("id_expediente", "ID Expediente"), ("titulo", "Título"), ("estado", "Estado"), ("organo_contratacion", "Órgano Contratación"), ("importe_sin_iva", "Importe sin IVA"), ("procedimiento", "Procedimiento"), ("plazo_presentacion", "Plazo Presentación"), ("numero_lotes", "Nº Lotes"), ("numero_adjudicaciones", "Nº Adjudicaciones"), ("fichero_origen_atom", "Fichero Origen")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/licitaciones/{item["slug"]}"))}">Ver detalle</a>' for item in rows]
        heading = "Licitaciones TI Canarias"
        description = "La vista replica la hoja principal del Excel versionado y expone el expediente, su estado, el órgano contratante, los importes clave y el fichero `.atom` consolidado visible para trazabilidad."
    elif selected_view == "lotes":
        rows = dataset["lotes"]
        columns = [("id_expediente", "ID Expediente"), ("titulo_licitacion", "Título Licitación"), ("numero_lote", "Nº Lote"), ("nombre_lote", "Nombre Lote"), ("importe_sin_iva", "Importe sin IVA (€)"), ("importe_con_iva", "Importe con IVA (€)"), ("cpvs", "CPVs"), ("ubicacion", "Ubicación"), ("criterios_adjudicacion", "Criterios Adjudicación")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/licitaciones/{item["licitacion_slug"]}"))}">Ver licitación</a>' for item in rows]
        heading = "Detalle Lotes"
        description = "La hoja de lotes permite revisar el desglose funcional de cada expediente por lote, manteniendo importes, ubicación, CPVs y criterios de adjudicación."
    else:
        rows = dataset["adjudicaciones"]
        columns = [("id_expediente", "ID Expediente"), ("titulo", "Título"), ("fecha_adjudicacion", "Fecha Adjudicación"), ("lote", "Lote"), ("ganador", "Ganador"), ("importe_adjudicacion_sin_iva", "Importe Adj. sin IVA"), ("importe_adjudicacion_total", "Importe Adj. Total"), ("id_contrato", "ID Contrato"), ("fichero_origen_atom", "Fichero Origen")]
        actions = [f'<a class="offer-action" href="{escape(build_url(request.base_path, f"/datos-consolidados/adjudicaciones/{item["slug"]}"))}">Ver contrato</a>' for item in rows]
        heading = "Adjudicaciones"
        description = "La hoja de adjudicaciones expone el resultado contractual visible para la muestra actual, incluyendo adjudicatario, importes, lote y trazabilidad al origen cuando la licitación asociada la aporta."
    content = render_datos_consolidados(dataset, selected_view, heading, description, columns, actions, rows, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_licitacion_detail(request: Request, start_response, id: str) -> list[bytes]:
    detail = build_licitacion_detail(id)
    if detail is None:
        return _not_found(start_response)
    content = render_licitacion_detail(detail, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_adjudicacion_detail(request: Request, start_response, id: str) -> list[bytes]:
    detail = build_adjudicacion_detail(id)
    if detail is None:
        return _not_found(start_response)
    content = render_adjudicacion_detail(detail, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_catalog_page(request: Request, start_response) -> list[bytes]:
    try:
        payload = build_catalog(
            filters=_parse_catalog_filters(request),
            page=_parse_catalog_page(request),
            page_size=_parse_catalog_page_size(request),
        )
        content = render_catalog(payload, request.base_path, request.access_context)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_opportunity_detail(request: Request, start_response, id: str) -> list[bytes]:
    try:
        detail = build_opportunity_detail(id)
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))
    if detail is None:
        return _not_found(start_response)
    content = render_opportunity_detail(detail, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_kpis_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_kpis"):
        return _deny_html(request, start_response, "view_kpis")
    try:
        catalog = build_catalog()
        _, alerts = load_alerts(resolve_alerts_path())
    except CatalogDataSourceError as exc:
        content = _catalog_data_error_html(request.base_path, str(exc))
        return send_response(start_response, "503 Service Unavailable", "text/html; charset=utf-8", b"".join(html_body(content)))

    visible_alerts = _visible_alerts(request, alerts)
    alerts_summary = summarize_alerts(visible_alerts)
    pipeline_payload = _visible_pipeline_payload(request)
    payload = {
        "rol_activo": request.access_context.role_label,
        "alcance": "Indicadores globales" if request.access_context.is_admin else "Indicadores del contexto propio del colaborador",
        "indicadores": [
            {
                "nombre": "Cobertura visible",
                "valor": catalog["total_oportunidades_catalogo"],
                "lectura": "Oportunidades TI actualmente visibles en el catalogo consultable.",
                "alcance": "Consulta general del producto.",
            },
            {
                "nombre": "Adopcion de alertas",
                "valor": alerts_summary["alertas_activas"],
                "lectura": "Alertas activas dentro del alcance permitido por el rol.",
                "alcance": "Global para administracion o propio para colaboracion.",
            },
            {
                "nombre": "Uso de pipeline",
                "valor": pipeline_payload["summary"]["total_oportunidades"],
                "lectura": "Oportunidades actualmente seguidas en pipeline dentro del alcance visible.",
                "alcance": "Global para administracion o propio para colaboracion.",
            },
        ],
    }
    content = render_kpis(payload, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_permissions_page(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_permissions"):
        return _deny_html(request, start_response, "view_permissions")
    payload = {
        "rol_activo": request.access_context.role_label,
        "usuario_activo": request.access_context.user_id,
        "matriz": [
            {
                "rol": "Administrador",
                "consulta": "Catalogo, detalle, datos consolidados, KPIs, alertas y pipeline.",
                "gestion": "Puede crear y editar alertas propias o de otros contextos, y operar el pipeline.",
                "gobierno": "Puede revisar la matriz de permisos y las restricciones visibles.",
            },
            {
                "rol": "Colaborador",
                "consulta": "Catalogo, detalle, datos consolidados, KPIs y su propio espacio operativo.",
                "gestion": "Solo puede gestionar sus alertas y su pipeline propio.",
                "gobierno": "No accede a administracion global de permisos.",
            },
            {
                "rol": "Lector/Invitado",
                "consulta": "Catalogo, detalle y datos consolidados.",
                "gestion": "No puede crear ni modificar alertas, pipeline ni configuracion.",
                "gobierno": "No accede a vistas operativas de permisos ni KPIs.",
            },
        ],
    }
    content = render_permissions_matrix(payload, request.base_path, request.access_context)
    return send_response(start_response, "200 OK", "text/html; charset=utf-8", b"".join(html_body(content)))


def handle_api_users(request: Request, start_response) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(payload)))


def handle_api_user_detail(request: Request, start_response, id: str) -> list[bytes]:
    if not has_capability(request.access_context, "view_users"):
        return _deny_json(start_response, "view_users")
    try:
        payload = _visible_users_payload(request, selected_user_id=id)
    except UsersDatabaseError as exc:
        return send_response(start_response, "503 Service Unavailable", "application/json; charset=utf-8", b"".join(json_body({"error": str(exc)})))
    user = payload.get("usuario_seleccionado")
    if user is None:
        return _not_found(start_response)
    return send_response(start_response, "200 OK", "application/json; charset=utf-8", b"".join(json_body(user)))


routes = [
    Route("GET", "/static/{filename}", handle_static),
    Route("GET", "/api/datos-consolidados", handle_api_dataset),
    Route("GET", "/api/alertas", handle_api_alerts),
    Route("GET", "/api/pipeline", handle_api_pipeline),
    Route("GET", "/api/usuarios/{id}", handle_api_user_detail),
    Route("GET", "/api/usuarios", handle_api_users),
    Route("POST", "/alertas", handle_create_alert),
    Route("POST", "/alertas/{id}/editar", handle_update_alert),
    Route("POST", "/alertas/{id}/desactivar", handle_deactivate_alert),
    Route("POST", "/pipeline", handle_create_pipeline_entry),
    Route("POST", "/pipeline/{id}/estado", handle_update_pipeline_entry),
    Route("POST", "/usuarios", handle_create_user),
    Route("POST", "/usuarios/{id}", handle_update_user),
    Route("POST", "/usuarios/{id}/estado", handle_change_user_state),
    Route("POST", "/usuarios/{id}/invitacion", handle_resend_user_invitation),
    Route("POST", "/usuarios/{id}/reiniciar", handle_reset_user_access),
    Route("GET", "/api/oportunidades/{id}", handle_api_opportunity_detail),
    Route("GET", "/api/oportunidades", handle_api_opportunities),
    Route("GET", "/api/fuentes", handle_api_sources),
    Route("GET", "/api/fuentes-prioritarias", handle_api_prioritized_sources),
    Route("GET", "/api/clasificacion-ti", handle_api_classification),
    Route("GET", "/clasificacion-ti", handle_classification_page),
    Route("GET", "/cobertura-fuentes", handle_coverage_page),
    Route("GET", "/priorizacion-fuentes-reales", handle_prioritization_page),
    Route("GET", "/kpis", handle_kpis_page),
    Route("GET", "/permisos", handle_permissions_page),
    Route("GET", "/usuarios/{id}", handle_users_page),
    Route("GET", "/usuarios", handle_users_page),
    Route("GET", "/alertas", handle_alerts_page),
    Route("GET", "/pipeline", handle_pipeline_page),
    Route("GET", "/datos-consolidados", handle_dataset_page),
    Route("GET", "/datos-consolidados/licitaciones/{id}", handle_licitacion_detail),
    Route("GET", "/datos-consolidados/adjudicaciones/{id}", handle_adjudicacion_detail),
    Route("GET", "/oportunidades/{id}", handle_opportunity_detail),
    Route("GET", "/", handle_catalog_page),
]


def _match_pattern(path: str, pattern: str) -> dict[str, str] | None:
    path_parts = [part for part in path.strip("/").split("/") if part]
    pattern_parts = [part for part in pattern.strip("/").split("/") if part]
    if pattern == "/":
        return {} if path == "/" else None
    if len(path_parts) != len(pattern_parts):
        return None
    params: dict[str, str] = {}
    for path_part, pattern_part in zip(path_parts, pattern_parts):
        if pattern_part.startswith("{") and pattern_part.endswith("}"):
            params[pattern_part[1:-1]] = path_part
            continue
        if path_part != pattern_part:
            return None
    return params


def application(environ, start_response):
    base_path = resolve_base_path()
    query = parse_qs(str(environ.get("QUERY_STRING", "")), keep_blank_values=False)
    request = Request(
        environ=environ,
        method=(environ.get("REQUEST_METHOD", "GET") or "GET").upper(),
        path=_resolve_request_path(environ, base_path),
        base_path=base_path,
        query=query,
        access_context=resolve_access_context(environ, query),
    )
    for route in routes:
        if route.method != request.method:
            continue
        params = _match_pattern(request.path, route.pattern)
        if params is None:
            continue
        return route.handler(request, start_response, **params)
    return _not_found(start_response)
