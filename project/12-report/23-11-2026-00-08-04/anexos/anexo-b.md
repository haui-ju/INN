# Anexo B: Scripts del ETL

Este anexo reúne el código de Power Query y DAX de cada paso de la sección 3.1, en el orden en que se ejecuta.

**PAS-01.** Crear el parámetro de la ruta de datos y las funciones auxiliares

```m
(archivo as text) as table =>
let
    Origen = Csv.Document(File.Contents(RutaDatos & archivo), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

```m
(t as nullable text) as nullable date =>
let
    s = Text.Trim(Text.Start(t ?? "", 10))
in
    if s = "" then null
    else if Text.Contains(s, "/") then
        try Date.FromText(s, [Format = "dd/MM/yyyy", Culture = "es-PE"]) otherwise null
    else
        try Date.FromText(s, [Format = "yyyy-MM-dd", Culture = "en-US"]) otherwise null
```

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? "")
in
    if s = "" then null else try Number.FromText(s, "en-US") otherwise null
```

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? ""),
    h = if Text.Contains(s, " ") then Text.AfterDelimiter(s, " ", {0, RelativePosition.FromEnd}) else s
in
    if Text.Length(h) >= 4 and Text.Middle(h, 2, 1) = ":" then try Number.FromText(Text.Start(h, 2), "en-US") otherwise null else null
```

```m
(h as nullable number) as text =>
    if h = null then "Sin hora"
    else if h >= 11 and h < 15 then "Mañana"
    else if h >= 15 and h < 19 then "Tarde"
    else if h >= 19 and h < 23 then "Noche"
    else "Fuera de turno"
```

**PAS-02.** Importar el catálogo, los alias de producto y los costos operativos

```m
// Consulta Catalogo
let
    Enc = LeerCsv("apoyo-catalogo-productos.csv"),
    Tipos = Table.TransformColumnTypes(Enc, {{"precio_lista", type number}, {"pollos_equivalentes", type number},
                                            {"kg_pollo_vivo", type number}, {"costo_otros", type number}}, "en-US")
in
    Tipos
```

```m
// Consulta Alias
let
    ConAlias = Table.AddColumn(Catalogo, "nombre_fuente", each Text.Split([alias], "|") & {[producto]}, type list),
    Expandida = Table.ExpandListColumn(ConAlias, "nombre_fuente"),
    Alias = Table.SelectColumns(Expandida, {"nombre_fuente", "producto"})
in
    Alias
```

```m
// Consulta CostosOperativos (el costo del local de cada mes)
let
    Enc = LeerCsv("apoyo-costos-operativos.csv"),
    Tipos = Table.TransformColumnTypes(Enc, {{"planilla", type number}, {"alquiler", type number}, {"servicios", type number},
                                            {"otros", type number}, {"total", type number}}, "en-US")
in
    Tipos
