## MODIFIED Requirements

### Requirement: Cinco porqués
Cada problema SHALL tener una cadena de cinco porqués que termina en una causa accionable, y SHALL citar el `PRB` del que parte; una cadena puede cerrarse antes solo si registra «Cierre anticipado» con el motivo de por qué la causa ya es accionable, y el título o la introducción que nombran el método SHALL decir «cinco porqués» únicamente si todas las cadenas tienen cinco niveles. El problema principal SHALL resumirse en una frase que el Design Thinking pueda citar en `ENF-01`.

#### Scenario: Cadena sin causa accionable
- **WHEN** la última causa de una cadena no puede atacarse con la solución
- **THEN** la skill pide al usuario precisarla antes de confirmar

#### Scenario: Cadena corta sin cierre anticipado
- **WHEN** una cadena tiene tres niveles y no registra «Cierre anticipado»
- **THEN** la validación informa el `POR` y que debe completarse o justificarse

#### Scenario: Título que promete más niveles
- **WHEN** el título dice «cinco porqués» y una cadena cierra en tres niveles con su motivo
- **THEN** la validación informa que el nombre del método debe ajustarse

### Requirement: Validación del Lean Canvas
La validación SHALL comprobar los nueve bloques, que cada `PRB` tenga su cadena `POR` con cinco niveles o su cierre anticipado justificado, que cada `SUP` esté definido y ordenado por riesgo, los códigos citados, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Problema sin porqués
- **WHEN** `PRB-02` no tiene cadena `POR`
- **THEN** la validación informa el archivo y el código
