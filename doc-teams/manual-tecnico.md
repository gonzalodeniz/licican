# Manual tecnico

## Publico objetivo
Equipo tecnico que necesita entender la implementacion actual, sus limites y la trazabilidad con la documentacion funcional.

## Resumen de arquitectura actual
La aplicacion es un servicio WSGI minimo en Python sin framework externo visible. Su objetivo actual es exponer la cobertura inicial de fuentes del MVP definida para `PB-007`.

## Componentes implementados
- Punto de entrada HTTP: [src/podencoti/app.py](/opt/apps/podencoti/src/podencoti/app.py)
- Carga y validacion de datos: [src/podencoti/source_coverage.py](/opt/apps/podencoti/src/podencoti/source_coverage.py)
- Configuracion versionada de cobertura: [data/source_coverage.json](/opt/apps/podencoti/data/source_coverage.json)
- Pruebas unitarias y de comportamiento HTTP basico: [tests/test_app.py](/opt/apps/podencoti/tests/test_app.py) y [tests/test_source_coverage.py](/opt/apps/podencoti/tests/test_source_coverage.py)

## Flujo de ejecucion
1. `podencoti.app.main()` levanta un servidor local con `wsgiref.simple_server` en `127.0.0.1:8000`.
2. La funcion `application()` enruta segun `PATH_INFO`.
3. La ruta `/` renderiza HTML con `_html_response()`.
4. La ruta `/api/fuentes` devuelve un `payload` JSON con `sources` y `summary`.
5. Ambas rutas cargan los datos desde `load_source_coverage()`.

## Modelo de datos
`SourceCoverage` define estos campos:
- `nombre`
- `categoria`
- `estado`
- `descripcion`
- `alcance`
- `referencia_funcional`

Los estados validos estan restringidos a:
- `MVP`
- `Posterior`
- `Por definir`

Si el JSON contiene otro estado, `load_source_coverage()` lanza `ValueError`.

## Contrato HTTP actual
### `GET /`
- Tipo: `text/html; charset=utf-8`
- Respuesta esperada: pagina con resumen de cobertura y tabla de fuentes.

### `GET /api/fuentes`
- Tipo: `application/json; charset=utf-8`
- Respuesta esperada:

```json
{
  "sources": [
    {
      "nombre": "string",
      "categoria": "string",
      "estado": "MVP | Posterior | Por definir",
      "descripcion": "string",
      "alcance": "string",
      "referencia_funcional": "string"
    }
  ],
  "summary": {
    "MVP": 0,
    "Posterior": 0,
    "Por definir": 0
  }
}
```

### Otras rutas
- Respuesta `404 Not Found`
- Cuerpo: `No encontrado`

## Trazabilidad funcional
La implementacion esta alineada con:
- `PB-007` y `HU-07` para hacer visible la cobertura inicial de fuentes.
- La propuesta de cobertura indicada en [product-manager/refinamiento-funcional.md](/opt/apps/podencoti/product-manager/refinamiento-funcional.md).
- La necesidad de evitar una promesa de exhaustividad descrita en [product-manager/roadmap.md](/opt/apps/podencoti/product-manager/roadmap.md).

## Brechas explicitas entre vision y producto actual
- La vision del producto habla de un agregador inteligente de licitaciones TI; el codigo actual solo expone una configuracion estaticamente versionada de fuentes.
- Los artefactos funcionales `PB-001` a `PB-005` y `PB-008` siguen pendientes en la implementacion observable de este repositorio.
- No existe actualmente integracion automatizada con portales oficiales, persistencia, autenticacion, filtros, detalle de expediente, alertas ni pipeline.

## Decisiones tecnicas observables
- Se prioriza simplicidad de entrega con libreria estandar de Python.
- La capa de datos se apoya en un archivo JSON local en lugar de base de datos o servicio externo.
- La salida HTML genera su contenido en una funcion unica y embebe estilos CSS en el propio documento.

## Verificacion tecnica
Comando verificado en este repositorio:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Cobertura comprobada por las pruebas:
- Renderizado de la ruta `/`
- Respuesta JSON de `/api/fuentes`
- Manejo de `404`
- Validacion de estados soportados
- Resumen agregado por estado

## Limitaciones tecnicas
- No hay estrategia de configuracion mediante variables de entorno.
- No existe observabilidad estructurada ni logging dedicado.
- `wsgiref.simple_server` es adecuado para desarrollo local, no para un despliegue productivo exigente.
- La documentacion funcional menciona futuras capacidades cuya materializacion tecnica aun no tiene contrato de API ni estructura de datos implementada.
