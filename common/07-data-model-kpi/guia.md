# Playbook del modelo de datos y los KPI (secciones 2.4 y 2.5)

Guía para que un agente diseñe el modelo dimensional y los indicadores del capítulo 2 del informe de BI (`common/structure/model1.md`): tablas de hechos, dimensiones, relaciones y los KPI que miden cada objetivo. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `07-make-data-model-kpi` (y lo ajusta `07-make-data-model-kpi-update`). Escribe en `project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide un modelo de datos con hechos, dimensiones y relaciones bien definidos y KPI justificados y articulados a los objetivos. Deja además `modelo.json`, que leerán las skills del capítulo 3 (ETL y dashboard).

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): objetivos `OE-nn` con su métrica, meta e **indicador**, y las fuentes `FUE-nn` con los datos que traen.
2. La corrida vigente de `06-make-bi-solution` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution`): componentes de la arquitectura, fuentes y almacenamiento.
3. La corrida vigente de `05-make-problem-objectives`: matriz de articulación (qué causas mide cada objetivo).
4. El config (`rubro`) y `project/domain.md` para los nombres del dominio (canales, turnos, locales, productos).

### 0.2 Preguntar y confirmar
Pregunta solo lo que falta: el grano de los hechos si el brief no lo deja claro, las metas de los KPI que el brief no fija y la frecuencia con que la gerencia revisa cada indicador. Muestra un plan (hechos con su granularidad, dimensiones, relaciones y una fila por KPI con su objetivo) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/2.4.md` y `2.5.md`: la primera línea es el encabezado exacto (`## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones` y `## 2.5. Indicadores clave de rendimiento`); después, solo texto final del informe, sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- La sección 2.4 marca su figura en una línea sola: `<!-- figura: modelo-datos -->`. El HTML queda en `visuales/` y su explicación en `leer-imagen/`; los escribe `visuales.py construir --visual modelo-datos --run <corrida>` a partir de `modelo.json`. 2.5 no lleva figura.
- `modelo.json`: el mismo modelo y los mismos KPI en datos (ver 0.5). Las secciones en Markdown son la fuente de verdad del texto y el archivo debe coincidir con ellas.
- `referencias.md` si se cita (por ejemplo, Kimball y Ross, 2013) y `README.md` con la procedencia.
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada sección).

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `FCT-nn` | Tabla de hechos | Primera celda de la tabla de hechos de 2.4 |
| `DIM-nn` | Dimensión | Primera celda de la tabla de dimensiones de 2.4 |
| `REL-nn` | Relación hecho-dimensión | Primera celda de la tabla de relaciones de 2.4 |
| `KPI-nn` | Indicador clave | Primera celda de las tablas de 2.5 |
| `OE-nn`, `FUE-nn` | Objetivo y fuente del brief | Brief (se citan, no se vuelven a definir) |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un ítem.

### 0.5 `modelo.json`
```json
{
  "schema": 1,
  "hechos": [{"codigo": "FCT-01", "nombre": "fPedidos", "granularidad": "…", "medidas": [{"nombre": "venta_bruta", "tipo": "decimal", "agregacion": "suma"}], "claves": ["fecha_key"]}],
  "dimensiones": [{"codigo": "DIM-01", "nombre": "dCalendario", "clave": "fecha_key", "atributos": ["fecha", "anio"], "jerarquias": ["Año > Mes > Día"]}],
  "relaciones": [{"codigo": "REL-01", "desde": "fPedidos", "hacia": "dCalendario", "campos": "fecha_key", "cardinalidad": "*:1", "filtro": "Simple"}],
  "kpis": [{"codigo": "KPI-01", "nombre": "…", "formula": "…", "medida": "…", "origen": ["fPedidos.venta_bruta"], "meta": "…", "frecuencia": "Mensual", "objetivo": "OE-02", "decision": "…"}]
}
```
`tipo` de una medida es `entero` o `decimal`. Todo lo demás repite lo escrito en las secciones: mismos códigos, nombres, medidas, claves, atributos, relaciones y KPI.

