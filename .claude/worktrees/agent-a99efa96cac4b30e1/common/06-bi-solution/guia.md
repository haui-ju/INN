# Playbook de la solución de BI (secciones 2.1 a 2.3)

Guía para que un agente redacte la primera parte del capítulo 2 del informe de BI (`common/structure/model1.md`): la propuesta de solución, la arquitectura de Inteligencia de Negocios por capas y las herramientas seleccionadas. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `06-make-bi-solution` (y lo ajusta `06-make-bi-solution-update`). Escribe en `project/06-bi-solution/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica («Diseño técnico de solución en Inteligencia de Negocios») pide una arquitectura de BI clara y herramientas bien seleccionadas y sustentadas; el modelo de datos y los KPI se diseñan después con `07-make-data-model-kpi`.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): usuarios, decisiones que apoyará el dashboard, fuentes de datos previstas (`FUE-nn`), herramientas previstas del alcance y objetivos `OE-nn`.
2. La corrida vigente de `05-make-problem-objectives` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 05-make-problem-objectives`): enunciado de la problemática y causas principales (`CAU-nn`), y la matriz de articulación.
3. El config (`modo_datos`, `tipo`) y, si hace falta contexto, la corrida vigente de `04-make-strategic-analysis` (estrategias FODA que la solución hace posibles).

Si falta la corrida de `05`, avisa, indica ejecutarla y pregunta si continúa solo con el brief: entonces la respuesta a la problemática se apoya en el problema principal del brief y no cita causas.

### 0.2 Preguntar y confirmar
Pregunta solo lo que falta: si la herramienta de ETL y la de almacenamiento ya están decididas (si no, quedan «Pendiente»), si existe alguna fuente de datos que el brief no prevé y qué páginas espera ver la gerencia. Muestra un plan (decisiones y usuarios, una fila por `OE` con sus componentes, los componentes por capa y las herramientas) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/2.1.md`, `2.2.md` y `2.3.md`: la primera línea es el encabezado exacto (`## 2.1. Propuesta de solución en BI`, `## 2.2. Arquitectura de Inteligencia de Negocios`, `## 2.3. Herramientas utilizadas`); después, solo texto final (prosa académica y tablas), sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- 2.2 marca su figura en una línea sola: `<!-- figura: arquitectura-bi -->`. El HTML queda en `visuales/` y su explicación en `leer-imagen/`; los escribe `visuales.py construir --visual arquitectura-bi --run <corrida>` (lee 2.2 y 2.3). 2.1 y 2.3 no llevan figura.
- `referencias.md` (una referencia por línea, APA 7) si se cita algo, y `README.md` (procedencia; único archivo que puede decir que un dato es generado).
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada sección); `12-make-report` renumera las tablas en todo el informe.

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `CAP-nn` | Componente de la arquitectura (una caja de la figura) | Primera celda de la tabla de 2.2 |
| `HER-nn` | Herramienta seleccionada | Primera celda de la tabla de 2.3 |
| `OE-nn`, `FUE-nn` | Objetivo específico y fuente de datos | Se reutilizan del brief, sin renumerar |
| `CAU-nn` | Causa principal | Se reutiliza de 1.8 (corrida de `05`) |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un componente o una herramienta. `07-make-data-model-kpi` lee la arquitectura para decidir las tablas del modelo.

### 0.5 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. La arquitectura cita su marco una vez (Kimball & Ross, 2013) y cada cita va en `referencias.md`.

### 0.6 Trazabilidad (lo que la rúbrica revisa)
- **Objetivo → componente:** cada `OE` del brief tiene su fila en la tabla de 2.1 con los `CAP` que lo atienden.
- **Fuente del brief → capa de fuentes:** cada `FUE` del brief aparece en un componente de la capa de fuentes. Si la solución necesita una fuente que el brief no prevé (por ejemplo, el control de producción para medir la merma), se incluye como componente con su descripción y se recomienda al usuario agregarla al brief con `01-make-project-brief-update`.
- **Componente → herramienta:** cada capa de ETL, almacenamiento y visualización tiene al menos una herramienta en 2.3.
- **Arquitectura → modelo:** la salida del almacenamiento son las tablas de hechos y dimensiones que define 2.4.

---

## 1. Propuesta de solución en BI (2.1)

- Un párrafo que presenta la solución: qué integra, para quién y con qué resultado.
- **Decisiones que apoya.** Viñetas con las decisiones del brief (sección 5), concretas y con su verbo («Ajustar el precio de los combos en las apps de delivery»).
- **Usuarios.** Quién usará el dashboard y quién decide (del brief).
- **Respuesta a la problemática.** Dos o tres frases: cómo la solución ataca el problema central y sus causas principales (`CAU-nn` de 1.8).
- La tabla `Objetivo | Componentes | Cómo lo atiende`, con **una fila por cada `OE` del brief**: los `CAP` que lo atienden (al menos uno) y una frase con el resultado que lo hace posible.

