# Design

## Context

Estado observado: `pipeline.json` define `13-design-html-boards` (verbo `design`, requiere `01-design-system`, `11-make-sprint-plan` y `12-make-ceremonies-kanban`, con `update`). `gantt.json` (sprints con fechas ISO y tareas con predecesoras y responsable) y `tablero.json` (columnas con WIP, métricas y tarjetas) ya están especificados y validados. `01-design-system` produce `tokens.json` (colores claro y oscuro, pares, tipografía, espacio, radio y sombra) y un `preview.html` generado por script, con el patrón de variables `--c-<clave>` y la alternancia claro/oscuro; el config guarda `diseno` (ruta al `DESIGN.md` vigente, o `null`). `12-make-ceremonies-kanban` define las métricas Tiempo de ciclo y Rendimiento, que se miden después. Los puntos 6.x.2, 6.x.4, A.1 y A.2 del índice piden capturas fechadas y cifras con fecha. No hay herramienta fiable para generar imágenes dentro del kit.

## Goals / Non-Goals

**Goals:** dos tableros HTML autónomos con la identidad del proyecto; línea base y estado real separados; indicadores calculados en un solo lugar; capturas fechadas para el informe.

**Non-Goals:** generar imágenes, el `-update` de `06-make-design-thinking-prototypes`, ejecutar las skills.

## Decisions

### D1. Salida
`gantt.html` y `kanban.html` (los que tengan fuente), `data.json` y `README.md` (procedencia, corridas base usadas, diseño usado, cómo capturar y, si hubo, el enlace de la vista privada).

### D2. `data.json`
```json
{"schema": 1, "proyecto": "...", "fecha_corte": "2026-11-20",
 "diseno": "project/design-system/<corrida>/tokens.json",
 "gantt": { ...contenido de gantt.json... },
 "tablero": { ...contenido de tablero.json... },
 "estado": {
   "tareas": {"TAR-01": {"avance": 100, "inicio_real": "2026-11-02", "fin_real": "2026-11-06"}},
   "tarjetas": {"TAR-01": {"columna": "Hecho", "entrada_en_curso": "2026-11-02", "llegada_hecho": "2026-11-06"}}},
 "calculado": { ... }}
```
`fecha_corte` es `null` si no hay estado. `diseno` es la ruta del `tokens.json` usado, o `"base"` si se usaron los tokens base. `gantt` y `tablero` se copian **sin cambios** de las corridas vigentes (la línea base nunca se modifica); `estado` es lo único que el usuario actualiza. Una tarea o tarjeta sin entrada en `estado` se considera con avance 0 y en la columna inicial. Solo se incluyen `gantt` o `tablero` si existe su fuente.

### D3. Estado: reglas
Avance entero de 0 a 100; avance 100 exige `fin_real`; `fin_real` ≥ `inicio_real`; todas las fechas ≤ `fecha_corte`; la columna de la tarjeta existe en el tablero; una tarjeta en la columna final exige `llegada_hecho` y una en columna de trabajo `entrada_en_curso`; `llegada_hecho` ≥ `entrada_en_curso`; **coherencia:** avance 100 si y solo si la tarjeta está en la columna final. Los códigos de `estado` existen en el plan.

### D4. Indicadores (`calculado`)
Funciones puras en `_shared/boards.py`: `avance_global` y `avance_por_sprint` (promedio entero del avance de las tareas), `tareas_hechas`, `tiempo_ciclo_promedio_dias` (promedio de `llegada_hecho − entrada_en_curso`, `null` si no hay tarjetas completas), `rendimiento_por_semana` (tareas con `llegada_hecho`, agrupadas por el lunes de su semana), `wip_actual` (tarjetas por columna) y `atrasadas` (tareas cuyo fin planificado es anterior a la fecha de corte y con avance < 100). Se usan días calendario. La skill y el validador comparten estas funciones, por lo que no hay dos implementaciones. Los valores mostrados se redondean como están en `calculado`.

