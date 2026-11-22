# Guía paso a paso del ETL en Power BI

> **Esta guía la ejecuta el equipo en Power BI Desktop.** No se ejecutó Power Query para escribirla: el código M es una propuesta que se prueba y se ajusta. Lo que importa es el **punto de control** que cierra cada paso (cuántas filas deben quedar): si tu número coincide, el paso salió bien; si no, la tabla «Si tu número no coincide» de la sección 10 te dice qué paso revisar.

Los datos son **generados para el proyecto** (`modo_datos: generado`) y cubren de 2025-08-01 a 2026-10-31 (457 días, un local). Están en la carpeta `data/`. Las cifras de esta guía salen de la hoja de respuestas (`data/respuestas/`): si sigues los pasos, tus resultados deberían coincidir con ellas.

## 0. Antes de empezar

### Qué vas a construir

Nueve tablas con la forma de `modelo.json` (2.4): cuatro de hechos y cinco dimensiones.

| Tabla | Qué guarda | Filas que debe tener |
|---|---|---|
| `fPedidos` | Una fila por línea de pedido, canal y día | 91 297 |
| `fProduccion` | Una fila por turno y día | 1 366 |
| `fPrecioInsumo` | Una fila por día | 457 |
| `fMetaKpi` | Una fila por KPI y mes | 105 |
| `dCalendario` | Atributos: fecha, anio, mes, nombre_mes, dia_semana, es_feriado | 457 |
| `dProducto` | Atributos: producto, categoria | 8 |
| `dCanal` | Atributos: canal, tipo_canal, comision_pct | 5 |
| `dTurno` | Atributos: turno, hora_inicio, hora_fin | 3 |
| `dKpi` | Atributos: kpi, objetivo, tiene_meta, frecuencia | 7 |

### Los archivos de `data/`

| Archivo | Qué es | Filas | Defectos que trae |
|---|---|---|---|
| `fue-01-caja.csv` | Ventas del salón y para llevar (una fila por línea de ticket) | 59 134 | fechas, nombres de producto, duplicados, vacíos y registros inválidos |
| `fue-02-rappi.csv` | Reporte de Rappi, con la comisión de cada línea | 13 448 | fechas, nombres de producto, duplicados, cancelados y filas sin monto |
| `fue-03-pedidosya.csv` | Reporte de PedidosYa, con **otros nombres de columna** y la comisión como porcentaje | 9 737 | los mismos |
| `fue-04-whatsapp.csv` | Pedidos del delivery propio, con el teléfono del cliente | 8 978 | los mismos y datos personales |
| `fue-05-produccion.csv` | Pollos preparados, vendidos y merma por día y turno | 1 374 | fechas, un responsable vacío, jornadas repetidas y jornadas imposibles |
| `fue-06-precios-pollo.csv` | Precio diario del kilo de pollo vivo | 437 | fechas y 20 días sin precio |
| `apoyo-catalogo-productos.csv` | Lista de precios y receta de cada producto, con los nombres que usan las fuentes | 8 | ninguno (es la referencia para homologar) |
| `apoyo-costos-operativos.csv` | Costo operativo de cada mes (planilla, alquiler, servicios y otros) | 15 | ninguno |

### Tres cosas de configuración que evitan la mitad de los errores

1. **Codificación UTF-8** (`Encoding = 65001` en el código M): si no, «Salón» y «Mañana» salen con símbolos raros.
2. **El punto es el separador decimal** en los archivos (`62.00`). Tu Windows puede estar en español con coma decimal: por eso el código lee los números con `Number.FromText(texto, "en-US")`. **No dejes que Power BI «detecte el tipo»** al importar: puede leer `62.00` como texto o como 6200.
3. **Las fechas con barras son día/mes/año** (`03/08/2025` es el 3 de agosto). Si Power BI las lee como mes/día, las ventas de agosto aparecen en marzo. El código fija el formato.

### Cómo llevar tu propia evidencia

En cada paso, anota **cuántas filas tenía la tabla antes y después**. Al final hay una tabla para copiar esas cifras: son la evidencia (`evidencia.json`) con la que se redactan la sección 3.1 y el anexo A. Si algo no coincide, no sigas: corrige y vuelve a contar.

## 1. Pasos del ETL

| Código | Paso | Resultado esperado |
|---|---|---|
| PAS-01 | Crear el parámetro `RutaDatos` y las funciones auxiliares | Seis consultas de ayuda, sin tablas cargadas |
| PAS-02 | Importar el catálogo, los alias y los costos operativos | `Catalogo` (8 filas), `Alias` (32 filas), `CostosOperativos` (15 filas) |
| PAS-03 | Importar y limpiar la caja (FUE-01) | 59 134 filas en el esquema común |
| PAS-04 | Importar y limpiar Rappi (FUE-02) | 13 448 filas en el esquema común |
| PAS-05 | Importar y limpiar PedidosYa (FUE-03) | 9 737 filas en el esquema común |
| PAS-06 | Importar WhatsApp (FUE-04) y anonimizar el teléfono | 8 978 filas y 886 clientes con código |
| PAS-07 | Anexar las cuatro fuentes | `Pedidos_bruto` con 91 297 filas |
| PAS-08 | Homologar los nombres de producto | Ninguna fila sin producto del catálogo |
| PAS-09 | Marcar duplicados y registros válidos | 674 duplicados, 735 inválidos y 89 888 válidos |
| PAS-10 | Calendario, dimensiones y claves | `dCalendario`, `dProducto`, `dCanal`, `dTurno` y `dKpi` |
| PAS-11 | Precio diario del pollo e imputación | 457 días, 20 imputados |
| PAS-12 | Calcular las medidas de `fPedidos` | `fPedidos` con 91 297 filas y los totales de la sección 7 |
| PAS-13 | Construir `fProduccion` | 1 366 filas |
| PAS-14 | Construir `fMetaKpi` | 105 filas |
| PAS-15 | Cargar el modelo y crear las relaciones | Nueve relaciones, de varios a uno |
| PAS-16 | Verificar contra la hoja de respuestas | Los totales coinciden |

