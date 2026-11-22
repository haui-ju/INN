## MODIFIED Requirements

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer el plan de sprints vigente (`gantt.json`), el tablero vigente (`tablero.json`), los tokens del sistema de diseño al que apunta `diseno` y el config; cada tablero SHALL generarse solo si existe su fuente, y si falta el sistema de diseño SHALL avisarlo y usar los tokens base de `01-design-system`. Además SHALL detectar qué visuales de `html-visuals` tienen fuente.

#### Scenario: Sin sistema de diseño
- **WHEN** `diseno` está vacío en el config
- **THEN** la skill lo avisa, ofrece `01-design-system` y, si continúa, usa los tokens base y lo anota en el `README.md`

#### Scenario: Sin tablero Kanban
- **WHEN** el config no tiene corrida de `12-make-ceremonies-kanban`
- **THEN** la skill genera solo el Gantt y avisa que el Kanban necesita ese paso

#### Scenario: Visuales disponibles
- **WHEN** existen las corridas de 02, 03 y 05 pero no las de 17 y 18
- **THEN** la skill ofrece los visuales de esas fuentes y avisa que los de 17 y 18 se suman después con el `-update`

### Requirement: Plan y confirmación antes de escribir
La skill SHALL preguntar la fecha de corte y el estado real (avance de las tareas, columna de las tarjetas y fechas reales) o si se muestra solo la línea base, preguntar qué visuales generar, presentar un resumen con los indicadores resultantes y esperar la confirmación antes de crear archivos.

#### Scenario: Solo línea base
- **WHEN** el usuario no tiene avance que informar
- **THEN** la skill genera los tableros con 0 % de avance y todas las tarjetas en la columna inicial, sin fecha de corte

#### Scenario: Elegir visuales
- **WHEN** el usuario pide solo el FODA y el Lean Canvas
- **THEN** el resumen lista esos dos visuales y la corrida no incluye otros

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/html-boards/<DD-MM-AAAA-HH-MM-SS>/` con `gantt.html`, `kanban.html` (los que correspondan), `data.json`, `README.md`, `leer-imagen/<visual>.md` por cada imagen y, si se eligieron visuales, `visuales/<visual>.html` con su `visuales/<visual>.json`, y SHALL registrarla en el paso `13-design-html-boards` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el resumen
- **THEN** la corrida contiene los tableros pedidos, `data.json`, los visuales elegidos y el `README.md`, y el config la registra

### Requirement: Validación de los tableros
La validación SHALL comprobar `data.json` contra el plan y el tablero vigentes, el estado y los indicadores, que cada HTML sea la plantilla con solo el bloque de tokens (los del sistema de diseño de `diseno`) y el de datos (iguales a `data.json`) sustituidos, los visuales de `visuales/` y las explicaciones de `leer-imagen/` según `html-visuals`, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Datos embebidos distintos
- **WHEN** el JSON embebido en `kanban.html` difiere de `data.json`
- **THEN** la validación informa el archivo y el bloque de datos

#### Scenario: Tokens distintos del diseño
- **WHEN** el bloque de tokens de `gantt.html` no corresponde a los tokens de `diseno`
- **THEN** la validación informa el archivo y el bloque de tokens

#### Scenario: Visual desactualizado
- **WHEN** `visuales/foda.json` difiere de la extracción actual
- **THEN** la validación informa el archivo y sugiere el `-update`

#### Scenario: Explicación que no coincide
- **WHEN** `leer-imagen/gantt.md` no corresponde a los datos actuales de `data.json`
- **THEN** la validación informa el archivo y que debe regenerarse

### Requirement: Skill 13-design-html-boards-update
La skill `13-design-html-boards-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (estado real, fecha de corte, resincronizar con el plan y el tablero, cambiar de diseño, agregar o actualizar visuales, cambiar un dato de un visual), mostrar el plan con los archivos afectados, esperar confirmación, editar `data.json`, volver a extraer los visuales y regenerar `leer-imagen/`, volver a copiar las plantillas con los datos y los tokens nuevos y validar, sin tocar lo que no depende del cambio.

#### Scenario: Actualizar el avance
- **WHEN** el usuario informa que `TAR-05` está al 60 % y la fecha de corte nueva
- **THEN** la copia actualiza `estado`, recalcula los indicadores, vuelve a copiar las plantillas y deja el resto idéntico a la base

#### Scenario: Cambió el diseño
- **WHEN** el config apunta a un sistema de diseño nuevo
- **THEN** la copia vuelve a copiar las plantillas con sus tokens sin tocar el estado

#### Scenario: Cambiar un dato de un visual
- **WHEN** el usuario pide cambiar un valor que se ve en un visual cuya fuente es otra skill
- **THEN** la skill indica la skill de origen, deja que su `-update` cambie solo ese dato y luego vuelve a extraer los visuales

#### Scenario: Agregar un visual tardío
- **WHEN** ya existe la corrida de 17 y la de tableros no tiene `resultados-lean`
- **THEN** la copia agrega `visuales/resultados-lean.html` y su JSON y deja lo demás igual
