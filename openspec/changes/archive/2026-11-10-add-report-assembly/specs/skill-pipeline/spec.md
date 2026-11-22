## ADDED Requirements

### Requirement: Prerrequisitos por avance
`pipeline.json` SHALL admitir en una skill el campo opcional `requiere_por_avance` (los pasos que la alimentan en cada avance), y la comprobación de prerrequisitos SHALL aceptar el avance (1, 2 o 3) y avisar solo de los pasos de ese avance, usando la unión de todos los avances cuando no se indica; las demás skills conservan `requiere`.

#### Scenario: Avance indicado
- **WHEN** se comprueba una skill con `requiere_por_avance` para el avance 2
- **THEN** solo se avisa de los pasos del avance 2 que ya existen como skill y no tienen corrida

#### Scenario: Skill sin el campo
- **WHEN** se comprueba una skill sin `requiere_por_avance`
- **THEN** la comprobación usa su lista `requiere` como hasta ahora
