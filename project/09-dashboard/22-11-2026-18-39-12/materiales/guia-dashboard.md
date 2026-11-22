# Guía paso a paso del dashboard en Power BI

Esta guía la ejecuta el equipo en Power BI. Está escrita para los datos y el modelo de este proyecto. El código DAX es una propuesta: se prueba, se ajusta y lo que cuenta es el resultado. Compara cada resultado con los valores esperados de la última sección y con el HTML `dashboard-referencia.html`.

## 1. Antes de empezar

1. Debes tener cargado el modelo en estrella que dejó el ETL: las tablas de hechos `fPedidos`, `fProduccion`, `fPrecioInsumo` y `fMetaKpi`, y las dimensiones `dCalendario`, `dProducto`, `dCanal`, `dTurno` y `dKpi`.
2. En la vista **Modelo** crea las relaciones de la tabla siguiente (de varios a uno, con el filtro en una sola dirección). Marca `dCalendario` como tabla de fechas.
3. Crea una tabla vacía para guardar las medidas: **Inicio → Especificar datos**, con una columna cualquiera, y nómbrala `Medidas`. Todas las medidas de esta guía van allí.
4. Si `fPedidos` conserva todas las filas leídas (91 297 en este caso), recuerda que las filas descartadas tienen `registro_valido` = 0 y sus importes en 0: las sumas de venta, comisión y costo solo cuentan las filas válidas.

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | fPedidos | dCalendario | fecha_key | *:1 | Simple |
| REL-02 | fPedidos | dProducto | producto_key | *:1 | Simple |
| REL-03 | fPedidos | dCanal | canal_key | *:1 | Simple |
| REL-04 | fPedidos | dTurno | turno_key | *:1 | Simple |
| REL-05 | fProduccion | dCalendario | fecha_key | *:1 | Simple |
| REL-06 | fProduccion | dTurno | turno_key | *:1 | Simple |
| REL-07 | fPrecioInsumo | dCalendario | fecha_key | *:1 | Simple |
| REL-08 | fMetaKpi | dKpi | kpi_key | *:1 | Simple |
| REL-09 | fMetaKpi | dCalendario | fecha_key | *:1 | Simple |

## 2. Columnas calculadas y de apoyo

Estas columnas no vienen en las fuentes tal cual: se crean en Power Query (la mayoría) o con DAX. Cada fila dice en qué tabla va, cómo se calcula y de qué campos y archivos sale.

