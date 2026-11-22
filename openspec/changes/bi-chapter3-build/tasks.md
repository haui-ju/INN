# Tasks

## 1. Base y contrato con el capítulo 2

- [x] 1.1 Revisar lo archivado del capítulo 2 (`modelo.json`, códigos `FCT`, `DIM`, `REL` y `KPI`, componentes CAP-07 a CAP-09 y la sección 1.3 para las ventas anuales) y ajustar estas tareas si algo difiere; verificar que `projectcfg.py check --skill 08-make-etl` avisa por 07 cuando falta su corrida.
- [x] 1.2 Confirmar `pipeline.json` (08 requiere 07; 09 requiere 07 y 08; ambas con `update`) y la carpeta `data/` en la raíz; verificar con `projectcfg.py validate` y con la prueba del pipeline.

## 2. Generación de datos

- [x] 2.0 Alinear el periodo de los datos: ejecutar `01-make-project-brief-update` (alcance y FUE-01), `06-make-bi-solution-update` (HER-02 en 2.3) y `07-make-data-model-kpi-update` (lectura de 2.4) para cambiar «de enero a octubre de 2026» por «de agosto de 2025 a octubre de 2026», y agregar `data/` al `.gitignore` salvo `data/README.md` y `data/parametros.json`; verificar con `grep` que ninguna sección vigente conserva el periodo anterior y con `git check-ignore data/ventas.csv`.

- [x] 2.1 Crear `_shared/datagen.py` (solo biblioteca estándar) que lee `data/parametros.json`, genera las seis fuentes en CSV UTF-8 con semilla fija y escribe `data/README.md`; verificar con una prueba de reproducibilidad (dos ejecuciones idénticas byte a byte) y otra de que cambiar la semilla cambia los datos.
- [x] 2.2 Calibrar el generador con las cifras del informe (participación de aplicaciones, comisión por aplicación, margen neto mensual, merma, precio del pollo y crecimiento interanual de ventas) y declarar la tolerancia de cada una; verificar con pruebas de cada cifra y con la de «cifra fuera de tolerancia» (no entrega archivos).
- [x] 2.3 Agregar los defectos intencionales (registros inválidos, días sin precio, duplicados entre aplicaciones, nombres de producto y fechas mezclados, nulos) con su cantidad registrada en `data/respuestas/defectos.csv`; verificar con una prueba que cada tipo aparece y coincide con lo registrado.
- [x] 2.4 Escribir la hoja de respuestas en `data/respuestas/` (filas por fuente, ventas y comisión por mes y canal, producción por turno, precio medio por mes y días imputados); verificar que los totales coinciden con los de una limpieza de referencia hecha en la propia prueba.
- [x] 2.5 Verificar el volumen (del orden de cien mil líneas de venta y cobertura de todos los días del periodo) y que las ventas anualizadas son coherentes con las UIT de la sección 1.3; medir el tiempo de generación y dejar constancia de que son segundos.

## 3. Skill 08-make-etl

- [x] 3.1 Crear `common/08-etl/guia.md` y `models/` (README, plantillas de 3.1, anexo A, anexo B, la guía de Power Query y `evidencia.json`, cada una con ficha, instrucciones, formato, ejemplo y checklist); verificar que cada plantilla tiene las cinco partes.
- [x] 3.2 Crear `_shared/rules/etl.py` con `PREFIJOS` (`REG`, `PAS`) y las comprobaciones de la spec `etl-construction`: encabezado de `secciones/3.1.md`, campos del modelo con origen, reglas con evidencia, cada defecto de la hoja de respuestas con su regla, cifras de 3.1 presentes en la evidencia, declaración de datos generados, anexos A y B con sus títulos de tabla; verificar con pruebas de cada escenario.
- [x] 3.3 Implementar la comparación con la hoja de respuestas (desde `data/salida/` o desde totales tecleados) en `_shared/` y verificar con una prueba que un mes distinto informa tabla, mes, desvío y regla probable.
- [x] 3.4 Escribir `.claude/skills/08-make-etl/SKILL.md` (fuentes, parámetros con confirmación, generación, materiales para el equipo, pausa hasta tener evidencia, comparación, redacción de 3.1 y los anexos, revisión de redacción, validación y registro); verificar con una prueba de flujo que una corrida de ejemplo valida sin incidencias y deja 3.1 disponible.
- [x] 3.5 Escribir `08-make-etl-update/SKILL.md` y `references/dependencias.md`; verificar con pruebas que corregir una cifra cambia solo 3.1 y el anexo A, y que regenerar los datos marca la evidencia como desactualizada.

## 4. Skill 09-make-dashboard

