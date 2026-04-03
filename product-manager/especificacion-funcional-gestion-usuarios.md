# Especificacion Funcional de Gestion de Usuarios

## 1. Proposito
Definir el funcionamiento funcional y visual del modulo de `Gestion de usuarios` en Licican, orientado a administracion interna de cuentas, roles, permisos y control basico de acceso.

## 2. Necesidad de negocio
- Licican necesita una forma trazable de dar de alta, mantener y retirar cuentas sin gestionar usuarios de forma manual fuera del sistema.
- La administracion de accesos debe quedar alineada con un entorno de backoffice institucional, claro y consistente con el resto de la aplicacion.
- El producto requiere control operativo sobre quien accede y con que rol actua cada cuenta.
- Los cambios de acceso y permisos deben quedar auditados para soporte, seguridad y trazabilidad administrativa.

## 3. Objetivo funcional
Permitir a administradores de plataforma, administradores funcionales y responsables con permisos suficientes gestionar cuentas de usuario de extremo a extremo: alta, edicion, activacion, desactivacion, baja logica, reasignacion de roles, reenvio de invitacion, reinicio de acceso y consulta de trazabilidad.

## 4. Alcance

### 4.1 MVP
- Listado paginado de usuarios.
- Filtros por nombre, apellidos, email, identificador, estado y rol.
- Tarjetas KPI con usuarios totales, activos, inactivos y pendientes o roles definidos.
- Alta de usuario.
- Edicion de datos basicos.
- Cambio de rol principal.
- Revision de roles y estado de acceso.
- Activacion y desactivacion.
- Baja logica.
- Reactivacion.
- Reenvio de invitacion.
- Reinicio de acceso o contrasena.
- Consulta de detalle.
- Visualizacion de ultimo acceso.
- Acceso a historial o trazabilidad de cambios.

### 4.2 Fuera de alcance del MVP
- Gestion masiva de usuarios.
- Sincronizacion con directorios externos o federacion de identidad.
- SSO, MFA o politicas avanzadas de autenticacion.
- Flujos de aprobacion en cadena para altas complejas.
- Exportacion avanzada y automatizaciones de segmento o cohortes.

### 4.3 Mejoras futuras
- Acciones masivas sobre varios usuarios.
- Exportacion avanzada con filtros guardados.
- Integracion con directorios corporativos.
- Delegacion de permisos por estructura organizativa.
- Alertas administrativas por usuarios bloqueados o sin acceso prolongado.

## 5. Estados posibles de usuario
- `invitado / pendiente de activacion`: la cuenta existe pero el usuario aun no ha completado el acceso inicial.
- `activo`: la cuenta puede acceder y operar dentro de sus permisos.
- `inactivo`: la cuenta esta deshabilitada temporalmente y no puede acceder.
- `bloqueado`: el acceso esta retenido por una condicion de seguridad o control operativo.
- `baja logica`: la cuenta se retira de uso activo pero se conserva para trazabilidad e historico.

## 6. Acciones permitidas
- Alta de usuario.
- Edicion de datos basicos.
- Modificacion de rol principal.
- Revision de roles y estado de acceso.
- Activacion de usuario.
- Desactivacion o baja logica.
- Reactivacion.
- Reenvio de invitacion si el usuario sigue pendiente.
- Restablecimiento o reinicio de acceso o contrasena.
- Consulta de detalle del usuario.
- Visualizacion del estado actual.
- Visualizacion del ultimo acceso.
- Acceso a historial o trazabilidad de cambios.

## 7. Elementos obligatorios de interfaz
- Titulo de pantalla: `Gestion de usuarios`.
- Texto descriptivo breve: explica que permite administrar cuentas, roles y accesos.
- Boton principal de alta: `Nuevo usuario` o `Anadir usuario`.
- Boton secundario opcional: `Exportar`.
- Bloque de KPIs con:
  - usuarios totales
  - usuarios activos
  - usuarios inactivos
  - invitaciones pendientes o roles definidos
- Bloque de filtros con:
  - busqueda por nombre, apellidos, email o identificador
  - filtro por estado
  - filtro por rol
  - boton `Aplicar filtros`
  - boton `Limpiar filtros`
