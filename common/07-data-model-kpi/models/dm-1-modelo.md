# Plantilla: Diseño del modelado de datos (`secciones/2.4.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.4.md` y la figura `modelo-datos` |
| **Punto** | 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones |
| **Códigos** | `FCT-nn`, `DIM-nn`, `REL-nn` |
| **Entradas** | fuentes y objetivos del brief, arquitectura de `06-make-bi-solution`, dominio del negocio |
| **Salida** | el modelo en estrella con sus hechos, dimensiones y relaciones, y su figura |

## Instrucciones para el agente
1. La primera línea es `## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones`.
2. Un párrafo que justifica el esquema en estrella con su cita (Kimball y Ross, 2013) y resume cuántos hechos y dimensiones tiene.
3. La marca `<!-- figura: modelo-datos -->` en una línea sola.
4. **Tablas de hechos.** Tabla `Código | Tabla de hechos | Granularidad | Medidas | Claves`: una fila por hecho, con su granularidad («una fila por …»), sus medidas escritas `nombre (agregación)` separadas por punto y coma y sus claves hacia las dimensiones.
5. **Dimensiones.** Tabla `Código | Dimensión | Clave | Atributos | Jerarquías` con la clave, los atributos separados por punto y coma y las jerarquías `Nivel > Nivel` (o «—»). Incluye una dimensión de tiempo si algún KPI se mide por periodo.
6. **Relaciones.** Tabla `Código | Desde | Hacia | Campos | Cardinalidad | Filtro`: una fila por relación hecho-dimensión, con nombres de tablas que existen, el campo que las une, la cardinalidad (`*:1`) y la dirección del filtro (`Simple` o `Ambos`). Toda dimensión aparece en alguna relación.
7. **Lectura del modelo.** Una o dos frases: qué preguntas del negocio permite responder el modelo.
8. Escribe `modelo.json` con el mismo contenido (ver el playbook) y construye la figura: `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

[Párrafo que justifica el esquema en estrella, con su cita.]

<!-- figura: modelo-datos -->

**Tablas de hechos.** [Frase que presenta los hechos.]

Tabla 1: Tablas de hechos

| Código | Tabla de hechos | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | f[Nombre] | Una fila por [grano] | [medida] (suma); [medida] (promedio) | [clave]_key; [clave]_key |

**Dimensiones.** [Frase que presenta las dimensiones.]

Tabla 2: Dimensiones

| Código | Dimensión | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | d[Nombre] | [clave]_key | [atributo]; [atributo] | [Nivel > Nivel] o — |

**Relaciones.** [Frase que presenta las relaciones.]

Tabla 3: Relaciones del modelo

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | f[Nombre] | d[Nombre] | [clave]_key | *:1 | Simple |

**Lectura del modelo.** [Qué preguntas permite responder.]
```

## Ejemplo

```markdown
## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

El modelo sigue un esquema en estrella, en el que las tablas de hechos guardan lo que se mide y las dimensiones describen por qué ejes se analiza (Kimball & Ross, 2013). Tiene tres tablas de hechos y cinco dimensiones compartidas, de modo que las ventas, la producción y el precio del insumo se pueden cruzar por fecha, local y turno.

<!-- figura: modelo-datos -->

**Tablas de hechos.** Cada hecho tiene un grano propio y sus medidas se suman o promedian a ese nivel.

Tabla 1: Tablas de hechos

| Código | Tabla de hechos | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | fPedidos | Una fila por línea de pedido, canal y día | cantidad (suma); venta_bruta (suma); comision (suma); costo_estimado (suma); pollos_equivalentes (suma); registro_valido (suma) | fecha_key; producto_key; canal_key; local_key; turno_key |
| FCT-02 | fProduccion | Una fila por local, turno y día | pollos_preparados (suma); pollos_vendidos (suma); pollos_merma (suma) | fecha_key; local_key; turno_key |
| FCT-03 | fPrecioInsumo | Una fila por día | precio_kg (promedio) | fecha_key |

**Dimensiones.** Las dimensiones se comparten entre los hechos para que los filtros de una página afecten a todos los visuales.

Tabla 2: Dimensiones

| Código | Dimensión | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | dCalendario | fecha_key | fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Año > Mes > Fecha |
| DIM-02 | dProducto | producto_key | producto; categoria | Categoría > Producto |
| DIM-03 | dCanal | canal_key | canal; tipo_canal; comision_pct | — |
| DIM-04 | dLocal | local_key | local; zona | — |
| DIM-05 | dTurno | turno_key | turno; hora_inicio; hora_fin | — |

**Relaciones.** Todas las relaciones son de varios a uno, desde el hecho hacia la dimensión, y filtran en un solo sentido.

Tabla 3: Relaciones del modelo

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | fPedidos | dCalendario | fecha_key | *:1 | Simple |
| REL-02 | fPedidos | dProducto | producto_key | *:1 | Simple |
| REL-03 | fPedidos | dCanal | canal_key | *:1 | Simple |
| REL-04 | fPedidos | dLocal | local_key | *:1 | Simple |
| REL-05 | fPedidos | dTurno | turno_key | *:1 | Simple |
| REL-06 | fProduccion | dCalendario | fecha_key | *:1 | Simple |
| REL-07 | fProduccion | dLocal | local_key | *:1 | Simple |
| REL-08 | fProduccion | dTurno | turno_key | *:1 | Simple |
| REL-09 | fPrecioInsumo | dCalendario | fecha_key | *:1 | Simple |

**Lectura del modelo.** Con este modelo se puede calcular el margen de cada canal por mes, comparar lo preparado con lo vendido en cada turno y contrastar el precio del pollo vivo con el margen del mismo periodo.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: modelo-datos -->` una sola vez.
- [ ] Cada hecho declara su granularidad y sus medidas con agregación.
- [ ] Hay una dimensión de tiempo si algún KPI se mide por periodo.
- [ ] Toda dimensión aparece en alguna relación y toda relación cita tablas que existen.
- [ ] `modelo.json` repite el mismo modelo y la figura está construida con `visuales.py construir`.
