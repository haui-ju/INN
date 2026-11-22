# Tasks

## 1. Base de comparación y cabecera del índice

- [x] 1.1 Guardar en una carpeta temporal una copia del índice actual, de los puntos 3.1.1 a 3.1.8 y de los anexos B, D, E y F; verificar que la copia existe y que contiene los ocho puntos 3.1.x y los cuatro anexos
- [x] 1.2 Escribir al inicio de `common/structure/model1.md` la cabecera de control: leyenda de marcas `[A1]`, `[A2]`, `[A3]` y `+`, historial de versiones (tres filas: avance 1, avance 2 y final, con fecha y cambios en blanco) y reglas de contenido (no repetir, lo grande a anexos, pie de foto con código, cifras con fecha, aviso de que 3.1.x y los anexos B a F no se renumeran); verificar que las cuatro partes aparecen y que la tabla de versiones tiene tres filas

## 2. Capítulos 1 a 3

- [x] 2.1 Reescribir el capítulo 1 «La empresa y el problema» (1.1 a 1.6, con 1.3 como modelo de negocio inicial: 5 porqués y Lean Canvas v0), corrigiendo erratas y con marcas `[A1]`; verificar que no quedan «porques» ni «problemasticas» y que cada punto tiene marca
- [x] 2.2 Escribir el capítulo 2 «Marco metodológico» (2.1 innovación, 2.2 gestión ágil, 2.3 integración de las metodologías en el proyecto, 2.4 marco conceptual con glosario) con una nota breve de contenido por punto; verificar que son cuatro puntos numerados 2.1 a 2.4
- [x] 2.3 Reescribir el capítulo 3 «Innovación» conservando 3.1 (3.1.1 a 3.1.8) y añadiendo 3.2 Lean Startup, 3.3 Lean Change Management y 3.4 Lean Canvas validado con sus subpuntos y notas; verificar con una comparación de texto que 3.1.1 a 3.1.8 solo difieren de la copia en las referencias cruzadas y en las marcas de avance

## 3. Capítulos 4 a 7

- [x] 3.1 Escribir el capítulo 4 «Gestión ágil: lo planificado» (4.1 Scrum, 4.2 requerimientos funcionales, 4.3 no funcionales, 4.4 historias y Product Backlog, 4.5 criterios de aceptación y DoD, 4.6 planificación de sprints y Gantt línea base, 4.7 ceremonias, 4.8 Kanban diseño) sin notas de trabajo en los títulos; verificar que no hay números repetidos ni paréntesis con decisiones de herramientas
- [x] 3.2 Escribir el capítulo 5 «Desarrollo del sistema» (5.1 arquitectura, 5.2 modelo de datos, 5.3 diseño de interfaz, 5.4 implementación por módulos y sprints, 5.5 pruebas y validación) con marcas de avance; verificar que 5.3 y 5.5 existen, pues son el destino de las referencias cruzadas
- [x] 3.3 Escribir el capítulo 6 «Resultados y avance» con 6.1, 6.2 y 6.3, cada uno con los mismos nueve bloques y su nota de qué pegar, y 6.4 análisis consolidado; verificar que los tres avances tienen nueve bloques idénticos en el mismo orden
- [x] 3.4 Escribir el capítulo 7 y mantener Referencias bibliográficas; verificar que 7.1 a 7.3 existen y que los capítulos van de 1 a 7 sin saltos

## 4. Anexos

- [x] 4.1 Reemplazar el Anexo A por «Evidencias de gestión ágil» (A.1 Gantt y cronograma, A.2 tablero Kanban, A.3 actas de Sprint Review y retrospectiva, A.4 capturas de herramientas) y conservar B, C, D, E y F con sus subpuntos; verificar con la copia de la tarea 1.1 que los textos de B, D, E y F son idénticos
- [x] 4.2 Añadir marcas de avance a los anexos; verificar que cada anexo y subanexo tiene marca

## 5. Referencias cruzadas

- [x] 5.1 Actualizar en el índice las referencias a `5.1`, `5.2.3` y `5.4.2` por `4.2`, `5.3` y `5.5`; verificar con `grep` que no quedan las antiguas en `model1.md`
- [x] 5.2 Actualizar las mismas referencias en `.claude/skills/make-design-thinking/scripts/reference/build.py` y en `project/design-thinking/10-11-2026-00-00-46/` (documento y anexos); verificar generando el paquete por defecto en una carpeta temporal y comprobando con `diff -r` que es idéntico al del proyecto
- [x] 5.3 Comprobar que `patch_run.py` y `read_run.py` siguen funcionando sobre el paquete actualizado; verificar ejecutando `read_run.py` y `patch_run.py --dry-run` sobre una copia temporal

## 6. Decisiones pendientes y apuntes

- [x] 6.1 Mover a `apuntes.md` las notas de trabajo de los títulos del Gantt y del Kanban (MCP, Miro, HTML, Trello) bajo una sección «Decisiones pendientes» y añadir la correspondencia entre los 12 temas del equipo y los puntos del nuevo índice; verificar que las notas ya no están en `model1.md` y sí en `apuntes.md`

## 7. Verificación final

- [x] 7.1 Ejecutar una comprobación de numeración sobre `model1.md` (ningún título numerado repetido, secuencia consecutiva por nivel, todos los puntos con marca de avance); verificar que el script no reporta incidencias
- [x] 7.2 Ejecutar `openspec validate reorder-report-index --strict` y `grep` de las referencias antiguas en el repositorio; verificar que la validación pasa y que no hay coincidencias fuera de `openspec/changes/archive`

## Workflow follow-up

- Archivar el cambio cuando se cumplan los requisitos de revisión del proyecto, de modo que `report-index-structure` pase a `openspec/specs/`.
- Completar el historial de versiones con las fechas reales de los tres avances.
