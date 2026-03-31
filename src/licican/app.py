from __future__ import annotations

from wsgiref.simple_server import make_server

from licican.config import resolve_base_path, resolve_host, resolve_port
from licican.web.router import application


def main() -> None:
    """Arranca el servidor WSGI local."""
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
