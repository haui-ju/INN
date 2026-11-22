# Plantilla: Construcción del dashboard (`secciones/3.2.md`)

| | |
|---|---|
| **Entregable** | `secciones/3.2.md` |
| **Punto** | 3.2. Construcción del dashboard en Power BI (incluye imagen) |
| **Códigos** | `PAG-nn`; cita `KPI-nn` del modelo |
| **Entradas** | usuarios y decisiones del brief, `modelo.json` (KPI con su meta), `valores.json` y capturas que entrega el equipo |
| **Salida** | las páginas con su pregunta, usuario, visualizaciones y filtros; una captura por página; el valor real de cada KPI frente a su meta |

## Instrucciones para el agente
1. La primera línea es `## 3.2. Construcción del dashboard en Power BI`. Escribe esta sección **solo cuando el equipo entregó `valores.json` y una captura por página**; con las páginas y las medidas por escribir, entrega la especificación y detente.
2. Un párrafo que dice quién consulta el dashboard (los usuarios del brief), con qué herramienta se construyó y cuántas páginas tiene.
3. **Páginas.** Tabla `Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI`. Una fila por página `PAG-nn`. El usuario es uno de los del brief; el KPI es el código `KPI-nn` de `modelo.json` (varios separados por punto y coma). **Todo KPI del modelo aparece en una página.**
4. **Capturas.** Una línea `<!-- captura: pag-nn -->` por página, sola en su línea, con el mismo número de la página y en minúscula. El archivo `capturas/pag-nn.png` lo entrega el equipo.
5. **Valor real.** Tabla `Código | KPI | Valor real | Meta | Estado | Página`. El valor sale **solo** de `valores.json`, con los mismos decimales que muestra el dashboard; la meta es la de `modelo.json` (se copia tal cual); el estado es `Cumple`, `No cumple` o `Sin meta` (si el KPI no tiene meta). La página es la `PAG-nn` donde se ve el KPI.
6. **Lectura del dashboard.** Dos o tres frases: qué decisión apoya cada página y qué dicen los valores sobre ellas, sin cifras que no estén en la tabla.
7. **Metas pendientes.** Solo si algún KPI no tiene meta: nómbralo con su código, di que la meta se propone con su valor real y que se registra con `07-make-data-model-kpi-update`.
8. Cada tabla lleva antes una línea `Tabla N: título`. Sin comentarios ni notas: solo texto final y las marcas de captura.

## Formato

```markdown
## 3.2. Construcción del dashboard en Power BI

[Párrafo: quién lo consulta, con qué herramienta y cuántas páginas tiene.]

**Páginas.** [Frase que presenta la tabla.]

Tabla 1: Páginas del dashboard

| Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI |
|---|---|---|---|---|---|---|
| PAG-01 | [nombre] | [pregunta] | [usuario del brief] | [visuales] | [filtros] | KPI-01; KPI-02 |

<!-- captura: pag-01 -->

**Valor real de los KPI.** [Frase que presenta la tabla.]

Tabla 2: Valor real de cada KPI frente a su meta

| Código | KPI | Valor real | Meta | Estado | Página |
|---|---|---|---|---|---|
| KPI-01 | [nombre] | [valor de valores.json] | [meta de modelo.json] | [Cumple, No cumple o Sin meta] | PAG-01 |

**Lectura del dashboard.** [Qué decisión apoya cada página y qué dicen los valores.]

**Metas pendientes.** [Solo si hay KPI sin meta.]
```

## Ejemplo

```markdown
## 3.2. Construcción del dashboard en Power BI

El dashboard lo consultan el gerente general, que decide los precios y las compras, y el jefe de cocina, que decide la producción de cada turno. Se construyó en Power BI con cuatro páginas, una por cada pregunta que esas decisiones necesitan responder.

**Páginas.** Cada página responde una pregunta de negocio con sus visualizaciones y sus filtros, y muestra los KPI que la contestan.

Tabla 1: Páginas del dashboard

| Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI |
|---|---|---|---|---|---|---|
| PAG-01 | Calidad de datos | ¿Se puede confiar en las cifras antes de decidir? | Gerente general | Tarjeta del porcentaje de registros válidos y barras de registros por canal | Mes y canal | KPI-01 |
| PAG-02 | Margen por canal | ¿Qué canal deja más margen después de la comisión? | Gerente general | Tarjetas del margen neto y de la participación del canal directo, y barras del margen por canal | Mes, canal y local | KPI-02; KPI-04 |
| PAG-03 | Producción y merma | ¿Cuántos pollos se preparan de más en cada turno? | Jefe de cocina | Tarjeta del porcentaje de merma y columnas de merma por turno y día de la semana | Mes, turno y local | KPI-03 |
| PAG-04 | Precio del pollo vivo | ¿Cuánto cuesta el kilogramo de pollo vivo en la semana? | Gerente general | Tarjeta del precio promedio y línea del precio por semana | Mes | KPI-05 |

<!-- captura: pag-01 -->

<!-- captura: pag-02 -->

<!-- captura: pag-03 -->

<!-- captura: pag-04 -->

**Valor real de los KPI.** La tabla compara el valor que mostró el dashboard con la meta de cada indicador.

Tabla 2: Valor real de cada KPI frente a su meta

| Código | KPI | Valor real | Meta | Estado | Página |
|---|---|---|---|---|---|
| KPI-01 | Calidad de datos del ETL | 97,2 % | 98 % o más | No cumple | PAG-01 |
| KPI-02 | Margen neto por canal | 8,4 % | 12 % o más en el margen neto global | No cumple | PAG-02 |
| KPI-03 | Porcentaje de merma por turno | 6,9 % | 3 % o menos | No cumple | PAG-03 |
| KPI-04 | Participación del canal directo | 71,0 % | 70 % o más | Cumple | PAG-02 |
| KPI-05 | Precio promedio del pollo vivo por kilogramo | S/ 6,55 | Pendiente | Sin meta | PAG-04 |

**Lectura del dashboard.** La página de margen muestra que el canal directo cumple su participación, pero el margen neto sigue lejos de la meta; la de producción muestra una merma de más del doble de la meta, que el jefe de cocina puede atacar turno por turno. La calidad de datos queda cerca de la meta, de modo que las cifras de las demás páginas se pueden usar para decidir.

**Metas pendientes.** KPI-05 no tiene meta: se propone con su valor real y se registra con 07-make-data-model-kpi-update.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Cada KPI del modelo está en una página; cada página tiene usuario del brief, visualizaciones y filtros.
- [ ] Una línea `<!-- captura: pag-nn -->` por página y su archivo `capturas/pag-nn.png`.
- [ ] Todo valor de la tabla sale de `valores.json` y la meta es la de `modelo.json`.
- [ ] El estado concuerda con el valor y la meta (`Sin meta` solo si no hay meta).
- [ ] Hay «Lectura del dashboard» y, si falta alguna meta, «Metas pendientes».
- [ ] Cada tabla tiene su título `Tabla N: …`.
