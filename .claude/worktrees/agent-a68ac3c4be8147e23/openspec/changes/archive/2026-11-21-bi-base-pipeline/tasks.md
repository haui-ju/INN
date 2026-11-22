# Tasks

## 1. Respaldo del molde

- [x] 1.1 Con confirmación del usuario, crear la etiqueta git `pre-bi-pipeline` sobre `HEAD` y verificar con `git show pre-bi-pipeline:.claude/skills/19-make-report/SKILL.md` que las skills viejas están en ella.
- [x] 1.2 Buscar con `grep -rn "import" .claude/skills/_shared/*.py` quién importa a quién y anotar en un archivo de trabajo qué módulos del kit se quedan y cuáles se retiran (design D7); verificar que ningún módulo que se queda importe uno que se retira.

## 2. Pipeline y registro de secciones

- [x] 2.1 Reescribir `.claude/skills/_shared/pipeline.json` con las skills `00` a `13`, carpetas numeradas, `requiere`, `update` y `secciones` por skill (1.1 a 1.10, 2.1 a 2.5, 3.1, 3.2, 4 y 5); verificar con una prueba que el orden es consecutivo y que ninguna sección está en dos skills ni sin skill.
- [x] 2.2 En `projectcfg.py`, subir el config a `schema: 3`, agregar `calendario` e `informe.secciones`, quitar `enfoque`, `resultado_esperado`, `avances` y los roles de Scrum, y rechazar un `schema` desconocido; verificar con pruebas de config nuevo, config con `schema: 2` y roles libres.
- [x] 2.3 Ampliar `register` para marcar como disponibles las secciones de la skill, respetar `fijada` y no mover las secciones cuando el fork de un update no valida; verificar con pruebas de skill terminada, paso fijado y update fallido.
- [x] 2.4 Agregar la consulta de secciones disponibles y pendientes (con la skill que produce cada pendiente), el tratamiento de carpeta borrada y la reconciliación con `pipeline.json`; verificar con las pruebas de informe parcial, ninguna sección y sección desconocida.
- [x] 2.5 Quitar de `projectcfg.py` el soporte de avances (`requiere_por_avance`, parámetro `avance` de `check`); verificar que `projectcfg.py check --skill 03-make-business-diagnosis` avisa los pasos faltantes sin bloquear.

## 3. Skills 00-init y 00-init-update

- [x] 3.1 Reescribir `.claude/skills/00-init/SKILL.md` para los datos de BI (nombre, rubro, empresa por RUC o propio, integrantes con rol opcional, modo de datos), con calendario vacío y `informe.secciones` pendientes, y que sugiera `01-make-project-brief`; verificar ejecutando `projectcfg.py validate` sobre el config que genera.
- [x] 3.2 Reescribir `00-init-update` (cambia nombre, rubro, tipo, RUC, equipo y modo de datos; remite al brief para tema y fechas); verificar con una prueba de cambio de equipo que conserva los comentarios del config.

## 4. Skill 01-make-project-brief

- [x] 4.1 Renombrar `common/project-brief/` a `common/01-project-brief/` y reescribir su guía y `brief-1-nucleo.md` con las ocho secciones de BI, objetivos con KPI y calendario único; verificar que la plantilla tiene ficha, instrucciones, formato, ejemplo y checklist.
- [x] 4.2 Renombrar las skills `00b-make-project-brief` y `-update` a `01-make-project-brief` y `01-make-project-brief-update` y actualizar su flujo, la carpeta `project/01-project-brief/` y el registro del paso; verificar que los `SKILL.md` no citan `00b`.
- [x] 4.3 Adaptar `brief.py` y `rules/project_brief.py` a las nuevas secciones, al calendario único y a la coherencia con el config (tema y fechas); verificar con pruebas de sección ausente, objetivo sin KPI, plazo distinto de la entrega y entrega anterior al inicio.
- [x] 4.4 Ajustar `tests/test_project_brief.py` y `brief_fixtures.py` a lo anterior; verificar que el archivo de pruebas pasa.

## 5. Skill 02-design-system

