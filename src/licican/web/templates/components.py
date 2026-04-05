from __future__ import annotations

from html import escape

from licican.shared.text import slugify


def render_table(
    headers: list[str],
    rows: list[str],
    empty_message: str | None = None,
    *,
    wrapper_class: str = "table-wrap",
    table_class: str = "",
) -> str:
    """Renderiza una tabla HTML simple."""
    if not rows and empty_message is not None:
        return f'<section class="note">{escape(empty_message)}</section>'
    header_html = "".join(f"<th>{escape(label)}</th>" for label in headers)
    wrapper_class_attr = f' class="{escape(wrapper_class)}"' if wrapper_class else ""
    table_class_attr = f' class="{escape(table_class)}"' if table_class else ""
    return f"""
      <div{wrapper_class_attr}>
        <table{table_class_attr}>
          <thead><tr>{header_html}</tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    """


def render_badges(items: list[tuple[str, str]] | dict[str, object], tone: str = "") -> str:
    """Renderiza badges de texto."""
    if isinstance(items, dict):
        pairs = [(key, str(value)) for key, value in items.items()]
    else:
        pairs = items
    class_name = f"badge {tone}".strip()
    return "".join(f'<span class="{class_name}">{escape(label)}: {escape(value)}</span>' for label, value in pairs)


def render_metric(value: object, label: str) -> str:
    """Renderiza un bloque métrico."""
    return f'<article class="metric"><strong>{escape(str(value))}</strong>{escape(label)}</article>'


def render_state_badge(value: object) -> str:
    """Renderiza un badge visual para estados funcionales."""
    text = escape(str(value))
    normalized = str(value).strip().lower()

    tone = "neutral"
    if normalized in {"resuelta", "adjudicada", "activa", "mvp", "global"}:
        tone = "success"
    elif normalized in {"anulada", "desierta", "desistida", "descartada", "inactiva", "deshabilitado", "bloqueado"}:
        tone = "danger"
    elif normalized in {"nueva", "evaluando", "preparando oferta", "presentada", "posterior", "por definir", "propio", "pendiente", "invitado / pendiente de activacion"}:
        tone = "warning"
    return f'<span class="status-badge {tone}">{text}</span>'


def render_role_badge(value: object) -> str:
    """Renderiza un badge visual para roles administrativos."""
    raw_value = " ".join(str(value).split()).strip()
    normalized_slug = slugify(raw_value)
    label = _role_badge_label(normalized_slug, raw_value)
    role_class = _ROLE_BADGE_CLASS_ALIASES.get(normalized_slug, normalized_slug)
    return f'<span class="badge-rol badge-rol--{escape(role_class)}">{escape(label)}</span>'


def render_icon_button(
    *,
    label: str,
    icon_svg: str,
    href: str | None = None,
    method: str | None = None,
    button_type: str = "button",
    css_class: str = "",
    tooltip: str | None = None,
    aria_label: str | None = None,
    hidden_input_name: str | None = None,
    hidden_input_value: str | None = None,
    onclick: str | None = None,
    data_attrs: dict[str, str] | None = None,
) -> str:
    """Renderiza un icono de accion compacto con tooltip CSS."""
    tooltip_text = tooltip or label
    aria_text = aria_label or tooltip_text
    classes = "btn-icon"
    if css_class:
        classes = f"{classes} {css_class}".strip()
    attrs = [f'class="{escape(classes)}"', f'data-tooltip="{escape(tooltip_text)}"', f'aria-label="{escape(aria_text)}"']
    if button_type:
        attrs.append(f'type="{escape(button_type)}"')
    if href is not None:
        attrs.append(f'data-href="{escape(href)}"')
    if method is not None:
        attrs.append(f'data-method="{escape(method)}"')
    if onclick is not None:
        attrs.append(f'onclick="{escape(onclick)}"')
    if data_attrs:
        attrs.extend(f'data-{escape(key)}="{escape(value)}"' for key, value in data_attrs.items())

    icon_html = f'<span class="btn-icon__icon" aria-hidden="true">{icon_svg}</span>'
    if href is not None:
        return f'<a {" ".join(attrs)} href="{escape(href)}">{icon_html}</a>'

    hidden_input_html = ""
    if hidden_input_name is not None:
        hidden_input_html = f'<input type="hidden" name="{escape(hidden_input_name)}" value="{escape(hidden_input_value or "")}" />'
    return f'<form class="btn-icon-form" method="{escape(method or "post")}" action="{escape(href or "")}">{hidden_input_html}<button {" ".join(attrs)}>{icon_html}</button></form>'


_ROLE_BADGE_LABEL_ALIASES: dict[str, str] = {
    "administrador-funcional": "administrador funcional",
    "administrador-de-plataforma": "administrador",
    "manager": "Manager",
    "gestor": "Manager",
    "colaborador": "colaborador",
    "invitado": "usuario",
    "usuario": "usuario",
    "superadmin": "superadmin",
    "administrador": "administrador",
}

_ROLE_BADGE_CLASS_ALIASES: dict[str, str] = {
    "administrador-funcional": "administrador-funcional",
    "administrador-de-plataforma": "administrador",
    "manager": "gestor",
    "gestor": "gestor",
    "colaborador": "colaborador",
    "invitado": "usuario",
    "usuario": "usuario",
    "superadmin": "superadmin",
    "administrador": "administrador",
}


def _role_badge_label(normalized_slug: str, raw_value: str) -> str:
    if normalized_slug in _ROLE_BADGE_LABEL_ALIASES:
        return _ROLE_BADGE_LABEL_ALIASES[normalized_slug]
    return raw_value or normalized_slug.replace("-", " ")


def render_inline_svg_icon(name: str) -> str:
    """Devuelve un SVG inline minimo para una accion de interfaz."""
    icons = {
        "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
        "confirm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
        "edit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5Z"/></svg>',
        "ban": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M7.5 7.5 16.5 16.5"/></svg>',
        "restore": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><path d="M3 12a9 9 0 1 1 3 6.7"/><path d="M3 17v-5h5"/></svg>',
        "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><circle cx="7.5" cy="15.5" r="3.5"/><path d="M10.5 15.5H21"/><path d="M18 12.5v3"/><path d="M15 13.5v2"/></svg>',
        "trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M6 6l1 14h10l1-14"/><path d="M10 11v5"/><path d="M14 11v5"/></svg>',
        "more": '<svg viewBox="0 0 24 24" fill="currentColor" focusable="false" aria-hidden="true"><circle cx="5" cy="12" r="1.75"/><circle cx="12" cy="12" r="1.75"/><circle cx="19" cy="12" r="1.75"/></svg>',
        "cancel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false" aria-hidden="true"><path d="M18 6 6 18"/><path d="M6 6l12 12"/></svg>',
    }
    return icons.get(name, icons["more"])


def render_status_note(message: str | None, tone: str = "ok") -> str:
    """Renderiza una nota de estado."""
    if message is None:
        return ""
    class_name = "note" if tone == "ok" else "note note-warning"
    return f'<section class="{class_name}">{escape(message)}</section>'
