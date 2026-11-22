# Plantilla: Indicadores clave de rendimiento (`secciones/2.5.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.5.md` |
| **Punto** | 2.5. Indicadores clave de rendimiento |
| **Códigos** | `KPI-nn`; cita `OE-nn` del brief |
| **Entradas** | objetivos con su indicador y meta (brief), modelo de 2.4, decisiones del brief |
| **Salida** | cada KPI con su fórmula, su medida, sus campos de origen, su meta, su frecuencia, el objetivo que mide y la decisión que apoya |

## Instrucciones para el agente
1. La primera línea es `## 2.5. Indicadores clave de rendimiento`.
2. Un párrafo que explica el criterio con que se eligieron los KPI (medir cada objetivo y sostener una decisión) y cuántos son.
3. **Definición.** Tabla `Código | KPI | Fórmula | Medida propuesta | Origen`. La fórmula va en palabras; la medida propuesta es el nombre de la medida DAX; el origen son campos del modelo de 2.4 escritos `tabla.campo` y separados por punto y coma. Para cada `OE` hay un KPI con el **mismo nombre que su indicador en el brief**.
4. **Gestión.** Tabla `Código | Meta | Frecuencia | Objetivo | Decisión que apoya`: la meta con cifra y comparador (o «Pendiente»), la frecuencia (Diaria, Semanal, Mensual, Trimestral, Anual o «Por carga»), el `OE-nn` que mide y una de las decisiones del brief.
5. Cada `OE` del brief tiene al menos un KPI; todo campo de origen existe en 2.4.
6. **Lectura de los KPI.** Una o dos frases: qué dirá el semáforo del dashboard sobre el estado del proyecto.

## Formato

```markdown
## 2.5. Indicadores clave de rendimiento

[Párrafo con el criterio de elección y la cantidad de KPI.]

**Definición.** [Frase que presenta la tabla.]

Tabla 1: Definición de los KPI

| Código | KPI | Fórmula | Medida propuesta | Origen |
|---|---|---|---|---|
| KPI-01 | [indicador del brief] | [fórmula en palabras] | [Nombre de la medida] | [tabla.campo]; [tabla.campo] |

**Gestión.** [Frase que presenta la tabla.]

Tabla 2: Meta, frecuencia y decisión de cada KPI

| Código | Meta | Frecuencia | Objetivo | Decisión que apoya |
|---|---|---|---|---|
| KPI-01 | [cifra y comparador o Pendiente] | [frecuencia] | OE-01 | [decisión del brief] |

**Lectura de los KPI.** [Qué dirá el semáforo del dashboard.]
```

## Ejemplo

```markdown
## 2.5. Indicadores clave de rendimiento

Los indicadores se eligieron con dos criterios: que midan el logro de un objetivo específico y que sostengan una decisión de la gerencia. Son cinco, tres de ellos con el mismo nombre que el indicador de su objetivo en el brief, y todos se calculan con campos del modelo de datos.

**Definición.** Cada indicador se define con su fórmula, la medida que lo calcula en Power BI y los campos del modelo de los que sale.

Tabla 1: Definición de los KPI

| Código | KPI | Fórmula | Medida propuesta | Origen |
|---|---|---|---|---|
| KPI-01 | Calidad de datos del ETL | Registros válidos entre registros cargados | % Registros válidos | fPedidos.registro_valido |
| KPI-02 | Margen neto por canal | (Venta bruta menos comisión menos costo estimado) entre venta bruta, por canal | Margen neto % | fPedidos.venta_bruta; fPedidos.comision; fPedidos.costo_estimado; dCanal.canal |
| KPI-03 | Porcentaje de merma por turno | Pollos de merma entre pollos preparados, por turno | % Merma | fProduccion.pollos_merma; fProduccion.pollos_preparados; dTurno.turno |
| KPI-04 | Participación del canal directo | Ventas de los canales propios entre las ventas totales | % Canal directo | fPedidos.venta_bruta; dCanal.tipo_canal |
| KPI-05 | Precio promedio del pollo vivo por kilogramo | Promedio del precio diario por kilogramo en el periodo | Precio pollo vivo | fPrecioInsumo.precio_kg; dCalendario.fecha |

**Gestión.** Cada indicador tiene una meta, una frecuencia de revisión, el objetivo que mide y la decisión que apoya.

Tabla 2: Meta, frecuencia y decisión de cada KPI

| Código | Meta | Frecuencia | Objetivo | Decisión que apoya |
|---|---|---|---|---|
| KPI-01 | 98 % o más | Por carga | OE-01 | Confiar en las cifras del dashboard antes de decidir |
| KPI-02 | 12 % o más en el margen neto global | Mensual | OE-02 | Ajustar el precio de los combos en las apps de delivery |
| KPI-03 | 3 % o menos | Diaria | OE-03 | Definir cuántos pollos hornear por turno y día de la semana |
| KPI-04 | 70 % o más | Mensual | OE-02 | Ajustar el precio de los combos en las apps de delivery |
| KPI-05 | Pendiente | Semanal | OE-02 | Anticipar compras ante subidas del precio del pollo vivo |

**Lectura de los KPI.** El semáforo del dashboard compara cada indicador con su meta: si el margen por canal o la merma se alejan de ella, la gerencia sabe qué decisión revisar. La meta del precio del insumo se fija cuando se conozca la serie completa de precios.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Cada `OE` del brief tiene al menos un KPI y uno de ellos se llama como su indicador.
- [ ] Todo campo de origen existe en las tablas de 2.4.
- [ ] Cada KPI tiene meta (o «Pendiente»), frecuencia, objetivo y decisión.
- [ ] Si algún KPI tiene frecuencia por periodo, el modelo tiene dimensión de tiempo.
