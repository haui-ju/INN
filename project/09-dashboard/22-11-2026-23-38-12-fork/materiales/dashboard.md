# Dashboard: páginas, cuadros y columnas

Cada página es una sección y cada cuadro una subsección. **X** = eje horizontal (o filas), **Y** = valor, **Leyenda** = series. Las medidas entre corchetes están al final.

## PAG-01. Resumen del negocio

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dCanal[canal]

**Pregunta de negocio:** ¿gana el negocio lo que debería y qué indicadores están fuera de su meta? Es la página de entrada: resume el estado de todos los KPI y dirige al dueño a la página donde está la causa.

### Tarjetas de KPI

- KPI-03 Margen neto global: `[Margen neto %]` y su meta.
  - **Para qué sirve:** Dice cuánto de cada sol vendido queda como utilidad después de comisión, costo del pollo e insumos y costo operativo.
  - **Cómo se lee:** Valor del último mes (oct 26) frente a la meta de 12 %. Muestra 8,0 % con «No cumple»: faltan 4 puntos.
  - **Qué objetivo ayuda a cumplir:** OE-02 y OE-05: es el indicador del objetivo general (recuperar el margen neto).
- KPI-02 Margen de contribución por canal y producto: `[Margen de contribución %]` y su meta.
  - **Para qué sirve:** Dice cuánto deja cada venta después de la comisión y el costo del producto, antes del costo operativo.
  - **Cómo se lee:** Valor del último mes: 54,4 %. Aparece «Sin meta» porque la meta sigue pendiente en 2.5; no es un error.
  - **Qué objetivo ayuda a cumplir:** OE-02: confirma que el margen de canales y productos está medido.
- KPI-01 Calidad de datos del ETL: `[% Registros válidos]` y su meta.
  - **Para qué sirve:** Dice qué parte de los registros cargados pasó las reglas de calidad, es decir, cuánto se puede confiar en el resto del dashboard.
  - **Cómo se lee:** 98,3 % frente a la meta de 98 %: «Cumple». Si bajara de la meta, las demás cifras no serían confiables.
  - **Qué objetivo ayuda a cumplir:** OE-01: es el indicador del ETL (98 % o más).
- KPI-04 Porcentaje de merma por turno: `[% Merma]` y su meta.
  - **Para qué sirve:** Dice qué parte de los pollos preparados se pierde sin venderse.
  - **Cómo se lee:** 6,4 % frente a la meta de 3 % o menos: «No cumple». La causa se ve en la página 3, por turno y por día.
  - **Qué objetivo ayuda a cumplir:** OE-03: es el indicador de reducción de la merma (de 7 % a 3 % o menos).
- KPI-06 Precio pollo vivo por kilogramo: `[Precio pollo vivo]` y su meta.
  - **Para qué sirve:** Muestra el precio del insumo principal, el que más mueve el costo del producto.
  - **Cómo se lee:** S/ 6,82 por kg en oct 26. «Sin meta»: sirve para comparar contra meses anteriores. Su efecto en el margen se ve en la página 4.
  - **Qué objetivo ayuda a cumplir:** OE-04: da el valor del precio del insumo que se cruza con el margen.

### 1. Margen neto mensual contra la meta (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Margen neto %]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px, etiqueta de datos solo en el último punto; la meta va como línea constante punteada (panel Analytics).
- **Para qué sirve:** Dice si el negocio se acerca o se aleja del margen neto que quiere (12 %) mes a mes.
- **Cómo se lee:** Cada punto es el margen neto de un mes y la línea punteada es la meta. Baja de 14,0 % (ago 25) a 8,0 % (oct 26): cumple la meta hasta ene 26 (12,1 %) y desde feb 26 (11,1 %) queda por debajo con una brecha que crece. Una línea que se separa de la meta hacia abajo pide revisar las páginas 2 y 4.
- **Qué objetivo ayuda a cumplir:** OE-02 y OE-05: es el indicador central del objetivo general (recuperar el margen neto) y muestra la tendencia, no solo el valor del mes.

### 2. Ventas mensuales por canal (apiladas)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Venta bruta]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Columnas apiladas; orden de la leyenda: Salón, Para llevar, WhatsApp, Rappi y PedidosYa.
- **Para qué sirve:** Muestra cuánto vende cada canal y cómo cambia su peso en el tiempo.
- **Cómo se lee:** Cada columna es un mes y cada color un canal. Salón y Para llevar bajan (S/ 68 593 → S/ 60 633 y S/ 63 440 → S/ 54 272) mientras Rappi y PedidosYa suben (S/ 15 935 → S/ 43 733 y S/ 10 647 → S/ 32 602). La venta total crece, pero se mueve hacia los canales que cobran comisión.
- **Qué objetivo ayuda a cumplir:** OE-02: explica de dónde viene la caída del margen. OE-01: si un canal faltara o saliera con un salto raro, delataría un error de carga.

