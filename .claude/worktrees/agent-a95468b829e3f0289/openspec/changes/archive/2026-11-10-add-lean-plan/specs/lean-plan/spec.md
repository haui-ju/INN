## Purpose
Define el plan Lean del proyecto (puntos 3.2 a 3.4 del informe): el playbook ampliado y sus modelos, las skills que lo generan y lo ajustan, las hipótesis, el MVP textual, los experimentos y criterios de decisión, la gestión del cambio, el canvas validado v1 y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos del plan Lean
`common/lean/guia.md` SHALL incluir las secciones de Lean Startup, Lean Change Management y Canvas validado v1 (con errores frecuentes, checklist y referencias) sin renumerar las de Lean Canvas, y `common/lean/models/` SHALL incluir `lean-2-hipotesis-supuestos.md`, `lean-3-mvp.md`, `lean-4-ciclo-medir-aprender.md`, `lean-5-gestion-cambio.md` y `lean-6-canvas-validado.md`, cada una con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `07-make-lean-plan` va a escribir una sección
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Playbook previo intacto
- **WHEN** se compara la guía con la del Lean Canvas inicial
- **THEN** las secciones de Lean Canvas y de 5 porqués conservan su numeración

### Requirement: Fuentes y prerrequisitos del plan
La skill SHALL leer el canvas v0 vigente, la corrida vigente de Design Thinking, el config y `project/domain.md`; si falta alguno de los dos primeros SHALL avisarlo y preguntar si continúa, y sin Design Thinking SHALL NOT generar el canvas v1.

#### Scenario: Sin Design Thinking
- **WHEN** el config no tiene corrida de Design Thinking
- **THEN** la skill lo avisa, ofrece ejecutar `05-make-design-thinking` y, si el usuario continúa, deja el canvas v1 sin generar

#### Scenario: Proyecto propio
- **WHEN** el config indica `tipo: propio`
- **THEN** los actores y el cambio se describen sin presuponer una empresa

### Requirement: Plan y confirmación antes de escribir
La skill SHALL preguntar qué supuestos priorizar, cuántos experimentos son viables en tres sprints y el criterio de éxito de cada métrica, mostrar el plan completo (hipótesis, MVP, experimentos, actores y cambios del canvas) y esperar la confirmación antes de crear archivos.

