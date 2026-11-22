# Spec Delta

## MODIFIED Requirements

### Requirement: Carpeta de corrida por fecha y hora
Toda skill de generación SHALL escribir su resultado en `project/<NN-carpeta>/<DD-MM-AAAA-HH-MM-SS>/`, donde `<NN-carpeta>` es la carpeta numerada del paso según `pipeline.json`, de modo que cada ejecución genere una carpeta nueva sin tocar las anteriores.

#### Scenario: Dos ejecuciones del mismo paso
- **WHEN** el usuario ejecuta dos veces la misma skill
- **THEN** se crean dos carpetas con fecha y hora distintas dentro de la carpeta numerada del paso y ninguna modifica a la otra

#### Scenario: Carpeta numerada
- **WHEN** `07-make-data-model-kpi` termina una corrida
- **THEN** su resultado queda en `project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/`

### Requirement: Patrón de las skills update
Cada skill de generación con homóloga `-update` SHALL, al ejecutarse esta, tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir al usuario la lista de cambios (agregar, quitar, corregir), aplicarlos solo a los archivos afectados de la copia y validar la coherencia.

#### Scenario: Corrección de una corrida
- **WHEN** el usuario pide quitar un KPI y corregir una dimensión en una corrida de modelo de datos
- **THEN** el fork modifica solo los archivos que contienen esos elementos y los que dependen de ellos