### D5. Generación del HTML
`boards.py render` lee `data.json` y los tokens (los de `diseno`, o `base` desde `.claude/skills/01-design-system/references/tokens-base.json`) y escribe los HTML de forma determinista, sin recursos externos: un solo archivo, variables `--c-*`, `--espacio-*`, `--radio-*`, `--sombra-*`, tema claro por defecto, oscuro con `prefers-color-scheme` y `data-theme`, `meta viewport`, y los datos como `<script type="application/json" id="datos">`. Pequeño `<script>` inline para alternar el tema y filtrar por sprint. Es la misma excepción justificada al «no regenerar» que el sistema de diseño: el HTML es derivado y el `-update` lo vuelve a generar.

### D6. Gantt
Eje de tiempo desde el inicio del sprint 1 hasta el fin del sprint 3, con bandas por sprint (fechas y capacidad). Una fila por tarea agrupada por sprint: barra en su fecha planificada, relleno con el avance real, hitos como marcador, y por tarea código, nombre, historia, responsable y predecesoras. Línea vertical en la fecha de corte. Se desplaza dentro de su contenedor en teléfono. Cabecera: «al DD-MM-AAAA» o «Línea base», proyecto y avance global.

### D7. Kanban
Una columna por columna del tablero con sus tarjetas (código, título, historia, responsable), el contador «n de límite» (marca visible cuando n supera el límite) y las políticas visibles. Panel de métricas con las definidas en `tablero.json` y sus valores a la fecha de corte (tiempo de ciclo promedio y rendimiento por semana). Misma cabecera con fecha de corte.

### D8. Capturas
La skill no genera imágenes. El `README.md` de la corrida indica cómo capturar cada tablero (abrir el HTML en el navegador, ajustar el ancho, usar la captura del navegador) y propone el pie de foto: «Figura X: Gantt al DD-MM-AAAA». Como las cifras del informe deben llevar su fecha, la fecha de corte está siempre visible.

### D9. Publicación privada
Tras validar, la skill ofrece publicar una vista privada con la herramienta Artifact. Solo con confirmación explícita y por tablero; el HTML autónomo se publica tal cual (cumple el límite de tamaño). El enlace se anota en el `README.md`. No se guarda en el config.

### D10. Validación
`rules/html_boards.py`: `data.json` (esquema, línea base igual al plan y tablero vigentes con `projectcfg.current_run`, reglas de estado, `calculado` recalculado), tokens usados (cargados desde `diseno` o base), y por HTML: sin recursos externos, `meta viewport`, alternancia de tema, variables `--c-*` con valores de los tokens, JSON embebido igual a `data.json`, cada tarea o tarjeta presente, fecha de corte o «Línea base» y los indicadores mostrados. Sin plan o tablero vigente informa un aviso por comprobación imposible.

### D11. `-update`
Patrón del cambio 1. Modos: estado (avances, columnas, fechas y fecha de corte), resincronizar con el plan y el tablero vigentes (copia la línea base nueva, conserva el estado de los códigos que siguen existiendo y elimina el de los que ya no), cambiar el diseño y corregir datos. Siempre: editar `data.json` → regenerar HTML → validar.

### D12. Playbook
`common/html-boards/guia.md`: 0 reglas, 1 HTML autónomo, 2 línea base y estado, 3 Gantt, 4 Kanban, 5 cálculos, 6 capturas, 7 publicación opcional, 8 errores y checklist. Sin referencias bibliográficas. Plantillas `html-1-gantt`, `html-2-kanban`, `html-3-esquema-datos` y `README.md`.

## Risks / Trade-offs

- [Las cifras del HTML difieren de las de `data.json`] → Una sola implementación de los cálculos y comprobación de que el HTML las muestra.
- [El estado queda desactualizado frente al plan] → La validación compara con el plan y el tablero vigentes; el `-update` resincroniza conservando el estado.
- [El Gantt es ilegible en teléfono] → Contenedor con desplazamiento propio y filtro por sprint.
- [Sin sistema de diseño] → Tokens base con aviso; el `-update` cambia el diseño después.
- [El usuario cree que hay capturas listas] → El `README.md` y la skill dicen explícitamente que no se generan imágenes.
- [Publicar algo por error] → Solo con confirmación explícita y por tablero.

## Migration Plan

Sin migración: el paso es nuevo.

## Open Questions

- Si más adelante conviene generar PNG con un navegador sin cabeza (fuera de alcance por ahora).
- Si el estado real debería alimentarse automáticamente desde la bitácora de implementación (lo decide el cambio 12).
