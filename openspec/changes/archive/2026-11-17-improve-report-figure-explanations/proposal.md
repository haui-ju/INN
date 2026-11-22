# Proposal

## Why

Los textos «Cómo leer la figura» del informe repiten lo que el lector ya ve ("23 ideas ubicadas según impacto y factibilidad; 7 se incluyen, 11 se posponen") y no dicen para qué sirve la figura, qué conclusión permite ni por qué algo aparece resaltado. Además, muchas tablas del informe aparecen sin una frase que diga qué muestran y qué hay que concluir, así que el lector las ve "flotando". Hoy ambos problemas nacen en las skills fuente (el generador de `leer-imagen` de `13-design-html-boards` y de `14b-make-ui-mockups`) y en el ensamblado de `19-make-report`, que copia sin añadir sentido.

## What Changes

- Cada `leer-imagen/<visual>.md` pasa de tres viñetas descriptivas (Qué muestra / Cómo leerla / Qué transmite) a una explicación breve de 2 a 3 frases con tres funciones: **para qué sirve** la figura, **qué dice** (la conclusión que se desprende de sus datos) y **por qué se resalta** lo resaltado (cuadrante sombreado, tarjeta destacada, etapa en rojo, bloque cambiado, columna sobre el límite). Sigue derivándose solo de los datos de la imagen, sin texto manual por corrida.
- Se añade al kit un catálogo estático de **propósitos** (una frase por visual, por tipo de tabla y por punto del índice) que vive en `report_map.json` y en los modelos fuente, no en el ensamblado.
- `19-make-report` antepone a cada tabla del informe una frase de propósito (para qué sirve y qué concluir) tomada de ese catálogo; no redacta contenido de capítulo: si una tabla no tiene propósito en el catálogo, el informe lo avisa.
- «Cómo leer la figura» sigue siendo un párrafo, ahora más corto y en este orden: para qué sirve, qué dice, por qué se resalta lo resaltado.
- Las validaciones fallan cuando una explicación solo enumera contenido (sin función «para qué sirve», sin conclusión o sin motivo del resaltado cuando hay resaltado) y cuando una tabla del informe queda sin propósito. Cubre también las pantallas finales (`14b`) y el Gantt y el Kanban (`13`).
- Se ajustan los textos de ejemplo de `common/report/guia.md`, `common/html/` y los modelos para reflejar el nuevo formato. Todo el código nuevo va en inglés; los textos que ve el usuario y los README, en español.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `html-visuals`: la explicación de cada imagen cambia de «qué muestra / cómo leerla / qué transmite» a «para qué sirve / qué dice / por qué se resalta», con una validación que rechaza explicaciones solo descriptivas.
- `report-assembly`: el armado antepone un propósito a cada tabla desde el catálogo, copia la nueva explicación de la figura y la validación falla si falta el propósito de una tabla o la explicación es solo descriptiva.
- `ui-mockups`: la explicación de las pantallas finales y de la galería (`leer-imagen/UI-nn.md`, `galeria.md`) adopta el mismo formato.

## Impact

- Código: `.claude/skills/_shared/visuales.py` (`leer_imagen` y sus funciones por visual), `mockups.py` (`leer_pantalla`, `leer_galeria`), `report.py` y `report_prosa.py` (copia de la explicación y antepuesta del propósito), `report_map.json` (campo `proposito`), `rules/html_boards.py`, `rules/report.py` y `rules/ui_mockups.py` (nuevas comprobaciones) y sus pruebas en `_shared/tests/`.
- Documentación: `common/report/guia.md`, `common/report/models/`, `common/html/DESIGN.md` y las skills `13-design-html-boards`, `14b-make-ui-mockups` y `19-make-report`.
- Las corridas existentes de `13` y `14b` dejarán de pasar la validación hasta ejecutar su `-update` (regeneran `leer-imagen/`); no se modifica ninguna corrida anterior.
- Sin dependencias nuevas.
