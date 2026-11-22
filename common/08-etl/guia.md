# Playbook del ETL (sección 3.1 y anexos A y B)

Guía para que un agente prepare el trabajo del equipo y redacte el ETL del capítulo 3 del informe de BI (`common/structure/model1.md`): extracción, transformación, reglas de calidad y carga. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `08-make-etl` (y lo ajusta `08-make-etl-update`). Escribe en `project/08-etl/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide un ETL con reglas de calidad y resultados medibles, y el diccionario y los scripts como anexos A y B.

**Quién hace qué.** La skill no ejecuta Power Query ni Power BI. Prepara los materiales (datos, diccionario, guía paso a paso y código para pegar), se detiene, y redacta solo cuando el equipo trae la evidencia de lo que hizo. Nunca escribe una cifra que no esté en `evidencia.json`.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): fuentes `FUE-nn` con su tipo, sus datos y el modo de acceso, y los objetivos.
2. La corrida vigente de `06-make-bi-solution` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution`): componentes de ETL y de almacenamiento y herramientas.
3. `modelo.json` de la corrida vigente de `07-make-data-model-kpi`: tablas, campos y claves del destino. Sin él, la skill se detiene.
4. `data/` (parámetros, archivos y hoja de respuestas) y el config (`modo_datos`).

### 0.2 Dos mitades con una pausa entre ellas
1. **Materiales.** Datos (ver 1), diccionario de datos y guía de Power Query (ver 2). La guía de Power Query de este caso la genera `_shared/etl_guia.py` con las cifras de la limpieza de referencia (`_shared/etl_referencia.py`), de modo que cada paso cierra con el número de filas que debe quedar. Se entregan y la skill se detiene.
2. **Redacción.** Cuando el equipo entrega la evidencia, la skill la guarda en la corrida, compara los totales con la hoja de respuestas (ver 4) y redacta 3.1 y los anexos. Sin evidencia, 3.1 y los anexos no se escriben.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/3.1.md`: la primera línea es el encabezado exacto `## 3.1. Construcción de la solución ETL`; después, solo texto final del informe, sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- `anexos/A.md` (`# Anexo A: Diccionario de datos y calidad de datos`) y `anexos/B.md` (`# Anexo B: Scripts del ETL`): se agregan al final del informe.
- `evidencia.json` (entrada del equipo, ver 3), `capturas/` (opcional) y `README.md` con la procedencia.
- `referencias.md` si se cita (por ejemplo, Kimball y Ross, 2013).
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada archivo).

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `REG-nn` | Regla de calidad | Primera celda de la tabla de reglas de 3.1 |
| `PAS-nn` | Paso de Power Query | Primera celda de la tabla de pasos de 3.1 y rótulo del script en el anexo B |
| `FUE-nn` | Fuente del brief | Brief (se cita, no se vuelve a definir) |
| `FCT-nn`, `DIM-nn` | Tablas del modelo | Sección 2.4 (se citan) |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un ítem.

### 0.5 Texto limpio
Ningún archivo, salvo `README.md`, califica los datos como falsos, inventados, de prueba o simulados. Los datos del proyecto se declaran **generados** para el proyecto: así se dice en 3.1.

---

## 1. Datos generados (primer paso)

Con `modo_datos: generado`, la skill genera las fuentes con `python3 .claude/skills/_shared/datagen.py`: primero `parametros` (deriva y muestra `data/parametros.json`), y solo después de que el usuario lo confirme, `generar --confirmar`. Deja un CSV por fuente en `data/` (`fue-01-caja.csv` …), la hoja de respuestas en `data/respuestas/` y un `data/README.md`. Con `modo_datos: real`, no genera: pide al equipo los archivos autorizados.

