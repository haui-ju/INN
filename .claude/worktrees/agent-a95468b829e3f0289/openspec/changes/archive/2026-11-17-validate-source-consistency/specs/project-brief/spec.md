## MODIFIED Requirements

### Requirement: Objetivos del brief
La sección 3 SHALL definir un objetivo general `OG-01` y al menos dos objetivos específicos `OE-nn`, cada uno con verbo, métrica, meta y plazo `Avance N (DD-MM-AAAA)` con N de 1 a 3, cada `OE` SHALL indicar a qué `OG` aporta, y cada objetivo SHALL declarar sobre qué se medirá (prototipo, sistema o piloto) de modo que su plazo caiga en un avance en el que esa base existe.

#### Scenario: Objetivo sin métrica
- **WHEN** un `OE` no tiene métrica ni meta
- **THEN** la validación informa el código y la causa

#### Scenario: Plazo fuera del calendario
- **WHEN** el plazo de `OE-02` cita una fecha distinta de la entrega del avance en el calendario
- **THEN** la validación informa el código y las dos fechas

#### Scenario: Objetivo sin base de medición
- **WHEN** un objetivo no declara si se mide sobre el prototipo, el sistema o un piloto
- **THEN** la validación informa el código

#### Scenario: Plazo anterior a la base de medición
- **WHEN** un objetivo se mide sobre el sistema y su plazo es el Avance 1, cuando todavía no hay sistema
- **THEN** la validación informa el código y el avance en que existe la base
