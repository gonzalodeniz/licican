from __future__ import annotations

from html import escape

from licican.web.responses import build_url


def render_login(
    *,
    base_path: str,
    csrf_token: str,
    reason: str | None = None,
    error_message: str | None = None,
) -> str:
    info_message = _resolve_info_message(reason)
    error_html = f'<div class="note note-warning login-feedback">{escape(error_message)}</div>' if error_message else ""
    info_html = f'<div class="note login-feedback">{escape(info_message)}</div>' if info_message else ""
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Licican | Iniciar sesión</title>
    <link rel="stylesheet" href="{escape(build_url(base_path, '/static/style.css'))}" />
  </head>
  <body class="login-body">
    <main class="login-shell">
      <section class="login-card" aria-labelledby="login-title">
        <p class="nav-kicker">Licican</p>
        <h1 id="login-title">Iniciar sesión</h1>
        <p class="login-copy">Acceda para consultar oportunidades, alertas y seguimiento operativo interno.</p>
        {info_html}
        {error_html}
        <form method="post" action="{escape(build_url(base_path, '/login'))}" class="login-form">
          <input type="hidden" name="csrf_token" value="{escape(csrf_token)}" />
          <label class="form-field" for="username">
            <span>Usuario o email</span>
            <input id="username" name="username" type="text" autocomplete="username" required />
          </label>
          <label class="form-field" for="password">
            <span>Contraseña</span>
            <input id="password" name="password" type="password" autocomplete="current-password" required />
          </label>
          <button class="button button-primary login-submit" type="submit">Iniciar sesión</button>
        </form>
      </section>
    </main>
  </body>
</html>"""


def _resolve_info_message(reason: str | None) -> str | None:
    normalized = (reason or "").strip().lower()
    if normalized == "timeout":
        return "Su sesión ha expirado por inactividad."
    if normalized == "logout":
        return "Ha cerrado sesión correctamente."
    return None