### 3. KPI del dashboard contra su meta (tabla)

- **X:** `dKpi[kpi]`
- **Y:** [Margen neto %], [Margen de contribución %], [% Registros válidos], [% Merma], [Error del pronóstico %], [Precio pollo vivo], [% KPI con meta]
- **Filtro del cuadro:** dCalendario[mes_anio] = último mes del periodo
- **Formato:** Tabla con una fila por KPI; el estado se escribe con texto (Cumple, No cumple, Sin meta) y un icono, no solo con color.
- **Para qué sirve:** Resume los 7 KPI en una sola tabla con su valor, su meta y su estado, para revisar el avance del proyecto.
- **Cómo se lee:** Una fila por KPI, con el valor de oct 26. Estado con texto e icono: ✔ Cumple (KPI-01), ✖ No cumple (KPI-03, KPI-04, KPI-05, KPI-07) y – Sin meta (KPI-02, KPI-06). KPI-07 en 71,4 % indica que 5 de 7 KPI tienen meta.
- **Qué objetivo ayuda a cumplir:** OE-05: es la prueba directa de «KPI con meta y semáforo». Los 5 KPI con meta se leen aquí; los 2 pendientes quedan a la vista para cerrarlos.

## PAG-02. Rentabilidad por canal y producto

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dProducto[categoria]

**Pregunta de negocio:** ¿qué canales y productos dejan margen después de la comisión? Sostiene la decisión de fijar precios diferenciados por canal.

### Tarjetas de KPI

- KPI-02 Margen de contribución por canal y producto: `[Margen de contribución %]` y su meta.
  - **Para qué sirve:** Mismo valor de la página 1, para que esta página se entienda sola al filtrar por año, mes o categoría.
  - **Cómo se lee:** Margen después de comisión y costo del producto: 54,4 % en oct 26, sin meta definida.
  - **Qué objetivo ayuda a cumplir:** OE-02: margen por canal y producto.

### 1. Margen de contribución por canal (barras)

- **Eje Y (categorías):** `dCanal[canal]`
- **Eje X (valores):** [Margen de contribución %]
- **Ojo:** en barras horizontales los ejes van al revés que en columnas; la medida va en Eje X, no en Eje Y.
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Barras horizontales ordenadas de mayor a menor margen.
- **Para qué sirve:** Compara qué canal deja más margen por cada sol vendido, ya descontada la comisión.
- **Cómo se lee:** Barras de mayor a menor: Para llevar 65,3 %, WhatsApp 65,1 %, Salón 64,7 %, PedidosYa 40,5 % y Rappi 35,5 %. Los canales propios rinden unos 25 puntos más que las aplicaciones.
- **Qué objetivo ayuda a cumplir:** OE-02: mide el margen de los 5 canales (100 % de los canales) y sustenta el precio diferenciado en apps.

### 2. Margen de contribución por canal y producto (matriz)

- **X:** `dProducto[producto]`
- **Y:** [Margen de contribución %]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Matriz con formato condicional de color de fondo (escala de un solo color).
- **Para qué sirve:** Baja el análisis al producto para ver qué platos aguantan la comisión y cuáles no.
- **Cómo se lee:** Filas = productos, columnas = canales; un fondo más oscuro es más margen. Va de 27,6 % (Parrilla familiar en Rappi) a 68,6 % (Adicional). Las parrillas son el punto débil en apps (27,6 % a 34,4 %); los adicionales y combos resisten mejor (38,6 % a 43,6 %).
- **Qué objetivo ayuda a cumplir:** OE-02: cubre los productos y canales del periodo y indica dónde subir el precio primero y qué promocionar.

### 3. Participación de las ventas por canal (apiladas100)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Participación de ventas %]
- **Leyenda:** `dCanal[canal]`
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Columnas apiladas al 100 %.
- **Para qué sirve:** Muestra cómo se reparte la venta entre canales sin el efecto del tamaño del mes.
- **Cómo se lee:** Cada columna suma 100 %. Salón pasa de 38,9 % a 27,9 %, Para llevar de 36,0 % a 25,0 %, Rappi de 9,0 % a 20,1 % y PedidosYa de 6,0 % a 15,0 %. WhatsApp sube de 10,0 % a 12,0 %.
- **Qué objetivo ayuda a cumplir:** OE-02: explica por qué baja el margen global (más peso en canales de margen bajo). Es la base para promover el delivery propio por WhatsApp.