| Código | Regla de calidad | Defecto que trata | Paso |
|---|---|---|---|
| REG-01 | Estandarizar todas las fechas a un solo formato | `formato_fecha` | PAS-01, 03 a 06, 11, 13 |
| REG-02 | Homologar el nombre de cada producto contra el catálogo | `nombre_producto` | PAS-08 |
| REG-03 | Marcar y no contar las copias duplicadas | `duplicado` | PAS-09, 13 |
| REG-04 | Marcar y no contar los registros inválidos (sin cantidad o monto, o cancelados) | `registro_invalido` | PAS-03 a 06, 09, 13 |
| REG-05 | Completar los vacíos que se pueden deducir | `nulo` | PAS-03, 13 |
| REG-06 | Imputar el precio de los días sin precio y marcarlos | `dia_sin_precio` | PAS-11 |
| REG-07 | Reemplazar el teléfono del cliente por un código | datos personales | PAS-06 |

## 2. Preparación (PAS-01 y PAS-02)

### PAS-01. El parámetro y las funciones auxiliares

En Power BI Desktop: **Transformar datos** (abre el Editor de Power Query). Crea cada elemento con **Nueva consulta ▸ Consulta en blanco** y pega el código en el **Editor avanzado**. Estas consultas **no se cargan al modelo**: desmarca «Habilitar carga» (clic derecho sobre la consulta).

**Consulta `RutaDatos`** (parámetro de texto, en «Administrar parámetros»): la carpeta con los CSV, por ejemplo `C:\datos\` (con la barra final).

**Consulta `LeerCsv`** (función): lee un CSV como texto, sin que Power BI adivine los tipos.

```m
(archivo as text) as table =>
let
    Origen = Csv.Document(File.Contents(RutaDatos & archivo), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

**Consulta `FechaTexto`** (función): entiende `2025-08-01`, `01/08/2025` y cualquiera de los dos con hora (`01/08/2025 13:09`).

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

**Consulta `NumTexto`** (función): convierte un texto con punto decimal en número, y el texto vacío en `null`.

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? "")
in
    if s = "" then null else try Number.FromText(s, "en-US") otherwise null
```

**Consulta `HoraTexto`** (función): devuelve la hora (0 a 23) de `11:04` o de `2025-08-01 12:08:00`.

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? ""),
    h = if Text.Contains(s, " ") then Text.AfterDelimiter(s, " ", {0, RelativePosition.FromEnd}) else s
in
    if Text.Length(h) >= 4 and Text.Middle(h, 2, 1) = ":" then try Number.FromText(Text.Start(h, 2), "en-US") otherwise null else null
```

**Consulta `TurnoDeHora`** (función): el turno que corresponde a una hora, con los mismos límites que `dTurno`.

```m
(h as nullable number) as text =>
    if h = null then "Sin hora"
    else if h >= 11 and h < 15 then "Mañana"
    else if h >= 15 and h < 19 then "Tarde"
    else if h >= 19 and h < 23 then "Noche"
    else "Fuera de turno"
```

**Punto de control:** seis consultas de ayuda (`RutaDatos`, `LeerCsv`, `FechaTexto`, `NumTexto`, `HoraTexto`, `TurnoDeHora`). Prueba `FechaTexto("03/08/2025 13:09")` y `FechaTexto("2025-08-03")`: ambas deben dar el **3 de agosto de 2025**.

### PAS-02. Catálogo, alias y costos operativos

El **catálogo** es la lista de precios y recetas del dueño. Es la referencia para homologar nombres y para calcular costos. Cada producto trae sus **alias**: los nombres con que lo escriben las fuentes.

```text
producto,categoria,precio_lista,pollos_equivalentes,kg_pollo_vivo,costo_otros,alias
Pollo entero a la brasa,Pollo,62.00,1.00,1.90,9.00,POLLO ENTERO|Pollo entero|Pollo a la brasa entero
Medio pollo a la brasa,Pollo,34.00,0.50,0.95,5.50,1/2 pollo|Medio pollo|1/2 Pollo a la brasa
Cuarto de pollo con papas,Pollo,19.00,0.25,0.48,3.50,1/4 pollo c/ papas|Cuarto pollo|1/4 Pollo + papas
```

```m
// Consulta Catalogo
let
    Enc = LeerCsv("apoyo-catalogo-productos.csv"),
    Tipos = Table.TransformColumnTypes(Enc, {{"precio_lista", type number}, {"pollos_equivalentes", type number},
                                            {"kg_pollo_vivo", type number}, {"costo_otros", type number}}, "en-US")
in
    Tipos
```

