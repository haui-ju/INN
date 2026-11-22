---
name: 03-make-business-diagnosis-update
description: Cambia el diagnóstico del negocio ya creado (secciones 1.1 a 1.4 en project/03-business-diagnosis/) sin rehacerlo: copia la corrida vigente como "-fork", cambia solo lo pedido (datos de la empresa, reseña, misión o visión copiadas de domain.md, industria, ventas, UIT o categoría de tamaño, o un bloque del Business Model Canvas), vuelve a construir la figura bmc si cambió el Canvas, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "03-make-business-diagnosis-update", "cambiar la misión", "corregir el tamaño de la empresa", "actualizar la UIT", "cambiar un bloque del Canvas" o "completar lo pendiente del diagnóstico".
---

# 03-make-business-diagnosis-update

Homóloga de `03-make-business-diagnosis`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Como `04` y `05` leen esta corrida, al cerrar dice cuáles hay que actualizar.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 03-make-business-diagnosis [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/visuales.py construir --visual bmc --run <fork> --carpeta <fork>/visuales`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/03-business-diagnosis/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (por ejemplo, ventas en UIT y categoría si cambian las ventas o la UIT); no reescribe ni reordena lo demás.
- **Misión, visión y datos de la empresa siguen a `domain.md`:** si el usuario los cambia, se corrige primero `domain.md` (con su confirmación) y luego la sección; el validador compara ambos.
- **Lo pendiente se completa aquí** con datos que da el usuario o que se verifican con su fuente; no se inventan.
- **Las mismas reglas que 03:** encabezados exactos, RUC según el tipo, tamaño por la Ley 30056, nueve bloques con nombre exacto, figura con `visuales.py`, citas en `referencias.md`, texto limpio y procedencia solo en `README.md`.
- El tipo de proyecto o el RUC se cambian con `00-init-update`; el tema o la problemática, con `01-make-project-brief-update`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 03-make-business-diagnosis` y muestra los avisos.
2. Base: `projectcfg.py current --step 03-make-business-diagnosis`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/03-business-diagnosis/`. Si no hay ninguna, indica `03-make-business-diagnosis`.

### 2. Pedir los cambios
Pregunta qué cambia y el valor nuevo; muestra el texto actual de esa sección. Si hay datos «Pendiente» (ventas, UIT), ofrécelos.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las secciones y filas que cambian (valor actual y nuevo), lo que se recalcula (ventas en UIT, categoría), si hay que corregir antes `domain.md`, si se reconstruye la figura `bmc` y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 03-make-business-diagnosis --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`. La base no se modifica; el `README.md` de la copia anota el origen y los cambios.

### 5. Editar
1. Si el cambio toca misión, visión o datos generales, corrige primero `project/domain.md` (con confirmación).
2. Edita solo las secciones afectadas de `<fork>/secciones/` y, si cambian las citas, `referencias.md`.
3. Si cambió `secciones/1.4.md` (o el nombre comercial de 1.1), `python3 .claude/skills/_shared/visuales.py construir --visual bmc --run <fork> --carpeta <fork>/visuales`.
4. Actualiza el `README.md` del fork (lista de cambios).

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones afectadas, la figura (si tocaba), `referencias.md` y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 03-make-business-diagnosis --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección, si se corrigió `domain.md`, si se reconstruyó la figura, resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