| Tabla | Columna | Dónde | Cómo se calcula | Campos y archivos de origen | Para qué sirve |
|---|---|---|---|---|---|
| fPedidos | `venta_bruta` | Power Query | Caja: cantidad × precio_unitario − descuento (descuento vacío = 0). Rappi: monto. PedidosYa: total. WhatsApp: monto. En las filas descartadas, 0. | `cantidad`; `precio_unitario`; `descuento`; `monto`; `total` · `data/fue-01-caja.csv`; `data/fue-02-rappi.csv`; `data/fue-03-pedidosya.csv`; `data/fue-04-whatsapp.csv` | Cada fuente trae el importe con un nombre distinto; se calcula uno solo. |
| fPedidos | `comision` | Power Query | Rappi: la columna comision. PedidosYa: total × comision_pct ÷ 100. Salón, para llevar y WhatsApp: 0. | `comision`; `total`; `comision_pct` · `data/fue-02-rappi.csv`; `data/fue-03-pedidosya.csv` | La comisión de las aplicaciones es el costo de vender por ese canal. |
| fPedidos | `costo_estimado` | Power Query | cantidad × (kg_pollo_vivo × precio_kg del día + costo_otros). El producto se une con el catálogo y el día con fPrecioInsumo (último precio disponible si falta el día). | `cantidad`; `kg_pollo_vivo`; `costo_otros`; `precio_kg` · `data/apoyo-catalogo-productos.csv`; `data/fue-06-precios-pollo.csv` | El costo de los insumos sube cuando sube el pollo vivo. |
| fPedidos | `costo_operativo` | Power Query | total del mes × venta_bruta de la línea ÷ suma de venta_bruta de las líneas válidas del mes. | `total`; `venta_bruta` · `data/apoyo-costos-operativos.csv` | Reparte la planilla, el alquiler, los servicios y otros costos del mes en proporción a la venta. |
| fPedidos | `pollos_equivalentes` | Power Query | cantidad × pollos_equivalentes del producto en el catálogo. | `cantidad`; `pollos_equivalentes` · `data/apoyo-catalogo-productos.csv` | Convierte medios pollos, cuartos y combos a pollos enteros. |
| fPedidos | `registro_valido / registro_total` | Power Query | registro_total = 1 en cada fila leída; registro_valido = 1 si la fila pasa todas las reglas de calidad y 0 si es duplicada o inválida (con sus medidas en 0). | `(todas las reglas del ETL)` · `data/fue-01-caja.csv`; `data/fue-02-rappi.csv`; `data/fue-03-pedidosya.csv`; `data/fue-04-whatsapp.csv` | El ETL conserva todas las filas leídas para poder medir la calidad de datos. |
| fPrecioInsumo | `valor_imputado` | Power Query | 1 si el día no tiene fila en la fuente y se completó con el último precio; 0 en los demás. | `fecha` · `data/fue-06-precios-pollo.csv` | Permite marcar en el gráfico los días sin precio. |
| dCalendario | `anio, mes, nombre_mes, dia_semana` | DAX | anio = YEAR ( [fecha] ); mes = MONTH ( [fecha] ); nombre_mes = FORMAT ( [fecha], "mmm yy" ); dia_semana = FORMAT ( [fecha], "dddd" ). Ordena nombre_mes por mes y dia_semana por WEEKDAY ( [fecha], 2 ). | `fecha` · `(calendario generado desde la fecha mínima y máxima)` | Los gráficos por mes y por día de la semana usan estas columnas. |
| dCalendario | `es_feriado` | Power Query | Verdadero en los feriados nacionales del periodo: 1 de enero, 1 de mayo, 29 de junio, 28 y 29 de julio, 30 de agosto, 8 de octubre, 1 de noviembre, 8 y 25 de diciembre. | `fecha` · `(lista de feriados escrita a mano)` | No alimenta ningún KPI; sirve como filtro. |
| dKpi | `tiene_meta` | Especificar datos | Verdadero si el KPI tiene una meta en la sección 2.5 y no verdadero si dice Pendiente. | `kpi` · `(lista de KPI de la sección 2.5)` | Es la base del KPI-07. |
| fMetaKpi | `meta` | Especificar datos | Meta de cada KPI y mes copiada de la sección 2.5. | `kpi_key`; `fecha_key` · `(metas de la sección 2.5)` | Permite dibujar la meta como línea y calcular el estado. |

## 3. Medidas y KPI

Crea cada medida en la tabla `Medidas` (**clic derecho → Nueva medida**) y pega el DAX. Los nombres entre corchetes deben coincidir exactamente.

### MED-01 · Venta bruta

**Cómo se calcula:** Suma de la venta bruta de las líneas válidas (las líneas descartadas tienen la venta en 0).
**Tablas de origen:** `fPedidos`.

```dax
Venta bruta =
SUM ( fPedidos[venta_bruta] )
```

### MED-02 · Comisión pagada

**Cómo se calcula:** Suma de la comisión que cobran las aplicaciones (0 en salón, para llevar y WhatsApp).
**Tablas de origen:** `fPedidos`.

```dax
Comisión pagada =
SUM ( fPedidos[comision] )
```

### MED-03 · Costo estimado

**Cómo se calcula:** Suma del costo estimado de cada línea: insumos del producto, con el precio del pollo vivo del día.
**Tablas de origen:** `fPedidos`.

```dax
Costo estimado =
SUM ( fPedidos[costo_estimado] )
```

### MED-04 · Costo operativo

**Cómo se calcula:** Suma del costo operativo del mes (planilla, alquiler, servicios y otros) repartido entre las líneas.
**Tablas de origen:** `fPedidos`.

```dax
Costo operativo =
SUM ( fPedidos[costo_operativo] )
```

### MED-05 · Margen de contribución % — KPI-02

**Cómo se calcula:** Lo que queda de cada sol vendido después de la comisión y del costo estimado. Meta: Pendiente.
**Tablas de origen:** `fPedidos`.

```dax
Margen de contribución % =
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado], [Venta bruta] )
```

### MED-06 · Margen neto % — KPI-03

