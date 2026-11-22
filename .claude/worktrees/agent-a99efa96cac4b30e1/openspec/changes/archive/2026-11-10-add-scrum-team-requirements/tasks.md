# Tasks

## 1. Playbooks y modelos

- [x] 1.1 Verificar por búsqueda las fuentes (Schwaber y Sutherland 2020 ya verificada; confirmar edición y título de ISO/IEC 25010 e ISO/IEC/IEEE 29148) y escribir `common/scrum/guia.md` (roles, artefactos y compromisos, cadencia, reparto para cuatro personas, errores, checklist, referencias); verificar que cubre cada requisito de la spec `scrum-setup` y que solo cita fuentes confirmadas
- [x] 1.2 Crear `common/scrum/models/scr-1-equipo-roles.md`, `scr-2-artefactos.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que cada plantilla tiene esas partes, que el ejemplo es coherente con el config de ejemplo (cuatro integrantes, tres avances) y que los enlaces resuelven
- [x] 1.3 Escribir `common/requirements/guia.md` (derivación desde los REQ, RF, RNF con las categorías confirmadas, matriz, errores, checklist y referencias verificadas); verificar que cubre cada requisito de la spec `requirements`
- [x] 1.4 Crear `common/requirements/models/req-1-rf.md`, `req-2-rnf.md`, `req-3-matriz-trazabilidad.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que los ejemplos citan `REQ` del paquete de referencia de Design Thinking y que los enlaces resuelven

## 2. Config

- [x] 2.1 En `projectcfg.py` validar el valor de `rol`, añadir `set_roles` y el comando `set-roles` y actualizar `COMENTARIOS` de `equipo[].rol`; con pruebas que cubran: reparto válido, dos Product Owner, sin Scrum Master, rol inexistente, integrante fuera del equipo y config intacto tras un rechazo; verificar que las pruebas del kit siguen pasando
- [x] 2.2 Actualizar el texto de `00-init-update` y de `00-init` sobre los roles (valores permitidos y uso de `set-roles`); verificar con `grep` que ambas skills remiten a `08-make-scrum-setup` y a los tres valores

## 3. Validación

- [x] 3.1 Registrar las carpetas `scrum-setup` y `requirements` en `RULES` e implementar `rules/scrum_setup.py` (estructura, coherencia con el config, cadencia, artefactos, puntos del índice) con pruebas con fixtures de las plantillas; verificar que pasa con un ejemplo completo y que informa archivo y causa con un segundo Scrum Master, un integrante ausente, una fecha distinta, un compromiso incorrecto y un punto inexistente
- [x] 3.2 Implementar `rules/requirements.py` (`PREFIJOS`, RF y RNF, cobertura de los `REQ`, categorías, metas con cifra, matriz alineada con `rf.md`, códigos del Design Thinking) con pruebas con fixtures de las plantillas y un Design Thinking generado con `build.py`; verificar que pasa con un ejemplo completo y que informa archivo y causa con un RF sin origen, un `REQ` inexistente, un `REQ` sin cubrir, un RNF sin cifra, una categoría inválida y una matriz desalineada

## 4. Skills 08 y 09

- [x] 4.1 Crear `.claude/skills/08-make-scrum-setup/SKILL.md` (config, reparto propuesto, preguntas, confirmación, `set-roles`, escritura, validación y registro); verificar que aparece en la lista y que cada requisito de la spec `scrum-setup` tiene una instrucción
- [x] 4.2 Crear `.claude/skills/09-make-requirements/SKILL.md` (Design Thinking vigente, Scrum vigente y plan Lean opcional, propuesta de RF y RNF, confirmación, escritura, validación y registro); verificar que aparece en la lista y que cada requisito de la spec `requirements` tiene una instrucción

## 5. Skills update

- [x] 5.1 Crear `.claude/skills/08-make-scrum-setup-update/SKILL.md` y `references/dependencias.md`; verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que los cambios de rol usan `set-roles`
- [x] 5.2 Crear `.claude/skills/09-make-requirements-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de cada RF y RNF y qué corridas posteriores los citan); verificar que aparece en la lista y que avisa de las historias que citan un RF

## 6. Verificación final

- [x] 6.1 Ejecutar `openspec validate add-scrum-team-requirements --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `08-…` y `09-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. Las skills `08-make-scrum-setup` y `09-make-requirements` y sus `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-user-stories-backlog`.
