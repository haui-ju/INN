---
name: 02-design-system-update
description: Cambia un color, una tipografía, un token o un componente de un sistema de diseño ya creado, sin rehacerlo: copia la corrida vigente como "-fork", edita solo lo afectado, regenera la vista previa y valida el contraste. Úsala cuando el usuario pida "02-design-system-update", "cambiar el color de acento", "otra tipografía", "agregar un componente" sobre project/02-design-system/.
---

# 02-design-system-update

Homóloga de `02-design-system`. Parte de una corrida existente, la bifurca y edita solo lo afectado. `preview.html` es la plantilla `common/html/vista-previa/` rellena con `tokens.json`: se vuelve a copiar con el script, y todo lo demás que no depende del cambio queda idéntico a la base.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `current`, `check`, `register`, `set-diseno`)
- `python3 .claude/skills/_shared/runs.py fork --step 02-design-system [--base NOMBRE] --cambios "..."`
- `python3 .claude/skills/_shared/validate_run.py <corrida>`
- `python3 .claude/skills/02-design-system/scripts/render_preview.py <tokens.json> <preview.html> --titulo "<nombre>"`
- `references/dependencias.md`: qué archivos dependen de qué tokens y componentes (léela antes de planear).
- Playbook y plantillas: `common/02-design-system/guia.md` y `models/`.

## Flujo

### 1. Config y base
1. `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 02-design-system-update` y muestra los avisos.
2. Base: `projectcfg.py current --step 02-design-system`. **Muéstrala al usuario para confirmarla**; solo si la rechaza, lista las de `project/02-design-system/`. Si no hay ninguna, indica `02-design-system`.

### 2. Pedir los cambios
Pregunta qué cambia: **color** (acento, estado, superficie), **tipografía**, **espacio, radio o sombra**, **un componente** (estados, tokens, regla) o **un componente nuevo**. Si el pedido es ambiguo, pregunta.

### 3. Plan con confirmación (antes de escribir)
Con `references/dependencias.md`: lista los archivos que se tocarán y los efectos en cadena (por ejemplo: cambiar `acento` afecta `tokens.json`, la tabla de color y los componentes que lo citan en `DESIGN.md`, y obliga a regenerar `preview.html`). **Calcula el contraste** de los pares afectados en claro y oscuro y muéstralo. Si un par no cumple AA, propón un ajuste. Espera la confirmación.

### 4. Bifurcar
`python3 .claude/skills/_shared/runs.py fork --step 02-design-system --base <base> --cambios "<cambio>"`. La base no se modifica; el `README.md` de la copia anota el origen y los cambios.

### 5. Editar solo lo afectado
1. `tokens.json`: el cambio, manteniendo las mismas claves en claro y oscuro y los `pares`.
2. `DESIGN.md`: las tablas y componentes que citan los tokens cambiados (no reescribas el resto).
3. `preview.html`: **vuelve a generarlo** con `render_preview.py` (no se edita a mano).
4. No toques `README.md` salvo para ampliar la lista de cambios.

### 6. Validar
`python3 .claude/skills/_shared/validate_run.py <fork>` hasta que no haya incidencias. Comprueba con `diff -rq <base> <fork>` que solo cambian los archivos del plan, `preview.html` y `README.md`.

### 7. Registrar
- **Sin incidencias:** `projectcfg.py register --step 02-design-system --run <fork>` y `projectcfg.py set-diseno --value project/02-design-system/<fork>/DESIGN.md`.
- **Con incidencias que no puedas resolver (por ejemplo un contraste que el usuario insiste en mantener):** conserva el fork, registra con `--no-mover`, no cambies `diseno` e informa cada incidencia (archivo y causa).

### 8. Informe
Carpeta del fork, cambios por archivo, contrastes antes y después, resultado del validador, si el puntero y `diseno` se movieron y cómo volver a la base (editar `run` y `diseno` en `project/config.yaml`). Si hay HTML ya generado con el diseño anterior (tableros, informe), avisa que no se actualiza aquí.