**Cómo se calcula:** Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo. Meta: 12 % o más.
**Tablas de origen:** `fPedidos`.

```dax
Margen neto % =
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado] - [Costo operativo], [Venta bruta] )
```

### MED-07 · Calidad de datos % — KPI-01

**Cómo se calcula:** Filas válidas entre filas leídas de las cuatro fuentes de ventas; el ETL conserva todas las filas y marca cada una con 1 o 0. Meta: 98 % o más.
**Tablas de origen:** `fPedidos`.

```dax
Calidad de datos % =
DIVIDE ( SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] ) )
```

### MED-08 · Pollos preparados

**Cómo se calcula:** Pollos que la cocina preparó en el turno.
**Tablas de origen:** `fProduccion`.

```dax
Pollos preparados =
SUM ( fProduccion[pollos_preparados] )
```

### MED-09 · Pollos vendidos

**Cómo se calcula:** Pollos equivalentes que se vendieron en el turno.
**Tablas de origen:** `fProduccion`.

```dax
Pollos vendidos =
SUM ( fProduccion[pollos_vendidos] )
```

### MED-10 · Pollos de merma

**Cómo se calcula:** Pollos preparados que no se vendieron.
**Tablas de origen:** `fProduccion`.

```dax
Pollos de merma =
SUM ( fProduccion[pollos_merma] )
```

### MED-11 · Merma % — KPI-04

**Cómo se calcula:** Pollos de merma entre pollos preparados. Meta: 3 % o menos.
**Tablas de origen:** `fProduccion`.

```dax
Merma % =
DIVIDE ( [Pollos de merma], [Pollos preparados] )
```

### MED-12 · Precio promedio del pollo vivo — KPI-06

**Cómo se calcula:** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio). Meta: Pendiente.
**Tablas de origen:** `fPrecioInsumo`.

```dax
Precio promedio del pollo vivo =
AVERAGE ( fPrecioInsumo[precio_kg] )
```

### MED-13 · Pronóstico de referencia

**Cómo se calcula:** Promedio de lo vendido en las cuatro jornadas anteriores del mismo día de la semana y el mismo turno.
**Tablas de origen:** `fProduccion`, `dCalendario`, `dTurno`.

```dax
Pronóstico de referencia =
VAR fechaActual = MAX ( dCalendario[fecha] )
VAR diaSemana = WEEKDAY ( fechaActual, 2 )
VAR anteriores =
    TOPN (
        4,
        FILTER ( ALL ( dCalendario ), dCalendario[fecha] < fechaActual && WEEKDAY ( dCalendario[fecha], 2 ) = diaSemana ),
        dCalendario[fecha], DESC
    )
RETURN
    AVERAGEX ( anteriores, CALCULATE ( [Pollos vendidos] ) )
```

### MED-14 · Error del pronóstico % — KPI-05

**Cómo se calcula:** Error porcentual absoluto medio entre lo vendido y el pronóstico, por día y turno. Meta: 15 % o menos.
**Tablas de origen:** `fProduccion`, `dCalendario`, `dTurno`.

```dax
Error del pronóstico % =
AVERAGEX (
    CROSSJOIN ( VALUES ( dCalendario[fecha] ), VALUES ( dTurno[turno] ) ),
    IF ( NOT ISBLANK ( [Pronóstico de referencia] ) && [Pollos vendidos] > 0,
        DIVIDE ( ABS ( [Pollos vendidos] - [Pronóstico de referencia] ), [Pollos vendidos] ) )
)
```

### MED-15 · Participación de ventas %

**Cómo se calcula:** Parte de la venta total que representa cada canal.
**Tablas de origen:** `fPedidos`, `dCanal`.

```dax
Participación de ventas % =
DIVIDE ( [Venta bruta], CALCULATE ( [Venta bruta], ALL ( dCanal[canal] ) ) )
```

### MED-16 · KPI con meta % — KPI-07

**Cómo se calcula:** KPI del dashboard que tienen meta entre todos los KPI. Meta: 100 %.
**Tablas de origen:** `dKpi`.

```dax
KPI con meta % =
DIVIDE ( CALCULATE ( COUNTROWS ( dKpi ), dKpi[tiene_meta] = TRUE () ), COUNTROWS ( dKpi ) )
```

### MED-17 · Meta del KPI

