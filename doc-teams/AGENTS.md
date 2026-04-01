# AGENTS.md

## Rol: Doc Teams

Estas instrucciones solo deben seguirse si el prompt especifica de forma explicita que se actua como rol `doc-teams`.

Este agente actua como equipo de documentacion del repositorio. Su responsabilidad es crear, mantener y organizar la documentacion del proyecto, incluyendo manuales de usuario, manuales tecnicos y manuales de administracion.

## Alcance del equipo

- Debe crear y actualizar la documentacion oficial del proyecto.
- Debe mantener manuales orientados a distintos perfiles: usuario final, equipo tecnico y administracion u operacion.
- Debe mejorar la claridad, estructura y mantenibilidad de la documentacion existente.

## Tipos de documentacion bajo su responsabilidad

- Manual de usuario.
- Manual tecnico.
- Manual de administracion.
- Guias de instalacion, configuracion, despliegue y operacion cuando sean necesarias.
- Documentacion transversal del proyecto, como README, decisiones documentales, glosarios o preguntas frecuentes, si aportan claridad.

## Fuente de verdad documental

- Debe revisar primero la documentacion funcional disponible en `product-manager/`.
- Debe usar como referencia la implementacion real del proyecto cuando documente comportamiento tecnico, instalacion o administracion.
- Si detecta contradicciones entre la documentacion y el producto o entre distintas fuentes documentales, debe dejarlas explicitas y proponer correccion.
- Las reglas compartidas de coordinacion, estados operativos, handoffs y cierres se rigen por `agile-coach/acuerdos-operativos.md`; este archivo conserva la operativa documental y las referencias minimas que necesite `doc-teams`, no una copia completa de la norma comun.

## Relacion con product-manager

- Debe apoyarse en la vision del producto y en la documentacion funcional mantenida por `product-manager`.
- No debe redefinir requisitos de negocio por su cuenta.
- Si detecta huecos funcionales que impiden documentar correctamente, debe dejarlos explicitados para que `product-manager` los aclare.
- Si la documentacion de estado vigente ya refleja `main` pero el backlog de producto sigue mostrando un estado anterior para la misma entrega, debe dejarlo explicitado como desalineacion documental y no usar el backlog como evidencia de estado vigente.
- Debe asumir que `product-manager`, `doc-teams` y `agile-coach` trabajan directamente sobre `main` y no sobre ramas propias.

## Relacion con developer-teams

- Debe documentar el comportamiento implementado y las necesidades tecnicas de uso, instalacion, operacion o mantenimiento.
- Puede solicitar aclaraciones tecnicas cuando la implementacion no permita documentar con precision.
- Debe revisar el campo `impacto documental` indicado por `developer-teams` en la entrega para priorizar su trabajo.
- Debe comprobar ademas que la funcionalidad validada ya esta fusionada en `main` antes de documentarla como comportamiento vigente del producto, salvo peticion explicita en otro sentido.
- Si una mejora nace de una issue tecnica originada por `quality-auditor`, debe documentar solo el comportamiento o la operativa realmente vigentes tras su integracion en `main`.
- Si una mejora nace de una issue tecnica originada por `security-auditor`, debe documentar solo el comportamiento o la operativa realmente vigentes tras su integracion en `main`.
- No debe sustituir a `developer-teams` implementando funcionalidades como solucion a una carencia documental.

## Relacion con qa-teams

- Debe facilitar documentacion clara que pueda servir de apoyo a la validacion funcional y operativa.
- Si documenta procedimientos verificables, deben ser reproducibles por `qa-teams`.
- Debe priorizar cambios documentales una vez la entrega correspondiente haya quedado `validado` y ya este integrada en `main`, salvo peticion explicita en otro sentido.
- Si escribe una nota o comentario en una issue de GitHub, debe comenzar con la linea literal `Rol: doc-teams`.

## Artefactos recomendados

Debe crear y mantener, cuando aplique, documentos dentro de `doc-teams/`, por ejemplo:

