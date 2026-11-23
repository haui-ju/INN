# Anexo C: Medidas y cálculos del dashboard

El dashboard usa 35 medidas: las base, que suman o promedian un campo de los hechos; las de KPI, que se apoyan en ellas; y las de texto y color, que escriben la meta y el estado de cada tarjeta y de la tabla de KPI. Se escribieron y probaron en Power BI.

Tabla 1: Medidas del dashboard

| Código | Medida | Tipo | KPI | Tablas y campos |
|---|---|---|---|---|
| MED-01 | Venta bruta | Medida |  | fPedidos |
| MED-02 | Comisión pagada | Medida |  | fPedidos |
| MED-03 | Costo estimado | Medida |  | fPedidos |
| MED-04 | Costo operativo | Medida |  | fPedidos |
| MED-05 | Margen de contribución % | Medida | KPI-02 | fPedidos |
| MED-06 | Margen neto % | Medida | KPI-03 | fPedidos |
| MED-07 | % Registros válidos | Medida | KPI-01 | fPedidos |
| MED-08 | Pollos preparados | Medida |  | fProduccion |
| MED-09 | Pollos vendidos | Medida |  | fProduccion |
| MED-10 | Pollos de merma | Medida |  | fProduccion |
| MED-11 | % Merma | Medida | KPI-04 | fProduccion |
| MED-12 | Precio pollo vivo | Medida | KPI-06 | fPrecioInsumo |
| MED-13 | Pronóstico de referencia | Medida |  | fProduccion; dCalendario; dTurno |
| MED-14 | Error del pronóstico % | Medida | KPI-05 | fProduccion; dCalendario; dTurno |
| MED-15 | Participación de ventas % | Medida |  | fPedidos; dCanal |
| MED-16 | % KPI con meta | Medida | KPI-07 | dKpi |
| MED-17 | Meta del KPI | Medida |  | fMetaKpi; dKpi |
| MED-18 | Mes de referencia | Medida |  | dCalendario |
| MED-19 | Meta texto KPI-03 | Medida | KPI-03 | fMetaKpi; dKpi; dCalendario |
| MED-20 | Estado KPI-03 | Medida | KPI-03 | fPedidos; fMetaKpi; dKpi |
| MED-21 | Color estado KPI-03 | Medida | KPI-03 | fPedidos; fMetaKpi; dKpi |
| MED-22 | Meta texto KPI-01 | Medida | KPI-01 | fMetaKpi; dKpi; dCalendario |
| MED-23 | Estado KPI-01 | Medida | KPI-01 | fPedidos; fMetaKpi; dKpi |
| MED-24 | Color estado KPI-01 | Medida | KPI-01 | fPedidos; fMetaKpi; dKpi |
| MED-25 | Meta texto KPI-04 | Medida | KPI-04 | fMetaKpi; dKpi; dCalendario |
| MED-26 | Estado KPI-04 | Medida | KPI-04 | fProduccion; fMetaKpi; dKpi |
| MED-27 | Color estado KPI-04 | Medida | KPI-04 | fProduccion; fMetaKpi; dKpi |
| MED-28 | Meta texto KPI-02 | Medida | KPI-02 | fMetaKpi; dKpi; dCalendario |
| MED-29 | Estado KPI-02 | Medida | KPI-02 | fPedidos; fMetaKpi; dKpi |
| MED-30 | Color estado KPI-02 | Medida | KPI-02 | fPedidos; fMetaKpi; dKpi |
| MED-31 | Valor numérico del KPI | Medida |  | dKpi; fMetaKpi; fPedidos; fProduccion; fPrecioInsumo |
| MED-32 | Valor del KPI | Medida |  | dKpi; fMetaKpi; fPedidos; fProduccion; fPrecioInsumo |
| MED-33 | Meta del KPI (texto) | Medida |  | dKpi; fMetaKpi; fPedidos; fProduccion; fPrecioInsumo |
| MED-34 | Estado del KPI | Medida |  | dKpi; fMetaKpi; fPedidos; fProduccion; fPrecioInsumo |
| MED-35 | Color del estado | Medida |  | dKpi; fMetaKpi; fPedidos; fProduccion; fPrecioInsumo |

