# Design

## Context

Estado observado: no existe `common/methodological-framework/` ni skill de capítulo; `pipeline.json` define `04-make-methodological-framework` (verbo `make`, carpeta `methodological-framework`, requiere solo `00-init`, con `update`). El índice `model1.md` define el capítulo 2 con cuatro puntos (2.1 innovación, 2.2 ágiles, 2.3 integración, 2.4 marco conceptual `[A1+]`) sin subpuntos numerados. El playbook de Design Thinking ya fija reglas de citas (máximo 1 o 2 por fase, lista cerrada, formato APA 7 de `common/citation-style/APA7.md`) y no cita fuentes de Design Thinking como método. El validador admite `PREFIJOS`, el gancho `validar(run)` y `RULES`. Los capítulos 1 (company-chapter) y el Lean Canvas fijan el patrón de bloques, `README.md` de procedencia y verificación contra otras corridas.

## Goals / Non-Goals

**Goals:** un capítulo 2 comparable y validable; una integración entre metodologías trazable al índice; un glosario que se pueda ampliar sin rehacer el capítulo; citas verificadas.

**Non-Goals:** aplicar las metodologías, la lista global de referencias, ejecutar la skill, cambiar `model1.md`.

## Decisions

### D1. Salida
`capitulo-2.md` (2.1 a 2.4), `glosario.md` (misma tabla que 2.4), `referencias.md` (entradas APA de las fuentes citadas) y `README.md`. **Alternativa:** todo en un archivo; descartada porque el glosario se amplía de forma independiente y `19-make-report` necesita las referencias aparte.

### D2. Estructura por metodología
Subsecciones sin numerar (`### Design Thinking`, `### Lean Startup`, `### Lean Change Management` en 2.1; `### Scrum`, `### Kanban` en 2.2) para no alterar el índice. Cada una usa etiquetas en negrita seguidas de punto (`**Qué es.**`, `**Principios.**`, `**Cuándo se usa.**`, `**En este proyecto.**`) y las propias: DT `**Fases.**`; Lean Startup y Lean Change `**Ciclo.**`; Scrum `**Roles.**`, `**Eventos.**`, `**Artefactos.**`; Kanban `**Prácticas.**`, `**Métricas.**`. **En este proyecto** conecta con las skills y los puntos del informe que la aplican. La profundidad solo cambia la extensión: resumen (un párrafo o una lista corta por etiqueta) o detallado (más ejemplos).

### D3. Metodologías aplicadas
Se proponen desde `pipeline.json` (Design Thinking: 05 y 06; Lean: 02, 07 y 17; Scrum: 08 a 12; Kanban: 12) y el usuario confirma o quita. La tabla de 2.3 y las subsecciones deben coincidir; el validador lo comprueba.

### D4. Integración (2.3)
Una línea de flujo (`Design Thinking → Lean Startup → Lean Change Management → Scrum → Kanban`, solo con las aplicadas) y una tabla `Metodología | Recibe | Produce | Dónde en el informe`. «Dónde» lista puntos del índice (por ejemplo `3.1.7`, `3.4`, `4.4`, `6.1.4`); el validador extrae los números con `\d(\.\d+)+` y comprueba que existen como puntos en `common/structure/model1.md` (líneas `- N.N.N.`). La raíz del repositorio se resuelve como `run.parents[2]`.

### D5. Glosario
Tabla `Término | Definición | Origen | Se usa en`, orden alfabético sin acentos ni mayúsculas, sin términos repetidos. El playbook define **términos obligatorios** por metodología (por ejemplo Scrum: Product Owner, Scrum Master, Equipo de desarrollo, Sprint, Product Backlog, Sprint Backlog, Incremento, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective, Definition of Done; Kanban: Tablero, Columna, WIP, Tiempo de ciclo, Rendimiento; Design Thinking: Empatizar, Definir, Idear, Prototipar, Testear, POV, HMW; Lean Startup: Hipótesis, MVP, Construir-medir-aprender, Pivotar, Perseverar; Lean Change: Insight, Opción, Experimento) más una lista de **términos opcionales** de capítulos posteriores (Requerimiento funcional, Requerimiento no funcional, Historia de usuario, Criterio de aceptación, Diagrama de Gantt, Objetivo del sprint…). Cada término obligatorio debe aparecer también en el texto de su metodología. «Origen» es una metodología, `Negocio` o `Proyecto`; «Se usa en» lista puntos del índice válidos. `glosario.md` y 2.4 son idénticos (comparación normalizada).

