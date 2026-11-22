---
name: 01-make-project-brief-update
description: Cambia el núcleo del proyecto de BI ya definido sin rehacerlo: copia la corrida vigente del brief como "-fork", cambia solo lo pedido (el tema o la empresa, la problemática, un objetivo o su indicador, la justificación o el alcance, los usuarios o las decisiones, una fuente de datos, la fecha de inicio o de entrega, o un supuesto o riesgo), completa lo que estaba pendiente, copia al config lo que cambie, rehace domain.md solo si cambió el tema, el tipo o el RUC, valida e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "01-make-project-brief-update", "cambiar un objetivo", "mover la fecha de entrega", "ajustar la problemática", "agregar una fuente de datos" o "completar lo pendiente del brief" sobre project/01-project-brief/.
---

# 01-make-project-brief-update

Homóloga de `01-make-project-brief`. Parte de una corrida existente, la bifurca y edita **solo lo afectado** del `brief.md`; lo demás queda idéntico a la base. Como todas las demás skills leen el brief, al cerrar dice cuáles hay que actualizar.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `show`, `register`, `set-nucleo`)
- `python3 .claude/skills/_shared/runs.py fork --step 01-make-project-brief [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/brief.py leer | al-config`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear) y `common/01-project-brief/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro del brief (por ejemplo, los plazos de los objetivos si se mueve la entrega); no reescribe lo demás, no reformula textos y no reordena.
- **Lo pendiente se completa aquí.** Una fecha, una meta o una evidencia que estaba «Pendiente» se pide al usuario y se escribe; no la inventes.
- **Las mismas reglas que 01:** objetivos con métrica, meta, indicador y plazo `Entrega (fecha)` igual a la entrega del calendario; fuentes con tipo y acceso válidos; sin presuponer una empresa.
- **El config sigue al brief:** después de editar, `brief.py al-config` copia el tema y las fechas.
- **`domain.md`** solo se rehace (con confirmación) si cambió el tema, el tipo de proyecto o el RUC; los cambios de RUC o tipo se hacen primero en `00-init-update`.
- Los datos técnicos (nombre, rubro, equipo, modo de datos) **no** se cambian aquí: son de `00-init-update`.
- Texto limpio; la procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 01-make-project-brief` y muestra los avisos.
2. Base: `projectcfg.py current --step 01-make-project-brief`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/01-project-brief/`. Si no hay ninguna, indica `01-make-project-brief`.

### 2. Pedir los cambios
Pregunta qué cambia y qué valor nuevo; muestra el brief actual de esa sección. Si hay secciones «Pendiente», ofrécelas.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las secciones y filas que cambian (valor actual y nuevo), los plazos u otros textos del brief que dependen del cambio, lo que se copiará al config y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 01-make-project-brief --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`. La base no se modifica; el `README.md` de la copia anota el origen y los cambios.

### 5. Editar
1. Edita solo lo afectado de `<fork>/brief.md`.
2. `python3 .claude/skills/_shared/brief.py al-config --run <fork>` (si algo no es coherente, corrige antes de seguir).
3. Si cambió el tema, el tipo o el RUC, propón rehacer `domain.md` (con la plantilla de `01-make-project-brief/references/domain-plantilla.md`) y no lo reemplaces sin confirmación.
4. Actualiza el `README.md` del fork (lista de cambios).

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian `brief.md` y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 01-make-project-brief --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección, lo que se copió al config, si se rehízo `domain.md`, resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar según lo que cambió** (tabla de `references/dependencias.md`; solo las que ya existan en `.claude/skills/`).
