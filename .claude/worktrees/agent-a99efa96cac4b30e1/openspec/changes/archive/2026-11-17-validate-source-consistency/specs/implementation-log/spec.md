## MODIFIED Requirements

### Requirement: Resultados de pruebas
La bitácora SHALL registrar los resultados de los casos de prueba con `CP` del diseño vigente, sprint, fecha, resultado (Pasó, Falló o No ejecutado) y observación, que es obligatoria cuando el resultado es Falló o No ejecutado; al cierre de cada sprint, todo caso del plan que verifique una historia terminada en ese sprint SHALL tener un resultado, y los casos de historias sin avance SHALL figurar como No ejecutado con su motivo.

#### Scenario: Caso inexistente
- **WHEN** un resultado cita `CP-15` y el plan de pruebas vigente no lo define
- **THEN** la validación informa el código

#### Scenario: Caso de una historia terminada sin resultado
- **WHEN** `HU-08` se terminó en el sprint 3 y el caso `CP-19`, que verifica uno de sus criterios, no tiene resultado
- **THEN** la validación informa el caso y la historia

#### Scenario: Caso sin ejecutar sin motivo
- **WHEN** un resultado es No ejecutado y no tiene observación
- **THEN** la validación informa el caso
