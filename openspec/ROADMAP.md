# Ruta de cambios de las skills

Cada fila es un change de OpenSpec. Su `README.md` (en `openspec/changes/<nombre>/`) define qué hace, qué playbook y modelos crea, qué pregunta, qué produce, qué puntos del índice alimenta, cómo se actualiza y cómo se valida. Falta el proposal de cada uno (`/opsx:propose <nombre>`), que amplía y mejora esa definición.

Orden de ejecución de los proposals: de arriba hacia abajo. Un change solo depende de los anteriores.

| # | Change | Skills (cada una con su `-update`) | Playbook que crea o amplía | Índice (`model1.md`) |
|---|---|---|---|---|
| 1 | `add-project-config-init` (archivado) | `00-init`, renombre de 05 y 06, `05-…-update` | `_shared/` | — |
| 1b | `use-config-yaml-and-domain` | `00-init` (ajustada), `00-init-update` | `_shared/` (YAML), plantilla de `domain.md` | — |
| 2 | `add-design-system` | 01 | `common/design-system/` (crea) | — |
| 3 | `add-lean-canvas-initial` | 02 | `common/lean/` (crea) | 1.3.1, 1.3.2 |
| 4 | `add-company-chapter` | 03 | `common/company/` (crea) | 1.1, 1.2, 1.4 a 1.6 |
| 5 | `add-methodological-framework` | 04 | `common/methodological-framework/` (crea) | 2.1 a 2.4 |
| 6 | `add-lean-plan` | 07 | `common/lean/` (amplía) | 3.2 a 3.4; **corrige marcas** 3.2.3, 3.2.4, 3.3, 3.4 |
| 7 | `add-scrum-team-requirements` | 08, 09 | `common/scrum/` y `common/requirements/` (crea) | 4.1 a 4.3 |
| 8 | `add-user-stories-backlog` | 10 | `common/user-stories/` (crea) | 4.4, 4.5 |
| 9 | `add-sprint-plan-ceremonies` | 11, 12 | `common/scrum/` (amplía), `common/kanban/` (crea) | 4.6 a 4.8 |
| 10 | `add-html-boards` | 13 | `common/html-boards/` (crea) | Anexos A.1, A.2 |
| 11 | `add-system-design` | 14 | `common/system-design/` (crea) | 5.1 a 5.3, 5.5.1, D.4; **corrige marca** 5.4 |
| 12 | `add-sprint-execution-reports` | 15, 16 (×3) | `common/sprint-reports/` (crea) | 5.4, 6.1 a 6.3, A.3, E |
| 13 | `add-final-analysis` | 17, 18 | `common/final-analysis/` (crea) | 3.2.3, 3.2.4 (resultados), 6.4, 7 |
| 14 | `add-report-assembly` | 19 (sin `-update`) | `common/report/` (crea, breve) | Todo el índice |
| 15 | `add-app-definition-skills` | 21 y 22 (cada una con su `-update`) | `common/app-definition/` y `common/app-technical-definition/` (crean) | — (definición de la app, fuera del informe; corridas en `project/app/definition/`) |

## Reglas que se repiten en todos

- **Patrón común:** specs archivadas `project-config`, `run-versioning` y `skill-pipeline`.
- **Playbook como el de Design Thinking:** `common/<tema>/guia.md` + `models/` con una plantilla por entregable y un `README.md`.
- **Códigos de trazabilidad propios** sin chocar con los del Design Thinking (`OBS`, `ENT`, `HAL-E`, `PER`, `PP`, `POV`, `HMW`, `IDE`, `REQ`, `FLO`, `FLU`, `PAN`, `PRO`, `TST`, `HAL-T`, `CON`, `ENF`).
- **Regla del índice:** no renumerar los puntos 3.1.1 a 3.1.8 ni los anexos B, D, E y F.
- **Definir no es ejecutar:** ninguna skill se ejecuta al crear su change.

## Decisiones transversales abiertas

1. **Prerrequisitos por avance** (cambio 14): `pipeline.json` solo exige `18` para `19`, pero el avance 1 no necesita los capítulos 5 y 6.
2. **Esquemas de datos compartidos** (`gantt.json`, `tablero.json`): se fijan en los cambios 9 y 10.
3. ~~Dónde vive `DESIGN.md`~~ Decidido: `project/design-system/<corrida>/DESIGN.md`; el campo `diseno` del config lo actualiza la skill.
4. **`-update` de `06-make-design-thinking-prototypes`:** fuera de la ruta (edita tableros de Miro) salvo que el usuario lo pida.
5. **Cambio 1 pendiente de prueba:** el patrón `-update` no se ha probado sobre una copia de la corrida; se hará cuando el usuario lo pida.
