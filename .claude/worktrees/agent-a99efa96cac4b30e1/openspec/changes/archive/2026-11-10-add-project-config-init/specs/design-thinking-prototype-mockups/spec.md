# Spec Delta

## MODIFIED Requirements

### Requirement: Selección de la corrida
La skill SHALL usar como corrida base la registrada en el config para el paso `05-make-design-thinking`, mostrarla al usuario para su confirmación y solo listar las corridas de `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` (de la más reciente a la más antigua) si el usuario la rechaza o el config no tiene una.

#### Scenario: Corrida vigente en el config
- **WHEN** el usuario invoca la skill y el config registra una corrida para el paso `05-make-design-thinking`
- **THEN** la skill la muestra como corrida base y pide confirmación en lugar de preguntar cuál usar

#### Scenario: Existen varias corridas
- **WHEN** el usuario invoca la skill, el config no registra una corrida del paso y hay dos o más corridas en `project/design-thinking/`
- **THEN** la skill lista las corridas con su fecha y hora y espera que el usuario elija una

#### Scenario: El usuario rechaza la corrida vigente
- **WHEN** el usuario no acepta la corrida del config y existen varias corridas
- **THEN** la skill lista las corridas con su fecha y hora y espera que el usuario elija una

#### Scenario: No existe ninguna corrida
- **WHEN** el usuario invoca la skill y `project/design-thinking/` no contiene corridas
- **THEN** la skill informa que no hay corridas, deriva a `05-make-design-thinking` y no crea tableros ni archivos

### Requirement: Insumos de la corrida
La skill SHALL leer de la corrida elegida las pantallas (`PAN`), los escenarios (`FLU`), los requerimientos (`REQ`) y, si existen, los hallazgos de prueba (`HAL-T`) antes de proponer el plan.

#### Scenario: La corrida no tiene fase 4
- **WHEN** la corrida elegida no contiene el inventario de pantallas de la fase 4
- **THEN** la skill se detiene, explica que faltan las pantallas y deriva a `05-make-design-thinking` para generar solo la fase 4, sin dibujar nada

#### Scenario: La corrida no tiene fase 5
- **WHEN** la corrida contiene la fase 4 pero no el reporte de la fase 5
- **THEN** la skill propone solo la sección v1 y omite la sección v2
