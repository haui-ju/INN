# run-versioning Specification

## Purpose
Define cómo se versionan las corridas de las skills de generación (carpetas por fecha y hora, bifurcación `-fork`), el patrón de las skills `-update` que corrigen una corrida sin regenerarla, la validación de coherencia y la regla compartida de texto limpio.

## Requirements

### Requirement: Carpeta de corrida por fecha y hora
Toda skill de generación SHALL escribir su resultado en `project/<NN-carpeta>/<DD-MM-AAAA-HH-MM-SS>/`, donde `<NN-carpeta>` es la carpeta numerada del paso según `pipeline.json`, de modo que cada ejecución genere una carpeta nueva sin tocar las anteriores.

#### Scenario: Dos ejecuciones del mismo paso
- **WHEN** el usuario ejecuta dos veces la misma skill
- **THEN** se crean dos carpetas con fecha y hora distintas dentro de la carpeta numerada del paso y ninguna modifica a la otra

#### Scenario: Carpeta numerada
- **WHEN** `07-make-data-model-kpi` termina una corrida
- **THEN** su resultado queda en `project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/`

### Requirement: README de procedencia
Cada corrida SHALL incluir un `README.md` en su raíz que registre su procedencia (modo de datos y, en un fork, la corrida de origen y los cambios), y esa SHALL ser la única mención de procedencia dentro de la corrida.

#### Scenario: Corrida con datos generados
- **WHEN** se genera una corrida con `modo_datos` igual a `generado`
- **THEN** solo su `README.md` indica la procedencia y ningún otro archivo de la corrida la menciona

### Requirement: Texto limpio compartido
Ningún archivo de una corrida, salvo su `README.md`, SHALL contener términos que califiquen los datos como falsos, inventados, ficticios, simulados, ilustrativos o de prueba, y esta regla SHALL estar definida en un solo lugar del kit compartido.

#### Scenario: Revisión de una corrida
- **WHEN** el validador revisa los archivos de una corrida
- **THEN** reporta cualquier término prohibido encontrado fuera del `README.md` con su archivo y línea

### Requirement: Bifurcación de una corrida
La bifurcación SHALL copiar la corrida base a `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>-fork/`, sin modificar la base, y anotar en el `README.md` de la copia la corrida de origen.

#### Scenario: Fork de la corrida vigente
- **WHEN** se bifurca la corrida vigente de un paso
- **THEN** existe una carpeta nueva con sufijo `-fork`, idéntica a la base salvo su `README.md`, y la base queda intacta

### Requirement: Patrón de las skills update
Cada skill de generación con homóloga `-update` SHALL, al ejecutarse esta, tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir al usuario la lista de cambios (agregar, quitar, corregir), aplicarlos solo a los archivos afectados de la copia y validar la coherencia.

#### Scenario: Corrección de una corrida
- **WHEN** el usuario pide quitar un KPI y corregir una dimensión en una corrida de modelo de datos
- **THEN** el fork modifica solo los archivos que contienen esos elementos y los que dependen de ellos

### Requirement: Update sin regenerar
Las skills `-update` SHALL NOT regenerar la corrida completa: los archivos no afectados por los cambios SHALL quedar idénticos byte a byte a los de la base.

#### Scenario: Archivos no afectados
- **WHEN** termina un update
- **THEN** una comparación del fork con la base muestra diferencias solo en los archivos afectados y en el `README.md`

### Requirement: Validador de coherencia
El kit compartido SHALL incluir un validador que compruebe, sobre una corrida, que los códigos de trazabilidad citados existen, que las referencias entre archivos resuelven, que las fracciones y cifras repetidas coinciden y que se cumple el texto limpio, e informe cada incidencia.

#### Scenario: Código citado que no existe
- **WHEN** un archivo cita un código de evidencia que ya no está definido
- **THEN** el validador lo informa con su archivo y el código

### Requirement: Registro del fork en el config
Al terminar un update, la skill SHALL registrar el fork en el `historial` del paso y, si `fijada` no es `true`, convertirlo en la corrida vigente; si la validación falla, SHALL conservar el fork, no cambiar la corrida vigente e informar al usuario de las incidencias.

#### Scenario: Validación fallida
- **WHEN** el validador reporta incidencias sobre el fork
- **THEN** el fork se conserva, `run` no cambia y se muestra la lista de incidencias
