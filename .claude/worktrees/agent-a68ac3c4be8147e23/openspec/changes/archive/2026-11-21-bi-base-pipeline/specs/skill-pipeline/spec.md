# Spec Delta

## MODIFIED Requirements

### Requirement: Preguntar y confirmar
Toda skill de generación SHALL preguntar al usuario lo que necesite y no esté en el config, y SHALL presentar sus propuestas (por ejemplo objetivos, KPI o visuales) para que el usuario las acepte, rechace o corrija antes de generar.

#### Scenario: Propuesta rechazada
- **WHEN** el usuario rechaza una propuesta
- **THEN** la skill la ajusta con sus correcciones y vuelve a presentarla antes de continuar

### Requirement: Playbook propio con modelos y formularios
Toda skill de generación que necesite un método SHALL apoyarse en un playbook propio en `common/<NN-tema>/guia.md` con sus plantillas en `common/<NN-tema>/models/`, con reglas, pasos, cantidades de referencia, formularios y checklist, y cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill sin playbook
- **WHEN** se crea una skill de generación sin playbook
- **THEN** su creación incluye el playbook y las plantillas correspondientes

### Requirement: Ampliación del índice del informe
Cuando una skill requiera puntos o anexos que el índice (`common/structure/model1.md`) no contempla, el cambio que crea la skill SHALL ampliar el índice sin alterar la numeración de los capítulos 1 a 5 y SHALL declarar las secciones nuevas en `pipeline.json`.

#### Scenario: Skill que necesita un anexo nuevo
- **WHEN** una skill produce evidencias que no caben en los anexos actuales
- **THEN** su cambio agrega el anexo al índice y a la skill en `pipeline.json`

### Requirement: El brief como fuente común
Todas las skills numeradas a partir de `03-make-business-diagnosis` SHALL listar el brief vigente en sus fuentes obligatorias y tomar de él el tema, la problemática, los objetivos, el alcance, los usuarios y el calendario que necesiten, sin volver a preguntarlos.

#### Scenario: Revisión de las fuentes
- **WHEN** se revisa el `SKILL.md` de cualquier skill de `03` a `11`
- **THEN** cita el brief de `01-make-project-brief` entre sus fuentes

## REMOVED Requirements

### Requirement: Prerrequisitos por avance
**Reason**: El proyecto tiene una sola entrega y ya no hay avances; los prerrequisitos de cada skill son una lista única.
**Migration**: Declarar los pasos que alimentan una skill solo en `requiere` de `pipeline.json`.

### Requirement: Pasos de la app en el orden de las skills
**Reason**: La app y su scaffold se retiran del pipeline.
**Migration**: Ninguna; los pasos de BI se declaran en `pipeline.json` según el orden de las skills.

### Requirement: Esquema de nombres de skills
**Reason**: Se reemplaza por «Esquema de nombres numerados» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Esquema de nombres numerados».

### Requirement: Orden de las skills
**Reason**: Se reemplaza por «Secuencia de las skills de BI» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Secuencia de las skills de BI».

### Requirement: Skills sin homóloga de actualización
**Reason**: Se reemplaza por «Skills de ensamblado sin homóloga de actualización» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Skills de ensamblado sin homóloga de actualización».

## ADDED Requirements

### Requirement: Esquema de nombres numerados
Las skills del proyecto SHALL llamarse `[orden de dos dígitos]-[verbo]-[nombre]`, con los verbos `init`, `make` y `design`, sin letras intercaladas, y con el sufijo `-update` si son la homóloga de actualización de otra skill; la carpeta que produce una skill en `project/` y en `common/` SHALL llevar su mismo número y su nombre sin el verbo `make` (con `design` se conserva el nombre completo).

#### Scenario: Nombre de una skill de actualización
- **WHEN** se nombra la homóloga de actualización de `04-make-strategic-analysis`
- **THEN** se llama `04-make-strategic-analysis-update` y conserva el número de su skill

#### Scenario: Carpeta de salida
- **WHEN** `03-make-business-diagnosis` produce una corrida
- **THEN** su resultado queda en `project/03-business-diagnosis/` y su playbook en `common/03-business-diagnosis/`

#### Scenario: Skill de diseño
- **WHEN** se nombra la carpeta de `02-design-system`
- **THEN** es `project/02-design-system/` y `common/02-design-system/`

### Requirement: Secuencia de las skills de BI
El orden de ejecución de las skills SHALL ser una secuencia fija y consecutiva, definida en `pipeline.json` con `orden` igual al número de la skill: `00-init`, `01-make-project-brief`, `02-design-system`, `03-make-business-diagnosis`, `04-make-strategic-analysis`, `05-make-problem-objectives`, `06-make-bi-solution`, `07-make-data-model-kpi`, `08-make-etl`, `09-make-dashboard`, `10-make-storytelling`, `11-make-conclusions`, `12-make-report` y `13-make-annex-html`.

#### Scenario: Secuencia completa
- **WHEN** se consulta `pipeline.json`
- **THEN** lista las skills de `00` a `13` en ese orden, sin números repetidos ni huecos

#### Scenario: Listado de las skills
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** las skills del proyecto aparecen en el orden de ejecución

#### Scenario: Skill retirada
- **WHEN** se revisa `.claude/skills/`
- **THEN** no existen skills de Design Thinking, Lean, Scrum, Kanban, sprints, historias, diseño de sistema, bitácora ni app

### Requirement: Skills de ensamblado sin homóloga de actualización
`12-make-report` y `13-make-annex-html` SHALL NOT tener homóloga `-update`, porque se ejecutan de nuevo cada vez; `00-init` SHALL tener `00-init-update` para cambiar el config y `domain.md` sin repetir todas las preguntas.

#### Scenario: Corrección del informe armado
- **WHEN** el usuario necesita rehacer el documento
- **THEN** ejecuta de nuevo `12-make-report` en lugar de una skill de actualización

#### Scenario: Cambio de un dato del proyecto
- **WHEN** el usuario necesita cambiar el equipo o una fecha
- **THEN** ejecuta `00-init-update` en lugar de repetir `00-init`
