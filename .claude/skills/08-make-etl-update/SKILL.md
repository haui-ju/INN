---
name: 08-make-etl-update
description: Cambia el ETL ya documentado (sección 3.1 y anexos A y B en project/08-etl/) sin rehacerlo: copia la corrida vigente como "-fork", cambia solo lo pedido (una regla de calidad, un paso o su código, una cifra de la evidencia que el equipo corrigió, el volumen o la semilla de los datos), mantiene evidencia.json, 3.1 y el anexo A de acuerdo, vuelve a comparar con la hoja de respuestas, valida, registra e indica qué skills hay que actualizar después. Si se regeneran los datos, marca la evidencia anterior como desactualizada hasta que el equipo repita el ETL. Úsala cuando el usuario pida "08-make-etl-update", "corregir una cifra del ETL", "agregar una regla de calidad", "cambiar un paso", "regenerar los datos" o después de un -update de 06 o 07. Para crear el capítulo desde cero usa 08-make-etl.
---

# 08-make-etl-update

Homóloga de `08-make-etl`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Una cifra cambia a la vez en la evidencia, en 3.1 y en el anexo A.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 08-make-etl [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/datagen.py` (`parametros`, `generar --confirmar`, `verificar`) y `python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia <ruta> --actualizar`
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution` (fuentes del brief y arquitectura vigente)
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/08-etl/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (una regla nueva obliga a revisar la hoja de defectos, el anexo A y los pasos que la aplican); no reescribe ni reordena lo demás.
- **La evidencia manda.** Una cifra nueva la da el equipo: se escribe primero en `evidencia.json` y luego en 3.1 y en el anexo A. No se estima ni se corrige a ojo.
- **Los códigos no se reutilizan:** una regla o un paso nuevos toman el siguiente número libre; uno eliminado deja su número sin usar. Antes de eliminar un paso, revisa su bloque del anexo B y las reglas que lo citan.
- **Datos regenerados = evidencia vieja.** Si cambian la semilla o el volumen, la hoja de respuestas cambia: renombra `evidencia.json` del fork a `evidencia-desactualizada.json` y no redactes cifras nuevas hasta que el equipo repita el ETL y traiga la evidencia nueva. Al regenerar los datos, vuelve a generar la guía del fork con `python3 .claude/skills/_shared/etl_guia.py construir --run <fork>` para que sus puntos de control sigan la nueva hoja de respuestas.
- **Las mismas reglas que 08:** solo la evidencia, cada defecto con su regla, campos del modelo con origen, pasos con su código, datos generados declarados, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 08-make-etl` y muestra los avisos.
2. Base: `projectcfg.py current --step 08-make-etl`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/08-etl/`. Si no hay ninguna, indica `08-make-etl`.

### 2. Pedir los cambios
Pregunta qué se cambia (una regla, un paso, una cifra, el código de un script, el volumen o la semilla de los datos); muestra la fila actual. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran, por ejemplo, un defecto nuevo de la hoja de respuestas que todavía no tiene regla.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las filas que cambian (código, valor actual y nuevo), dónde se repiten (evidencia, 3.1, anexo A, anexo B), si hay que volver a comparar con la hoja de respuestas y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 08-make-etl --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Si cambian los datos: confirma los parámetros con el usuario (`datagen.py parametros`), ejecuta `generar --confirmar` y `verificar`, renombra la evidencia del fork a `evidencia-desactualizada.json`, avisa que el equipo debe repetir el ETL y detente.
2. Si cambia una cifra o se agrega una regla: edita primero `<fork>/evidencia.json` con lo que el equipo trajo; después las filas afectadas de `<fork>/secciones/3.1.md` y de `<fork>/anexos/A.md`, y, si cambia un paso, su bloque de `<fork>/anexos/B.md`.
3. Vuelve a comparar: `python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia <fork>/evidencia.json --actualizar` y ajusta la «Verificación» de 3.1.
4. Actualiza el `README.md` del fork (lista de cambios).

### 6. Revisar la redacción y validar
Si el cambio tocó texto, invoca al agente `revisor-redactor` (subagent_type `revisor-redactor`) con las rutas de lo editado del fork; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después:

`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian `evidencia.json`, 3.1, el anexo A (y el B si cambió un paso) y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 08-make-etl --run <fork>`.
- **Con incidencias que no puedas resolver (por ejemplo, evidencia desactualizada):** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por archivo, resultado de la comparación con la hoja de respuestas, resultado del validador, si el puntero se movió, cómo volver a la base (editar `run` en `project/config.yaml`) y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
