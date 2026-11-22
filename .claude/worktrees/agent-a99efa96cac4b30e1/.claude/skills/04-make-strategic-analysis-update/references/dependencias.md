# Dependencias del análisis estratégico

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/04-strategic-analysis/<corrida>/`). Las skills de `06` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y a quién llega

| Archivo | Viene de | Lo leen |
|---|---|---|
| `secciones/1.5.md` (PESTEL: `POL`, `ECO`, `SOC`, `TEC`, `AMB`, `LEG`) | fuentes verificadas, brief, corrida de `03` | 1.6 (evidencia de oportunidades y amenazas), 05 (columna PESTEL de la matriz), visual `pestel`, 12 |
| `secciones/1.6.md` (FODA `FOR`, `DEB`, `OPO`, `AME` y estrategias `FO`, `FA`, `DO`, `DA`) | Canvas de `03`, PESTEL, brief | 1.7 (evidencia de causas), 05 (columna FODA), visual `foda`, 12 |
| `secciones/1.7.md` (efecto y causas `CAU`) | problema principal del brief, FODA | 05 (causas principales de 1.8 y columna Causas de la matriz), visual `ishikawa`, 12 |
| `visuales/*.html`, `*.json`, `leer-imagen/*.md` | cada sección (`visuales.py construir`) | 12 |
| `referencias.md` | fuentes y marcos citados | 12 |

## Qué afecta cada cambio

| Cambio | Edición en la corrida | Figuras | Skills `-update` a ejecutar después |
|---|---|---|---|
| Agregar o corregir un hallazgo PESTEL o su fuente | fila de `secciones/1.5.md`, `referencias.md` | `pestel` | `05-make-problem-objectives-update` si la matriz cita ese código |
| Eliminar un hallazgo PESTEL | fila de 1.5 y la evidencia de las oportunidades o amenazas que lo citan en 1.6 | `pestel`, `foda` si cambió su evidencia | `05-make-problem-objectives-update` si la matriz lo cita |
| Agregar, corregir o eliminar un ítem FODA | fila de `secciones/1.6.md`; las estrategias que lo combinan; la evidencia de las causas de 1.7 que lo citan | `foda` (e `ishikawa` si cambió una evidencia) | `05-make-problem-objectives-update` si la matriz lo cita |
| Agregar, corregir o eliminar una estrategia cruzada | tabla de estrategias de 1.6 | `foda` | `05-make-problem-objectives-update` si la matriz la cita |
| Agregar, corregir o eliminar una causa del Ishikawa | fila de `secciones/1.7.md` | `ishikawa` | `05-make-problem-objectives-update` (causas principales de 1.8 y matriz) |
| Copiar un problema principal nuevo del brief | rótulo **Efecto.** de 1.7 y, si hace falta, causas | `ishikawa` | `05-make-problem-objectives-update` (enunciado de 1.8) |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Problema principal, objetivos o indicadores | `01-make-project-brief-update` |
| Datos de la empresa, tamaño o Canvas | `03-make-business-diagnosis-update` |
| Causas principales o matriz de articulación | `05-make-problem-objectives-update` |
| Colores o tipografía de los visuales | `02-design-system-update` y volver a construir las figuras |
