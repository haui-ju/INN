# Playbook del análisis estratégico (secciones 1.5 a 1.7)

Guía para que un agente redacte el análisis del entorno y de la problemática del capítulo 1 del informe de BI (`common/structure/model1.md`): PESTEL, matriz FODA con estrategias cruzadas y diagrama de Ishikawa. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `04-make-strategic-analysis` (y lo ajusta `04-make-strategic-analysis-update`). Escribe en `project/04-strategic-analysis/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide integrar FODA, PESTEL, Canvas e Ishikawa con la problemática bien definida y todos los elementos articulados a los objetivos.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): **el problema principal es el efecto del Ishikawa**; la evidencia, las fuentes de datos y los usuarios orientan el FODA.
2. La corrida vigente de `03-make-business-diagnosis` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 03-make-business-diagnosis`): industria, tipo de cliente, entorno competitivo y Canvas (recursos, actividades, canales y costos alimentan fortalezas y debilidades).
3. `project/domain.md` (clientes y competencia) y el config (`rubro`, `tipo`, `modo_datos`).
4. Fuentes externas verificadas para el PESTEL (instituciones oficiales, normas, estudios). **Ninguna cifra externa se escribe sin su fuente**; si no se encuentra, el hallazgo se reformula sin cifra o se deja fuera.

### 0.2 Preguntar y confirmar
Pregunta solo lo que falta (por ejemplo, competidores concretos o una fortaleza que solo conoce el equipo). Muestra un plan (hallazgos PESTEL en una línea cada uno, los cuatro cuadros del FODA, las estrategias y las causas del Ishikawa por categoría) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/1.5.md`, `1.6.md` y `1.7.md`: la primera línea es el encabezado exacto (`## 1.5. Análisis PESTEL`, `## 1.6. Matriz FODA`, `## 1.7. Diagrama de la problemática: Ishikawa`); después, solo texto final (prosa académica y tablas), sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- Cada sección marca su figura en una línea sola: `<!-- figura: pestel -->`, `<!-- figura: foda -->` y `<!-- figura: ishikawa -->`. Los HTML quedan en `visuales/` y sus explicaciones en `leer-imagen/`; los escribe `visuales.py construir --run <corrida>`, que recibe de la skill el «Qué debes entender» de cada figura con `--interpretacion` (3 a 6 frases con los datos del caso: qué conclusión saca el lector, no cómo se ve). El HTML del PESTEL trae dos láminas (tres factores cada una) y el del FODA dos (la matriz de cuatro cuadros y las estrategias cruzadas), cada una con proporción de diapositiva para recortarla de la captura. Los HTML quedan en `visuales/` y sus explicaciones en `leer-imagen/`; los escribe `visuales.py construir --run <corrida>`.
- `referencias.md` (una referencia por línea, APA 7) y `README.md` (procedencia; único archivo que puede decir que un dato es generado).
- **Título de cada tabla.** Antes de cada tabla va una línea `Tabla N: título` (N empieza en 1 en cada sección); `12-make-report` renumera las tablas en todo el informe y avisa las que no tienen título.

### 0.4 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `POL-nn`, `ECO-nn`, `SOC-nn`, `TEC-nn`, `AMB-nn`, `LEG-nn` | Hallazgo político, económico, social, tecnológico, ecológico (ambiental) y legal | Primera celda de la tabla de 1.5 |
| `FOR-nn`, `DEB-nn`, `OPO-nn`, `AME-nn` | Fortaleza, debilidad, oportunidad, amenaza | Primera celda de las tablas de 1.6 |
| `FO-nn`, `FA-nn`, `DO-nn`, `DA-nn` | Estrategia cruzada (el prefijo es su tipo) | Primera celda de la tabla de estrategias de 1.6 |
| `CAU-nn` | Causa del Ishikawa | Primera celda de la tabla de 1.7 |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un ítem. La skill `05-make-problem-objectives` cita estos códigos en su matriz de articulación.

### 0.5 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Cada sección cita su marco una vez (Aguilar, 1967; Gürel & Tat, 2017; Ishikawa, 1986) y cada fuente del PESTEL va en `referencias.md`. Las fuentes internas de la empresa (registro de caja, control de producción) se nombran con su año, sin cita.

### 0.6 Articulación (lo que la rúbrica revisa)
- **PESTEL → FODA:** cada oportunidad y amenaza cita en su evidencia el código PESTEL del que sale (o una fuente con su año).
- **Canvas → FODA:** las fortalezas y debilidades se apoyan en recursos, actividades, canales y costos del Canvas (1.4).
- **FODA → Ishikawa:** la evidencia de cada causa cita la debilidad o amenaza que la respalda, o un hecho con su año.
- **Ishikawa → objetivos:** las causas son las que `05` priorizará y vinculará a los `OE`; deben poder atenderse o medirse con datos.

