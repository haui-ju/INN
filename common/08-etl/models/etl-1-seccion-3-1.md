# Plantilla: Construcción de la solución ETL (`secciones/3.1.md`)

| | |
|---|---|
| **Entregable** | `secciones/3.1.md` |
| **Punto** | 3.1. Construcción de la solución ETL |
| **Códigos** | `REG-nn`, `PAS-nn`; cita `FUE-nn` del brief y las tablas del modelo |
| **Entradas** | `evidencia.json` del equipo, fuentes del brief, `modelo.json`, `data/respuestas/` y el config (`modo_datos`) |
| **Salida** | la extracción, los pasos, las reglas de calidad con sus cifras, la carga y la verificación contra la hoja de respuestas |

## Instrucciones para el agente
1. La primera línea es `## 3.1. Construcción de la solución ETL`. Escribe solo con la evidencia que trajo el equipo: ninguna cifra sale de otro lugar.
2. **Párrafo inicial.** La herramienta (la del componente de ETL de la arquitectura), que lo construyó el equipo y que los datos son **generados** para el proyecto (cómo se calibraron y que incluyen defectos para ejercitar el ETL). Si `modo_datos` es `real`, di de dónde salen.
3. **Extracción.** Una frase y la tabla `Código | Fuente | Archivo | Filas leídas`: una fila por cada fuente del brief; las filas leídas salen de `tablas` (`FUE-nn`) de la evidencia.
4. **Transformación.** Una frase (el código completo está en el anexo B). Si `data/` tiene archivos de apoyo (`apoyo-*.csv`), explica en palabras cómo se calculan `costo_estimado` (cantidad por los kilos de pollo vivo del producto por el precio del día más sus otros costos) y `costo_operativo` (el total del mes repartido en proporción a la venta). Después, la tabla `Código | Paso | Tabla | Resultado` con los `PAS-nn`.
5. **Reglas de calidad.** Una frase y la tabla `Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después`. El defecto es uno de `registro_invalido`, `duplicado`, `nombre_producto`, `formato_fecha`, `nulo` o `dia_sin_precio`; **cada defecto de `data/respuestas/defectos.csv` tiene una regla**. Las filas salen de `reglas` de la evidencia.
6. **Carga.** Una frase y la tabla `Tabla | Filas cargadas` con todas las tablas del modelo.
7. **Verificación.** Un párrafo con el resultado de comparar los totales con la hoja de respuestas: «coinciden» o cuántas diferencias hay. Si las hay, la tabla `Tabla | Mes | Esperado | Obtenido | Diferencia`.
8. **Lectura del ETL.** Una o dos frases: qué garantiza el ETL para los KPI (por ejemplo, el porcentaje de registros válidos).
9. No digas que un paso se ejecutó si la evidencia no lo respalda.

## Formato

```markdown
## 3.1. Construcción de la solución ETL

[Párrafo: herramienta, quién lo construyó y declaración de datos generados.]

**Extracción.** [Frase.]

Tabla 1: Fuentes extraídas

| Código | Fuente | Archivo | Filas leídas |
|---|---|---|---|
| FUE-01 | [fuente] | [archivo.csv] | [filas] |

**Transformación.** [Frase.]

Tabla 2: Pasos del ETL en Power Query

| Código | Paso | Tabla | Resultado |
|---|---|---|---|
| PAS-01 | [paso] | [tabla] | [resultado] |

**Reglas de calidad.** [Frase.]

Tabla 3: Reglas de calidad y su resultado

| Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después |
|---|---|---|---|---|---|---|
| REG-01 | [regla] | [defecto] | [tabla] | [criterio] | [filas] | [filas] |

**Carga.** [Frase.]

Tabla 4: Tablas cargadas al modelo

| Tabla | Filas cargadas |
|---|---|
| [tabla] | [filas] |

**Verificación.** [Resultado de la comparación con la hoja de respuestas.]

**Lectura del ETL.** [Qué garantiza para los KPI.]
```

## Ejemplo

