# Plantilla: Modelo de datos (`secciones/2.4.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.4.md`, la figura `modelo-datos` y la parte del modelo de `modelo.json` |
| **Punto** | 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones |
| **Códigos** | `FCT-nn`, `DIM-nn`, `REL-nn` |
| **Entradas** | arquitectura de 2.2 (fuentes y salida del almacenamiento), objetivos e indicadores del brief, decisiones de 2.1, KPI que se van a medir (2.5) |
| **Salida** | las tablas de hechos con su granularidad, las dimensiones y las relaciones del modelo en estrella |

## Instrucciones para el agente
1. La primera línea es `## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones`.
2. Un párrafo con su cita (Kimball & Ross, 2013) que presenta el modelo en estrella y la marca `<!-- figura: modelo-datos -->` en una línea sola.
3. **Tablas de hechos.** Una frase y la tabla `Código | Tabla | Granularidad | Medidas | Claves`; medidas como `nombre (tipo, agregación)` y claves separadas por punto y coma.
4. **Dimensiones.** Una frase y la tabla `Código | Tabla | Clave | Atributos | Jerarquías`; jerarquías con `>` o «—». Incluye una dimensión de tiempo si algún KPI se mide por periodo.
5. **Relaciones.** Una frase y la tabla `Código | Desde | Hacia | Campos | Cardinalidad | Filtro`, con cardinalidad `N:1`, `1:1`, `1:N` o `N:N` y filtro `Único` o `Ambos`. Toda dimensión participa en una relación.
6. **Lectura del modelo.** Dos o tres frases: qué responde cada hecho, qué dimensiones comparten y que el diccionario completo va en el Anexo A con el capítulo 3.
7. Después de escribir 2.4 y 2.5: `python3 .claude/skills/_shared/diseno.py modelo --run <corrida>` y `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

[Párrafo que presenta el modelo, con su cita.]

<!-- figura: modelo-datos -->

**Tablas de hechos.** [Frase sobre los procesos que se miden.]

Tabla 1: Tablas de hechos

| Código | Tabla | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | fct_[proceso] | Una fila por [evento] | [medida] ([tipo], [agregación]); [medida] ([tipo], [agregación]) | id_[dimensión]; id_[dimensión] |

**Dimensiones.** [Frase sobre los ejes de análisis.]

Tabla 2: Dimensiones

| Código | Tabla | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | dim_fecha | id_fecha | fecha; semana; mes; anio | anio > mes > fecha |

**Relaciones.** [Frase sobre cómo se unen.]

Tabla 3: Relaciones del modelo

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | fct_[proceso] | dim_fecha | id_fecha | N:1 | Único |

**Lectura del modelo.** [Qué responde cada hecho y qué comparten.]
```

## Ejemplo

```markdown
## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

El modelo sigue el esquema en estrella del modelado dimensional: cada proceso del negocio se registra en una tabla de hechos con su granularidad y se analiza por dimensiones compartidas (Kimball & Ross, 2013). El modelo de Pollería Don Tito tiene tres tablas de hechos y seis dimensiones, como muestra la figura.

<!-- figura: modelo-datos -->

**Tablas de hechos.** Se miden tres procesos: la venta, la producción por turno y la carga de los datos, que permite medir su calidad.

Tabla 1: Tablas de hechos

| Código | Tabla | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | fct_ventas | Una fila por producto de cada ticket o pedido | cantidad (entero, suma); importe_bruto (moneda, suma); comision (moneda, suma); costo_insumos (moneda, suma) | id_fecha; id_producto; id_canal; id_local; id_turno |
| FCT-02 | fct_produccion | Una fila por local y turno de cada día | pollos_preparados (entero, suma); pollos_vendidos (entero, suma); pollos_merma (entero, suma); precio_pollo_kg (moneda, promedio) | id_fecha; id_local; id_turno |
| FCT-03 | fct_calidad | Una fila por fuente en cada carga del ETL | registros_leidos (entero, suma); registros_validos (entero, suma) | id_fecha; id_fuente |

**Dimensiones.** Las dimensiones son los ejes por los que la gerencia filtra y compara: el periodo, el producto, el canal, el local, el turno y la fuente de los datos.

Tabla 2: Dimensiones

| Código | Tabla | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | dim_fecha | id_fecha | fecha; dia_semana; semana; mes; anio | anio > mes > fecha |
| DIM-02 | dim_producto | id_producto | producto; categoria; precio_lista | categoria > producto |
| DIM-03 | dim_canal | id_canal | canal; tipo_canal; comision_pct | tipo_canal > canal |
| DIM-04 | dim_local | id_local | local; distrito | — |
| DIM-05 | dim_turno | id_turno | turno; hora_inicio; hora_fin | — |
| DIM-06 | dim_fuente | id_fuente | fuente; tipo_fuente | — |

**Relaciones.** Cada hecho se une a sus dimensiones por una clave, de muchos a uno y con filtro en un solo sentido, de la dimensión al hecho.

Tabla 3: Relaciones del modelo

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | fct_ventas | dim_fecha | id_fecha | N:1 | Único |
| REL-02 | fct_ventas | dim_producto | id_producto | N:1 | Único |
| REL-03 | fct_ventas | dim_canal | id_canal | N:1 | Único |
| REL-04 | fct_ventas | dim_local | id_local | N:1 | Único |
| REL-05 | fct_ventas | dim_turno | id_turno | N:1 | Único |
| REL-06 | fct_produccion | dim_fecha | id_fecha | N:1 | Único |
| REL-07 | fct_produccion | dim_local | id_local | N:1 | Único |
| REL-08 | fct_produccion | dim_turno | id_turno | N:1 | Único |
| REL-09 | fct_calidad | dim_fecha | id_fecha | N:1 | Único |
| REL-10 | fct_calidad | dim_fuente | id_fuente | N:1 | Único |

**Lectura del modelo.** Las ventas responden cuánto deja cada canal y la producción cuánto pollo se pierde por turno; ambas comparten la fecha, el local y el turno, de modo que la merma y el margen se pueden comparar en el mismo periodo. El diccionario completo de cada campo, con sus tipos y reglas de calidad, va en el Anexo A con la construcción del ETL.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: modelo-datos -->`.
- [ ] Cada hecho tiene granularidad, medidas con tipo y agregación, y claves.
- [ ] Cada dimensión tiene clave y atributos; jerarquías con atributos existentes o «—».
- [ ] Hay dimensión de tiempo si algún KPI se mide por periodo.
- [ ] Cada relación une tablas y campos existentes, con cardinalidad y filtro; ninguna dimensión queda suelta.
- [ ] La cita de Kimball y Ross (2013) está en `referencias.md`.
