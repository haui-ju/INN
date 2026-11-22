## Purpose
Define las historias de usuario del proyecto (puntos 4.4.1, 4.4.2 y 4.5 del informe): el playbook y sus modelos, las skills que derivan las historias de los requerimientos, sus criterios de aceptación, el Product Backlog priorizado y la Definition of Done, y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de historias de usuario
El repositorio SHALL incluir `common/user-stories/guia.md` y `common/user-stories/models/` con `hu-1-historia.md`, `hu-2-criterios-aceptacion.md`, `hu-3-definition-of-done.md`, `hu-4-product-backlog.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `10-make-user-stories` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

#### Scenario: Contenido de la guía
- **WHEN** se revisa `guia.md`
- **THEN** incluye el formato de la historia, los criterios INVEST, los criterios Dado/Cuando/Entonces, la Definition of Done, las escalas de estimación, el orden del backlog, los errores frecuentes, el checklist y referencias verificadas

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer la corrida vigente de requerimientos (RF y RNF), la configuración de Scrum vigente (quién es Product Owner), el plan Lean vigente si existe y el config; si falta la de requerimientos SHALL avisarlo y preguntar si continúa, porque sin RF no hay historias de origen.

#### Scenario: Sin requerimientos
- **WHEN** el config no tiene corrida de `09-make-requirements`
- **THEN** la skill lo avisa, ofrece ejecutarla y, si el usuario continúa, la validación marcará las historias sin RF de origen

### Requirement: Acuerdo de historias y confirmación
La skill SHALL proponer primero la lista de historias derivada de los RF (título, quién, qué y para qué), esperar que el usuario las confirme, quite, cambie o agregue, y solo entonces proponer los criterios de aceptación; SHALL pedir una segunda confirmación del conjunto antes de crear archivos.

#### Scenario: Historia quitada
- **WHEN** el usuario quita una historia propuesta
- **THEN** la skill no genera sus criterios y avisa si algún RF queda sin historia

#### Scenario: Historia sin RF
- **WHEN** el usuario pide una historia que no corresponde a ningún RF
- **THEN** la skill propone agregarla primero a los requerimientos y no la crea

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/user-stories/<DD-MM-AAAA-HH-MM-SS>/` con `historias/HU-nn.md`, `backlog.md` (punto 4.4.2), `criterios-dod.md` (punto 4.5) y `README.md`, y SHALL registrarla en el paso `10-make-user-stories` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene un archivo por historia, el backlog, el resumen de criterios con la Definition of Done y el `README.md`, y el config la registra

### Requirement: Historia de usuario trazable
Cada historia SHALL tener un código `HU-nn` y un título, estar redactada como «Como…, quiero…, para…», citar los RF de los que nace con los REQ que resultan de ellos, e indicar los RNF que le aplican o «Ninguno».

#### Scenario: Historia sin RF
- **WHEN** `HU-04` no cita ningún RF
- **THEN** la validación informa el código y la causa

#### Scenario: REQ derivado incorrecto
- **WHEN** la historia muestra `REQ-03` pero su RF cita `REQ-02`
- **THEN** la validación informa la diferencia

### Requirement: Criterios de aceptación
Cada historia SHALL tener al menos dos criterios `CA-nn`, cada uno con escenario, Dado, Cuando y Entonces, y los códigos `CA` SHALL ser únicos en toda la corrida.

#### Scenario: Historia con un criterio
- **WHEN** `HU-02` tiene un solo criterio
- **THEN** la validación informa la historia y el mínimo

#### Scenario: Código repetido
- **WHEN** dos historias usan `CA-03`
- **THEN** la validación informa el código

### Requirement: Cobertura de los requerimientos funcionales
Todo RF de la corrida vigente de requerimientos SHALL tener al menos una historia que lo cite o figurar en «RF sin historia» del backlog con su motivo.

#### Scenario: RF sin cubrir
- **WHEN** `RF-05` no tiene historia ni motivo
- **THEN** la validación informa el código

### Requirement: Product Backlog priorizado
`backlog.md` SHALL declarar la escala de estimación y el criterio de orden y listar todas las historias, numeradas desde 1 sin repetir, con su prioridad igual a la más alta de sus RF, en orden de mayor a menor prioridad, y con una estimación de la escala declarada.

#### Scenario: Orden incorrecto
- **WHEN** una historia `Debería` aparece antes que una `Debe`
- **THEN** la validación informa el orden

#### Scenario: Estimación fuera de la escala
- **WHEN** una historia se estima en 4 y la escala declarada es 1, 2, 3, 5, 8, 13
- **THEN** la validación informa la historia y la escala

### Requirement: Definition of Done
`criterios-dod.md` SHALL resumir los criterios de aceptación por historia, de modo que coincidan con los de los archivos de historias, y listar al menos cinco condiciones observables de la Definition of Done, que el Product Owner confirma.

#### Scenario: Resumen desalineado
- **WHEN** el resumen de `HU-01` omite `CA-02`
- **THEN** la validación informa la diferencia

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (una a tres historias por RF, dos a cinco criterios por historia y ocho a veinte historias en total) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Treinta historias
- **WHEN** la lista propuesta supera las veinte historias
- **THEN** la skill avisa el rango de referencia y respeta la decisión del usuario

### Requirement: Validación de las historias de usuario
La validación SHALL comprobar la estructura de los archivos, la trazabilidad contra la corrida vigente de requerimientos, la coherencia entre historias, backlog y resumen de criterios, las citas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: RF inexistente
- **WHEN** una historia cita `RF-09` y los requerimientos vigentes no lo definen
- **THEN** la validación informa el código y la corrida

### Requirement: Skill 10-make-user-stories-update
La skill `10-make-user-stories-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (agregar, quitar o corregir historias y criterios, orden, estimación, Definition of Done), mostrar el plan con los archivos y citas afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Quitar una historia
- **WHEN** el usuario quita `HU-03`
- **THEN** la copia quita su archivo, su fila del backlog y sus criterios del resumen, renumera solo el orden del backlog y deja el resto idéntico a la base

#### Scenario: Historia usada en el plan de sprints
- **WHEN** el plan de sprints vigente cita `HU-03`
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en las historias de usuario
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Historia de ejemplo
- **WHEN** el playbook muestra una historia
- **THEN** usa contenido realista del proyecto sin etiquetas de procedencia