- [x] 4.1 Crear `common/09-dashboard/guia.md` y `models/` (README, plantillas de especificación de páginas, 3.2, anexo C, anexo D y `valores.json`); verificar que cada plantilla tiene las cinco partes.
- [x] 4.2 Crear `_shared/rules/dashboard.py` con `PREFIJOS` (`PAG`, `MED`) y las comprobaciones de la spec `dashboard-construction`: cada KPI en una página, cada página con su usuario, medidas con tablas y campos del modelo, valores citados presentes en `valores.json`, capturas por página, anexos C y D; verificar con pruebas de cada escenario.
- [x] 4.3 Generar la medida DAX propuesta de cada KPI desde `modelo.json` y sus campos de origen; verificar con una prueba que todas las tablas y campos citados existen en el modelo.
- [x] 4.4 Implementar la propuesta de metas pendientes (KPI-02 y KPI-06) a partir de los valores reales y verificar que la skill no edita 2.5 y avisa qué `-update` la cierra.
- [x] 4.5 Escribir `.claude/skills/09-make-dashboard/SKILL.md` (fuentes, especificación con confirmación, medidas, pausa hasta tener valores y capturas, redacción de 3.2 y los anexos, revisión de redacción, validación y registro); verificar con una prueba de flujo que una corrida de ejemplo valida y deja 3.2 disponible.
- [x] 4.6 Escribir `09-make-dashboard-update/SKILL.md` y `references/dependencias.md`; verificar con una prueba que reemplazar una captura cambia solo esa captura y 3.2, y deja idéntico el anexo C.

## 5. Capturas en el informe

- [x] 5.1 Agregar a `_shared/report.py` el marcador `<!-- captura: <id> -->` (numeración junto con las figuras, marcador de imagen, enlace a la captura sin copiarla y entrada en `INDICE.md`) y el aviso cuando falta el archivo; verificar con las pruebas de los dos escenarios de la spec.
- [x] 5.2 Hacer que la marca «(incluye imagen)» se cumpla con una captura y avise solo cuando no hay ninguna imagen; verificar con una prueba de una sección que trae solo capturas.
- [x] 5.3 Actualizar `common/12-report/guia.md` y `12-make-report/SKILL.md` con el marcador de captura y el contrato de `capturas/`.

## 6. Integración

- [x] 6.1 Armar un informe de prueba con `report.py construir` sobre corridas de ejemplo de 03 a 09; verificar que 3.1 y 3.2 aparecen con sus capturas numeradas, que los anexos A a D entran y que `faltantes.md` solo lista los capítulos 4 y 5.
- [x] 6.2 Ejecutar `python3 -m unittest discover -s .claude/skills/_shared/tests`, `python3 .claude/skills/_shared/html_tpl.py comprobar` y `openspec validate bi-chapter3-build --strict`; verificar que todo pasa.
- [x] 6.3 Actualizar `openspec/ROADMAP.md` y la lista de skills de `common/` si los nombra; verificar que las referencias a 08 y 09 coinciden con `pipeline.json`.

## 7. Guías a la medida y dashboard de referencia

- [x] 7.1 Ampliar la hoja de respuestas con el margen de contribución por mes, canal y producto, la producción por día de la semana, el precio diario con marca de imputado y el pronóstico de referencia, y agregar KPI-05 a los KPI esperados; verificar con pruebas contra una limpieza de referencia.
- [x] 7.2 Generar los datos reales en `data/` con los parámetros confirmados por el usuario; verificar que las cifras calibradas pasan y que `git check-ignore` ignora los CSV y no el README ni los parámetros.
- [x] 7.3 Crear `_shared/dashboard_ref.py` y su esquema de `materiales/paginas.json` (visuales con tipo, eje X, eje Y, serie, tabla de origen, medida y filtros) y generar el HTML de referencia con el diseño del proyecto; verificar con pruebas que es autónomo, que trae cada página y que los valores coinciden con la hoja de respuestas.
- [x] 7.4 Escribir la guía de construcción del dashboard (por visual, KPI y columna calculada) para el proyecto; verificar que cada visual, KPI y columna del HTML aparece en la guía con sus tablas y campos.
- [x] 7.5 Escribir la guía de ETL a la medida del caso (por fuente: columnas, defectos con su cantidad, por qué, cómo y filas esperadas en cada paso) y verificar cada punto de control contra una limpieza de referencia hecha con la hoja de respuestas.
- [x] 7.6 Incorporar ambas guías y el HTML a las skills 08 y 09 (cómo se generan y qué se entrega al equipo) y ejecutar la suite completa; verificar que todo pasa y que `openspec validate bi-chapter3-build --strict` es válido.

## Workflow follow-up

- Sincronizar las specs y archivar el change con `/opsx:archive`.
