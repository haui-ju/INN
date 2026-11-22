# Design

## Context

Hoy `leer-imagen/<visual>.md` lo escribe `visuales.py` (`leer_imagen` y una función por visual) y, para las pantallas finales, `mockups.py` (`leer_pantalla`, `leer_galeria`). Es texto determinista derivado de los datos, y `rules/html_boards.py::check_leer_imagen` exige que el archivo sea igual al que se deriva hoy. `report.py` copia esos puntos y `report_prosa.py` los une en un párrafo con «Cómo leer la figura.». `19-make-report` no redacta capítulos, así que cualquier frase nueva debe vivir en el kit (catálogo) o en la fuente, no inventarse al ensamblar. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Una explicación de 2 a 3 frases por figura con tres funciones: para qué sirve, qué dice, por qué se resalta lo resaltado.
- Una frase de propósito antes de cada tabla del cuerpo del informe.
- Seguir siendo determinista y verificable: la validación recalcula el texto esperado desde los datos.

**Non-Goals:**
- No se rediseñan las plantillas HTML ni sus datos.
- No se reduce el volumen del informe ni se mueven bloques a anexos (change `compact-report-readability`).
- No se corrigen las inconsistencias de las corridas fuente (se hace con los `-update`).
- No se usa un modelo de lenguaje para redactar las explicaciones.

## Decisions

**1. Tres funciones, fijadas por estructura y no por estilo.** Cada `leer-imagen/<visual>.md` conserva su formato de viñetas pero con las etiquetas «Para qué sirve», «Qué dice», «Por qué se resalta» (esta última solo si el visual resalta algo) y «Pie de foto sugerido». El ensamblado las une en un párrafo en ese orden. *Alternativa descartada:* un párrafo libre por visual; no se puede validar y vuelve a describir lo visible.

**2. «Para qué sirve» sale de un catálogo estático; «Qué dice» y «Por qué se resalta» salen de los datos.** El propósito de un visual es una frase fija (por ejemplo, la matriz: «ayuda a decidir qué ideas entran al MVP»). La conclusión se calcula de los datos con reglas simples por visual (cuántas ideas entran y de qué total; la etapa más baja del recorrido; qué hipótesis no se cumplió; qué columna superó su límite). El motivo del resaltado se declara por visual como una regla sobre los datos y se redacta con ese umbral (cuadrante sombreado = impacto y factibilidad ≥ 4, tomado del dato; etapa roja = emoción negativa; bloque cambiado = difiere del v0; barra roja del Kanban = columna sobre su límite; tarea atrasada = fin planificado anterior al corte). *Alternativa descartada:* escribir la explicación a mano por corrida; rompe el principio de «sin texto escrito a mano» y se desactualiza cuando cambia un dato.

**3. Propósito de tablas en `report_map.json`, por punto y orden.** Una clave nueva `propositos` con entradas como `"4.2#1": "Lista lo que el sistema debe hacer; sirve para verificar cada función con su criterio."`. El armado antepone la frase solo si la tabla de la corrida fuente no trae ya una frase introductoria propia; si no hay ninguna ni entrada, avisa y la validación falla. Así `19` sigue sin redactar contenido: las frases son parte del kit, revisadas con el índice, y no dependen de la corrida. *Alternativa descartada:* poner la frase en cada skill fuente; obligaría a ejecutar los `-update` de 14 skills por una mejora de presentación. Los modelos fuente nuevos sí llevarán la frase para que las corridas futuras ya la traigan.

**4. Validación estructural, no semántica.** Un verificador no puede juzgar si un texto «solo describe». Se valida lo comprobable: que el archivo sea igual al derivado hoy de los datos (como ya se hace), que existan «para qué sirve» y «qué dice», que «por qué se resalta» exista si y solo si los datos resaltan algo, que el total no pase de 3 frases ni 70 palabras sin el pie, y que cada tabla del cuerpo tenga propósito. La calidad del texto la garantizan las funciones que lo generan y sus pruebas con casos reales (matriz, Kanban, Gantt).

**5. Compatibilidad.** Las corridas de `13` y `14b` existentes dejan de pasar `check_leer_imagen` hasta ejecutar `13-design-html-boards-update` / `14b-make-ui-mockups-update`, que solo regeneran `leer-imagen/`. La corrida de `19` ya construida no cambia; se vuelve a armar después.

## Risks / Trade-offs

- [El catálogo de propósitos de tablas puede quedar corto frente a las ~60 tablas del informe] → El primer paso inventaría todas las tablas del índice y la validación lista las que faltan; el catálogo se completa antes de dar el change por terminado.
- [Frases fijas suenan genéricas] → Cada una menciona qué concluir en términos del proyecto (variables del dato) y se revisan en el pase de redacción con `redaccion-academica`.
- [Tope de 70 palabras puede quedarse corto en visuales ricos como el Gantt] → Se mide con las corridas reales; el tope es una constante del kit y se ajusta con evidencia.
- [Las explicaciones nuevas cambian de texto en cada visual y rompen pruebas existentes] → Se actualizan las pruebas del kit junto con cada visual, no al final.
- [El propósito antepuesto duplica una introducción que algunos capítulos ya traen] → Regla de «conservar la frase propia de la fuente» y prueba de no duplicación.

## Open Questions

- Ninguna que cambie las specs o las tareas; los umbrales de palabras y frases se ajustan al medirlos.