### D6. Términos del negocio
De 3 a 6, tomados del tema del config, `domain.md` y el canvas vigente (por ejemplo «stock», «talla»), con origen `Negocio` si el proyecto es empresa y `Proyecto` si es propio. El usuario confirma.

### D7. Citas y referencias
Lista cerrada en la guía, con fuentes **verificadas por búsqueda antes de escribirlas**, candidatas: Brown (2008) para Design Thinking (no se incluye la guía del d.school: no se verificó); Ries (2011) para Lean Startup; Little (2014) para Lean Change Management; Schwaber y Sutherland (2020) para Scrum; Anderson (2010) y Anderson y Carmichael (2016) para Kanban; Maurya (2012) ya está verificada en `common/lean`. Máximo 2 por subsección de metodología y 2 en cada uno de 2.3 y 2.4 (una sola fuente principal basta; una metodología no puede quedar sin poder citar la suya solo por compartir punto con otras). El validador extrae citas `Autor (año)` y `(Autor, año)` del capítulo y exige que estén en la lista de `rules/methodological_framework.py`, que debe coincidir con la guía, y que `referencias.md` tenga una entrada por cada fuente citada y ninguna extra.

### D8. Validación
`rules/methodological_framework.py`: `validar(run)` comprueba secciones 2.1 a 2.4 y sus títulos, subsecciones con etiquetas por metodología (conjunto de metodologías igual al de la tabla de 2.3), orden del flujo, puntos existentes en el índice, glosario (obligatorios, orden, duplicados, origen válido, «Se usa en» válido, términos obligatorios presentes en el texto de su metodología), igualdad glosario/2.4, citas y referencias. Sin `PREFIJOS` (no hay códigos de trazabilidad).

### D9. `-update`
Patrón del cambio 1, con tres modos: términos (agregar, quitar, corregir), metodologías aplicadas (quitar o añadir una: toca su subsección, la tabla y el flujo de 2.3, el glosario y `referencias.md`) y ampliación del glosario (lee los textos de las corridas vigentes y propone términos opcionales que aparezcan; el usuario confirma). `references/dependencias.md` relaciona cada parte con los archivos que la citan.

### D10. Texto limpio y propio
Como en los demás pasos: la procedencia solo va en `README.md`; «En este proyecto» describe lo que el proyecto hace, sin etiquetas.

## Risks / Trade-offs

- [Fuentes mal citadas] → Lista cerrada, verificación por búsqueda antes de escribirla y comprobación automática de que el capítulo solo cita esa lista.
- [Glosario que crece sin control] → Orden, no duplicados y «Se usa en» obligatorio; el `-update` pide confirmación de cada ampliación.
- [Capítulo genérico que no refleja el proyecto] → «En este proyecto» obligatorio y trazado a skills y puntos reales del índice.
- [Cambios del índice que invaliden «Dónde en el informe»] → La validación vuelve a leer `model1.md`; el `-update` corrige las filas afectadas.
- [Variación de criterios de qué es «obligatorio»] → La lista de obligatorios vive en la guía y en el módulo de reglas, con una prueba que las compara.

## Migration Plan

Sin migración: el paso es nuevo.

## Open Questions

- Si el glosario final del informe se toma de la corrida vigente de este paso o se regenera en el armado (decisión del cambio 14).
- Si algún término del glosario debe mantenerse en inglés (por ejemplo «Product Backlog»); por defecto se mantiene el nombre usado en el índice.
