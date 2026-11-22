# Design

## Context

Estado observado: `report.py` convierte en `_convertir_informe` las líneas `**Pegar.**` de los informes de sprint (6.N.2, 6.N.3, 6.N.4, 6.N.5, 6.N.7) en `![Figura j: pie](evidencias/archivo)`, registra `reun.evid`, copia esos archivos de la bitácora a `evidencias/` y avisa de los que faltan; `renumerar` cuenta `![Figura n:` y reemplaza «Figura n»; `rules/report.py::check_figuras` exige numeración consecutiva, código o fecha en el pie y que la imagen exista; `md_a_html` convierte `![…](…)` en `<figure><img>`. El índice ya marca los puntos con imagen (`imagen` en `cargar_indice`) y `13-design-html-boards` deja `leer-imagen/<visual>.md` (título, puntos con etiqueta y «Pie de foto sugerido»). `report_map.json` ya tiene a 13 como fuente.

## Goals / Non-Goals

**Goals:** que el informe no lleve imágenes ni las copie; que cada punto con imagen tenga su marcador numerado, con pie, archivo sugerido y la explicación de la figura; que faltantes no mezcle imágenes.

**Non-Goals:** generar o insertar imágenes, cambiar los informes de sprint, cambiar el índice, tocar Miro o Figma, ejecutar skills.

## Decisions

### D1. Formato del marcador
Una línea propia, entre paréntesis, que `renumerar` y la validación reconocen: `(INCLUIR IMAGEN: Figura 3: Gantt al 22-12-2026. Archivo sugerido: gantt-2026-12-22.png.)`. Tras ella, si hay explicación, una línea `**Cómo leer la figura:**` y los puntos de `leer-imagen`. Una sola expresión regular define el marcador.

### D2. De dónde sale cada marcador
1. **Líneas «Pegar» de los informes de sprint** (6.N.2 Gantt, 6.N.3 incremento, 6.N.4 Kanban, 6.N.5 Review, 6.N.7 pruebas): cada archivo listado pasa a ser un marcador con el pie que hoy se arma (`Gantt al DD-MM-AAAA`, `HU-XX … (REQ-XX)`, etc.) y el nombre del archivo como sugerido. «Sin captura.» sigue como nota y no genera marcador.
2. **Puntos con marca de imagen y visual de 13** (1.2, 1.3.2, 3.1.2.2, 3.1.3.2, 3.1.4.2, 3.2.3, 3.2.4, 3.4, 4.1.1, 4.6.2, 4.7, 4.8, 6.4.1 a 6.4.3): `report_map.json` declara el visual de cada punto (`imagen_visual`); el marcador usa el título del visual y la fecha de la corrida de 13 como trazabilidad («datos al DD-MM-AAAA»), o su fecha de corte para Gantt, Kanban y panel, y `<visual>.png` como archivo.
3. **Puntos con imagen aportada por el usuario sin línea «Pegar»** (3.1.5.3, 5.3, D.3): un marcador con el título del punto y su código en el pie, y un archivo sugerido derivado del código (`pantallas-3-1-5-3.png`).
Un punto con imagen que ya tenga marcador (por 1) no recibe otro.

### D3. Explicación de la figura
Para los marcadores de visuales, el kit lee `leer-imagen/<visual>.md` de la corrida vigente de 13 y copia sus puntos sin el título ni el «Pie de foto sugerido». Si falta la corrida o el archivo, el marcador queda sin explicación y se agrega un aviso a lo que imprime `construir`; no entra en `faltantes.md` ni bloquea.

### D4. Salida sin imágenes
`construir` deja de crear `evidencias/` y de copiar archivos; `reun.evid` y el aviso «la evidencia … no está» desaparecen. El `README.md` de la corrida no cambia (solo procedencia): el documento solo trae el marcador y su explicación, nada más.

### D5. Numeración y pies
`renumerar` cuenta los marcadores en lugar de `![Figura n:` y actualiza las menciones «Figura n» del bloque, igual que hoy. Todo pie conserva la regla de llevar un código de trazabilidad o una fecha `DD-MM-AAAA`.

### D6. HTML opcional
`md_a_html` muestra el marcador como un recuadro punteado con el texto de la línea (sin `<img>`) y las explicaciones como lista; el recurso externo sigue prohibido.

### D7. Validación
`check_figuras` pasa a comprobar: numeración consecutiva de los marcadores, código o fecha en el pie, ausencia de `![…](…)` y de `evidencias/`, que cada punto con marca de imagen y de avance vigente tenga marcador, y que los marcadores de visuales lleven la explicación cuando exista la corrida de 13. `faltantes.md` se comprueba como hoy (solo puntos sin fuente).

### D8. Pruebas
Fixtures con informes de sprint y una corrida de 13 (con `leer-imagen/`); pruebas de: marcadores de los tres orígenes, numeración, pie, explicación presente y ausente, `evidencias/` inexistente, HTML sin `<img>`, validación de punto con imagen sin marcador y de `![…](…)`.

## Risks / Trade-offs

- [Un marcador sin explicación cuando 13 no se ejecutó] → aviso claro y orden de ejecución sugerido; no bloquea.
- [El visual de un punto cambió de fuente tras armar el informe] → el informe se vuelve a armar (la skill no tiene `-update`); la explicación sale siempre de la corrida vigente de 13.
- [Archivo sugerido distinto del que el usuario descargue] → es solo una sugerencia; el nombre real lo decide el usuario.

## Migration Plan

Se reemplaza el armado de figuras y se actualizan fixtures y pruebas; no hay corridas de `project/report/` previas que migrar.

## Open Questions

- Si más adelante conviene un modo que inserte las imágenes a partir de una carpeta que el usuario indique.
