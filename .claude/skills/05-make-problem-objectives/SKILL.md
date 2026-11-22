---
name: 05-make-problem-objectives
description: Redacta las secciones 1.8 a 1.10 del informe de Inteligencia de Negocios en project/05-problem-objectives/ (secciones/1.8.md a 1.10.md): la problemática central con sus causas principales tomadas del Ishikawa y su evidencia, el objetivo general y los objetivos específicos copiados del brief sin volver a proponerlos, y una matriz de articulación que vincula cada objetivo específico con causas del Ishikawa, ítems y estrategias FODA, hallazgos PESTEL, bloques del Canvas y su indicador. Propone las causas principales y la matriz, y espera la confirmación antes de escribir. Úsala después de 04-make-strategic-analysis o cuando el usuario pida "05-make-problem-objectives", "problemática central", "objetivos en el informe", "matriz de articulación" o "cerrar el capítulo 1". Para cambiar uno ya creado usa 05-make-problem-objectives-update.
---

# 05-make-problem-objectives

Cierra el capítulo 1: define la problemática central con sus causas principales, reproduce los objetivos del brief y demuestra, con la matriz de articulación, que cada objetivo responde al diagnóstico (lo que la rúbrica llama «todos los elementos articulados a los objetivos del proyecto y sustentados»).

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/05-problem-objectives/guia.md` (playbook: fuentes, objetivos copiados, causas principales, matriz de articulación, errores y checklist).
2. `common/05-problem-objectives/models/README.md` y las plantillas `po-1-problematica.md`, `po-2-objetivo-general.md` y `po-3-objetivos-especificos.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`) y las corridas vigentes de `03` y `04` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 03-make-business-diagnosis` y `--paso 04-make-strategic-analysis`).

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/diagnostico.py` (`titulos`, `leer --paso …`)
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/problem_objectives.py`).

## Reglas

- **Los objetivos no se vuelven a proponer:** `OG-01` y los `OE-nn` se copian del brief sin cambios. Si el usuario quiere cambiar uno, indica `01-make-project-brief-update` y vuelve a ejecutar esta skill o su `-update`.
- **Las causas principales salen del Ishikawa vigente** (de dos a cuatro), con su código, categoría y texto iguales; el criterio es su peso en el problema y que se puedan medir con datos.
- **La matriz articula todo:** una fila por `OE` con causas, ítems o estrategias FODA, hallazgos PESTEL (o «—»), bloques del Canvas por su nombre exacto e indicador del brief; cada causa principal queda atendida por algún objetivo. Si una no lo está, propón al usuario un `OE` nuevo en el brief o revisar la priorización.
- **Contrato de la corrida:** cada `secciones/<punto>.md` empieza con su encabezado exacto y solo tiene texto final; estas secciones no llevan figura; si se cita algo, va a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 05-make-problem-objectives` y muestra los avisos. Sin corrida vigente de `04`, detente e indica `04-make-strategic-analysis` (la matriz no se puede armar sin sus códigos). Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `05-make-problem-objectives-update`.
2. **Insumos.** Lee el brief (problema, afectados, evidencia, `OG-01` y `OE-nn` con su indicador) y las corridas de `03` (bloques del Canvas) y `04` (códigos PESTEL, FODA, estrategias y causas).
3. **Propuesta.** Prioriza de dos a cuatro causas del Ishikawa y arma una fila de la matriz por `OE`. Comprueba que cada causa principal quede atendida.
4. **Plan y confirmación.** Muestra el enunciado, las causas principales con su porqué y la matriz completa; recuerda que los objetivos se copian del brief. **Espera la confirmación**; ajusta y vuelve a mostrar si el usuario pide cambios.
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 05-make-problem-objectives)` y escribe en `$RUN/secciones/` los archivos `1.8.md`, `1.9.md` y `1.10.md` con las plantillas; `$RUN/README.md` (corridas de origen de `01`, `03` y `04`, qué propuso el agente y qué confirmó el usuario) y `$RUN/referencias.md` solo si hay citas.
6. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (encabezados, causas iguales al Ishikawa, objetivos iguales al brief, matriz completa y con códigos vigentes, cobertura de causas).
7. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 05-make-problem-objectives --run <carpeta>` (marca 1.8 a 1.10 como disponibles). Si responde `"movido": false`, díselo al usuario.
8. **Cierre.** Entrega la ruta, la problemática y sus causas principales, la matriz en una tabla corta, avisa que el capítulo 1 está completo (`projectcfg.py secciones`) y sugiere `06-make-bi-solution` si existe o `12-make-report` para ver el avance del informe.
