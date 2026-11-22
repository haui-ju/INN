# Plantilla: Guía paso a paso de Power Query (`materiales/guia-power-query.md`)

| | |
|---|---|
| **Entregable** | `materiales/guia-power-query.md` (material para el equipo; no entra al informe) |
| **Punto** | Previo a 3.1 y al anexo B |
| **Códigos** | `PAS-nn`, `REG-nn`; cita `FUE-nn` y las tablas de `modelo.json` |
| **Entradas** | las fuentes del brief, los archivos de `data/`, `data/respuestas/defectos.csv` y `modelo.json` |
| **Salida** | los pasos ordenados con el código M propuesto para que el equipo los ejecute en Power BI |

## Instrucciones para el agente
1. Escribe en la primera línea `# Guía paso a paso de Power Query` y, justo debajo, que **la ejecuta el equipo** en Power BI, que el código es una propuesta que se prueba y se ajusta y que el resultado que importa es el de cada paso.
2. Ordena los pasos así: importar (UTF-8), tipar, depurar nulos y registros inválidos, homologar nombres de producto, formatos de fecha y nombres de columna, anexar las fuentes de pedidos, completar los días sin precio, calcular claves y medidas y cargar.
3. Una tabla `Código | Paso | Tabla | Resultado esperado` y, por cada paso, un rótulo `**PAS-nn.** título` con su código M (o su lista de pasos de la interfaz).
4. Una segunda tabla `Código | Regla | Defecto que trata`: una regla `REG-nn` por cada tipo de defecto de `data/respuestas/defectos.csv`, con el paso que la aplica.
5. Cierra con la lista de lo que el equipo debe anotar y traer: filas antes y después de cada regla, filas leídas de cada fuente, filas cargadas de cada tabla y los totales del modelo.
6. No digas que algo funciona ni que se ejecutó.

## Formato

````markdown
# Guía paso a paso de Power Query

[Aviso: lo ejecuta el equipo.]

Tabla 1: Pasos propuestos

| Código | Paso | Tabla | Resultado esperado |
|---|---|---|---|
| PAS-01 | [paso] | [tabla] | [resultado] |

**PAS-01.** [Título]

```m
[código M]
```

Tabla 2: Reglas de calidad propuestas

| Código | Regla | Defecto que trata |
|---|---|---|
| REG-01 | [regla] | [defecto] |

**Lo que debe anotar el equipo.** [Lista.]
````

## Ejemplo

````markdown
# Guía paso a paso de Power Query

Esta guía la ejecuta el equipo en Power BI Desktop. El código es una propuesta: se prueba y se ajusta, y lo que cuenta es el resultado de cada paso.

Tabla 1: Pasos propuestos

| Código | Paso | Tabla | Resultado esperado |
|---|---|---|---|
| PAS-01 | Importar los CSV de las tres fuentes con codificación UTF-8 | FUE-01; FUE-02; FUE-03 | Tres consultas con los encabezados en la primera fila |
| PAS-02 | Cambiar el tipo de cada columna | FUE-01; FUE-02; FUE-03 | Ninguna columna numérica o de fecha queda como texto |
| PAS-03 | Anexar caja y aplicaciones y aplicar las reglas | fPedidos | Una sola tabla de pedidos limpia |

**PAS-01.** Importar los CSV

```m
let
    Origen = Csv.Document(File.Contents("C:\datos\fue-01-caja.csv"), [Delimiter = ",", Encoding = 65001]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

**PAS-02.** Cambiar el tipo de cada columna

1. Seleccionar las columnas numéricas y elegir el tipo número.
2. Seleccionar las columnas de fecha y elegir el tipo fecha.

**PAS-03.** Anexar y limpiar

```m
= Table.Distinct(Table.Combine({Caja, Apps}), {"pedido_id"})
```

Tabla 2: Reglas de calidad propuestas

| Código | Regla | Defecto que trata |
|---|---|---|
| REG-01 | Homologar los nombres de producto con una tabla de equivalencias | `nombre_producto` |
| REG-02 | Convertir todas las fechas al formato AAAA-MM-DD | `formato_fecha` |
| REG-03 | Quitar los pedidos que llegan por la caja y por una aplicación | `duplicado` |
| REG-04 | Descartar los registros sin cantidad o con monto negativo | `registro_invalido` |
| REG-05 | Reemplazar los turnos vacíos por «Sin turno» | `nulo` |
| REG-06 | Completar los días sin precio con el último precio publicado | `dia_sin_precio` |

**Lo que debe anotar el equipo.** Las filas de la tabla de trabajo antes y después de cada regla, las filas leídas de cada fuente, las filas cargadas de cada tabla del modelo y los totales de ventas, comisión y líneas del modelo cargado.
````

## Checklist
- [ ] Dice que la ejecuta el equipo y que el código es una propuesta.
- [ ] Una regla por cada tipo de defecto de la hoja de respuestas.
- [ ] Cada `PAS-nn` tiene su código M o su lista de pasos.
- [ ] Termina con lo que el equipo debe anotar.
