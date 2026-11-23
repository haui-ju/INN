# Guía paso a paso del dashboard en Power BI

Esta guía la ejecuta el equipo en Power BI y está escrita para los datos y el modelo de este proyecto. Hay una sección por página. En cada una vas elemento por elemento (segmentadores, tarjetas y gráficos) y, en cada elemento, ves qué muestra, cómo se calcula, de qué tablas y columnas sale, su fórmula, cómo armarlo y el valor esperado. Cada medida y cada columna calculada se explica **en el primer elemento que la usa**; después solo se la menciona. El DAX es una propuesta que se prueba y se ajusta. Compara cada resultado con el valor esperado y con el HTML `dashboard-referencia.html`.

Antes de la primera página, parte del modelo que dejó el ETL (nueve tablas y nueve relaciones, con `dCalendario` marcada como tabla de fechas) y crea una tabla vacía para guardar las medidas: **Inicio ▸ Especificar datos**, con una columna cualquiera, y nómbrala `Medidas`. `fPedidos` conserva todas las filas leídas (91 297 en este caso) y las descartadas tienen `registro_valido` = 0 e importes en 0: por eso las sumas de venta, comisión y costo solo cuentan las filas válidas.

## PAG-01 · Resumen del negocio

**Para quién:** Dueño. **Pregunta que responde:** ¿Gana el negocio lo que debería y qué indicadores están fuera de su meta?

### Elemento 1 · Segmentadores