```

**PAS-03.** Importar y limpiar la caja

```m
let
    Origen = LeerCsv("fue-01-caja.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                precio = NumTexto(f[precio_unitario]),
                dscto = NumTexto(f[descuento]) ?? 0,
                invalido = (cant = null) or (cant <= 0) or (precio = null),
                h = HoraTexto(f[hora])
            in
                [fuente = "FUE-01", pedido = f[ticket_id], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = f[canal], producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else Number.Round(cant * precio - dscto, 2), comision = 0,
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-04.** Importar y limpiar Rappi

```m
let
    Origen = LeerCsv("fue-02-rappi.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (monto_n = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha_hora])
            in
                [fuente = "FUE-02", pedido = f[pedido_id], fecha = FechaTexto(f[fecha_hora]), hora = h, turno = TurnoDeHora(h),
                 canal = "Rappi", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n,
                 comision = if invalido then 0 else (NumTexto(f[comision]) ?? 0),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-05.** Importar y limpiar PedidosYa

```m
let
    Origen = LeerCsv("fue-03-pedidosya.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cant]),
                total = NumTexto(f[total]),
                pct = NumTexto(f[comision_pct]) ?? 0,
                invalido = (total = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-03", pedido = f[nro_pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "PedidosYa", producto_fuente = f[item], cantidad = cant ?? 0,
                 monto = if invalido then 0 else total,
                 comision = if invalido then 0 else Number.Round(total * pct / 100, 2),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-06.** Importar WhatsApp y reemplazar el teléfono por un código

```m
let
    Origen = LeerCsv("fue-04-whatsapp.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (cant = null) or (cant <= 0) or (monto_n = null),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-04", pedido = f[pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "WhatsApp", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n, comision = 0,
                 es_invalido = invalido, telefono = f[telefono]]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, telefono = nullable text])
in
    Filas
```

```m
// Consulta Clientes
let
    Distintos = Table.Distinct(Table.SelectColumns(WhatsApp, {"telefono"})),
    Indice = Table.AddIndexColumn(Distintos, "n", 1, 1, Int64.Type),
    Codigo = Table.AddColumn(Indice, "cliente_id", each "C-" & Text.PadStart(Text.From([n]), 4, "0"), type text)
in
    Codigo
```

```m
// Al final de la consulta WhatsApp: reemplaza telefono por cliente_id
    Unido = Table.NestedJoin(Filas, {"telefono"}, Clientes, {"telefono"}, "c", JoinKind.LeftOuter),
    Anonimo = Table.ExpandTableColumn(Unido, "c", {"cliente_id"}),
    Resultado = Table.RemoveColumns(Anonimo, {"telefono"})
```

**PAS-07.** Anexar las cuatro fuentes de venta

```m
// Consulta Pedidos_bruto
let
    Union = Table.Combine({Caja, Rappi, PedidosYa, WhatsApp_anonimo})
in
    Union
```

**PAS-08.** Homologar los nombres de producto con el catálogo

```m
// Consulta Pedidos_homologado (usa la consulta Alias del PAS-02)
let
    Cruce = Table.NestedJoin(Pedidos_bruto, {"producto_fuente"}, Alias, {"nombre_fuente"}, "a", JoinKind.LeftOuter),
    Producto = Table.ExpandTableColumn(Cruce, "a", {"producto"})
in
    Producto
```

**PAS-09.** Marcar los duplicados y los registros válidos

```m
// Consulta Pedidos_marcado
let
    Clave = Table.AddColumn(Pedidos_homologado, "clave", each [pedido] & "|" & [producto], type text),
    Grupos = Table.Group(Clave, {"clave"}, {{"filas", each Table.AddIndexColumn(_, "ord", 0, 1, Int64.Type), type table}}),
    Planas = Table.ExpandTableColumn(Grupos, "filas", List.RemoveItems(Table.ColumnNames(Clave), {"clave"}) & {"ord"}),
    Duplicado = Table.AddColumn(Planas, "es_duplicado", each [ord] > 0, type logical),
    Valido = Table.AddColumn(Duplicado, "registro_valido", each if [es_duplicado] or [es_invalido] then 0 else 1, Int64.Type)
in
    Valido
```

**PAS-10.** Crear el calendario, las dimensiones y las claves

```m
// Consulta Feriados (lista de referencia: ajústala con el calendario oficial)
{ #date(2025, 8, 30), #date(2025, 10, 8), #date(2025, 11, 1), #date(2025, 12, 8), #date(2025, 12, 25), #date(2026, 1, 1), #date(2026, 4, 2), #date(2026, 4, 3), #date(2026, 5, 1), #date(2026, 6, 29), #date(2026, 7, 28), #date(2026, 7, 29), #date(2026, 8, 30), #date(2026, 10, 8) }
```

```m
// Consulta dCalendario
let
    Inicio = #date(2025, 8, 1),
    Fin = #date(2026, 10, 31),
    Dias = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),
    Tabla = Table.FromList(Dias, Splitter.SplitByNothing(), {"fecha"}, null, ExtraValues.Error),
    Tipada = Table.TransformColumnTypes(Tabla, {{"fecha", type date}}),
    Clave = Table.AddColumn(Tipada, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    Anio = Table.AddColumn(Clave, "anio", each Date.Year([fecha]), Int64.Type),
    Mes = Table.AddColumn(Anio, "mes", each Date.Month([fecha]), Int64.Type),
    NombreMes = Table.AddColumn(Mes, "nombre_mes", each {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"}{Date.Month([fecha]) - 1}, type text),
    DiaSemana = Table.AddColumn(NombreMes, "dia_semana", each {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"}{Date.DayOfWeek([fecha], Day.Monday)}, type text),
    AnioMes = Table.AddColumn(DiaSemana, "anio_mes", each Date.Year([fecha]) * 100 + Date.Month([fecha]), Int64.Type),
    MesAnio = Table.AddColumn(AnioMes, "mes_anio", each {"ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"}{Date.Month([fecha]) - 1} & " " & Text.End(Text.From(Date.Year([fecha])), 2), type text),
    Feriado = Table.AddColumn(MesAnio, "es_feriado", each List.Contains(Feriados, [fecha]), type logical)
in
    Feriado
```

```m
// Consulta dProducto
let
    Cols = Table.SelectColumns(Catalogo, {"producto", "categoria"}),
    Clave = Table.AddIndexColumn(Cols, "producto_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dCanal
let
    Datos = #table(type table [canal = text, tipo_canal = text, comision_pct = number],
        {{"Salón", "Presencial", 0}, {"Para llevar", "Presencial", 0}, {"WhatsApp", "Delivery propio", 0}, {"Rappi", "Aplicación", 30}, {"PedidosYa", "Aplicación", 25}}),
    Clave = Table.AddIndexColumn(Datos, "canal_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dTurno
let
    Datos = #table(type table [turno = text, hora_inicio = time, hora_fin = time],
        {{"Mañana", #time(11, 0, 0), #time(15, 0, 0)}, {"Tarde", #time(15, 0, 0), #time(19, 0, 0)}, {"Noche", #time(19, 0, 0), #time(23, 0, 0)}}),
    Clave = Table.AddIndexColumn(Datos, "turno_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dKpi: los indicadores de 2.5
let
    Datos = #table(type table [kpi = text, objetivo = text, tiene_meta = logical, frecuencia = text],
        {{"Calidad de datos del ETL", "OE-01", true, "Por carga"},
         {"Margen de contribución por canal y producto", "OE-02", false, "Mensual"},
         {"Margen neto global", "OE-02", true, "Mensual"},
         {"Porcentaje de merma por turno", "OE-03", true, "Diaria"},
         {"Precisión del pronóstico de demanda", "OE-03", true, "Semanal"},
         {"Precio promedio del pollo vivo por kilogramo", "OE-04", false, "Semanal"},
         {"KPI con meta en el dashboard", "OE-05", true, "Por carga"}}),
    Clave = Table.AddIndexColumn(Datos, "kpi_key", 1, 1, Int64.Type)
in
    Clave
```

**PAS-11.** Armar el precio diario del pollo vivo e imputar los días sin precio

```m
// Consulta PrecioDia (de ella sale fPrecioInsumo)
let
    Origen = LeerCsv("fue-06-precios-pollo.csv"),
    Publicado = Table.FromRecords(
        Table.TransformRows(Origen, (f) => [fecha = FechaTexto(f[fecha]), precio_kg = NumTexto(f[precio_kg])]),
        type table [fecha = date, precio_kg = nullable number]),
    Dias = Table.SelectColumns(dCalendario, {"fecha"}),
    Cruce = Table.NestedJoin(Dias, {"fecha"}, Publicado, {"fecha"}, "p", JoinKind.LeftOuter),
    Precio = Table.ExpandTableColumn(Cruce, "p", {"precio_kg"}),
    Orden = Table.Sort(Precio, {{"fecha", Order.Ascending}}),
    Marca = Table.AddColumn(Orden, "valor_imputado", each if [precio_kg] = null then 1 else 0, Int64.Type),
    Relleno = Table.FillDown(Marca, {"precio_kg"}),
    Tipos = Table.TransformColumnTypes(Relleno, {{"precio_kg", type number}})
in
    Tipos
```

**PAS-12.** Calcular las medidas de los pedidos

```m
// Consulta fPedidos
let
    // 1. Catálogo (equivalentes, kilos de pollo y otros insumos) y precio del pollo del día
    ConCat = Table.NestedJoin(Pedidos_marcado, {"producto"}, Catalogo, {"producto"}, "c", JoinKind.LeftOuter),
    ExpCat = Table.ExpandTableColumn(ConCat, "c", {"pollos_equivalentes", "kg_pollo_vivo", "costo_otros"}, {"eq", "kg", "otros"}),
    ConPrecio = Table.NestedJoin(ExpCat, {"fecha"}, PrecioDia, {"fecha"}, "p", JoinKind.LeftOuter),
    ExpPrecio = Table.ExpandTableColumn(ConPrecio, "p", {"precio_kg"}),
    // 2. Mes de la venta y venta válida de cada mes (para repartir el costo operativo)
    Mes = Table.AddColumn(ExpPrecio, "mes", each Date.ToText([fecha], [Format = "yyyy-MM", Culture = "en-US"]), type text),
    Venta = Table.AddColumn(Mes, "venta_bruta", each [monto] * [registro_valido], type number),
    VentaMes = Table.Group(Venta, {"mes"}, {{"venta_mes", each List.Sum([venta_bruta]), type number}}),
    ConMes = Table.NestedJoin(Venta, {"mes"}, VentaMes, {"mes"}, "vm", JoinKind.LeftOuter),
    ExpMes = Table.ExpandTableColumn(ConMes, "vm", {"venta_mes"}),
    ConOper = Table.NestedJoin(ExpMes, {"mes"}, CostosOperativos, {"mes"}, "co", JoinKind.LeftOuter),
    ExpOper = Table.ExpandTableColumn(ConOper, "co", {"total"}, {"total_mes"}),
    // 3. Medidas por línea (0 si el registro no es válido)
    Comision = Table.AddColumn(ExpOper, "comision_v", each [comision] * [registro_valido], type number),
    Cantidad = Table.AddColumn(Comision, "cantidad_v", each [cantidad] * [registro_valido], type number),
    Equivalentes = Table.AddColumn(Cantidad, "pollos_equivalentes", each [cantidad] * [eq] * [registro_valido], type number),
    CostoEst = Table.AddColumn(Equivalentes, "costo_estimado", each [registro_valido] * [cantidad] * ([kg] * [precio_kg] + [otros]), type number),
    CostoOp = Table.AddColumn(CostoEst, "costo_operativo", each if [venta_mes] = 0 then 0 else [total_mes] * [venta_bruta] / [venta_mes], type number),
    Total = Table.AddColumn(CostoOp, "registro_total", each 1, Int64.Type),
    // 4. Claves hacia las dimensiones
    KFecha = Table.AddColumn(Total, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KProd = Table.NestedJoin(KFecha, {"producto"}, dProducto, {"producto"}, "d1", JoinKind.LeftOuter),
    KProd2 = Table.ExpandTableColumn(KProd, "d1", {"producto_key"}),
    KCanal = Table.NestedJoin(KProd2, {"canal"}, dCanal, {"canal"}, "d2", JoinKind.LeftOuter),
    KCanal2 = Table.ExpandTableColumn(KCanal, "d2", {"canal_key"}),
    KTurno = Table.NestedJoin(KCanal2, {"turno"}, dTurno, {"turno"}, "d3", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "d3", {"turno_key"}),
    // 5. Solo las columnas del modelo
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "producto_key", "canal_key", "turno_key", "cantidad_v", "venta_bruta", "comision_v",
                                        "costo_estimado", "costo_operativo", "pollos_equivalentes", "registro_valido", "registro_total"}),
    Nombres = Table.RenameColumns(Sel, {{"cantidad_v", "cantidad"}, {"comision_v", "comision"}})
in
    Nombres
```

**PAS-13.** Construir la producción por turno

```m
// Consulta fProduccion
let
    Origen = LeerCsv("fue-05-produccion.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                prep = NumTexto(f[pollos_preparados]),
                ven = NumTexto(f[pollos_vendidos]),
                mer = NumTexto(f[pollos_merma])
            in
                [fecha = FechaTexto(f[fecha]), turno = f[turno], pollos_preparados = prep, pollos_vendidos = ven, pollos_merma = mer,
                 es_invalido = (prep = null) or (ven = null) or (ven > prep)]),
        type table [fecha = nullable date, turno = text, pollos_preparados = nullable number, pollos_vendidos = nullable number,
                    pollos_merma = nullable number, es_invalido = logical]),
    SinCopias = Table.Distinct(Filas, {"fecha", "turno"}),
    Validas = Table.SelectRows(SinCopias, each not [es_invalido]),
    KFecha = Table.AddColumn(Validas, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KTurno = Table.NestedJoin(KFecha, {"turno"}, dTurno, {"turno"}, "t", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "t", {"turno_key"}),
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "turno_key", "pollos_preparados", "pollos_vendidos", "pollos_merma"})
in
    Sel
```

**PAS-14.** Construir las metas de los KPI

```m
// Consulta fMetaKpi
let
    Meses = List.Transform({0..14}, each Date.AddMonths(#date(2025, 8, 1), _)),
    Metas = #table(type table [kpi_key = Int64.Type, meta = nullable number], {{1, 98.0}, {2, null}, {3, 12.0}, {4, 3.0}, {5, 15.0}, {6, null}, {7, 100.0}}),
    Cruce = Table.AddColumn(Metas, "fecha", each Meses, type list),
    Expandida = Table.ExpandListColumn(Cruce, "fecha"),
    Clave = Table.AddColumn(Expandida, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + 1, Int64.Type),
    Real = Table.AddColumn(Clave, "valor_real", each null, type nullable number),
    Sel = Table.SelectColumns(Real, {"kpi_key", "fecha_key", "meta", "valor_real"})
in
    Sel
```

**PAS-15.** Cargar el modelo y crear las relaciones

1. En Inicio, elegir Cerrar y aplicar, con solo las nueve tablas del modelo habilitadas para la carga.
2. En la vista de modelo, crear las nueve relaciones de varios a uno y de un solo sentido: fPedidos con dCalendario, dProducto, dCanal y dTurno; fProduccion con dCalendario y dTurno; fPrecioInsumo con dCalendario; fMetaKpi con dKpi y dCalendario.
3. Marcar dCalendario como tabla de fechas con la columna fecha y ordenar nombre_mes por mes.

**PAS-16.** Verificar los totales contra la hoja de respuestas

```dax
Ventas = SUM(fPedidos[venta_bruta])
Comisión = SUM(fPedidos[comision])
Costo estimado = SUM(fPedidos[costo_estimado])
Costo operativo = SUM(fPedidos[costo_operativo])
Margen neto % = DIVIDE([Ventas] - [Comisión] - [Costo estimado] - [Costo operativo], [Ventas])
Filas leídas = SUM(fPedidos[registro_total])
Filas válidas = SUM(fPedidos[registro_valido])
```
