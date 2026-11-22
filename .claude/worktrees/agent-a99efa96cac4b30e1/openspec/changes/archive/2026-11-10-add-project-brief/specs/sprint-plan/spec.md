## MODIFIED Requirements

### Requirement: Sprints y fechas
`plan-sprints.md` SHALL tener tres sprints cuyo inicio y fin coincidan con el inicio y la entrega de cada avance en el config (copia del calendario del brief), y cada uno con una capacidad en puntos y un objetivo del sprint; si el inicio del primer sprint está vacío SHALL avisarlo y remitir a `00b-make-project-brief-update`, y los inicios sin dato SHALL ser el día posterior al fin del sprint anterior.

#### Scenario: Sprint que no termina en la fecha del avance
- **WHEN** el sprint 2 termina el 20-12-2026 y el config indica 31-12-2026
- **THEN** la validación informa el sprint y las dos fechas

#### Scenario: Sin inicio del proyecto
- **WHEN** `avances[0].inicio` está vacío
- **THEN** la skill lo avisa y no pregunta el inicio por su cuenta: indica `00b-make-project-brief-update`