---

## 1. PESTEL (1.5)

- Un párrafo que presenta el análisis con su cita, la marca de figura y la tabla `Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente`.
- **Factor**: Político, Económico, Social, Tecnológico, Ecológico o Legal, coherente con el prefijo del código. Al menos un hallazgo por factor (referencia: de uno a tres).
- **Hallazgo**: un hecho del entorno, concreto y verificable. **Efecto en el negocio**: qué le pasa a esta empresa por ese hecho (no una definición del factor).
- **Tipo**: Oportunidad o Amenaza. **Fuente**: autor o institución y año, `INEI (2025)`, o una fuente interna con su año.
- Cierra con una **Síntesis.** de dos frases: qué factores pesan más y cuáles se trasladan al FODA.

## 2. Matriz FODA (1.6)

- Un párrafo con su cita, la marca de figura y cuatro tablas `Código | Fortaleza | Evidencia o fuente` (y lo mismo con Debilidad, Oportunidad y Amenaza). Referencia: de tres a cinco ítems por cuadro; el validador exige al menos uno.
- Fortalezas y debilidades son internas (recursos, procesos, datos, personas); oportunidades y amenazas son externas y salen del PESTEL o del entorno competitivo.
- **Estrategias cruzadas.** Una frase y la tabla `Código | Tipo | Estrategia | Combina`: al menos una de cada tipo. **FO** usa fortalezas para aprovechar oportunidades; **FA** usa fortalezas para frenar amenazas; **DO** supera debilidades con oportunidades; **DA** reduce debilidades frente a amenazas. La columna **Combina** lista los códigos (al menos uno del cuadro interno y uno del externo que el tipo indica).
- Las estrategias que una solución de BI hace posible (medir, integrar, pronosticar) son las que `05` vincula a los objetivos.

## 3. Ishikawa (1.7)

- Un párrafo con su cita, el rótulo **Efecto.** con el problema principal del brief **copiado sin cambios**, la marca de figura y la tabla `Código | Categoría | Causa | Evidencia`.
- **Categorías 6M:** Método, Mano de obra, Materiales, Maquinaria, Medición y Medio ambiente (nombres exactos). Al menos seis causas repartidas en al menos cuatro categorías.
- Cada causa es concreta (qué pasa, dónde) y lleva evidencia: el código FODA que la respalda o un hecho con su año.
- Cierra con una **Lectura del diagrama.** de dos frases: en qué categorías se concentran las causas y cuáles se pueden medir con datos.

---

## 4. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/strategic_analysis.py`: encabezados, figuras y sus explicaciones, códigos citados sin definir, seis factores con efecto, tipo y fuente con año, cuatro cuadros con evidencia, oportunidades y amenazas con respaldo PESTEL o fuente, estrategias de los cuatro tipos bien combinadas, efecto igual al problema del brief, categorías 6M y cantidades mínimas, sin el marcador de datos modelados y citas con su referencia.

## 5. Errores frecuentes y checklist

**Errores:** un PESTEL de definiciones sin efecto en la empresa; cifras externas sin fuente; oportunidades que en realidad son fortalezas; estrategias que no citan códigos o que mezclan cuadros que su tipo no indica; un efecto del Ishikawa redactado distinto del brief; causas genéricas («falta de tecnología») sin evidencia; reutilizar un código eliminado.

**Checklist:**
- [ ] Cada sección empieza con su encabezado exacto y marca su figura.
- [ ] Seis factores PESTEL, cada uno con efecto, tipo y fuente con año.
- [ ] Cuatro cuadros FODA con evidencia; oportunidades y amenazas citan el PESTEL.
- [ ] Al menos una estrategia FO, FA, DO y DA, con los códigos que combina.
- [ ] El efecto del Ishikawa es el problema principal del brief; causas 6M con evidencia.
- [ ] Visuales `pestel`, `foda` e `ishikawa` construidos con `--run`.
- [ ] Cada cita tiene su línea en `referencias.md`; la procedencia está solo en `README.md`.
- [ ] El usuario confirmó el plan antes de escribir.

---

## Referencias

Aguilar, F. J. (1967). *Scanning the business environment*. Macmillan.

Gürel, E., & Tat, M. (2017). SWOT analysis: A theoretical review. *The Journal of International Social Research, 10*(51), 994-1006. https://doi.org/10.17719/jisr.2017.1832

Ishikawa, K. (1986). *Guide to quality control* (2.ª ed.). Asian Productivity Organization.

*(Formato APA 7, ver `common/citation-style/APA7.md`. Las fuentes del PESTEL se verifican y se agregan a `referencias.md` de la corrida.)*
