---
name: 04-make-strategic-analysis
description: Redacta las secciones 1.5 a 1.7 del informe de Inteligencia de Negocios en project/04-strategic-analysis/ (secciones/1.5.md a 1.7.md): análisis PESTEL con efecto en el negocio y fuente por hallazgo, matriz FODA con evidencia y estrategias cruzadas FO, FA, DO y DA, y diagrama de Ishikawa cuyo efecto es el problema del brief con causas por categorías 6M, cada una con su figura HTML (pestel, foda, ishikawa). Articula el PESTEL con el FODA y el FODA con el Ishikawa, muestra un plan y espera la confirmación antes de escribir. Úsala después de 03-make-business-diagnosis o cuando el usuario pida "04-make-strategic-analysis", "PESTEL", "FODA", "estrategias cruzadas", "Ishikawa" o "análisis estratégico". Para cambiar uno ya creado usa 04-make-strategic-analysis-update.
---

# 04-make-strategic-analysis

Analiza el entorno y la problemática del negocio: PESTEL (1.5), matriz FODA con estrategias cruzadas (1.6) e Ishikawa (1.7). La rúbrica pide integrar FODA, PESTEL, Canvas e Ishikawa con la problemática bien definida; `05-make-problem-objectives` cita estos códigos en su matriz de articulación.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/04-strategic-analysis/guia.md` (playbook: fuentes, contrato de la corrida, códigos, articulación, PESTEL, FODA, estrategias, Ishikawa 6M, errores y checklist).
2. `common/04-strategic-analysis/models/README.md` y las plantillas `sa-1-pestel.md`, `sa-2-foda.md` y `sa-3-ishikawa.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`), la corrida vigente de `03-make-business-diagnosis` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 03-make-business-diagnosis`), `project/domain.md` y el config.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/diagnostico.py` (`titulos`, `leer --paso …`)
- `python3 .claude/skills/_shared/visuales.py construir --visual <pestel|foda|ishikawa> --run <corrida> --carpeta <corrida>/visuales [--diseno <tokens.json>]`
- WebSearch y WebFetch para verificar los hallazgos del PESTEL (instituciones oficiales, normas).
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/strategic_analysis.py`).

## Reglas

- **El efecto del Ishikawa es el problema principal del brief, copiado sin cambios.** Si el usuario quiere otro problema, indica `01-make-project-brief-update`.
- **Ninguna cifra externa sin fuente verificada.** Busca cada hallazgo del PESTEL, muéstralo con su fuente y su año; si no se encuentra, se reformula sin cifra o se deja fuera. Las fuentes internas se nombran con su año. Con `modo_datos: real`, solo lo que informa el usuario o lo verificado.
- **Articulación:** oportunidades y amenazas citan el código PESTEL del que salen (o una fuente con año); fortalezas y debilidades se apoyan en el Canvas y los registros de la empresa; las causas del Ishikawa citan la debilidad o amenaza que las respalda.
- **Estrategias cruzadas:** al menos una FO, FA, DO y DA; cada una combina los códigos de los dos cuadros que su tipo indica.
- **Códigos** (`POL`, `ECO`, `SOC`, `TEC`, `AMB`, `LEG`, `FOR`, `DEB`, `OPO`, `AME`, `FO`, `FA`, `DO`, `DA`, `CAU`): numerados por prefijo, sin repetir.
- **Contrato de la corrida:** cada `secciones/<punto>.md` empieza con su encabezado exacto y solo tiene texto final; cada figura es la línea `<!-- figura: <visual> -->`; los visuales se generan con `visuales.py`, nunca a mano; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 04-make-strategic-analysis` y muestra los avisos. Si falta la corrida de `03`, avisa que el FODA no podrá apoyarse en el Canvas y pregunta si continúa. Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `04-make-strategic-analysis-update`.
2. **Insumos.** Lee el brief (problema, evidencia, fuentes), la corrida de `03` (industria, competencia, Canvas) y `domain.md`. Muéstrale al usuario el problema que será el efecto del Ishikawa.
3. **Investigación del entorno.** Por cada factor PESTEL busca uno a tres hallazgos que afecten a esta empresa y muéstralos con su fuente y año.
4. **Preguntas** (AskUserQuestion), solo lo que falte: fortalezas o debilidades que solo conoce el equipo, competidores concretos, hechos observados en el negocio.
5. **Plan y confirmación.** Muestra en líneas cortas: hallazgos PESTEL (código, factor, tipo, fuente), los cuatro cuadros del FODA con su evidencia, las estrategias (código, tipo, combina) y las causas del Ishikawa por categoría con su evidencia. **Espera la confirmación.**
6. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 04-make-strategic-analysis)` y escribe en `$RUN/secciones/` los archivos `1.5.md`, `1.6.md` y `1.7.md` con las plantillas; `$RUN/referencias.md` y `$RUN/README.md` (modo de datos, fuentes verificadas, qué propuso el agente y qué confirmó el usuario).
7. **Figuras.** Para `pestel`, `foda` e `ishikawa`: `python3 .claude/skills/_shared/visuales.py construir --visual <visual> --run <corrida> --carpeta $RUN/visuales` (con `--diseno` si hay sistema de diseño vigente).
8. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias; si cambias una tabla, vuelve a construir su figura.
9. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 04-make-strategic-analysis --run <carpeta>` (marca 1.5 a 1.7 como disponibles). Si responde `"movido": false`, díselo al usuario.
10. **Cierre.** Entrega la ruta, un resumen por sección (cuántos hallazgos, ítems, estrategias y causas), las fuentes externas usadas, cómo abrir los tres HTML para copiar las imágenes, y sugiere `05-make-problem-objectives`.
