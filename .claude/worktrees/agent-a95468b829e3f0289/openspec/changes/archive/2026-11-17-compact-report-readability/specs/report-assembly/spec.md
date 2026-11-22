## ADDED Requirements

### Requirement: Densidad de códigos en la prosa
El armado SHALL escribir la prosa del informe con el nombre primero y el código una sola vez entre paréntesis, con no más de dos códigos por frase, y SHALL colapsar en un rango («TST-01 a TST-08») toda serie de tres o más códigos consecutivos del mismo prefijo. Dentro de las tablas SHALL conservar los códigos completos como llaves.

#### Scenario: Serie de requerimientos
- **WHEN** una frase cita REQ-01, REQ-02, REQ-03, REQ-04, REQ-05 y REQ-06
- **THEN** el informe la escribe como «REQ-01 a REQ-06»

#### Scenario: Nombre antes que el código
- **WHEN** una frase hace referencia a la historia HU-08
- **THEN** el informe escribe el nombre de la historia seguido de «(HU-08)» y no solo el código

#### Scenario: Códigos en tablas
- **WHEN** una tabla trae una columna de evidencia con varios códigos
- **THEN** la columna conserva los códigos completos o su rango y no se resume en prosa

### Requirement: Colocación por bloque en el cuerpo o en un anexo
El armado SHALL permitir colocar en el cuerpo o en el anexo G cada bloque extenso declarado como trasladable en `report_map.json`: historias de usuario con criterios de aceptación (4.4.1), resumen de criterios (4.5), Gantt completo (4.6.2), casos de prueba (5.5.1) y glosario (2.4). La skill SHALL preguntar la colocación de cada bloque, con la vigente del índice como valor por omisión, y, cuando se elija el anexo, SHALL dejar en el cuerpo un resumen de una a tres frases con el enlace al bloque.

#### Scenario: Casos de prueba al anexo
- **WHEN** el usuario elige colocar los casos de prueba en el anexo
- **THEN** el punto 5.5.1 conserva su resumen y un enlace a G.2, y la tabla completa aparece solo en G.2

#### Scenario: Sin elección
- **WHEN** el usuario acepta los valores por omisión
- **THEN** el informe sale con la colocación vigente del índice

#### Scenario: Bloque en el cuerpo
- **WHEN** el usuario elige mantener el glosario en el cuerpo
- **THEN** el punto 2.4 trae la tabla completa y el anexo G no incluye G.4

### Requirement: Sin contenido repetido entre secciones
El armado SHALL mostrar cada bloque una sola vez: el Product Backlog completo solo en 4.4.2 (4.6.1 lo cita y muestra únicamente la asignación por sprint), el resumen de criterios de 4.5 solo cuando no se incluyan los criterios dentro de las historias, y los participantes de las ceremonias una sola vez en 4.7 antes de sus cuatro subpuntos.

#### Scenario: Backlog y sprints
- **WHEN** se arma 4.6.1
- **THEN** la tabla de historias por sprint no repite el título, la estimación ni la prioridad ya mostrados en 4.4.2

#### Scenario: Participantes de las ceremonias
- **WHEN** las cuatro ceremonias comparten los mismos participantes
- **THEN** 4.7 los lista una vez y solo indica las diferencias en cada ceremonia

### Requirement: Validación de densidad y de colocación
La validación SHALL fallar cuando un párrafo fuera de tablas supere el máximo de códigos por frase, cuando quede una serie consecutiva sin colapsar, cuando un bloque trasladado aparezca a la vez en el cuerpo y en el anexo G o sin su resumen y su enlace, y cuando un enlace al anexo G no resuelva; SHALL informar punto y causa.

#### Scenario: Frase con demasiados códigos
- **WHEN** una frase del cuerpo cita cinco códigos distintos
- **THEN** la validación informa el punto y el exceso

#### Scenario: Bloque duplicado
- **WHEN** la tabla de casos de prueba aparece en 5.5.1 y en G.2
- **THEN** la validación informa que el bloque está duplicado

#### Scenario: Bloque trasladado sin enlace
- **WHEN** el glosario va al anexo y 2.4 no lleva el enlace a G.4
- **THEN** la validación informa el punto
