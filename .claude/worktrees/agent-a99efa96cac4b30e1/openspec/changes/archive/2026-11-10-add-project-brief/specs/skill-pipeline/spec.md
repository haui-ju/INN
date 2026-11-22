## MODIFIED Requirements

### Requirement: Orden de las skills
El orden de ejecución de las skills SHALL ser una secuencia fija de veintidós pasos, de `00-init` a `19-make-report`, con `00b-make-project-brief` entre `00-init` y `01-design-system` y `14b-make-ui-mockups` entre `14-make-system-design` y `15-make-implementation-log`, definida en `pipeline.json` con `orden` consecutivo.

#### Scenario: Secuencia completa
- **WHEN** se consulta `pipeline.json`
- **THEN** lista en orden `00-init`, `00b-make-project-brief`, `01-design-system` a `14-make-system-design`, `14b-make-ui-mockups` y `15-make-implementation-log` a `19-make-report`

#### Scenario: Listado de las skills
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** las skills del proyecto aparecen en el orden de ejecución

## ADDED Requirements

### Requirement: El brief como fuente común
Todas las skills numeradas a partir de `02-make-initial-lean-canvas` SHALL listar el brief vigente en sus fuentes obligatorias y tomar de él el tema, la problemática, los objetivos, el alcance, los usuarios, el resultado esperado y el calendario que necesiten, sin volver a preguntarlos.

#### Scenario: Revisión de las fuentes
- **WHEN** se revisa el `SKILL.md` de cualquier skill de `02` a `19`
- **THEN** cita el brief de `00b-make-project-brief` entre sus fuentes
