## ADDED Requirements

### Requirement: Pasos de la app en el orden de las skills
`pipeline.json` SHALL declarar `24-make-app-scaffold` y su homóloga `-update` después de las skills de definición y de plan de la app, con prerrequisitos el TRD y el plan de implementación vigentes, y SHALL comprobar esos prerrequisitos como los demás pasos.

#### Scenario: Prerrequisito faltante
- **WHEN** se ejecuta `projectcfg.py check --skill 24-make-app-scaffold` sin corrida del TRD
- **THEN** la comprobación avisa que falta ese paso

#### Scenario: Orden de carpetas
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** `24-make-app-scaffold` aparece después de las skills de definición de la app
