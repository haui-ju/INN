## MODIFIED Requirements

### Requirement: Explicación de la figura
Bajo el marcador de un visual de `13-design-html-boards` o de una pantalla de `14b-make-ui-mockups`, el armado SHALL copiar la explicación de `leer-imagen/<visual>.md` de la corrida vigente, sin su título ni su pie de foto, como un solo párrafo tras la línea «Cómo leer la figura.» en el orden «para qué sirve», «qué dice» y «por qué se resalta»; si falta la corrida o el archivo, SHALL dejar el marcador solo y avisarlo sin incluirlo en `faltantes.md`.

#### Scenario: Explicación presente
- **WHEN** existe `leer-imagen/foda.md` en la corrida vigente de 13
- **THEN** el marcador del FODA va seguido de «Cómo leer la figura.» y de un párrafo con para qué sirve el FODA y qué dice

#### Scenario: Sin corrida de 13
- **WHEN** el config no tiene corrida de `13-design-html-boards`
- **THEN** los marcadores de visuales salen sin explicación y el kit avisa que falta ese paso

### Requirement: Validación del informe
La validación SHALL comprobar la estructura, los puntos presentes y ausentes, el orden, el historial de versiones, los marcadores de imagen, las referencias, los faltantes, el HTML opcional, los enlaces, el texto limpio, que cada tabla del cuerpo del informe tenga una frase de propósito y que cada explicación de figura conserve las funciones «para qué sirve» y «qué dice», e informar cada incidencia con archivo y causa.

#### Scenario: Punto de un avance posterior
- **WHEN** el avance 1 incluye el punto 5.1
- **THEN** la validación informa que pertenece a un avance posterior

#### Scenario: Punto con imagen sin marcador
- **WHEN** el punto 4.7 lleva la marca «(incluye imagen)» y el documento no tiene su marcador
- **THEN** la validación informa el punto

#### Scenario: Tabla sin propósito
- **WHEN** una tabla del capítulo 4 no tiene ninguna frase de propósito antes de ella
- **THEN** la validación informa el punto y la tabla

#### Scenario: Explicación de figura solo descriptiva
- **WHEN** la explicación bajo un marcador solo enumera contenido y no dice para qué sirve la figura
- **THEN** la validación informa la figura

## ADDED Requirements

### Requirement: Propósito de cada tabla
`report_map.json` SHALL declarar una frase de propósito (para qué sirve la tabla y qué concluir) por cada tabla del cuerpo del informe, identificada por su punto del índice y su orden dentro del punto, y el armado SHALL anteponerla a la tabla en prosa. El armado NO SHALL redactar propósitos nuevos.

#### Scenario: Tabla con propósito en el catálogo
- **WHEN** el punto 4.2 tiene su tabla de requerimientos funcionales y el catálogo declara su propósito
- **THEN** el informe antepone esa frase a la tabla

#### Scenario: Tabla con frase propia en la fuente
- **WHEN** la corrida fuente ya abre la tabla con una frase que dice qué muestra y qué concluir
- **THEN** el armado conserva esa frase y no agrega la del catálogo

#### Scenario: Sin inventar
- **WHEN** una tabla no tiene entrada en el catálogo
- **THEN** el armado avisa la tabla y no escribe un propósito propio

#### Scenario: Tabla sin ninguna frase
- **WHEN** una tabla del cuerpo no tiene frase propia ni entrada en el catálogo
- **THEN** el armado avisa la tabla y la validación falla, sin escribir un propósito inventado