**Qué muestra.** Filtros para recortar toda la página por periodo, canal o turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `dCalendario[anio]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[nombre_mes]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCanal[canal]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Cómo armarlo en Power BI.**

1. Inserta un **Segmentador** por cada campo de la tabla anterior (arrastra el campo a **Campo**).
2. Para `dCalendario[nombre_mes]` ordena por `mes`: Herramientas de columna ▸ **Ordenar por columna** ▸ `mes`.
3. En **Vista ▸ Sincronizar segmentadores** activa la sincronización con las demás páginas.

**Valor esperado.** No tiene valor: al filtrar, todos los elementos de la página deben recalcularse.

### Elemento 2 · Tarjeta KPI-03 · Margen neto global

**Qué muestra.** El valor del indicador KPI-03 para el periodo que filtres, con su meta (12 % o más) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | **Columna calculada** (Power Query). Caja: cantidad × precio_unitario − descuento (descuento vacío = 0). Rappi: monto. PedidosYa: total. WhatsApp: monto. En las filas descartadas, 0. | Campos: `cantidad`; `precio_unitario`; `descuento`; `monto`; `total`. Archivos: `data/fue-01-caja.csv`; `data/fue-02-rappi.csv`; `data/fue-03-pedidosya.csv`; `data/fue-04-whatsapp.csv`. Cada fuente trae el importe con un nombre distinto; se calcula uno solo. |
| `fPedidos[comision]` | **Columna calculada** (Power Query). Rappi: la columna comision. PedidosYa: total × comision_pct ÷ 100. Salón, para llevar y WhatsApp: 0. | Campos: `comision`; `total`; `comision_pct`. Archivos: `data/fue-02-rappi.csv`; `data/fue-03-pedidosya.csv`. La comisión de las aplicaciones es el costo de vender por ese canal. |
| `fPedidos[costo_estimado]` | **Columna calculada** (Power Query). cantidad × (kg_pollo_vivo × precio_kg del día + costo_otros). El producto se une con el catálogo y el día con fPrecioInsumo (último precio disponible si falta el día). | Campos: `cantidad`; `kg_pollo_vivo`; `costo_otros`; `precio_kg`. Archivos: `data/apoyo-catalogo-productos.csv`; `data/fue-06-precios-pollo.csv`. El costo de los insumos sube cuando sube el pollo vivo. |
| `fPedidos[costo_operativo]` | **Columna calculada** (Power Query). total del mes × venta_bruta de la línea ÷ suma de venta_bruta de las líneas válidas del mes. | Campos: `total`; `venta_bruta`. Archivos: `data/apoyo-costos-operativos.csv`. Reparte la planilla, el alquiler, los servicios y otros costos del mes en proporción a la venta. |

**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):

- **MED-01** · **Medida `Venta bruta`**: Suma de la venta bruta de las líneas válidas (las líneas descartadas tienen la venta en 0). Tablas: `fPedidos`.

```dax
Venta bruta =
SUM ( fPedidos[venta_bruta] )
```

- **MED-02** · **Medida `Comisión pagada`**: Suma de la comisión que cobran las aplicaciones (0 en salón, para llevar y WhatsApp). Tablas: `fPedidos`.

```dax
Comisión pagada =
SUM ( fPedidos[comision] )
```

- **MED-03** · **Medida `Costo estimado`**: Suma del costo estimado de cada línea: insumos del producto, con el precio del pollo vivo del día. Tablas: `fPedidos`.

```dax
Costo estimado =
SUM ( fPedidos[costo_estimado] )
```

- **MED-04** · **Medida `Costo operativo`**: Suma del costo operativo del mes (planilla, alquiler, servicios y otros) repartido entre las líneas. Tablas: `fPedidos`.

```dax
Costo operativo =
SUM ( fPedidos[costo_operativo] )
```

- **MED-06** · **Medida `Margen neto %`** (KPI-03): Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo. Meta: 12 % o más. Tablas: `fPedidos`.

```dax
Margen neto % =
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado] - [Costo operativo], [Venta bruta] )
```

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Margen neto %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: verde si el valor es mayor o igual a 12 y rojo en caso contrario.
4. Agrega como subtítulo el texto «Meta: 12 % o más» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **8.0 %** → No cumple (meta 12 % o más). Primer mes (ago 25): 14.0 %.

### Elemento 3 · Tarjeta KPI-02 · Margen de contribución por canal y producto

**Qué muestra.** El valor del indicador KPI-02 para el periodo que filtres, con su meta (Pendiente) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Lo que queda de cada sol vendido después de la comisión y del costo estimado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| [Venta bruta] | Medida | Ya la creaste en PAG-01 · Elemento 2 |
| [Comisión pagada] | Medida | Ya la creaste en PAG-01 · Elemento 2 |
| [Costo estimado] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):

- **MED-05** · **Medida `Margen de contribución %`** (KPI-02): Lo que queda de cada sol vendido después de la comisión y del costo estimado. Meta: Pendiente. Tablas: `fPedidos`.

```dax
Margen de contribución % =
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado], [Venta bruta] )
```

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Margen de contribución %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: deja un color neutro: este indicador no tiene meta todavía (aparece como «Sin meta»).
4. Agrega como subtítulo el texto «Meta: Pendiente» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **54.4 %** → Sin meta (meta Pendiente). Primer mes (ago 25): 61.3 %.

### Elemento 4 · Tarjeta KPI-01 · Calidad de datos del ETL

**Qué muestra.** El valor del indicador KPI-01 para el periodo que filtres, con su meta (98 % o más) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Filas válidas entre filas leídas de las cuatro fuentes de ventas; el ETL conserva todas las filas y marca cada una con 1 o 0.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[registro_valido]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fPedidos[registro_total]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):

- **MED-07** · **Medida `Calidad de datos %`** (KPI-01): Filas válidas entre filas leídas de las cuatro fuentes de ventas; el ETL conserva todas las filas y marca cada una con 1 o 0. Meta: 98 % o más. Tablas: `fPedidos`.

```dax
Calidad de datos % =
DIVIDE ( SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] ) )
```

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Calidad de datos %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: verde si el valor es mayor o igual a 98 y rojo en caso contrario.
4. Agrega como subtítulo el texto «Meta: 98 % o más» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **98.3 %** → Cumple (meta 98 % o más). Primer mes (ago 25): 98.8 %.

### Elemento 5 · Tarjeta KPI-04 · Porcentaje de merma por turno

**Qué muestra.** El valor del indicador KPI-04 para el periodo que filtres, con su meta (3 % o menos) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Pollos de merma entre pollos preparados.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_merma]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):

- **MED-10** · **Medida `Pollos de merma`**: Pollos preparados que no se vendieron. Tablas: `fProduccion`.

```dax
Pollos de merma =
SUM ( fProduccion[pollos_merma] )
```

- **MED-08** · **Medida `Pollos preparados`**: Pollos que la cocina preparó en el turno. Tablas: `fProduccion`.

```dax
Pollos preparados =
SUM ( fProduccion[pollos_preparados] )
```

- **MED-11** · **Medida `Merma %`** (KPI-04): Pollos de merma entre pollos preparados. Meta: 3 % o menos. Tablas: `fProduccion`.

```dax
Merma % =
DIVIDE ( [Pollos de merma], [Pollos preparados] )
```

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Merma %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: verde si el valor es menor o igual a 3 y rojo en caso contrario.
4. Agrega como subtítulo el texto «Meta: 3 % o menos» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **6.4 %** → No cumple (meta 3 % o menos). Primer mes (ago 25): 7.4 %.

### Elemento 6 · Tarjeta KPI-06 · Precio promedio del pollo vivo por kilogramo

**Qué muestra.** El valor del indicador KPI-06 para el periodo que filtres, con su meta (Pendiente) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPrecioInsumo[precio_kg]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):

- **MED-12** · **Medida `Precio promedio del pollo vivo`** (KPI-06): Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio). Meta: Pendiente. Tablas: `fPrecioInsumo`.

```dax
Precio promedio del pollo vivo =
AVERAGE ( fPrecioInsumo[precio_kg] )
```

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Precio promedio del pollo vivo]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: deja un color neutro: este indicador no tiene meta todavía (aparece como «Sin meta»).
4. Agrega como subtítulo el texto «Meta: Pendiente» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **S/ 6.82** → Sin meta (meta Pendiente). Primer mes (ago 25): S/ 6.06.

### Elemento 7 · Gráfico de líneas: Margen neto mensual contra la meta

**Qué muestra.** El margen baja de 14 % a 8 % y desde febrero de 2026 queda bajo la meta de 12 %.

**Cómo se calcula.**

- **Margen neto %:** Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo.
- **Meta del KPI:** Meta cargada para el KPI seleccionado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_operativo]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fMetaKpi[meta]` | **Columna calculada** (Power Query (guía de ETL, PAS-10 y PAS-14)). Meta de cada KPI y mes copiada de la sección 2.5. | Campos: `kpi_key`; `fecha_key`. Archivos: `(metas de la sección 2.5)`. Permite dibujar la meta como línea y calcular el estado. |
| `dCalendario[mes_anio]` | **Columna calculada** (Power Query (guía de ETL, PAS-10)). Abreviatura del mes y año de dos dígitos: «ago 25», «oct 26». Ordénala por anio_mes. | Campos: `fecha`. Archivos: `(se calcula desde la fecha de dCalendario)`. Es el eje de tiempo de los gráficos por mes: un punto por cada uno de los 15 meses. |
| `dCalendario[anio_mes]` | **Columna calculada** (Power Query (guía de ETL, PAS-10)). anio × 100 + mes: 202508 es agosto de 2025. Sirve para ordenar los meses cronológicamente. | Campos: `fecha`. Archivos: `(se calcula desde la fecha de dCalendario)`. El periodo tiene dos agostos, dos septiembres y dos octubres: sin esta columna el eje por mes juntaría los dos años en un solo punto. |
| [Margen neto %] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Margen neto %] |

