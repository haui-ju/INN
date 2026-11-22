---
name: 13-make-annex-html
description: Convierte a HTML autónomo, con el sistema de diseño del proyecto, los anexos (anexos/anexo-<letra>.md) de la corrida vigente de 12-make-report, uno por archivo más un índice, en anexos/html/ de esa misma corrida, según el estándar de common/document-html. No crea corrida propia ni cambia ningún Markdown. Úsala cuando el usuario pida "13-make-annex-html", "pasar los anexos a HTML", "anexos en HTML" o cuando cambien los anexos y haga falta regenerar o comprobar su HTML sin rearmar el informe.
---

# 13-make-annex-html

Último paso del pipeline. Trabaja sobre la corrida vigente de `12-make-report`: no tiene carpeta propia ni `-update`.

## Fuentes obligatorias

1. `common/document-html/README.md` y `common/document-html/plantilla.html` (estándar del documento HTML).
2. `common/12-report/guia.md`, sección 6 (de dónde salen los anexos A a D).
3. `project/config.yaml` (`diseno` y la corrida vigente de `12-make-report`).

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check --skill 13-make-annex-html`, `current --step 12-make-report`)
- `python3 .claude/skills/_shared/report.py anexos [--run CORRIDA] [--comprobar]` (usa `doc_html.py` con los tokens del sistema de diseño del config, o los base si no hay)
- `python3 .claude/skills/_shared/validate_run.py` (reglas de la corrida del informe).

## Reglas

- **El HTML no se edita a mano.** Si un texto está mal, se corrige con el `-update` de la skill que produjo el anexo, se vuelve a armar el informe (`12-make-report`) y se regenera el HTML.
- Un HTML por cada `.md` de `anexos/`, con la misma ruta bajo `anexos/html/`, más `anexos/html/index.html`. Autónomos y sin recursos externos.
- No crea corrida ni modifica ningún `.md`.
- Texto limpio: los HTML reflejan los anexos tal cual; no agregan notas sobre el origen de los datos.

## Flujo

1. **Config.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 13-make-annex-html` y muestra los avisos.
2. **Corrida.** `projectcfg.py current --step 12-make-report`; confirma con el usuario que es la corrida que quiere convertir (o usa `--run`). Sin corrida, indica `12-make-report`.
3. **Construir.** `python3 .claude/skills/_shared/report.py anexos [--run CORRIDA]`. Si responde que la corrida no tiene anexos, explica que salen de las secciones 3.1 (`08-make-etl`) y 3.2 (`09-make-dashboard`) y detente.
4. **Comprobar.** `python3 .claude/skills/_shared/report.py anexos --comprobar [--run CORRIDA]`. Debe responder «sin incidencias».
5. **Validar.** `python3 .claude/skills/_shared/validate_run.py project/12-report/<corrida>` hasta que no haya incidencias.
6. **Cierre.** Entrega el número de archivos, la ruta de `anexos/html/index.html` y, si el sistema de diseño está vacío, que se usaron los tokens base (se cambia con `02-design-system`).