### 0.6 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Lo desconocido (por ejemplo, una meta que la gerencia aún no fija) dice «Pendiente». Cada cita en texto lleva su referencia en `referencias.md`.

---

## 1. Modelo de datos (2.4)

### 1.1 Estrella por defecto
Una **estrella** con uno o más hechos y dimensiones compartidas. Un copo de nieve se acepta si se justifica en el párrafo inicial. Nombres: `f<Nombre>` para hechos y `d<Nombre>` para dimensiones, en singular o plural coherente y sin tildes ni espacios (como se verán en Power BI); los campos van en minúsculas con guion bajo.

### 1.2 Hechos
- **Granularidad:** qué representa una fila («una fila por línea de pedido, canal y día»). Todas las medidas de la tabla deben ser válidas a ese grano.
- **Medidas** con su agregación (`suma`, `promedio`, `conteo`, `conteo distinto`, `mínimo` o `máximo`), escritas `nombre (agregación)` y separadas por punto y coma. Se prefieren medidas aditivas; un porcentaje no es una medida del hecho, es un KPI calculado.
- **Claves:** una por cada dimensión a la que apunta, con el mismo nombre que la clave de la dimensión.

### 1.3 Dimensiones
- Cada dimensión tiene **clave**, **atributos** (los campos por los que se filtra o agrupa) y, si existen, **jerarquías** escritas `Nivel > Nivel`.
- **Dimensión de tiempo obligatoria** cuando algún KPI tiene frecuencia diaria, semanal, mensual, trimestral o anual: `dCalendario` con fecha, año, mes, día de la semana y, si el rubro lo usa, feriado.
- Dimensiones habituales por rubro: producto, canal, local o zona, turno, cliente (anonimizado).

### 1.4 Relaciones
Una fila por relación hecho-dimensión con los campos que la unen, la **cardinalidad** (`*:1` de varios a uno es la normal; `1:1`, `1:*` y `*:*` solo si se justifica) y la **dirección de filtro** (`Simple`, de la dimensión al hecho, o `Ambos`). **Toda dimensión participa en al menos una relación** y toda relación cita tablas que existen en el modelo.

### 1.5 Figura
La marca `<!-- figura: modelo-datos -->` va después del párrafo inicial. La figura muestra las dimensiones, los hechos con su granularidad y las relaciones con su cardinalidad.

## 2. KPI (2.5)

Cada KPI tiene dos tablas:
- **Definición:** `Código | KPI | Fórmula | Medida propuesta | Origen`. La fórmula va en palabras; la medida propuesta es un nombre de medida DAX (la definitiva va en el anexo del capítulo 3); el origen son campos del modelo escritos `tabla.campo`, separados por punto y coma.
- **Gestión:** `Código | Meta | Frecuencia | Objetivo | Decisión que apoya`. La meta lleva cifra y comparador («12 % o más») o «Pendiente»; la frecuencia es Diaria, Semanal, Mensual, Trimestral, Anual o «Por carga»; el objetivo es el `OE-nn` al que responde; la decisión es una de las del brief.

**Reglas:** cada `OE` del brief tiene al menos un KPI; el KPI del indicador del objetivo usa el mismo nombre que el indicador del brief; todo campo de origen existe en el modelo.

## 3. Errores frecuentes
- Un hecho sin granularidad o con medidas que no son válidas a su grano.
- Dimensiones sueltas o relaciones que citan tablas que no existen.
- KPI que usan campos que el modelo no tiene.
- Metas sin cifra y sin «Pendiente».
- KPI sin objetivo o con objetivos que el brief no tiene.
- `modelo.json` que no se actualizó al cambiar las secciones.

## 4. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/data_model_kpi.py`: encabezados, al menos un hecho con granularidad y medidas con agregación, dimensiones con clave y atributos, dimensión de tiempo si hay KPI por periodo, relaciones a tablas existentes y sin dimensiones sueltas, cada `OE` del brief con KPI, campos de origen dentro del modelo, meta o «Pendiente», `modelo.json` igual a las secciones, la figura marcada y construida y las citas con su referencia.