- Tabla principal de usuarios.
- Paginacion.
- Acciones por fila.
- Acceso a vista detalle o formulario de edicion.
- Layout coherente con una interfaz institucional:
  - sidebar izquierda oscura
  - area de trabajo clara
  - tarjetas de resumen
  - filtros compactos
  - tabla principal dominante
  - acciones por fila visibles y contenidas

## 8. Formulario de alta y edicion
Campos obligatorios o visibles segun contexto:
- nombre
- apellidos
- email
- rol
- estado
  - observaciones internas, si procede
  - fecha de alta, si aplica como dato visible o automatico

Reglas de formulario:
- El estado debe ser visible y controlado por el sistema cuando la politica lo requiera.
- El rol debe quedar claramente identificado como rol principal.
- La fecha de alta puede ser de solo lectura si el sistema la asigna automaticamente.

## 9. Validaciones
- El email debe tener formato valido.
- El email no puede duplicarse.
- El nombre y el rol son obligatorios.
- Los cambios sensibles requieren confirmacion previa.
- No se puede dejar al sistema sin ningun usuario administrador activo.
- Un usuario inactivo no debe poder acceder.
- Un usuario en estado pendiente aun no esta plenamente activo.
- Los cambios de permisos y roles deben quedar auditados.
- El reinicio de acceso o contrasena debe quedar registrado.
- La baja logica debe conservar trazabilidad historica.

## 10. Casos limite y errores esperables
- Intentar crear o editar un usuario con un email ya existente.
- Intentar asignar un rol restringido sin permisos suficientes.
- Intentar desactivar al ultimo administrador activo.
- Intentar reactivar un usuario con datos incompletos o inconsistentes.
- Intentar reenviar una invitacion a un usuario ya activo.
- Intentar reiniciar el acceso de un usuario no invitado todavia.
- Intentar aplicar cambios concurrentes sobre el mismo usuario desde dos sesiones distintas.
- Intentar eliminar fisicamente un usuario con historial operativo.
- Intentar consultar el detalle de un usuario sin permisos suficientes.
- Mostrar ultimo acceso vacio cuando el usuario nunca ha iniciado sesion.

## 11. Dependencias y consideraciones para backend y auditoria
- Debe existir un modelo persistente de usuarios, roles y ambitos de acceso.
- Debe existir trazabilidad historica de cambios de estado, rol y permisos.
- La baja logica debe preferirse a la eliminacion fisica.
- Las acciones de alta, edicion, activacion, desactivacion, reactivacion, invitacion y reinicio deben quedar auditadas con usuario ejecutor, fecha y cambio aplicado.
- El backend debe impedir que el sistema quede sin administradores activos.
- La capa de permisos debe proteger endpoints, no solo la interfaz.
- La invitacion pendiente necesita control de expiracion o reemision.
- El detalle del usuario debe exponer estado actual, ultimo acceso y historial relevante.
- Las consultas del listado deben soportar paginacion y filtros para no degradar la operacion.

## 12. Definicion de exito
- Un administrador con permisos puede listar, crear, editar y controlar usuarios desde un unico modulo.
- El sistema impide accesos no autorizados y bloquea cambios peligrosos como desactivar al ultimo administrador.
- Los estados de usuario se muestran de forma clara y no dejan ambiguedad sobre quien puede acceder.
- Los cambios relevantes quedan auditados y son consultables.
- La interfaz mantiene una lectura sobria, institucional y coherente con el resto de Licican.

## 13. Criterios de aceptacion funcional
1. El usuario con permisos suficientes ve el modulo `Gestion de usuarios` con listado paginado, filtros, KPIs y acciones por fila.
2. El usuario puede crear una cuenta con datos validos y verla reflejada en el listado y en el detalle.
3. El sistema rechaza emails duplicados con un mensaje claro.
4. El usuario puede editar datos basicos, cambiar rol y ajustar estado cuando tenga autorizacion para hacerlo.
5. El usuario puede activar, desactivar, reactivar y dar baja logica a una cuenta con confirmacion previa en acciones sensibles.
6. El usuario puede reenviar invitacion a cuentas pendientes y reiniciar acceso o contrasena cuando corresponda.
7. El detalle del usuario muestra estado actual, ultimo acceso e historial o trazabilidad de cambios.
8. El sistema impide dejar la plataforma sin ningun administrador activo.