Además de las fuentes, `data/` trae dos **archivos de apoyo**: `apoyo-catalogo-productos.csv` (`producto, categoria, precio_lista, pollos_equivalentes, kg_pollo_vivo, costo_otros, alias`; los nombres alternativos van en `alias` separados por `|`) y `apoyo-costos-operativos.csv` (`mes, planilla, alquiler, servicios, otros, total`). Con ellos el ETL calcula `costo_estimado` = cantidad × (`kg_pollo_vivo` × precio por kilogramo del día + `costo_otros`) y `costo_operativo` = el total del mes repartido en proporción a la venta del mes.

Las fechas con barras son día/mes/año. Un precio faltante es un día sin fila en la fuente de precios: se imputa el último precio publicado y `respuestas/precio-mes.csv` cuenta los días imputados. La comisión llega como monto en unas aplicaciones y como porcentaje (`comision_pct`) en otras: el ETL la homologa a monto.

Los defectos intencionales (registros inválidos, duplicados entre aplicaciones, nombres de producto distintos, fechas con formatos mezclados, nulos y días sin precio) están contados en `data/respuestas/defectos.csv`, con la regla que debería tratarlos. **Cada tipo de defecto necesita una regla `REG-nn`** en 3.1.

## 2. Materiales para el equipo

### 2.1 Diccionario de datos (base del anexo A)
Una tabla con los campos de cada fuente (y de cada archivo de apoyo, que se nombra «Apoyo: …»), el tipo, la regla de calidad que lo trata y el campo del modelo al que llega, y una tabla de **origen de cada campo del modelo** (un `FUE-nn.campo`, un `apoyo-<archivo>.campo` o un cálculo). Todo campo de `modelo.json` tiene un origen o un cálculo; los costos del modelo se explican con los archivos de apoyo.

### 2.2 Guía paso a paso de Power Query
Pasos `PAS-nn` ordenados: **importar** cada CSV (UTF-8), **tipar**, **depurar** (nulos y registros inválidos), **homologar** (nombres de producto, formatos de fecha, nombres de columna entre aplicaciones), **anexar** las fuentes de pedidos en una sola tabla, **calcular** claves y medidas del modelo y **cargar**. Cada paso indica la tabla, el resultado esperado y el código M propuesto para pegar. Se dice de forma explícita que lo ejecuta el equipo y que el código se prueba y se ajusta en Power BI.

La guía se escribe para Power BI Desktop. Si parte del equipo trabaja en el navegador, el mismo paso se anota en la columna «Resultado»; lo que cuenta es el resultado (filas y totales), no la herramienta.

## 3. Evidencia que trae el equipo (`evidencia.json`)

```json
{
  "schema": 1,
  "reglas": [{"codigo": "REG-01", "filas_antes": 1600, "filas_despues": 1600}],
  "tablas": [{"nombre": "FUE-01", "filas": 1200}, {"nombre": "fPedidos", "filas": 1550}],
  "totales": {"ventas_total": 79200.0, "comision_total": 9450.0, "lineas_total": 1550},
  "verificacion": {"estado": "coincide", "diferencias": []}
}
```
- `reglas`: las filas de la tabla de trabajo antes y después de aplicar cada regla (en Power Query, las filas que muestra el editor en el paso anterior y en el paso de la regla).
- `tablas`: en `nombre` va un código de fuente (`FUE-nn`, filas leídas) o una tabla del modelo (`fPedidos`, `dCalendario`, filas cargadas).
- `totales`: lo que suma el modelo cargado (ventas brutas, comisión y líneas válidas), para comparar con la hoja de respuestas.
- `verificacion`: la deja `python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia <ruta> --actualizar`. Cada diferencia trae tabla, mes, medida, esperado, obtenido, desvío y la regla probable.

La skill pide estos valores al equipo con preguntas concretas (una por regla y una por tabla) y los guarda tal cual. Las capturas de Power Query son opcionales y van en `capturas/`.

## 4. Verificación contra la hoja de respuestas

`python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia <ruta>` compara los totales del equipo con `data/respuestas/`. Si el equipo exportó sus tablas cargadas a `data/salida/<tabla>.csv` (`fPedidos`, `fProduccion`, `fPrecioInsumo`, `dCalendario`, `dCanal` y `dTurno`, con los nombres de columna del modelo), la comparación es por mes y canal o turno; si no, usa `totales` de la evidencia.

