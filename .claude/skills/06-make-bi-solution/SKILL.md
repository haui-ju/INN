---
name: 06-make-bi-solution
description: Redacta las secciones 2.1 a 2.3 del informe de Inteligencia de Negocios en project/06-bi-solution/ (secciones/2.1.md a 2.3.md): la propuesta de solución (decisiones que apoya, usuarios y cómo responde a la problemática y a cada objetivo específico), la arquitectura de BI en cuatro capas (fuentes, ETL, almacenamiento y visualización) con su figura HTML arquitectura-bi, y las herramientas elegidas con su función, justificación y alternativa descartada (Power BI fijo; ETL y almacenamiento pueden quedar «Pendiente»). Lee el brief y el capítulo 1, muestra un plan y espera la confirmación antes de escribir. Úsala después de 05-make-problem-objectives o cuando el usuario pida "06-make-bi-solution", "propuesta de solución", "arquitectura de BI", "capas de la solución" o "herramientas del proyecto". Para cambiar uno ya creado usa 06-make-bi-solution-update.
---

# 06-make-bi-solution

Abre el capítulo 2: define qué solución de BI se propone, con qué arquitectura y con qué herramientas. La rúbrica pide una arquitectura clara, herramientas sustentadas y una solución articulada a los objetivos; `07-make-data-model-kpi` toma de aquí las fuentes y el almacenamiento para modelar.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/06-bi-solution/guia.md` (playbook: fuentes, contrato de la corrida, códigos, propuesta, capas, herramientas, errores y checklist).
2. `common/06-bi-solution/models/README.md` y las plantillas `bs-1-propuesta.md`, `bs-2-arquitectura.md` y `bs-3-herramientas.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`), la corrida vigente de `05-make-problem-objectives` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 05-make-problem-objectives`), `project/domain.md` y el config.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/diagnostico.py` (`titulos`, `leer --paso …`)
- `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <corrida> --carpeta <corrida>/visuales [--diseno <tokens.json>]`
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/bi_solution.py`).

## Reglas

- **Las cuatro capas, en este orden:** Fuentes, ETL, Almacenamiento y Visualización, con al menos un componente por capa. Cada `FUE-nn` del brief es un componente de la capa de fuentes; no se agregan fuentes que el brief no tenga (si hace falta una, indica `01-make-project-brief-update`).
- **Cada `OE` del brief aparece en la tabla de 2.1** con los `CAP-nn` de 2.2 que lo atienden.
- **Herramientas sustentadas:** función, justificación con un criterio y alternativa descartada. **Power BI** va en la capa de visualización. La herramienta de **ETL** y la de **almacenamiento** pueden quedar «Pendiente» con su motivo si el usuario aún no decide; en otra capa no se acepta. Nunca elijas por el usuario una herramienta pendiente: propón opciones y deja que decida.
- **Códigos** `CAP-nn` y `HER-nn`: numerados por prefijo, sin repetir.
- **Contrato de la corrida:** cada `secciones/<punto>.md` empieza con su encabezado exacto y solo tiene texto final; solo 2.2 lleva figura, la línea `<!-- figura: arquitectura-bi -->`; el HTML se genera con `visuales.py`, nunca a mano; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 06-make-bi-solution` y muestra los avisos. Si falta la corrida de `05-make-problem-objectives`, avisa que la propuesta no podrá citar la problemática ni las causas principales, indica ejecutarla y pregunta si continúa solo con el brief. Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `06-make-bi-solution-update`.
2. **Insumos.** Lee del brief las decisiones, los usuarios, las fuentes `FUE-nn`, los `OE-nn` y las herramientas previstas del alcance, y de `05` la problemática y las causas principales.
3. **Preguntas** (AskUserQuestion), solo lo que falte: qué herramienta usará el equipo para el ETL y para el almacenamiento (o «todavía no se decide»), si hay una herramienta impuesta y dónde se publicará el dashboard. Si el usuario no decide, propón dos o tres opciones con su criterio.
4. **Plan y confirmación.** Muestra en líneas cortas: decisiones y usuarios, los componentes por capa (código, nombre y qué `FUE` atiende), las herramientas (código, capa, elección o «Pendiente», alternativa) y una fila por `OE` con sus componentes. **Espera la confirmación.**
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 06-make-bi-solution)` y escribe en `$RUN/secciones/` los archivos `2.1.md`, `2.2.md` y `2.3.md` con las plantillas (conviene redactar 2.2 primero para fijar los `CAP-nn`); `$RUN/referencias.md` si hay citas y `$RUN/README.md` (modo de datos, corridas de origen de `01` y `05`, qué propuso el agente y qué confirmó el usuario, herramientas pendientes).
6. **Figura.** `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <corrida> --carpeta $RUN/visuales` (con `--diseno` si hay sistema de diseño vigente).
7. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias; si cambias la tabla de 2.2 o 2.3, vuelve a construir la figura.
8. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 06-make-bi-solution --run <carpeta>` (marca 2.1 a 2.3 como disponibles). Si responde `"movido": false`, díselo al usuario.
9. **Cierre.** Entrega la ruta, un resumen por sección (componentes por capa, herramientas y cuáles quedan «Pendiente»), cómo abrir el HTML de la figura para copiar la imagen y, si hay herramientas pendientes, que se completan con `06-make-bi-solution-update` y deben resolverse antes de entregar el informe. Sugiere `07-make-data-model-kpi`.
