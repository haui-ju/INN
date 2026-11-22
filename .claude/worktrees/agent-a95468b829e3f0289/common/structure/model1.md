# Índice general del informe

## Control del documento

**Portada.** Título del proyecto, empresa, curso, integrantes del equipo, docente y fecha de entrega (los toma `12-make-report` del config y del brief).

**Formato de entrega.** Word o PDF, letra Arial 11, interlineado 1.5 y márgenes estándar. El dashboard se desarrolla en Power BI y se presenta en la exposición.

**Qué secciones se arman.** Cada punto numerado lo produce una sola skill (ver `.claude/skills/_shared/pipeline.json`). Al terminar, la skill marca sus puntos como disponibles en `informe.secciones` del config, y `12-make-report` arma el informe solo con los disponibles; el resto se lista en `faltantes.md`.

**Reglas de contenido.**

- No se repite contenido entre secciones: si una figura o tabla ya apareció, se cita por su número.
- Lo extenso (diccionario de datos completo, scripts, medidas, capturas de cada página) va a los anexos; en el cuerpo, un resumen y su análisis.
- Toda figura lleva pie de foto con número y título («Figura 4: Matriz FODA de Pollería Don Tito»).
- Toda cifra lleva su fecha o su fuente («margen neto 8 % en 2026, según el estado de resultados»).
- Cada elemento del diagnóstico se articula con los objetivos del proyecto (1.9 y 1.10), como pide la rúbrica.

## Capítulo 1: Diagnóstico estratégico y análisis del negocio

- 1.1. Nombre de la empresa (razón social, nombre comercial, RUC si aplica y breve reseña)
- 1.2. Misión y visión
- 1.3. Industria y tamaño (sector, actividad económica, tipo de cliente, entorno competitivo y tamaño de la organización)
- 1.4. Modelo de negocio: Business Model Canvas (los nueve bloques del lienzo) (incluye imagen)
- 1.5. Análisis PESTEL (factores políticos, económicos, sociales, tecnológicos, ecológicos y legales, con su efecto en el negocio) (incluye imagen)
- 1.6. Matriz FODA (fortalezas, oportunidades, debilidades y amenazas, y estrategias cruzadas) (incluye imagen)
- 1.7. Diagrama de la problemática: Ishikawa (causas agrupadas por categoría que explican el efecto) (incluye imagen)
- 1.8. Problemática central del negocio (enunciado del problema, sus causas principales y su evidencia)
- 1.9. Objetivo general del proyecto
- 1.10. Objetivos específicos (cada uno con su métrica, meta e indicador)

## Capítulo 2: Diseño técnico de solución en Inteligencia de Negocios

- 2.1. Propuesta de solución en BI (qué decisiones apoya, para quién y cómo responde a la problemática)
- 2.2. Arquitectura de Inteligencia de Negocios (fuentes, ETL, almacenamiento y visualización) (incluye imagen)
- 2.3. Herramientas utilizadas (cada herramienta con su función y su justificación)
- 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones (incluye imagen)
- 2.5. Indicadores clave de rendimiento (KPI) (fórmula, fuente, meta y objetivo al que responde cada uno)

## Capítulo 3: Construcción y calidad del dashboard en Power BI

- 3.1. Construcción de la solución ETL (extracción, transformación, reglas de calidad y carga)
- 3.2. Construcción del dashboard en Power BI (páginas, visualizaciones, filtros y KPI) (incluye imagen)

## Capítulo 4: Storytelling con datos

- 4. Storytelling con datos (visualización clara y narrativa interpretativa de los resultados, orientada a la toma de decisiones) (incluye imagen)

## Capítulo 5: Conclusiones, recomendaciones y lecciones aprendidas

- 5. Conclusiones, recomendaciones y lecciones aprendidas

## Referencias bibliográficas

## Anexos

- Anexo A: Diccionario de datos y calidad de datos (tablas, campos, tipos, reglas de calidad y resultados)
- Anexo B: Scripts del ETL (código o pasos de transformación completos)
- Anexo C: Medidas y cálculos del dashboard (medidas DAX y columnas calculadas)
- Anexo D: Especificación y capturas del dashboard (una captura por página con su descripción)