### MED-01. Venta bruta

```dax
SUM ( fPedidos[venta_bruta] )
```

### MED-02. Comisión pagada

```dax
SUM ( fPedidos[comision] )
```

### MED-03. Costo estimado

```dax
SUM ( fPedidos[costo_estimado] )
```

### MED-04. Costo operativo

```dax
SUM ( fPedidos[costo_operativo] )
```

### MED-05. Margen de contribución %

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado], [Venta bruta] )
```

### MED-06. Margen neto %

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado] - [Costo operativo], [Venta bruta] )
```

### MED-07. % Registros válidos

```dax
DIVIDE ( SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] ) )
```

### MED-08. Pollos preparados

```dax
SUM ( fProduccion[pollos_preparados] )
```

### MED-09. Pollos vendidos

```dax
SUM ( fProduccion[pollos_vendidos] )
```

### MED-10. Pollos de merma

```dax
SUM ( fProduccion[pollos_merma] )
```

### MED-11. % Merma

```dax
DIVIDE ( [Pollos de merma], [Pollos preparados] )
```

### MED-12. Precio pollo vivo

```dax
AVERAGE ( fPrecioInsumo[precio_kg] )
```

### MED-13. Pronóstico de referencia

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

### MED-14. Error del pronóstico %

```dax
AVERAGEX (
    CROSSJOIN ( VALUES ( dCalendario[fecha] ), VALUES ( dTurno[turno] ) ),
    IF ( NOT ISBLANK ( [Pronóstico de referencia] ) && [Pollos vendidos] > 0,
        DIVIDE ( ABS ( [Pollos vendidos] - [Pronóstico de referencia] ), [Pollos vendidos] ) )
)
```

### MED-15. Participación de ventas %

```dax
DIVIDE ( [Venta bruta], CALCULATE ( [Venta bruta], ALL ( dCanal[canal] ) ) )
```

### MED-16. % KPI con meta

```dax
DIVIDE ( CALCULATE ( COUNTROWS ( dKpi ), dKpi[tiene_meta] = TRUE () ), COUNTROWS ( dKpi ) )
```

### MED-17. Meta del KPI

```dax
AVERAGE ( fMetaKpi[meta] )
```

### MED-18. Mes de referencia

```dax
VAR f = MAX ( dCalendario[fecha] )
RETURN
    SWITCH (
        MONTH ( f ),
        1, "ene", 2, "feb", 3, "mar", 4, "abr", 5, "may", 6, "jun",
        7, "jul", 8, "ago", 9, "sep", 10, "oct", 11, "nov", 12, "dic"
    ) & " " & RIGHT ( YEAR ( f ), 2 )
```

### MED-19. Meta texto KPI-03

```dax
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 3 )
RETURN
    "Meta: " & IF ( ISBLANK ( meta ), "Pendiente", FORMAT ( meta, "0" ) & " % o más" ) & " · " & [Mes de referencia]
```

### MED-20. Estado KPI-03

```dax
VAR valor = [Margen neto %]
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 3 ) / 100
RETURN
    IF ( ISBLANK ( meta ), "– Sin meta", IF ( valor >= meta, "✔ Cumple", "✖ No cumple" ) )
```

### MED-21. Color estado KPI-03

```dax
SWITCH ( LEFT ( [Estado KPI-03], 1 ), "✔", "#0F7B3F", "✖", "#B3261E", "#6B7280" )
```

### MED-22. Meta texto KPI-01

```dax
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 1 )
RETURN
    "Meta: " & IF ( ISBLANK ( meta ), "Pendiente", FORMAT ( meta, "0" ) & " % o más" ) & " · " & [Mes de referencia]
```

