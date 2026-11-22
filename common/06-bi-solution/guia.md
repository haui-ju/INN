# Playbook de la solución de BI (secciones 2.1 a 2.3)

Guía para que un agente redacte el diseño técnico de la solución del capítulo 2 del informe de BI (`common/structure/model1.md`): la propuesta de solución, la arquitectura por capas con su figura y las herramientas seleccionadas y sustentadas. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `06-make-bi-solution` (y lo ajusta `06-make-bi-solution-update`). Escribe en `project/06-bi-solution/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide una arquitectura de BI clara, herramientas seleccionadas y sustentadas y una solución articulada a los objetivos del proyecto.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): usuarios, decisiones que apoyará el dashboard, fuentes de datos previstas (`FUE-nn`), objetivos (`OG-01`, `OE-nn`) y herramientas previstas en el alcance.
2. La corrida vigente de `05-make-problem-objectives` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 05-make-problem-objectives`): problemática central, causas principales y la matriz de articulación.
3. El config (`rubro`, `tipo`, `modo_datos`) y `project/domain.md` (empresa y contexto).
4. Fuentes externas para sustentar herramientas o el marco de capas (documentación oficial, textos de referencia). **Ninguna afirmación técnica de una herramienta se escribe sin saber que es cierta**; si no se puede verificar, se formula sin cifra.

### 0.2 Preguntar y confirmar
Pregunta solo lo que el brief no trae: qué herramienta usará el equipo para el ETL y para el almacenamiento (o si todavía no se decide), si hay una herramienta ya impuesta y dónde se publicará el dashboard. Muestra un plan (decisiones y usuarios, una fila por objetivo con su componente, los componentes por capa y las herramientas con su alternativa) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/2.1.md`, `2.2.md` y `2.3.md`: la primera línea es el encabezado exacto (`## 2.1. Propuesta de solución en BI`, `## 2.2. Arquitectura de Inteligencia de Negocios`, `## 2.3. Herramientas utilizadas`); después, solo texto final del informe (prosa académica y tablas), sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- La sección 2.2 marca su figura en una línea sola: `<!-- figura: arquitectura-bi -->`. El HTML queda en `visuales/` y su explicación en `leer-imagen/`; los escribe `visuales.py construir --visual arquitectura-bi --run <corrida>`. 2.1 y 2.3 no llevan figura.
- `referencias.md` (una referencia por línea, APA 7) si se cita algo, y `README.md` (procedencia; único archivo que puede decir que un dato es generado).
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada sección); `12-make-report` renumera las tablas en todo el informe y avisa las que no tienen título.

### 0.3b Qué leen las demás skills
`07-make-data-model-kpi` toma de 2.2 las fuentes y el almacenamiento para modelar y de 2.1 los objetivos para formular los KPI; el capítulo 3 (ETL y dashboard) toma de 2.3 las herramientas. Por eso los códigos no se reutilizan ni se renumeran.

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `CAP-nn` | Componente de la arquitectura | Primera celda de la tabla de 2.2 |
| `HER-nn` | Herramienta | Primera celda de la tabla de 2.3 |
| `OE-nn`, `FUE-nn` | Objetivo y fuente del brief | Brief (se citan, no se vuelven a definir) |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un ítem.

### 0.5 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Lo que aún no se decide se escribe «Pendiente» con su motivo; no se redacta como hecho. Cada cita en texto lleva su referencia en `referencias.md`.

---

## 1. Propuesta de solución (2.1)

- **Decisiones que apoya.** Viñetas con las decisiones del brief (sección 5), una por línea.
- **Usuarios.** Quién usa la solución y para qué decide (del brief).
- **Respuesta a la problemática.** Un párrafo: cómo la solución ataca la problemática central y sus causas principales (de 1.8), sin repetir el diagnóstico.
- **Tabla de objetivos.** `Objetivo | Componentes | Cómo lo atiende`, con **una fila por cada `OE` del brief**, los `CAP-nn` de 2.2 que lo atienden y una frase de cómo.

## 2. Arquitectura de BI (2.2)

- Un párrafo que presenta las **cuatro capas en este orden**: **Fuentes → ETL → Almacenamiento → Visualización** (puede citar un marco, por ejemplo Kimball y Ross, 2013).
- La marca de figura `<!-- figura: arquitectura-bi -->`.
- Tabla `Código | Capa | Componente | Función | Entrada y salida`, con **al menos un componente por capa**:
  - **Fuentes:** un componente por cada `FUE-nn` del brief, que cita su código en el componente o la función.
  - **ETL:** extracción, transformación y reglas de calidad, y carga.
  - **Almacenamiento:** dónde queda el modelo dimensional que consume el dashboard.
  - **Visualización:** el dashboard y su publicación.
- Cierra con una **Lectura de la arquitectura.** de una o dos frases: cómo fluye el dato desde la fuente hasta la decisión.

## 3. Herramientas utilizadas (2.3)

- Una frase que introduce la tabla y la tabla `Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada`.
- Hay al menos una fila por cada capa de **ETL**, **Almacenamiento** y **Visualización**; las fuentes no llevan herramienta.
- **Power BI** figura en la capa de **Visualización** (la consigna lo exige).
- Cada herramienta tiene capa, función concreta, justificación (por qué esta y no otra, con criterios como costo, curva de aprendizaje, integración y tamaño de los datos) y la alternativa que se descartó.
- **Pendiente.** Las herramientas de **ETL** y de **Almacenamiento** pueden decir «Pendiente» en la columna de herramienta, con el motivo en la justificación (por ejemplo, «se decide al construir el capítulo 3»). En cualquier otra capa, «Pendiente» es un error. Se completa con `06-make-bi-solution-update` y debe resolverse antes de entregar el informe.

## 4. Errores frecuentes
- Describir herramientas en vez de capas: la arquitectura se dibuja con funciones y la herramienta es una decisión posterior.
- Una fuente del brief que no aparece en la arquitectura, o una fuente nueva que el brief no tiene.
- Un objetivo sin componente que lo atienda.
- Justificar con «es la más usada» o «es gratuita» sin criterio de comparación.
- Dejar «Pendiente» sin motivo o en la capa de visualización.

## 5. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/bi_solution.py`: encabezados, decisiones, usuarios y respuesta, una fila de la tabla de 2.1 por cada `OE` del brief con componentes que existen, las cuatro capas en orden, cada `FUE` del brief en la capa de fuentes, cada herramienta con su justificación y su alternativa («Pendiente» solo en ETL y almacenamiento), Power BI en visualización, la figura marcada y construida y las citas con su referencia.
