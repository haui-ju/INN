## MODIFIED Requirements

### Requirement: Recogida de información y coherencia con el proyecto
La skill SHALL leer del brief vigente el tema, la problemática, los usuarios y el resultado esperado, del config el rubro y el tipo de proyecto y de `project/domain.md` el contexto, proponer un borrador completo y preguntar solo lo que falte; con `tipo: propio` SHALL NOT presuponer una empresa.

#### Scenario: Proyecto propio
- **WHEN** el config indica `tipo: propio`
- **THEN** el canvas describe segmentos y propuesta de valor sin referirse a una empresa existente

#### Scenario: Proyecto con empresa
- **WHEN** el config indica `tipo: empresa` y existe `domain.md`
- **THEN** los bloques usan el rubro y el contexto de la empresa de `domain.md`

#### Scenario: Problema principal
- **WHEN** el brief describe un problema principal
- **THEN** el canvas parte de él y no vuelve a preguntarlo