#### Scenario: Experimentos de más
- **WHEN** el usuario pide seis experimentos de negocio
- **THEN** la skill avisa que el rango de referencia es de dos a cuatro y respeta su decisión

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/lean-plan/<DD-MM-AAAA-HH-MM-SS>/` con `seccion-3-2.md`, `seccion-3-3.md`, `canvas-v1.md` y `README.md`, y SHALL registrarla en el paso `07-make-lean-plan` del config al terminar; el `README.md` SHALL anotar las corridas base usadas.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene los cuatro archivos y el config la registra

### Requirement: Hipótesis falsables y trazables
Cada hipótesis SHALL tener un código `HIP-nn`, estar formulada de modo que pueda refutarse, citar al menos un `SUP` del canvas v0, tener una métrica `MET-nn` y un criterio de éxito, y SHALL citar la evidencia previa (`HAL-E`, `PP` o `REQ`) cuando exista en el Design Thinking.

#### Scenario: Hipótesis sin métrica
- **WHEN** `HIP-03` no tiene métrica
- **THEN** la validación informa el código y la causa

#### Scenario: Supuesto del canvas sin hipótesis
- **WHEN** un supuesto de riesgo alto no es cubierto por ninguna hipótesis
- **THEN** la validación lo informa

### Requirement: MVP textual
El punto 3.2.2 SHALL describir el MVP como alcance, no como software: los `REQ` que incluye (tomados de los de 3.1.4.3), lo que no incluye y qué `HIP` prueba cada `REQ`, y todo `REQ` citado SHALL existir en la corrida vigente de Design Thinking.

#### Scenario: Requerimiento inexistente
- **WHEN** el MVP cita `REQ-09` y el Design Thinking vigente solo define cinco
- **THEN** la validación informa el código y la corrida

### Requirement: Ciclo construir-medir-aprender
El punto 3.2.3 SHALL listar los experimentos `EXP-nn` (hipótesis que ponen a prueba, método, métrica, criterio de éxito y avance en que se ejecutan) y las métricas de aprendizaje `MET-nn`, y cada experimento SHALL asignarse a uno de los tres avances.

#### Scenario: Experimento sin avance
- **WHEN** un experimento no indica el avance
- **THEN** la validación informa el código

### Requirement: Criterios de pivotar o perseverar
El punto 3.2.4 SHALL fijar para cada hipótesis, antes de ejecutar los experimentos, cuándo se persevera y cuándo se pivota, y SHALL dejar la decisión final para los resultados (punto de `17-make-lean-results`).

#### Scenario: Hipótesis sin criterio
- **WHEN** una `HIP` no aparece en la tabla de criterios
- **THEN** la validación lo informa

### Requirement: Gestión del cambio
Los puntos 3.3.1 a 3.3.3 SHALL describir qué cambia en el negocio (`CAM-nn` con antes y después), el ciclo de insights `INS`, opciones `OPC` y experimentos de cambio `EXP`, y los actores `ACT-nn` con su resistencia esperada y la acción de acompañamiento, de modo que cada opción cite un insight, cada experimento de cambio una opción y cada cambio un actor existente.

#### Scenario: Opción sin insight
- **WHEN** `OPC-02` no cita ningún insight
- **THEN** la validación informa el código

### Requirement: Canvas validado v1
`canvas-v1.md` SHALL declarar la versión v1, tener los nueve bloques del v0, el estado de cada supuesto (validado, refutado o pendiente, con su evidencia o su `HIP`) y una tabla `Bloque | v0 | v1 | Evidencia` que liste exactamente los bloques cuyo texto difiere del v0, citando evidencia existente en el Design Thinking vigente.

#### Scenario: Cambio no registrado
- **WHEN** el bloque «Solución» difiere del v0 y no figura en la tabla
- **THEN** la validación lo informa

#### Scenario: Supuesto sin estado
- **WHEN** `SUP-02` del v0 no aparece en el v1
- **THEN** la validación lo informa

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (tres a seis hipótesis, dos a cuatro experimentos de negocio, dos a cuatro de cambio, dos a cinco actores) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Una sola hipótesis
- **WHEN** el usuario pide una hipótesis
- **THEN** la skill avisa que el rango de referencia es de tres a seis y respeta su decisión

### Requirement: Marcas de avance de los puntos Lean
El índice `common/structure/model1.md` SHALL marcar 3.2.3, 3.2.4, 3.3 y 3.4 con `[A1+]`.

#### Scenario: Revisión del índice
- **WHEN** se revisa el índice tras este cambio
- **THEN** los cuatro puntos llevan la marca `[A1+]` y las demás se conservan

### Requirement: Validación del plan Lean
La validación SHALL comprobar la estructura de los tres archivos, la trazabilidad entre códigos, la coherencia con el canvas v0 vigente (`SUP`, `PRB`), que los códigos del Design Thinking citados existan en su corrida vigente, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Código del Design Thinking inexistente
- **WHEN** una hipótesis cita `HAL-E-07` y esa corrida no lo define
- **THEN** la validación informa el código y que no existe en la corrida vigente de Design Thinking

### Requirement: Skill 07-make-lean-plan-update
La skill `07-make-lean-plan-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (hipótesis, experimentos, métricas, actores o canvas v1), mostrar el plan con los archivos y citas afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Quitar una hipótesis
- **WHEN** el usuario quita `HIP-04`
- **THEN** la copia actualiza sus experimentos, métricas, criterios y supuestos asociados y el canvas v1 si cambiaba por ella, y deja el resto idéntico a la base

#### Scenario: Resultados ya registrados
- **WHEN** `HIP-02` ya tiene resultados en `lean-results`
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en el plan Lean
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Hipótesis de ejemplo
- **WHEN** el plan describe una hipótesis sobre los usuarios
- **THEN** usa contenido realista del proyecto sin etiquetas de procedencia
