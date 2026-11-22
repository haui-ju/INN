## Purpose
Define los requerimientos del sistema (puntos 4.2 y 4.3 del informe): el playbook y sus modelos, la skill que deriva los requerimientos funcionales de los REQ del Design Thinking y propone los no funcionales medibles, la matriz de trazabilidad y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de requerimientos
El repositorio SHALL incluir `common/requirements/guia.md` (derivación desde los REQ, redacción y prioridad de los RF, categorías y medibilidad de los RNF, matriz, errores frecuentes, checklist y lista cerrada de referencias verificadas) y `common/requirements/models/` con `req-1-rf.md`, `req-2-rnf.md`, `req-3-matriz-trazabilidad.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `09-make-requirements` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer la corrida vigente de Design Thinking (los `REQ`, sus puntos de dolor y los hallazgos de prueba), la configuración de Scrum vigente, el config y, si existe, el plan Lean vigente; si falta el Design Thinking SHALL avisarlo y preguntar si continúa, porque sin `REQ` no hay requerimientos de origen.

#### Scenario: Sin Design Thinking
- **WHEN** el config no tiene corrida de Design Thinking
- **THEN** la skill lo avisa, ofrece ejecutar `05-make-design-thinking` y, si el usuario continúa, la validación marcará los RF sin origen

### Requirement: Plan y confirmación antes de escribir
La skill SHALL proponer los RF (al menos uno por `REQ`), su prioridad y los RNF con su categoría, métrica y meta, preguntar al usuario las prioridades, las categorías que aplican y el criterio de cada RNF, y esperar su confirmación antes de crear archivos.

#### Scenario: RNF de más
- **WHEN** el usuario pide diez RNF
- **THEN** la skill avisa que el rango de referencia es de cuatro a ocho y respeta su decisión

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/requirements/<DD-MM-AAAA-HH-MM-SS>/` con `rf.md` (punto 4.2), `rnf.md` (punto 4.3), `matriz-trazabilidad.md` y `README.md`, y SHALL registrarla en el paso `09-make-requirements` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene los cuatro archivos y el config la registra

### Requirement: Requerimientos funcionales trazables
Cada RF SHALL tener un código `RF-nn`, estar redactado como «El sistema debe…», citar al menos un `REQ` que exista en la corrida vigente de Design Thinking, tener una prioridad (`Debe`, `Debería` o `Podría`) y un criterio de verificación.

#### Scenario: RF sin origen
- **WHEN** `RF-04` no cita ningún `REQ`
- **THEN** la validación informa el código y la causa

#### Scenario: REQ inexistente
- **WHEN** un RF cita `REQ-09` y el Design Thinking vigente no lo define
- **THEN** la validación informa el código y la corrida

### Requirement: Requerimientos no funcionales medibles
Cada RNF SHALL tener un código `RNF-nn`, una categoría de la lista del playbook, una métrica, una meta con cifra, un origen (códigos del Design Thinking o de los RF, o «contexto») y cómo se verificará.

#### Scenario: RNF sin cifra
- **WHEN** la meta de `RNF-02` es «rápido»
- **THEN** la validación informa que la meta no tiene una cifra

#### Scenario: Categoría fuera de la lista
- **WHEN** un RNF usa una categoría que el playbook no define
- **THEN** la validación informa el código y la categoría

### Requirement: Matriz de trazabilidad REQ a RF
`matriz-trazabilidad.md` SHALL listar cada `REQ` del Design Thinking vigente con su funcionalidad y los RF que lo cubren, de modo que coincida con las citas de `rf.md`; un `REQ` sin RF SHALL indicar el motivo.

#### Scenario: REQ sin cubrir
- **WHEN** `REQ-05` no tiene RF ni motivo
- **THEN** la validación lo informa

#### Scenario: Matriz desalineada
- **WHEN** la matriz asigna `RF-03` a `REQ-02` pero `rf.md` lo cita para `REQ-03`
- **THEN** la validación informa la diferencia

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (uno a dos RF por `REQ` y cuatro a ocho RNF) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Tres RNF
- **WHEN** el usuario pide solo tres RNF
- **THEN** la skill avisa que el rango de referencia es de cuatro a ocho y respeta su decisión

### Requirement: Validación de los requerimientos
La validación SHALL comprobar la estructura de los archivos, la trazabilidad entre códigos, que los códigos del Design Thinking citados existan en su corrida vigente, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Código del Design Thinking inexistente
- **WHEN** un RNF cita `HAL-T-09` y esa corrida no lo define
- **THEN** la validación informa el código y que no existe en la corrida vigente

### Requirement: Skill 09-make-requirements-update
La skill `09-make-requirements-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (agregar, quitar o corregir RF y RNF, prioridad, criterio), mostrar el plan con los archivos y citas afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Quitar un RF
- **WHEN** el usuario quita `RF-03`
- **THEN** la copia actualiza `rf.md`, la matriz y los RNF que lo citaban, y deja el resto idéntico a la base

#### Scenario: RF usado por historias
- **WHEN** las historias de usuario vigentes citan `RF-03`
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en los requerimientos
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Requerimiento de ejemplo
- **WHEN** el playbook muestra un RF
- **THEN** usa contenido realista del proyecto sin etiquetas de procedencia