**Fórmulas.** Crea en la tabla `Medidas` las que todavía no tengas:

- **MED-17** · **Medida `Meta del KPI`**: Meta cargada para el KPI seleccionado. Tablas: `fMetaKpi`, `dKpi`.

```dax
Meta del KPI =
AVERAGE ( fMetaKpi[meta] )
```

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Margen neto %].
5. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
6. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
7. Línea de 2 px, etiqueta de datos solo en el último punto; la meta va como línea constante punteada (panel Analytics).

**Valor esperado.** ago 25: 14.0 % → oct 26: 8.0 %.

### Elemento 8 · Gráfico de columnas apiladas: Ventas mensuales por canal

**Qué muestra.** Las ventas crecen y las aplicaciones (Rappi y PedidosYa) ocupan una franja cada vez mayor.

**Cómo se calcula.**

- **Venta bruta:** Suma de la venta bruta de las líneas válidas (las líneas descartadas tienen la venta en 0).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCalendario[anio_mes]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCanal[canal]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Venta bruta] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Venta bruta] |
| Leyenda | dCanal[canal] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Venta bruta]` (PAG-01 · Elemento 2).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de columnas apiladas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Venta bruta].
5. Arrastra a **Leyenda** dCanal[canal].
6. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
7. Columnas apiladas; orden de la leyenda: Salón, Para llevar, WhatsApp, Rappi y PedidosYa.

**Valor esperado.** Salón: S/ 68 593 → S/ 60 633; Para llevar: S/ 63 440 → S/ 54 272; WhatsApp: S/ 17 697 → S/ 26 102; Rappi: S/ 15 935 → S/ 43 733; PedidosYa: S/ 10 647 → S/ 32 602.

### Elemento 9 · Tabla: KPI del dashboard contra su meta

**Qué muestra.** La calidad de datos cumple; el margen neto, la merma, el pronóstico y los KPI con meta no cumplen, y dos KPI siguen sin meta.

**Cómo se calcula.**

- **Margen de contribución %:** Lo que queda de cada sol vendido después de la comisión y del costo estimado.
- **Margen neto %:** Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo.
- **Calidad de datos %:** Filas válidas entre filas leídas de las cuatro fuentes de ventas; el ETL conserva todas las filas y marca cada una con 1 o 0.
- **Merma %:** Pollos de merma entre pollos preparados.
- **Precio promedio del pollo vivo:** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio).
- **Error del pronóstico %:** Error porcentual absoluto medio entre lo vendido y el pronóstico, por día y turno.
- **KPI con meta %:** KPI del dashboard que tienen meta entre todos los KPI.
- **Meta del KPI:** Meta cargada para el KPI seleccionado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_operativo]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[registro_valido]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fPedidos[registro_total]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_merma]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fPrecioInsumo[precio_kg]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_vendidos]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[fecha]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dTurno[turno]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dKpi[tiene_meta]` | **Columna calculada** (Power Query (guía de ETL, PAS-10 y PAS-14)). Verdadero si el KPI tiene una meta en la sección 2.5 y no verdadero si dice Pendiente. | Campos: `kpi`. Archivos: `(lista de KPI de la sección 2.5)`. Es la base del KPI-07. |
| `fMetaKpi[meta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dKpi[kpi]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| [Margen de contribución %] | Medida | Ya la creaste en PAG-01 · Elemento 3 |
| [Margen neto %] | Medida | Ya la creaste en PAG-01 · Elemento 2 |
| [Calidad de datos %] | Medida | Ya la creaste en PAG-01 · Elemento 4 |
| [Merma %] | Medida | Ya la creaste en PAG-01 · Elemento 5 |
| [Precio promedio del pollo vivo] | Medida | Ya la creaste en PAG-01 · Elemento 6 |
| [Meta del KPI] | Medida | Ya la creaste en PAG-01 · Elemento 7 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dKpi[kpi] |
| Valores (eje Y) | [Margen neto %], [Margen de contribución %], [Calidad de datos %], [Merma %], [Error del pronóstico %], [Precio promedio del pollo vivo], [KPI con meta %] |

**Fórmulas.** Crea en la tabla `Medidas` las que todavía no tengas:

- **MED-09** · **Medida `Pollos vendidos`**: Pollos equivalentes que se vendieron en el turno. Tablas: `fProduccion`.

```dax
Pollos vendidos =
SUM ( fProduccion[pollos_vendidos] )
```

- **MED-13** · **Medida `Pronóstico de referencia`**: Promedio de lo vendido en las cuatro jornadas anteriores del mismo día de la semana y el mismo turno. Tablas: `fProduccion`, `dCalendario`, `dTurno`.

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

- **MED-14** · **Medida `Error del pronóstico %`** (KPI-05): Error porcentual absoluto medio entre lo vendido y el pronóstico, por día y turno. Meta: 15 % o menos. Tablas: `fProduccion`, `dCalendario`, `dTurno`.

```dax
Error del pronóstico % =
AVERAGEX (
    CROSSJOIN ( VALUES ( dCalendario[fecha] ), VALUES ( dTurno[turno] ) ),
    IF ( NOT ISBLANK ( [Pronóstico de referencia] ) && [Pollos vendidos] > 0,
        DIVIDE ( ABS ( [Pollos vendidos] - [Pronóstico de referencia] ), [Pollos vendidos] ) )
)
```

- **MED-16** · **Medida `KPI con meta %`** (KPI-07): KPI del dashboard que tienen meta entre todos los KPI. Meta: 100 %. Tablas: `dKpi`.

```dax
KPI con meta % =
DIVIDE ( CALCULATE ( COUNTROWS ( dKpi ), dKpi[tiene_meta] = TRUE () ), COUNTROWS ( dKpi ) )
```

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Tabla** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Columnas** dKpi[kpi] y cada medida de la lista: [Margen de contribución %], [Margen neto %], [Calidad de datos %], [Merma %], [Precio promedio del pollo vivo], [Error del pronóstico %], [KPI con meta %], [Meta del KPI].
3. En el panel Filtros de este visual aplica: dCalendario[mes_anio] = último mes del periodo.
4. Tabla con una fila por KPI; el estado se escribe con texto (Cumple, No cumple, Sin meta) y un icono, no solo con color.

**Valor esperado.** 7 filas, mes oct 26.

> El pronóstico de referencia es el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. El pronóstico de Power BI **no coincidirá exactamente**; para comparar usa la medida «Pronóstico de referencia».

## PAG-02 · Rentabilidad por canal y producto

**Para quién:** Dueño. **Pregunta que responde:** ¿Qué canales y productos dejan margen después de la comisión?

### Elemento 1 · Segmentadores

**Qué muestra.** Filtros para recortar toda la página por periodo, canal o turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `dCalendario[anio]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[nombre_mes]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dProducto[categoria]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Cómo armarlo en Power BI.**

