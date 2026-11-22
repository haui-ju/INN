## MODIFIED Requirements

### Requirement: Skills sin homóloga de actualización
`19-make-report` SHALL NOT tener homóloga `-update`, porque el armado del informe se ejecuta de nuevo cada vez; `00-init` SHALL tener `00-init-update` para cambiar el config y `domain.md` sin repetir todas las preguntas.

#### Scenario: Corrección del armado del informe
- **WHEN** el usuario necesita rehacer el documento de un avance
- **THEN** ejecuta de nuevo `19-make-report` en lugar de una skill de actualización

#### Scenario: Cambio de un dato del proyecto
- **WHEN** el usuario necesita cambiar el equipo o una fecha
- **THEN** ejecuta `00-init-update` en lugar de repetir `00-init`
