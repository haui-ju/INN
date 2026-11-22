# Spec Delta

## MODIFIED Requirements

### Requirement: Recogida de información
La skill SHALL leer del config (`project/config.json`) el tema, el enfoque, el resultado esperado, el contexto y el modo de datos, y SHALL preguntar al usuario solo lo que falte o no pueda deducir (por ejemplo el alcance por fases o si hay datos reales), sin repetir lo que ya consta.

#### Scenario: Config completo
- **WHEN** el usuario invoca la skill y el config tiene tema y enfoque
- **THEN** la skill no los pregunta y los usa en el plan

#### Scenario: Config ausente
- **WHEN** el usuario invoca la skill y no existe `project/config.json`
- **THEN** la skill indica que debe ejecutarse `00-init` y ofrece hacerlo antes de continuar

#### Scenario: Información incompleta
- **WHEN** el config no tiene el enfoque
- **THEN** la skill pregunta el enfoque, no lo asume y lo guarda en el config

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` con `README.md`, `documento.md`, `anexos.md` y una carpeta `bloques/` con una subcarpeta por fase generada, y SHALL registrar la corrida en el paso `05-make-design-thinking` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma un plan para todas las fases
- **THEN** la corrida contiene `README.md`, `documento.md`, `anexos.md` y las subcarpetas `fase-0` a `fase-5` dentro de `bloques/`

#### Scenario: Registro en el config
- **WHEN** la skill termina una corrida
- **THEN** el paso `05-make-design-thinking` del config incluye la corrida en su historial y, si no está fijada otra, como corrida vigente
