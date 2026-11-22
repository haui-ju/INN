## MODIFIED Requirements

### Requirement: Plan de pruebas
`plan-pruebas.md` SHALL listar casos `CP-nn` con numeración consecutiva, tipo (Unidad, Integración, Sistema o Aceptación), criterios de aceptación o RNF que verifican, pasos o datos y resultado esperado, de modo que todo `CA` y todo `RNF` tenga al menos un caso o figure en «Sin caso de prueba» con su motivo, y que no haya dos casos con el mismo tipo, la misma verificación y los mismos datos.

#### Scenario: CA sin caso
- **WHEN** `CA-05` no lo verifica ningún caso ni figura con motivo
- **THEN** la validación informa el código

#### Scenario: Caso sin origen
- **WHEN** `CP-07` no cita ningún `CA` ni `RNF`
- **THEN** la validación informa el código

#### Scenario: Hueco en la numeración
- **WHEN** existen `CP-22` y `CP-25` y no `CP-23` ni `CP-24`
- **THEN** la validación informa los códigos faltantes

#### Scenario: Casos duplicados
- **WHEN** `CP-22` y `CP-34` tienen el mismo tipo, verifican el mismo `RNF` y usan los mismos datos
- **THEN** la validación informa ambos casos
