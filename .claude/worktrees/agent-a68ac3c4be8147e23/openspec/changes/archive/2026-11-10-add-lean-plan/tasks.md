# Tasks

## 1. Playbook, modelos e índice

- [x] 1.1 Ampliar `common/lean/guia.md`: reemplazar la sección 4 reservada por las secciones de Lean Startup, Lean Change Management, Canvas validado v1 y errores y checklist del plan; ampliar 0.3 (códigos) y 0.4 (cantidades) y las Referencias con Ries (2011) y Little (2014); verificar que las secciones 1 a 3 no cambian, que cubre cada requisito de la spec `lean-plan` y que las referencias coinciden con las ya verificadas en `common/methodological-framework/guia.md`
- [x] 1.2 Crear `common/lean/models/lean-2-hipotesis-supuestos.md`, `lean-3-mvp.md`, `lean-4-ciclo-medir-aprender.md`, `lean-5-gestion-cambio.md` y `lean-6-canvas-validado.md` y actualizar `models/README.md`; verificar que cada plantilla tiene ficha, instrucciones, formato, ejemplo y checklist, que el ejemplo de cada una es coherente con el de `lean-1-canvas` (mismos `SUP`, `PRB` y bloques) y que los enlaces del README resuelven
- [x] 1.3 Corregir en `common/structure/model1.md` las marcas de 3.2.3, 3.2.4, 3.3 y 3.4 a `[A1+]`; verificar con `grep` que solo cambian esas cuatro líneas y que `openspec validate --specs --strict` sigue pasando

## 2. Validación

- [x] 2.1 Registrar la carpeta `lean-plan` en `RULES` de `validate_run.py`; verificar que las pruebas de los demás pasos siguen pasando
- [x] 2.2 Implementar `.claude/skills/_shared/rules/lean_plan.py` (`PREFIJOS`, estructura de los tres archivos, trazabilidad `SUP`→`HIP`→`MET`/`EXP`, MVP y `REQ`, criterios, cadena de cambio, canvas v1 contra el v0, códigos del Design Thinking contra su corrida vigente) con pruebas que usen como fixture los ejemplos de las plantillas, un canvas v0 y una corrida de Design Thinking generada con `build.py`; verificar que pasa con un plan completo y que informa archivo y causa en copias con una `HIP` sin métrica, un `SUP` alto sin hipótesis, un `REQ` inexistente, una opción sin insight, un cambio de bloque sin registrar y un código del Design Thinking inexistente

## 3. Skill 07-make-lean-plan

- [x] 3.1 Crear `.claude/skills/07-make-lean-plan/SKILL.md` (corridas base, preguntas, plan con confirmación, escritura, validación y registro); verificar que aparece en la lista con el nombre `07-make-lean-plan` y que cada requisito de la spec tiene una instrucción

## 4. Skill 07-make-lean-plan-update

- [x] 4.1 Crear `.claude/skills/07-make-lean-plan-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de cada código y qué corridas posteriores los citan); verificar que aparece en la lista, que sigue el patrón de `run-versioning` y que cubre los modos de hipótesis, experimentos, cambio y canvas v1

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-lean-plan --strict`, las pruebas del kit y la comprobación de que las skills `07-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `07-make-lean-plan` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-scrum-team-requirements`.
