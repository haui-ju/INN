# Tasks

## 1. Lean Canvas y Design Thinking

- [x] 1.1 En `rules/lean_canvas.py` exigir cinco niveles o `Cierre anticipado` con motivo y coherencia con el nombre del método; verificar con pruebas en `tests/test_lean_canvas.py` (cadena de tres niveles sin cierre falla; con cierre justificado pasa; título «cinco porqués» con cadena corta falla).
- [x] 1.2 Actualizar la plantilla y el playbook de `02-make-initial-lean-canvas` con el campo `Cierre anticipado`; verificar leyendo el modelo y con la prueba de fixtures de `lean_canvas`.
- [x] 1.3 En `rules/design_thinking.py` comprobar que cada idea incluida alimenta un `REQ`, que las cifras de ideas y `REQ` expliquen su relación y que los `HAL-T` sean consecutivos; verificar con pruebas de 7 ideas y 6 `REQ` sin explicación, idea sin `REQ` y hueco `HAL-T-01/03`.

## 2. Lean plan y resultados

- [x] 2.1 En `rules/lean_plan.py` y el modelo de `07` agregar el umbral «Iterar si» y comprobar que los tres umbrales no dejen huecos ni se solapen; verificar con pruebas del caso 90 %/60 % sin zona y de solapes.
- [x] 2.2 En `rules/lean_results.py` hacer que «Iterar» cite el texto de «Iterar si» y que el estado de los supuestos del canvas v1 coincida con las decisiones; verificar con pruebas de decisión Iterar sin zona y de supuesto pendiente con decisión Perseverar.

## 3. Calendario, estado real y pruebas

- [x] 3.1 En `rules/ceremonies_kanban.py` detectar solapes de horario (incluida la Daily) y fechas en fin de semana; verificar con pruebas de Planning 19:00–21:00 con Daily 19:30 y de una Planning en domingo.
- [x] 3.2 En `rules/html_boards.py` exigir predecesoras terminadas para toda tarea con avance 100; verificar con una prueba de `TAR-37` terminada con `TAR-42` en 0.
- [x] 3.3 En `rules/system_design.py` exigir `CP` consecutivos y rechazar casos duplicados (mismo tipo, verificación y datos); verificar con pruebas del hueco `CP-23/24` y de `CP-22` y `CP-34`.
- [x] 3.4 En `rules/implementation_log.py` exigir resultado para los casos de historias terminadas y observación en «No ejecutado»; verificar con pruebas de caso sin resultado y de «No ejecutado» sin motivo.

## 4. Objetivos y análisis final

- [x] 4.1 En `rules/project_brief.py` y el modelo de `00b` agregar la base de medición por objetivo y comprobar que el plazo caiga donde existe esa base; verificar con pruebas de objetivo sin base y de plazo anterior al sistema.
- [x] 4.2 En `rules/final_analysis.py` comparar la métrica medida con el indicador (Parcial con la diferencia si no coinciden) y exigir conclusión y trabajo futuro para toda historia sin avance; verificar con pruebas de `OG-01` y de `HU-14`.

## 5. Documentación y cierre

- [x] 5.1 Actualizar los playbooks de `common/` y los `SKILL.md` de las skills afectadas con las reglas nuevas y el `-update` que corrige cada una; verificar leyendo cada archivo.
- [x] 5.2 Ejecutar la suite completa de `_shared/tests/`, validar las corridas vigentes y escribir la lista de `-update` que hay que ejecutar para corregir los datos; verificar que la suite pasa y que la lista cubre cada inconsistencia del informe.

## Workflow follow-up

- Ejecutar los `-update` de la lista (02, 05, 07, 12, 13, 14, 15, 17, 18) y volver a armar el informe con `19-make-report`; no forma parte de este change.