### 4. Comisión pagada por mes (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Comisión pagada]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px con etiqueta en el último punto.
- **Para qué sirve:** Cuantifica en soles lo que se paga a Rappi y PedidosYa cada mes.
- **Cómo se lee:** Una línea ascendente indica que la comisión crece con el peso de las apps. El último punto muestra cuánto se pagó en oct 26.
- **Qué objetivo ayuda a cumplir:** OE-02: convierte la diferencia de margen en dinero. Ayuda a evaluar si un descuento propio, menor que la comisión, conviene.

## PAG-03. Producción y merma por turno

Usuario: Jefe de cocina · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes], dTurno[turno]

**Pregunta de negocio:** ¿cuánto pollo se prepara de más o de menos en cada turno y día? Sostiene la decisión de cuánto preparar y con qué personal.

### Tarjetas de KPI

- KPI-04 Porcentaje de merma por turno: `[% Merma]` y su meta.
  - **Para qué sirve:** Dice qué parte de los pollos preparados se pierde sin venderse.
  - **Cómo se lee:** 6,4 % frente a la meta de 3 % o menos: «No cumple». La causa se ve en la página 3, por turno y por día.
  - **Qué objetivo ayuda a cumplir:** OE-03: es el indicador de reducción de la merma (de 7 % a 3 % o menos).
- KPI-05 Precisión del pronóstico de demanda: `[Error del pronóstico %]` y su meta.
  - **Para qué sirve:** Dice qué tan lejos queda el pronóstico de lo que realmente se vende por día y turno.
  - **Cómo se lee:** 28,2 % frente a la meta de 15 % o menos: «No cumple». Menor error permite preparar la cantidad justa.
  - **Qué objetivo ayuda a cumplir:** OE-03: mide si el pronóstico sirve para reducir la merma.

### 1. Merma por turno contra la meta (columnas)

- **X:** `dTurno[turno]`
- **Y:** [% Merma]
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas con la meta como línea constante.
- **Para qué sirve:** Indica en qué turno se pierde más pollo y a qué distancia está de la meta de 3 %.
- **Cómo se lee:** Una columna por turno; la línea es la meta. Mañana 6,7 %, Tarde 8,3 % y Noche 6,6 %: los tres duplican la meta, y la tarde es la peor.
- **Qué objetivo ayuda a cumplir:** OE-03: es el indicador del objetivo (de 7 % a 3 % o menos). Dice dónde empezar a ajustar la cantidad preparada.

### 2. Merma por día de la semana (columnas)

- **X:** `dCalendario[dia_semana] (ordenada de lunes a domingo)`
- **Y:** [% Merma]
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas con la meta como línea constante.
- **Para qué sirve:** Detecta qué días de la semana concentran la merma.
- **Cómo se lee:** Una columna por día; la línea es la meta. Martes 11,5 % es el pico; lunes 8,3 %, miércoles 8,2 % y jueves 7,9 % siguen. Domingo 3,7 % es el único día cercano a la meta.
- **Qué objetivo ayuda a cumplir:** OE-03: permite fijar cuántos pollos preparar por día de la semana, no solo por turno.

### 3. Preparados y vendidos (columnas)

- **X:** `dCalendario[dia_semana] (ordenada de lunes a domingo)`
- **Y:** [Pollos preparados], [Pollos vendidos]
- **Leyenda:** Medidas en la leyenda
- **Filtro del cuadro:** Todo el periodo
- **Formato:** Columnas agrupadas con dos medidas.
- **Para qué sirve:** Muestra cuánto se prepara frente a cuánto se vende, para ver el exceso detrás de la merma.
- **Cómo se lee:** Dos columnas por día: la diferencia es el sobrante. En domingo se preparan 6 062 y se venden 5 835. Si la columna de preparados supera a la de vendidos por mucho, ese día se produce de más.
- **Qué objetivo ayuda a cumplir:** OE-03: traduce el porcentaje de merma en pollos concretos y apoya la decisión de producción.

### 4. Vendidos contra pronóstico de referencia (últimos 28 días) (linea)

- **X:** `dCalendario[fecha]`
- **Y:** [Pollos vendidos], [Pronóstico de referencia]
- **Leyenda:** Medidas en la leyenda
- **Filtro del cuadro:** dCalendario[fecha]: últimos 28 días
- **Formato:** Línea con dos series; el pronóstico va punteado.
- **Para qué sirve:** Compara lo vendido con el pronóstico simple de las últimas 4 semanas, para saber si anticipar la demanda es posible.
- **Cómo se lee:** Línea sólida = vendido; línea punteada = pronóstico. Cuando ambas se acercan, el pronóstico sirve para preparar; el 31/10 se vendieron 89 y el pronóstico decía 100. Se ven los últimos 28 días.
- **Qué objetivo ayuda a cumplir:** OE-03: es la evidencia de «pronosticar la demanda». Su error (28,2 %) está sobre la meta de 15 %: muestra que falta afinar el método.

## PAG-04. Precio del pollo vivo y margen

