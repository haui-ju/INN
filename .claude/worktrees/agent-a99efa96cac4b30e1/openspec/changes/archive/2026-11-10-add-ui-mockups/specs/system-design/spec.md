## MODIFIED Requirements

### Requirement: Diseño de interfaz
`interfaz.md` SHALL indicar, bajo el encabezado `### 5.3.1. Destino de las pantallas del prototipo`, el destino de cada `PAN` (se conserva, se modifica o se descarta, con motivo) y, bajo `### 5.3.2. Pantallas finales`, las pantallas `UI-nn` con su `PAN` de origen o «—» si son nuevas, las historias que cubren y los cambios respecto al prototipo.

#### Scenario: PAN sin destino
- **WHEN** `PAN-04` del Design Thinking no figura en la tabla de destinos
- **THEN** la validación informa el código

#### Scenario: Pantalla nueva
- **WHEN** una pantalla final no proviene de ningún `PAN`
- **THEN** su origen es «—» y debe indicar la historia que la justifica

#### Scenario: Encabezado sin numerar
- **WHEN** `interfaz.md` tiene «### Pantallas finales» sin «5.3.2.»
- **THEN** la validación informa el encabezado esperado