1. Inserta un **Segmentador** por cada campo de la tabla anterior (arrastra el campo a **Campo**).
2. Para `dCalendario[nombre_mes]` ordena por `mes`: Herramientas de columna ▸ **Ordenar por columna** ▸ `mes`.
3. En **Vista ▸ Sincronizar segmentadores** activa la sincronización con las demás páginas.

**Valor esperado.** No tiene valor: al filtrar, todos los elementos de la página deben recalcularse.

### Elemento 2 · Tarjeta KPI-02 · Margen de contribución por canal y producto

**Qué muestra.** El valor del indicador KPI-02 para el periodo que filtres, con su meta (Pendiente) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Lo que queda de cada sol vendido después de la comisión y del costo estimado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| [Venta bruta] | Medida | Ya la creaste en PAG-01 · Elemento 2 |
| [Comisión pagada] | Medida | Ya la creaste en PAG-01 · Elemento 2 |
| [Costo estimado] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

**Fórmula.** Usa la medida `[Margen de contribución %]`, que ya creaste en PAG-01 · Elemento 3.

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Margen de contribución %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: deja un color neutro: este indicador no tiene meta todavía (aparece como «Sin meta»).
4. Agrega como subtítulo el texto «Meta: Pendiente» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **54.4 %** → Sin meta (meta Pendiente). Primer mes (ago 25): 61.3 %.

