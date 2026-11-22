## Purpose
Define los informes de avance por sprint (puntos 6.1, 6.2 y 6.3 del informe) y el acta de Sprint Review y retrospectiva (anexo A.3): las skills que los generan y los ajustan, la trazabilidad de sus cifras con la bitácora, el plan y los tableros, la regla de no repetir contenido entre avances y su validación.

## ADDED Requirements

### Requirement: Fuentes y prerrequisitos del informe
La skill SHALL leer la corrida vigente de la bitácora, la del plan de sprints, la de los tableros HTML (`data.json`), la de ceremonias, la configuración de Scrum, el config y el informe del sprint anterior si existe; si falta la bitácora o no tiene entradas del sprint pedido SHALL avisarlo y ofrecer `15-make-implementation-log`, y si el corte del tablero no cae en ese sprint SHALL ofrecer `13-design-html-boards-update`, sin bloquear.

#### Scenario: Bitácora sin el sprint
- **WHEN** la bitácora vigente no tiene entradas del sprint 2
- **THEN** la skill lo avisa, ofrece agregarlas con `15-make-implementation-log-update` y, si el usuario continúa, el informe marcará lo que no pueda comprobar

### Requirement: Una corrida por sprint
La skill SHALL pedir el número de sprint, generar un informe por sprint (avance N igual al sprint N) en `project/sprint-report/<DD-MM-AAAA-HH-MM-SS>/` con `informe-avance-N.md`, `acta-review-retro.md`, `data.json` (copia del tablero vigente) y `README.md`, y registrar la corrida en el paso `16-make-sprint-report` del config con el sprint indicado.

#### Scenario: Tercer avance
- **WHEN** el usuario genera el informe del sprint 3
- **THEN** el config guarda su corrida en la entrada del sprint 3 sin cambiar las de los sprints 1 y 2

### Requirement: Preguntas y confirmación antes de escribir
La skill SHALL preguntar lo mostrado y comentado en la Sprint Review, las decisiones, lo que fue bien y lo que se debe mejorar, las acciones con responsable y las evidencias que se pegan; SHALL proponer el resto desde la bitácora y los tableros, usar solo lo que el usuario aporta cuando `modo_datos` es `real`, y mostrar el informe completo y esperar confirmación antes de crear archivos.

#### Scenario: Sin comentarios en la Review
- **WHEN** el usuario no recibió comentarios
- **THEN** el informe lo dice con esas palabras y no se agregan comentarios

### Requirement: Informe de avance
`informe-avance-N.md` SHALL tener los nueve puntos `## 6.N.1.` a `## 6.N.9.` del índice (resumen, Gantt actualizado, incremento, Kanban, Sprint Review, retrospectiva, pruebas, riesgos y cambios y plan del siguiente avance), cada uno con su parte `**Pegar.**` (archivo de evidencia o «Sin captura») o `**Texto.**` según el índice.

#### Scenario: Punto ausente
- **WHEN** falta el punto 6.2.7
- **THEN** la validación informa el punto

### Requirement: Cifras trazables
Los puntos 6.N.2 y 6.N.4 SHALL llevar una línea `**Cifras.**` con la fecha de corte y los indicadores del `data.json` de la corrida, copia del tablero vigente con un corte dentro del sprint (avance global y del sprint, tareas hechas y atrasadas; WIP, tiempo de ciclo y rendimiento), e iguales a los que calcula el kit.

#### Scenario: Corte fuera del sprint
- **WHEN** el corte de `data.json` es posterior al fin del sprint del informe
- **THEN** la validación informa la fecha y el sprint

#### Scenario: Avance distinto del tablero
- **WHEN** el informe dice 70 % y el tablero vigente calcula 62 %
- **THEN** la validación informa la cifra y el valor del tablero

### Requirement: Incremento, pruebas y riesgos
El punto 6.N.3 SHALL llevar cada captura con el pie «Figura X: HU-XX nombre (REQ-XX)», con historias existentes y los `REQ` de su origen; el 6.N.7 SHALL dar «N de M pruebas pasaron» igual al de los resultados del sprint en la bitácora; el 6.N.8 SHALL citar los `RIE` del sprint; el 6.N.9 SHALL citar las tareas del siguiente sprint según el plan y las de sprints anteriores sin terminar (en el avance 3, solo las pendientes).

#### Scenario: Pie de foto con historia inexistente
- **WHEN** una figura cita `HU-09` y las historias vigentes no la definen
- **THEN** la validación informa el código

#### Scenario: Pruebas que no coinciden
- **WHEN** el informe dice 8 de 10 pruebas pasaron y la bitácora registra 7 de 10 para ese sprint
- **THEN** la validación informa ambas cifras

### Requirement: Acta de Review y retrospectiva
`acta-review-retro.md` SHALL tener `## Sprint Review` (fecha dentro del sprint, participantes del equipo del config, historias mostradas, comentarios y decisiones) y `## Sprint Retrospective` con las tablas «Qué fue bien», «Qué mejorar» y «Acciones» (acción, responsable del equipo y sprint de aplicación), y los puntos 6.N.5 y 6.N.6 SHALL resumirla sin copiarla.

#### Scenario: Responsable ajeno al equipo
- **WHEN** una acción asigna a una persona que no está en el equipo del config
- **THEN** la validación informa la acción

### Requirement: Sin repetición entre avances
El informe SHALL NOT repetir un párrafo de ocho o más palabras del informe del avance anterior; el contenido ya presentado se remite por número de punto y lo extenso va a los anexos.

#### Scenario: Párrafo copiado
- **WHEN** el informe del avance 2 reproduce un párrafo del avance 1
- **THEN** la validación informa el punto y el avance de origen

### Requirement: Validación del informe
La validación SHALL comprobar la estructura, las cifras contra los tableros, la bitácora y el plan vigentes, los códigos citados, las evidencias, las citas permitidas (Schwaber y Sutherland 2020 y Anderson 2010, máximo dos por archivo), los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Evidencia inexistente
- **WHEN** un punto pega un archivo que no existe en las evidencias de la bitácora vigente
- **THEN** la validación informa el archivo

### Requirement: Skill 16-make-sprint-report-update
La skill `16-make-sprint-report-update` SHALL tomar la corrida base del sprint indicado (o la que indique el usuario), bifurcarla, pedir los cambios (cifras, evidencias, Review, retrospectiva, riesgos o plan del siguiente avance), resincronizar las cifras con los tableros vigentes si el usuario lo pide, mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Tablero actualizado
- **WHEN** el usuario actualizó el tablero HTML y pide resincronizar el avance 1
- **THEN** la copia actualiza las líneas «Cifras» y los textos que las citan, y deja el resto idéntico a la base

#### Scenario: Informe posterior afectado
- **WHEN** el cambio altera una cifra que un informe posterior cita por número de punto
- **THEN** la skill lo avisa en el plan y no modifica ese informe

### Requirement: Texto limpio en los informes
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Retrospectiva
- **WHEN** se redacta lo que fue bien y lo que se debe mejorar
- **THEN** se usa el lenguaje del proyecto sin etiquetas de procedencia
