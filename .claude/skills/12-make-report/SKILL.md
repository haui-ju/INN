---
name: 12-make-report
description: Arma el informe de Inteligencia de Negocios de una sola entrega en project/12-report/ (informe.md) con las secciones ya disponibles en el config, en el orden del índice: control del documento con los datos del config y del brief, introducción por capítulo, marcadores de imagen con «Cómo copiarla» y «Cómo leer la figura», figuras y tablas numeradas, referencias combinadas, anexos A a D si su sección de origen existe, faltantes.md con lo pendiente y la skill que lo produce, imágenes para copiar y HTML opcional. No redacta capítulos: junta, ordena y numera. Úsala cuando el usuario pida "12-make-report", "armar el informe", "ver el informe", "qué falta para entregar" o "informe en HTML". No tiene -update: se vuelve a ejecutar cada vez.
---

# 12-make-report

Ensambla el documento de entrega con lo que ya produjeron las skills de contenido (`03` a `11`) y muestra qué falta. Se puede ejecutar en cualquier punto del pipeline: solo entran las secciones que tienen corrida.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/12-report/guia.md` (playbook: reglas, contrato con las skills de contenido, figuras, anexos, faltantes, formatos y errores).
2. `common/12-report/models/README.md`, `rep-0-control-documento.md`, `rep-1-introducciones.md` y `rep-9-referencias.md`.
3. `common/structure/model1.md` (índice: capítulos, títulos, marcas «(incluye imagen)» y anexos) y `project/config.yaml` (`proyecto`, `equipo`, `calendario`, `diseno`, `informe.secciones`).
4. **El brief vigente** (`python3 .claude/skills/_shared/brief.py leer`): de él sale la empresa de la portada.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check --skill 12-make-report`, `secciones`, `register`)
- `python3 .claude/skills/_shared/report.py` (`plan`, `construir`, `render`, `anexos`)
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/report.py`, que se cargan solas por la carpeta `12-report`).

## Reglas

- **No redactes contenido de los capítulos.** El texto sale de `secciones/<punto>.md` de cada corrida vigente; si algo está mal, se corrige con el `-update` de la skill que lo produjo y se vuelve a armar. Nunca edites `informe.md` a mano.
- **Solo lo disponible.** Las secciones pendientes no aparecen y van a `faltantes.md` con la skill que las produce. No preguntes si poner un marcador u omitirlas.
- **Nada se inventa:** el curso y el docente los informa el usuario (si no, quedan «Pendiente»); las introducciones salen del playbook; el informe no copia nada del `README.md` de las corridas.
- **El informe no lleva imágenes.** Cada figura es `(INCLUIR IMAGEN: Figura N: <pie>. Archivo sugerido: imagenes/<visual>.html)` con «Cómo copiarla» y «Cómo leer la figura»; el equipo inserta la imagen a mano. Si falta el HTML o la explicación, el marcador queda y se avisa con el `-update` que lo resuelve.
- **Una sola entrega:** sin historial de versiones ni marcas de avance. Cada ejecución crea una corrida nueva y no toca las anteriores.
- **Formato:** Markdown siempre; HTML opcional con el sistema de diseño (`render`); anexos en HTML con `13-make-annex-html`. Word o PDF los genera el equipo a partir del Markdown.
- Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `python3 .claude/skills/_shared/projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 12-make-report` y muestra los avisos (no bloquean).
2. **Plan.** `python3 .claude/skills/_shared/report.py plan`. Muestra las secciones disponibles con su corrida, las pendientes con la skill que las produce, los anexos y las figuras incompletas. Si faltan secciones, ofrece ejecutar antes sus skills y pregunta si continúa con lo que hay.
3. **Preguntas (AskUserQuestion).** El **curso** y el **docente** para la portada (o «Pendiente») y si quiere también el **HTML** del informe.
4. **Confirmación.** Resume el plan (secciones que entran, faltantes, anexos, datos de portada y formato) y **espera la confirmación**.
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 12-make-report)` y
   `python3 .claude/skills/_shared/report.py construir --salida $RUN [--curso "..."] [--docente "..."]`.
   Escribe `informe.md`, `faltantes.md`, `README.md` (procedencia), `imagenes/` con `INDICE.md` y, si hay anexos, `anexos/anexo-<letra>.md`. Muestra los avisos que imprime (figuras sin HTML o sin explicación, tablas sin título, secciones con «(incluye imagen)» sin figura) con la skill que los corrige.
6. **HTML (opcional).** `python3 .claude/skills/_shared/report.py render $RUN/informe.md` (avisa si usó los tokens base porque `diseno` está vacío). Si hay anexos y el usuario quiere sus HTML, sigue con `13-make-annex-html` después de registrar.
7. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Si una incidencia viene de una skill de contenido, indica su `-update` en vez de editar el informe; si viene del armado, crea otra corrida y vuelve a construir.
8. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 12-make-report --run <carpeta>`. Si responde `"movido": false` (paso fijado), díselo al usuario.
9. **Cierre.** Sugiere pasar el agente `revisor-redactor` sobre `informe.md` antes de entregar (reglas en `common/redaccion/guia.md`; los cambios se hacen en las corridas con los `-update`, nunca solo en `informe.md`). Entrega la ruta, cuántas secciones entraron de las 19, el número de figuras, la lista de faltantes con la skill que los produce, los avisos y qué hacer antes de entregar: insertar las imágenes en los marcadores (abrir cada HTML de `imagenes/`), completar los datos «Pendiente» y pasar el Markdown a Word o PDF con Arial 11 e interlineado 1.5.
