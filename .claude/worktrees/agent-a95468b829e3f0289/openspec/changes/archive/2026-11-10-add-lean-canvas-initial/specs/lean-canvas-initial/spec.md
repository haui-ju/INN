## Purpose
Define el Lean Canvas inicial (v0) del proyecto: su playbook y modelos, las skills que lo crean y lo ajustan, los códigos de trazabilidad del problema, los porqués y los supuestos de riesgo, y su validación, como punto de partida del Design Thinking y del plan Lean.

## ADDED Requirements

### Requirement: Playbook y modelos de Lean Canvas
El repositorio SHALL incluir `common/lean/guia.md` con las secciones de Lean Canvas y 5 porqués (reglas, bloques, cantidades de referencia, errores frecuentes, checklist y referencias citables) y `common/lean/models/` con `lean-0-cinco-porques.md`, `lean-1-canvas.md` y un `README.md`, cada plantilla con ficha, instrucciones para el agente, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `02-make-initial-lean-canvas` va a escribir un entregable
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Playbook ampliable
- **WHEN** el cambio del plan Lean añade Lean Startup y Lean Change
- **THEN** amplía `common/lean/guia.md` sin renumerar las secciones de Lean Canvas

### Requirement: Recogida de información y coherencia con el proyecto
La skill SHALL leer del config el tema, el rubro, el tipo de proyecto y el resultado esperado y de `project/domain.md` el contexto, proponer un borrador completo y preguntar solo lo que falte; con `tipo: propio` SHALL NOT presuponer una empresa.

#### Scenario: Proyecto propio
- **WHEN** el config indica `tipo: propio`
- **THEN** el canvas describe segmentos y propuesta de valor sin referirse a una empresa existente

#### Scenario: Proyecto con empresa
- **WHEN** el config indica `tipo: empresa` y existe `domain.md`
- **THEN** los bloques usan el rubro y el contexto de la empresa de `domain.md`

### Requirement: Plan y confirmación antes de escribir
La skill SHALL mostrar el canvas propuesto (los nueve bloques, los problemas y sus supuestos de riesgo) y esperar la confirmación del usuario antes de crear archivos, ajustando la propuesta hasta que la confirme.

#### Scenario: Problema rechazado
- **WHEN** el usuario cambia el problema principal
- **THEN** la skill rehace los porqués y los bloques afectados, muestra de nuevo la propuesta y no escribe hasta la confirmación

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/initial-lean-canvas/<DD-MM-AAAA-HH-MM-SS>/` con `canvas.md`, `cinco-porques.md` y `README.md`, y SHALL registrarla en el paso `02-make-initial-lean-canvas` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma la propuesta
- **THEN** la corrida contiene los tres archivos y el paso 02 del config la incluye en su historial

### Requirement: Nueve bloques del Lean Canvas
`canvas.md` SHALL declarar la versión v0 y contener los nueve bloques (problema, segmentos de clientes, propuesta de valor única, solución, canales, fuentes de ingreso, estructura de costos, métricas clave y ventaja competitiva), cada uno completo y en el orden del playbook.

#### Scenario: Bloque vacío
- **WHEN** un bloque queda sin contenido
- **THEN** la validación lo informa con el nombre del bloque

### Requirement: Códigos de problema, porqués y supuestos
Cada problema SHALL llevar un código `PRB-nn` (el principal es `PRB-01`), cada cadena de porqués un código `POR-nn` ligado a su `PRB`, y cada supuesto de mayor riesgo un código `SUP-nn` con su bloque, nivel de riesgo (alto, medio o bajo) y una pista de cómo se validará.

#### Scenario: Supuestos ordenados
- **WHEN** se listan los supuestos
- **THEN** aparecen ordenados por riesgo, del más alto al más bajo

#### Scenario: Código citado sin definir
- **WHEN** el canvas cita `SUP-07` y no existe
- **THEN** la validación informa el archivo y el código

### Requirement: Cinco porqués
Cada problema SHALL tener una cadena de entre tres y cinco porqués que termina en una causa accionable, y SHALL citar el `PRB` del que parte; el problema principal SHALL resumirse en una frase que el Design Thinking pueda citar en `ENF-01`.

#### Scenario: Cadena sin causa accionable
- **WHEN** la última causa de una cadena no puede atacarse con la solución
- **THEN** la skill pide al usuario precisarla antes de confirmar

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (uno a tres problemas, tres a seis supuestos) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Siete supuestos
- **WHEN** el usuario pide siete supuestos
- **THEN** la skill avisa que el rango de referencia es tres a seis y respeta su decisión

### Requirement: Validación del Lean Canvas
La validación SHALL comprobar los nueve bloques, que cada `PRB` tenga su cadena `POR`, que cada `SUP` esté definido y ordenado por riesgo, los códigos citados, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Problema sin porqués
- **WHEN** `PRB-02` no tiene cadena `POR`
- **THEN** la validación informa el archivo y el código

### Requirement: Skill 02-make-initial-lean-canvas-update
La skill `02-make-initial-lean-canvas-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (bloque, problema, porqués o supuesto), mostrar el plan con los archivos y citas afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Cambio de un supuesto
- **WHEN** el usuario cambia el riesgo de `SUP-02`
- **THEN** la copia actualiza su fila, reordena la lista, deja el resto idéntico a la base y valida

#### Scenario: Código ya usado en otra corrida
- **WHEN** el usuario quita `SUP-03` y el plan Lean o el Design Thinking lo citan
- **THEN** la skill lo avisa en el plan y no modifica esas corridas

### Requirement: Texto limpio en el canvas
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Ejemplo de bloque
- **WHEN** el canvas muestra un segmento de clientes
- **THEN** usa contenido realista del proyecto sin etiquetas de procedencia
