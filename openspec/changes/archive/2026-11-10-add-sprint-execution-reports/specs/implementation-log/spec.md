## Purpose
Define la bitácora de implementación del proyecto (punto 5.4 del informe, resultados de pruebas por sprint y riesgos y cambios): el playbook y sus modelos, las skills que la generan y la ajustan, la trazabilidad con el plan de sprints, el diseño del sistema y las historias, y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de los informes de sprint
El repositorio SHALL incluir `common/sprint-reports/guia.md` y `common/sprint-reports/models/` con `log-1-bitacora-sprint.md`, `rep-1-informe-avance.md`, `rep-2-acta-review-retro.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir la bitácora, los resultados de pruebas, los riesgos y cambios, las evidencias, el informe de avance, la Sprint Review y la retrospectiva.

#### Scenario: Skill que necesita el formato
- **WHEN** `15-make-implementation-log` va a escribir `bitacora.md`
- **THEN** lee antes la guía y `log-1-bitacora-sprint.md` y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos de la bitácora
La skill SHALL leer la corrida vigente del plan de sprints (sprints, `HU` y `TAR`), la del diseño del sistema (componentes, `TBL`, `UI` y `CP`), la de historias, el config (incluido `modo_datos`) y `project/domain.md`; si falta el plan o el diseño SHALL avisarlo y preguntar si continúa.

#### Scenario: Sin diseño del sistema
- **WHEN** el config no tiene corrida de `14-make-system-design`
- **THEN** la skill lo avisa, ofrece ejecutarla y, si el usuario continúa, la validación marcará los `TBL`, `UI` y `CP` que no pueda comprobar

### Requirement: Preguntas y confirmación antes de escribir
La skill SHALL preguntar los sprints a registrar, las historias que avanzaron o se terminaron, los módulos, las evidencias disponibles, los resultados de las pruebas y los riesgos y cambios, usando el plan como guía por historia y tarea; con `modo_datos` igual a `real` SHALL usar solo lo que el usuario aporta, y SHALL mostrar el registro completo y esperar confirmación antes de crear archivos.

#### Scenario: Dato no aportado
- **WHEN** el usuario no informa el estado de una tarea
- **THEN** la skill no lo inventa y lo deja como «En curso» solo si el usuario lo confirma, o sin entrada

### Requirement: Estructura de salida de la bitácora
La skill SHALL crear cada corrida en `project/implementation-log/<DD-MM-AAAA-HH-MM-SS>/` con `bitacora.md`, `evidencias/` y `README.md`, y SHALL registrarla en el paso `15-make-implementation-log` del config; la bitácora SHALL acumular todos los sprints registrados y los sprints nuevos se agregan con la skill `-update`.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el registro
- **THEN** la corrida contiene `bitacora.md`, la carpeta `evidencias/` y el `README.md`, y el config la registra

### Requirement: Módulos de implementación
`bitacora.md` SHALL tener `## 5.4. Implementación por módulos` con un `### 5.4.n.` por módulo acordado, que cite sus historias, su componente, sus tablas y sus pantallas existentes en el plan y el diseño, de modo que toda historia con avance pertenezca a un módulo.

#### Scenario: Historia sin módulo
- **WHEN** `HU-02` tiene entradas de bitácora y ningún módulo la cita
- **THEN** la validación informa el código

### Requirement: Entradas de bitácora
La bitácora SHALL listar entradas `BIT-nn` con fecha, sprint, historia, tarea, módulo, qué se hizo, estado (Terminado, En curso o Bloqueado) y evidencia, de modo que la fecha caiga dentro del sprint, la tarea exista y sea de la historia citada, y la evidencia sea un archivo de `evidencias/` o «—».

#### Scenario: Fecha fuera del sprint
- **WHEN** `BIT-04` es del sprint 1 con una fecha posterior a su fin
- **THEN** la validación informa el código

#### Scenario: Evidencia inexistente
- **WHEN** `BIT-02` cita un archivo que no está en `evidencias/`
- **THEN** la validación informa el código y el archivo

### Requirement: Resultados de pruebas
La bitácora SHALL registrar los resultados de los casos de prueba con `CP` del diseño vigente, sprint, fecha, resultado (Pasó, Falló o No ejecutado) y observación, que es obligatoria cuando el resultado es Falló.

#### Scenario: Caso inexistente
- **WHEN** un resultado cita `CP-15` y el plan de pruebas vigente no lo define
- **THEN** la validación informa el código

### Requirement: Riesgos y cambios
La bitácora SHALL registrar riesgos y cambios del plan como `RIE-nn` con sprint, fecha, tipo (Riesgo o Cambio), descripción, efecto en el plan y las historias o tareas afectadas, que existen en el plan vigente.

#### Scenario: Cambio sin efecto
- **WHEN** `RIE-01` no indica su efecto en el plan
- **THEN** la validación informa el código

### Requirement: Validación de la bitácora
La validación SHALL comprobar la estructura, la trazabilidad contra el plan, el diseño y las historias vigentes, las fechas, las evidencias, los códigos, las citas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Código repetido
- **WHEN** `BIT-03` aparece definido dos veces
- **THEN** la validación informa el código

### Requirement: Skill 15-make-implementation-log-update
La skill `15-make-implementation-log-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (agregar un sprint, corregir o quitar una entrada, sumar una evidencia, mover una historia entre sprints, resultados de pruebas, riesgos), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Agregar el sprint 2
- **WHEN** el usuario agrega las entradas del sprint 2
- **THEN** la copia añade las entradas, los resultados y los riesgos, actualiza los módulos si corresponde y deja el sprint 1 idéntico a la base

#### Scenario: Informe que cita la entrada
- **WHEN** un informe de sprint vigente cita `BIT-04`, que el usuario corrige
- **THEN** la skill lo avisa en el plan y no modifica ese informe

### Requirement: Texto limpio en la bitácora
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Entrada de bitácora
- **WHEN** se describe qué se hizo en una tarea
- **THEN** se usa el lenguaje del proyecto sin etiquetas de procedencia
