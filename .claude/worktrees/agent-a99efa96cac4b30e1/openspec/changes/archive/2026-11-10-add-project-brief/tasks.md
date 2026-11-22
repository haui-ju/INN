## 1. Config, pipeline y kit
- [x] 1.1 `projectcfg.py`: campo `avances[].inicio` (validación y comentario), subcomando `set-nucleo` (tema, resultado, enfoque, inicios y entregas, con validación y comentarios) y aviso de brief ausente para toda skill desde la 02 y de `domain.md` ausente
- [x] 1.2 `pipeline.json`: paso `00b-make-project-brief` (orden 1, carpeta `project-brief`, requiere `00-init`, update verdadero) y órdenes siguientes; ajustar `test_pipeline.py` y `test_flujo_skills.py` (22 pasos)
- [x] 1.3 `brief.py` (leer secciones, tablas y calendario del brief; `copiar al config`) y `rules/project_brief.py`, registrada en `validate_run.py`

## 2. Playbook y skills 00b
- [x] 2.1 Crear `common/project-brief/` (guía con las preguntas por sección y cómo pulir, `models/README.md` y `brief-1-nucleo.md`, con la plantilla de `domain.md`)
- [x] 2.2 Crear `00b-make-project-brief` (fuentes, preguntas y pulido, resumen y confirmación, escritura de `brief.md` y `domain.md`, `set-nucleo`, validación, registro)
- [x] 2.3 Crear `00b-make-project-brief-update` con `references/dependencias.md` (qué `-update` correr después)
- [x] 2.4 Pruebas del brief: secciones, objetivos, calendario, coherencia con el config, `domain.md`, flujo `00-init` → `00b` y que un cambio de una fila solo cambia lo afectado

## 3. Ajustar las demás skills
- [x] 3.1 `00-init` y `00-init-update`: solo datos técnicos, sin `domain.md`, y remisión a 00b
- [x] 3.2 `02` y `03` (y `rules/company.py`): leer el brief; `03` copia `OG-01`, `OE-nn`, justificación y alcance y la validación los compara con el brief
- [x] 3.3 `11` (y `rules/sprint_plan.py`): inicio y entrega desde el config
- [x] 3.4 Agregar el brief a las fuentes de `04`, `05`, `07`, `08`, `09`, `10`, `12`, `13`, `14`, `14b`, `15`, `16`, `17`, `18` y `19` según la tabla del diseño, y a las dependencias de sus `-update`
- [x] 3.5 Prueba de flujo: toda skill de `02` a `19` cita el brief; actualizar `common/*/guia.md` que mencionen preguntar tema o fechas

## 4. Cierre
- [x] 4.1 Ejecutar la suite completa, `openspec validate add-project-brief --strict` y `openspec validate --specs --strict`
