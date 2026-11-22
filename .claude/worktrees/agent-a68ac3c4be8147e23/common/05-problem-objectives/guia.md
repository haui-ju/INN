# Playbook de la problemática y los objetivos (secciones 1.8 a 1.10)

Guía para que un agente cierre el capítulo 1 del informe de BI (`common/structure/model1.md`): la problemática central del negocio, el objetivo general, los objetivos específicos y la **matriz de articulación** que une cada objetivo con el diagnóstico. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `05-make-problem-objectives` (y lo ajusta `05-make-problem-objectives-update`). Escribe en `project/05-problem-objectives/<DD-MM-AAAA-HH-MM-SS>/`. Es la sección que demuestra lo que pide la rúbrica: «todos los elementos están articulados a los objetivos del proyecto y sustentados».

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): problema principal, afectados, evidencia y los objetivos `OG-01` y `OE-nn` con su métrica, meta, plazo e indicador.
2. La corrida vigente de `04-make-strategic-analysis` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 04-make-strategic-analysis`): causas del Ishikawa, ítems y estrategias FODA y hallazgos PESTEL, con sus códigos.
3. La corrida vigente de `03-make-business-diagnosis` (`diagnostico.py leer --paso 03-make-business-diagnosis`): los nueve bloques del Canvas por su nombre exacto.

### 0.2 Los objetivos no se vuelven a proponer
`OG-01` y los `OE-nn` **se copian del brief sin cambios** (objetivo, métrica, meta, plazo, aporte e indicador). Si el usuario quiere cambiar un objetivo, se hace con `01-make-project-brief-update` y luego se vuelve a ejecutar esta skill o su `-update`. El validador compara fila por fila con el brief vigente.

### 0.3 Preguntar y confirmar
Lo que se decide aquí es **qué causas son las principales** (de dos a cuatro, tomadas del Ishikawa) y **cómo se articula cada objetivo** con el diagnóstico. Propón ambas cosas, muéstralas en un plan (causas principales con su porqué y una fila de la matriz por `OE`) y **espera la confirmación** antes de escribir.

### 0.4 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/1.8.md`, `1.9.md` y `1.10.md`: la primera línea es el encabezado exacto (`## 1.8. Problemática central del negocio`, `## 1.9. Objetivo general del proyecto`, `## 1.10. Objetivos específicos`); después, solo texto final del informe (prosa y tablas), sin notas de trabajo ni otros encabezados de nivel 1 o 2. Estas secciones no llevan figura.
- `referencias.md` solo si se cita algo (por ejemplo, un criterio de objetivos medibles) y `README.md` con la procedencia.

### 0.5 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Las cifras de la evidencia llevan su fecha o su fuente, igual que en el brief.

---

## 1. Problemática central (1.8)

- **Enunciado.** Dos o tres frases: el problema principal del brief (con sus cifras), a quién afecta y por qué importa para la decisión. No contradice el efecto del Ishikawa.
- **Afectados.** Las áreas o personas que sufren el problema (del brief).
- **Causas principales.** Una frase que explica el criterio de priorización (peso en el problema y posibilidad de medirlo con datos) y la tabla `Código | Causa principal | Categoría | Evidencia`, con **entre dos y cuatro causas copiadas del Ishikawa** (mismo código, misma categoría y mismo texto). La evidencia es un dato con su fecha o su fuente.
- **Evidencia.** Viñetas con los datos que prueban el problema (del brief y del diagnóstico).

## 2. Objetivo general (1.9)

Una frase que lo vincula con la problemática y la tabla del brief `Código | Objetivo | Métrica | Meta | Plazo | Indicador`, copiada sin cambios.

## 3. Objetivos específicos y matriz de articulación (1.10)

- Una frase y la tabla del brief `Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador`, copiada sin cambios.
- **Matriz de articulación.** Una frase y la tabla `Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador`, con **una fila por cada `OE` del brief**:
  - **Causas (Ishikawa):** los `CAU-nn` que el objetivo atiende (al menos uno).
  - **FODA:** ítems (`FOR`, `DEB`, `OPO`, `AME`) o estrategias (`FO`, `FA`, `DO`, `DA`) que el objetivo aprovecha o corrige (al menos uno).
  - **PESTEL:** los hallazgos del entorno que lo condicionan, o «—» si ninguno.
  - **Canvas:** los bloques del lienzo donde actúa, con su nombre exacto, separados por punto y coma.
  - **Indicador:** el del objetivo en el brief, igual.
- **Cobertura:** cada causa principal de 1.8 aparece en al menos una fila. Si una no tiene objetivo, o se agrega un `OE` en el brief o se revisa la priorización.
- Cierra con una **Lectura de la matriz.** de dos frases: qué causas atiende cada objetivo y cómo se medirá su logro con los KPI del capítulo 2.

---

## 4. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/problem_objectives.py`: encabezados, enunciado, afectados y evidencia, causas principales iguales al Ishikawa vigente, objetivos iguales al brief vigente, una fila de la matriz por `OE` con códigos y bloques existentes en las corridas vigentes de `03` y `04`, indicador igual al del brief, cobertura de las causas principales, sin el marcador de datos modelados y citas con su referencia. Si falta una corrida de origen, lo informa.

## 5. Errores frecuentes y checklist

**Errores:** reescribir un objetivo o su meta; elegir causas principales que no están en el Ishikawa o cambiarles el texto; una matriz que cita códigos que ya no existen tras un `-update` de `04`; filas sin causa; un indicador distinto del brief; dejar una causa principal sin objetivo.

**Checklist:**
- [ ] Cada sección empieza con su encabezado exacto.
- [ ] El enunciado recoge el problema del brief con sus cifras.
- [ ] De dos a cuatro causas principales, copiadas del Ishikawa.
- [ ] `OG-01` y los `OE` son idénticos al brief.
- [ ] La matriz tiene una fila por `OE`, con causas, FODA, PESTEL o «—», Canvas e indicador.
- [ ] Cada causa principal está atendida por algún objetivo.
- [ ] La procedencia está solo en `README.md`; el usuario confirmó el plan.

---

## Referencias

Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals and objectives. *Management Review, 70*(11), 35-36.

*(Formato APA 7, ver `common/citation-style/APA7.md`. Solo si se cita en la corrida, se agrega a su `referencias.md`.)*
