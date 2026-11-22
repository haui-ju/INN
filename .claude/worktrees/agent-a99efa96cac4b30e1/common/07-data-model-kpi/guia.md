# Playbook del modelo de datos y los KPI (secciones 2.4 y 2.5)

Guía para que un agente redacte la segunda parte del capítulo 2 del informe de BI (`common/structure/model1.md`): el modelo de datos dimensional (hechos, dimensiones y relaciones) y los indicadores clave de rendimiento. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `07-make-data-model-kpi` (y lo ajusta `07-make-data-model-kpi-update`). Escribe en `project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide un modelo de datos con hechos, dimensiones y relaciones correctos y KPI justificados; el capítulo 3 (ETL y dashboard) construye exactamente este modelo, que lee de `modelo.json`.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): objetivos `OE-nn` con su indicador y su meta, decisiones que apoyará el dashboard y fuentes previstas (`FUE-nn`).
2. La corrida vigente de `06-make-bi-solution` (`python3 .claude/skills/_shared/diseno.py leer --paso 06-make-bi-solution`): componentes de la arquitectura, fuentes y herramientas.
3. La corrida vigente de `05-make-problem-objectives` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 05-make-problem-objectives`): problemática, causas principales y matriz de articulación.

Si falta la corrida de `06`, avisa y pregunta si continúa solo con las fuentes del brief. Si falta la de `05`, avisa e indica ejecutarla; los KPI se trazan igual con los objetivos del brief.

### 0.2 Preguntar y confirmar
Pregunta solo lo que falta: qué representa una venta en los registros (ticket, pedido, línea de producto), qué atributos necesita filtrar la gerencia (canal, local, turno, producto, periodo) y la meta de cada KPI si el brief no la fija. Muestra un plan (hechos con su granularidad, dimensiones, relaciones y una fila por KPI con su objetivo) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report` y el capítulo 3)
- `secciones/2.4.md` y `2.5.md`: la primera línea es el encabezado exacto (`## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones` y `## 2.5. Indicadores clave de rendimiento`); después, solo texto final (prosa académica y tablas), sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- 2.4 marca su figura en una línea sola: `<!-- figura: modelo-datos -->`. La construye `visuales.py construir --visual modelo-datos --run <corrida>` a partir de `modelo.json`. 2.5 no lleva figura.
- `modelo.json`: el modelo y los KPI legibles por máquina, **escritos desde las secciones** con `python3 .claude/skills/_shared/diseno.py modelo --run <corrida>`. Nunca se edita a mano: se cambia la sección y se vuelve a escribir.
- `referencias.md` (una referencia por línea, APA 7) si se cita algo, y `README.md` (procedencia; único archivo que puede decir que un dato es generado).
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada sección).

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `FCT-nn` | Tabla de hechos | Primera celda de la tabla de hechos de 2.4 |
| `DIM-nn` | Dimensión | Primera celda de la tabla de dimensiones de 2.4 |
| `REL-nn` | Relación entre un hecho y una dimensión | Primera celda de la tabla de relaciones de 2.4 |
| `KPI-nn` | Indicador clave de rendimiento | Primera celda de las tablas de 2.5 |
| `OE-nn` | Objetivo específico | Se reutiliza del brief |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un elemento. Los nombres de las tablas van en minúsculas y sin espacios, con prefijo `fct_` o `dim_` (`fct_ventas`, `dim_fecha`); los campos, igual (`importe_bruto`). Así los usa el capítulo 3 en el ETL y en las medidas DAX.

### 0.5 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. El modelo cita su marco una vez (Kimball & Ross, 2013) y los KPI el suyo si lo usan (Parmenter, 2015); cada cita va en `referencias.md`.

---

## 1. Modelo de datos (2.4)

### 1.1 Estrella por defecto
El modelo es una **estrella**: una o pocas tablas de hechos en el centro y dimensiones conformadas alrededor (tiempo, producto, canal, local, cliente, turno, según el rubro). Un copo de nieve (una dimensión que se relaciona con otra) solo se acepta si se justifica en la lectura del modelo. Una tabla de hechos de auditoría de las cargas (registros leídos y válidos por fuente) es la forma de medir la calidad de datos que pide la rúbrica.

### 1.2 Tablas de hechos
Tabla `Código | Tabla | Granularidad | Medidas | Claves`:
- **Granularidad**: qué representa **una fila** («Una fila por producto de cada ticket o pedido»). Se decide antes que las medidas y no se mezclan granos en una misma tabla.
- **Medidas**: `nombre (tipo, agregación)` separadas por punto y coma. Tipo: entero, decimal, moneda o porcentaje. Agregación: suma, promedio, conteo, conteo distinto, mínimo o máximo. Las medidas aditivas (importes, cantidades) se suman; los precios y porcentajes no se suman (promedio o se recalculan).
- **Claves**: las claves foráneas hacia sus dimensiones, separadas por punto y coma.

### 1.3 Dimensiones
Tabla `Código | Tabla | Clave | Atributos | Jerarquías`:
- **Clave**: la clave primaria (`id_fecha`). **Atributos**: separados por punto y coma; son los campos por los que se filtra o se agrupa.
- **Jerarquías**: niveles de lo general a lo particular con `>` (`anio > mes > fecha`), usando nombres de atributos; varias, separadas por punto y coma; «—» si no hay.
- **Dimensión de tiempo obligatoria** si algún KPI se mide por periodo (diario, semanal, mensual…): una tabla cuyo nombre incluye `fecha`, `tiempo` o `calendario`, con fecha, semana, mes y año.

