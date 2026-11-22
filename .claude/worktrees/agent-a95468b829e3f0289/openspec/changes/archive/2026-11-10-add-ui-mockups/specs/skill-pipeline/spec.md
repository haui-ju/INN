## MODIFIED Requirements

### Requirement: Esquema de nombres de skills
Las skills del proyecto SHALL llamarse `[orden de dos dígitos][letra minúscula opcional]-[verbo]-[nombre]`, con los verbos `init`, `make` y `design`, y con el sufijo `-update` si son la homóloga de actualización de otra skill; la letra se reserva para un paso intercalado entre dos números existentes sin renumerarlos.

#### Scenario: Nombre de una skill de actualización
- **WHEN** se nombra la homóloga de actualización de `05-make-design-thinking`
- **THEN** se llama `05-make-design-thinking-update` y conserva el número de su skill

#### Scenario: Paso intercalado
- **WHEN** se agrega un paso entre `14-make-system-design` y `15-make-implementation-log`
- **THEN** se llama `14b-make-ui-mockups` y su homóloga `14b-make-ui-mockups-update`

### Requirement: Orden de las skills
El orden de ejecución de las skills SHALL ser una secuencia fija de veintiún pasos, de `00-init` a `19-make-report`, con `14b-make-ui-mockups` entre `14-make-system-design` y `15-make-implementation-log`, definida en `pipeline.json` con `orden` consecutivo.

#### Scenario: Secuencia completa
- **WHEN** se consulta `pipeline.json`
- **THEN** lista en orden los pasos `00-init` a `14-make-system-design`, `14b-make-ui-mockups` y `15-make-implementation-log` a `19-make-report`

#### Scenario: Listado de las skills
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** las skills del proyecto aparecen en el orden de ejecución
