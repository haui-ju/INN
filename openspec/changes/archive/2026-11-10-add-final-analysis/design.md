# Design

## Context

Estado observado: `pipeline.json` define `17-make-lean-results` (requiere 07 y 15) y `18-make-final-analysis` (requiere 16 y 17), ambos con `update`. El plan Lean aporta `HIP`, `MET`, `EXP` (de negocio en 3.2.3 y de cambio en 3.3.2, con numeración única y avance asignado), el criterio de éxito de cada experimento y la tabla «Hipótesis | Perseverar si | Pivotar si» escrita antes de ejecutar. El capítulo 1 aporta `OG-01` y los `OE-nn` con métrica, meta y plazo. Cada informe de sprint guarda una copia del `data.json` del tablero (estado y `calculado`); `boards.py` calcula los indicadores. La bitácora aporta `BIT`, resultados de `CP` y `RIE`; el Design Thinking, `TST` y `HAL-T`. El índice define 3.2.3, 3.2.4 (`[A1+]`), 6.4.1 a 6.4.5 y 7.1 a 7.3 (`[A3]`). Python de la biblioteca estándar.

## Goals / Non-Goals

**Goals:** cerrar el ciclo Lean con los criterios fijados de antemano; comparar lo real con lo planificado con cifras trazables; conclusiones, recomendaciones y trabajos futuros con evidencia; análisis honesto de limitaciones.

**Non-Goals:** actualizar el canvas validado, armar el informe, generar imágenes, ejecutar las skills.

## Decisions

### D1. Resultados Lean (`resultados.md`)
`## 3.2.3. Resultados del ciclo construir-medir-aprender` con la tabla `Código | EXP | Avance | Resultado | Criterio de éxito | ¿Se cumplió? | Evidencia` (`RES-nn`). El `EXP` existe en el plan; el avance y el criterio de éxito son **copia exacta** del plan (no se reescriben tras ver el resultado); el resultado lleva una cifra; `¿Se cumplió?` es `Sí`, `No` o `Parcial`; la evidencia cita `BIT`, `CP`, `HU`, `TST`, `HAL-T` o `RIE` existentes, o archivos de `evidencias/`. Todo `EXP` tiene un `RES` o figura en `### Sin resultado` (`EXP | Motivo`), por ejemplo los de un avance aún no ejecutado.

### D2. Decisión (`decision.md`)
`## 3.2.4. Decisión de pivotar o perseverar` con `Hipótesis | Resultados | Criterio aplicado | Decisión | Justificación`. Decisión: `Perseverar`, `Pivotar`, `Iterar` o `Pendiente`. El **criterio aplicado** es el texto exacto de «Perseverar si» o «Pivotar si» del plan (según la decisión), «Zona de iterar» si es `Iterar`, y «—» si es `Pendiente`. Los resultados citados son `RES` de experimentos que ponen a prueba esa hipótesis. Una línea `**Decisión general.**` (`Perseverar`, `Pivotar` o `Iterar`) con su justificación. La skill propone la decisión aplicando los criterios y el usuario la confirma.

### D3. Análisis consolidado (`analisis-consolidado.md`)
Una línea `**Avances incluidos.** 1, 2, 3` que debe coincidir con los informes de sprint registrados en el config; si falta alguno, el análisis es parcial y lo declara. Cinco puntos `## 6.4.n.`:
- **6.4.1 Cumplimiento de los objetivos:** `Código | Objetivo | Meta | Resultado | Base | Valoración | Evidencia` para `OG-01` y cada `OE` del capítulo 1 vigente (objetivo y meta iguales a los del capítulo). Valoración `Cumplido`, `Parcial`, `No cumplido` o `No evaluable`; base `Sistema`, `Piloto`, `Prototipo` o `Sin medir` (`Sin medir` si y solo si `No evaluable`). La evidencia cita `RES`, `HU`, `CP`, `BIT`, `TST`, `HAL-T` o `HIP` existentes.
- **6.4.2 Gantt real contra la línea base:** línea `**Corte.**` y tabla `Sprint | Tareas | Terminadas | Avance | Fin planificado | Fin real` calculada del `data.json` del último informe incluido (fin real = última `fin_real` si el sprint terminó, «—» si no).
- **6.4.3 Métricas Kanban acumuladas:** tabla `Avance | Corte | Tareas hechas | Nuevas en el sprint | Tiempo de ciclo | Rendimiento` con una fila por informe incluido (iguales a lo que calcula el kit sobre su `data.json`) y una fila `Acumulado`; la suma de las nuevas es las hechas al último corte.
- **6.4.4 Validación con usuarios:** tabla `Fuente | n | Resultado | Evidencia` (`Design Thinking`, `Sistema (piloto)` o `Sistema (usuarios finales)`; la evidencia cita códigos existentes: `TST`, `HAL-T`, `RES`, `BIT`, `HU` o `CP`).
- **6.4.5 Discusión:** `**Texto.**` y tabla `Limitación | Efecto en los resultados`. Si alguna base de 6.4.1 no es `Sistema`, o 6.4.4 no tiene filas del sistema, hay al menos una limitación.

