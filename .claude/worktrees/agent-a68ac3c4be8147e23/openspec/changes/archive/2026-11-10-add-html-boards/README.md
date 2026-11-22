# add-html-boards: Tableros HTML (Gantt y Kanban)

**Cambio 10 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-html-boards`).

## Valor
Gantt y Kanban visibles, con el sistema de diseño del proyecto, que se pueden capturar para el informe y actualizar con el avance real sin rehacerlos.

## Skills
- `13-design-html-boards` (verbo `design`) y `13-design-html-boards-update`.

## Prerrequisitos
`01-design-system`, `11-make-sprint-plan`, `12-make-ceremonies-kanban`.

## Playbook
`common/html-boards/guia.md` (lo crea este cambio): reglas de HTML autónomo (un archivo, datos embebidos, sin librerías externas salvo fuentes), responsive y vista de impresión, accesibilidad, qué muestra cada tablero (Gantt con línea base y avance; Kanban con columnas, WIP y métricas), cómo se toma una captura para el informe.

## Modelos y formularios (`common/html-boards/models/`)
- `html-1-gantt.md` (especificación del tablero), `html-2-kanban.md`, `html-3-esquema-datos.md` (esquema de `gantt.json` y `tablero.json`), `README.md`.

## Qué pregunta la skill
Qué tableros generar, qué sprint/avance mostrar, si marcar progreso real, y si publicar una vista privada con Artifact (opcional, se confirma siempre).

## Salida
`project/html-boards/<corrida>/`: `gantt.html`, `kanban.html`, `data.json` (copia de las corridas 11 y 12 con el estado), `README.md`.

## Índice
Alimenta los **Anexos A.1 y A.2** y las capturas de **6.x.2 y 6.x.4**.

## Update
Excepción justificada al «no regenerar»: el HTML es derivado de `data.json`. El `-update` edita `data.json` (estado, fechas, tarjetas) y vuelve a renderizar solo los HTML, dejando el resto idéntico.

## Validación
Los HTML abren sin recursos externos, los datos embebidos coinciden con `data.json`, los tokens usados existen en `DESIGN.md`, texto limpio.

## Fuera de alcance
El `-update` de `06-make-design-thinking-prototypes` (edita tableros de Miro) queda fuera del roadmap salvo que el usuario lo pida. Generar capturas PNG.

## Decisiones abiertas para el proposal
- Cómo obtener capturas (el navegador del usuario o un paso de la skill).
- Si el renderizador es un script del kit o código generado en cada corrida.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
