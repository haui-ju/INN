# Proposal

## Why

`19-make-report` hoy convierte las líneas «Pegar» de los informes de sprint en imágenes (`![Figura X: …](evidencias/…)`) y copia las evidencias a `evidencias/`. Pero las imágenes del informe las inserta el usuario a mano (capturas de los HTML de `13-design-html-boards`, fotos, pantallas), y ahora cada imagen tiene su explicación en `leer-imagen/<visual>.md`. El informe debe dejar **marcadores** donde va cada imagen, con su número de figura, su pie y el archivo sugerido, junto a la explicación de lo que la imagen transmite, y no tocar archivos de imagen.

## What Changes

- **Marcadores en lugar de imágenes.** Cada punto con la marca «(incluye imagen)» del índice lleva, en el documento, un marcador entre paréntesis: `(INCLUIR IMAGEN: Figura X: <pie>. Archivo sugerido: <archivo>.)`. Ninguna imagen se incrusta y no se copia ninguna evidencia: `evidencias/` deja de existir en la salida.
- **Figuras numeradas y con trazabilidad.** Los marcadores se renumeran de forma consecutiva en todo el documento; el pie de cada uno lleva un código de trazabilidad o una fecha `DD-MM-AAAA` (las líneas «Pegar» de los informes de sprint conservan su pie y su archivo, que pasan al marcador).
- **Explicación junto a la figura.** Debajo de cada marcador de un visual de `13-design-html-boards`, el armado copia los puntos de `leer-imagen/<visual>.md` (sin el título ni el pie de foto, que ya están en el marcador) bajo «Cómo leer la figura:». Si no hay corrida de 13, el marcador va solo y el kit avisa (aviso, no bloqueo).
- **Faltantes sin imágenes.** `faltantes.md` sigue listando solo puntos sin fuente; ni las imágenes ni sus archivos ni sus explicaciones son faltantes, y el kit deja de avisar de evidencias ausentes.
- **HTML opcional:** el marcador se muestra como un recuadro visible «Incluir imagen», no como `<img>`.
- **Validación:** cada punto con la marca de imagen y marca de avance vigente debe tener su marcador; los marcadores no pueden apuntar a rutas de imagen incrustadas ni haber `![…](…)`; numeración, pie y explicación se comprueban.

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- `report-assembly`: documento acumulado y estructura de salida, figuras (ahora marcadores), explicación de cada figura, faltantes, formato HTML y validación.

## Impact

- **Archivos modificados:** `.claude/skills/_shared/report.py` (`_convertir_informe`, `renumerar`, `armar`, `construir`, HTML), `rules/report.py` (`check_figuras`, validación), `report_map.json` (puntos con visual), `.claude/skills/19-make-report/SKILL.md`, `common/report/guia.md` y `models/README.md`, pruebas de reporte y fixtures.
- **Sin cambio:** las skills de origen, `16-make-sprint-report` (sigue pidiendo los archivos y pies de las capturas, que ahora el informe solo referencia), `13-design-html-boards` y los visuales, el índice y sus marcas.
- **Fuera de alcance:** insertar imágenes en el informe (lo hace el usuario a mano); Miro y Figma; ejecutar las skills.
- **Supuestos registrados:** el archivo sugerido de un visual es `<visual>.png` (Gantt, Kanban y panel con su fecha de corte: `gantt-AAAA-MM-DD.png`); los puntos con imagen aportada por el usuario (3.1.5.3, 5.3, D.3) llevan un marcador con el título del punto y un archivo sugerido derivado de su código; una corrida de 13 solo es necesaria para las explicaciones.
