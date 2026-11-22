---
name: 02-design-system
description: Define el sistema de diseño del proyecto (cálido, editorial y profesional, estilo Claude: acento terracota, titulares serif y texto sans): tokens, DESIGN.md y una vista previa HTML autónoma en claro y oscuro, dentro de project/02-design-system/. Úsala cuando el usuario pida "02-design-system", "sistema de diseño", "DESIGN.md", "paleta y tipografía" o antes de generar los visuales HTML del diagnóstico o el informe. Para cambiar uno ya creado usa 02-design-system-update.
---

# 02-design-system

Crea la identidad visual única del proyecto. Las demás skills (los visuales del capítulo 1, `12-make-report` y la maqueta del dashboard) leen el resultado desde el config.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/02-design-system/guia.md` (playbook: principios, tokens, accesibilidad, componentes, HTML autónomo).
2. `common/02-design-system/models/README.md` y las plantillas `ds-*.md` (formato de cada entregable).
3. `project/config.yaml` (tema, rubro, tipo de proyecto, nombre) y, si existe, `project/domain.md`.

## Recursos de la skill

- `references/tokens-base.json`: tokens por defecto con contraste AA verificado. Cópialos y cambia solo lo que el usuario pida.
- `references/design-base.md`: `DESIGN.md` completo y coherente con esos tokens; es el modelo de estructura.
- `scripts/render_preview.py <tokens.json> <preview.html> --titulo "<nombre>"`: copia la plantilla `common/html/vista-previa/` con los tokens (React, Tailwind y fuentes incrustados; tema claro por defecto y oscuro con el botón; botones «Copiar imagen» y «Descargar imagen»).
- Kit compartido `.claude/skills/_shared/`: `projectcfg.py`, `runs.py`, `validate_run.py` (reglas en `rules/design_system.py`).

## Reglas

- Pregunta solo lo que el config y `domain.md` no traen, propone un sistema completo y **espera la confirmación antes de escribir**.
- **Un solo acento.** Los colores de estado solo comunican estados.
- `tokens.json` es la única fuente de valores; `DESIGN.md` y `preview.html` deben coincidir con él.
- Sin recursos externos en `preview.html`: pila de fuentes del sistema. Si el usuario pide una fuente concreta, decláraselo con respaldo del sistema y avísale que no se incrusta.
- Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado. Los ejemplos son contenido realista y neutro del proyecto.
- Claude Design es opcional: puedes mencionarlo si el usuario quiere explorar o publicar una vista privada, pero no es parte de este flujo.

## Flujo

1. **Config.** `python3 .claude/skills/_shared/projectcfg.py validate`. Si falla, detente e indica `00-init`. Luego `projectcfg.py check --skill 02-design-system` y muestra los avisos (no bloquean).
2. **Preguntas** (ficha `ds-0-brief`; AskUserQuestion): tono (formal, cercano, técnico), dos o tres referencias visuales, colores de marca si existen, tipografía preferida y si quiere modo oscuro (sí por defecto). Si ya hay una corrida en el config (`projectcfg.py current --step 02-design-system`), avisa que se creará otra versión y ofrece `02-design-system-update` para cambios pequeños.
3. **Propuesta.** Parte de `references/tokens-base.json`; si el usuario aportó un color de marca, úsalo como `acento` y ajusta la luminosidad del tema oscuro para mantener AA. Muestra un resumen: paleta clara y oscura (hex), tipografía, escala de espacio y radio, y los seis componentes. Avisa en una línea si algo sale de las cantidades de referencia (guía 0.6).
4. **Confirmación.** Espera la respuesta; si pide cambios, actualiza y muestra de nuevo. No escribas nada hasta que confirme.
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 02-design-system)` y escribe en `$RUN`:
   - `tokens.json` (ficha `ds-1-tokens`).
   - `DESIGN.md` con la estructura de `ds-3-design-md` y los componentes de `ds-2-componentes`, tomando `references/design-base.md` como modelo; las tablas repiten `tokens.json`.
   - `preview.html`: `python3 .claude/skills/02-design-system/scripts/render_preview.py $RUN/tokens.json $RUN/preview.html --titulo "<nombre del proyecto>"`.
   - `README.md` con la procedencia (modo de datos del config y la lista de decisiones del brief). Es el único lugar donde se anota.
6. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige las incidencias (contraste, tokens, componentes, recursos externos) y repite hasta que no haya.
7. **Registrar.**
   - `python3 .claude/skills/_shared/projectcfg.py register --step 02-design-system --run <carpeta>`
   - `python3 .claude/skills/_shared/projectcfg.py set-diseno --value project/02-design-system/<carpeta>/DESIGN.md`
   Si la salida dice que el paso está fijado o `"movido": false`, díselo al usuario: `diseno` no cambió y puede editar el config a mano.
8. **Cierre.** Entrega la ruta de la corrida, un resumen de la paleta y los componentes, el resultado del validador, cómo abrir `preview.html` y los supuestos que tomaste para que el usuario los corrija.