### Elemento 3 · Gráfico de barras agrupadas (horizontales): Margen de contribución por canal

**Qué muestra.** Salón, para llevar y WhatsApp dejan cerca de 65 %; PedidosYa deja 40.5 % y Rappi 35.5 %, por la comisión.

**Cómo se calcula.**

- **Margen de contribución %:** Lo que queda de cada sol vendido después de la comisión y del costo estimado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dCanal[canal]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Margen de contribución %] | Medida | Ya la creaste en PAG-01 · Elemento 3 |

| Dónde va | Campo |
|---|---|
| Eje Y (categorías) | dCanal[canal] |
| Eje X (valores) | [Margen de contribución %] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Margen de contribución %]` (PAG-01 · Elemento 3).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de barras agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje Y** dCanal[canal] (en las barras horizontales las categorías van en el eje Y y la medida en el eje X; si lo pones al revés, Power BI dice que el campo no es una medida).
3. Arrastra a **Eje X** [Margen de contribución %].
4. Barras horizontales ordenadas de mayor a menor margen.

**Valor esperado.** Para llevar: 65.3 %; WhatsApp: 65.1 %; Salón: 64.7 %; PedidosYa: 40.5 %; Rappi: 35.5 %.

### Elemento 4 · Matriz: Margen de contribución por canal y producto

**Qué muestra.** El color más oscuro marca mayor margen; las aplicaciones bajan en todos los productos.

**Cómo se calcula.**

- **Margen de contribución %:** Lo que queda de cada sol vendido después de la comisión y del costo estimado.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dProducto[producto]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCanal[canal]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Margen de contribución %] | Medida | Ya la creaste en PAG-01 · Elemento 3 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dProducto[producto] |
| Valores (eje Y) | [Margen de contribución %] |
| Columnas | dCanal[canal] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Margen de contribución %]` (PAG-01 · Elemento 3).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Matriz** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Filas** dProducto[producto]; a **Columnas** dCanal[canal]; y a **Valores** [Margen de contribución %].
3. Matriz con formato condicional de color de fondo (escala de un solo color).

**Valor esperado.** de 27.6 % a 68.6 %.

### Elemento 5 · Gráfico de columnas apiladas al 100 %: Participación de las ventas por canal

**Qué muestra.** Las aplicaciones suben de 15 % a 35 % de las ventas.

**Cómo se calcula.**

- **Participación de ventas %:** Parte de la venta total que representa cada canal.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dCanal[canal]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCalendario[anio_mes]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Participación de ventas %] |
| Leyenda | dCanal[canal] |

**Fórmulas.** Crea en la tabla `Medidas` las que todavía no tengas:

- **MED-15** · **Medida `Participación de ventas %`**: Parte de la venta total que representa cada canal. Tablas: `fPedidos`, `dCanal`.

```dax
Participación de ventas % =
DIVIDE ( [Venta bruta], CALCULATE ( [Venta bruta], ALL ( dCanal[canal] ) ) )
```

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de columnas apiladas al 100 %** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Participación de ventas %].
5. Arrastra a **Leyenda** dCanal[canal].
6. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
7. Columnas apiladas al 100 %.

