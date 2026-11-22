## MODIFIED Requirements

### Requirement: Indicadores calculados
El kit SHALL calcular el avance global y por sprint, las tareas hechas, el tiempo de ciclo promedio en días, el rendimiento por semana, la cantidad de tarjetas por columna comparada con su límite WIP y las tareas atrasadas, y la validación SHALL recalcularlos y exigir que coincidan con `calculado` de `data.json`; los HTML SHALL mostrar los valores de `calculado` sin recalcularlos.

#### Scenario: Indicador desactualizado
- **WHEN** `calculado` indica 3 tareas hechas y el estado tiene 4
- **THEN** la validación informa el indicador y los dos valores

#### Scenario: Tablero que no recalcula
- **WHEN** `calculado` indica 4 tareas hechas
- **THEN** el HTML muestra 4 sin recontarlas

### Requirement: HTML autónomo con el sistema de diseño
Cada HTML SHALL ser una copia de su plantilla de `common/html/` que solo difiere en el bloque de tokens (variables CSS de color claro y oscuro, espacio, radio y sombra del sistema de diseño) y en el bloque de datos embebido (`data.json`), SHALL funcionar sin conexión y sin recursos externos, alternar entre ambos temas, adaptarse a pantalla de teléfono sin desplazamiento horizontal de la página y llevar los botones de imagen de la plantilla.

#### Scenario: Recurso externo
- **WHEN** un HTML carga un script o una hoja de estilos externa
- **THEN** la validación informa el archivo porque difiere de la plantilla

#### Scenario: Color distinto al token
- **WHEN** una variable `--c-acento` tiene un valor que no es el de los tokens
- **THEN** la validación informa que el bloque de tokens difiere

#### Scenario: Plantilla modificada a mano
- **WHEN** un HTML de la corrida tiene cambios fuera de los bloques de tokens y de datos
- **THEN** la validación informa el archivo y que debe volver a copiarse la plantilla

### Requirement: Validación de los tableros
La validación SHALL comprobar `data.json` contra el plan y el tablero vigentes, el estado y los indicadores, que cada HTML sea la plantilla con solo el bloque de tokens (los del sistema de diseño de `diseno`) y el de datos (iguales a `data.json`) sustituidos, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Datos embebidos distintos
- **WHEN** el JSON embebido en `kanban.html` difiere de `data.json`
- **THEN** la validación informa el archivo y el bloque de datos

#### Scenario: Tokens distintos del diseño
- **WHEN** el bloque de tokens de `gantt.html` no corresponde a los tokens de `diseno`
- **THEN** la validación informa el archivo y el bloque de tokens

### Requirement: Skill 13-design-html-boards-update
La skill `13-design-html-boards-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (estado real, fecha de corte, resincronizar con el plan y el tablero, cambiar de diseño), mostrar el plan con los archivos afectados, esperar confirmación, editar `data.json`, volver a copiar las plantillas con los datos y los tokens nuevos y validar.

#### Scenario: Actualizar el avance
- **WHEN** el usuario informa que `TAR-05` está al 60 % y la fecha de corte nueva
- **THEN** la copia actualiza `estado`, recalcula los indicadores, vuelve a copiar las plantillas y deja el resto idéntico a la base

#### Scenario: Cambió el diseño
- **WHEN** el config apunta a un sistema de diseño nuevo
- **THEN** la copia vuelve a copiar las plantillas con sus tokens sin tocar el estado
