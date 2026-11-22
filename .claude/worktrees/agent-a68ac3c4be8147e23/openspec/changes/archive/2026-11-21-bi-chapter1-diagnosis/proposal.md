# Proposal

## Why

Tras `bi-base-pipeline`, el pipeline de BI tiene el índice, el config, el brief y el sistema de diseño, pero ninguna skill produce el capítulo 1 (diagnóstico estratégico), que es el primer criterio de la rúbrica: misión, visión, industria y tamaño, más FODA, PESTEL, Canvas e Ishikawa con la problemática bien definida y todos los elementos articulados a los objetivos. `pipeline.json` ya declara las tres skills (`03`, `04` y `05`) y sus secciones; falta construirlas para que el ensamblado (`12-make-report`, en un change paralelo) tenga qué armar.

## What Changes

- **`03-make-business-diagnosis`** y su `-update`: secciones 1.1 (nombre de la empresa), 1.2 (misión y visión), 1.3 (industria y tamaño, con la categoría según ventas anuales en UIT y la Ley 30056) y 1.4 (Business Model Canvas de nueve bloques con su visual `bmc`), a partir de `domain.md` y del brief.
- **`04-make-strategic-analysis`** y su `-update`: 1.5 PESTEL (seis factores con hallazgo, efecto, tipo y fuente), 1.6 FODA (ítems con código y evidencia más estrategias cruzadas FO, FA, DO y DA) y 1.7 Ishikawa (efecto igual al problema del brief y causas por categorías 6M), cada una con su visual (`pestel`, `foda`, `ishikawa`).
- **`05-make-problem-objectives`** y su `-update`: 1.8 problemática central (enunciado, causas principales tomadas del Ishikawa y evidencia), 1.9 y 1.10 con el OG y los OE copiados del brief, y una matriz de articulación que vincula cada OE con causas del Ishikawa, ítems FODA, factores PESTEL, bloques del Canvas y su indicador.
- **Contrato de sección por corrida**: cada skill escribe `secciones/<punto>.md` con el encabezado exacto del índice, marca las figuras con `<!-- figura: <visual> -->`, deja el HTML en `visuales/` y su explicación en `leer-imagen/`, y opcionalmente `referencias.md` en APA 7. Es lo que lee `12-make-report`.
- **Playbooks** `common/03-business-diagnosis/`, `common/04-strategic-analysis/` y `common/05-problem-objectives/` (guía y una plantilla por sección, con el caso Pollería Don Tito como ejemplo).
- **Validadores** `rules/business_diagnosis.py`, `rules/strategic_analysis.py` y `rules/problem_objectives.py`, con un módulo compartido de lectura del capítulo 1 y sus pruebas.
- **Visuales HTML** `bmc`, `pestel` e `ishikawa` nuevos y `foda` ampliado con las estrategias cruzadas, registrados en `visuales.py` (extractor, explicación, propósito, título y origen); la vista previa del sistema de diseño cambia sus textos de ejemplo de sprints por ejemplos de BI.

## Capabilities

### New Capabilities

- `business-diagnosis`: skill `03-make-business-diagnosis` y su `-update`; contenido, fuentes y validación de las secciones 1.1 a 1.4.
- `strategic-analysis`: skill `04-make-strategic-analysis` y su `-update`; PESTEL, FODA con estrategias cruzadas e Ishikawa (1.5 a 1.7) y su validación.
- `problem-objectives`: skill `05-make-problem-objectives` y su `-update`; problemática central, objetivos copiados del brief y matriz de articulación (1.8 a 1.10).
- `report-visuals`: visuales HTML del informe (plantillas en `common/html/`, registro en `visuales.py`, extracción desde las secciones, construcción en la corrida y texto «leer la imagen»).

### Modified Capabilities

(ninguna: el índice, el pipeline y el registro de secciones ya declaran lo que estas skills aportan)

## Impact

- **Skills** nuevas en `.claude/skills/`: `03-make-business-diagnosis`, `04-make-strategic-analysis`, `05-make-problem-objectives` y sus `-update` (con `references/dependencias.md`).
- **Kit compartido**: `visuales.py` (registros de cuatro visuales y extracción por corrida), un módulo nuevo de lectura del capítulo 1, tres módulos en `rules/` y sus pruebas en `tests/` (más fixtures del caso de ejemplo); `tests/test_html_tpl.py` amplía `PLANTILLAS`.
- **Plantillas HTML**: `common/html/bmc`, `pestel`, `ishikawa` y `foda` (mock con datos de BI y estrategias), fuentes en `common/html/_build/src/visuales/` y manifiesto recompilado.
- **Sin cambios** en `pipeline.json`, `common/structure/model1.md`, `_shared/README.md` ni en las skills de informe (`12` y `13`), que construye otro change con el mismo contrato de secciones.
