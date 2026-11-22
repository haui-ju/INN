---
name: 03-make-business-diagnosis
description: Redacta las secciones 1.1 a 1.4 del informe de Inteligencia de Negocios en project/03-business-diagnosis/ (secciones/1.1.md a 1.4.md): nombre y datos de la empresa, misión y visión, industria y tamaño (ventas anuales en UIT y categoría según la Ley 30056) y el Business Model Canvas de nueve bloques con su figura HTML, a partir de project/domain.md y del brief. Confirma el tipo de proyecto, pregunta solo lo que falta, muestra un plan y espera la confirmación antes de escribir. Úsala después de 01-make-project-brief o cuando el usuario pida "03-make-business-diagnosis", "diagnóstico del negocio", "misión y visión", "industria y tamaño", "tamaño de la empresa" o "Business Model Canvas". Para cambiar uno ya creado usa 03-make-business-diagnosis-update.
---

# 03-make-business-diagnosis

Abre el capítulo 1 (diagnóstico estratégico): presenta la empresa, su misión y visión, su industria y su tamaño, y su modelo de negocio en un Business Model Canvas. La rúbrica pide misión, visión, industria y tamaño, y un Canvas articulado con la problemática; `04-make-strategic-analysis` y `05-make-problem-objectives` leen esta corrida.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/03-business-diagnosis/guia.md` (playbook: fuentes, tipo de proyecto, datos modelados, contrato de la corrida, tamaño por UIT, Canvas, errores y checklist).
2. `common/03-business-diagnosis/models/README.md` y las plantillas `bd-1-empresa.md`, `bd-2-mision-vision.md`, `bd-3-industria-tamano.md` y `bd-4-canvas.md` (formato exacto de cada sección).
3. `project/config.yaml`, `project/domain.md` y el brief vigente (`python3 .claude/skills/_shared/brief.py leer`).

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/diagnostico.py titulos` (encabezado exacto de cada sección) y `leer --paso 03-make-business-diagnosis --run <corrida>`
- `python3 .claude/skills/_shared/visuales.py construir --visual bmc --run <corrida> --carpeta <corrida>/visuales [--diseno <tokens.json>] [--interpretacion "<texto>"]`
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/business_diagnosis.py`).

## Reglas

- **No des por hecho que existe una empresa.** Muestra `proyecto.tipo` y confírmalo. Con `propio`, el RUC dice «No aplica (empresa planteada por el equipo)»; con `empresa`, es el del config. Si el usuario corrige el tipo, indica `00-init-update` y no continúes.
- **Los datos salen de `domain.md` y del brief**, no de memoria. Misión y visión se copian tal cual; si no constan, se proponen, se confirman y se escriben primero en `domain.md`.
- **Datos modelados:** muestra qué secciones de `domain.md` llevan «(modelado por el agente, …)» y pregunta si hay dato real. El informe va sin el marcador; la procedencia, solo en el `README.md`.
- **Tamaño:** ventas anuales ÷ UIT del año (confírmala con una búsqueda del decreto supremo) y categoría de la Ley 30056 (guía, sección 3). Nunca por número de trabajadores.
- **Canvas:** los nueve bloques con sus nombres exactos y una lectura que nombra los bloques donde está la problemática del brief.
- **Contrato de la corrida:** cada `secciones/<punto>.md` empieza con `## <punto>. <título del índice>` y solo tiene texto final; la figura del Canvas es la línea `<!-- figura: bmc -->`; el visual se genera con `visuales.py`, nunca a mano; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 03-make-business-diagnosis` y muestra los avisos (no bloquean; sin brief o sin `domain.md`, sugiere `01-make-project-brief`). Si ya hay una corrida (`projectcfg.py current --step 03-make-business-diagnosis`), avisa que se creará otra versión y ofrece `03-make-business-diagnosis-update`.
2. **Tipo de proyecto.** Muestra `empresa` o `propio` (y el RUC) y confírmalo.
3. **Insumos.** Lee `domain.md` y el brief. Muestra lo que ya sabes (nombre, actividad, misión, visión, clientes, competencia) y lista las secciones con datos modelados; pregunta, una por una, si el usuario aporta el dato real.
4. **Preguntas** (AskUserQuestion), solo lo que falte: ventas anuales y año, trabajadores, tipo de cliente, competidores, elementos del Canvas que no salgan de `domain.md` ni del brief. Busca la UIT del año y muéstrala con su fuente.
5. **Plan y confirmación.** Muestra: tipo, fuente de cada sección, misión y visión que se copiarán, el cálculo del tamaño (ventas ÷ UIT = n UIT → categoría) y los nueve bloques en una línea cada uno con la lectura del modelo. **Espera la confirmación.**
6. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 03-make-business-diagnosis)` y escribe en `$RUN/secciones/` los archivos `1.1.md`, `1.2.md`, `1.3.md` y `1.4.md` con las plantillas; `$RUN/referencias.md` (una referencia por línea) y `$RUN/README.md` (modo de datos, tipo, secciones salidas de datos modelados, qué confirmó o corrigió el usuario).
7. **Figura.** Antes redacta el «Qué debes entender» de la figura: 3 a 6 frases y hasta 130 palabras, con los datos del caso, que digan qué conclusión debe sacar el lector y por qué importa para la problemática; no describas cómo se ve ni repitas conteos. Pásalo con `--interpretacion "<texto>"`; el validador lo exige y el informe lo usa en «Cómo leer la figura». `python3 .claude/skills/_shared/visuales.py construir --visual bmc --run <corrida> --carpeta $RUN/visuales` (con `--diseno project/02-design-system/<corrida>/tokens.json` si hay sistema de diseño vigente). Deja `visuales/bmc.html` y `leer-imagen/bmc.md`.
8. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole las rutas de `$RUN/secciones/*.md` y los datos propios del caso; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; no debe quedar ningún aviso bloqueante y, si falta un dato, pregúntaselo al usuario). Después, `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (encabezados, figura, RUC, misión y visión, tamaño, nueve bloques, marcador, citas). Si corriges el Canvas, vuelve a construir la figura.
9. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 03-make-business-diagnosis --run <carpeta>` (marca 1.1 a 1.4 como disponibles). Si responde `"movido": false` (paso fijado), díselo al usuario.
10. **Cierre.** Entrega la ruta, un resumen por sección, la categoría de tamaño con su cálculo, las secciones salidas de datos modelados, cómo abrir `visuales/bmc.html` para copiar la imagen, y sugiere `04-make-strategic-analysis`.