Los alias se separan con `|`. Para homologar necesitas **una fila por cada nombre posible** (el alias y el nombre oficial):

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

**Punto de control:** `Catalogo` 8 filas; `Alias` 32 filas (8 nombres oficiales y 24 alias); `CostosOperativos` 15 filas (de 2025-08 a 2026-10). El total de `CostosOperativos` suma **S/ 1 377 628**.

## 3. Las cuatro fuentes de ventas (PAS-03 a PAS-06)

Las cuatro fuentes dicen casi lo mismo (quién compró qué, cuándo, por cuánto) con **columnas distintas**. El primer objetivo es llevarlas todas al mismo **esquema común**:

| Columna común | Qué es |
|---|---|
| `fuente` | FUE-01 a FUE-04 |
| `pedido` | Identificador del ticket o pedido |
| `fecha` | Fecha ya convertida (REG-01) |
| `hora y turno` | La hora de la venta y su turno (Mañana 11–15, Tarde 15–19, Noche 19–23) |
| `canal` | Salón, Para llevar, WhatsApp, Rappi o PedidosYa |
| `producto_fuente` | El nombre tal como lo escribe la fuente (se homologa después) |
| `cantidad` | Unidades de la línea |
| `monto` | Venta de la línea en soles (0 si la fila es inválida) |
| `comision` | Comisión de la aplicación (0 en los canales propios) |
| `es_invalido` | `true` si la fila no sirve (REG-04) |
| `cliente_id` | Solo en WhatsApp: un código en lugar del teléfono (REG-07) |

En las cuatro consultas se hace lo mismo: se lee todo como texto, se convierte cada campo con las funciones auxiliares y se marca la fila inválida. **Nada se borra todavía**: así puedes contar.

### PAS-03. Caja (FUE-01)

```text
ticket_id,fecha,hora,turno,canal,producto,cantidad,precio_unitario,descuento,estado
T-001604,2025-08-01,11:04,Mañana,Para llevar,Cuarto de pollo con papas,1,19.0,0,OK
T-000479,2025-08-01,11:25,Mañana,Salón,Cuarto de pollo con papas,1,19.0,0,OK
T-000479,2025-08-01,11:25,Mañana,Salón,Bebida,2,9.0,0,OK
```

| Defecto | Cuántas filas | Por qué importa | Cómo se trata |
|---|---|---|---|
| Fechas en el otro formato (REG-01) | 2 393 | Un día/mes/año leído como mes/día mueve ventas de mes | `FechaTexto` entiende los dos formatos |
| Nombres de producto distintos (REG-02) | 7 307 | Un mismo producto aparecería con varios nombres y su margen quedaría repartido | Se homologan en el PAS-08 |
| Copias duplicadas (REG-03) | 302 | Cada copia suma otra vez la venta | Se marcan en el PAS-09 |
| Registros inválidos (REG-04) | 461 | Sin cantidad o monto no hay venta que contar | `es_invalido = true` y monto 0 |
| Vacíos (REG-05) | 1 765 | Un turno vacío rompe el análisis por turno; un descuento vacío es 0 | El turno se deduce de la hora; el descuento vacío vale 0 |

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

**Punto de control:** la consulta `Caja` tiene **59 134 filas**; si filtras `es_invalido = true` y `fecha` vacía, no debe quedar ninguna fecha vacía. Cuenta las filas con barras en la fecha: **2 393** (incluye las copias duplicadas).

### PAS-04. Rappi (FUE-02)

```text
pedido_id,fecha_hora,producto,cantidad,monto,comision,estado
RP-001851,2025-08-01 12:08:00,"Combo familiar (pollo, papas y bebida)",2,156.00,46.80,ENTREGADO
RP-001851,2025-08-01 12:08:00,Gaseosa 1.5 L,2,18.00,5.40,ENTREGADO
RP-001851,2025-08-01 12:08:00,Adicional,2,14.00,4.20,ENTREGADO
```

| Defecto | Cuántas filas | Por qué importa | Cómo se trata |
|---|---|---|---|
| Fechas en el otro formato (REG-01) | 568 | Un día/mes/año leído como mes/día mueve ventas de mes | `FechaTexto` entiende los dos formatos |
| Nombres de producto distintos (REG-02) | 8 095 | Un mismo producto aparecería con varios nombres y su margen quedaría repartido | Se homologan en el PAS-08 |
| Copias duplicadas (REG-03) | 144 | Cada copia suma otra vez la venta | Se marcan en el PAS-09 |
| Registros inválidos (REG-04) | 125 | Sin cantidad o monto no hay venta que contar | `es_invalido = true` y monto 0 |
| Pedidos cancelados (parte de REG-04) | 44 | Suman S/ 1 620.00 que no se cobraron | Cuentan como inválidos |

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

**Punto de control:** `Rappi` tiene **13 448 filas**. La comisión ya viene en cada fila (30 % del monto).

### PAS-05. PedidosYa (FUE-03)

