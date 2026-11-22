# Tasks

Molde consultado en la etiqueta `pre-bi-pipeline`: `.claude/skills/03-make-company-chapter/SKILL.md`, `common/company/guia.md` y `models/emp-2-diagnostico.md`, `.claude/skills/_shared/visuales.py` (`ex_foda`, `_x_foda`, `PROPOSITOS`).

## 1. Kit común del capítulo 1

- [x] 1.1 Crear `_shared/diagnostico.py` (títulos del índice, encabezado esperado, lectura de las secciones de `03`, `04` y `05`, comprobaciones comunes de encabezado, figuras, marcador y citas, CLI `leer`) y verificar con `tests/test_diagnostico.py`.
- [x] 1.2 Hacer que los extractores de `visuales.py` acepten `--run` y verificar con una prueba que `extraer` usa la corrida indicada.

## 2. Skill 03-make-business-diagnosis

- [x] 2.1 Escribir `common/03-business-diagnosis/guia.md` y `models/` (README y plantillas 1.1 a 1.4 con ejemplo Pollería Don Tito) y verificar que las rutas citadas existen.
- [x] 2.2 Crear `rules/business_diagnosis.py` y el fixture del capítulo 1 (`tests/diagnostico_fixtures.py`); verificar con `tests/test_business_diagnosis.py` que el ejemplo valida y que cada regla detecta su error.
- [x] 2.3 Crear `.claude/skills/03-make-business-diagnosis/SKILL.md` y `03-make-business-diagnosis-update/` con `references/dependencias.md`; verificar con `tests/test_pipeline.py`.

## 3. Skill 04-make-strategic-analysis

- [x] 3.1 Escribir `common/04-strategic-analysis/guia.md` y `models/` (README y plantillas 1.5, 1.6 y 1.7) y verificar que las rutas citadas existen.
- [x] 3.2 Crear `rules/strategic_analysis.py`; verificar con `tests/test_strategic_analysis.py` (ejemplo válido, factor faltante, estrategia mal combinada, efecto distinto del brief, categoría desconocida, código sin definir).
- [x] 3.3 Crear `04-make-strategic-analysis/SKILL.md` y su `-update` con `references/dependencias.md`; verificar con `tests/test_pipeline.py`.

## 4. Skill 05-make-problem-objectives

- [x] 4.1 Escribir `common/05-problem-objectives/guia.md` y `models/` (README y plantillas 1.8, 1.9 y 1.10 con la matriz de articulación) y verificar que las rutas citadas existen.
- [x] 4.2 Crear `rules/problem_objectives.py`; verificar con `tests/test_problem_objectives.py` (ejemplo válido, causa inexistente, objetivo distinto del brief, causa principal sin objetivo, indicador distinto, sin corrida de `04`).
- [x] 4.3 Crear `05-make-problem-objectives/SKILL.md` y su `-update` con `references/dependencias.md`; verificar con `tests/test_pipeline.py`.

## 5. Visuales HTML

- [x] 5.1 Registrar `bmc`, `pestel`, `foda` e `ishikawa` en `visuales.py` (VISUALES, EXTRACTORES, EXPLICACION, PROPOSITOS, TITULOS, ORIGEN) y verificar con `tests/test_visuales.py` (extracción, origen, explicación válida, construcción en la corrida).
- [x] 5.2 Crear las fuentes React en `common/html/_build/src/visuales/{bmc,pestel,ishikawa}/` y ampliar `foda` con estrategias cruzadas; crear `common/html/<visual>/mock.json` y `README.md` (foda con datos de BI) y verificar que `npm run build` compila.
- [x] 5.3 Cambiar los textos de sprints de `vista-previa/Vista.jsx` por ejemplos de BI, recompilar y verificar con `html_tpl.py comprobar` y `tests/test_html_tpl.py` (con `PLANTILLAS` ampliado) y montando cada plantilla con `_build/test/montar.mjs`.
- [x] 5.4 Actualizar `common/html/README.md` (tabla de plantillas) y verificar que menciona los cuatro visuales.

## 6. Integración

- [x] 6.1 Ejecutar `python3 -m unittest discover -s .claude/skills/_shared/tests`, `npm run check:pipeline` y `python3 .claude/skills/_shared/html_tpl.py comprobar` y verificar que pasan.
- [x] 6.2 Recorrer el flujo de las tres skills sobre un proyecto temporal (`runs.py new`, escribir, `visuales.py construir --run`, `validate_run.py`, `projectcfg.py register`, `projectcfg.py secciones`) y verificar que 1.1 a 1.10 quedan disponibles.
- [x] 6.3 `openspec validate bi-chapter1-diagnosis --strict` sin errores.

## Workflow follow-up

- Sincronizar los deltas a `openspec/specs/`, validar con `openspec validate --specs --strict` y archivar en `openspec/changes/archive/2026-11-21-bi-chapter1-diagnosis/`.
- Commit en la rama del worktree.
