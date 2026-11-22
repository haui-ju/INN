# Design

## Context

Ver `proposal.md` (Why). Estado del que parte:

- `pipeline.json` declara `10-make-storytelling` (sección 4, carpeta `10-storytelling`, requiere 09) y `11-make-conclusions` (sección 5, carpeta `11-conclusions`, requiere 05 y 10), ambas con `update: true`. El índice marca la sección 4 con «(incluye imagen)»; la 5 no lleva imagen.
- `bi-chapter3-build` entrega `valores.json` y `capturas/` en la corrida de `09-make-dashboard`, y el marcador `<!-- captura: <id> -->` en `12-make-report`. Este change se aplica después.
- El brief fija los objetivos `OG` y `OE` con su indicador, los usuarios (dueño y jefe de cocina) y las decisiones que el dashboard apoya. `modelo.json` trae las metas de los KPI; KPI-02 y KPI-06 pueden seguir «Pendiente».
- `modo_datos` es `generado`.

## Goals / Non-Goals

**Goals:**
- Que las secciones 4 y 5 digan solo lo que los valores reales muestran, y que cada objetivo tenga su hallazgo y su conclusión.
- Que el informe quede completo (cinco capítulos y anexos A a D) y sin listas de faltantes.

**Non-Goals:**
- Medir nada ni abrir Power BI: los valores son entrada del equipo.
- Cambiar el modelo, los KPI o sus metas: eso lo hacen `07-make-data-model-kpi-update` y `09-make-dashboard`.
- Generar gráficos nuevos: el relato usa las capturas del dashboard.

## Decisions

**D1. Una skill por capítulo, como declara `pipeline.json`.** 10 cuenta qué muestran los datos y qué decisión apoyan; 11 contrasta con los objetivos y cierra. Separarlas permite corregir un valor y rehacer solo el relato, o ajustar una recomendación sin tocar los hallazgos.

**D2. `valores.json` es la única fuente de cifras.** El validador extrae las cifras de cada hallazgo y conclusión y las compara con `valores.json`; una cifra que no está falla. Alternativa descartada: confiar en la redacción de la skill, que es justo donde se cuelan cifras inventadas.

**D3. Un hallazgo por captura que lo sostiene.** Cada `HLZ-nn` cita una captura de `09-make-dashboard` (marcada con `<!-- captura: <id> -->`), de modo que el informe muestra lo que el dueño verá y no hay figura sin hallazgo ni hallazgo sin evidencia visual.

**D4. Estado de cumplimiento calculado, no opinado.** La conclusión de cada `OE` toma «cumplido», «parcial» o «no cumplido» al comparar el valor real con la meta del KPI según el sentido del indicador (mayor es mejor para el margen, menor es mejor para la merma). Sin meta, la conclusión declara que no se puede concluir (escenario «KPI sin meta»). Alternativa descartada: redondear a «cumplido» cuando el valor se acerca a la meta.

**D5. Códigos propios.** `HLZ-nn`, `CNC-nn`, `REC-nn` y `LEC-nn`, que reutilizan `OE`, `OG` y `KPI`. No chocan con los prefijos de las skills activas, y se agregan a `PREFIJOS` de cada validador.

**D6. Limitación de datos generados declarada dos veces.** En la sección 4 (al empezar) y en la 5 (como limitación). Es una condición de honestidad del informe: los hallazgos describen un caso calibrado, no un negocio real.

**D7. Las recomendaciones terminan en un indicador.** Cada `REC-nn` nombra quién decide y qué KPI mostrará si funcionó, para que el cierre vuelva a los KPI del capítulo 2 y no sean consejos sueltos.

## Risks / Trade-offs

- **Los valores reales cambian después de redactar** → `09-make-dashboard-update` lo propaga: `10-make-storytelling-update` y `11-make-conclusions-update` actualizan solo lo que cita el valor cambiado, y el validador lo detecta si no se hizo.
- **Todas las conclusiones salen «no cumplido» o «cumplido» por la calibración de los datos** → es una consecuencia de los datos generados; por eso la limitación se declara y la guía pide explicar qué mostró cada KPI, no solo el estado.
- **Metas pendientes bloquean conclusiones** → se cierran antes con `07-make-data-model-kpi-update` (propuestas por `09-make-dashboard`); si siguen pendientes, la conclusión lo dice.

## Migration Plan

No hay corridas previas. Se aplica después de `bi-chapter3-build`: primero `10` con su validador y sus pruebas, luego `11`, y al final la integración con el informe completo.

## Open Questions

Ninguna.
