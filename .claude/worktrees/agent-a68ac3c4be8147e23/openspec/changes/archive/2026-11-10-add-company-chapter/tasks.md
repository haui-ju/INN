# Tasks

## 1. Playbook y modelos

- [x] 1.1 Escribir `common/company/guia.md` (secciones 0 a 7 de la decisión D7: reglas, presentación, diagnóstico, objetivos, justificación y alcances, adaptación a proyecto propio, referencias APA7 verificadas, errores y checklist); verificar que cubre cada requisito de la spec `company-chapter` y que las referencias existen y coinciden con `common/citation-style/APA7.md`
- [x] 1.2 Crear `common/company/models/emp-1-presentacion.md`, `emp-2-diagnostico.md`, `emp-3-objetivos.md`, `emp-4-justificacion-alcance.md` y `README.md` con ficha, instrucciones (incluida la variante de proyecto propio), formato, ejemplo y checklist; verificar que cada plantilla tiene esas partes, que el ejemplo no lleva etiquetas de procedencia y que los enlaces del README resuelven

## 2. Validación

- [x] 2.1 Registrar la carpeta `company-chapter` en `RULES` de `validate_run.py` (el gancho `validar(run)` ya existe); verificar que las pruebas de Design Thinking, del sistema de diseño y del Lean Canvas siguen pasando
- [x] 2.2 Implementar `.claude/skills/_shared/rules/company.py` (`PREFIJOS`, secciones 1.1 a 1.6, título de 1.1 según el tipo, evidencia del FODA, objetivos medibles y ligados a `OG-01`, coherencia de 1.3 con el canvas vigente), con pruebas que usen como fixture los ejemplos de las plantillas y un canvas generado con el formato de `lean-canvas-initial`; verificar que pasa con un capítulo completo de cada tipo y que informa archivo y causa en copias con una sección ausente, un `OE` sin métrica, un `FOR` sin definir y un 1.3 distinto del canvas

## 3. Skill 03-make-company-chapter

- [x] 3.1 Crear `.claude/skills/03-make-company-chapter/SKILL.md` (confirmación del tipo, fuentes, datos modelados, plan con confirmación, escritura por bloques, armado de `capitulo-1.md`, `README.md` de procedencia, validación y registro); verificar que aparece en la lista con el nombre `03-make-company-chapter` y que cada requisito de la spec tiene una instrucción

## 4. Skill 03-make-company-chapter-update

- [x] 4.1 Crear `.claude/skills/03-make-company-chapter-update/SKILL.md` y `references/dependencias.md` (qué bloques y partes del capítulo dependen de cada código y cómo se relaciona 1.3 con el canvas); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que avisa de las citas de `OE` en otras corridas

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-company-chapter --strict`, las pruebas del kit y la comprobación de que las skills `03-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `03-make-company-chapter` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-methodological-framework`.
