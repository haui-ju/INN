# Proposal

## Why

El capítulo 3 del informe («Construcción y calidad del dashboard en Power BI») es, junto con el capítulo 2, el criterio de mayor peso de la rúbrica: pide el ETL con sus reglas de calidad y el dashboard con sus páginas, visualizaciones, filtros y KPI. Hoy `pipeline.json` declara las skills `08-make-etl` (3.1, anexos A y B) y `09-make-dashboard` (3.2, anexos C y D), pero ninguna existe, así que `12-make-report` los lista como pendientes. El diseño del capítulo 2 ya está cerrado (arquitectura, modelo en estrella y siete KPI), por lo que ahora se puede construir.

Dos condiciones del proyecto definen cómo se hace. Los datos son **generados** (`modo_datos: generado`), de modo que hay que producirlos con calidad y volumen, coherentes con las cifras que el informe ya afirma. Y el ETL y el dashboard los construye **el equipo a mano en Power BI**, no la skill. Por eso las skills de este capítulo no ejecutan nada en Power BI: preparan los datos, las guías y el código para pegar, y después redactan las secciones con la evidencia y los valores reales que el equipo trae. Nunca inventan un resultado del dashboard.

## What Changes

- **Generación de datos** (primer paso de `08-make-etl`): produce las seis fuentes del brief (FUE-01 a FUE-06) como archivos CSV en `data/` (carpeta raíz del repositorio, fuera de `project/`), con semilla fija, volumen suficiente (del orden de cien mil líneas de venta entre agosto de 2025 y octubre de 2026 (quince meses), un local) y calibrados con las cifras del informe: margen neto de 14 % a 8 %, merma de 7 %, aplicaciones de 15 % a 35 % de las ventas con comisión de 25 % a 30 %, precio del pollo vivo de S/ 6.10 a S/ 6.90 en julio y ventas que crecen 18 % frente al mismo periodo del año anterior. Incluye defectos a propósito, ligados al modelo (registros inválidos, días sin precio que se imputan, duplicados entre aplicaciones, nombres de producto distintos entre fuentes, fechas con formatos mezclados), y una **hoja de respuestas** con los totales esperados por mes y por canal para verificar el ETL del equipo.
- **Nueva skill `08-make-etl`** (y su `-update`): además de los datos, entrega el diccionario de datos y una guía paso a paso de Power Query. El equipo hace la limpieza y la carga en Power BI y trae la evidencia (filas antes y después de cada regla, sus scripts, capturas). La skill compara los totales del equipo con la hoja de respuestas, avisa de las diferencias y redacta 3.1 (extracción, transformación, reglas de calidad y carga), el anexo A (diccionario y calidad de datos) y el anexo B (scripts del ETL).
- **Nueva skill `09-make-dashboard`** (y su `-update`): a partir de `modelo.json` entrega la especificación de páginas, visualizaciones y filtros, y las medidas DAX de los siete KPI con sus metas. El equipo construye el dashboard y trae capturas por página y los valores reales de cada KPI. La skill redacta 3.2 (páginas, visualizaciones, filtros y KPI), el anexo C (medidas y cálculos) y el anexo D (especificación y capturas).
- **Marcador de captura en el informe:** `12-make-report` entiende `<!-- captura: <id> -->` (una imagen que el equipo guarda, no un visual generado) y la numera como figura con su marcador «(INCLUIR IMAGEN: …)». Así la sección 3.2, que lleva la marca «(incluye imagen)», no queda con aviso.
- **Guías a la medida del caso:** además de las plantillas, la primera mitad de cada skill entrega una guía escrita para los datos reales del proyecto. La de `08-make-etl` explica archivo por archivo qué limpiar y estandarizar, por qué, cómo y cuántas filas deben quedar después de cada paso (puntos de control tomados de la hoja de respuestas). La de `09-make-dashboard` explica, página por página, cada visual (tabla y campo de cada eje, medida y filtros), cada KPI con su cálculo y cada columna calculada con sus tablas de origen.
- **Dashboard de referencia en HTML:** `09-make-dashboard` genera un HTML autónomo con el sistema de diseño del proyecto que muestra cómo debería quedar cada página, con los valores esperados calculados desde los datos generados, para que el equipo compare su resultado con el de referencia.
- **Metas pendientes:** KPI-02 y KPI-06 tienen la meta «Pendiente» en 2.5 «hasta conocer los márgenes reales». Con los valores reales del dashboard, `09-make-dashboard` propone esas metas y las cierra con `07-make-data-model-kpi-update`.
- **Periodo de los datos alineado:** el brief y las secciones 2.3 y 2.4 dicen «de enero a octubre de 2026». Con datos de agosto de 2025 a octubre de 2026, la generación pide corregir esas frases con `01-make-project-brief-update`, `06-make-bi-solution-update` y `07-make-data-model-kpi-update` antes de generar, para que el informe no se contradiga.
- **`data/` no se versiona:** se agrega al `.gitignore` salvo `data/README.md` y `data/parametros.json`, porque los CSV se regeneran con la semilla.
- Ambas skills siguen el contrato de las corridas de contenido (`secciones/<punto>.md`, `anexos/<letra>.md`, `referencias.md`) y registran sus secciones con `register`, de modo que `12-make-report` las incluye en cuanto existen.
- Playbooks en `common/08-etl/` y `common/09-dashboard/`, validadores en `_shared/rules/`, el generador de datos en el kit compartido y pruebas.

## Capabilities

### New Capabilities

- `synthetic-data-generation`: generación reproducible de las fuentes en CSV bajo `data/`, calibrada con las cifras del informe, con defectos intencionales, parámetros visibles y hoja de respuestas.
- `etl-construction`: skill `08-make-etl` y su `-update`; diccionario y guía de Power Query, verificación de la evidencia del equipo contra la hoja de respuestas y redacción de 3.1 con los anexos A y B.
- `dashboard-construction`: skill `09-make-dashboard` y su `-update`; especificación de páginas, medidas DAX por KPI, evidencia del equipo y redacción de 3.2 con los anexos C y D.

### Modified Capabilities

- `report-assembly`: se agrega el marcador `<!-- captura: <id> -->` para imágenes que aporta el equipo (capturas del dashboard), con su numeración, su marcador de imagen y su aviso cuando falta el archivo.

## Impact

- **Skills:** `.claude/skills/08-make-etl`, `08-make-etl-update`, `09-make-dashboard`, `09-make-dashboard-update`.
- **Kit:** `_shared/datagen.py` (generador) y `_shared/dashboard_ref.py` (dashboard de referencia), `_shared/rules/etl.py` y `_shared/rules/dashboard.py`, soporte de capturas en `_shared/report.py` y pruebas en `_shared/tests/`.
- **Playbooks:** `common/08-etl/` y `common/09-dashboard/` con guía y plantillas.
- **Datos:** `data/` (CSV generados, `parametros.json`, `respuestas/` y un `README.md`), ignorada por git salvo el README y los parámetros. Se pueden regenerar con la semilla, por lo que no son fuente de verdad.
- **Capítulos ya cerrados:** una corrección de texto, vía `-update`, en el brief (alcance y FUE-01), 2.3 (HER-02) y 2.4 (lectura del modelo).
- **Dependencias:** requiere el capítulo 2 integrado (`modelo.json`, KPI y arquitectura). Desbloquea el capítulo 4 y 5 (`bi-chapter45-closing`), que necesita los valores reales del dashboard.
