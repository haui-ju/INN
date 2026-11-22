## MODIFIED Requirements

### Requirement: Orden de las skills
El orden de ejecución de las skills SHALL ser una secuencia fija, de `00-init` a `19-make-report`, con `00b-make-project-brief` entre `00-init` y `01-design-system` y `14b-make-ui-mockups` entre `14-make-system-design` y `15-make-implementation-log`, seguida de `21-make-app-definition` y `22-make-app-technical-definition`, definida en `pipeline.json` con `orden` consecutivo. Las dos últimas SHALL tener homóloga `-update`, su corrida SHALL guardarse en `project/app/definition/` y SHALL requerir `14-make-system-design`; `22-make-app-technical-definition` SHALL requerir además `21-make-app-definition`.

#### Scenario: Secuencia completa
- **WHEN** se consulta `pipeline.json`
- **THEN** lista en orden `00-init`, `00b-make-project-brief`, `01-design-system` a `14-make-system-design`, `14b-make-ui-mockups`, `15-make-implementation-log` a `19-make-report`, `21-make-app-definition` y `22-make-app-technical-definition`

#### Scenario: Listado de las skills
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** las skills del proyecto aparecen en el orden de ejecución

#### Scenario: Prerrequisito de la definición técnica
- **WHEN** el usuario ejecuta `22-make-app-technical-definition` y `21-make-app-definition` no tiene corrida
- **THEN** la skill avisa cuál falta y pregunta si continúa

#### Scenario: Carpeta de la corrida
- **WHEN** `21-make-app-definition` termina una corrida
- **THEN** su resultado queda en `project/app/definition/<DD-MM-AAAA-HH-MM-SS>/` y se registra en `pasos` del config
