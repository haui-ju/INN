---
name: 10-make-storytelling-update
description: Cambia la narrativa ya redactada (sección 4 y capturas en project/10-storytelling/) sin rehacerla: copia la corrida vigente como "-fork", actualiza solo los hallazgos que citan un valor del dashboard que cambió en 09-make-dashboard (valor, estado, brecha y la narrativa que los cita), agrega o quita un hallazgo, cambia una captura o una decisión, mantiene la tabla, las cifras y las capturas de acuerdo con valores.json, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "10-make-storytelling-update", "actualizar los hallazgos", "cambió un valor del dashboard", "agregar un hallazgo" o "cambiar la decisión de un hallazgo". Para crear la sección desde cero usa 10-make-storytelling.
---

# 10-make-storytelling-update

Homóloga de `10-make-storytelling`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. **Los valores los sigue entregando el equipo:** la skill no mide ni corrige un valor, solo actualiza lo que lo cita.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 10-make-storytelling [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 07-make-data-model-kpi`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/10-storytelling/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la sección (un valor nuevo obliga a recalcular el estado, la brecha y la narrativa del hallazgo que lo cita); no reescribe ni reordena los demás hallazgos.
- **Un valor cambiado en 09 actualiza solo los hallazgos que citan ese KPI.** Para encontrarlos, corre `validate_run.py` sobre la base: sus incidencias nombran cada hallazgo cuya cifra ya no coincide con `valores.json`. Los demás no se tocan.
- **Las cifras siguen a `valores.json` de 09:** el valor de la tabla, el estado (con el comparador de la meta), la brecha en puntos y toda cifra de la narrativa del hallazgo se recalculan juntos. Si el estado cambió (de «No cumple» a «Cumple»), revisa también la decisión y las prioridades.
- **Los códigos no se reutilizan:** un hallazgo nuevo toma el siguiente número libre; uno eliminado deja su número sin usar. Antes de eliminar uno, comprueba que su objetivo siga con otro hallazgo y mueve su captura si la compartía.
- **Las capturas se copian de 09** sin modificarlas, y cada una se marca una sola vez. Si cambió una captura en 09, vuelve a copiarla.
- **Las mismas reglas que 10:** objetivo con hallazgo, KPI que mide ese objetivo, decisión de un usuario del brief, declaración de datos generados, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 10-make-storytelling` y muestra los avisos. Si la corrida vigente de 09 no trae `valores.json`, detente.
2. Base: `projectcfg.py current --step 10-make-storytelling`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/10-storytelling/`. Si no hay ninguna, indica `10-make-storytelling`.

### 2. Pedir los cambios
Pregunta qué cambia (un valor de 09, un hallazgo, una captura o una decisión) y muestra lo actual. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: si cambió un valor en 09, sus incidencias listan los hallazgos afectados.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista los hallazgos que cambian (valor actual y nuevo, estado actual y nuevo), las frases de la narrativa que citan la cifra, si cambia el orden de prioridades y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 10-make-storytelling --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`. La base no se modifica.

### 5. Editar
1. En `<fork>/secciones/4.md`, edita solo los hallazgos afectados: su fila de la tabla (valor real y estado), las cifras de su `**Qué muestra.**` (valor, meta y brecha) y, si el estado cambió, su decisión y `**Prioridades.**`.
2. Si cambió una captura, copia de nuevo `pag-nn.png` (y `pag-nn.md`) desde la corrida de 09 a `<fork>/capturas/`.
3. Si se agrega o quita un hallazgo, mantén cada objetivo con al menos uno y cada captura marcada una sola vez.
4. Actualiza el `README.md` del fork (lista de cambios y metas que siguen pendientes).

### 6. Revisar la redacción y validar
Si el cambio tocó texto, invoca al agente `revisor-redactor` (subagent_type `revisor-redactor`) con la ruta de `<fork>/secciones/4.md`; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después:

`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian `secciones/4.md`, las capturas y `README.md` previstos.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 10-make-storytelling --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, hallazgos cambiados (valor y estado antes y después), resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
