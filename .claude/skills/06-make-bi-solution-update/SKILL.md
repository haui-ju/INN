---
name: 06-make-bi-solution-update
description: Cambia la solución de BI ya creada (secciones 2.1 a 2.3 en project/06-bi-solution/) sin rehacerla: copia la corrida vigente como "-fork", cambia solo lo pedido (una decisión, un componente o una capa de la arquitectura, una herramienta, o completa una herramienta «Pendiente» como la de ETL), actualiza lo que depende de ello, reconstruye la figura arquitectura-bi si cambió la arquitectura o las herramientas, valida, registra e indica qué skills hay que actualizar después. Úsala cuando el usuario pida "06-make-bi-solution-update", "decidir la herramienta de ETL", "cambiar un componente de la arquitectura", "cambiar una herramienta", "agregar una fuente a la arquitectura" o después de un -update de 01 o 05.
---

# 06-make-bi-solution-update

Homóloga de `06-make-bi-solution`. Parte de una corrida existente, la bifurca y edita **solo lo afectado**; lo demás queda idéntico a la base. Es la forma de completar las herramientas que quedaron «Pendiente» y de poner al día la arquitectura cuando el brief cambia sus fuentes u objetivos.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`)
- `python3 .claude/skills/_shared/runs.py fork --step 06-make-bi-solution [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <fork> --carpeta <fork>/visuales`
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 07-make-data-model-kpi` (para saber qué fuentes y tablas cita el modelo vigente)
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `references/dependencias.md` (léela antes de planear), `common/06-bi-solution/guia.md` y `models/`.

## Reglas

- **Un update solo actualiza:** cambia lo pedido y lo que depende de ello dentro de la corrida (por ejemplo, al decidir la herramienta de ETL cambian su fila de 2.3 y el nombre del componente de 2.2); no reescribe ni reordena lo demás.
- **Los códigos no se reutilizan:** un componente o herramienta nuevos toman el siguiente número libre de su prefijo; uno eliminado deja su número sin usar. Antes de eliminar un `CAP-nn`, revisa la tabla de 2.1 que lo cita.
- **Las herramientas pendientes las decide el usuario:** propón opciones con su criterio, pero escribe solo lo que elige.
- **Las mismas reglas que 06:** cuatro capas en orden, cada `FUE` y cada `OE` del brief cubiertos, Power BI en visualización, justificación y alternativa en cada herramienta, figura con `visuales.py`, texto limpio y procedencia solo en `README.md`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 06-make-bi-solution` y muestra los avisos.
2. Base: `projectcfg.py current --step 06-make-bi-solution`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/06-bi-solution/`. Si no hay ninguna, indica `06-make-bi-solution`.

### 2. Pedir los cambios
Pregunta qué se cambia (una decisión, un componente, una herramienta, una capa o completar lo pendiente); muestra la tabla actual de esa sección. Corre `python3 .claude/skills/_shared/validate_run.py <base>`: sus incidencias muestran, por ejemplo, fuentes u objetivos del brief que la arquitectura ya no cubre.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista las filas que cambian (código, valor actual y nuevo), los códigos nuevos o eliminados y quién los cita, la figura que se reconstruye y **qué skills `-update` habrá que ejecutar después**. **Espera la confirmación.**

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 06-make-bi-solution --base <base> --cambios "<cambio 1>" --cambios "<cambio 2>"`.

### 5. Editar
1. Edita solo las filas afectadas de `<fork>/secciones/2.1.md`, `2.2.md` o `2.3.md` y, si cambian las citas, `referencias.md`.
2. Si cambió la tabla de 2.2 o la de 2.3, `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <fork> --carpeta <fork>/visuales`.
3. Actualiza el `README.md` del fork (lista de cambios y herramientas que siguen pendientes).

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian las secciones, la figura, su explicación y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 06-make-bi-solution --run <fork>`.
- **Con incidencias que no puedas resolver:** conserva el fork, registra con `--no-mover` e informa cada una (archivo y causa).

### 8. Informe
Fork creado, cambios por sección, códigos nuevos y eliminados, figura reconstruida, resultado del validador, si el puntero se movió, cómo volver a la base y **la lista de skills `-update` que hay que ejecutar** según `references/dependencias.md` (solo las que ya existan en `.claude/skills/`).
