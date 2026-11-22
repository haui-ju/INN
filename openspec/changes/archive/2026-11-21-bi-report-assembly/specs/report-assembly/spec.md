# report-assembly Specification

## Purpose
Define el armado del informe de Inteligencia de Negocios de una sola entrega (`12-make-report`): qué secciones entran, de dónde sale cada parte, cómo se tratan las figuras, las tablas, las referencias y los anexos, qué se lista como faltante y qué comprueba la validación de la corrida.

## ADDED Requirements

### Requirement: Contrato de las corridas de contenido
Cada skill que aporta secciones SHALL dejar en su corrida `secciones/<punto>.md` por sección (encabezado `## <punto>. <título>`; los capítulos 4 y 5 usan `secciones/4.md` y `secciones/5.md`), las figuras como `<!-- figura: <visual> -->` con `visuales/<visual>.html` y `leer-imagen/<visual>.md`, y opcionalmente `referencias.md` y `anexos/<letra>.md`. El informe SHALL NOT copiar nada del `README.md` de esas corridas.

#### Scenario: Sección leída de su corrida
- **WHEN** la sección 1.6 está disponible con la corrida vigente de `04-make-strategic-analysis`
- **THEN** el informe toma el texto de `secciones/1.6.md` de esa corrida y nada de su `README.md`

#### Scenario: Sección disponible sin archivo
- **WHEN** la sección 1.5 figura disponible pero su corrida no tiene `secciones/1.5.md`
- **THEN** el informe no la incluye y `faltantes.md` la lista con la skill que la produce y la causa

### Requirement: Solo secciones disponibles en el orden del índice
El informe SHALL incluir solo las secciones con estado `disponible` según el registro del config, en el orden del índice, con el número y el título del índice en su encabezado. Las secciones pendientes SHALL NOT aparecer en el informe y SHALL listarse en `faltantes.md` con la skill que las produce, sin preguntar al usuario si poner un marcador u omitirlas.

#### Scenario: Informe parcial
- **WHEN** solo se registraron las corridas de 03, 04 y 05
- **THEN** el informe contiene 1.1 a 1.10 en orden y `faltantes.md` lista 2.1 a 5 con su skill

#### Scenario: Título del índice
- **WHEN** el encabezado de `secciones/1.4.md` usa otro texto después del número
- **THEN** el informe muestra `## 1.4.` con el título del índice

#### Scenario: Ninguna sección disponible
- **WHEN** no hay ninguna sección disponible
- **THEN** el informe trae la portada y las referencias, ningún capítulo, y `faltantes.md` lista las 19 secciones

### Requirement: Portada y control del documento
El informe SHALL abrir con un control del documento armado desde el config (nombre, tema, equipo con su rol, fecha de entrega) y el brief vigente (empresa), más el curso y el docente que informe el usuario. Lo que falte SHALL decir «Pendiente» y figurar en `faltantes.md`. SHALL NOT llevar historial de versiones ni marcas de avance.

#### Scenario: Datos completos
- **WHEN** el config tiene la entrega 30-11-2026 y el brief nombra la empresa
- **THEN** el control del documento muestra esa fecha, la empresa y los integrantes del config

#### Scenario: Sin curso ni docente
- **WHEN** el usuario no informa el curso ni el docente
- **THEN** ambos campos dicen «Pendiente» y `faltantes.md` los lista como datos de portada

### Requirement: Introducción por capítulo
Cada capítulo con al menos una sección disponible SHALL abrir con una introducción breve tomada del playbook que nombra solo sus secciones incluidas; un capítulo sin secciones disponibles SHALL NOT aparecer.

#### Scenario: Capítulo con parte de sus secciones
- **WHEN** del capítulo 1 solo están disponibles 1.1 a 1.4
- **THEN** su introducción nombra 1.1 a 1.4 y no nombra 1.5 a 1.10

#### Scenario: Capítulo sin secciones
- **WHEN** ninguna sección del capítulo 3 está disponible
- **THEN** el informe no tiene el encabezado del capítulo 3

### Requirement: Marcadores de figura
Cada línea `<!-- figura: <visual> -->` SHALL reemplazarse por `(INCLUIR IMAGEN: Figura N: <pie>. Archivo sugerido: imagenes/<visual>.html)`, una línea «Cómo copiarla» y un párrafo «Cómo leer la figura» redactado desde `leer-imagen/<visual>.md`. Si falta el HTML o la explicación, SHALL quedar el marcador y SHALL avisarse. El informe SHALL NOT incrustar imágenes.

