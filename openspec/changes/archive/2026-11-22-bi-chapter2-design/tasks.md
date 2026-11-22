# Tasks

## 1. Base y contrato con el capítulo 1

- [x] 1.1 Revisar lo integrado de `bi-chapter1-diagnosis` (archivos de `05-make-problem-objectives`, códigos de objetivos y causas, cómo se construyen los visuales) y ajustar estas tareas si algo difiere del contrato; verificar que `projectcfg.py check --skill 06-make-bi-solution` avisa por 05 cuando falta su corrida.

## 2. Skill 06-make-bi-solution

- [x] 2.1 Crear `common/06-bi-solution/guia.md` y `models/` (README, plantillas de 2.1, 2.2 y 2.3 con ficha, instrucciones, formato, ejemplo de BI y checklist); verificar que cada plantilla tiene las cinco partes.
- [x] 2.2 Crear `_shared/rules/bi_solution.py` con `PREFIJOS` (`CAP`, `HER`) y las comprobaciones: encabezados de `secciones/2.1.md` a `2.3.md`, cada `OE` del brief en la propuesta, las cuatro capas en orden, cada `FUE` del brief en la capa de fuentes, herramientas con justificación (o «Pendiente» en ETL y almacenamiento) y Power BI en visualización; verificar con pruebas de cada escenario de la spec `bi-solution-design`.
- [x] 2.3 Registrar el visual `arquitectura-bi` en `visuales.py` (extractor desde `secciones/2.2.md`, explicación y propósito) con su plantilla en `common/html/arquitectura-bi/`; verificar con `html_tpl.py comprobar`, `tests/test_html_tpl.py` y una prueba de extracción.
- [x] 2.4 Escribir `.claude/skills/06-make-bi-solution/SKILL.md` (fuentes, preguntas, propuesta con confirmación, escritura según el contrato, `visuales.py construir`, validación y registro); verificar con una prueba de flujo que una corrida de ejemplo valida sin incidencias y deja 2.1 a 2.3 disponibles.
- [x] 2.5 Escribir `06-make-bi-solution-update/SKILL.md` y `references/dependencias.md`; verificar con una prueba que completar la herramienta de ETL en un fork cambia solo 2.2, 2.3, la figura y el README.

## 3. Skill 07-make-data-model-kpi

- [x] 3.1 Crear `common/07-data-model-kpi/guia.md` y `models/` (README, plantillas de 2.4, 2.5 y `modelo.json`); verificar que cada plantilla tiene las cinco partes y que el ejemplo de `modelo.json` coincide con el ejemplo de las secciones.
- [x] 3.2 Crear `_shared/rules/data_model_kpi.py` con `PREFIJOS` (`FCT`, `DIM`, `REL`, `KPI`) y las comprobaciones de la spec `data-model-kpi` (granularidad, dimensión de tiempo, dimensiones relacionadas, relaciones a tablas existentes, cada `OE` con KPI, campos del KPI en el modelo, meta, `modelo.json` igual a las secciones); verificar con pruebas de cada escenario.
- [x] 3.3 Registrar el visual `modelo-datos` en `visuales.py` (desde `modelo.json`) con su plantilla en `common/html/modelo-datos/`; verificar con `html_tpl.py comprobar` y una prueba de extracción.
- [x] 3.4 Escribir `.claude/skills/07-make-data-model-kpi/SKILL.md`; verificar con una prueba de flujo que una corrida de ejemplo valida y deja 2.4 y 2.5 disponibles.
- [x] 3.5 Escribir `07-make-data-model-kpi-update/SKILL.md` y `references/dependencias.md`; verificar con una prueba que agregar un KPI en un fork cambia solo 2.5, `modelo.json` y el README.

## 4. Integración

- [x] 4.1 Armar un informe de prueba con `report.py construir` sobre corridas de ejemplo de 03 a 07; verificar que el capítulo 2 aparece completo con sus dos figuras numeradas y que `faltantes.md` ya no lista 2.1 a 2.5.
- [x] 4.2 Ejecutar `python3 -m unittest discover -s .claude/skills/_shared/tests`, `npm run check:pipeline`, `python3 .claude/skills/_shared/html_tpl.py comprobar` y `openspec validate bi-chapter2-design --strict`; verificar que todo pasa.

## Workflow follow-up

- Sincronizar las specs y archivar el change con `/opsx:archive`.
- Commit en `bi-pipeline`.
