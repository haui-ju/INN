## MODIFIED Requirements

### Requirement: Documento acumulado y estructura de salida
La skill SHALL crear cada corrida en `project/report/<DD-MM-AAAA-HH-MM-SS>/` con `informe-avance-N.md`, `anexos/`, `faltantes.md` y `README.md` (sin carpeta de evidencias ni archivos de imagen), SHALL incluir todos los puntos del índice cuya primera marca sea igual o anterior al avance y ninguno posterior, y SHALL registrar la corrida en el paso `19-make-report` del config.

#### Scenario: Avance 1
- **WHEN** se arma el avance 1
- **THEN** el documento incluye los puntos marcados `[A1]` y `[A1+]` y no incluye 5.1, 6.2 ni el capítulo 7

#### Scenario: Avance 2
- **WHEN** se arma el avance 2
- **THEN** el documento incluye también los puntos `[A2]` y los `[A1+]` con su texto vigente

#### Scenario: Sin imágenes en la salida
- **WHEN** se arma cualquier avance
- **THEN** la corrida no contiene `evidencias/` ni archivos de imagen y el documento no incrusta ninguna imagen

### Requirement: Figuras y evidencias
El armado SHALL reemplazar las líneas de captura de los informes de sprint por marcadores de imagen que conservan su pie y su archivo, numerar los marcadores de forma consecutiva en todo el documento, y todo pie SHALL llevar un código de trazabilidad o una fecha `DD-MM-AAAA`; SHALL NOT incrustar imágenes ni copiar evidencias.

#### Scenario: Pie sin código ni fecha
- **WHEN** un marcador tiene un pie sin código de trazabilidad ni fecha
- **THEN** la validación informa la figura

#### Scenario: Numeración con saltos
- **WHEN** el documento tiene los marcadores de las figuras 1, 2 y 4
- **THEN** la validación informa el salto

#### Scenario: Imagen incrustada
- **WHEN** el documento contiene `![Figura 1: …](ruta)`
- **THEN** la validación informa que las imágenes no se incrustan y deben ser marcadores

### Requirement: Faltantes
`faltantes.md` SHALL listar, con el punto, el título, el paso que lo produce y qué hacer, todo punto con marca igual o anterior al avance que no tenga fuente, y SHALL coincidir con lo que el documento deja con marcador de pendiente u omite, sin listar un punto que tiene contenido ni las imágenes, sus archivos o sus explicaciones.

#### Scenario: Punto omitido sin registrar
- **WHEN** el punto 5.1 no está en el documento ni en `faltantes.md`
- **THEN** la validación informa el punto

#### Scenario: Punto con contenido en faltantes
- **WHEN** `faltantes.md` lista 4.2 y el documento lo tiene con contenido
- **THEN** la validación informa el punto

#### Scenario: Imagen sin archivo
- **WHEN** un marcador sugiere un archivo que no existe
- **THEN** `faltantes.md` no lo lista y no hay aviso de evidencia ausente

### Requirement: Formatos de salida
El Markdown SHALL ser la fuente del documento; el kit SHALL poder generar un HTML autónomo con el sistema de diseño (con aviso si usa los tokens base) cuyos encabezados coincidan con los del Markdown y que muestre cada marcador de imagen como un recuadro visible, sin etiquetas de imagen; las demás conversiones y una vista privada quedan a elección del usuario, esta última solo con confirmación explícita.

#### Scenario: HTML con recurso externo
- **WHEN** el HTML carga una hoja de estilo o fuente externa
- **THEN** la validación informa el recurso

#### Scenario: Marcador en el HTML
- **WHEN** se genera el HTML de un documento con marcadores de imagen
- **THEN** cada marcador aparece como un recuadro «Incluir imagen» y no hay etiquetas `<img>`

### Requirement: Validación del informe
La validación SHALL comprobar la estructura, los puntos presentes y ausentes, el orden, el historial de versiones, los marcadores de imagen, las referencias, los faltantes, el HTML opcional, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Punto de un avance posterior
- **WHEN** el avance 1 incluye el punto 5.1
- **THEN** la validación informa que pertenece a un avance posterior

#### Scenario: Punto con imagen sin marcador
- **WHEN** el punto 4.7 lleva la marca «(incluye imagen)» y el documento no tiene su marcador
- **THEN** la validación informa el punto

## ADDED Requirements

### Requirement: Marcador de imagen
Cada punto incluido con la marca «(incluye imagen)» del índice SHALL llevar un marcador en una línea propia, `(INCLUIR IMAGEN: Figura X: <pie>. Archivo sugerido: <archivo>.)`, tomado de la línea «Pegar» del informe de sprint, del visual que `report_map.json` declara para el punto o, si ninguno aplica, del título y el código del punto.

#### Scenario: Gantt del avance
- **WHEN** el informe del sprint 1 pega la captura del Gantt con corte al 22-12-2026
- **THEN** el punto 6.1.2 lleva `(INCLUIR IMAGEN: Figura 7: Gantt al 22-12-2026. Archivo sugerido: gantt-2026-12-22.png.)`

#### Scenario: Visual del diagnóstico
- **WHEN** el punto 1.2 no tiene línea «Pegar» y hay corrida de 13 con el visual `foda`
- **THEN** el punto lleva el marcador del FODA con su fecha y `foda.png` como archivo sugerido

#### Scenario: Sin captura
- **WHEN** el informe de sprint dice «Sin captura.»
- **THEN** el punto conserva esa nota y no genera marcador

### Requirement: Explicación de la figura
Bajo el marcador de un visual de `13-design-html-boards`, el armado SHALL copiar los puntos de `leer-imagen/<visual>.md` de la corrida vigente, sin su título ni su pie de foto, tras la línea «Cómo leer la figura:»; si falta la corrida o el archivo, SHALL dejar el marcador solo y avisarlo sin incluirlo en `faltantes.md`.

#### Scenario: Explicación presente
- **WHEN** existe `leer-imagen/foda.md` en la corrida vigente de 13
- **THEN** el marcador del FODA va seguido de «Cómo leer la figura:» y sus puntos

#### Scenario: Sin corrida de 13
- **WHEN** el config no tiene corrida de `13-design-html-boards`
- **THEN** los marcadores de visuales salen sin explicación y el kit avisa que falta ese paso
