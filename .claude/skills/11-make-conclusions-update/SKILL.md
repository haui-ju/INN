---
name: 11-make-conclusions-update
description: Cambia las conclusiones ya redactadas (sección 5 en project/11-conclusions/) sin rehacerlas: copia la corrida vigente como "-fork", cambia solo lo pedido (la conclusión de un objetivo y las recomendaciones ligadas a ella cuando cambia un valor real o se cierra una meta, una recomendación, una lección o la limitación), recalcula el estado con el valor real frente a la meta, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "11-make-conclusions-update", "cambiar una conclusión", "actualizar las conclusiones", "se cerró una meta", "cambió un valor del dashboard" o "ajustar una recomendación". Para crear la sección desde cero usa 11-make-conclusions.
---

# 11-make-conclusions-update

Homóloga de `11-make-conclusions`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. **El estado se recalcula con los valores reales**: un valor o una meta nuevos los entrega el equipo (en `09-make-dashboard-update`) o se cierran en `07-make-data-model-kpi-update`; esta skill los refleja en la sección 5.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/rules/conclusions.py estados [--json]` (estados recalculados con el `valores.json` y las metas vigentes)
- `python3 .claude/skills/_shared/runs.py fork --step 11-make-conclusions [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/brief.py leer`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear) y `common/11-conclusions/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello. Un valor o una meta nuevos cambian la conclusión del objetivo que mide ese KPI, su fila del respaldo, las recomendaciones ligadas a esa conclusión y, si cambia su estado, la conclusión del objetivo general; no reescribe ni reordena lo demás.
- **El estado es el calculado.** Tras el cambio, corre `rules/conclusions.py estados` y usa el estado que imprime; no lo opines.
- **No se inventa una meta ni un valor.** Un KPI sin meta sigue sin concluirse hasta que `07-make-data-model-kpi-update` cierre la meta y `09-make-dashboard-update` actualice `valores.json`.
- **Cambia de estado ⇒ cambia la recomendación.** Una conclusión que pasa a `Cumplido` ya no necesita recomendación (eliminarla deja su número sin usar); una que deja de cumplir necesita al menos una, con quién decide y su KPI.
- **Los códigos no se reutilizan:** una conclusión, recomendación o lección nueva toma el siguiente número libre.
- **Las mismas reglas que 11:** una conclusión por objetivo, respaldo con valores de `valores.json` y metas de 2.5, meta pendiente declarada, lecciones y limitación de datos generados, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 11-make-conclusions` y muestra los avisos.
2. Base: `projectcfg.py current --step 11-make-conclusions`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/11-conclusions/`. Si no hay ninguna, indica `11-make-conclusions`.

### 2. Pedir los cambios
Pregunta qué cambia (un valor del dashboard, una meta que se cerró, una recomendación, una lección o la limitación) y muestra lo actual. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran qué conclusión ya no concuerda con los valores vigentes.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las conclusiones que cambian de estado (estado actual y nuevo, con valor y meta), sus filas de respaldo, las recomendaciones que se modifican, se agregan o se eliminan, y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 11-make-conclusions --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`. La base no se modifica.

### 5. Editar
1. Edita en `<fork>/secciones/5.md` solo lo afectado: la fila de la conclusión (estado y texto), su fila de respaldo (valor y estado del KPI), las recomendaciones ligadas y, si cambió, la conclusión del objetivo general.
2. Si cambió una meta o el estado de un KPI, comprueba que el texto de «meta pendiente» sigue siendo cierto.
3. Actualiza el `README.md` del fork (lista de cambios y metas que siguen pendientes).

### 6. Revisar la redacción y validar
Si el cambio tocó texto, invoca al agente `revisor-redactor` (subagent_type `revisor-redactor`) con la ruta de `<fork>/secciones/5.md`; aplica con Edit solo lo que el usuario apruebe. Después:

`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian `secciones/5.md` y `README.md`, y que dentro de 5 solo cambian las filas previstas.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 11-make-conclusions --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, conclusiones que cambiaron de estado, recomendaciones modificadas, resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
