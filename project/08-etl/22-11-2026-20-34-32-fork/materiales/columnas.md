# Columnas por crear en Power BI

Carga los CSV de `data/limpio/` con estos nombres de tabla: `fPedidos` (pedidos.csv), `fProduccion` (produccion.csv), `fPrecioInsumo` (precios-pollo.csv), `Catalogo` (catalogo-productos.csv), `Costos` (costos-operativos.csv).
Los CSV ya vienen con los nombres listos (`comision_origen` y `monto_origen` en `fPedidos`). Solo pon el tipo **Fecha** a la columna `fecha` de `fPedidos`, `fProduccion` y `fPrecioInsumo`. Todas las columnas de abajo son **columna calculada (DAX)**.

## dCalendario (tabla nueva)

```dax
dCalendario = CALENDAR ( DATE ( 2025, 8, 1 ), DATE ( 2026, 10, 31 ) )
```
Renombra `[Date]` a `fecha` y agrega:

| Columna | Fórmula |
|---|---|
| fecha_key | `YEAR([fecha])*10000 + MONTH([fecha])*100 + DAY([fecha])` |
| anio | `YEAR([fecha])` |
| mes | `MONTH([fecha])` |
| nombre_mes | `FORMAT([fecha], "mmmm", "es-PE")` |
| dia_semana | `FORMAT([fecha], "dddd", "es-PE")` (ordénala por `num_dia_semana`) |
| num_dia_semana | `WEEKDAY([fecha], 2)` |
| anio_mes | `[anio]*100 + [mes]` |
| mes_anio | `FORMAT([fecha], "mmm yy", "es-PE")` (ordénala por `anio_mes`) |
| es_feriado | `MONTH([fecha])*100 + DAY([fecha]) IN {101,501,629,728,729,830,1008,1101,1208,1225}` |

Marca la tabla como tabla de fechas con la columna `fecha`.

## Dimensiones (Entrar datos, o índice desde 1 en Power Query)

| Tabla | Columnas | Filas |
|---|---|---|
| dProducto | producto_key, producto, categoria | Del `Catalogo`: deja `producto` y `categoria` y agrega un índice desde 1 como `producto_key`. |
| dCanal | canal_key, canal, tipo_canal, comision_pct | 1 Salón, Propio, 0 · 2 Para llevar, Propio, 0 · 3 WhatsApp, Propio, 0 · 4 Rappi, Aplicación, 30 · 5 PedidosYa, Aplicación, 25 |
| dTurno | turno_key, turno, hora_inicio, hora_fin | 1 Mañana 11:00 15:00 · 2 Tarde 15:00 19:00 · 3 Noche 19:00 23:00 |
| dKpi | kpi_key, kpi, objetivo, tiene_meta, frecuencia | Los 7 KPI de la sección 2.5. `tiene_meta` es falso para KPI-02 y KPI-06. |

## fPedidos

Crea en este orden:

| Columna | Fórmula |
|---|---|
| registro_total | `1` |
| registro_valido | `IF([es_duplicado]=0 && [es_invalido]=0, 1, 0)` |
| venta_bruta | `IF([registro_valido]=0, 0, IF([fuente]="FUE-01", [cantidad]*[precio_unitario]-[descuento], [monto_origen]))` |
| comision | `IF([registro_valido]=0, 0, SWITCH([canal], "Rappi", [comision_origen], "PedidosYa", [monto_origen]*[comision_pct]/100, 0))` |
| costo_estimado | `IF([registro_valido]=0, 0, [cantidad] * ( LOOKUPVALUE(Catalogo[kg_pollo_vivo], Catalogo[producto], [producto]) * LOOKUPVALUE(fPrecioInsumo[precio_kg], fPrecioInsumo[fecha], [fecha]) + LOOKUPVALUE(Catalogo[costo_otros], Catalogo[producto], [producto]) ))` |
| mes_texto (auxiliar) | `FORMAT([fecha], "yyyy-MM")` |
| costo_operativo | `DIVIDE( LOOKUPVALUE(Costos[total], Costos[mes], [mes_texto]) * [venta_bruta], CALCULATE(SUM(fPedidos[venta_bruta]), ALLEXCEPT(fPedidos, fPedidos[mes_texto])) )` |
| pollos_equivalentes | `IF([registro_valido]=0, 0, [cantidad] * LOOKUPVALUE(Catalogo[pollos_equivalentes], Catalogo[producto], [producto]))` |
| fecha_key | `YEAR([fecha])*10000 + MONTH([fecha])*100 + DAY([fecha])` |
| producto_key | `LOOKUPVALUE(dProducto[producto_key], dProducto[producto], [producto])` |
| canal_key | `LOOKUPVALUE(dCanal[canal_key], dCanal[canal], [canal])` |
| turno_key | `LOOKUPVALUE(dTurno[turno_key], dTurno[turno], [turno])` |

## fProduccion

| Columna | Fórmula |
|---|---|
| fecha_key | `YEAR([fecha])*10000 + MONTH([fecha])*100 + DAY([fecha])` |
| turno_key | `LOOKUPVALUE(dTurno[turno_key], dTurno[turno], [turno])` |

## fPrecioInsumo

| Columna | Fórmula |
|---|---|
| fecha_key | `YEAR([fecha])*10000 + MONTH([fecha])*100 + DAY([fecha])` |

## fMetaKpi (Entrar datos)

Una fila por KPI y mes (7 × 15 = 105): `kpi_key`, `fecha_key` (primer día del mes), `meta` (la de 2.5; vacía si es Pendiente) y `valor_real` (puede quedar vacía).

## Relaciones (varios a uno, un solo sentido)

`fPedidos` → dCalendario (fecha_key), dProducto (producto_key), dCanal (canal_key), dTurno (turno_key) · `fProduccion` → dCalendario, dTurno · `fPrecioInsumo` → dCalendario · `fMetaKpi` → dKpi (kpi_key), dCalendario (fecha_key).
