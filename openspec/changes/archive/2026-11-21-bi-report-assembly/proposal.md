# Proposal

## Why

El change `bi-base-pipeline` retiró el ensamblado del informe por avances (`19-make-report`, `report.py` y su validador) y dejó listo el registro de secciones (`informe.secciones`) para que un ensamblado nuevo arme el informe de Inteligencia de Negocios, de una sola entrega, solo con lo que ya se ejecutó. Mientras no exista, el equipo no puede ver el documento armado ni saber qué falta, y la spec `report-index-structure` exige un `report.py` que hoy no existe.

## What Changes

- **Skill `12-make-report`** (sin `-update`): arma `project/12-report/<corrida>/informe.md` con las secciones `disponible` del config, en el orden del índice, con portada y control del documento (config y brief), una introducción breve por capítulo con secciones, referencias combinadas y deduplicadas, anexos A a D solo si su sección de origen está disponible, `faltantes.md` con lo pendiente y la skill que lo produce, `README.md` de procedencia, copia de los HTML de figuras a `imagenes/` con `imagenes/INDICE.md` y HTML opcional con el sistema de diseño.
- **Contrato con las skills de contenido**: cada corrida aporta `secciones/<punto>.md`, marcas de figura `<!-- figura: <visual> -->` con `visuales/<visual>.html` y `leer-imagen/<visual>.md`, `referencias.md` opcional y, a futuro, `anexos/<letra>.md`. El informe reemplaza cada marca por el marcador de imagen, la línea «Cómo copiarla» y el párrafo «Cómo leer la figura», con numeración consecutiva de figuras y tablas.
- **Skill `13-make-annex-html`**: convierte a HTML autónomo los anexos de la corrida vigente de `12-make-report`, sin corrida propia.
- **Kit compartido**: `_shared/report.py` (CLI `plan`, `construir`, `render` y `anexos`, y `cargar_indice` con la marca de imagen por punto), `_shared/rules/report.py` (validador de la carpeta `12-report`), pruebas con corridas propias de 03, 04 y 05; `doc_html.py` toma la hoja de estilos del estándar visual de una plantilla que sí existe y reubica los enlaces relativos que no van a un `.md`.
- **Playbook** `common/12-report/guia.md` y `common/12-report/models/` (control del documento, introducciones por capítulo, referencias).

## Capabilities

### New Capabilities

- `report-assembly`: armado del informe de una sola entrega a partir de las secciones disponibles (orden, portada, introducciones, figuras, tablas, referencias, anexos, faltantes, procedencia, HTML opcional) y su validación.
- `annex-html`: conversión de los anexos del informe vigente a documentos HTML autónomos con el sistema de diseño, sin corrida propia.

### Modified Capabilities

(ninguna: `report-index-structure` ya exige la marca de imagen expuesta por `report.py` y la omisión de anexos sin origen; este change las cumple sin cambiar sus requisitos)

## Impact

- **Skills** (`.claude/skills/`): nuevas `12-make-report` y `13-make-annex-html`.
- **Kit** (`.claude/skills/_shared/`): nuevos `report.py`, `rules/report.py`, `tests/report_fixtures.py`, `tests/test_report.py`, `tests/test_report_rules.py` y `tests/test_doc_html.py`; ajuste de `doc_html.py` (origen de la hoja de estilos) y de la fila del informe en `README.md`.
- **Playbooks** (`common/`): nuevo `common/12-report/`; `common/document-html/README.md` cita la nueva fuente de estilos.
- **Skills de contenido 03 a 11**: deben escribir sus corridas según el contrato (lo cumplen las 03 a 05 que se construyen en paralelo).
- `pipeline.json` no cambia.
