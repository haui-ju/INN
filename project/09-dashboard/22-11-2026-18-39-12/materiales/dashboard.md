# Dashboard: páginas, cuadros y columnas

Cada página es una sección y cada cuadro una subsección. **X** = eje horizontal (o filas), **Y** = valor, **Leyenda** = series. Las medidas entre corchetes están al final.

## PAG-01. Resumen del negocio

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dCanal[canal]

### Tarjetas de KPI

- KPI-03 Margen neto global: `[Margen neto %]` y su meta.
- KPI-02 Margen de contribución por canal y producto: `[Margen de contribución %]` y su meta.
- KPI-01 Calidad de datos del ETL: `[% Registros válidos]` y su meta.
- KPI-04 Porcentaje de merma por turno: `[% Merma]` y su meta.
- KPI-06 Precio pollo vivo por kilogramo: `[Precio pollo vivo]` y su meta.

### 1. Margen neto mensual contra la meta (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Margen neto %]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px, etiqueta de datos solo en el último punto; la meta va como línea constante punteada (panel Analytics).

### 2. Ventas mensuales por canal (apiladas)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Venta bruta]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Columnas apiladas; orden de la leyenda: Salón, Para llevar, WhatsApp, Rappi y PedidosYa.

### 3. KPI del dashboard contra su meta (tabla)

- **X:** `dKpi[kpi]`
- **Y:** [Margen neto %], [Margen de contribución %], [% Registros válidos], [% Merma], [Error del pronóstico %], [Precio pollo vivo], [% KPI con meta]
- **Filtro del cuadro:** dCalendario[mes_anio] = último mes del periodo
- **Formato:** Tabla con una fila por KPI; el estado se escribe con texto (Cumple, No cumple, Sin meta) y un icono, no solo con color.

## PAG-02. Rentabilidad por canal y producto

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dProducto[categoria]

### Tarjetas de KPI

- KPI-02 Margen de contribución por canal y producto: `[Margen de contribución %]` y su meta.

### 1. Margen de contribución por canal (barras)

- **X:** `dCanal[canal]`
- **Y:** [Margen de contribución %]
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Barras horizontales ordenadas de mayor a menor margen.

### 2. Margen de contribución por canal y producto (matriz)

- **X:** `dProducto[producto]`
- **Y:** [Margen de contribución %]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Matriz con formato condicional de color de fondo (escala de un solo color).

### 3. Participación de las ventas por canal (apiladas100)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Participación de ventas %]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Columnas apiladas al 100 %.

### 4. Comisión pagada por mes (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Comisión pagada]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px con etiqueta en el último punto.

## PAG-03. Producción y merma por turno

Usuario: Jefe de cocina · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dTurno[turno]

### Tarjetas de KPI

- KPI-04 Porcentaje de merma por turno: `[% Merma]` y su meta.
- KPI-05 Precisión del pronóstico de demanda: `[Error del pronóstico %]` y su meta.

### 1. Merma por turno contra la meta (columnas)

- **X:** `dTurno[turno]`
- **Y:** [% Merma]
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas con la meta como línea constante.

### 2. Merma por día de la semana (columnas)

- **X:** `dCalendario[dia_semana] (ordenada de lunes a domingo)`
- **Y:** [% Merma]
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas con la meta como línea constante.

### 3. Preparados y vendidos (columnas)

- **X:** `dCalendario[dia_semana] (ordenada de lunes a domingo)`
- **Y:** [Pollos preparados], [Pollos vendidos]
- **Leyenda:** Medidas en la leyenda
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas agrupadas con dos medidas.

### 4. Vendidos contra pronóstico de referencia (últimos 28 días) (linea)

- **X:** `dCalendario[fecha]`
- **Y:** [Pollos vendidos], [Pronóstico de referencia]
- **Leyenda:** Medidas en la leyenda
- **Filtro del cuadro:** dCalendario[fecha]: últimos 28 días
- **Formato:** Línea con dos series; el pronóstico va punteado.

## PAG-04. Precio del pollo vivo y margen

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes]

### Tarjetas de KPI

- KPI-06 Precio pollo vivo por kilogramo: `[Precio pollo vivo]` y su meta.

### 1. Precio diario del pollo vivo por kilogramo (linea)

- **X:** `dCalendario[fecha]`
- **Y:** [Precio pollo vivo]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px; los días con fPrecioInsumo[valor_imputado] = 1 se marcan con un punto.

### 2. Margen neto mensual (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Margen neto %]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Mismo eje horizontal que el visual 3: dos gráficos alineados en lugar de uno con dos ejes.

### 3. Precio promedio mensual del pollo vivo (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Precio pollo vivo]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Mismo eje horizontal que el visual 2.

## Medidas

**MED-01 Venta bruta**

```dax
SUM ( fPedidos[venta_bruta] )
```

**MED-02 Comisión pagada**

```dax
SUM ( fPedidos[comision] )
```

**MED-03 Costo estimado**

```dax
SUM ( fPedidos[costo_estimado] )
```

**MED-04 Costo operativo**

```dax
SUM ( fPedidos[costo_operativo] )
```

**MED-05 Margen de contribución %**

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado], [Venta bruta] )
```

**MED-06 Margen neto %**

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado] - [Costo operativo], [Venta bruta] )
```

**MED-07 % Registros válidos**

```dax
DIVIDE ( SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] ) )
```

**MED-08 Pollos preparados**

```dax
SUM ( fProduccion[pollos_preparados] )
```

**MED-09 Pollos vendidos**

```dax
SUM ( fProduccion[pollos_vendidos] )
```

**MED-10 Pollos de merma**

```dax
SUM ( fProduccion[pollos_merma] )
```

**MED-11 % Merma**

```dax
DIVIDE ( [Pollos de merma], [Pollos preparados] )
```

**MED-12 Precio pollo vivo**

```dax
AVERAGE ( fPrecioInsumo[precio_kg] )
```

**MED-13 Pronóstico de referencia**

```dax
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

**MED-14 Error del pronóstico %**

```dax
AVERAGEX (
    CROSSJOIN ( VALUES ( dCalendario[fecha] ), VALUES ( dTurno[turno] ) ),
    IF ( NOT ISBLANK ( [Pronóstico de referencia] ) && [Pollos vendidos] > 0,
        DIVIDE ( ABS ( [Pollos vendidos] - [Pronóstico de referencia] ), [Pollos vendidos] ) )
)
```

**MED-15 Participación de ventas %**

```dax
DIVIDE ( [Venta bruta], CALCULATE ( [Venta bruta], ALL ( dCanal[canal] ) ) )
```

**MED-16 % KPI con meta**

```dax
DIVIDE ( CALCULATE ( COUNTROWS ( dKpi ), dKpi[tiene_meta] = TRUE () ), COUNTROWS ( dKpi ) )
```

**MED-17 Meta del KPI**

```dax
AVERAGE ( fMetaKpi[meta] )
```
