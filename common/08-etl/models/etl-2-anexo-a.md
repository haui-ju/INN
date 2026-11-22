# Plantilla: Anexo A, Diccionario de datos y calidad de datos (`anexos/A.md`)

| | |
|---|---|
| **Entregable** | `anexos/A.md` |
| **Punto** | Anexo A: Diccionario de datos y calidad de datos (tablas, campos, tipos, reglas de calidad y resultados) |
| **Códigos** | cita `FUE-nn`, `REG-nn` y los campos del modelo `tabla.campo` |
| **Entradas** | la sección `3.1.md` de la misma corrida, `evidencia.json`, `modelo.json` y los archivos de `data/` |
| **Salida** | el diccionario de los campos de entrada, el origen de cada campo del modelo y el resultado de cada regla |

## Instrucciones para el agente
1. La primera línea es `# Anexo A: Diccionario de datos y calidad de datos`. Una frase presenta el anexo.
2. **Diccionario de los campos de entrada.** Tabla `Fuente | Campo | Tipo | Regla de calidad | Destino`: una fila por campo de cada fuente del brief y de cada archivo de apoyo, que se nombra «Apoyo: …» (los campos salen de los encabezados de los CSV de `data/`). El tipo es texto, entero, decimal o fecha. La regla es un `REG-nn` de 3.1 o «—». El destino es un `tabla.campo` del modelo o «—».
3. **Origen de los campos del modelo.** Tabla `Tabla | Campo | Origen`: **todas** las tablas de `modelo.json` y todos sus campos (claves, medidas y atributos). En `Campo` van varios campos con el mismo origen, separados por punto y coma. El origen es una lista, separada por punto y coma, de `FUE-nn.campo`, de `apoyo-<archivo>.campo` (por ejemplo `apoyo-catalogo-productos.kg_pollo_vivo`) o de «Cálculo: » con la expresión en palabras.
4. **Resultado de las reglas de calidad.** Tabla `Código | Filas antes | Filas después | Diferencia`: una fila por regla de 3.1, con las cifras de la evidencia; la diferencia es filas después menos filas antes.
5. Antes de cada tabla va su título `Tabla N: …`.

## Formato

```markdown
# Anexo A: Diccionario de datos y calidad de datos

[Frase de presentación.]

Tabla 1: Diccionario de los campos de entrada

| Fuente | Campo | Tipo | Regla de calidad | Destino |
|---|---|---|---|---|
| FUE-01 | [campo] | [tipo] | REG-01 | [tabla.campo] |

Tabla 2: Origen de los campos del modelo

| Tabla | Campo | Origen |
|---|---|---|
| [tabla] | [campo]; [campo] | FUE-01.[campo]; Cálculo: [expresión] |

Tabla 3: Resultado de las reglas de calidad

| Código | Filas antes | Filas después | Diferencia |
|---|---|---|---|
| REG-01 | [filas] | [filas] | [diferencia] |
```

## Ejemplo

```markdown
# Anexo A: Diccionario de datos y calidad de datos

Este anexo lista los campos de las tres fuentes, el origen de cada campo del modelo y el resultado de cada regla de calidad.

Tabla 1: Diccionario de los campos de entrada

| Fuente | Campo | Tipo | Regla de calidad | Destino |
|---|---|---|---|---|
| FUE-01 | ticket_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-01 | fecha | fecha | REG-02 | dCalendario.fecha |
| FUE-01 | turno | texto | REG-05 | dTurno.turno |
| FUE-01 | canal | texto | — | dCanal.canal |
| FUE-01 | producto | texto | REG-01 | dProducto.producto |
| FUE-01 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-01 | precio_unitario | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-02 | pedido_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-02 | monto | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-02 | comision | decimal | — | fPedidos.comision |
| FUE-03 | fecha | fecha | REG-06 | dCalendario.fecha |
| FUE-03 | precio_kg | decimal | REG-06 | fPrecioInsumo.precio_kg |
| Apoyo: catálogo de productos | kg_pollo_vivo | decimal | — | fPedidos.costo_estimado |
| Apoyo: catálogo de productos | costo_otros | decimal | — | fPedidos.costo_estimado |

Tabla 2: Origen de los campos del modelo

| Tabla | Campo | Origen |
|---|---|---|
| fPedidos | fecha_key; producto_key; canal_key; local_key; turno_key | Cálculo: clave sustituta que se busca en cada dimensión |
| fPedidos | cantidad; venta_bruta | FUE-01.cantidad; FUE-01.precio_unitario; FUE-02.monto |
| fPedidos | comision | FUE-02.comision |
| fPedidos | costo_estimado | apoyo-catalogo-productos.kg_pollo_vivo; apoyo-catalogo-productos.costo_otros; FUE-03.precio_kg; Cálculo: cantidad por los kilos de pollo vivo por el precio del día más otros costos |
| fPedidos | pollos_equivalentes | apoyo-catalogo-productos.pollos_equivalentes |
| fPedidos | registro_valido | Cálculo: uno si el registro pasa las reglas REG-03 y REG-04 |
| fProduccion | fecha_key; local_key; turno_key | Cálculo: clave sustituta que se busca en cada dimensión |
| fProduccion | pollos_preparados; pollos_vendidos; pollos_merma | FUE-01.cantidad; Cálculo: preparados y merma según el registro de cocina |
| fPrecioInsumo | fecha_key | Cálculo: clave sustituta que se busca en dCalendario |
| fPrecioInsumo | precio_kg | FUE-03.precio_kg |
| dCalendario | fecha_key; fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Cálculo: una fila por cada día del periodo |
| dProducto | producto_key; producto; categoria | FUE-01.producto; Cálculo: categoría según la tabla de equivalencias |
| dCanal | canal_key; canal; tipo_canal; comision_pct | FUE-01.canal; Cálculo: tipo y comisión según el canal |
| dLocal | local_key; local; zona | Cálculo: lista de locales del dominio del proyecto |
| dTurno | turno_key; turno; hora_inicio; hora_fin | FUE-01.turno; Cálculo: horario de cada turno |

Tabla 3: Resultado de las reglas de calidad

| Código | Filas antes | Filas después | Diferencia |
|---|---|---|---|
| REG-01 | 1600 | 1600 | 0 |
| REG-02 | 1600 | 1600 | 0 |
| REG-03 | 1600 | 1568 | -32 |
| REG-04 | 1568 | 1550 | -18 |
| REG-05 | 1550 | 1550 | 0 |
| REG-06 | 80 | 92 | 12 |
```

## Checklist
- [ ] Primera línea `# Anexo A: Diccionario de datos y calidad de datos` y un título `Tabla N:` antes de cada tabla.
- [ ] Todas las fuentes del brief tienen campos en la tabla 1.
- [ ] Todo campo de todas las tablas del modelo aparece en la tabla 2 con su origen.
- [ ] Una fila por cada regla de 3.1, con las cifras de la evidencia.
