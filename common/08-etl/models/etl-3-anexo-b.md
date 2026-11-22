# Plantilla: Anexo B, Scripts del ETL (`anexos/B.md`)

| | |
|---|---|
| **Entregable** | `anexos/B.md` |
| **Punto** | Anexo B: Scripts del ETL (código o pasos de transformación completos) |
| **Códigos** | `PAS-nn` (los de la tabla de pasos de 3.1) |
| **Entradas** | los scripts finales que el equipo ejecutó en Power Query o, si no usó código, los pasos que siguió |
| **Salida** | el código o los pasos completos de cada paso del ETL |

## Instrucciones para el agente
1. La primera línea es `# Anexo B: Scripts del ETL`. Una frase dice que es el código que el equipo ejecutó.
2. Un bloque por cada `PAS-nn` de 3.1, en el mismo orden, con el rótulo `**PAS-nn.** título` y debajo un bloque de código (M de Power Query) o una lista numerada de pasos.
3. **Copia el código que el equipo trajo, tal cual.** Si es distinto del propuesto en la guía, el anexo conserva el del equipo, que es el que se ejecutó. Si el equipo no trae el código de un paso, no lo inventes: dilo al equipo y deja ese paso fuera de 3.1 hasta que lo traiga.
4. No hay tablas en este anexo.

## Formato

````markdown
# Anexo B: Scripts del ETL

[Frase de presentación.]

**PAS-01.** [Título del paso]

```m
[código M]
```

**PAS-02.** [Título del paso]

1. [Paso en la interfaz]
2. [Paso en la interfaz]
````

## Ejemplo

````markdown
# Anexo B: Scripts del ETL

Este anexo reúne el código que el equipo ejecutó en Power Query, un bloque por cada paso de la sección 3.1.

**PAS-01.** Importar los CSV de las tres fuentes

```m
let
    Origen = Csv.Document(File.Contents("C:\datos\fue-01-caja.csv"), [Delimiter = ",", Encoding = 65001]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

**PAS-02.** Cambiar el tipo de cada columna

```m
= Table.TransformColumnTypes(Encabezados, {{"cantidad", Int64.Type}, {"precio_unitario", type number}, {"fecha", type date}})
```

**PAS-03.** Homologar los nombres de columna y de producto

```m
= Table.RenameColumns(Tipos, {{"precio_unitario", "venta_bruta"}, {"ticket_id", "pedido_id"}})
```

**PAS-04.** Anexar caja y aplicaciones y aplicar las reglas

```m
let
    Anexo = Table.Combine({Caja, Apps}),
    SinDuplicados = Table.Distinct(Anexo, {"pedido_id"}),
    Validos = Table.SelectRows(SinDuplicados, each [cantidad] > 0 and [venta_bruta] > 0),
    Turnos = Table.ReplaceValue(Validos, null, "Sin turno", Replacer.ReplaceValue, {"turno"})
in
    Turnos
```

**PAS-05.** Completar los días sin precio

```m
= Table.FillDown(DiasConPrecio, {"precio_kg"})
```

**PAS-06.** Calcular las claves y las medidas del modelo

1. En la consulta de pedidos, combinar con cada dimensión por su nombre y expandir la clave.
2. Agregar la columna `registro_valido` con el valor uno.
3. Agregar `costo_estimado` y `pollos_equivalentes` con la tabla de equivalencias de productos.

**PAS-07.** Cargar las tablas al modelo

1. En Inicio, elegir Cerrar y aplicar.
2. En la vista de modelo, comprobar que las relaciones son las de la sección 2.4.
````

## Checklist
- [ ] Primera línea `# Anexo B: Scripts del ETL`.
- [ ] Un bloque por cada `PAS-nn` de 3.1, con código o con una lista de pasos.
- [ ] El código es el que el equipo ejecutó, no el propuesto.
