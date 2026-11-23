# Anexo A: Diccionario de datos y calidad de datos

Este anexo lista los campos de las seis fuentes y de los dos archivos de apoyo, el origen de cada campo del modelo y el resultado de cada regla de calidad.

Tabla 32: Diccionario de los campos de entrada

| Fuente | Campo | Tipo | Regla de calidad | Destino |
|---|---|---|---|---|
| FUE-01 | ticket_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-01 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-01 | hora | texto | REG-05 | fPedidos.turno_key |
| FUE-01 | turno | texto | REG-05 | dTurno.turno |
| FUE-01 | canal | texto | — | dCanal.canal |
| FUE-01 | producto | texto | REG-02 | dProducto.producto |
| FUE-01 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-01 | precio_unitario | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-01 | descuento | decimal | REG-05 | fPedidos.venta_bruta |
| FUE-01 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-02 | pedido_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-02 | fecha_hora | fecha | REG-01 | dCalendario.fecha |
| FUE-02 | producto | texto | REG-02 | dProducto.producto |
| FUE-02 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-02 | monto | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-02 | comision | decimal | — | fPedidos.comision |
| FUE-02 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-03 | nro_pedido | texto | REG-03 | fPedidos.registro_valido |
| FUE-03 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-03 | item | texto | REG-02 | dProducto.producto |
| FUE-03 | cant | entero | REG-04 | fPedidos.cantidad |
| FUE-03 | total | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-03 | comision_pct | decimal | — | fPedidos.comision |
| FUE-03 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-04 | pedido | texto | REG-03 | fPedidos.registro_valido |
| FUE-04 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-04 | telefono | texto | — | — |
| FUE-04 | producto | texto | REG-02 | dProducto.producto |
| FUE-04 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-04 | monto | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-04 | tipo_entrega | texto | — | dCanal.canal |
| FUE-05 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-05 | turno | texto | REG-03 | dTurno.turno |
| FUE-05 | pollos_preparados | entero | REG-04 | fProduccion.pollos_preparados |
| FUE-05 | pollos_vendidos | entero | REG-04 | fProduccion.pollos_vendidos |
| FUE-05 | pollos_merma | entero | — | fProduccion.pollos_merma |
| FUE-05 | responsable | texto | REG-05 | — |
| FUE-06 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-06 | precio_kg | decimal | REG-06 | fPrecioInsumo.precio_kg |
| Apoyo: catálogo de productos | producto | texto | REG-02 | dProducto.producto |
| Apoyo: catálogo de productos | categoria | texto | — | dProducto.categoria |
| Apoyo: catálogo de productos | precio_lista | decimal | — | — |
| Apoyo: catálogo de productos | pollos_equivalentes | decimal | — | fPedidos.pollos_equivalentes |
| Apoyo: catálogo de productos | kg_pollo_vivo | decimal | — | fPedidos.costo_estimado |
| Apoyo: catálogo de productos | costo_otros | decimal | — | fPedidos.costo_estimado |
| Apoyo: catálogo de productos | alias | texto | REG-02 | dProducto.producto |
| Apoyo: costos operativos | mes | texto | — | dCalendario.mes |
| Apoyo: costos operativos | planilla | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | alquiler | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | servicios | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | otros | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | total | decimal | — | fPedidos.costo_operativo |

Tabla 33: Origen de los campos del modelo

| Tabla | Campo | Origen |
|---|---|---|
| fPedidos | fecha_key; producto_key; canal_key; turno_key | Cálculo: clave sustituta que se busca en cada dimensión con la fecha, el producto homologado, el canal y el turno de la fuente |
| fPedidos | cantidad | FUE-01.cantidad; FUE-02.cantidad; FUE-03.cant; FUE-04.cantidad |
| fPedidos | venta_bruta | FUE-01.precio_unitario; FUE-01.descuento; FUE-02.monto; FUE-03.total; FUE-04.monto |
| fPedidos | comision | FUE-02.comision; FUE-03.comision_pct; Cálculo: total por el porcentaje de comisión entre cien en PedidosYa |
| fPedidos | costo_estimado | apoyo-catalogo-productos.kg_pollo_vivo; apoyo-catalogo-productos.costo_otros; FUE-06.precio_kg; Cálculo: cantidad por los kilos de pollo vivo por el precio del día más otros costos |
| fPedidos | costo_operativo | apoyo-costos-operativos.total; Cálculo: total del mes repartido en proporción a la venta del mes |
| fPedidos | pollos_equivalentes | apoyo-catalogo-productos.pollos_equivalentes |
| fPedidos | registro_valido; registro_total | Cálculo: uno si la línea no es duplicada ni inválida y uno por cada fila leída |
| fProduccion | fecha_key; turno_key | Cálculo: clave sustituta que se busca en dCalendario y dTurno |
| fProduccion | pollos_preparados; pollos_vendidos; pollos_merma | FUE-05.pollos_preparados; FUE-05.pollos_vendidos; FUE-05.pollos_merma |
| fPrecioInsumo | fecha_key | Cálculo: clave sustituta que se busca en dCalendario |
| fPrecioInsumo | precio_kg | FUE-06.precio_kg; Cálculo: último precio publicado en los días sin precio |
| fPrecioInsumo | valor_imputado | Cálculo: uno si el día no tenía precio |
| fMetaKpi | kpi_key; fecha_key | Cálculo: clave de dKpi y primer día de cada mes |
| fMetaKpi | meta; valor_real | Cálculo: metas de la sección 2.5 y medidas del dashboard |
| dCalendario | fecha_key; fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Cálculo: una fila por cada día del periodo y lista de feriados |
| dProducto | producto_key; producto; categoria | apoyo-catalogo-productos.producto; apoyo-catalogo-productos.categoria; Cálculo: número de fila como clave |
| dCanal | canal_key; canal; tipo_canal; comision_pct | FUE-01.canal; Cálculo: lista de canales con su tipo y su comisión de 30 % en Rappi y 25 % en PedidosYa |
| dTurno | turno_key; turno; hora_inicio; hora_fin | FUE-05.turno; Cálculo: horario de cada turno |
| dKpi | kpi_key; kpi; objetivo; tiene_meta; frecuencia | Cálculo: KPI de la sección 2.5 |

Tabla 34: Resultado de las reglas de calidad

| Código | Filas antes | Filas después | Diferencia |
|---|---|---|---|
| REG-01 | 91297 | 91297 | 0 |
| REG-02 | 91297 | 91297 | 0 |
| REG-03 | 91297 | 90623 | -674 |
| REG-04 | 90623 | 89888 | -735 |
| REG-05 | 89888 | 89888 | 0 |
| REG-06 | 437 | 457 | 20 |
