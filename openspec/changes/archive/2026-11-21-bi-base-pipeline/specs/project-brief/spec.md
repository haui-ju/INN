# Spec Delta

## MODIFIED Requirements

### Requirement: Playbook y modelos del brief
El repositorio SHALL incluir `common/01-project-brief/guia.md` y `common/01-project-brief/models/` con `brief-1-nucleo.md` (formato del brief y de `domain.md` con empresa o propio) y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir las preguntas por sección, cómo pulir una redacción, objetivos medibles, el calendario y la regla de lo pendiente.

#### Scenario: Skill que necesita el formato
- **WHEN** `01-make-project-brief` va a escribir el brief
- **THEN** lee antes la guía y la plantilla y respeta su formato

### Requirement: Preguntas y pulido del brief
La skill `01-make-project-brief` SHALL recorrer las secciones del brief una por una preguntando lo necesario, proponer una redacción de cada una a partir de lo que el usuario cuenta, ajustarla con él hasta su confirmación y escribir solo tras confirmar el resumen completo; lo que el usuario no sabe SHALL quedar como «Pendiente» y no redactarse como hecho.

#### Scenario: Respuesta incompleta
- **WHEN** el usuario no sabe la meta de un objetivo
- **THEN** la skill propone una meta, la presenta como propuesta y, si el usuario no la acepta, deja «Pendiente»

#### Scenario: Modo de datos real
- **WHEN** el config indica `modo_datos: real`
- **THEN** el brief usa solo lo que el usuario informa y marca el resto como «Pendiente»

### Requirement: Estructura del brief
La skill SHALL crear cada corrida en `project/01-project-brief/<DD-MM-AAAA-HH-MM-SS>/` con `brief.md` y `README.md`, y SHALL registrarla en el paso `01-make-project-brief` del config; `brief.md` SHALL tener las secciones 1 Tema y empresa, 2 Problemática, 3 Objetivos, 4 Justificación y alcance, 5 Usuarios y decisiones que apoyará el dashboard, 6 Fuentes de datos previstas, 7 Calendario y 8 Supuestos y riesgos iniciales.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el resumen
- **THEN** la corrida contiene `brief.md` con las ocho secciones y el `README.md`, y el config la registra

### Requirement: Coherencia con el config
La skill SHALL copiar al config el tema y las fechas de inicio y entrega del calendario, y la validación SHALL exigir que coincidan con las secciones 1 y 7 del brief vigente.

#### Scenario: Tema distinto
- **WHEN** el tema del config difiere del de la sección 1 del brief
- **THEN** la validación informa los dos textos e indica `01-make-project-brief-update`

### Requirement: Todas las skills leen el brief
Cada skill numerada a partir de `03-make-business-diagnosis` SHALL listar el brief vigente entre sus fuentes y tomar de él los datos del núcleo en lugar de preguntarlos, y el kit SHALL avisar, sin bloquear, cuando no hay corrida vigente del brief.

#### Scenario: Skill sin brief
- **WHEN** el usuario ejecuta `03-make-business-diagnosis` sin corrida de `01-make-project-brief`
- **THEN** la skill avisa que falta el brief, indica ejecutarla y pregunta si continúa

#### Scenario: Objetivos ya definidos
- **WHEN** existe el brief
- **THEN** `05-make-problem-objectives` copia `OG-01` y los `OE-nn` y no los vuelve a proponer

## REMOVED Requirements

### Requirement: Calendario de los tres sprints
**Reason**: El proyecto tiene una sola entrega y ya no hay sprints.
**Migration**: Usar el requisito «Calendario único del brief».

### Requirement: Objetivos del brief
**Reason**: Se reemplaza por «Objetivos del brief de BI» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Objetivos del brief de BI».

### Requirement: Skill 00b-make-project-brief-update
**Reason**: Se reemplaza por «Skill 01-make-project-brief-update» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Skill 01-make-project-brief-update».

## ADDED Requirements

### Requirement: Calendario único del brief
La sección 7 SHALL tener una sola fila con inicio y entrega, en `DD-MM-AAAA`, con la entrega posterior o igual al inicio.

#### Scenario: Entrega anterior al inicio
- **WHEN** la entrega es anterior al inicio
- **THEN** la validación informa las dos fechas

#### Scenario: Fecha pendiente
- **WHEN** el usuario aún no conoce la fecha de entrega
- **THEN** la fila queda «Pendiente», las skills posteriores la tratan como pendiente y `01-make-project-brief-update` la completa

### Requirement: Objetivos del brief de BI
La sección 3 SHALL definir un objetivo general `OG-01` y al menos dos objetivos específicos `OE-nn`, cada uno con verbo, métrica, meta y plazo `Entrega (DD-MM-AAAA)` igual a la fecha de entrega del calendario, y cada `OE` SHALL indicar a qué `OG` aporta y qué indicador de negocio o KPI del dashboard permitirá medirlo.

#### Scenario: Objetivo sin métrica
- **WHEN** un `OE` no tiene métrica ni meta
- **THEN** la validación informa el código y la causa

#### Scenario: Plazo fuera del calendario
- **WHEN** el plazo de `OE-02` cita una fecha distinta de la entrega del calendario
- **THEN** la validación informa el código y las dos fechas

#### Scenario: Objetivo sin indicador
- **WHEN** un `OE` no indica el KPI o indicador con que se medirá
- **THEN** la validación informa el código

### Requirement: Skill 01-make-project-brief-update
La skill `01-make-project-brief-update` SHALL bifurcar la corrida base, pedir los cambios, mostrar el plan con las secciones afectadas y las skills que habría que actualizar después, esperar confirmación, editar solo lo afectado, copiar al config lo que cambie, regenerar `domain.md` solo si cambió el tema, el tipo o el RUC y validar.

#### Scenario: Cambiar la fecha de entrega
- **WHEN** el usuario mueve la fecha de entrega
- **THEN** la copia cambia la fila del calendario y los plazos que la citan, actualiza el config y avisa que hay que revisar las skills cuyas corridas citan esa fecha
