## MODIFIED Requirements

### Requirement: Recogida de información
La skill SHALL leer de `project/config.yaml` el tema, el enfoque, el resultado esperado y el modo de datos, y de `project/domain.md` el contexto, y SHALL preguntar al usuario solo lo que falte o no pueda deducir (por ejemplo el alcance por fases o si hay datos reales), sin repetir lo que ya consta.

#### Scenario: Config completo
- **WHEN** el usuario invoca la skill y el config tiene tema y enfoque
- **THEN** la skill no los pregunta y los usa en el plan

#### Scenario: Config ausente
- **WHEN** el usuario invoca la skill y no existe `project/config.yaml`
- **THEN** la skill indica que debe ejecutarse `00-init` y ofrece hacerlo antes de continuar

#### Scenario: Información incompleta
- **WHEN** el config no tiene el enfoque
- **THEN** la skill pregunta el enfoque, no lo asume y lo guarda en el config