**Cómo se calcula:** Meta cargada para el KPI seleccionado.
**Tablas de origen:** `fMetaKpi`, `dKpi`.

```dax
Meta del KPI =
AVERAGE ( fMetaKpi[meta] )
```

## 4. Páginas y visuales

Crea una página por cada fila de la tabla y arma sus visuales en el orden indicado. Los números coinciden con los del HTML de referencia.

### PAG-01 · Resumen del negocio

**Para quién:** Dueño. **Pregunta que responde:** ¿Gana el negocio lo que debería y qué indicadores están fuera de su meta?

**Tarjetas de KPI (fila superior):** KPI-03 (Margen neto global), KPI-02 (Margen de contribución por canal y producto), KPI-01 (Calidad de datos del ETL), KPI-04 (Porcentaje de merma por turno), KPI-06 (Precio promedio del pollo vivo por kilogramo). Para cada una inserta una **Tarjeta**, arrastra su medida a **Campos** y aplica un formato condicional con la meta (verde si cumple, rojo si no, y agrega el texto del estado).

**Segmentadores:** `dCalendario[anio]`, `dCalendario[nombre_mes]`, `dCanal[canal]`. Inserta un **Segmentador** por cada campo y sincronízalos con las demás páginas.

#### PAG-01 · Visual 1: Margen neto mensual contra la meta

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Margen neto %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Línea de 2 px, etiqueta de datos solo en el último punto; la meta va como línea constante punteada (panel Analytics).

Tablas de origen: `fPedidos`, `dCalendario`. Medidas: MED-06, MED-17.

**Qué debes ver:** El margen baja de 14 % a 8 % y desde febrero de 2026 queda bajo la meta de 12 %.

#### PAG-01 · Visual 2: Ventas mensuales por canal

1. En el panel Visualizaciones elige **Gráfico de columnas apiladas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Venta bruta].
4. Arrastra a **Leyenda** dCanal[canal].
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas apiladas; orden de la leyenda: Salón, Para llevar, WhatsApp, Rappi y PedidosYa.

Tablas de origen: `fPedidos`, `dCalendario`, `dCanal`. Medidas: MED-01.

**Qué debes ver:** Las ventas crecen y las aplicaciones (Rappi y PedidosYa) ocupan una franja cada vez mayor.

#### PAG-01 · Visual 3: KPI del dashboard contra su meta

1. En el panel Visualizaciones elige **Tabla** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Columnas** dKpi[kpi] y cada medida de la lista: [Margen de contribución %], [Margen neto %], [Calidad de datos %], [Merma %], [Precio promedio del pollo vivo], [Error del pronóstico %], [KPI con meta %], [Meta del KPI].
3. En el panel Filtros de este visual aplica: dCalendario[nombre_mes] = último mes del periodo.
4. Tabla con una fila por KPI; el estado se escribe con texto (Cumple, No cumple, Sin meta) y un icono, no solo con color.

Tablas de origen: `dKpi`, `fMetaKpi`. Medidas: MED-05, MED-06, MED-07, MED-11, MED-12, MED-14, MED-16, MED-17.

**Qué debes ver:** La calidad de datos cumple; el margen neto, la merma, el pronóstico y los KPI con meta no cumplen, y dos KPI siguen sin meta.

### PAG-02 · Rentabilidad por canal y producto

**Para quién:** Dueño. **Pregunta que responde:** ¿Qué canales y productos dejan margen después de la comisión?

**Tarjetas de KPI (fila superior):** KPI-02 (Margen de contribución por canal y producto). Para cada una inserta una **Tarjeta**, arrastra su medida a **Campos** y aplica un formato condicional con la meta (verde si cumple, rojo si no, y agrega el texto del estado).

**Segmentadores:** `dCalendario[anio]`, `dCalendario[nombre_mes]`, `dProducto[categoria]`. Inserta un **Segmentador** por cada campo y sincronízalos con las demás páginas.

#### PAG-02 · Visual 1: Margen de contribución por canal

1. En el panel Visualizaciones elige **Gráfico de barras agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dCanal[canal].
3. Arrastra a **Eje Y** [Margen de contribución %].
4. Barras horizontales ordenadas de mayor a menor margen.

Tablas de origen: `fPedidos`, `dCanal`. Medidas: MED-05.

