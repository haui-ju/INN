# add-lean-canvas-initial: Lean Canvas inicial (v0)

**Cambio 3 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-lean-canvas-initial`).

## Valor
Fija la hipótesis de partida **antes** del Design Thinking: problema, segmentos y propuesta de valor. El `ENF-01` del Design Thinking cita «Problema (Lean Canvas)», y el canvas validado v1 (cambio 6) se contrasta con este v0. Crea además el playbook `common/lean/` que ampliará el cambio 6.

## Skills
- `02-make-initial-lean-canvas` y `02-make-initial-lean-canvas-update`.

## Prerrequisitos
`00-init`.

## Playbook
`common/lean/guia.md` (lo crea este cambio, secciones de Lean Canvas y 5 porqués): los 9 bloques, cómo redactar problema/segmentos/propuesta de valor, método de los 5 porqués (3 a 5 niveles, cortar en la causa accionable), cómo marcar los **supuestos de mayor riesgo** (`SUP-nn`), citas permitidas (1 o 2).

Códigos de trazabilidad propuestos: `PRB-nn` (problema), `POR-nn` (cadena de porqués), `SUP-nn` (supuesto).

## Modelos y formularios (`common/lean/models/`)
- `lean-0-cinco-porques.md`: una cadena por problema.
- `lean-1-canvas.md`: los 9 bloques con v0.
- `README.md` de los modelos.

## Qué pregunta la skill
Problema principal y problemas secundarios, segmentos de clientes, propuesta de valor única, solución tentativa, canales, ingresos, costos, métricas clave, ventaja. Propone un borrador desde el `tema` del config y desde el `ENF-01` si ya existe; el usuario confirma o ajusta.

## Salida
`project/initial-lean-canvas/<corrida>/`: `canvas.md` (9 bloques, versión v0), `cinco-porques.md`, `README.md`.

## Índice
Alimenta **1.3.1** (5 porqués) y **1.3.2** (canvas v0). Sin cambios al índice.

## Update
Corregir un bloque, agregar o quitar un problema o un supuesto: toca `canvas.md`, `cinco-porques.md` y las citas `PRB`/`SUP`; avisa si el Design Thinking o el plan Lean ya usan el código cambiado.

## Validación
Los 9 bloques presentes, cada `PRB` con su cadena `POR`, cada `SUP` definido, códigos citados definidos.

## Fuera de alcance
Canvas validado v1 (cambio 6), capítulo 1 completo (cambio 4).

## Decisiones abiertas para el proposal
- Escala para marcar el riesgo de un supuesto (alto/medio/bajo o puntaje).
- Si el canvas se entrega también como tablero visual (HTML con el sistema de diseño) o solo en markdown.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
