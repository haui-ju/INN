## MODIFIED Requirements

### Requirement: Campos del config
El config SHALL contener `proyecto` (nombre, tema, tipo `empresa` o `propio`, `ruc` solo si es empresa, y rubro), `enfoque` (A, B o C), `resultado_esperado`, `equipo` (nombre y rol opcional, que si existe es `Product Owner`, `Scrum Master` o `Equipo de desarrollo`), `avances` (tres entradas con número, sprint y fecha), `modo_datos` (`generado` o `real`), `diseno` (ruta dentro de `project/` o vacío), `dominio` (ruta a `project/domain.md`) y `pasos`.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** el config contiene todos esos campos, con `avances` de longitud 3 y `pasos` vacío

#### Scenario: Rol no permitido
- **WHEN** se escribe un rol distinto de los tres de Scrum
- **THEN** la escritura se rechaza y se informa de los valores válidos

## ADDED Requirements

### Requirement: Roles Scrum del equipo
El reparto de roles SHALL escribirse en `equipo[].rol` mediante una función del kit que acepte solo un reparto con exactamente un Product Owner, exactamente un Scrum Master y al menos un integrante del equipo de desarrollo, que nombre solo a personas del equipo y que deje a todos con un rol; `00-init-update` SHALL poder cambiarlo con las mismas reglas.

#### Scenario: Reparto completo
- **WHEN** la skill de Scrum confirma cuatro roles válidos
- **THEN** el config guarda el rol de cada integrante y conserva sus comentarios

#### Scenario: Dos Product Owner
- **WHEN** se intenta guardar un reparto con dos Product Owner
- **THEN** la escritura se rechaza, el config no cambia y se informa la causa