```markdown
## 3.1. Construcción de la solución ETL

El equipo construyó el ETL con Power Query, dentro de Power BI Desktop, a partir de los archivos CSV de las tres fuentes del proyecto. Los datos son generados para el proyecto: se calibraron con las cifras del informe y se les incluyeron defectos a propósito (duplicados, nombres de producto distintos, fechas con formatos mezclados, nulos y días sin precio) para que el ETL tenga qué corregir.

**Extracción.** Cada fuente se importó con su archivo CSV en codificación UTF-8 y su número de filas se registró antes de transformarla.

Tabla 1: Fuentes extraídas

| Código | Fuente | Archivo | Filas leídas |
|---|---|---|---|
| FUE-01 | Sistema de caja de los locales | fue-01-caja.csv | 1200 |
| FUE-02 | Reportes de las apps de delivery | fue-02-apps.csv | 400 |
| FUE-03 | Precios del pollo vivo en Lima Metropolitana | fue-03-precios.csv | 80 |

**Transformación.** Siete pasos llevan las tres fuentes a las tablas del modelo; el código completo de cada uno está en el anexo B. El costo estimado de cada línea es la cantidad por los kilos de pollo vivo del producto, por el precio del día, más sus otros costos, con los datos del catálogo de productos; el costo operativo de cada mes se reparte entre sus líneas en proporción a la venta.

Tabla 2: Pasos del ETL en Power Query

| Código | Paso | Tabla | Resultado |
|---|---|---|---|
| PAS-01 | Importar los CSV de las tres fuentes con codificación UTF-8 | FUE-01; FUE-02; FUE-03 | Tres consultas con los encabezados en la primera fila |
| PAS-02 | Cambiar el tipo de cada columna a fecha, número o texto | FUE-01; FUE-02; FUE-03 | Ninguna columna numérica o de fecha queda como texto |
| PAS-03 | Homologar los nombres de columna y de producto de las fuentes | fPedidos | Las columnas coinciden con las del modelo (REG-01) |
| PAS-04 | Anexar caja y aplicaciones y aplicar las reglas REG-02 a REG-05 | fPedidos | Una sola tabla de pedidos limpia |
| PAS-05 | Completar los días sin precio con el último precio publicado | fPrecioInsumo | Un precio por cada día del periodo (REG-06) |
| PAS-06 | Calcular las claves y las medidas del modelo | fPedidos; fProduccion | Claves sustitutas y medidas listas para cargar |
| PAS-07 | Cargar las tablas al modelo | Todas las del modelo | Modelo en estrella cargado |

**Reglas de calidad.** Seis reglas tratan los defectos que traen los datos. Todas conservan o reducen las filas de pedidos, salvo la de los días sin precio, que las completa.

Tabla 3: Reglas de calidad y su resultado

| Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después |
|---|---|---|---|---|---|---|
| REG-01 | Homologar los nombres de producto con una tabla de equivalencias | `nombre_producto` | fPedidos | Todo producto coincide con un nombre de dProducto | 1600 | 1600 |
| REG-02 | Convertir todas las fechas al formato AAAA-MM-DD | `formato_fecha` | fPedidos | Ninguna fecha queda como texto | 1600 | 1600 |
| REG-03 | Quitar los pedidos que llegan por la caja y por una aplicación | `duplicado` | fPedidos | Un solo registro por pedido | 1600 | 1568 |
| REG-04 | Descartar los registros sin cantidad o con monto negativo | `registro_invalido` | fPedidos | Todo registro tiene cantidad y monto positivos | 1568 | 1550 |
| REG-05 | Reemplazar los turnos vacíos por «Sin turno» | `nulo` | fPedidos | Ningún turno queda vacío | 1550 | 1550 |
| REG-06 | Completar los días sin precio con el último precio publicado | `dia_sin_precio` | fPrecioInsumo | Un precio por cada día del periodo | 80 | 92 |

**Carga.** El modelo en estrella quedó cargado con las tres tablas de hechos y las cinco dimensiones del diseño.

Tabla 4: Tablas cargadas al modelo

| Tabla | Filas cargadas |
|---|---|
| fPedidos | 1550 |
| fProduccion | 60 |
| fPrecioInsumo | 92 |
| dCalendario | 92 |
| dProducto | 12 |
| dCanal | 3 |
| dLocal | 2 |
| dTurno | 3 |

**Verificación.** Los totales del modelo cargado coinciden con los de la hoja de respuestas en todos los meses y canales: las ventas, la comisión y las líneas de pedido no tienen diferencias.

**Lectura del ETL.** Con las seis reglas aplicadas, el modelo conserva solo registros válidos, de modo que el porcentaje de registros válidos de los KPI se mide sobre datos ya depurados.
```

## Checklist
- [ ] Encabezado exacto en la primera línea y título `Tabla N:` antes de cada tabla.
- [ ] Declara que los datos son generados (si `modo_datos` es `generado`).
- [ ] Una fila por cada fuente del brief, con las filas de la evidencia.
- [ ] Cada defecto de la hoja de respuestas tiene una regla y cada regla tiene sus cifras.
- [ ] Todas las tablas del modelo están en la carga, con las filas de la evidencia.
- [ ] La verificación dice lo mismo que `evidencia.json` y no oculta diferencias.
