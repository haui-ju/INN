## ADDED Requirements

### Requirement: Anexo G de detalle de tablas del informe
El índice SHALL incluir el anexo G, «Detalle de tablas del informe», con los puntos G.1 Historias de usuario y criterios de aceptación, G.2 Casos de prueba, G.3 Diagrama de Gantt completo y G.4 Glosario, como destino opcional de los bloques extensos del cuerpo, sin cambiar la numeración de los capítulos ni de los anexos A a F.

#### Scenario: Revisión de la numeración
- **WHEN** se revisan los títulos de los anexos del índice
- **THEN** G aparece después de F con G.1 a G.4 una sola vez y los anexos A a F conservan su numeración

#### Scenario: Anexo G sin bloques elegidos
- **WHEN** ningún bloque se traslada al anexo
- **THEN** el informe no incluye el anexo G

### Requirement: Bloques trasladables declarados en el índice
El índice SHALL marcar cuáles puntos admiten colocación en el cuerpo o en el anexo G (4.4.1, 4.5, 4.6.2, 5.5.1 y 2.4), con la colocación por omisión de cada uno, y SHALL conservar en el cuerpo, aunque el bloque se traslade, el título del punto y su resumen.

#### Scenario: Punto trasladable
- **WHEN** se lee el punto 5.5.1 del índice
- **THEN** indica que admite anexo y su colocación por omisión

#### Scenario: Punto no trasladable
- **WHEN** se lee el punto 4.1.1 del índice
- **THEN** no lleva la marca de bloque trasladable