## 2. Arquitectura de BI (2.2)

Una arquitectura de BI tiene **cuatro capas, en este orden**:

| Capa | Qué hace | Ejemplos de componentes |
|---|---|---|
| Fuentes | Origen de los datos: sistemas, archivos, portales abiertos y registros internos | sistema de caja, reportes de aplicaciones, portal de precios |
| ETL | Extracción, transformación (limpieza, reglas de calidad, integración, cálculo de campos) y carga | flujo de limpieza e integración |
| Almacenamiento | Repositorio de las tablas depuradas del modelo dimensional | base de datos, carpeta de archivos depurados, modelo importado |
| Visualización | Modelo semántico, medidas y dashboard | modelo y dashboard en Power BI |

- Un párrafo con su cita (Kimball & Ross, 2013), la marca de figura y la tabla `Código | Capa | Componente | Función | Entrada | Salida`, ordenada por capa.
- **Capa**: exactamente Fuentes, ETL, Almacenamiento o Visualización. Cada capa tiene al menos un componente.
- **Componente**: un nombre corto. En la capa de fuentes, el nombre de la fuente con su código del brief (`Sistema de caja de los locales (FUE-01)`).
- **Función**, **Entrada** y **Salida**: qué hace el componente, qué recibe (otros `CAP` o datos de la empresa) y qué entrega. La salida del almacenamiento son las tablas del modelo; la de la visualización, el dashboard para los usuarios.
- Cierra con **Flujo de los datos.**: dos o tres frases que recorren la figura de izquierda a derecha y dicen con qué frecuencia se actualiza.

## 3. Herramientas utilizadas (2.3)

- Un párrafo con los criterios de selección (costo, curva de aprendizaje, compatibilidad con las fuentes y con Power BI, consigna del curso).
- La tabla `Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada`, con al menos una herramienta para ETL, almacenamiento y visualización.
- **Power BI** (Desktop) es obligatorio en la capa de visualización por la consigna del curso.
- **Justificación**: por qué esta herramienta y no otra, con criterios del proyecto. **Alternativa descartada**: la opción que se evaluó y por qué no se eligió.
- **Herramientas pendientes.** Mientras el usuario no decida cómo se construirá el capítulo 3, la herramienta de ETL y la de almacenamiento quedan así: **Herramienta** «Pendiente», **Justificación** «Pendiente: se decide con la construcción del capítulo 3» y **Alternativa descartada** «—». Se completan con `06-make-bi-solution-update` antes de entregar. Ninguna otra capa admite «Pendiente».
- Cierra con una frase que recuerde qué herramientas faltan decidir, si las hay.

---

## 4. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/bi_solution.py`: encabezados, la figura de 2.2 y su explicación, códigos `CAP` y `HER` citados sin definir o repetidos, decisiones, usuarios y respuesta a la problemática, una fila por cada `OE` del brief con componentes existentes, causas que existen en 1.8, las cuatro capas presentes y en orden, cada `FUE` del brief en la capa de fuentes, función, entrada y salida de cada componente, herramientas con justificación y alternativa (o «Pendiente» solo en ETL y almacenamiento), Power BI en visualización y citas con su referencia.

## 5. Errores frecuentes y checklist

**Errores:** una propuesta que repite el objetivo general sin decir qué decisiones apoya; capas mezcladas (un dashboard en la capa de almacenamiento); una fuente del brief que no aparece en la arquitectura; herramientas listadas sin justificación o sin alternativa; elegir por el usuario la herramienta de ETL que aún no decidió; dibujar la figura a mano en vez de construirla con `visuales.py`.

**Checklist:**
- [ ] Cada sección empieza con su encabezado exacto; 2.2 marca su figura.
- [ ] Las decisiones y los usuarios son los del brief; cada `OE` tiene su fila con componentes.
- [ ] Cuatro capas en orden, cada una con al menos un componente con función, entrada y salida.
- [ ] Cada `FUE` del brief está en la capa de fuentes.
- [ ] Cada herramienta tiene capa, función, justificación y alternativa, o es «Pendiente» en ETL o almacenamiento.
- [ ] Power BI está en la capa de visualización.
- [ ] Visual `arquitectura-bi` construido con `--run`; la procedencia está solo en `README.md`.
- [ ] El usuario confirmó el plan antes de escribir.

---

## Referencias

Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). John Wiley & Sons.

Microsoft. (2026). *Power BI Desktop* [Software].

*(Formato APA 7, ver `common/citation-style/APA7.md`. Solo lo que se cita en la corrida va a su `referencias.md`.)*