**Qué debes ver:** Salón, para llevar y WhatsApp dejan cerca de 65 %; PedidosYa deja 40.5 % y Rappi 35.5 %, por la comisión.

#### PAG-02 · Visual 2: Margen de contribución por canal y producto

1. En el panel Visualizaciones elige **Matriz** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Filas** dProducto[producto]; a **Columnas** dCanal[canal]; y a **Valores** [Margen de contribución %].
3. Matriz con formato condicional de color de fondo (escala de un solo color).

Tablas de origen: `fPedidos`, `dProducto`, `dCanal`. Medidas: MED-05.

**Qué debes ver:** El color más oscuro marca mayor margen; las aplicaciones bajan en todos los productos.

#### PAG-02 · Visual 3: Participación de las ventas por canal

1. En el panel Visualizaciones elige **Gráfico de columnas apiladas al 100 %** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Participación de ventas %].
4. Arrastra a **Leyenda** dCanal[canal].
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas apiladas al 100 %.

Tablas de origen: `fPedidos`, `dCalendario`, `dCanal`. Medidas: MED-15.

**Qué debes ver:** Las aplicaciones suben de 15 % a 35 % de las ventas.

#### PAG-02 · Visual 4: Comisión pagada por mes

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 4).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Comisión pagada].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Línea de 2 px con etiqueta en el último punto.

Tablas de origen: `fPedidos`, `dCalendario`. Medidas: MED-02.

**Qué debes ver:** La comisión crece junto con la participación de las aplicaciones.

### PAG-03 · Producción y merma por turno

**Para quién:** Jefe de cocina. **Pregunta que responde:** ¿Cuánto pollo se prepara de más o de menos en cada turno y día?

**Tarjetas de KPI (fila superior):** KPI-04 (Porcentaje de merma por turno), KPI-05 (Precisión del pronóstico de demanda). Para cada una inserta una **Tarjeta**, arrastra su medida a **Campos** y aplica un formato condicional con la meta (verde si cumple, rojo si no, y agrega el texto del estado).

**Segmentadores:** `dCalendario[anio]`, `dCalendario[nombre_mes]`, `dTurno[turno]`. Inserta un **Segmentador** por cada campo y sincronízalos con las demás páginas.

