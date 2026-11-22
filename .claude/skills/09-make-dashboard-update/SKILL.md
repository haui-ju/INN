---
name: 09-make-dashboard-update
description: Cambia el dashboard ya documentado (sección 3.2 y anexos C y D en project/09-dashboard/) sin rehacerlo: copia la corrida vigente como "-fork", cambia solo lo pedido (una página, una medida, el valor real de un KPI, una captura o una meta que se cerró en 2.5), mantiene valores.json, las capturas y los textos de acuerdo, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "09-make-dashboard-update", "cambiar el dashboard", "nueva captura", "actualizar un valor del dashboard", "cambiar una medida" o "ajustar una página". Para crear el capítulo desde cero usa 09-make-dashboard.
---

# 09-make-dashboard-update

Homóloga de `09-make-dashboard`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. **El equipo sigue siendo quien mide:** un valor, una captura o una medida nueva los entrega el equipo; la skill los registra y redacta.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 09-make-dashboard [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/dashboard_dax.py <modelo.json>` (borrador de una medida nueva)
- `python3 .claude/skills/_shared/dashboard_ref.py construir --run <fork>` (regenera `materiales/` desde `materiales/paginas.json`)
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 07-make-data-model-kpi`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/09-dashboard/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (un valor nuevo obliga a recalcular el estado en 3.2 y la lectura que lo cite); no reescribe ni reordena lo demás.
- **Los valores y las capturas los entrega el equipo.** `valores.json`, `capturas/pag-nn.png` y la medida final se actualizan con lo que el equipo traiga; sin eso, no cambies una cifra.
- **`valores.json` sigue a 3.2:** todo valor de 3.2 se repite en el JSON en el mismo paso; la validación compara ambos.
- **Meta cerrada:** si el equipo cerró una meta con `07-make-data-model-kpi-update`, actualiza la `meta` de `valores.json`, la fila de 3.2 y quita el KPI de «Metas pendientes». Si `valores.json` trae una meta y 2.5 sigue «Pendiente», no valida.
- **Los códigos no se reutilizan:** una página o una medida nueva toman el siguiente número libre; una eliminada deja su número sin usar. Antes de eliminar una página, revisa su captura, su descripción en el anexo D y los KPI que muestra.
- **Las mismas reglas que 09:** cada KPI en una página, usuario del brief, DAX que cita solo el modelo y sin `revisar`, capturas marcadas una vez en 3.2, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 09-make-dashboard` y muestra los avisos.
2. Base: `projectcfg.py current --step 09-make-dashboard`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/09-dashboard/`. Si no hay ninguna, indica `09-make-dashboard`.

### 2. Pedir los cambios
Pregunta qué se cambia (una página, una medida, un valor, una captura o una meta); muestra lo actual. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran, por ejemplo, un KPI nuevo de `modelo.json` que todavía no está en ninguna página.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista lo que cambia (valor actual y nuevo), lo que se recalcula (estado, lectura), qué debe traer el equipo y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 09-make-dashboard --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Con lo que el equipo entregó, edita `<fork>/valores.json` y `<fork>/capturas/` y repite el cambio en `<fork>/secciones/3.2.md` (tabla de valores, estado, lectura) y en los anexos que dependan de él.
2. Si cambian páginas, visuales o medidas, edita `<fork>/materiales/paginas.json` y regenera el dashboard de referencia y su guía con `dashboard_ref.py construir --run <fork>`; si solo cambian valores o capturas, no hace falta.
3. Un cambio de medida se hace en el anexo C (la final del equipo) y en la tabla de medidas; si es nueva, propón un borrador con `dashboard_dax.py` y espera la medida que el equipo ejecutó.
4. Actualiza el `README.md` del fork (lista de cambios y metas que siguen pendientes).

### 6. Revisar la redacción y validar
Si el cambio tocó texto, invoca al agente `revisor-redactor` (subagent_type `revisor-redactor`) con las rutas de las secciones o anexos editados del fork; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después:

`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones, los anexos, `valores.json`, las capturas y `README.md` previstos (reemplazar una captura no toca el anexo C).

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 09-make-dashboard --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por archivo, valores recalculados, resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
