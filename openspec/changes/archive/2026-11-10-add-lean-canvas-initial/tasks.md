# Tasks

## 1. Playbook y modelos

- [x] 1.1 Escribir `common/lean/guia.md` (reglas comunes, Lean Canvas, 5 porqués, referencias APA7 verificadas y encabezados reservados para el cambio del plan Lean); verificar que cubre cada requisito de la spec `lean-canvas-initial` y que las referencias citadas existen y coinciden con `common/citation-style/APA7.md`
- [x] 1.2 Crear `common/lean/models/lean-0-cinco-porques.md`, `lean-1-canvas.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que cada plantilla tiene esas cinco partes, que el ejemplo usa contenido realista sin etiquetas de procedencia y que el README enlaza con rutas que resuelven

## 2. Validación

- [x] 2.1 Registrar la carpeta `initial-lean-canvas` en `RULES` de `validate_run.py` (el gancho `validar(run)` ya existe); verificar que las pruebas de Design Thinking y del sistema de diseño siguen pasando
- [x] 2.2 Implementar `.claude/skills/_shared/rules/lean_canvas.py` (`PREFIJOS`, nueve bloques, versión v0, cadenas de tres a cinco porqués, riesgo y orden de `SUP`) con pruebas; verificar que pasa con un canvas de ejemplo completo y que informa archivo y causa en copias con un bloque vacío, un `PRB` sin porqués, un `SUP` sin definir y supuestos desordenados

## 3. Skill 02-make-initial-lean-canvas

- [x] 3.1 Crear `.claude/skills/02-make-initial-lean-canvas/SKILL.md` (config y `domain.md`, borrador, preguntas, confirmación, cantidades de referencia, escritura, validación y registro); verificar que aparece en la lista con el nombre `02-make-initial-lean-canvas` y que cada requisito de la spec tiene una instrucción

## 4. Skill 02-make-initial-lean-canvas-update

- [x] 4.1 Crear `.claude/skills/02-make-initial-lean-canvas-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de cada `PRB`, `POR` y `SUP`); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que avisa de las citas en otras corridas

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-lean-canvas-initial --strict`, las pruebas del kit y la comprobación de que las skills `02-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `02-make-initial-lean-canvas` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-company-chapter`.
