# Design

## Context

Estado observado en `common/structure/model1.md`: capítulos 1, 3, 4, 6 y 7 (sin 2 ni 5), `4.1.2` y `4.1.3` repetidos, `3.2` y `3.3` duplicados («BLean» y «Lean Change Managment»), notas de trabajo dentro de los títulos 4.1.x y el capítulo 6 vacío. `apuntes.md` lista los 12 temas del equipo con responsables (innovación, Design Thinking, Lean, Scrum y Kanban, requerimientos, historias y backlog, criterios de aceptación, sprints y Gantt, Sprint Review, ceremonias y DoD, Kanban).

Lo que depende del índice (verificado): `make-design-thinking` lee `3.1.x` y los anexos B, D, E y F (`SKILL.md`, spec `design-thinking-package-generation`); `patch_run.py` parchea textos de `3.1.5.x` y D.3; el generador `build.py` y el paquete generado citan `5.1`, `5.2.3` y `5.4.2` del orden anterior. Contexto de uso: el equipo construye el sistema y entrega el documento en tres avances; el formato es libre. Motivación: ver `proposal.md`.

## Goals / Non-goals

**Goals:**
- Un índice con orden lógico, numeración sin huecos ni repeticiones y un esqueleto que se llene en tres avances sin reestructurar.
- Mantener intactas las secciones que usan las skills.

**Non-goals:**
- Redactar el contenido de los capítulos.
- Cambiar el playbook de Design Thinking, sus plantillas o el generador más allá de las tres referencias cruzadas.
- Asignar responsables dentro del índice (eso va en `apuntes.md`).

## Decisions

### D1. Orden: marco, innovación, plan, sistema, resultados
```
1 Empresa y problema -> 2 Marco -> 3 Innovacion (DT, Lean)
        -> 4 Gestion agil: PLAN -> 5 Sistema -> 6 Resultados: REAL -> 7 Conclusiones
```
El capítulo 2 explica las metodologías antes de aplicarlas. Lo planificado (capítulo 4) se separa del sistema construido (capítulo 5) y de lo ejecutado (capítulo 6): así se compara plan contra realidad. **Alternativa:** poner Scrum y Kanban antes de la innovación; descartada porque los requerimientos nacen del Design Thinking.

### D2. Design Thinking se queda en `3.1`
Las skills, la spec y el paquete ya generado usan `3.1.1` a `3.1.8`. Mover el Design Thinking obligaría a renumerar todo. El capítulo 2 nuevo se añade antes y el resto de capítulos cambia sin tocar el 3.1.

### D3. Dos Lean Canvas
El canvas inicial (1.3, con los 5 porqués) es una hipótesis; el validado (3.4) incorpora lo que cambió el Design Thinking. Es el uso habitual del canvas en Lean y responde a la duda de si el Design Thinking iba antes o después.

### D4. El Anexo A se reutiliza para evidencias de gestión ágil
Quitar la matriz de consistencia dejaría un anexo A vacío o forzaría renombrar B a F (rompe las skills). El Anexo A pasa a «Evidencias de gestión ágil» (exportes del Gantt y del Kanban, actas de Sprint Review y capturas de Trello), que el capítulo 6 necesita.

### D5. Marcas de avance
`[A1]`, `[A2]`, `[A3]`: avance en que el punto se completa; `+` si se actualiza después. Asignación inicial propuesta (el equipo la ajusta):

| Capítulo | Marca |
|---|---|
| 1, 2, 3 (incluido 3.1 a 3.4) | `[A1]` |
| 4 (Scrum, RF, RNF, historias, DoD, Gantt base, ceremonias, Kanban) | `[A1]`; backlog `[A1+]` |
| 5.3 Diseño de interfaz | `[A1+]` (parte del prototipo del Design Thinking) |
| 5.1 Arquitectura, 5.2 Modelo de datos | `[A2]` |
| 5.4 Implementación | `[A2+]` |
| 5.5 Pruebas | plan `[A2]`, resultados `[A3]` |
| 6.1, 6.2, 6.3 | `[A1]`, `[A2]`, `[A3]` |
| 6.4, 7 | `[A3]` |
| Referencias | `[A1+]` |

### D6. Plantilla de 6.1 a 6.3: nueve bloques
Resumen; Gantt actualizado (captura del progreso y desvíos con causa); incremento del sistema (capturas con pie `Figura X: HU-05 Registrar venta (REQ-01)`); tablero Kanban (captura con fecha, WIP y métricas: tareas terminadas por semana y tiempo medio); Sprint Review; retrospectiva (qué fue bien, qué mejorar, qué cambiamos); pruebas; riesgos y cambios (enlaza con Lean Change); plan del siguiente avance. Cada bloque lleva una nota de qué pegar y qué texto escribir. 6.4 consolida solo en el final (cumplimiento de objetivos, métricas acumuladas, Gantt real contra base, validación con usuarios y discusión).

### D7. Notas de trabajo fuera de los títulos
Las dudas sobre herramientas (MCP de Trello, Miro, un HTML para el Gantt) pasan a una sección «Decisiones pendientes» de `apuntes.md`; el título solo nombra el contenido. Así no se pierde la decisión y el índice queda limpio.

### D8. Referencias cruzadas
Nuevo destino: requerimientos `4.2`, diseño de interfaz `5.3`, pruebas del sistema `5.5`. Se cambian en el índice, en `build.py` y en el paquete generado. Como el generador con valores por defecto debe producir el paquete idéntico, ambos se editan a la vez y se verifica con la comparación existente.

### D9. Estructura del índice resultante
```
Control del documento: leyenda, historial de versiones, reglas
1  La empresa y el problema          1.1 a 1.6  (1.3 modelo de negocio inicial)
2  Marco metodologico                2.1 innovacion, 2.2 agil, 2.3 integracion, 2.4 glosario
3  Innovacion                        3.1 DT (3.1.1-3.1.8), 3.2 Lean Startup, 3.3 Lean Change, 3.4 canvas validado
4  Gestion agil (lo planificado)     4.1 Scrum, 4.2 RF, 4.3 RNF, 4.4 historias y backlog, 4.5 criterios y DoD,
                                     4.6 planificacion y Gantt base, 4.7 ceremonias, 4.8 Kanban
5  Desarrollo del sistema            5.1 arquitectura, 5.2 datos, 5.3 interfaz, 5.4 implementacion, 5.5 pruebas
6  Resultados y avance (lo real)     6.1 avance 1, 6.2 avance 2, 6.3 avance final, 6.4 analisis consolidado
7  Conclusiones y recomendaciones
Referencias bibliograficas · Anexos A a F
```

## Risks / Trade-offs

- [Las marcas de avance son una suposición mía] → Se proponen como valores iniciales y el equipo las ajusta en el historial de versiones.
- [Alguien renumera el 3.1 o los anexos y rompe las skills] → La spec lo declara restricción y el índice lo avisa en su leyenda.
- [Referencias cruzadas olvidadas en otros documentos] → Búsqueda de `5.1`, `5.2.3` y `5.4.2` como verificación final.
- [Un capítulo 4 y un capítulo 5 pueden parecer solapados] → Se distingue por contenido: 4 es planificación y gestión; 5 es el producto técnico.

## Open Questions

- Fechas de los tres avances (se anotan en el historial de versiones cuando se conozcan; no cambia la estructura).
- Si los temas de dominio (informalidad empresarial, inventario, fichas de tallaje) deben ir al glosario 2.4; se decide al redactar el capítulo 2.
