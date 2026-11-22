# Tasks

## 1. Playbook y modelos

- [x] 1.1 Escribir `common/design-system/guia.md` (secciones 0 a 7 del diseño D7: reglas, principios, tokens, accesibilidad, componentes, HTML autónomo, consumo, errores y checklist); verificar que cubre cada requisito de la spec `design-system` y que ninguna regla contradice `project-config` ni `run-versioning`
- [x] 1.2 Crear en `common/design-system/models/` las plantillas `ds-0-brief.md`, `ds-1-tokens.md`, `ds-2-componentes.md`, `ds-3-design-md.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que cada plantilla tiene esas cinco partes y que el README las lista con enlaces que resuelven

## 2. Kit de validación

- [x] 2.1 Añadir a `.claude/skills/_shared/validate_run.py` el gancho opcional `validar(run)` y registrar la carpeta `design-system`; verificar con pruebas que los pasos sin gancho (Design Thinking) siguen pasando sin incidencias sobre la corrida existente
- [x] 2.2 Implementar `.claude/skills/_shared/rules/design_system.py` (claves claro y oscuro iguales, contraste WCAG de los pares, tokens citados existentes, recursos externos en `preview.html`, componentes con estados) con pruebas; verificar que pasa con unos tokens válidos y que informa archivo y causa en copias con un par de 3,2:1, un token inexistente, un recurso externo y un componente sin estados

## 3. Skill 01-design-system

- [x] 3.1 Crear `.claude/skills/01-design-system/references/tokens-base.json` (valores por defecto minimalistas, modernos y profesionales con pares AA verificados) y `scripts/render_preview.py` (genera `preview.html` autónomo desde `tokens.json`) con pruebas; verificar que el HTML generado pasa el validador, no tiene recursos externos y alterna claro y oscuro
- [x] 3.2 Crear `.claude/skills/01-design-system/SKILL.md` con el flujo (config, preguntas, propuesta, confirmación, escritura, validación, registro y `set-diseno`); verificar que la skill aparece en la lista con el nombre `01-design-system` y que cada requisito de la spec tiene una instrucción

## 4. Skill 01-design-system-update

- [x] 4.1 Crear `.claude/skills/01-design-system-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de qué tokens y componentes); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que contempla el caso de contraste insuficiente con `--no-mover`

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-design-system --strict`, las pruebas del kit y la verificación de que `01-design-system` y `01-design-system-update` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. Las skills `01-design-system` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-lean-canvas-initial`.