**Valor esperado.** Salón: 38.9 % → 27.9 %; Para llevar: 36.0 % → 25.0 %; WhatsApp: 10.0 % → 12.0 %; Rappi: 9.0 % → 20.1 %; PedidosYa: 6.0 % → 15.0 %.

### Elemento 6 · Gráfico de líneas: Comisión pagada por mes

**Qué muestra.** La comisión crece junto con la participación de las aplicaciones.

**Cómo se calcula.**

- **Comisión pagada:** Suma de la comisión que cobran las aplicaciones (0 en salón, para llevar y WhatsApp).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCalendario[anio_mes]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| [Comisión pagada] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Comisión pagada] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Comisión pagada]` (PAG-01 · Elemento 2).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 4).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Comisión pagada].
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Línea de 2 px con etiqueta en el último punto.

**Valor esperado.** ago 25: S/ 7 442 → oct 26: S/ 21 270.

## PAG-03 · Producción y merma por turno

**Para quién:** Jefe de cocina. **Pregunta que responde:** ¿Cuánto pollo se prepara de más o de menos en cada turno y día?

### Elemento 1 · Segmentadores

**Qué muestra.** Filtros para recortar toda la página por periodo, canal o turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `dCalendario[anio]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[nombre_mes]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dTurno[turno]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Cómo armarlo en Power BI.**

1. Inserta un **Segmentador** por cada campo de la tabla anterior (arrastra el campo a **Campo**).
2. Para `dCalendario[nombre_mes]` ordena por `mes`: Herramientas de columna ▸ **Ordenar por columna** ▸ `mes`.
3. En **Vista ▸ Sincronizar segmentadores** activa la sincronización con las demás páginas.

**Valor esperado.** No tiene valor: al filtrar, todos los elementos de la página deben recalcularse.

### Elemento 2 · Tarjeta KPI-04 · Porcentaje de merma por turno

**Qué muestra.** El valor del indicador KPI-04 para el periodo que filtres, con su meta (3 % o menos) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Pollos de merma entre pollos preparados.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_merma]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Pollos de merma] | Medida | Ya la creaste en PAG-01 · Elemento 5 |
| [Pollos preparados] | Medida | Ya la creaste en PAG-01 · Elemento 5 |

**Fórmula.** Usa la medida `[Merma %]`, que ya creaste en PAG-01 · Elemento 5.

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Merma %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: verde si el valor es menor o igual a 3 y rojo en caso contrario.
4. Agrega como subtítulo el texto «Meta: 3 % o menos» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **6.4 %** → No cumple (meta 3 % o menos). Primer mes (ago 25): 7.4 %.

### Elemento 3 · Tarjeta KPI-05 · Precisión del pronóstico de demanda

**Qué muestra.** El valor del indicador KPI-05 para el periodo que filtres, con su meta (15 % o menos) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Error porcentual absoluto medio entre lo vendido y el pronóstico, por día y turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_vendidos]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[fecha]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dTurno[turno]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Pronóstico de referencia] | Medida | Ya la creaste en PAG-01 · Elemento 9 |
| [Pollos vendidos] | Medida | Ya la creaste en PAG-01 · Elemento 9 |

**Fórmula.** Usa la medida `[Error del pronóstico %]`, que ya creaste en PAG-01 · Elemento 9.

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Error del pronóstico %]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: verde si el valor es menor o igual a 15 y rojo en caso contrario.
4. Agrega como subtítulo el texto «Meta: 15 % o menos» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **28.2 %** → No cumple (meta 15 % o menos). Primer mes (ago 25): 18.6 %.

> El pronóstico de referencia usa un método simple: el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. El pronóstico de Power BI (Analytics ▸ Pronóstico) usa suavizado exponencial con estacionalidad y **no coincidirá exactamente**.

### Elemento 4 · Gráfico de columnas agrupadas: Merma por turno contra la meta

**Qué muestra.** Los tres turnos están por encima de la meta de 3 %.

**Cómo se calcula.**

- **Merma %:** Pollos de merma entre pollos preparados.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_merma]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dTurno[turno]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Merma %] | Medida | Ya la creaste en PAG-01 · Elemento 5 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dTurno[turno] |
| Valores (eje Y) | [Merma %] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Merma %]` (PAG-01 · Elemento 5).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dTurno[turno].
3. Arrastra a **Eje Y** [Merma %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas con la meta como línea constante.

**Valor esperado.** Mañana: 6.7 %; Tarde: 8.3 %; Noche: 6.6 %.

### Elemento 5 · Gráfico de columnas agrupadas: Merma por día de la semana

**Qué muestra.** El martes sobra pollo (11.5 %) y el domingo casi no hay merma (3.7 %): falta pollo.

**Cómo se calcula.**

- **Merma %:** Pollos de merma entre pollos preparados.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_merma]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[dia_semana]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Merma %] | Medida | Ya la creaste en PAG-01 · Elemento 5 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[dia_semana] (ordenada de lunes a domingo) |
| Valores (eje Y) | [Merma %] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Merma %]` (PAG-01 · Elemento 5).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[dia_semana] (ordenada de lunes a domingo).
3. Arrastra a **Eje Y** [Merma %].
4. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Columnas con la meta como línea constante.