#### PAG-03 · Visual 1: Merma por turno contra la meta

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dTurno[turno].
3. Arrastra a **Eje Y** [Merma %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas con la meta como línea constante.

Tablas de origen: `fProduccion`, `dTurno`. Medidas: MED-11.

**Qué debes ver:** Los tres turnos están por encima de la meta de 3 %.

#### PAG-03 · Visual 2: Merma por día de la semana

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[dia_semana] (ordenada de lunes a domingo).
3. Arrastra a **Eje Y** [Merma %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas con la meta como línea constante.

Tablas de origen: `fProduccion`, `dCalendario`. Medidas: MED-11.

**Qué debes ver:** El martes sobra pollo (11.5 %) y el domingo casi no hay merma (3.7 %): falta pollo.

#### PAG-03 · Visual 3: Preparados y vendidos

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[dia_semana] (ordenada de lunes a domingo).
3. Arrastra a **Eje Y** las medidas: [Pollos preparados], [Pollos vendidos].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Columnas agrupadas con dos medidas.

Tablas de origen: `fProduccion`, `dCalendario`. Medidas: MED-08, MED-09.

**Qué debes ver:** La diferencia entre las dos columnas es la merma de cada día.

#### PAG-03 · Visual 4: Vendidos contra pronóstico de referencia (últimos 28 días)

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 4).
2. Arrastra a **Eje X** dCalendario[fecha].
3. Arrastra a **Eje Y** las medidas: [Pollos vendidos], [Pronóstico de referencia].
4. En el panel Filtros de este visual aplica: dCalendario[fecha]: últimos 28 días.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Línea con dos series; el pronóstico va punteado.

Tablas de origen: `fProduccion`, `dCalendario`, `dTurno`. Medidas: MED-09, MED-13.

**Qué debes ver:** El pronóstico sigue el patrón semanal pero no el pico de los fines de semana.

### PAG-04 · Precio del pollo vivo y margen

**Para quién:** Dueño. **Pregunta que responde:** ¿Cómo se mueve el precio del pollo vivo y cómo afecta al margen?

**Tarjetas de KPI (fila superior):** KPI-06 (Precio promedio del pollo vivo por kilogramo). Para cada una inserta una **Tarjeta**, arrastra su medida a **Campos** y aplica un formato condicional con la meta (verde si cumple, rojo si no, y agrega el texto del estado).

**Segmentadores:** `dCalendario[anio]`, `dCalendario[nombre_mes]`. Inserta un **Segmentador** por cada campo y sincronízalos con las demás páginas.

#### PAG-04 · Visual 1: Precio diario del pollo vivo por kilogramo

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dCalendario[fecha].
3. Arrastra a **Eje Y** [Precio promedio del pollo vivo].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Línea de 2 px; los días con fPrecioInsumo[valor_imputado] = 1 se marcan con un punto.

Tablas de origen: `fPrecioInsumo`, `dCalendario`. Medidas: MED-12.

**Qué debes ver:** Entre el 1 y el 14 de julio de 2026 el precio sube de S/ 6.10 a S/ 6.90; los puntos marcan días sin precio.

#### PAG-04 · Visual 2: Margen neto mensual

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Margen neto %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Mismo eje horizontal que el visual 3: dos gráficos alineados en lugar de uno con dos ejes.

Tablas de origen: `fPedidos`, `dCalendario`. Medidas: MED-06.

**Qué debes ver:** El margen sigue bajando después del salto de precio.

#### PAG-04 · Visual 3: Precio promedio mensual del pollo vivo

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[nombre_mes] (ordenada por dCalendario[mes]).
3. Arrastra a **Eje Y** [Precio promedio del pollo vivo].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Mismo eje horizontal que el visual 2.

Tablas de origen: `fPrecioInsumo`, `dCalendario`. Medidas: MED-12.

**Qué debes ver:** El precio se mantiene cerca de S/ 6.10 hasta junio y de S/ 6.90 desde agosto.

## 5. Valores esperados para comparar

Son los de `data/respuestas/kpi-esperados.csv`. Con filtros por mes deben coincidir con tu dashboard, salvo el pronóstico.

| Mes | KPI-01 | KPI-02 | KPI-03 | KPI-04 | KPI-05 | KPI-06 |
|---|---|---|---|---|---|---|
| 2025-08 | 98.77 | 61.28 | 14.0 | 7.42 | 18.64 | 6.06 |
| 2025-09 | 98.93 | 60.95 | 13.5 | 7.59 | 28.68 | 6.07 |
| 2025-10 | 98.53 | 60.61 | 12.92 | 7.34 | 33.59 | 6.03 |
| 2025-11 | 98.79 | 60.03 | 12.72 | 6.78 | 28.82 | 6.1 |
| 2025-12 | 98.54 | 59.76 | 12.32 | 6.73 | 25.73 | 6.06 |
| 2026-01 | 98.24 | 59.39 | 12.05 | 6.78 | 31.08 | 6.13 |
| 2026-02 | 98.34 | 59.03 | 11.11 | 7.2 | 28.24 | 6.07 |
| 2026-03 | 98.47 | 58.5 | 10.72 | 7.23 | 30.3 | 6.12 |
| 2026-04 | 98.47 | 58.2 | 10.59 | 7.22 | 29.0 | 6.08 |
| 2026-05 | 98.12 | 57.72 | 10.38 | 6.61 | 32.18 | 6.08 |
| 2026-06 | 98.43 | 57.47 | 9.53 | 7.44 | 27.28 | 6.06 |
| 2026-07 | 98.13 | 55.67 | 9.1 | 6.73 | 28.93 | 6.79 |
| 2026-08 | 98.47 | 55.17 | 8.52 | 6.74 | 38.48 | 6.9 |
| 2026-09 | 98.45 | 54.59 | 8.65 | 7.07 | 25.47 | 6.98 |
| 2026-10 | 98.29 | 54.44 | 8.0 | 6.44 | 28.19 | 6.82 |

Unidades: KPI-01 a KPI-05 en porcentaje; KPI-06 en soles por kilogramo.

**Advertencia sobre el pronóstico (KPI-05).** El valor esperado usa un método simple: el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. El pronóstico de Power BI (Analytics → Pronóstico) usa suavizado exponencial con estacionalidad y no coincidirá exactamente. Para comparar, usa la medida «Pronóstico de referencia» de esta guía.

