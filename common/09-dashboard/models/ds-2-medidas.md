# Plantilla: Medidas y cálculos del dashboard (`anexos/C.md`)

| | |
|---|---|
| **Entregable** | `anexos/C.md` (anexo C del informe) |
| **Punto** | Anexo C: Medidas y cálculos del dashboard (medidas DAX y columnas calculadas) |
| **Códigos** | `MED-nn`; cita `KPI-nn` del modelo |
| **Entradas** | `modelo.json` (KPI, fórmula, medida propuesta y campos de origen), la propuesta de `dashboard_dax.py` y las medidas finales del equipo |
| **Salida** | cada medida con el código DAX que el equipo ejecutó en Power BI |

## Instrucciones para el agente
1. La primera línea es `# Anexo C: Medidas y cálculos del dashboard`.
2. **Propón antes de escribir.** `python3 .claude/skills/_shared/dashboard_dax.py <modelo.json>` imprime una medida base por cada campo de un hecho que usan los KPI y una medida por KPI. Es un borrador: lo que dice `¡revisar!` no se pudo relacionar con el modelo y lo completa el equipo. Entrégalo al equipo y **di que lo prueba en Power BI**; no afirmes que funciona.
3. **El anexo lleva la medida final del equipo**, la que se ejecutó, aunque difiera de tu propuesta. No dejes marcas `revisar`.
4. Una tabla `Código | Medida | Tipo | KPI | Tablas y campos`: una fila por medida (`Tipo`: `Medida` o `Columna calculada`). La columna KPI lleva el `KPI-nn` cuya medida propuesta es esa, o queda vacía en las medidas base.
5. Después, para cada fila, un encabezado `### MED-nn. Nombre` y el DAX en un bloque ```` ```dax ````. El nombre es el que se cita entre corchetes en otras medidas.
6. El DAX usa **solo** tablas y campos de `modelo.json` (`fPedidos[venta_bruta]`) y medidas definidas en este anexo (`[Suma de venta_bruta]`). Cada KPI tiene su medida con el nombre de la «Medida propuesta» de 2.5.
7. La tabla lleva antes una línea `Tabla N: título`.

## Formato

````markdown
# Anexo C: Medidas y cálculos del dashboard

[Frase: cuántas medidas hay y que se construyeron en Power BI.]

Tabla 1: Medidas del dashboard

| Código | Medida | Tipo | KPI | Tablas y campos |
|---|---|---|---|---|
| MED-01 | [nombre] | Medida | | [tabla[campo]] |
| MED-02 | [Medida propuesta del KPI] | Medida | KPI-01 | [tabla[campo]] |

### MED-01. [nombre]

```dax
[DAX final]
```
````

## Ejemplo

````markdown
# Anexo C: Medidas y cálculos del dashboard

El dashboard usa doce medidas: siete base, una por cada campo de los hechos que alimenta un KPI, y cinco medidas de KPI que se apoyan en ellas. Se escribieron y probaron en Power BI.

Tabla 1: Medidas del dashboard

| Código | Medida | Tipo | KPI | Tablas y campos |
|---|---|---|---|---|
| MED-01 | Suma de registro_valido | Medida | | fPedidos[registro_valido] |
| MED-02 | Suma de venta_bruta | Medida | | fPedidos[venta_bruta] |
| MED-03 | Suma de comision | Medida | | fPedidos[comision] |
| MED-04 | Suma de costo_estimado | Medida | | fPedidos[costo_estimado] |
| MED-05 | Suma de pollos_merma | Medida | | fProduccion[pollos_merma] |
| MED-06 | Suma de pollos_preparados | Medida | | fProduccion[pollos_preparados] |
| MED-07 | Promedio de precio_kg | Medida | | fPrecioInsumo[precio_kg] |
| MED-08 | % Registros válidos | Medida | KPI-01 | fPedidos |
| MED-09 | Margen neto % | Medida | KPI-02 | fPedidos[venta_bruta]; fPedidos[comision]; fPedidos[costo_estimado] |
| MED-10 | % Merma | Medida | KPI-03 | fProduccion[pollos_merma]; fProduccion[pollos_preparados] |
| MED-11 | % Canal directo | Medida | KPI-04 | fPedidos[venta_bruta]; dCanal[tipo_canal] |
| MED-12 | Precio pollo vivo | Medida | KPI-05 | fPrecioInsumo[precio_kg] |

### MED-01. Suma de registro_valido

```dax
SUM(fPedidos[registro_valido])
```

### MED-02. Suma de venta_bruta

```dax
SUM(fPedidos[venta_bruta])
```

### MED-03. Suma de comision

```dax
SUM(fPedidos[comision])
```

### MED-04. Suma de costo_estimado

```dax
SUM(fPedidos[costo_estimado])
```

### MED-05. Suma de pollos_merma

```dax
SUM(fProduccion[pollos_merma])
```

### MED-06. Suma de pollos_preparados

```dax
SUM(fProduccion[pollos_preparados])
```

### MED-07. Promedio de precio_kg

```dax
AVERAGE(fPrecioInsumo[precio_kg])
```

### MED-08. % Registros válidos

```dax
DIVIDE([Suma de registro_valido], COUNTROWS(fPedidos))
```

### MED-09. Margen neto %

```dax
DIVIDE([Suma de venta_bruta] - [Suma de comision] - [Suma de costo_estimado], [Suma de venta_bruta])
```

### MED-10. % Merma

```dax
DIVIDE([Suma de pollos_merma], [Suma de pollos_preparados])
```

### MED-11. % Canal directo

```dax
DIVIDE(CALCULATE([Suma de venta_bruta], dCanal[tipo_canal] = "Propio"), [Suma de venta_bruta])
```

### MED-12. Precio pollo vivo

```dax
[Promedio de precio_kg]
```
````

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Cada KPI del modelo tiene su medida con el nombre de la «Medida propuesta» de 2.5.
- [ ] Todo `MED-nn` de la tabla tiene su encabezado y su bloque `dax`, y al revés.
- [ ] El DAX cita solo tablas y campos de `modelo.json` y medidas definidas en el anexo.
- [ ] Ninguna medida conserva una marca `revisar`.
- [ ] La tabla tiene su título `Tabla N: …`.
