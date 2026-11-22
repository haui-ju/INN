# Spec Delta

## Purpose

Define los visuales HTML del informe: plantillas autónomas en `common/html/`, su registro en el kit, la extracción de sus datos desde las secciones de una corrida, su construcción dentro de la corrida y el texto que explica cada imagen.

## ADDED Requirements

### Requirement: Plantillas de los visuales del capítulo 1
El repositorio SHALL incluir en `common/html/` las plantillas `bmc`, `pestel`, `foda` e `ishikawa`, cada una con `index.html` compilado, `README.md` (qué se cambia, esquema de datos y cómo obtener la imagen) y `mock.json` con datos de ejemplo de BI del esquema completo, y SHALL cumplir el contrato de `common/html/README.md` y las reglas de `common/html/DESIGN.md`.

#### Scenario: Plantilla autónoma
- **WHEN** se abre `common/html/ishikawa/index.html` sin conexión
- **THEN** se ve el diagrama con los datos del mock, sin recursos externos, con tema claro por defecto y los botones de imagen

#### Scenario: Plantillas sincronizadas
- **WHEN** se ejecuta `html_tpl.py comprobar`
- **THEN** informa que las plantillas coinciden con sus fuentes compiladas

### Requirement: FODA con estrategias cruzadas en el visual
La plantilla `foda` SHALL mostrar los cuatro cuadrantes y, debajo, las estrategias cruzadas FO, FA, DO y DA con su código, su texto y los ítems que combinan.

#### Scenario: Datos sin estrategias
- **WHEN** los datos del visual no traen estrategias
- **THEN** el visual muestra solo los cuadrantes

### Requirement: Registro de cada visual
Cada visual del informe SHALL estar registrado con su plantilla, la skill y la carpeta de origen, el extractor de datos, el título, una frase de propósito, la función que deriva qué dice la imagen y el archivo de origen; `visuales.py origen` SHALL informar la skill y el `-update` que lo cambian.

#### Scenario: Origen del Ishikawa
- **WHEN** se consulta el origen del visual `ishikawa`
- **THEN** responde `04-make-strategic-analysis`, `secciones/1.7.md` y `04-make-strategic-analysis-update`

### Requirement: Extracción desde las secciones de una corrida
El extractor de cada visual SHALL leer la tabla de su sección (`secciones/<punto>.md`) de la corrida indicada con `--run` o, si no se indica, de la vigente, y SHALL fallar con un motivo claro si falta la corrida, la sección o su tabla.

#### Scenario: Corrida aún sin registrar
- **WHEN** la skill construye el visual de una corrida nueva pasando `--run <corrida>`
- **THEN** los datos salen de esa corrida aunque el config aún apunte a otra

#### Scenario: Sección sin tabla
- **WHEN** `secciones/1.5.md` no tiene la tabla PESTEL
- **THEN** la extracción falla indicando la sección y la tabla que faltan

### Requirement: Construcción dentro de la corrida
`visuales.py construir` SHALL escribir `<visual>.json` y `<visual>.html` en la carpeta `visuales/` de la corrida y `leer-imagen/<visual>.md` junto a ella, con los tokens del sistema de diseño indicado o los tokens base.

#### Scenario: Visual del Canvas
- **WHEN** se construye `bmc` en una corrida de `03-make-business-diagnosis`
- **THEN** quedan `visuales/bmc.html`, `visuales/bmc.json` y `leer-imagen/bmc.md` en esa corrida

### Requirement: Texto «leer la imagen» derivado de los datos
El texto de `leer-imagen/<visual>.md` SHALL tener para qué sirve la imagen, qué dice (derivado de los datos) y el pie de foto sugerido, en tres frases como máximo y setenta palabras como máximo, y SHALL pasar la validación de explicaciones.

#### Scenario: Explicación del PESTEL
- **WHEN** se construye el visual `pestel`
- **THEN** su explicación dice cuántos hallazgos son oportunidades y cuántos amenazas y cumple los límites
