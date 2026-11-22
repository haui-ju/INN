## MODIFIED Requirements

### Requirement: Trazabilidad y coherencia
La skill SHALL asignar códigos de evidencia según el playbook y SHALL mantener consistentes las cifras, fracciones y referencias entre fases, documento y anexos; cada idea marcada «incluir» SHALL alimentar al menos un `REQ`, las cifras de ideas incluidas y de `REQ` del alcance del MVP SHALL explicar su relación (por ejemplo, varias ideas en un mismo `REQ`), y los códigos `HAL-T` SHALL ser consecutivos sin huecos de numeración.

#### Scenario: Cifra repetida en dos fases
- **WHEN** una cifra de la fase 1 se cita en la fase 2
- **THEN** ambas coinciden y la fase 2 cita el código de evidencia de origen

#### Scenario: Ideas y requerimientos que no cuadran
- **WHEN** la matriz incluye 7 ideas y el alcance del MVP lista 6 `REQ` sin explicar cómo se agrupan
- **THEN** la validación informa ambas cifras y que debe explicarse la relación

#### Scenario: Idea incluida sin requerimiento
- **WHEN** la idea `IDE-09` está marcada «incluir» y ningún `REQ` la cita
- **THEN** la validación informa el código

#### Scenario: Hueco en los hallazgos de prueba
- **WHEN** existen `HAL-T-02` y `HAL-T-04` y no `HAL-T-01` ni `HAL-T-03`
- **THEN** la validación informa los códigos faltantes
