## MODIFIED Requirements

### Requirement: Explicación de cada imagen
Por cada tablero y visual generado, el kit SHALL escribir `leer-imagen/<visual>.md` con una explicación de 2 a 3 frases que cumpla tres funciones: **para qué sirve** la imagen (frase fija del catálogo de propósitos del kit), **qué dice** (la conclusión que se desprende de los datos de la imagen, no un inventario de su contenido) y **por qué se resalta** lo resaltado (solo cuando la imagen resalta algo en esos datos), más un pie de foto sugerido. Lo que depende de la corrida SHALL derivarse solo de los datos de la imagen; el kit no SHALL usar texto escrito a mano por corrida.

#### Scenario: Explicación de la matriz de priorización
- **WHEN** se construye `matriz-priorizacion` con 23 ideas, de las cuales 7 caen en el cuadrante sombreado
- **THEN** `leer-imagen/matriz-priorizacion.md` dice para qué sirve la matriz, concluye cuántas ideas entran al MVP y por qué, y explica que el cuadrante sombreado reúne las ideas de impacto y factibilidad altos que cumplen el criterio de ingreso

#### Scenario: Explicación del FODA
- **WHEN** se construye el visual `foda` con 3 fortalezas, 3 debilidades, 2 oportunidades y 2 amenazas
- **THEN** `leer-imagen/foda.md` dice para qué sirve el FODA y concluye cómo se equilibra lo interno frente a lo externo, y trae un pie de foto sugerido

#### Scenario: Visual sin resaltado
- **WHEN** se construye el visual `foda`, que no resalta ningún elemento
- **THEN** su explicación lleva «para qué sirve» y «qué dice» y no incluye «por qué se resalta»

#### Scenario: Explicación del Kanban con una columna sobre su límite
- **WHEN** `kanban.html` tiene una columna con más tarjetas que su límite de trabajo en curso
- **THEN** `leer-imagen/kanban.md` explica que la columna se marca en rojo porque superó su límite y qué implica para el flujo

#### Scenario: Explicación del Gantt
- **WHEN** se genera `gantt.html` desde `data.json` con tareas atrasadas
- **THEN** `leer-imagen/gantt.md` indica para qué sirve el Gantt, concluye el avance real frente al plan y explica por qué se marcan las tareas atrasadas y la fecha de corte

## ADDED Requirements

### Requirement: Catálogo de propósitos de los visuales
El kit SHALL mantener un catálogo con una frase de propósito por visual y por tablero, fija y revisada con la plantilla, y SHALL declarar para cada visual qué elementos puede resaltar y con qué regla de los datos se decide. La explicación de una imagen NO SHALL generarse si su visual no tiene propósito en el catálogo.

#### Scenario: Visual sin propósito
- **WHEN** se agrega la plantilla de un visual nuevo y no tiene frase en el catálogo
- **THEN** `construir` y la validación informan que falta el propósito de ese visual

### Requirement: Validación de la explicación de la imagen
La validación SHALL exigir que cada `leer-imagen/<visual>.md` sea igual a la explicación derivada hoy de los datos, que contenga las funciones «para qué sirve» y «qué dice», que incluya «por qué se resalta» si y solo si los datos tienen elementos resaltados, y que no pase de 3 frases ni de 70 palabras en total sin contar el pie de foto; SHALL informar archivo y causa de cada incidencia.

#### Scenario: Explicación solo descriptiva
- **WHEN** `leer-imagen/foda.md` enumera las cantidades de cada cuadrante y no dice para qué sirve el FODA
- **THEN** la validación informa que falta la función «para qué sirve»

#### Scenario: Resaltado sin motivo
- **WHEN** el journey map tiene etapas marcadas en rojo y su explicación no dice por qué
- **THEN** la validación informa que falta «por qué se resalta»

#### Scenario: Explicación demasiado larga
- **WHEN** una explicación supera las 70 palabras
- **THEN** la validación informa el exceso