#### Scenario: Figura completa
- **WHEN** la sección 1.6 marca la figura `foda` y su corrida tiene el HTML y la explicación
- **THEN** el informe trae el marcador con el pie sugerido, «Cómo copiarla» hacia `imagenes/foda.html` y «Cómo leer la figura» con lo que dice la explicación

#### Scenario: Figura sin explicación
- **WHEN** la corrida tiene `visuales/pestel.html` pero no `leer-imagen/pestel.md`
- **THEN** el marcador queda sin «Cómo leer la figura» y el armado avisa la figura y la skill que la produce

### Requirement: Numeración de figuras y tablas
Las figuras y los títulos de tabla («Tabla N») SHALL numerarse de forma consecutiva en todo el informe, y las menciones «Figura k» y «Tabla k» de cada sección SHALL actualizarse al número final.

#### Scenario: Dos secciones con figura
- **WHEN** 1.4 y 1.5 traen una figura cada una
- **THEN** la de 1.4 es la Figura 1, la de 1.5 la Figura 2, y la mención «Figura 1» dentro de 1.5 pasa a «Figura 2»

### Requirement: Imágenes para copiar
El armado SHALL copiar a `imagenes/` de la corrida cada HTML de figura usado y SHALL escribir `imagenes/INDICE.md` con cada HTML, su figura y la sección donde va.

#### Scenario: Índice de imágenes
- **WHEN** el informe tiene las figuras `foda` y `pestel`
- **THEN** `imagenes/` contiene ambos HTML y `INDICE.md` los lista con su número de figura y su sección

### Requirement: Referencias combinadas
La sección Referencias bibliográficas SHALL reunir las entradas de `referencias.md` de las corridas usadas, sin duplicados y en orden alfabético, según APA 7.

#### Scenario: Entrada repetida
- **WHEN** las corridas de 03 y 04 traen la misma referencia
- **THEN** el informe la lista una sola vez

### Requirement: Anexos según su sección de origen
Cada anexo A a D SHALL incluirse solo si su sección de origen (A y B: 3.1; C y D: 3.2) está disponible y su corrida trae `anexos/<letra>.md`; si no, SHALL omitirse y listarse en `faltantes.md` con la skill que lo produce. Cada anexo incluido SHALL quedar también en `anexos/anexo-<letra>.md` de la corrida.

#### Scenario: Anexo sin origen
- **WHEN** la sección 3.1 está pendiente
- **THEN** el informe no trae los anexos A ni B y `faltantes.md` los lista con `08-make-etl`

### Requirement: Faltantes y procedencia
La corrida SHALL incluir `faltantes.md` (secciones, anexos y datos de portada pendientes, y figuras incompletas) y un `README.md` con la procedencia: modo de datos, corridas usadas por skill y opciones del armado. Ningún otro archivo SHALL anotar la procedencia.

#### Scenario: Faltantes coherentes
- **WHEN** se arma el informe
- **THEN** cada sección del índice aparece en el informe o en `faltantes.md`, nunca en ambos

### Requirement: Formatos de salida
El Markdown SHALL generarse siempre. El HTML SHALL ser opcional, autónomo, sin recursos externos, con los tokens del sistema de diseño del config (o los base con aviso) y con los mismos encabezados que el Markdown.

#### Scenario: HTML pedido
- **WHEN** el usuario pide el HTML
- **THEN** `informe.html` no carga recursos externos y sus encabezados coinciden con los de `informe.md`

### Requirement: Validación de la corrida del informe
La validación de una corrida de `project/12-report/` SHALL comprobar: control del documento sin versiones, capítulos y secciones del índice en orden y sin repetir, coherencia entre el informe y `faltantes.md`, marcadores de figura consecutivos con «Cómo copiarla» y su HTML, tablas consecutivas, sin imágenes incrustadas, marcas de figura sin reemplazar, referencias sin duplicados, anexos con su archivo y HTML coherente.

#### Scenario: Marca de figura sin reemplazar
- **WHEN** el informe conserva una línea `<!-- figura: foda -->`
- **THEN** la validación informa la incidencia

#### Scenario: Sección con imagen sin marcador
- **WHEN** la sección 1.6 está en el informe y no tiene ningún marcador de imagen
- **THEN** la validación informa que el punto lleva la marca «(incluye imagen)» y no tiene su marcador
