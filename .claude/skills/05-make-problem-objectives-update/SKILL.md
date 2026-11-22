---
name: 05-make-problem-objectives-update
description: Cambia la problemática y los objetivos del capítulo 1 ya creados (secciones 1.8 a 1.10 en project/05-problem-objectives/) sin rehacerlos: copia la corrida vigente como "-fork", vuelve a copiar del brief los objetivos que cambiaron, ajusta solo las causas principales o las filas de la matriz de articulación afectadas (por ejemplo, tras un cambio en el Ishikawa, el FODA, el PESTEL o el Canvas), valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "05-make-problem-objectives-update", "actualizar la matriz de articulación", "cambiar una causa principal", "copiar los objetivos nuevos del brief" o después de un -update de 01, 03 o 04.
---

# 05-make-problem-objectives-update

Homóloga de `05-make-problem-objectives`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Suele ejecutarse después de un `-update` de `01`, `03` o `04`, para que la matriz vuelva a citar códigos y objetivos vigentes.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 05-make-problem-objectives [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso …`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/05-problem-objectives/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello (una fila de objetivos, una fila de la matriz, una causa principal); no reescribe ni reordena lo demás.
- **Los objetivos siguen al brief:** si el brief vigente cambió un `OG` u `OE`, esa fila se vuelve a copiar sin cambios; si apareció un `OE` nuevo, se agrega su fila de objetivos y su fila de la matriz; si desapareció, se quitan ambas.
- **La matriz sigue a `03` y `04`:** un código o bloque que ya no existe se reemplaza por el vigente que corresponda (con confirmación) o se quita; cada causa principal debe seguir atendida.
- **Las mismas reglas que 05:** causas principales iguales al Ishikawa, indicador igual al brief, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 05-make-problem-objectives` y muestra los avisos.
2. Base: `projectcfg.py current --step 05-make-problem-objectives`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/05-problem-objectives/`. Si no hay ninguna, indica `05-make-problem-objectives`.

### 2. Diagnóstico de lo desactualizado
Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran qué filas ya no coinciden con el brief o con las corridas vigentes de `03` y `04`. Súmalas a lo que el usuario pide cambiar.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las filas que cambian (valor actual y nuevo), los códigos que se reemplazan o quitan, cómo queda la cobertura de las causas principales y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 05-make-problem-objectives --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Edita solo las filas o rótulos afectados de `<fork>/secciones/1.8.md`, `1.9.md` o `1.10.md`.
2. Actualiza el `README.md` del fork (lista de cambios y corridas de origen vigentes).

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones previstas y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 05-make-problem-objectives --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección, filas de la matriz reemplazadas, resultado del validador, si el puntero se movió, cómo volver a la base y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
