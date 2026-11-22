## Purpose
Define los resultados del ciclo Lean (punto 3.2.3) y la decisión de pivotar o perseverar (punto 3.2.4): las skills que los generan y los ajustan, la comparación con los criterios fijados en el plan, las evidencias y su validación.

## ADDED Requirements

### Requirement: Fuentes y prerrequisitos de los resultados Lean
La skill `17-make-lean-results` SHALL leer la corrida vigente del plan Lean (hipótesis, métricas, experimentos con su avance y criterio de éxito, y los criterios de pivotar o perseverar), la bitácora vigente, el Design Thinking vigente, el config (incluido `modo_datos`) y `project/domain.md`; si falta el plan o la bitácora SHALL avisarlo y preguntar si continúa.

#### Scenario: Sin plan Lean
- **WHEN** el config no tiene corrida de `07-make-lean-plan`
- **THEN** la skill lo avisa, ofrece ejecutarla y, si el usuario continúa, la validación marcará lo que no pueda comprobar

### Requirement: Preguntas y confirmación antes de escribir
La skill SHALL pedir, experimento por experimento, el resultado observado con su cifra y la evidencia; con `modo_datos` igual a `real` SHALL usar solo lo que el usuario aporta, SHALL proponer la decisión por hipótesis aplicando los criterios del plan, y SHALL mostrar todo y esperar la confirmación antes de crear archivos.

#### Scenario: Experimento sin ejecutar
- **WHEN** el usuario no ejecutó un experimento del avance 3
- **THEN** la skill no inventa resultado y lo deja en «Sin resultado» con su motivo

### Requirement: Estructura de salida de los resultados Lean
La skill SHALL crear cada corrida en `project/lean-results/<DD-MM-AAAA-HH-MM-SS>/` con `resultados.md` (3.2.3), `decision.md` (3.2.4), `evidencias/` y `README.md`, y SHALL registrarla en el paso `17-make-lean-results` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma los resultados y las decisiones
- **THEN** la corrida contiene los dos documentos, `evidencias/` y `README.md`, y el config la registra

### Requirement: Resultados de experimentos
`resultados.md` SHALL listar resultados `RES-nn` con el experimento, el avance, el resultado con una cifra, el criterio de éxito, si se cumplió (Sí, No o Parcial) y la evidencia, donde el avance y el criterio SHALL ser iguales a los del plan y todo experimento SHALL tener un resultado o figurar en «Sin resultado» con motivo.

#### Scenario: Criterio reescrito
- **WHEN** el criterio de éxito de `RES-01` difiere del que fijó el plan para `EXP-01`
- **THEN** la validación informa el código

#### Scenario: Experimento omitido
- **WHEN** `EXP-03` no tiene resultado ni figura en «Sin resultado»
- **THEN** la validación informa el código

### Requirement: Evidencia de los resultados
La evidencia de cada resultado SHALL citar códigos existentes de la bitácora (`BIT`, `CP`, `RIE`), de las historias (`HU`) o del Design Thinking (`TST`, `HAL-T`), o archivos de `evidencias/`, y la skill SHALL NOT generar imágenes.

#### Scenario: Archivo inexistente
- **WHEN** un resultado cita un archivo que no está en `evidencias/`
- **THEN** la validación informa el resultado y el archivo

### Requirement: Decisión de pivotar o perseverar
`decision.md` SHALL tener una fila por hipótesis con los resultados que la respaldan, el criterio aplicado, la decisión (Perseverar, Pivotar, Iterar o Pendiente) y su justificación, donde el criterio SHALL ser el texto exacto de «Perseverar si» o «Pivotar si» del plan según la decisión, «Zona de iterar» si es Iterar y «—» si es Pendiente, y una línea «Decisión general».

#### Scenario: Decisión que no corresponde al criterio
- **WHEN** la decisión es Pivotar y el criterio citado es el de «Perseverar si»
- **THEN** la validación informa la hipótesis

#### Scenario: Hipótesis sin decisión
- **WHEN** `HIP-02` no tiene fila
- **THEN** la validación informa el código

### Requirement: Validación de los resultados Lean
La validación SHALL comprobar la estructura, la trazabilidad contra el plan Lean, la bitácora y el Design Thinking vigentes, las evidencias, los códigos, las citas permitidas (Ries 2011 y Little 2014, máximo dos por archivo), los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Resultado de un experimento ajeno a la hipótesis
- **WHEN** una decisión cita `RES-02`, de un experimento que no pone a prueba esa hipótesis
- **THEN** la validación informa la hipótesis y el resultado

### Requirement: Skill 17-make-lean-results-update
La skill `17-make-lean-results-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (un resultado, una evidencia, una decisión o una justificación), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Corregir un resultado
- **WHEN** el usuario corrige la cifra de `RES-02`
- **THEN** la copia actualiza el resultado, si se cumplió, la decisión que lo cita y su justificación, y deja el resto idéntico a la base

#### Scenario: Análisis final que cita el resultado
- **WHEN** el análisis final vigente cita `RES-02`
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en los resultados Lean
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Resultado de un experimento
- **WHEN** se redacta el resultado observado
- **THEN** se usa el lenguaje del proyecto sin etiquetas de procedencia