```text
nro_pedido,fecha,item,cant,total,comision_pct,estado
PY-002077,01/08/2025 13:09,POLLO ENTERO,2,124.00,25,ENTREGADO
PY-002077,01/08/2025 13:09,Bebida,1,9.00,25,ENTREGADO
PY-002068,01/08/2025 14:41,1/4 Pollo + papas,2,38.00,25,ENTREGADO
```

| Defecto | Cuántas filas | Por qué importa | Cómo se trata |
|---|---|---|---|
| Fechas en el otro formato (REG-01) | 395 | Un día/mes/año leído como mes/día mueve ventas de mes | `FechaTexto` entiende los dos formatos |
| Nombres de producto distintos (REG-02) | 5 784 | Un mismo producto aparecería con varios nombres y su margen quedaría repartido | Se homologan en el PAS-08 |
| Copias duplicadas (REG-03) | 128 | Cada copia suma otra vez la venta | Se marcan en el PAS-09 |
| Registros inválidos (REG-04) | 98 | Sin cantidad o monto no hay venta que contar | `es_invalido = true` y monto 0 |
| Pedidos cancelados (parte de REG-04) | 35 | Suman S/ 1 047.00 que no se cobraron | Cuentan como inválidos |

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

Aquí las columnas se llaman distinto (`nro_pedido`, `item`, `cant`, `total`) y **la comisión no viene en soles sino como porcentaje** (`comision_pct`, 25): se calcula como `total × comision_pct / 100`, redondeada a dos decimales.

**Punto de control:** `PedidosYa` tiene **9 737 filas**. Las fechas de este archivo vienen **con barras** (día/mes/año): las **395** que vienen con guiones son las que están en el «otro» formato.

### PAS-06. WhatsApp (FUE-04) y datos personales

```text
pedido,fecha,telefono,producto,cantidad,monto,tipo_entrega
WA-001803,2025-08-01 12:08,916549514,Medio pollo a la brasa,1,34.00,Recojo
WA-001803,2025-08-01 12:08,916549514,Bebida,1,9.00,Delivery
WA-001803,2025-08-01 12:08,916549514,ADICIONAL,1,7.00,Delivery
```

| Defecto | Cuántas filas | Por qué importa | Cómo se trata |
|---|---|---|---|
| Fechas en el otro formato (REG-01) | 373 | Un día/mes/año leído como mes/día mueve ventas de mes | `FechaTexto` entiende los dos formatos |
| Nombres de producto distintos (REG-02) | 2 704 | Un mismo producto aparecería con varios nombres y su margen quedaría repartido | Se homologan en el PAS-08 |
| Copias duplicadas (REG-03) | 100 | Cada copia suma otra vez la venta | Se marcan en el PAS-09 |
| Registros inválidos (REG-04) | 51 | Sin cantidad o monto no hay venta que contar | `es_invalido = true` y monto 0 |

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

Después, en una consulta nueva `Clientes`, crea un código por cada teléfono distinto, y en `WhatsApp` cambia el teléfono por ese código:

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
(Como `Clientes` se construye a partir de `WhatsApp`, crea primero `WhatsApp` con el teléfono, luego `Clientes`, y duplica `WhatsApp` como `WhatsApp_anonimo` para añadir estos tres pasos. En `WhatsApp_anonimo` la columna `telefono` ya no existe y aparece `cliente_id`.)

**REG-07, el teléfono:** el número identifica a una persona (Ley 29733, de Protección de Datos Personales). El análisis no lo necesita: solo necesita saber **si es el mismo cliente**. Por eso se reemplaza por un código (`C-0001`, `C-0002`…) antes de cargar el modelo. Nunca cargues el teléfono al modelo ni al informe.

**Punto de control:** `WhatsApp_anonimo` tiene **8 978 filas** y **886 clientes distintos** (`Clientes`); la columna `telefono` ya no existe.

## 4. Unir y marcar (PAS-07 a PAS-09)

### PAS-07. Anexar las cuatro fuentes

```m
// Consulta Pedidos_bruto
let
    Union = Table.Combine({Caja, Rappi, PedidosYa, WhatsApp_anonimo})
in
    Union
```

**Punto de control:** `Pedidos_bruto` tiene **91 297 filas** (59 134 + 13 448 + 9 737 + 8 978). Este número es el **total de registros leídos** y es el denominador de KPI-01 (calidad de datos).

### PAS-08. Homologar los nombres de producto (REG-02)

Las fuentes escriben el mismo producto de varias maneras. Mira los nombres distintos de `producto_fuente` en `Pedidos_bruto` (Vista de columnas: «Distribución de la columna»): verás **unos 32 nombres** para **8 productos**. Se unen contra `Alias`:

```m
// Consulta Pedidos_homologado (usa la consulta Alias del PAS-02)
let
    Cruce = Table.NestedJoin(Pedidos_bruto, {"producto_fuente"}, Alias, {"nombre_fuente"}, "a", JoinKind.LeftOuter),
    Producto = Table.ExpandTableColumn(Cruce, "a", {"producto"})
in
    Producto
```

Ejemplo: `POLLO ENTERO`, `Pollo entero` y `Pollo a la brasa entero` pasan todos a **Pollo entero a la brasa**.

**Punto de control:** la tabla sigue con **91 297 filas** y **ninguna** con `producto` vacío (filtra `producto = null`: deben ser 0). Si hay filas vacías, hay un nombre que no está en `Alias`: revisa tildes y espacios. Debes ver exactamente **8** productos distintos.