Usuario: Dueño · Filtros de la página: dCalendario[anio], dCalendario[nombre_mes]

**Pregunta de negocio:** ¿cómo se mueve el precio del pollo vivo y cómo afecta al margen? Sostiene la decisión de anticipar compras y ajustar precios.

### Tarjetas de KPI

- KPI-06 Precio pollo vivo por kilogramo: `[Precio pollo vivo]` y su meta.
  - **Para qué sirve:** Muestra el precio del insumo principal, el que más mueve el costo del producto.
  - **Cómo se lee:** S/ 6,82 por kg en oct 26. «Sin meta»: sirve para comparar contra meses anteriores. Su efecto en el margen se ve en la página 4.
  - **Qué objetivo ayuda a cumplir:** OE-04: da el valor del precio del insumo que se cruza con el margen.

### 1. Precio diario del pollo vivo por kilogramo (linea)

- **X:** `dCalendario[fecha]`
- **Y:** [Precio pollo vivo]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Línea de 2 px; los días con fPrecioInsumo[valor_imputado] = 1 se marcan con un punto.
- **Para qué sirve:** Vigila el precio del pollo vivo día a día para ver subidas y detectar días sin dato.
- **Cómo se lee:** Cada punto es el precio de un día; los puntos marcados son días sin precio publicado, completados con el último precio disponible. Va de S/ 6,14 (01/08/2025) a S/ 6,85 (31/10/2026), con un salto en jul 26 (S/ 6,90 el 14/07).
- **Qué objetivo ayuda a cumplir:** OE-04: cubre el 100 % de los días del periodo y permite anticipar compras.

### 2. Margen neto mensual (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Margen neto %]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Mismo eje horizontal que el visual 3: dos gráficos alineados en lugar de uno con dos ejes.
- **Para qué sirve:** Muestra el margen neto mensual para compararlo con el precio del insumo.
- **Cómo se lee:** Es la misma serie de la página 1. Baja de 14,0 % a 8,0 %. Se coloca encima del gráfico de precio con el mismo eje de meses para comparar sin doble eje.
- **Qué objetivo ayuda a cumplir:** OE-04: forma la mitad de la comparación margen contra precio. Apoya OE-02.

### 3. Precio promedio mensual del pollo vivo (linea)

- **X:** `dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])`
- **Y:** [Precio pollo vivo]
- **Filtro del cuadro:** Ninguno: se ve todo el periodo
- **Formato:** Mismo eje horizontal que el visual 2.
- **Para qué sirve:** Resume el precio del pollo vivo por mes para compararlo con el margen del mismo mes.
- **Cómo se lee:** Va de S/ 6,06 (ago 25) a S/ 6,82 (oct 26), plano hasta jun 26 y con subida desde jul 26. Se lee junto al gráfico 2: si el margen cae en meses de precio estable, la causa no es el insumo, sino el cambio de canales.
- **Qué objetivo ayuda a cumplir:** OE-04: cruza el insumo con el margen. Ayuda a decidir cuánto ajustar precios cuando el pollo sube.

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

- **Para qué sirve:** Muestra de un vistazo el último mes de cada KPI frente a su meta, con el estado escrito (Cumple, No cumple, Sin meta).
- **Cómo se lee:** El número grande es el valor del último mes (oct 26); debajo va la meta. «No cumple» en margen neto (8,0 % frente a 12 %) y en merma (6,4 % frente a 3 %) son las alertas. «Sin meta» no es un error: la meta sigue pendiente en 2.5.
- **Qué objetivo ayuda a cumplir:** OE-05 (KPI con meta y semáforo); además entrega el valor de OE-01 a OE-04 en una sola vista.

- **Para qué sirve:** Repite el margen de contribución para que la página se entienda sola al filtrar por año, mes o categoría.
- **Cómo se lee:** Es el margen después de comisión y costo del pollo y los insumos, sin costo operativo. En oct 26 es 54,4 %.
- **Qué objetivo ayuda a cumplir:** OE-02 (margen por canal y producto).

- **Para qué sirve:** Pone junto lo que se pierde (merma) y qué tan bien se anticipa la demanda (error del pronóstico).
- **Cómo se lee:** Merma 6,4 % frente a meta de 3 %; error del pronóstico 28,2 % frente a meta de 15 %. Con menor error se puede preparar mejor y la merma baja.
- **Qué objetivo ayuda a cumplir:** OE-03 (pronosticar la demanda para reducir la merma).

- **Para qué sirve:** Da el precio promedio del pollo vivo del mes, que es el principal costo del producto.
- **Cómo se lee:** S/ 6,82 por kg en oct 26. No tiene meta: se usa para comparar contra meses anteriores, no para aprobar o desaprobar.
- **Qué objetivo ayuda a cumplir:** OE-04 (monitorear el efecto del precio del insumo).