### 1.4 Relaciones
Tabla `Código | Desde | Hacia | Campos | Cardinalidad | Filtro`:
- **Desde**: la tabla de hechos (o la dimensión hija en un copo de nieve). **Hacia**: la dimensión. Ambas por su nombre, como en las tablas anteriores.
- **Campos**: el campo que las une; debe existir en las dos tablas (clave foránea en el hecho y clave primaria en la dimensión).
- **Cardinalidad**: `N:1` (muchos a uno, lo normal de un hecho a su dimensión), `1:1`, `1:N` o `N:N`. **Filtro**: `Único` (la dimensión filtra al hecho; es la opción recomendada) o `Ambos` (solo si se justifica, porque puede volver ambiguo el modelo).
- Toda dimensión participa en al menos una relación y todo hecho se relaciona con al menos una dimensión.

Cierra con **Lectura del modelo.**: dos o tres frases sobre qué responde cada hecho, qué dimensiones comparten y dónde estará el diccionario completo (Anexo A, con el capítulo 3).

## 2. KPI (2.5)

Un KPI es una medida que dice si un objetivo avanza y orienta una decisión (Parmenter, 2015). Se formula en dos tablas:

- **Definición:** `Código | KPI | Fórmula | Medida propuesta | Origen`.
  - **Fórmula**: en palabras, con sus operaciones («Pollos sobrantes ÷ pollos preparados × 100, por turno»).
  - **Medida propuesta**: la medida DAX que se propone, entre comillas invertidas; usa los campos del modelo como `tabla[campo]`. La versión final va al Anexo C con el capítulo 3.
  - **Origen**: los campos que usa, como `tabla.campo` separados por punto y coma; todos deben existir en 2.4.
- **Seguimiento:** `Código | Meta | Frecuencia | Objetivo | Decisión que apoya`.
  - **Meta**: con cifra y sentido («3 % o menos»), coherente con la meta del objetivo en el brief; «Pendiente» si el usuario aún no la fija.
  - **Frecuencia**: Diaria, Semanal, Quincenal, Mensual, Trimestral, Semestral, Anual o Por carga.
  - **Objetivo**: el `OE-nn` del brief al que responde. **Cada `OE` del brief tiene al menos un KPI.**
  - **Decisión que apoya**: una de las decisiones del brief o de 2.1.
- El KPI que mide un objetivo repite el nombre de su indicador en el brief, para que la trazabilidad se lea sin códigos.

Cierra con **Lectura de los indicadores.**: una o dos frases que digan qué KPI responde a cada objetivo.

## 3. `modelo.json`

Lo escribe `diseno.py modelo --run <corrida>` desde 2.4 y 2.5. Esquema:

```json
{"schema": 1,
 "hechos": [{"codigo": "FCT-01", "nombre": "fct_…", "granularidad": "…", "medidas": [{"nombre": "…", "tipo": "…", "agregacion": "…"}], "claves": ["id_…"]}],
 "dimensiones": [{"codigo": "DIM-01", "nombre": "dim_…", "clave": "id_…", "atributos": ["…"], "jerarquias": [["…", "…"]]}],
 "relaciones": [{"codigo": "REL-01", "desde": "fct_…", "hacia": "dim_…", "campos": ["id_…"], "cardinalidad": "N:1", "filtro": "Único"}],
 "kpis": [{"codigo": "KPI-01", "nombre": "…", "formula": "…", "medida": "…", "origen": ["tabla.campo"], "meta": "…", "frecuencia": "…", "objetivo": "OE-01", "decision": "…"}]}
```

La validación compara `modelo.json` con las secciones y avisa cualquier diferencia: si se editó una sección, se vuelve a escribir.

---

## 4. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/data_model_kpi.py`: encabezados, la figura de 2.4 y su explicación, códigos citados sin definir o repetidos, granularidad, medidas con tipo y agregación y claves de cada hecho, clave y atributos de cada dimensión, jerarquías con atributos existentes, dimensión de tiempo si algún KPI tiene frecuencia periódica, relaciones con tablas y campos existentes, cardinalidad y filtro válidos, dimensiones y hechos sin relación, campos completos de cada KPI, cada `OE` del brief con su KPI, campos de origen y de la medida que existen en el modelo, meta o «Pendiente», `modelo.json` igual a las secciones y citas con su referencia.

## 5. Errores frecuentes y checklist

**Errores:** un hecho sin granularidad o con granos mezclados; sumar precios o porcentajes; dimensiones sin relación; relaciones de varios a varios o con filtro en ambos sentidos sin justificar; un KPI sin meta o sin objetivo; KPI que usan campos que el modelo no tiene; editar `modelo.json` a mano; escribir la medida DAX final aquí en lugar del Anexo C.

**Checklist:**
- [ ] Cada sección empieza con su encabezado exacto; 2.4 marca su figura.
- [ ] Cada hecho tiene granularidad, medidas con tipo y agregación, y claves.
- [ ] Cada dimensión tiene clave y atributos; hay dimensión de tiempo si algún KPI es periódico.
- [ ] Cada relación une tablas y campos existentes, con cardinalidad y filtro; ninguna dimensión queda suelta.
- [ ] Cada `OE` del brief tiene al menos un KPI; cada KPI tiene fórmula, medida, origen, meta, frecuencia y decisión.
- [ ] `modelo.json` escrito con `diseno.py modelo` y figura `modelo-datos` construida con `--run`.
- [ ] La procedencia está solo en `README.md`; el usuario confirmó el plan.

---

## Referencias

Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). John Wiley & Sons.

Parmenter, D. (2015). *Key performance indicators: Developing, implementing, and using winning KPIs* (3.ª ed.). John Wiley & Sons.

*(Formato APA 7, ver `common/citation-style/APA7.md`. Solo lo que se cita en la corrida va a su `referencias.md`.)*
