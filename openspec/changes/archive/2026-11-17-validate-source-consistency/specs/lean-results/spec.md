## MODIFIED Requirements

### Requirement: Decisión de pivotar o perseverar
`decision.md` SHALL tener una fila por hipótesis con los resultados que la respaldan, el criterio aplicado, la decisión (Perseverar, Pivotar, Iterar o Pendiente) y su justificación, donde el criterio SHALL ser el texto exacto de «Perseverar si», «Iterar si» o «Pivotar si» del plan según la decisión y «—» si es Pendiente, y una línea «Decisión general».

#### Scenario: Decisión que no corresponde al criterio
- **WHEN** la decisión es Pivotar y el criterio citado es el de «Perseverar si»
- **THEN** la validación informa la hipótesis

#### Scenario: Hipótesis sin decisión
- **WHEN** `HIP-02` no tiene fila
- **THEN** la validación informa el código

#### Scenario: Iterar sin zona en el plan
- **WHEN** la decisión es Iterar y el plan vigente no define «Iterar si» para esa hipótesis
- **THEN** la validación informa la hipótesis y que debe completarse el plan con `07-make-lean-plan-update`

### Requirement: Validación de los resultados Lean
La validación SHALL comprobar la estructura, la trazabilidad contra el plan Lean, la bitácora y el Design Thinking vigentes, las evidencias, los códigos, que el estado de cada supuesto en el canvas v1 vigente coincida con las decisiones (Perseverar es validado, Pivotar es refutado, Iterar y Pendiente son pendiente), las citas permitidas (Ries 2011 y Little 2014, máximo dos por archivo), los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Resultado de un experimento ajeno a la hipótesis
- **WHEN** una decisión cita `RES-02`, de un experimento que no pone a prueba esa hipótesis
- **THEN** la validación informa la hipótesis y el resultado

#### Scenario: Supuesto pendiente con decisión tomada
- **WHEN** `HIP-03` se decidió Perseverar y `SUP-05` sigue pendiente en el canvas v1
- **THEN** la validación informa el supuesto y que debe actualizarse con `07-make-lean-plan-update`
