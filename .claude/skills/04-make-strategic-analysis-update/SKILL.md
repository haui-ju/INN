---
name: 04-make-strategic-analysis-update
description: Cambia el análisis estratégico ya creado (secciones 1.5 a 1.7 en project/04-strategic-analysis/) sin rehacerlo: copia la corrida vigente como "-fork", agrega, corrige o elimina solo lo pedido (un hallazgo PESTEL o su fuente, un ítem FODA, una estrategia cruzada o una causa del Ishikawa) sin reutilizar códigos, reconstruye las figuras pestel, foda o ishikawa que cambien, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "04-make-strategic-analysis-update", "agregar una amenaza", "cambiar una estrategia FO", "corregir el PESTEL", "quitar una causa del Ishikawa" o "actualizar la fuente de un hallazgo".
---

# 04-make-strategic-analysis-update

Homóloga de `04-make-strategic-analysis`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Como `05` cita estos códigos, al cerrar dice si hay que actualizar la matriz de articulación.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 04-make-strategic-analysis [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/visuales.py construir --visual <pestel|foda|ishikawa> --run <fork> --carpeta <fork>/visuales`
- `python3 .claude/skills/_shared/diagnostico.py leer --paso 05-make-problem-objectives` (para saber qué códigos cita la matriz vigente)
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/04-strategic-analysis/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (por ejemplo, la evidencia de una oportunidad que citaba un hallazgo PESTEL eliminado); no reescribe ni reordena lo demás.
- **Los códigos no se reutilizan:** un ítem nuevo toma el siguiente número libre de su prefijo; uno eliminado deja su número sin usar. Antes de eliminar, revisa quién lo cita (estrategias, causas, matriz de `05`).
- **Las mismas reglas que 04:** fuentes verificadas con año, articulación PESTEL → FODA → Ishikawa, estrategias de los cuatro tipos bien combinadas, efecto igual al problema del brief, categorías 6M, figuras con `visuales.py`, texto limpio y procedencia solo en `README.md`.
- El problema principal (efecto) se cambia en el brief con `01-make-project-brief-update`, y después aquí se copia.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 04-make-strategic-analysis` y muestra los avisos.
2. Base: `projectcfg.py current --step 04-make-strategic-analysis`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/04-strategic-analysis/`. Si no hay ninguna, indica `04-make-strategic-analysis`.

### 2. Pedir los cambios
Pregunta qué se agrega, corrige o elimina; muestra la tabla actual de esa sección. Si el brief cambió su problema principal, ofrece copiarlo al efecto del Ishikawa.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las filas que cambian (código, valor actual y nuevo), los códigos nuevos, los que se eliminan y quién los cita (evidencias, estrategias, causas y la matriz de `05`), las figuras que se reconstruyen y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 04-make-strategic-analysis --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Edita solo las filas afectadas de `<fork>/secciones/1.5.md`, `1.6.md` o `1.7.md` y, si cambian las fuentes, `referencias.md`. Verifica toda fuente nueva.
2. Por cada sección cambiada, `python3 .claude/skills/_shared/visuales.py construir --visual <visual> --run <fork> --carpeta <fork>/visuales`. Si lo cambiado altera lo que la figura dice, pasa un `--interpretacion "<texto>"` nuevo (reglas en el paso de 04); si no, se conserva el anterior.
3. Actualiza el `README.md` del fork (lista de cambios).

### 6. Revisar la redacción y validar
Si el cambio tocó texto, invoca al agente `revisor-redactor` (subagent_type `revisor-redactor`) con las rutas de las secciones editadas del fork; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después:

`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones, figuras y archivos previstos.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 04-make-strategic-analysis --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección, códigos nuevos y eliminados, figuras reconstruidas, resultado del validador, si el puntero se movió, cómo volver a la base y **la lista de skills `-update` que hay que ejecutar** (por ejemplo `05-make-problem-objectives-update` si la matriz citaba un código cambiado o eliminado; solo las que ya existan en `.claude/skills/`).
