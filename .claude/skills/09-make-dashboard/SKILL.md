---
name: 09-make-dashboard
description: Prepara el dashboard del capítulo 3 del informe de Inteligencia de Negocios y redacta la sección 3.2 y los anexos C y D en project/09-dashboard/ (secciones/3.2.md, anexos/C.md y anexos/D.md): propone las páginas (pregunta de negocio, usuario del brief, visualizaciones, filtros y KPI) y las medidas DAX de cada KPI desde modelo.json, se las entrega al equipo para que las construya en Power BI y, cuando el equipo trae el valor real de cada KPI (valores.json) y una captura por página (capturas/pag-nn.png), redacta 3.2 (páginas, capturas y valor real frente a la meta), el anexo C (medidas DAX finales) y el anexo D (especificación por página), propone la meta de los KPI que siguen pendientes y valida. No abre Power BI ni inventa ningún valor. Úsala después de 08-make-etl o cuando el usuario pida "09-make-dashboard", "dashboard", "páginas del dashboard", "medidas DAX" o "capturas del dashboard". Para cambiar uno ya creado usa 09-make-dashboard-update.
---

# 09-make-dashboard

Prepara y documenta la construcción del dashboard (3.2 y anexos C y D). **El equipo construye el dashboard en Power BI**; esta skill tiene dos mitades: antes de la construcción entrega la especificación de páginas y las medidas propuestas, y después de ella, cuando el equipo trae sus valores y capturas, redacta. **Nunca escribe un valor del dashboard que el equipo no haya entregado.**

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/09-dashboard/guia.md` (playbook: fuentes, dos mitades, contrato de la corrida, páginas, medidas, valores y capturas, errores y checklist).
2. `common/09-dashboard/models/README.md` y las plantillas `ds-1-paginas.md`, `ds-2-medidas.md`, `ds-3-especificacion.md` y `ds-4-valores-json.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`: usuarios, decisiones y objetivos), `modelo.json` y 2.5 de la corrida vigente de `07-make-data-model-kpi`, la corrida vigente de `08-make-etl`, `project/domain.md` y el config.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/dashboard_dax.py <modelo.json>` (medidas DAX propuestas: una base por campo y una por KPI; lo que no pudo relacionar queda como `¡revisar!`)
- `python3 .claude/skills/_shared/dashboard_ref.py plan|construir --run <corrida>` (plan de páginas por defecto y dashboard de referencia con su guía; lee `data/respuestas/`, `modelo.json` y los tokens del diseño)
- `python3 .claude/skills/_shared/diagnostico.py leer --paso 07-make-data-model-kpi`
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/dashboard.py`).

## Reglas

- **No ejecutas nada en Power BI.** Propones; el equipo construye, prueba las medidas y trae los resultados. No digas que una medida «funciona» ni que una página «ya está» hasta que el equipo lo entregue.
- **Sin `modelo.json` te detienes.** Las medidas y los KPI salen de él; el DAX cita solo sus tablas y campos. Si un KPI necesita un campo que no existe, el cambio se hace con `07-make-data-model-kpi-update`.
- **Cada KPI del modelo está en una página**; cada página tiene una pregunta de negocio, un usuario **del brief**, visualizaciones y filtros.
- **Los valores salen solo de `valores.json`**, con los decimales del dashboard; la meta es la de 2.5 y el estado (`Cumple`, `No cumple`, `Sin meta`) se calcula con su comparador. Sin valores o sin la captura de una página, **no escribes 3.2 ni los anexos**.
- **Metas pendientes:** con el valor real de un KPI sin meta, propón una meta con su justificación y **pide confirmación**; no la escribas en 2.5. Se registra con `07-make-data-model-kpi-update`, y después el equipo actualiza `valores.json`.
- **El anexo C lleva la medida final del equipo** (la que se ejecutó), sin marcas `revisar`.
- **Las capturas se marcan una vez**, en 3.2, con `<!-- captura: pag-nn -->`; el anexo D describe cada página sin repetir la marca.
- **Códigos** `PAG` y `MED`: numerados por prefijo, sin repetir. **Contrato de la corrida:** `secciones/3.2.md` empieza con su encabezado exacto y solo tiene texto final; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

### Primera mitad: materiales para el equipo
1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 09-make-dashboard` y muestra los avisos. Si falta `modelo.json` de `07-make-data-model-kpi`, detente. Si falta la corrida de `08-make-etl`, avisa que no habrá valores reales cargados y pregunta si continúa solo con la especificación. Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `09-make-dashboard-update`.
2. **Insumos.** Lee del brief los usuarios, las decisiones y los `OE-nn`; de `modelo.json`, los KPI con su meta y sus campos de origen y las dimensiones (para los filtros).
3. **Preguntas** (AskUserQuestion), solo lo que falte: qué quiere ver cada usuario primero y si hay un filtro que el negocio exige.
4. **Plan y confirmación.** Muestra una fila por página (código, nombre, pregunta, usuario, visuales, filtros, KPI) y comprueba que todos los KPI estén cubiertos. **Espera la confirmación.**
5. **Entrega al equipo.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 09-make-dashboard)`. Escribe en `$RUN/materiales/paginas.json` el plan confirmado (`dashboard_ref.py plan --run $RUN` copia el plan por defecto del caso para ajustarlo; sigue la plantilla `ds-5-paginas-json`) y ejecuta `python3 .claude/skills/_shared/dashboard_ref.py construir --run $RUN`: deja `dashboard-referencia.html` (cómo debería verse cada página, con los valores esperados), `guia-dashboard.md` (una sección por página y, dentro, un bloque por elemento —segmentadores, cada tarjeta de KPI y cada gráfico— con qué muestra, cómo se calcula, tablas y columnas de origen, fórmula DAX, pasos en Power BI y valor esperado; cada medida y cada columna calculada se explica en el primer elemento que la usa) y los `.txt` de páginas y medidas. Muestra la ruta del HTML, resume la guía en la conversación y explica que el equipo compara sus resultados con los valores esperados (el pronóstico no coincidirá exactamente). Si `data/respuestas/` no existe, indica que primero se generan los datos con `08-make-etl`. Termina con la lista de lo que debe traer: el valor real de cada KPI con su unidad y su periodo, una captura por página y las medidas finales si cambiaron. **Detente aquí.** Reanuda cuando el equipo lo entregue.

### Segunda mitad: redacción con lo que el equipo entregó
6. **Recibir la entrega.** Escribe `$RUN/valores.json` con los valores tal como el equipo los dio (plantilla `ds-4-valores-json.md`) y copia las capturas a `$RUN/capturas/pag-nn.png`. Si falta el valor de un KPI o la captura de una página, pídelos; no redactes. Un valor que muestra una página sin captura no se cita.
7. **Metas pendientes.** Para cada KPI sin meta, propón una meta desde su valor real con su justificación y espera la confirmación del usuario. No edites 2.5: indica que se cierra con `07-make-data-model-kpi-update`.
8. **Escritura.** Escribe en `$RUN/secciones/3.2.md`, `$RUN/anexos/C.md` (con las medidas finales del equipo) y `$RUN/anexos/D.md` con las plantillas, `$RUN/referencias.md` si hay citas y `$RUN/README.md` (modo de datos, corridas de origen de `01`, `07` y `08`, qué propuso la skill y qué entregó el equipo, metas pendientes).
9. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole las rutas de `$RUN/secciones/3.2.md` y `$RUN/anexos/*.md` y los datos propios del caso; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después, `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (páginas, KPI cubiertos, capturas, valores y estados, medidas y anexos).
10. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 09-make-dashboard --run <carpeta>` (marca 3.2 como disponible). Si responde `"movido": false`, díselo al usuario.
11. **Cierre.** Entrega la ruta, un resumen (páginas, KPI con su valor y estado), las metas pendientes y la skill que las cierra, y recuerda que cada captura se pega en su marcador del informe. Sugiere `12-make-report` para ver el avance.