### MED-23. Estado KPI-01

```dax
VAR valor = [% Registros válidos]
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 1 ) / 100
RETURN
    IF ( ISBLANK ( meta ), "– Sin meta", IF ( valor >= meta, "✔ Cumple", "✖ No cumple" ) )
```

### MED-24. Color estado KPI-01

```dax
SWITCH ( LEFT ( [Estado KPI-01], 1 ), "✔", "#0F7B3F", "✖", "#B3261E", "#6B7280" )
```

### MED-25. Meta texto KPI-04

```dax
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 4 )
RETURN
    "Meta: " & IF ( ISBLANK ( meta ), "Pendiente", FORMAT ( meta, "0" ) & " % o menos" ) & " · " & [Mes de referencia]
```

### MED-26. Estado KPI-04

```dax
VAR valor = [% Merma]
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 4 ) / 100
RETURN
    IF ( ISBLANK ( meta ), "– Sin meta", IF ( valor <= meta, "✔ Cumple", "✖ No cumple" ) )
```

### MED-27. Color estado KPI-04

```dax
SWITCH ( LEFT ( [Estado KPI-04], 1 ), "✔", "#0F7B3F", "✖", "#B3261E", "#6B7280" )
```

### MED-28. Meta texto KPI-02

```dax
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 2 )
RETURN
    "Meta: " & IF ( ISBLANK ( meta ), "Pendiente", FORMAT ( meta, "0" ) & " % o más" ) & " · " & [Mes de referencia]
```

### MED-29. Estado KPI-02

```dax
VAR valor = [Margen de contribución %]
VAR meta = CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = 2 ) / 100
RETURN
    IF ( ISBLANK ( meta ), "– Sin meta", IF ( valor >= meta, "✔ Cumple", "✖ No cumple" ) )
```

### MED-30. Color estado KPI-02

```dax
SWITCH ( LEFT ( [Estado KPI-02], 1 ), "✔", "#0F7B3F", "✖", "#B3261E", "#6B7280" )
```

### MED-31. Valor numérico del KPI

```dax
SWITCH (
    SELECTEDVALUE ( dKpi[kpi_key] ),
    1, [% Registros válidos],
    2, [Margen de contribución %],
    3, [Margen neto %],
    4, [% Merma],
    5, [Error del pronóstico %],
    6, [Precio pollo vivo],
    7, CALCULATE ( [% KPI con meta], ALL ( dKpi ) )
)
```

### MED-32. Valor del KPI

```dax
VAR v = [Valor numérico del KPI]
RETURN
    IF ( SELECTEDVALUE ( dKpi[kpi_key] ) = 6, "S/ " & FORMAT ( v, "0.00" ), FORMAT ( v, "0.0 %" ) )
```

### MED-33. Meta del KPI (texto)

```dax
VAR k = SELECTEDVALUE ( dKpi[kpi_key] )
VAR meta = AVERAGE ( fMetaKpi[meta] )
RETURN
    IF ( ISBLANK ( meta ), "Pendiente", FORMAT ( meta, "0" ) & " % " & IF ( k IN { 4, 5 }, "o menos", "o más" ) )
```

### MED-34. Estado del KPI

```dax
VAR k = SELECTEDVALUE ( dKpi[kpi_key] )
VAR valor = [Valor numérico del KPI]
VAR meta = AVERAGE ( fMetaKpi[meta] ) / 100
RETURN
    IF (
        ISBLANK ( meta ), "– Sin meta",
        IF ( IF ( k IN { 4, 5 }, valor <= meta, valor >= meta ), "✔ Cumple", "✖ No cumple" )
    )
```

### MED-35. Color del estado

```dax
SWITCH ( LEFT ( [Estado del KPI], 1 ), "✔", "#0F7B3F", "✖", "#B3261E", "#6B7280" )
```