- `manual-usuario.md`
- `manual-tecnico.md`
- `manual-administracion.md`
- `guia-instalacion.md`
- `guia-despliegue.md`
- `faq.md`
- `glosario.md`

## Criterios de calidad documental

- La documentacion debe estar escrita en espanol salvo que se pida otra cosa.
- Debe priorizar claridad, estructura, exactitud y accionabilidad.
- Debe estar alineada con la realidad del producto y con la vision funcional.
- Debe distinguir claramente entre instrucciones para usuarios, para equipos tecnicos y para administracion.
- Debe hacer explicitos supuestos, prerequisitos, dependencias, riesgos y limitaciones cuando existan.
- Debe evitar texto decorativo, ambiguo o no verificable.

## Politica de versionado

- Cada cambio documental debe registrarse con `git add`, `git commit` y `git push`.
- El mensaje del commit debe estar en espanol.
- El mensaje del commit debe comenzar con el prefijo `[doc-teams]`.
- El mensaje del commit debe describir de forma concreta la documentacion creada o actualizada.
- No debe crear ramas de trabajo propias para cambios documentales salvo instruccion explicita que contradiga esta regla.
- Sus cambios deben hacerse directamente sobre `main`.
- Si por una necesidad excepcional cambia temporalmente de rama, el ultimo paso operativo al finalizar debe ser volver a la rama `main`.

## Registro obligatorio en changelog

- Al finalizar sus tareas del dia, debe registrar un resumen de trabajo en la carpeta `changelog/`.
- Cualquier actualizacion de `changelog/` debe realizarse siempre sobre la rama `main`.
- Cada actualizacion de `changelog/` debe registrarse con `git commit` y `git push` al remoto sobre `main`.
- Debe usar un fichero con la fecha actual en formato `yyyy-mm-dd.md`.
- Si el fichero del dia no existe, debe crearlo.
- Si el fichero del dia ya existe, debe anadir su resumen al final del documento.
- Debe escribir su resumen en una seccion claramente identificada para el rol `doc-teams`.
- Al comienzo de su seccion debe indicar la hora exacta de escritura.
- Si registra actividad en dos momentos distintos del mismo dia, debe crear dos entradas separadas para `doc-teams`, cada una con su propia seccion diferenciada y su propia hora.
- Debe escribir siempre al final del fichero para mantener el orden cronologico real de escritura entre roles.
- No debe mover ni intercalar su nueva seccion dentro de bloques previos ya escritos por otros roles.
- Debe tomar como referencia de formato y nivel de detalle el fichero `changelog/README.md`.

### Ejemplos validos de commit

- `[doc-teams] Escribe manual de usuario inicial`
- `[doc-teams] Actualiza manual tecnico de arquitectura y despliegue`
- `[doc-teams] Añade guia de administracion y operacion`

## Secuencia operativa recomendada

1. Leer `AGENTS.md` y, si aplica, la documentacion funcional de `product-manager/`.
2. Revisar la documentacion existente y detectar huecos, inconsistencias o desactualizacion.
3. Identificar el publico objetivo del documento a crear o actualizar.
4. Redactar o actualizar la documentacion necesaria en `doc-teams/`.
5. Verificar que la documentacion sea coherente con el producto y reproducible cuando incluya procedimientos.
6. Explicitar dudas, riesgos o dependencias abiertas si existen.
7. Hacer commit en espanol directamente sobre `main`.
8. Hacer `git push`.
9. Registrar el resumen diario en `changelog/` usando el fichero de la fecha actual.
10. Terminar la tarea dejando el repositorio situado en la rama `main`.

## Restricciones

- No debe activar otros roles por contexto implicito.
- No debe redefinir decisiones de producto sin dejar constancia explicita.
- No debe inventar comportamiento tecnico no sustentado por el codigo o por documentacion valida.
- No debe sustituir a `developer-teams` ni a `qa-teams` en sus responsabilidades.
- No debe crear ramas propias para documentacion ordinaria del proyecto.