### PAS-09. Marcar duplicados y registros válidos (REG-03 y REG-04)

Una **copia duplicada** es una fila idéntica a otra (mismo pedido y mismo producto) que se coló dos veces, por ejemplo cuando el reporte de una aplicación se descargó dos veces. Si no se trata, la venta se cuenta doble. Para no perder la cuenta de lo que llegó, **no se borra**: se marca. Una fila es **válida** si no es copia y no es inválida.

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

| Resultado | Filas | Cómo contarlo |
|---|---|---|
| Filas leídas | 91 297 | todas las filas de la tabla |
| Copias duplicadas | 674 | `es_duplicado = true` |
| Quedan sin copias | 90 623 | `es_duplicado = false` |
| Inválidas entre las que quedan | 735 | `es_duplicado = false` y `es_invalido = true` |
| **Válidas** | **89 888** | `registro_valido = 1` |

**Por qué importa:** si no quitas las copias, las ventas suben **S/ 20 950.50** de más; si cuentas los cancelados de las aplicaciones, suben **S/ 2 667.00**. KPI-01 (calidad de datos) = filas válidas ÷ filas leídas = **98.46 %**, por encima de su meta de 98 %.

> Las cifras de «copias» de la hoja `defectos.csv` cuentan cada copia **una vez**, y los demás defectos sobre las filas **sin copias**; por eso algunos conteos que haces sobre el archivo tal cual llega salen un poco mayores (las copias traen los mismos defectos). Esta guía te da las dos cifras cuando difieren.

## 5. Dimensiones y claves (PAS-10)

Una **dimensión** es una lista corta de «cosas» por las que se analiza (días, productos, canales, turnos, indicadores). Cada una lleva una **clave** (`*_key`) y los hechos guardan esa clave para unirse a ella.

### `dCalendario`: un día por fila

Todos los días del periodo, **también los que no tuvieron ventas** (457 días). El calendario es la columna vertebral del tiempo: sin él no se puede hacer la imputación del precio ni comparar meses.

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
    Feriado = Table.AddColumn(DiaSemana, "es_feriado", each List.Contains(Feriados, [fecha]), type logical)
in
    Feriado
