# Tasks

## 1. Playbook y modelos

- [x] 1.1 Verificar por búsqueda las fuentes candidatas (Brown 2008, Ries 2011, Little 2014, Schwaber y Sutherland 2020, Anderson 2010, Anderson y Carmichael 2016) y escribir `common/methodological-framework/guia.md` (qué cubre cada metodología, criterio de elección, integración, glosario con términos obligatorios y opcionales, errores frecuentes, checklist y referencias APA 7 verificadas); verificar que cubre cada requisito de la spec `methodological-framework` y que solo cita fuentes confirmadas
- [x] 1.2 Crear en `common/methodological-framework/models/` las plantillas `mar-1-innovacion.md`, `mar-2-agiles.md`, `mar-3-integracion.md`, `mar-4-glosario.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que cada plantilla tiene esas partes, que los ejemplos no llevan etiquetas de procedencia y que los enlaces del README resuelven

## 2. Validación

- [x] 2.1 Registrar la carpeta `methodological-framework` en `RULES` de `validate_run.py`; verificar que las pruebas de los demás pasos siguen pasando
- [x] 2.2 Implementar `.claude/skills/_shared/rules/methodological_framework.py` (secciones, etiquetas por metodología, integración y puntos del índice, glosario, citas y referencias) con pruebas que usen como fixture los ejemplos de las plantillas; verificar que pasa con un capítulo completo y que informa archivo y causa en copias con una etiqueta ausente, una metodología sin fila en 2.3, un punto inexistente, un término obligatorio ausente, un glosario desalineado y una cita fuera de la lista

## 3. Skill 04-make-methodological-framework

- [x] 3.1 Crear `.claude/skills/04-make-methodological-framework/SKILL.md` (config, metodologías propuestas desde `pipeline.json`, profundidad, términos del negocio, plan con confirmación, escritura, validación y registro); verificar que aparece en la lista con el nombre `04-make-methodological-framework` y que cada requisito de la spec tiene una instrucción

## 4. Skill 04-make-methodological-framework-update

- [x] 4.1 Crear `.claude/skills/04-make-methodological-framework-update/SKILL.md` y `references/dependencias.md` (términos, metodologías aplicadas y ampliación del glosario); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que contempla los tres modos

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-methodological-framework --strict`, las pruebas del kit y la comprobación de que las skills `04-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `04-make-methodological-framework` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-lean-plan`.
