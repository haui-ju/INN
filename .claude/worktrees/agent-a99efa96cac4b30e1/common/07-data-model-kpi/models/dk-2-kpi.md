# Plantilla: Indicadores clave de rendimiento (`secciones/2.5.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.5.md` y la parte de KPI de `modelo.json` |
| **Punto** | 2.5. Indicadores clave de rendimiento |
| **Códigos** | `KPI-nn`; cita `OE-nn` (del brief) y los campos del modelo de 2.4 |
| **Entradas** | objetivos del brief con su indicador y su meta, decisiones del brief y de 2.1, modelo de 2.4 |
| **Salida** | cada KPI con fórmula, medida propuesta, origen, meta, frecuencia, objetivo y decisión |

## Instrucciones para el agente
1. La primera línea es `## 2.5. Indicadores clave de rendimiento`. Esta sección no lleva figura.
2. Un párrafo que presenta los KPI con su cita (Parmenter, 2015).
3. La tabla de definición `Código | KPI | Fórmula | Medida propuesta | Origen`: la fórmula en palabras, la medida DAX propuesta entre comillas invertidas con campos `tabla[campo]` y el origen como `tabla.campo` separados por punto y coma. Todos los campos existen en 2.4.
4. La tabla de seguimiento `Código | Meta | Frecuencia | Objetivo | Decisión que apoya`, con los mismos códigos y en el mismo orden. Meta con cifra o «Pendiente»; frecuencia Diaria, Semanal, Quincenal, Mensual, Trimestral, Semestral, Anual o Por carga; objetivo `OE-nn` del brief.
5. Cada `OE` del brief tiene al menos un KPI; el KPI que lo mide repite el nombre de su indicador en el brief.
6. **Lectura de los indicadores.** Una o dos frases: qué KPI responde a cada objetivo.
7. Después de escribir: `python3 .claude/skills/_shared/diseno.py modelo --run <corrida>`.

## Formato

```markdown
## 2.5. Indicadores clave de rendimiento

[Párrafo que presenta los KPI, con su cita.]

Tabla 1: Definición de los KPI

| Código | KPI | Fórmula | Medida propuesta | Origen |
|---|---|---|---|---|
| KPI-01 | [indicador del brief] | [fórmula en palabras] | `[Nombre] = [expresión DAX con tabla[campo]]` | tabla.campo; tabla.campo |

Tabla 2: Seguimiento de los KPI

| Código | Meta | Frecuencia | Objetivo | Decisión que apoya |
|---|---|---|---|---|
| KPI-01 | [meta con cifra o Pendiente] | [frecuencia] | OE-01 | [decisión] |

**Lectura de los indicadores.** [Qué KPI responde a cada objetivo.]
```

## Ejemplo

```markdown
## 2.5. Indicadores clave de rendimiento

Un indicador clave de rendimiento muestra si un objetivo avanza y orienta una decisión concreta (Parmenter, 2015). Cada KPI de la solución responde a un objetivo específico, se calcula solo con campos del modelo de datos y tiene una meta que la gerencia revisa con la frecuencia indicada.

Tabla 1: Definición de los KPI

| Código | KPI | Fórmula | Medida propuesta | Origen |
|---|---|---|---|---|
| KPI-01 | Calidad de datos del ETL | Registros válidos ÷ registros leídos × 100, por fuente y carga | `Calidad de datos % = DIVIDE(SUM(fct_calidad[registros_validos]), SUM(fct_calidad[registros_leidos]))` | fct_calidad.registros_validos; fct_calidad.registros_leidos; dim_fuente.fuente |
| KPI-02 | Margen neto por canal | (Ventas − comisiones − costo de insumos) ÷ ventas × 100, por canal | `Margen neto % = DIVIDE(SUM(fct_ventas[importe_bruto]) - SUM(fct_ventas[comision]) - SUM(fct_ventas[costo_insumos]), SUM(fct_ventas[importe_bruto]))` | fct_ventas.importe_bruto; fct_ventas.comision; fct_ventas.costo_insumos; dim_canal.canal |
| KPI-03 | Porcentaje de merma por turno | Pollos sobrantes ÷ pollos preparados × 100, por turno | `Merma % = DIVIDE(SUM(fct_produccion[pollos_merma]), SUM(fct_produccion[pollos_preparados]))` | fct_produccion.pollos_merma; fct_produccion.pollos_preparados; dim_turno.turno |
| KPI-04 | Variación semanal del precio del pollo vivo | (Precio promedio de la semana − precio promedio de la semana anterior) ÷ precio promedio de la semana anterior × 100 | `Variación precio % = DIVIDE(AVERAGE(fct_produccion[precio_pollo_kg]) - CALCULATE(AVERAGE(fct_produccion[precio_pollo_kg]), DATEADD(dim_fecha[fecha], -7, DAY)), CALCULATE(AVERAGE(fct_produccion[precio_pollo_kg]), DATEADD(dim_fecha[fecha], -7, DAY)))` | fct_produccion.precio_pollo_kg; dim_fecha.fecha; dim_fecha.semana |

Tabla 2: Seguimiento de los KPI

| Código | Meta | Frecuencia | Objetivo | Decisión que apoya |
|---|---|---|---|---|
| KPI-01 | 98 % o más | Mensual | OE-01 | Aprobar los datos de cada mes antes de usarlos en el dashboard |
| KPI-02 | 12 % o más en cada canal | Mensual | OE-02 | Ajustar el precio de los combos en las apps de delivery |
| KPI-03 | 3 % o menos | Semanal | OE-03 | Definir cuántos pollos hornear por turno y día de la semana |
| KPI-04 | Alerta cuando sube más de 5 % | Semanal | OE-02 | Anticipar compras ante subidas del precio del pollo vivo |

**Lectura de los indicadores.** La calidad de datos mide el primer objetivo y es la condición para confiar en los demás; el margen neto por canal y la variación del precio del pollo miden el segundo, y el porcentaje de merma por turno, el tercero.
```

## Checklist
- [ ] Encabezado exacto en la primera línea y sin figura.
- [ ] Las dos tablas tienen los mismos códigos, en el mismo orden.
- [ ] Cada `OE` del brief tiene al menos un KPI y cada KPI responde a un `OE` del brief.
- [ ] Cada campo del origen y de la medida existe en el modelo de 2.4.
- [ ] Cada KPI tiene meta (o «Pendiente»), frecuencia y decisión.
- [ ] La cita de Parmenter (2015) está en `referencias.md`.
