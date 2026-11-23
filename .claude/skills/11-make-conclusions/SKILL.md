---
name: 11-make-conclusions
description: Redacta el capítulo 5 del informe de Inteligencia de Negocios en project/11-conclusions/ (secciones/5.md): una conclusión CNC-nn por cada objetivo específico y una por el general, con su estado (cumplido, parcial, no cumplido o sin meta) calculado del valor real de valores.json frente a la meta de 2.5 según el sentido del indicador, con su respaldo en cifras; recomendaciones REC-nn accionables ligadas a una conclusión, con quién decide y el KPI que mostrará si funcionó; lecciones aprendidas LEC-nn del proceso y la limitación de los datos generados. Si un KPI no tiene meta no concluye su cumplimiento ni la inventa. Muestra los estados calculados y un plan, espera la confirmación y valida. Úsala después de 10-make-storytelling o cuando el usuario pida "11-make-conclusions", "conclusiones", "recomendaciones", "lecciones aprendidas" o "cerrar el informe". Para cambiar uno ya creado usa 11-make-conclusions-update.
---

# 11-make-conclusions

Cierra el informe: contrasta lo que el dashboard midió con los objetivos del proyecto (punto 1.10), recomienda qué hacer y deja lo aprendido. La rúbrica pide conclusiones respaldadas por los resultados, recomendaciones accionables y lecciones aprendidas.

**El estado de cada objetivo se calcula, no se opina.** Sale del valor real de `valores.json` (lo midió el equipo en Power BI) frente a la meta de 2.5. **Nunca escribe una cifra que no esté en `valores.json`, no concluye el cumplimiento de un KPI sin meta ni la inventa, y no redondea un valor «cercano» a «cumplido».**

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/11-conclusions/guia.md` (playbook: fuentes, regla del estado, conclusiones, recomendaciones, lecciones, errores y checklist).
2. `common/11-conclusions/models/README.md` y la plantilla `cn-1-seccion-5.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`: `OG`, `OE` con su indicador, usuarios y decisiones), `modelo.json` y 2.5 de la corrida vigente de `07-make-data-model-kpi` (qué KPI mide cada objetivo y su meta), **`valores.json` de la corrida vigente de `09-make-dashboard`**, la corrida vigente de `05-make-problem-objectives` (problemática y matriz), la de `10-make-storytelling` si existe (hallazgos `HLZ-nn` citables), `project/domain.md` y el config (`modo_datos`).

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/rules/conclusions.py estados [--json]` (estado calculado de cada KPI, de cada objetivo específico y del general, con su valor real y su meta)
- `python3 .claude/skills/_shared/brief.py leer`
- `python3 .claude/skills/_shared/runs.py new --step 11-make-conclusions`
- `python3 .claude/skills/_shared/validate_run.py <corrida>` (reglas en `.claude/skills/_shared/rules/conclusions.py`).

## Reglas

- **Sin `valores.json` te detienes.** Sin los valores reales del equipo no hay conclusiones: pide que se registren con `09-make-dashboard` y no redactes.
- **Sin `10` avisas y sigues.** Con los valores del dashboard alcanza; si existe `10`, puedes citar sus hallazgos `HLZ-nn`.
- **Una conclusión por objetivo:** una `CNC-nn` por cada `OE-nn` del brief y una por el `OG-nn`. El estado es el que imprime `rules/conclusions.py estados`; no lo cambies.
- **Respaldo en cifras:** una fila por cada KPI de cada objetivo específico, con el valor de `valores.json` y la meta de 2.5 tal cual.
- **Meta pendiente:** si un KPI no tiene meta, la conclusión de su objetivo dice que su cumplimiento no se puede concluir porque la meta está pendiente. La meta se propone con `09-make-dashboard` y se registra con `07-make-data-model-kpi-update`; después se actualiza esta sección con `11-make-conclusions-update`.
- **Recomendaciones accionables:** toda conclusión que no sea `Cumplido` tiene al menos una `REC-nn`, ligada a una `CNC-nn`, con quién decide (un usuario del brief) y el KPI de `modelo.json` que mostrará si funcionó.
- **Lecciones y limitaciones:** al menos una `LEC-nn` sobre el proceso, y con `modo_datos: generado` el párrafo `**Limitaciones.**` dice que los datos se generaron para el proyecto y que los resultados dependen de esa calibración.
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, califica los datos con los términos de `_shared/policy.json`; la procedencia va solo en `README.md`.
- **Contrato de la corrida:** `secciones/5.md` empieza con `## 5. Conclusiones, recomendaciones y lecciones aprendidas` y solo tiene texto final; cada tabla lleva antes `Tabla N: título`; las citas van a `referencias.md` (APA 7).

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 11-make-conclusions` y muestra los avisos (falta `10`: avisa y sigue). Corre `python3 .claude/skills/_shared/rules/conclusions.py estados`: si responde que falta `valores.json`, detente.
2. **Insumos.** Lee del brief los objetivos con su indicador y los usuarios; de `modelo.json`, los KPI con su meta; de la corrida de `05`, la problemática (punto 1.8); de `10`, si existe, los hallazgos.
3. **Estados.** Muestra al usuario la salida de `estados`: por cada objetivo, sus KPI con valor, meta y estado, y el estado del objetivo y del general. Señala los KPI sin meta y los objetivos que quedan `Sin meta`.
4. **Preguntas** (AskUserQuestion), solo lo que falte: quién decide la acción de cada recomendación cuando el brief admite más de un usuario, y qué lecciones del proceso quiere resaltar el equipo.
5. **Plan y confirmación.** Muestra una fila por conclusión (código, objetivo, estado, qué dirá), las recomendaciones propuestas (conclusión, acción, quién decide, KPI) y las lecciones; comprueba que toda conclusión que no es `Cumplido` tiene una recomendación. **Espera la confirmación.**
6. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 11-make-conclusions)`. Escribe `$RUN/secciones/5.md` con la plantilla `cn-1-seccion-5.md`, `$RUN/referencias.md` si hay citas y `$RUN/README.md` (modo de datos, corridas de origen de `01`, `07`, `09` y `10`, y las metas que siguen pendientes).
7. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole la ruta de `$RUN/secciones/5.md` y los datos propios del caso (valores reales, metas y estados); aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después, `python3 .claude/skills/_shared/validate_run.py $RUN` hasta que no haya incidencias.
8. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 11-make-conclusions --run <carpeta>` (marca la sección 5 como disponible). Si responde `"movido": false`, díselo al usuario.
9. **Cierre.** Entrega la ruta, un resumen (estado de cada objetivo, recomendaciones y metas pendientes con la skill que las cierra) y sugiere `12-make-report` para armar el informe completo.
