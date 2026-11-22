# Tasks

## 1. Molde y base

- [x] 1.1 Leer del molde (`git show pre-bi-pipeline:<ruta>`) `19-make-report/SKILL.md`, `20-make-annex-html/SKILL.md`, `_shared/report.py`, `report_prosa.py`, `rules/report.py`, `tests/test_report*.py` y `common/report/`, y anotar en design D1 qué se reutiliza; verificar que design.md lo lista.
- [x] 1.2 Hacer que `doc_html.py` tome la hoja de estilos de `common/html/vista-previa/index.html` cuando no exista `pantalla`, reubique los enlaces relativos a archivos que no son `.md` hacia la carpeta del HTML y anotarlo en `common/document-html/README.md`; verificar con `tests/test_doc_html.py` que `construir` y `comprobar` funcionan sobre una carpeta con varios `.md` y un enlace a `../imagenes/`.

## 2. Índice y plan

- [x] 2.1 Crear `_shared/report.py` con `cargar_indice` (capítulos, puntos con título limpio, detalle e `imagen`, anexos); verificar con pruebas que 1.6 y 4 tienen `imagen` verdadero, 1.1 falso, y que el título de 1.4 es «Modelo de negocio: Business Model Canvas».
- [x] 2.2 Crear fixtures en `tests/report_fixtures.py` (config, brief y corridas de 03, 04 y 05 según el contrato, registradas con `projectcfg.register`) y el comando `plan` (texto y `--json`) con disponibles, pendientes con su skill, secciones sin archivo, anexos y figuras; verificar con pruebas de informe parcial, sin secciones y sección sin archivo.

## 3. Construcción del informe

- [x] 3.1 Implementar `construir`: control del documento (config, brief, curso y docente), capítulos con introducción desde el playbook, secciones con el título del índice, referencias deduplicadas y ordenadas, `faltantes.md` y `README.md`; verificar con pruebas de orden, ausencia de pendientes, portada y referencias.
- [x] 3.2 Implementar las figuras (marcador, «Cómo copiarla», «Cómo leer la figura», copia a `imagenes/` e `imagenes/INDICE.md`) y la numeración global de figuras y tablas con sus menciones; verificar con pruebas de figura completa, figura sin explicación, figura sin HTML y renumeración entre secciones.
- [x] 3.3 Implementar los anexos A a D según su sección de origen (en el informe y en `anexos/anexo-<letra>.md`) y su ausencia en faltantes; verificar con pruebas de anexo sin origen y anexo presente.
- [x] 3.4 Implementar `render` (HTML con `doc_html` y los tokens del config) y `anexos` (HTML de los anexos de la corrida vigente, `--comprobar`); verificar con pruebas de HTML sin recursos externos, encabezados iguales al Markdown y comprobación sin incidencias.

## 4. Validador

- [x] 4.1 Crear `_shared/rules/report.py` (`validar(run)`) con las comprobaciones de la spec y verificar que `validate_run.py` lo carga por la carpeta `12-report`; verificar con `tests/test_report_rules.py` que una corrida recién armada no tiene incidencias y que cada corrupción (marca sin reemplazar, figura salteada, sin «Cómo copiarla», imagen incrustada, sección en informe y faltantes, sección con imagen sin marcador, referencia duplicada, tabla de versiones, anexo sin archivo) se informa.

## 5. Playbook y skills

- [x] 5.1 Escribir `common/12-report/guia.md` y `common/12-report/models/` (`README.md`, `rep-0-control-documento.md`, `rep-1-introducciones.md`, `rep-9-referencias.md`) con ficha, instrucciones, formato, ejemplo y checklist; verificar que `report.py` lee las introducciones del modelo (prueba) y que una corrida armada con ellas pasa la política de texto limpio de `validate_run.py`.
- [x] 5.2 Escribir `.claude/skills/12-make-report/SKILL.md` (fuentes, herramientas, reglas, contrato, flujo con confirmación del plan, registro) y `.claude/skills/13-make-annex-html/SKILL.md`; verificar con `tests/test_pipeline.py` (frontmatter, sin `-update`, rutas citadas existentes) y `npm run check:pipeline`.
- [x] 5.3 Actualizar la fila del informe en `.claude/skills/_shared/README.md`; verificar que cita `report.py` y `rules/report.py`.

## 6. Integración

- [x] 6.1 Ejecutar `python3 -m unittest discover -s .claude/skills/_shared/tests`, `npm run check:pipeline` y `python3 .claude/skills/_shared/html_tpl.py comprobar`; verificar que los tres terminan sin fallos.
- [x] 6.2 Armar de punta a punta un informe en una raíz temporal con los fixtures (`plan`, `construir`, `render`, `anexos`, `validate_run.py`); verificar que la corrida queda sin incidencias.

## Workflow follow-up

- Sincronizar las specs `report-assembly` y `annex-html` a `openspec/specs/` y validar con `openspec validate --specs --strict`.
- Archivar el change en `openspec/changes/archive/2026-11-21-bi-report-assembly/`.
