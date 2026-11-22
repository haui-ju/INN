---
name: 07-make-data-model-kpi-update
description: Cambia el modelo de datos y los KPI ya creados (secciones 2.4 y 2.5 y modelo.json en project/07-data-model-kpi/) sin rehacerlos: copia la corrida vigente como "-fork", cambia solo lo pedido (una tabla de hechos o su granularidad, una medida, una dimensión o un atributo, una relación, un KPI, su meta o su frecuencia), mantiene modelo.json igual a las secciones, reconstruye la figura modelo-datos si cambió el modelo, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "07-make-data-model-kpi-update", "agregar un KPI", "cambiar una meta", "agregar una dimensión", "agregar una medida", "cambiar una relación" o después de un -update de 01, 05 o 06.
---

# 07-make-data-model-kpi-update

Homóloga de `07-make-data-model-kpi`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Cada cambio se hace a la vez en las secciones y en `modelo.json`.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 07-make-data-model-kpi [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <fork> --carpeta <fork>/visuales`
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution` (objetivos del brief y fuentes de la arquitectura vigente)
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/07-data-model-kpi/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (por ejemplo, una medida nueva obliga a revisar los KPI que la usan y la fila de `modelo.json`); no reescribe ni reordena lo demás.
- **`modelo.json` sigue a las secciones:** todo cambio en 2.4 o 2.5 se repite en el JSON en el mismo paso; la validación compara ambos.
- **Los códigos no se reutilizan:** una tabla, relación o KPI nuevos toman el siguiente número libre de su prefijo; uno eliminado deja su número sin usar. Antes de eliminar una tabla o un campo, revisa las relaciones y los KPI que lo citan.
- **Las mismas reglas que 07:** granularidad y agregación en cada hecho, dimensiones relacionadas, dimensión de tiempo si hay KPI por periodo, cada `OE` con KPI (uno con el nombre de su indicador), campos de origen dentro del modelo, meta o «Pendiente», figura con `visuales.py`, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 07-make-data-model-kpi` y muestra los avisos.
2. Base: `projectcfg.py current --step 07-make-data-model-kpi`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/07-data-model-kpi/`. Si no hay ninguna, indica `07-make-data-model-kpi`.

### 2. Pedir los cambios
Pregunta qué se cambia (una tabla, una medida, una dimensión, una relación o un KPI); muestra la tabla actual. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran, por ejemplo, un `OE` nuevo del brief que todavía no tiene KPI.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las filas que cambian (código, valor actual y nuevo), los códigos nuevos o eliminados y quién los cita (relaciones, KPI, `modelo.json`), la figura que se reconstruye y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 07-make-data-model-kpi --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Edita solo las filas afectadas de `<fork>/secciones/2.4.md` o `2.5.md` y, si cambian las citas, `referencias.md`.
2. Repite el mismo cambio en `<fork>/modelo.json`.
3. Si cambió el modelo (tablas, medidas, claves, relaciones), `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <fork> --carpeta <fork>/visuales`.
4. Actualiza el `README.md` del fork (lista de cambios y metas que siguen pendientes).

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones, `modelo.json`, la figura, su explicación y `README.md` previstos (un KPI nuevo no toca 2.4 ni la figura).

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 07-make-data-model-kpi --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección y en `modelo.json`, códigos nuevos y eliminados, figura reconstruida (o no), resultado del validador, si el puntero se movió, cómo volver a la base y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