### D4. Conclusiones (`conclusiones.md`)
`## 7.1. Conclusiones` (`CNC-nn | Conclusión | Evidencia`), `## 7.2. Recomendaciones` (`REC-nn | Recomendación | Se apoya en`, cita `CNC`) y `## 7.3. Trabajos futuros` (`TRF-nn | Trabajo futuro | Motivo | Origen`, cita `CNC`, `REC`, `RIE` o una limitación). Toda `CNC` cita al menos un código de evidencia existente (`RES`, `OG`, `OE`, `HIP`, `HU`, `CP`, `BIT`, `RIE`, `TST`, `HAL-T`), y `OG-01` y cada `OE` están citados en alguna conclusión. Las acciones de la última retrospectiva con «Trabajos futuros» se ofrecen al usuario como `TRF`.

### D5. Objetivos medibles solo con piloto
La **base** de la valoración lo hace explícito: un objetivo medido en piloto o prototipo se valora con esa base y obliga a declarar la limitación; uno sin medición es `No evaluable` con motivo. No se esconde ni se infla.

### D6. Informe de sprint faltante
Si falta el informe de un sprint, la skill avisa y ofrece `16-make-sprint-report`; si el usuario continúa, el análisis declara los avances incluidos y se valida solo contra ellos; el texto lo dice con esas palabras.

### D7. Códigos
`RES-nn` se define en `resultados.md`; `CNC-nn`, `REC-nn` y `TRF-nn` en `conclusiones.md`. Sin choque con códigos existentes (`CON` es del Design Thinking).

### D8. Fuentes
Sin referencias nuevas: Ries (2011) para el ciclo construir-medir-aprender y las decisiones de pivotar o perseverar, Little (2014) para el cambio y Doran (1981) para objetivos medibles; ya verificadas. Máximo 1 o 2 citas por archivo.

### D9. Validación
`rules/lean_results.py` (`PREFIJOS = ["RES"]`) lee el plan Lean vigente (`HIP`, `MET`, `EXP`, criterios), la bitácora y el Design Thinking. `rules/final_analysis.py` (`PREFIJOS = ["CNC", "REC", "TRF"]`) lee los resultados Lean, el capítulo 1, los `data.json` de los informes de sprint, la bitácora y el Design Thinking; recalcula con `boards.calcular` y exige igualdad. Sin una fuente, un aviso por cada comprobación imposible.

### D10. `-update`
Patrón del cambio 1. `17`: resultados, evidencias y decisiones; `18`: valoraciones, cifras (resincronizar con los informes), validación con usuarios, limitaciones, conclusiones, recomendaciones y trabajos futuros. Avisan de lo que cita los códigos cambiados (decisión, conclusiones, informe final).

### D11. Prerrequisitos
`pipeline.json`: `18-make-final-analysis` requiere además `03-make-company-chapter`. Solo avisos.

## Risks / Trade-offs

- [Reescribir criterios tras ver los resultados] → el criterio de éxito y el de decisión son copia exacta del plan y se validan.
- [Valorar objetivos de forma complaciente] → base de la evidencia obligatoria, resultado con cifra y limitaciones forzadas.
- [Cifras acumuladas que no suman] → se recalculan con `boards.py` sobre los `data.json` de los informes.
- [Conclusiones sin sustento] → cada una cita códigos existentes y todo objetivo tiene conclusión.
- [Proyecto sin los tres informes] → análisis parcial declarado.

## Migration Plan

Se edita el prerrequisito de la skill 18 en `pipeline.json` y se registran dos carpetas en `validate_run.py`. Sin migración de datos.

## Open Questions

- Si conviene actualizar el canvas validado (3.4) con los resultados en un cambio aparte.