**Valor esperado.** Lunes: 8.3 %; Martes: 11.5 %; Miércoles: 8.2 %; Jueves: 7.9 %; Viernes: 6.6 %; Sábado: 6.1 %; Domingo: 3.7 %.

### Elemento 6 · Gráfico de columnas agrupadas: Preparados y vendidos

**Qué muestra.** La diferencia entre las dos columnas es la merma de cada día.

**Cómo se calcula.**

- **Pollos preparados:** Pollos que la cocina preparó en el turno.
- **Pollos vendidos:** Pollos equivalentes que se vendieron en el turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_preparados]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `fProduccion[pollos_vendidos]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[dia_semana]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Pollos preparados] | Medida | Ya la creaste en PAG-01 · Elemento 5 |
| [Pollos vendidos] | Medida | Ya la creaste en PAG-01 · Elemento 9 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[dia_semana] (ordenada de lunes a domingo) |
| Valores (eje Y) | [Pollos preparados], [Pollos vendidos] |
| Leyenda | Medidas en la leyenda |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Pollos preparados]` (PAG-01 · Elemento 5), `[Pollos vendidos]` (PAG-01 · Elemento 9).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de columnas agrupadas** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[dia_semana] (ordenada de lunes a domingo).
3. Arrastra a **Eje Y** las medidas: [Pollos preparados], [Pollos vendidos].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Columnas agrupadas con dos medidas.

**Valor esperado.** Domingo: Pollos preparados 6 062; Pollos vendidos 5 835.

### Elemento 7 · Gráfico de líneas: Vendidos contra pronóstico de referencia (últimos 28 días)

**Qué muestra.** El pronóstico sigue el patrón semanal pero no el pico de los fines de semana.

**Cómo se calcula.**

- **Pollos vendidos:** Pollos equivalentes que se vendieron en el turno.
- **Pronóstico de referencia:** Promedio de lo vendido en las cuatro jornadas anteriores del mismo día de la semana y el mismo turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fProduccion[pollos_vendidos]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[fecha]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Pollos vendidos] | Medida | Ya la creaste en PAG-01 · Elemento 9 |
| [Pronóstico de referencia] | Medida | Ya la creaste en PAG-01 · Elemento 9 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[fecha] |
| Valores (eje Y) | [Pollos vendidos], [Pronóstico de referencia] |
| Leyenda | Medidas en la leyenda |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Pollos vendidos]` (PAG-01 · Elemento 9), `[Pronóstico de referencia]` (PAG-01 · Elemento 9).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 4).
2. Arrastra a **Eje X** dCalendario[fecha].
3. Arrastra a **Eje Y** las medidas: [Pollos vendidos], [Pronóstico de referencia].
4. En el panel Filtros de este visual aplica: dCalendario[fecha]: últimos 28 días.
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Línea con dos series; el pronóstico va punteado.

**Valor esperado.** 31/10: Pollos vendidos 89; Pronóstico de referencia 100.

> El pronóstico de referencia es el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. El pronóstico de Power BI **no coincidirá exactamente**; para comparar usa la medida «Pronóstico de referencia».

## PAG-04 · Precio del pollo vivo y margen

**Para quién:** Dueño. **Pregunta que responde:** ¿Cómo se mueve el precio del pollo vivo y cómo afecta al margen?

### Elemento 1 · Segmentadores

**Qué muestra.** Filtros para recortar toda la página por periodo, canal o turno.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `dCalendario[anio]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[nombre_mes]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Cómo armarlo en Power BI.**

1. Inserta un **Segmentador** por cada campo de la tabla anterior (arrastra el campo a **Campo**).
2. Para `dCalendario[nombre_mes]` ordena por `mes`: Herramientas de columna ▸ **Ordenar por columna** ▸ `mes`.
3. En **Vista ▸ Sincronizar segmentadores** activa la sincronización con las demás páginas.

**Valor esperado.** No tiene valor: al filtrar, todos los elementos de la página deben recalcularse.

### Elemento 2 · Tarjeta KPI-06 · Precio promedio del pollo vivo por kilogramo

