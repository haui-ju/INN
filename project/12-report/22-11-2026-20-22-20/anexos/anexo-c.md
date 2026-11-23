# Anexo C: Medidas y cálculos del dashboard

El dashboard usa 17 medidas: las base, que suman o promedian un campo de los hechos, y las de KPI, que se apoyan en ellas. Se escribieron y probaron en Power BI.

Tabla 35: Medidas del dashboard

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