- **Coincide:** 3.1 lo dice.
- **Hay diferencias:** son un error del ETL del equipo, no algo que ocultar. La skill informa tabla, mes, desvío y la regla probable, **pide corregir el ETL antes de redactar** y, si el equipo decide entregar con las diferencias, 3.1 las muestra en una tabla.

## 5. Sección 3.1

Tablas (todas con título `Tabla N: …`):
- **Fuentes extraídas:** `Código | Fuente | Archivo | Filas leídas`. Una fila por cada fuente del brief; las filas leídas salen de `tablas` de la evidencia.
- **Pasos del ETL:** `Código | Paso | Tabla | Resultado`.
- **Reglas de calidad:** `Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después`. El defecto es uno de `registro_invalido`, `duplicado`, `nombre_producto`, `formato_fecha`, `nulo` o `dia_sin_precio`. Las filas salen de la evidencia.
- **Tablas cargadas:** `Tabla | Filas cargadas`: todas las del modelo.
- **Diferencias** (solo si la verificación las encontró): `Tabla | Mes | Esperado | Obtenido | Diferencia`.

Con archivos de apoyo en `data/`, **Transformación.** explica cómo se calculan `costo_estimado` y `costo_operativo` (la fórmula de arriba, en palabras). Rótulos en negrita: **Extracción.**, **Transformación.**, **Reglas de calidad.**, **Carga.**, **Verificación.** y **Lectura del ETL.** El párrafo inicial declara que los datos son generados para el proyecto y cómo se calibraron.

## 6. Anexos
- **Anexo A:** «Diccionario de los campos de entrada» (`Fuente | Campo | Tipo | Regla de calidad | Destino`), «Origen de los campos del modelo» (`Tabla | Campo | Origen`, con varios campos por fila separados por punto y coma) y «Resultado de las reglas de calidad» (`Código | Filas antes | Filas después | Filas descartadas`).
- **Anexo B:** el código o los pasos completos que el equipo ejecutó, bajo un rótulo `**PAS-nn.**` por cada paso de 3.1. Si el equipo no trae el código de un paso, el anexo lo dice y el paso no se incluye en 3.1.

## 7. Errores frecuentes
- Redactar con cifras esperadas en lugar de las que trajo el equipo.
- Un defecto de `defectos.csv` sin regla que lo trate.
- Una regla sin cifras de filas antes y después.
- Campos del modelo sin origen en el anexo A.
- Decir que un paso «se ejecutó» antes de tener evidencia.
- Ocultar las diferencias con la hoja de respuestas.
- No explicar de dónde salen los costos cuando el modelo los trae.

## 8. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/etl.py`: encabezados y títulos de tabla, evidencia presente y bien formada, fuentes del brief con sus filas, reglas con evidencia y con las mismas cifras, cada defecto de la hoja de respuestas con su regla, costos explicados si hay archivos de apoyo, tablas cargadas del modelo con las filas de la evidencia, verificación coherente con la evidencia, cifras de filas en el texto que estén en la evidencia, declaración de datos generados, anexo A (campos del modelo con origen y resultados iguales a la evidencia) y anexo B (cada paso con su código).

## Checklist
- [ ] Los datos están generados (o el equipo entregó los autorizados) y el usuario confirmó los parámetros.
- [ ] Hay `evidencia.json` con una fila por regla y por tabla.
- [ ] La comparación con la hoja de respuestas se hizo y su resultado está en 3.1.
- [ ] Cada defecto de `defectos.csv` tiene su `REG-nn`.
- [ ] 3.1 declara que los datos son generados.
- [ ] Todo campo del modelo tiene origen en el anexo A y cada `PAS-nn` tiene su código en el anexo B.
- [ ] Los textos pasaron por el agente `revisor-redactor`.