- [x] 5.1 Renombrar `common/design-system/` a `common/02-design-system/` y las skills `01-design-system` y `-update` a `02-design-system` y `02-design-system-update`, con la carpeta `project/02-design-system/` y el registro del paso; verificar que `diseno` apunta al `DESIGN.md` de la corrida.
- [x] 5.2 Ajustar `rules/design_system.py` y `tests/test_design_system.py` a las rutas numeradas; verificar que sus pruebas pasan.

## 6. Corridas en carpetas numeradas

- [x] 6.1 Ajustar `runs.py` y `validate_run.py` para escribir y validar en `project/<NN-carpeta>/<fecha-hora>/` según `pipeline.json`; verificar con `tests/test_runs.py` y `tests/test_validate_run.py` (dos ejecuciones crean dos carpetas dentro de la numerada).

## 7. Índice del informe

- [x] 7.1 Reescribir `common/structure/model1.md` con el control del documento sin versiones, los cinco capítulos (1.1 a 1.10, 2.1 a 2.5, 3.1 y 3.2, 4 y 5), las marcas «(incluye imagen)», las reglas de contenido y los anexos A a D con Referencias; verificar con una prueba que la numeración no tiene saltos ni repetidos y que cada punto del índice figura en `pipeline.json`.

## 8. Retiro de lo que no aplica

- [x] 8.1 Borrar las skills retiradas de `.claude/skills/` (`02` a `18` y `21` a `24` del pipeline viejo, `19-make-report`, `20-make-annex-html`, `06-make-design-thinking-prototypes` y sus `-update`); verificar con `ls .claude/skills` que solo quedan `00`, `01`, `02`, sus `-update`, `openspec-*`, `opsx-*`, `redaccion-academica` y `_shared`.
- [x] 8.2 Borrar de `common/` las carpetas retiradas y los visuales de `common/html/` que no se reutilizan (design D8); verificar con `ls common common/html` que quedan solo `01-project-brief`, `02-design-system`, `structure`, `citation-style`, `document-html` y, en `html`, `DESIGN.md`, `README.md`, `_build`, `vista-previa` y `foda`.
- [x] 8.3 Borrar del kit `_shared` los módulos, validadores (`rules/`), fixtures y tests de lo retirado (design D7) y comprobar `visuales.py`, `html_tpl.py` y `doc_html.py`: si no importan sin errores, recortarlos a lo reutilizable; verificar con `python3 -m unittest discover .claude/skills/_shared/tests` sin fallos ni errores de importación.
- [x] 8.4 Adaptar `scripts/check-pipeline.mjs` al nuevo `pipeline.json`; verificar con `npm run check:pipeline`.
- [x] 8.5 Borrar de `openspec/specs/` las 25 capacidades retiradas: `app-definition-docs`, `app-implementation-plan`, `app-scaffold`, `app-trd-interview`, `ceremonies-kanban`, `company-chapter`, `design-thinking-package-generation`, `design-thinking-prototype-mockups`, `final-analysis`, `html-boards`, `html-templates`, `html-visuals`, `implementation-log`, `lean-canvas-initial`, `lean-plan`, `lean-results`, `methodological-framework`, `report-assembly`, `requirements`, `scrum-setup`, `sprint-plan`, `sprint-report`, `system-design`, `ui-mockups` y `user-stories`; verificar con `openspec list --specs` que quedan solo las seis modificadas y `report-section-registry` (esta última aparece al archivar).

## 9. Integración

- [x] 9.1 Buscar referencias huérfanas con `grep -rniE "00b|01-design-system|avance|sprint|scrum|kanban|design thinking|lean" .claude/skills common scripts` y corregir las que no sean texto histórico justificado; verificar que la búsqueda queda sin resultados inesperados.
- [x] 9.2 Probar el flujo de extremo a extremo en un directorio temporal: `00-init` produce un config válido, `01` registra el brief, `02` registra el diseño y la consulta de secciones lista todas las del informe como pendientes; verificar que `projectcfg.py validate` pasa en cada paso.
- [x] 9.3 Ejecutar `openspec validate bi-base-pipeline --strict` y la suite del kit completa; verificar que ambas terminan sin errores.

## Workflow follow-up

- Revisar el árbol de trabajo y decidir con el usuario cuándo commitear el borrado (la etiqueta `pre-bi-pipeline` permite restaurar).
- Archivar el change con `/opsx:archive` cuando el usuario lo apruebe.
