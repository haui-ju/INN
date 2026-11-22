# Tasks

## 1. Anexo G en el índice y en el mapa

- [x] 1.1 Añadir a `common/structure/model1.md` el anexo G (G.1 a G.4) y la marca de punto trasladable en 2.4, 4.4.1, 4.5, 4.6.2 y 5.5.1; verificar con la prueba de `cargar_indice` que G.1 a G.4 y las marcas se leen, que B, D, E, F y 3.1.1 a 3.1.8 no cambian y que no hay saltos de numeración.
- [x] 1.2 Añadir a `report_map.json` la clave `trasladables` con punto, colocación por omisión, destino y fuente del resumen de cada bloque; verificar con una prueba que cada punto trasladable existe en el índice y tiene destino.

## 2. Colocación por bloque

- [x] 2.1 Implementar en `report.py` y `report_prosa.py` la colocación cuerpo/anexo con el resumen de una a tres frases y el enlace, escribiendo el anexo G solo con los bloques elegidos; verificar con pruebas de casos de prueba al anexo, glosario en el cuerpo y valores por omisión.
- [x] 2.2 Añadir el parámetro de colocación al comando `construir` y la pregunta por bloque a `.claude/skills/19-make-report/SKILL.md` y a `common/report/guia.md`, guardando la elección en el `README.md` de la corrida; verificar armando una corrida con un bloque trasladado y comprobando el README.

## 3. Menos repetición

- [x] 3.1 Hacer que 4.6.1 muestre solo la asignación por sprint y cite 4.4.2, que 4.5 se reduzca a una línea por historia y que 4.7 liste los participantes una sola vez; verificar con pruebas sobre la fixture de informe y comparando el conteo de líneas del avance 3 antes y después.

## 4. Densidad de códigos

- [x] 4.1 Implementar en `report_prosa.py` el colapso de series a rangos y la regla de nombre primero con un código entre paréntesis en la prosa que escribe el ensamblado; verificar con pruebas de la frase «REQ-01 … REQ-06», de series con huecos y de que las tablas no se modifican.
- [x] 4.2 Añadir `check_densidad` en `rules/report.py` (máximo por frase, series sin colapsar, solo fuera de tablas) con advertencia para párrafos de origen fuente que indique el `-update` responsable; verificar con pruebas de frase con cinco códigos y de tabla con muchos códigos que no falla.

## 5. Validación de colocación y cierre

- [x] 5.1 Añadir `check_colocacion` en `rules/report.py` (bloque duplicado, resumen o enlace ausente, enlace a G que no resuelve, G sin bloques); verificar con las tres pruebas de los escenarios de la spec.
- [x] 5.2 Ejecutar la suite de `_shared/tests/`, armar con `19-make-report` un informe del avance 3 en valores por omisión y otro con los cinco bloques en anexo, y validarlos con `validate_run.py`; verificar que ambos pasan y que el segundo reduce el cuerpo de forma medible respecto del avance 3 actual.

## Workflow follow-up

- Revisar con el usuario cuántos códigos por frase le resultan cómodos y qué bloques prefiere en el cuerpo antes de archivar.
- Se aplica después de `improve-report-figure-explanations`; comparte `report.py` y `rules/report.py`.
