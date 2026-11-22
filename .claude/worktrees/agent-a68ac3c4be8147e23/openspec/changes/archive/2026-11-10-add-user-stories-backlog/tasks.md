# Tasks

## 1. Playbook y modelos

- [x] 1.1 Verificar por búsqueda las fuentes (Cohn 2004, Wake 2003, North 2006; Cohn 2005 solo si se confirma; Schwaber y Sutherland 2020 ya verificada) y escribir `common/user-stories/guia.md` (formato de la historia, INVEST, criterios Dado/Cuando/Entonces, Definition of Done, escalas de estimación, orden del backlog, errores, checklist, referencias); verificar que cubre cada requisito de la spec `user-stories` y que solo cita fuentes confirmadas
- [x] 1.2 Crear `common/user-stories/models/hu-1-historia.md`, `hu-2-criterios-aceptacion.md`, `hu-3-definition-of-done.md`, `hu-4-product-backlog.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que los ejemplos son coherentes entre sí y con los RF, RNF y `REQ` de los ejemplos de `common/requirements/models/`, y que los enlaces resuelven

## 2. Validación

- [x] 2.1 Registrar la carpeta `user-stories` en `RULES` de `validate_run.py`; verificar que las pruebas de los demás pasos siguen pasando
- [x] 2.2 Implementar `.claude/skills/_shared/rules/user_stories.py` (`PREFIJOS`, historias, criterios, cobertura de RF, backlog, resumen y Definition of Done, citas) con pruebas que usen como fixture los ejemplos de las plantillas, una corrida de requerimientos y un Design Thinking generado con `build.py`; verificar que pasa con un ejemplo completo y que informa archivo y causa con una historia sin RF, un REQ derivado incorrecto, una historia con un solo criterio, un `CA` repetido, un RF sin cubrir, un orden incorrecto, una estimación fuera de la escala y un resumen desalineado

## 3. Skill 10-make-user-stories

- [x] 3.1 Crear `.claude/skills/10-make-user-stories/SKILL.md` (corridas base, acuerdo de historias, criterios, confirmación final, escritura, validación y registro); verificar que aparece en la lista con el nombre `10-make-user-stories` y que cada requisito de la spec tiene una instrucción

## 4. Skill 10-make-user-stories-update

- [x] 4.1 Crear `.claude/skills/10-make-user-stories-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de cada `HU` y `CA` y qué corridas posteriores los citan); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que cubre los modos de historias, criterios, backlog y Definition of Done

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-user-stories-backlog --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `10-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `10-make-user-stories` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-sprint-plan-ceremonies`.