```

**Punto de control:** **457 filas**, de 2025-08-01 a 2026-10-31. `fecha_key` del 1 de agosto de 2025 = `20250801`.

### `dProducto`, `dCanal`, `dTurno` y `dKpi`

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

**Punto de control:** `dProducto` **8** filas; `dCanal` **5**; `dTurno` **3**; `dKpi` **7**. En `dKpi`, `tiene_meta` es `false` para los KPI cuya meta sigue pendiente en 2.5.

## 6. El precio del pollo vivo (PAS-11)

El boletín de precios trae **437 filas para 457 días**: faltan **20** (fines de semana y feriados en que no se publicó). Pero el costo del pollo se calcula **día por día**: si un día no tiene precio, el costo de ese día saldría **0** y el margen se vería inflado.

La regla (REG-06): **usar el último precio publicado** y marcar el día como imputado (`valor_imputado = 1`) para que se pueda medir cuánto del dato es estimado.

```text
fecha,precio_kg
2025-08-01,6.14
2025-08-02,6.17
2025-08-03,6.07
```

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

**Consulta `fPrecioInsumo`:** copia `PrecioDia`, agrega `fecha_key` (igual que en `dCalendario`) y deja `fecha_key`, `precio_kg`, `valor_imputado`.

**Punto de control:** `PrecioDia` tiene **457 filas**; `valor_imputado = 1` en **20**; el precio del **1 de julio de 2026 es S/ 6.10** y el del **14 de julio, S/ 6.90** (el salto del que habla el informe).

## 7. Las medidas de `fPedidos` (PAS-12)

Hasta aquí cada fila dice qué pasó. Ahora se le agrega **cuánto vale**: la venta, la comisión, el costo del pollo y del local. Todas se multiplican por `registro_valido` (1 o 0), de modo que las filas duplicadas o inválidas **siguen en la tabla pero no suman**.

| Columna | Cómo se calcula | De dónde salen los datos |
|---|---|---|
| `venta_bruta` | `monto × registro_valido` | caja: `cantidad × precio_unitario − descuento`; apps y WhatsApp: el monto de la fuente |
| `comision` | `comision × registro_valido` | Rappi: viene en soles; PedidosYa: `total × comision_pct / 100`; caja y WhatsApp: 0 |
| `pollos_equivalentes` | `cantidad × pollos_equivalentes del producto × registro_valido` | `apoyo-catalogo-productos.csv` |
| `costo_estimado` | `cantidad × (kg_pollo_vivo × precio del pollo del día + costo_otros) × registro_valido` | catálogo + `PrecioDia` |
| `costo_operativo` | `costo del mes × venta_bruta de la línea ÷ venta_bruta del mes` | `apoyo-costos-operativos.csv` |
| `registro_valido` / `registro_total` | 1 si es válida, 0 si no / 1 en toda fila leída | marcas del PAS-09 |

Ejemplo: un **Pollo entero** vendido el 14 de julio con el pollo vivo a S/ 6.90 cuesta `1.90 kg × 6.90 + 9.00 = S/ 22.11`; con el pollo a S/ 6.10 habría costado S/ 20.59. Esa diferencia es la que erosiona el margen en los últimos meses.

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

**Punto de control:** `fPedidos` tiene **91 297 filas** y `SUM(registro_valido)` = **89 888**. Los totales de las columnas son:

| Columna | Total esperado |
|---|---|
| `venta_bruta` | S/ 2 917 426.10 |
| `comision` | S/ 206 732.30 |
| `costo_estimado` | S/ 1 016 976.96 |
| `costo_operativo` | S/ 1 377 628.00 |
| Margen neto del periodo | 10.83 % |

## 8. Producción y metas (PAS-13 y PAS-14)

### PAS-13. `fProduccion`

La cocina anota por cada día y turno cuántos pollos preparó, cuántos vendió y cuántos sobraron (merma). Defectos: **3** jornadas repetidas, **5** jornadas imposibles (vendidos mayores que preparados), **34** fechas en el otro formato y **14** responsables vacíos (no afectan a ningún KPI; se pueden dejar como «Sin dato»).

```text
fecha,turno,pollos_preparados,pollos_vendidos,pollos_merma,responsable
2025-08-01,Mañana,34,33,1,Rosa Quispe
2025-08-01,Tarde,15,14,1,Rosa Quispe
2025-08-01,Noche,37,34,3,Rosa Quispe
```

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

**Punto de control:** 1 374 filas leídas → 1 371 sin repetidas → **1 366** válidas. Debería haber 457 días × 3 turnos = 1371 jornadas; faltan 5 porque las jornadas imposibles se excluyen.

### PAS-14. `fMetaKpi`

Una fila por indicador y mes, con su **meta** (de 2.5). La columna `valor_real` queda vacía en el ETL: se calcula con las medidas del dashboard (en la guía del dashboard) y se compara con la meta.

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

| KPI | Meta de 2.5 |
|---|---|
| KPI-01 Calidad de datos del ETL | 98 % o más |
| KPI-02 Margen de contribución por canal y producto | Pendiente |
| KPI-03 Margen neto global | 12 % o más |
| KPI-04 Porcentaje de merma por turno | 3 % o menos |
| KPI-05 Precisión del pronóstico de demanda | 15 % o menos |
| KPI-06 Precio promedio del pollo vivo por kilogramo | Pendiente |
| KPI-07 KPI con meta en el dashboard | 100 % |

**Punto de control:** **105 filas** (7 indicadores × 15 meses). KPI-02 y KPI-06 quedan con meta vacía (pendiente).

## 9. Cargar y relacionar (PAS-15)

Cierra el editor con **Cerrar y aplicar**. Solo se cargan las nueve tablas del modelo; las demás consultas quedan como ayuda. Luego, en la **Vista de modelo**, crea estas relaciones (de varios a uno, un solo sentido de filtro):

| Código | Desde (varios) | Hacia (uno) | Campo | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | `fPedidos` | `dCalendario` | `fecha_key` | *:1 | Simple |
| REL-02 | `fPedidos` | `dProducto` | `producto_key` | *:1 | Simple |
| REL-03 | `fPedidos` | `dCanal` | `canal_key` | *:1 | Simple |
| REL-04 | `fPedidos` | `dTurno` | `turno_key` | *:1 | Simple |
| REL-05 | `fProduccion` | `dCalendario` | `fecha_key` | *:1 | Simple |
| REL-06 | `fProduccion` | `dTurno` | `turno_key` | *:1 | Simple |
| REL-07 | `fPrecioInsumo` | `dCalendario` | `fecha_key` | *:1 | Simple |
| REL-08 | `fMetaKpi` | `dKpi` | `kpi_key` | *:1 | Simple |
| REL-09 | `fMetaKpi` | `dCalendario` | `fecha_key` | *:1 | Simple |

Marca `dCalendario` como **tabla de fechas** (Herramientas de tabla ▸ Marcar como tabla de fechas ▸ columna `fecha`) y ordena `nombre_mes` por `mes` y `dia_semana` por su número para que los gráficos salgan en orden.

**Punto de control:** la vista de modelo muestra **nueve relaciones** y ninguna advertencia de relación ambigua o activa a medias.

## 10. Verificar contra la hoja de respuestas (PAS-16)

Crea estas medidas en una tabla vacía (Entrar datos ▸ tabla `_Medidas`) y arma una tabla con **mes** (`dCalendario[anio]`, `dCalendario[mes]`) y las medidas:

```dax
Ventas = SUM(fPedidos[venta_bruta])
Comisión = SUM(fPedidos[comision])
Costo estimado = SUM(fPedidos[costo_estimado])
Costo operativo = SUM(fPedidos[costo_operativo])
Margen neto % = DIVIDE([Ventas] - [Comisión] - [Costo estimado] - [Costo operativo], [Ventas])
Filas leídas = SUM(fPedidos[registro_total])
Filas válidas = SUM(fPedidos[registro_valido])
```

Tus valores deben coincidir con estos (tolerancia: un centavo por redondeo):

| Mes | Ventas | Comisión | Costo estimado | Costo operativo | Margen neto |
|---|---|---|---|---|---|
| 2025-08 | 176 311.90 | 7 442.25 | 60 817.41 | 83 369 | 14.0 % |
| 2025-09 | 178 410.10 | 8 246.90 | 61 419.11 | 84 661 | 13.5 % |
| 2025-10 | 183 807.00 | 9 185.95 | 63 220.58 | 87 660 | 12.92 % |
| 2025-11 | 188 713.80 | 10 190.05 | 65 240.27 | 89 287 | 12.72 % |
| 2025-12 | 208 136.10 | 12 060.80 | 71 692.17 | 98 743 | 12.32 % |
| 2026-01 | 178 473.20 | 11 017.35 | 61 457.93 | 84 486 | 12.05 % |
| 2026-02 | 175 619.30 | 11 615.10 | 60 339.27 | 84 155 | 11.11 % |
| 2026-03 | 187 660.00 | 13 124.80 | 64 759.83 | 89 657 | 10.72 % |
| 2026-04 | 192 216.80 | 14 169.25 | 66 172.31 | 91 525 | 10.59 % |
| 2026-05 | 198 345.80 | 15 434.85 | 68 418.52 | 93 899 | 10.38 % |
| 2026-06 | 201 683.00 | 16 504.30 | 69 266.67 | 96 691 | 9.53 % |
| 2026-07 | 212 641.00 | 18 190.95 | 76 063.60 | 99 026 | 9.1 % |
| 2026-08 | 207 499.50 | 18 582.90 | 74 435.20 | 96 803 | 8.52 % |
| 2026-09 | 210 566.80 | 19 696.45 | 75 932.17 | 96 724 | 8.65 % |
| 2026-10 | 217 341.80 | 21 270.40 | 77 741.92 | 100 942 | 8.0 % |

Por canal (todo el periodo):

| Canal | Líneas válidas | Ventas | Comisión |
|---|---|---|---|
| Salón | 30 212 | 969 031.20 | 0.00 |
| Para llevar | 28 159 | 883 627.90 | 0.00 |
| WhatsApp | 8 827 | 323 746.00 | 0.00 |
| Rappi | 13 179 | 429 541.00 | 128 862.30 |
| PedidosYa | 9 511 | 311 480.00 | 77 870.00 |

La hoja completa (por mes y canal) está en `data/respuestas/ventas-mes-canal.csv`. Si prefieres que lo compare un programa, exporta tus tablas a `data/salida/<tabla>.csv` (`fPedidos`, `fProduccion`, `fPrecioInsumo`, `dCalendario`, `dCanal`, `dTurno`) y ejecuta `python3 .claude/skills/_shared/datagen.py verificar`: te dice la tabla, el mes y la diferencia.

### Si tu número no coincide

| Lo que ves | Causa más probable |
|---|---|
| Ventas mayores en ≈ S/ 20 950 | No marcaste las copias duplicadas (PAS-09) |
| Ventas mayores en ≈ S/ 2 667 | Contaste los pedidos cancelados de Rappi y PedidosYa |
| Un mes con ventas de otro mes | Las fechas con barras se leyeron como mes/día (usa `FechaTexto`) |
| Margen de contribución demasiado alto en un producto | Productos sin homologar: el costo no se pudo calcular |
| Margen neto más alto en los días de julio | Días sin precio sin imputar (el costo del pollo sale 0) |
| Números con millones de pesos de más o de menos | El punto decimal se leyó como separador de miles (usa `en-US`) |
| `fPedidos` con más o menos filas que las leídas | Borraste filas en vez de marcarlas, o dejaste una consulta sin anexar |
| Una columna con `Error` | Un nombre de producto sin alias, o un texto con espacios (revisa el PAS-08) |

## 11. Lo que debes anotar y traer

Copia tus cifras en esta tabla (las esperadas son las de la hoja de respuestas). Con ella se redacta la sección 3.1 y el anexo A:

| Regla | Defecto | Filas antes | Filas después | Lo esperado |
|---|---|---|---|---|
| REG-01 | Fechas en otro formato | — | — | 3 777 fechas convertidas, 0 sin entender |
| REG-02 | Nombres de producto | 91 297 | 91 297 | 8 productos, 0 sin catálogo |
| REG-03 | Copias duplicadas | 91 297 | 90 623 | 674 copias |
| REG-04 | Registros inválidos | 90 623 | 89 888 | 735 inválidos |
| REG-05 | Vacíos | — | — | turno deducido de la hora; descuento vacío = 0 |
| REG-06 | Días sin precio | 437 | 457 | 20 días imputados |
| REG-07 | Teléfonos | 8 978 | 8 978 | 886 clientes con código |

Y las filas de cada tabla cargada:

| Tabla | Filas esperadas |
|---|---|
| `fPedidos` | 91 297 |
| `fProduccion` | 1 366 |
| `fPrecioInsumo` | 457 |
| `fMetaKpi` | 105 |
| `dCalendario` | 457 |
| `dProducto` | 8 |
| `dCanal` | 5 |
| `dTurno` | 3 |
| `dKpi` | 7 |

Trae además: **tus scripts** (las consultas de Power Query, para el anexo B), **capturas** del editor con los conteos y los **totales** de la sección 10. Con eso se redacta el ETL; **nada de esta guía se da por hecho hasta que lo traigas**.

## Apéndice. Diccionario de datos

### Tablas del modelo y origen de cada campo

| Tabla | Campo | Tipo | Origen |
|---|---|---|---|
| `fPedidos` | `fecha_key` | entero | FUE-01 a FUE-04: fecha |
| `fPedidos` | `producto_key` | entero | Catálogo: producto homologado |
| `fPedidos` | `canal_key` | entero | FUE-01 a FUE-04: canal |
| `fPedidos` | `turno_key` | entero | FUE-01 a FUE-04: hora → turno |
| `fPedidos` | `cantidad` | número | FUE-01 a FUE-04: cantidad |
| `fPedidos` | `venta_bruta` | número | Cálculo: monto de la línea |
| `fPedidos` | `comision` | número | FUE-02: comision; FUE-03: Cálculo total × comision_pct / 100 |
| `fPedidos` | `costo_estimado` | número | Cálculo: apoyo-catalogo-productos y FUE-06 |
| `fPedidos` | `costo_operativo` | número | Cálculo: apoyo-costos-operativos |
| `fPedidos` | `pollos_equivalentes` | número | Cálculo: apoyo-catalogo-productos |
| `fPedidos` | `registro_valido` | entero | Cálculo: marcas de duplicado e inválido |
| `fPedidos` | `registro_total` | entero | Cálculo: 1 por fila leída |
| `fProduccion` | `fecha_key` | entero | FUE-05: fecha |
| `fProduccion` | `turno_key` | entero | FUE-05: turno |
| `fProduccion` | `pollos_preparados` | número | FUE-05: pollos_preparados |
| `fProduccion` | `pollos_vendidos` | número | FUE-05: pollos_vendidos |
| `fProduccion` | `pollos_merma` | número | FUE-05: pollos_merma |
| `fPrecioInsumo` | `fecha_key` | entero | dCalendario: fecha |
| `fPrecioInsumo` | `precio_kg` | número | FUE-06: precio_kg (imputado si falta) |
| `fPrecioInsumo` | `valor_imputado` | entero | Cálculo: 1 si el día no tenía precio |
| `fMetaKpi` | `kpi_key` | entero | dKpi |
| `fMetaKpi` | `fecha_key` | entero | Cálculo: primer día de cada mes |
| `fMetaKpi` | `meta` | número | Cálculo: metas de 2.5 |
| `fMetaKpi` | `valor_real` | número | Cálculo: medidas del dashboard |
| `dCalendario` | `fecha_key` | entero | Cálculo: número de fila |
| `dCalendario` | `fecha` | fecha | Cálculo: lista de días |
| `dCalendario` | `anio` | entero | Cálculo: fecha |
| `dCalendario` | `mes` | entero | Cálculo: fecha |
| `dCalendario` | `nombre_mes` | texto | Cálculo: fecha |
| `dCalendario` | `dia_semana` | texto | Cálculo: fecha |
| `dCalendario` | `es_feriado` | lógico | Cálculo: lista de feriados |
| `dProducto` | `producto_key` | entero | Cálculo: número de fila |
| `dProducto` | `producto` | texto | apoyo-catalogo-productos: producto |
| `dProducto` | `categoria` | texto | apoyo-catalogo-productos: categoria |
| `dCanal` | `canal_key` | entero | Cálculo: número de fila |
| `dCanal` | `canal` | texto | Cálculo: lista de canales |
| `dCanal` | `tipo_canal` | texto | Cálculo: lista de canales |
| `dCanal` | `comision_pct` | número | Cálculo: 30 Rappi, 25 PedidosYa |
| `dTurno` | `turno_key` | entero | Cálculo: número de fila |
| `dTurno` | `turno` | texto | Cálculo: lista de turnos |
| `dTurno` | `hora_inicio` | hora | Cálculo: lista de turnos |
| `dTurno` | `hora_fin` | hora | Cálculo: lista de turnos |
| `dKpi` | `kpi_key` | entero | Cálculo: número de fila |
| `dKpi` | `kpi` | texto | Cálculo: 2.5 |
| `dKpi` | `objetivo` | texto | Cálculo: 2.5 |
| `dKpi` | `tiene_meta` | lógico | Cálculo: meta de 2.5 |
| `dKpi` | `frecuencia` | texto | Cálculo: 2.5 |

### Campos de las fuentes

- **`fue-01-caja.csv`:** `ticket_id`, `fecha`, `hora`, `turno`, `canal`, `producto`, `cantidad`, `precio_unitario`, `descuento`, `estado`
- **`fue-02-rappi.csv`:** `pedido_id`, `fecha_hora`, `producto`, `cantidad`, `monto`, `comision`, `estado`
- **`fue-03-pedidosya.csv`:** `nro_pedido`, `fecha`, `item`, `cant`, `total`, `comision_pct`, `estado`
- **`fue-04-whatsapp.csv`:** `pedido`, `fecha`, `telefono`, `producto`, `cantidad`, `monto`, `tipo_entrega`
- **`fue-05-produccion.csv`:** `fecha`, `turno`, `pollos_preparados`, `pollos_vendidos`, `pollos_merma`, `responsable`
- **`fue-06-precios-pollo.csv`:** `fecha`, `precio_kg`

Todas las columnas llegan como **texto**; la conversión a número, fecha y lógico (`true` o `false`) la hace el código de esta guía.

