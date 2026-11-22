## ADDED Requirements

### Requirement: Playbook y modelos del brief
El repositorio SHALL incluir `common/project-brief/guia.md` y `common/project-brief/models/` con `brief-1-nucleo.md` (formato del brief y de `domain.md` con empresa o propio) y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir las preguntas por sección, cómo pulir una redacción, objetivos medibles, el calendario y la regla de lo pendiente.

#### Scenario: Skill que necesita el formato
- **WHEN** `00b-make-project-brief` va a escribir el brief
- **THEN** lee antes la guía y la plantilla y respeta su formato

### Requirement: Preguntas y pulido del brief
La skill `00b-make-project-brief` SHALL recorrer las secciones del brief una por una preguntando lo necesario, proponer una redacción de cada una a partir de lo que el usuario cuenta, ajustarla con él hasta su confirmación y escribir solo tras confirmar el resumen completo; lo que el usuario no sabe SHALL quedar como «Pendiente» y no redactarse como hecho.

#### Scenario: Respuesta incompleta
- **WHEN** el usuario no sabe la meta de un objetivo
- **THEN** la skill propone una meta, la presenta como propuesta y, si el usuario no la acepta, deja «Pendiente»

#### Scenario: Modo de datos real
- **WHEN** el config indica `modo_datos: real`
- **THEN** el brief usa solo lo que el usuario informa y marca el resto como «Pendiente»

### Requirement: Estructura del brief
La skill SHALL crear cada corrida en `project/project-brief/<DD-MM-AAAA-HH-MM-SS>/` con `brief.md` y `README.md`, y SHALL registrarla en el paso `00b-make-project-brief` del config; `brief.md` SHALL tener las secciones 1 Tema, 2 Problemática, 3 Objetivos, 4 Justificación y alcance, 5 Usuarios y enfoque, 6 Resultado esperado, 7 Calendario y 8 Supuestos y riesgos iniciales.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el resumen
- **THEN** la corrida contiene `brief.md` con las ocho secciones y el `README.md`, y el config la registra

### Requirement: Objetivos del brief
La sección 3 SHALL definir un objetivo general `OG-01` y al menos dos objetivos específicos `OE-nn`, cada uno con verbo, métrica, meta y plazo `Avance N (DD-MM-AAAA)` con N de 1 a 3, y cada `OE` SHALL indicar a qué `OG` aporta.

#### Scenario: Objetivo sin métrica
- **WHEN** un `OE` no tiene métrica ni meta
- **THEN** la validación informa el código y la causa

#### Scenario: Plazo fuera del calendario
- **WHEN** el plazo de `OE-02` cita una fecha distinta de la entrega del avance en el calendario
- **THEN** la validación informa el código y las dos fechas

### Requirement: Calendario de los tres sprints
La sección 7 SHALL tener tres filas (sprint, avance, inicio y entrega, en `DD-MM-AAAA`) con sprints en orden, sin solaparse, entrega posterior o igual al inicio de su sprint e inicio de cada sprint posterior al día de la entrega anterior.

#### Scenario: Sprints solapados
- **WHEN** el sprint 2 empieza antes de la entrega del sprint 1
- **THEN** la validación informa los dos sprints y sus fechas

#### Scenario: Fecha pendiente
- **WHEN** el usuario aún no conoce la entrega del avance 3
- **THEN** la fila queda «Pendiente», las skills posteriores la tratan como pendiente y `00b-make-project-brief-update` la completa

### Requirement: Coherencia con el config
La skill SHALL copiar al config el tema, el enfoque, el resultado esperado y las fechas de inicio y entrega de cada avance, y la validación SHALL exigir que coincidan con las secciones 1, 5, 6 y 7 del brief vigente.

#### Scenario: Tema distinto
- **WHEN** el tema del config difiere del de la sección 1 del brief
- **THEN** la validación informa los dos textos e indica `00b-make-project-brief-update`

### Requirement: domain.md creado por la skill
Tras confirmar el brief, la skill SHALL crear `project/domain.md` (con empresa, buscar los datos por el RUC y mostrarlos con su fuente; con proyecto propio, describir la solución con lo del brief), con la regla de marcar «(modelado por el agente, por no contar con X)» todo dato sin fuente.

#### Scenario: Proyecto con empresa
- **WHEN** el config indica `tipo: empresa` con RUC
- **THEN** la skill muestra los datos encontrados con su fuente, pide confirmación y los escribe en `domain.md`

### Requirement: Todas las skills leen el brief
Cada skill numerada a partir de `02-make-initial-lean-canvas` SHALL listar el brief vigente entre sus fuentes y tomar de él los datos del núcleo en lugar de preguntarlos, y el kit SHALL avisar, sin bloquear, cuando no hay corrida vigente del brief.

#### Scenario: Skill sin brief
- **WHEN** el usuario ejecuta `02-make-initial-lean-canvas` sin corrida de `00b-make-project-brief`
- **THEN** la skill avisa que falta el brief, indica ejecutarla y pregunta si continúa

#### Scenario: Objetivos ya definidos
- **WHEN** existe el brief
- **THEN** `03-make-company-chapter` copia `OG-01` y los `OE-nn` y no los vuelve a proponer

### Requirement: Validación del brief
La validación SHALL comprobar las secciones y tablas, los objetivos, el calendario, la coherencia con el config, que `domain.md` exista, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Sección ausente
- **WHEN** falta «## 6. Resultado esperado»
- **THEN** la validación informa el encabezado esperado

### Requirement: Skill 00b-make-project-brief-update
La skill `00b-make-project-brief-update` SHALL bifurcar la corrida base, pedir los cambios, mostrar el plan con las secciones afectadas y las skills que habría que actualizar después, esperar confirmación, editar solo lo afectado, copiar al config lo que cambie, regenerar `domain.md` solo si cambió el tema, el tipo o el RUC y validar.

#### Scenario: Cambiar una fecha
- **WHEN** el usuario mueve la entrega del avance 2
- **THEN** la copia cambia solo esa fila y los plazos que la citan, actualiza el config y avisa que hay que ejecutar `11-make-sprint-plan-update`

### Requirement: Texto limpio en el brief
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Objetivo redactado
- **WHEN** el brief muestra un objetivo
- **THEN** usa el texto sin etiquetas de procedencia
