# Design

## Context

Estado observado: `pipeline.json` define `15-make-implementation-log` (requiere 11 y 14) y `16-make-sprint-report` (requiere 11 y 15, `por_sprint`); `projectcfg.py register --sprint N` y `current --sprint N` ya guardan una corrida por sprint. El plan de sprints aporta `gantt.json` (tareas `TAR-nn` con historia, sprint, fechas y responsable); el diseño del sistema, componentes, `TBL`, `UI` y `CP`; las historias, `HU` y `CA` con sus `REQ`; el paso 13, `data.json` con `estado` y `calculado` (`boards.calcular`); el paso 12, las ceremonias. El índice define 5.4, 6.1 a 6.3 (nueve puntos cada uno, con «pegar» y «texto») y el anexo A.3. El config tiene `modo_datos`, equipo con roles y los tres avances. Python de la biblioteca estándar.

## Goals / Non-Goals

**Goals:** registro real y trazable de cada sprint; informes con cifras verificables contra los tableros; sin repetición entre avances; una retrospectiva con acciones.

**Non-Goals:** análisis consolidado (6.4), resultados Lean, conclusiones, armado del informe, generar imágenes, ejecutar las skills.

## Decisions

### D1. Bitácora acumulada (`bitacora.md`)
Una corrida contiene todos los sprints registrados hasta ahora. `15` crea la bitácora con los sprints que el usuario indique; cada sprint nuevo se agrega con `15-make-implementation-log-update` (fork). Así `16` siempre lee una sola bitácora vigente.

### D2. Estructura de `bitacora.md`
`## 5.4. Implementación por módulos` con un `### 5.4.n. Módulo …` por módulo acordado con el usuario (`**Historias.**`, `**Componente.**`, `**Tablas.**`, `**Pantallas.**` citando `HU`, componente, `TBL` y `UI` existentes; toda historia con avance pertenece a un módulo). Después tres tablas:
- **Entradas:** `Código | Fecha | Sprint | HU | TAR | Módulo | Qué se hizo | Estado | Evidencia` (`BIT-nn`; estado `Terminado`, `En curso` o `Bloqueado`; fecha dentro del sprint; la `TAR` existe y es de la `HU`; la evidencia es un archivo de `evidencias/` o «—»).
- **Resultados de pruebas:** `CP | Sprint | Fecha | Resultado | Observación` (`CP` del diseño vigente; `Pasó`, `Falló` o `No ejecutado`; `Falló` exige observación).
- **Riesgos y cambios:** `Código | Sprint | Fecha | Tipo | Descripción | Efecto en el plan | HU o TAR` (`RIE-nn`; tipo `Riesgo` o `Cambio`).

### D3. Evidencias
`evidencias/` guarda los archivos que el usuario aporta (capturas, exportes, fotos). La skill registra solo el nombre; la validación comprueba que cada evidencia citada exista y la skill avisa de las que nadie cita. El kit no genera imágenes.

### D4. Informe de avance (`informe-avance-N.md`)
Un archivo por sprint con `# Avance N · [proyecto]` y los nueve puntos `## 6.N.1. …` a `## 6.N.9. …` del índice. Cada punto lleva `**Pegar.**` (archivo de evidencia o «Sin captura») y/o `**Texto.**` según el índice. Los puntos 6.N.2 y 6.N.4 llevan además una línea `**Cifras.**` con los indicadores de `calculado` del tablero HTML vigente («al DD-MM-AAAA»): avance global y por sprint, tareas hechas y atrasadas (Gantt); WIP, tiempo de ciclo y rendimiento (Kanban). La corrida guarda una copia de ese `data.json` (el tablero vigente al generar el informe) para que el informe siga siendo válido cuando el tablero avance; la validación recalcula con `boards.calcular` sobre la copia y exige igualdad, y comprueba que el corte caiga dentro del sprint.

