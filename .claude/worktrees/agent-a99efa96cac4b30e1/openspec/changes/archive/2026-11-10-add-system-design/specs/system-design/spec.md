## Purpose
Define el diseño del sistema del proyecto (puntos 5.1, 5.2, 5.3 y 5.5.1 del informe y los diagramas técnicos del anexo D.4): el playbook y sus modelos, las skills que lo generan y lo ajustan, la trazabilidad con los requerimientos, las historias y el prototipo, y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos del diseño del sistema
El repositorio SHALL incluir `common/system-design/guia.md` y `common/system-design/models/` con `sis-1-arquitectura.md`, `sis-2-modelo-datos.md`, `sis-3-interfaz.md`, `sis-4-plan-pruebas.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir las decisiones de arquitectura, el modelo de datos, el destino de las pantallas, el plan de pruebas y los diagramas como texto.

#### Scenario: Skill que necesita el formato
- **WHEN** `14-make-system-design` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer la corrida vigente de requerimientos (RF y RNF), la de historias (HU y CA), los `PAN` del Design Thinking vigente, el config y `project/domain.md`; si falta la de requerimientos o la de historias SHALL avisarlo y preguntar si continúa, y sin los mockups de `06-make-design-thinking-prototypes` SHALL avisar sin bloquear.

#### Scenario: Sin historias de usuario
- **WHEN** el config no tiene corrida de `10-make-user-stories`
- **THEN** la skill lo avisa, ofrece ejecutarla y, si el usuario continúa, la validación marcará los casos de prueba sin criterio de aceptación de origen

#### Scenario: Sin mockups en Miro
- **WHEN** el usuario no ejecutó `06-make-design-thinking-prototypes`
- **THEN** la skill continúa con los `PAN` del Design Thinking y avisa que no hay tablero de wireframes

### Requirement: Decisiones y confirmación antes de escribir
La skill SHALL preguntar el stack, el alojamiento y las restricciones del proyecto, proponer para cada decisión al menos dos alternativas con sus ventajas y desventajas, esperar la elección del usuario y mostrar el diseño completo antes de crear archivos.

#### Scenario: Stack sin elegir
- **WHEN** el usuario no decide el stack
- **THEN** la skill recomienda una opción con su motivo, la presenta como propuesta y no escribe nada hasta la confirmación

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/system-design/<DD-MM-AAAA-HH-MM-SS>/` con `arquitectura.md` (5.1), `modelo-datos.md` (5.2), `interfaz.md` (5.3), `plan-pruebas.md` (5.5.1), `diagramas/` y `README.md`, y SHALL registrarla en el paso `14-make-system-design` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el diseño
- **THEN** la corrida contiene los cuatro documentos, los diagramas y el `README.md`, y el config la registra

### Requirement: Arquitectura trazable
`arquitectura.md` SHALL listar decisiones `ADR-nn` (decisión, alternativas, motivo y RNF o «contexto») y componentes (responsabilidad, tecnología, RF que cubre, RNF que atiende y tablas), de modo que todo RF de la corrida vigente esté cubierto por un componente y todo RNF lo atienda una decisión o un componente.

#### Scenario: RF sin componente
- **WHEN** `RF-04` no figura en ningún componente
- **THEN** la validación informa el código

#### Scenario: Decisión sin alternativas
- **WHEN** `ADR-02` no indica alternativas consideradas
- **THEN** la validación informa el código

### Requirement: Modelo de datos
`modelo-datos.md` SHALL describir las tablas `TBL-nn` con sus campos principales y su clave primaria, las relaciones con su cardinalidad y el componente al que pertenece cada tabla, y toda tabla SHALL estar citada por un componente de `arquitectura.md`.

#### Scenario: Tabla huérfana
- **WHEN** `TBL-03` no la cita ningún componente
- **THEN** la validación informa el código

#### Scenario: Relación con tabla inexistente
- **WHEN** una relación nombra una tabla que no existe
- **THEN** la validación informa la relación

### Requirement: Diseño de interfaz
`interfaz.md` SHALL indicar el destino de cada `PAN` del prototipo (se conserva, se modifica o se descarta, con motivo) y listar las pantallas finales `UI-nn` con su `PAN` de origen o «—» si son nuevas, las historias que cubren y los cambios respecto al prototipo.

#### Scenario: PAN sin destino
- **WHEN** `PAN-04` del Design Thinking no figura en la tabla de destinos
- **THEN** la validación informa el código

#### Scenario: Pantalla nueva
- **WHEN** una pantalla final no proviene de ningún `PAN`
- **THEN** su origen es «—» y debe indicar la historia que la justifica

### Requirement: Plan de pruebas
`plan-pruebas.md` SHALL listar casos `CP-nn` con tipo (Unidad, Integración, Sistema o Aceptación), criterios de aceptación o RNF que verifican, pasos o datos y resultado esperado, de modo que todo `CA` y todo `RNF` tenga al menos un caso o figure en «Sin caso de prueba» con su motivo.

#### Scenario: CA sin caso
- **WHEN** `CA-05` no lo verifica ningún caso ni figura con motivo
- **THEN** la validación informa el código

#### Scenario: Caso sin origen
- **WHEN** `CP-07` no cita ningún `CA` ni `RNF`
- **THEN** la validación informa el código

### Requirement: Diagramas como texto
`diagramas/` SHALL contener como mínimo `componentes.mmd` y `modelo-datos.mmd` en sintaxis Mermaid, que mencionen todos los componentes y todas las tablas respectivamente, y SHALL poder tener diagramas de secuencia `secuencia-*.mmd`; el kit SHALL NOT generar imágenes.

#### Scenario: Componente ausente del diagrama
- **WHEN** `componentes.mmd` no menciona un componente de la arquitectura
- **THEN** la validación informa el componente

#### Scenario: Archivo que no es un diagrama
- **WHEN** un `.mmd` no empieza con un tipo de diagrama Mermaid
- **THEN** la validación informa el archivo

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (tres a seis decisiones de arquitectura, de tres a seis componentes, de tres a ocho tablas y al menos un caso por criterio de aceptación) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Doce tablas
- **WHEN** la propuesta tiene doce tablas
- **THEN** la skill avisa que el rango de referencia es de tres a ocho y respeta la decisión del usuario

### Requirement: Validación del diseño
La validación SHALL comprobar la estructura de los archivos, la trazabilidad contra la corrida vigente de requerimientos, de historias y el Design Thinking, la coherencia entre documentos y diagramas, las citas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: RF inexistente
- **WHEN** un componente cita `RF-09` y los requerimientos vigentes no lo definen
- **THEN** la validación informa el código y la corrida

### Requirement: Skill 14-make-system-design-update
La skill `14-make-system-design-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (decisiones, componentes, tablas, pantallas, casos de prueba o diagramas), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado, mantener los diagramas coherentes y validar.

#### Scenario: Agregar una tabla
- **WHEN** el usuario agrega `TBL-04`
- **THEN** la copia actualiza el modelo de datos, el componente que la usa, `modelo-datos.mmd` y los casos de prueba que correspondan, y deja el resto idéntico a la base

#### Scenario: Diseño usado en la bitácora
- **WHEN** la bitácora de implementación vigente cita `TBL-04`
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en el diseño del sistema
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Descripción de un componente
- **WHEN** la arquitectura describe un componente
- **THEN** usa el lenguaje del proyecto sin etiquetas de procedencia