**Qué muestra.** El valor del indicador KPI-06 para el periodo que filtres, con su meta (Pendiente) y un estado: Cumple, No cumple o Sin meta.

**Cómo se calcula.** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPrecioInsumo[precio_kg]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |

**Fórmula.** Usa la medida `[Precio promedio del pollo vivo]`, que ya creaste en PAG-01 · Elemento 6.

**Cómo armarlo en Power BI.**

1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).
2. Arrastra la medida `[Precio promedio del pollo vivo]` al campo **Campos**.
3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: deja un color neutro: este indicador no tiene meta todavía (aparece como «Sin meta»).
4. Agrega como subtítulo el texto «Meta: Pendiente» y el nombre del indicador como título.

**Valor esperado.** último mes (oct 26): **S/ 6.82** → Sin meta (meta Pendiente). Primer mes (ago 25): S/ 6.06.

### Elemento 3 · Gráfico de líneas: Precio diario del pollo vivo por kilogramo

**Qué muestra.** Entre el 1 y el 14 de julio de 2026 el precio sube de S/ 6.10 a S/ 6.90; los puntos marcan días sin precio.

**Cómo se calcula.**

- **Precio promedio del pollo vivo:** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPrecioInsumo[precio_kg]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[fecha]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| [Precio promedio del pollo vivo] | Medida | Ya la creaste en PAG-01 · Elemento 6 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[fecha] |
| Valores (eje Y) | [Precio promedio del pollo vivo] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Precio promedio del pollo vivo]` (PAG-01 · Elemento 6).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 1).
2. Arrastra a **Eje X** dCalendario[fecha].
3. Arrastra a **Eje Y** [Precio promedio del pollo vivo].
4. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
5. Línea de 2 px; los días con fPrecioInsumo[valor_imputado] = 1 se marcan con un punto.

**Valor esperado.** 2025-08-01: S/ 6.14; 14/07/2026: S/ 6.90; 2026-10-31: S/ 6.85.

### Elemento 4 · Gráfico de líneas: Margen neto mensual

**Qué muestra.** El margen sigue bajando después del salto de precio.

**Cómo se calcula.**

- **Margen neto %:** Lo que queda de cada sol vendido después de la comisión, el costo estimado y el costo operativo.

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPedidos[venta_bruta]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[comision]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_estimado]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `fPedidos[costo_operativo]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 2 |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCalendario[anio_mes]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| [Margen neto %] | Medida | Ya la creaste en PAG-01 · Elemento 2 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Margen neto %] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Margen neto %]` (PAG-01 · Elemento 2).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 2).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Margen neto %].
5. En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.
6. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
7. Mismo eje horizontal que el visual 3: dos gráficos alineados en lugar de uno con dos ejes.

**Valor esperado.** ago 25: 14.0 % → oct 26: 8.0 %.

### Elemento 5 · Gráfico de líneas: Precio promedio mensual del pollo vivo

**Qué muestra.** El precio se mantiene cerca de S/ 6.10 hasta junio y de S/ 6.90 desde agosto.

**Cómo se calcula.**

- **Precio promedio del pollo vivo:** Promedio del precio diario por kilogramo (con el último precio publicado en los días sin precio).

**Tablas y columnas.**

| Campo | Qué es | De dónde sale |
|---|---|---|
| `fPrecioInsumo[precio_kg]` | Columna del modelo | Viene del ETL (guía de ETL, PAS-10 a PAS-14) |
| `dCalendario[mes_anio]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| `dCalendario[anio_mes]` | Columna calculada | Ya la creaste en PAG-01 · Elemento 7 |
| [Precio promedio del pollo vivo] | Medida | Ya la creaste en PAG-01 · Elemento 6 |

| Dónde va | Campo |
|---|---|
| Eje X / filas | dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]) |
| Valores (eje Y) | [Precio promedio del pollo vivo] |

**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: `[Precio promedio del pollo vivo]` (PAG-01 · Elemento 6).

**Cómo armarlo en Power BI.**

1. En el panel Visualizaciones elige **Gráfico de líneas** y colócalo en la posición indicada en el HTML de referencia (visual 3).
2. Arrastra a **Eje X** dCalendario[mes_anio] (ordenada por dCalendario[anio_mes]).
3. Si los valores salen en orden alfabético, selecciona `dCalendario[mes_anio]` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `anio_mes`.
4. Arrastra a **Eje Y** [Precio promedio del pollo vivo].
5. En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.
6. Mismo eje horizontal que el visual 2.

**Valor esperado.** ago 25: S/ 6.06 → oct 26: S/ 6.82.