### D5. Puntos con trazabilidad
6.N.3: cada captura con pie «Figura X: HU-XX nombre (REQ-XX)»; las `HU` existen y los `REQ` son los de su origen. 6.N.7: «N de M pruebas pasaron» calculado con los resultados del sprint en la bitácora. 6.N.8: cita los `RIE` del sprint. 6.N.9: cita las `TAR` del siguiente sprint según el plan (copia en `data.json`) y las de sprints anteriores sin terminar; en el avance 3, solo los trabajos pendientes.

### D6. Sin repetición entre avances
Ningún párrafo de 8 o más palabras del informe es igual a uno del avance anterior del mismo proyecto; lo ya dicho se remite por número de punto («véase 6.1.4»). Lo extenso (tablas completas, exportes) va a los anexos A.1, A.2 y A.3.

### D7. Acta (`acta-review-retro.md`, anexo A.3)
`## Sprint Review` (fecha dentro del sprint, participantes del equipo del config, historias mostradas, comentarios y decisiones) y `## Sprint Retrospective` con tres tablas: `Qué fue bien`, `Qué mejorar` y `Acciones` (`Acción | Responsable | Sprint`; responsables del equipo; la última retrospectiva no tiene sprint siguiente y sus acciones van a «Trabajos futuros»). 6.N.5 y 6.N.6 resumen el acta sin copiarla.

### D8. Una corrida por sprint, secuencia
`16` se ejecuta una vez por sprint y se registra con `--sprint N`; el usuario indica N. `15` y `16` son skills independientes: `16` avisa si la bitácora vigente no tiene entradas del sprint N o si el corte del tablero HTML no cae en ese sprint, y ofrece `15-…-update` o `13-…-update`. No bloquea.

### D9. Códigos
`BIT-nn` y `RIE-nn`, únicos en toda la bitácora y definidos en la primera celda de sus tablas. Sin choque con los códigos existentes. El informe y el acta no definen códigos nuevos.

### D10. Fuentes
Sin referencias nuevas: Sprint Review y retrospectiva se apoyan en Schwaber y Sutherland (2020) y las métricas Kanban en Anderson (2010), ya verificadas. Máximo 1 o 2 citas por archivo.

### D11. Validación
`rules/implementation_log.py` (`PREFIJOS = ["BIT", "RIE"]`) resuelve plan, diseño e historias vigentes; `rules/sprint_report.py` resuelve además la bitácora, `data.json` del tablero y el informe del sprint anterior. Sin una fuente, un aviso por cada comprobación imposible.

### D12. `-update`
Patrón del cambio 1. `15`: agregar sprint, corregir o quitar una entrada, evidencia, mover una historia, resultados de pruebas, riesgos. `16`: cifras (resincronizar con el tablero vigente), evidencias, Review, retrospectiva, plan del siguiente avance. Avisa de los informes que citan los `BIT` o `RIE` cambiados y de los informes posteriores.

### D13. Prerrequisitos
`pipeline.json`: `16-make-sprint-report` requiere además `12-make-ceremonies-kanban` y `13-design-html-boards`. Solo avisos.

## Risks / Trade-offs

- [El usuario no recuerda lo que hizo] → la skill pregunta por historia y tarea del plan, no en abstracto.
- [Informes tres veces iguales] → regla de no repetición y remisión por número de punto.
- [Cifras que no coinciden con el tablero] → se recalculan con el mismo `boards.py` en la validación.
- [Evidencias sin archivo] → se valida su existencia; «Sin captura» es válido con motivo en la parte de texto.
- [Bitácora que crece] → se acumula por sprint, pero el informe solo muestra lo del sprint.

## Migration Plan

Se edita el prerrequisito de la skill 16 en `pipeline.json` y se registran dos carpetas en `validate_run.py`. Sin migración de datos.

## Open Questions

- Si más adelante conviene generar la bitácora desde el historial de git (por ahora la registra el usuario).
