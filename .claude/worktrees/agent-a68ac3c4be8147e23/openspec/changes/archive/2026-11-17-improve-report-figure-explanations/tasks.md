# Tasks

## 1. Catálogo de propósitos y reglas de resaltado

- [x] 1.1 Crear en `visuales.py` el catálogo de propósitos (una frase fija por visual y por tablero) y la declaración, por visual, de qué resalta y con qué regla de datos; verificar con una prueba que cada visual de `VISUALES` y cada tablero (`gantt`, `kanban`) tiene entrada.
- [x] 1.2 Reescribir las funciones de explicación de los diez visuales y de Gantt y Kanban para producir «Para qué sirve», «Qué dice» y, solo si hay resaltado, «Por qué se resalta», más el pie; verificar con pruebas en `_shared/tests/` que la matriz, el Kanban con columna sobre su límite, el journey map y el Gantt con atrasadas generan el texto esperado y que el FODA no incluye «por qué se resalta».
- [x] 1.3 Reescribir `mockups.py` (`leer_pantalla`, `leer_galeria`) con el mismo formato; verificar con la prueba de mockups con una pantalla modificada y una galería de proporción 2 conservadas y 1 nueva.
- [x] 1.4 Actualizar `rules/html_boards.py::check_leer_imagen` y `rules/ui_mockups.py` para exigir las funciones, el resaltado condicional y los topes (3 frases, 70 palabras); verificar con pruebas de explicación solo descriptiva, resaltado sin motivo y texto demasiado largo.

## 2. Propósito de tablas en el informe

- [x] 2.1 Inventariar las tablas del cuerpo del informe del avance 3 contra `common/structure/model1.md` y añadir la clave `propositos` a `report_map.json` con una frase por tabla (punto y orden); verificar con un script de prueba que ninguna tabla del informe de ejemplo queda sin entrada.
- [x] 2.2 Hacer que `report.py` y `report_prosa.py` antepongan el propósito a cada tabla, conserven la frase propia de la fuente si existe y copien la explicación de figura como un párrafo en el orden nuevo; verificar con pruebas de las tres situaciones (catálogo, frase propia, sin ninguna) y con el aviso de «tabla sin propósito».
- [x] 2.3 Añadir en `rules/report.py` las comprobaciones de propósito por tabla y de las funciones «para qué sirve» y «qué dice» en cada figura, e informar punto y causa; verificar con pruebas que fallan en una tabla sin propósito y en una figura solo descriptiva.

## 3. Documentación y regeneración

- [x] 3.1 Actualizar `common/report/guia.md`, `common/report/models/`, `common/html/DESIGN.md` y las skills `13-design-html-boards`, `14b-make-ui-mockups` y `19-make-report` con el nuevo formato y el catálogo; verificar leyendo que no queda ninguna mención a «Qué muestra / Cómo leerla / Qué transmite».
- [x] 3.2 Ejecutar la suite completa de `_shared/tests/` y corregir lo que falle; verificar que termina sin fallos.
- [x] 3.3 Regenerar `leer-imagen/` de la corrida vigente de 13 y 14b con sus `-update`, armar un informe de prueba con `19-make-report`, y verificar con `validate_run.py` que no hay incidencias y que la explicación de la matriz, el Kanban y el Gantt se lee como se pidió.

## Workflow follow-up

- Revisar a mano las explicaciones de las 12 figuras principales y el propósito de las tablas con el usuario antes de archivar.
- Este change no incluye la reducción del volumen ni los anexos opcionales (`compact-report-readability`) ni la corrección de datos fuente.
