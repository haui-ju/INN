## Purpose
Define el armado del informe del proyecto por avance (versiones 1, 2 y final): el playbook y sus modelos, la skill `19-make-report` y su script, la correspondencia entre los puntos del índice y las corridas vigentes, el documento acumulado, los faltantes, las figuras, las referencias bibliográficas, los formatos de salida y la validación.

## ADDED Requirements

### Requirement: Playbook y modelos del armado
El repositorio SHALL incluir `common/report/guia.md` y `common/report/models/` con `rep-0-control-documento.md`, `rep-9-referencias.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir el orden, las marcas de avance, las versiones acumuladas, las figuras, las referencias cruzadas, los faltantes, los formatos de salida, los errores y el checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `19-make-report` va a armar la portada o las referencias
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Correspondencia entre puntos y corridas
El kit SHALL declarar en `report_map.json` el paso, los archivos y, donde aplique, el sprint que alimentan cada punto del índice, y la skill SHALL tomar cada punto de la corrida vigente de su paso, con los puntos 5.5.2 y 5.5.3 derivados de la bitácora y el anexo C y el punto A.4 sin fuente.

#### Scenario: Punto con corrida vigente
- **WHEN** el config tiene corrida de `09-make-requirements`
- **THEN** los puntos 4.2 y 4.3 se toman de `rf.md` y `rnf.md` de esa corrida

#### Scenario: Informe de un sprint
- **WHEN** se arma el avance 2
- **THEN** los puntos 6.2.x se toman de la corrida registrada para el sprint 2 en `16-make-sprint-report`

### Requirement: Prerrequisitos por avance
`pipeline.json` SHALL declarar para `19-make-report` los pasos que alimentan cada avance, y `projectcfg.py check --skill 19-make-report --avance N` SHALL avisar solo de los pasos de ese avance sin corrida, sin bloquear la ejecución.

#### Scenario: Avance 1 sin análisis final
- **WHEN** el usuario arma el avance 1 y `18-make-final-analysis` no tiene corrida
- **THEN** la comprobación no avisa de ese paso porque el avance 1 no lo incluye

### Requirement: Preguntas y confirmación antes de escribir
La skill SHALL preguntar el avance (1, 2 o final), cómo tratar los puntos sin fuente (marcador de pendiente u omitir), el formato de salida y los cambios principales de la versión, y SHALL mostrar el plan (puntos incluidos, fuente de cada uno y faltantes) y esperar confirmación antes de crear archivos.

#### Scenario: Puntos sin fuente
- **WHEN** el plan encuentra tres puntos del avance sin corrida fuente
- **THEN** la skill los lista con el paso que los produce y pregunta si se dejan con marcador o se omiten

### Requirement: Documento acumulado y estructura de salida
La skill SHALL crear cada corrida en `project/report/<DD-MM-AAAA-HH-MM-SS>/` con `informe-avance-N.md`, `anexos/`, `evidencias/`, `faltantes.md` y `README.md`, SHALL incluir todos los puntos del índice cuya primera marca sea igual o anterior al avance y ninguno posterior, y SHALL registrar la corrida en el paso `19-make-report` del config.

#### Scenario: Avance 1
- **WHEN** se arma el avance 1
- **THEN** el documento incluye los puntos marcados `[A1]` y `[A1+]` y no incluye 5.1, 6.2 ni el capítulo 7

#### Scenario: Avance 2
- **WHEN** se arma el avance 2
- **THEN** el documento incluye también los puntos `[A2]` y los `[A1+]` con su texto vigente

### Requirement: Portada y control del documento
El documento SHALL abrir con la portada y el historial de versiones, con una fila por versión hasta el avance armado, con la fecha de `avances` del config, los capítulos que cambian según el índice y los cambios principales que informó el usuario.

#### Scenario: Fecha distinta del config
- **WHEN** la fecha de la versión 2 difiere de la del avance 2 en el config
- **THEN** la validación informa la versión

### Requirement: Numeración, títulos y orden
El armado SHALL reemplazar cada encabezado numerado por el número y el título del índice con el nivel que corresponde a su profundidad, y SHALL ordenar los puntos como el índice, de modo que no haya números repetidos ni fuera de orden.

#### Scenario: Título distinto del índice
- **WHEN** el encabezado del punto 4.2 no tiene el título del índice
- **THEN** la validación informa el punto

### Requirement: Figuras y evidencias
El armado SHALL convertir las líneas de captura de los informes en imágenes con pie `Figura X: …`, copiar las evidencias a `evidencias/` y renumerar las figuras de forma consecutiva en todo el documento, y todo pie SHALL llevar un código de trazabilidad o una fecha `DD-MM-AAAA`.

#### Scenario: Pie sin código ni fecha
- **WHEN** una figura tiene un pie sin código de trazabilidad ni fecha
- **THEN** la validación informa la figura

#### Scenario: Numeración con saltos
- **WHEN** el documento tiene las figuras 1, 2 y 4
- **THEN** la validación informa el salto

### Requirement: Faltantes
`faltantes.md` SHALL listar, con el punto, el título, el paso que lo produce y qué hacer, todo punto con marca igual o anterior al avance que no tenga fuente, y SHALL coincidir con lo que el documento deja con marcador de pendiente u omite, sin listar nunca un punto que tiene contenido.

#### Scenario: Punto omitido sin registrar
- **WHEN** el punto 5.1 no está en el documento ni en `faltantes.md`
- **THEN** la validación informa el punto

#### Scenario: Punto con contenido en faltantes
- **WHEN** `faltantes.md` lista 4.2 y el documento lo tiene con contenido
- **THEN** la validación informa el punto

### Requirement: Referencias bibliográficas
`Referencias bibliográficas` SHALL compilarse de la lista cerrada de `rep-9-referencias.md`, de modo que toda cita del documento tenga su entrada y toda entrada esté citada.

#### Scenario: Cita sin entrada
- **WHEN** el texto cita Ries (2011) y las referencias no lo incluyen
- **THEN** la validación informa la cita

#### Scenario: Entrada sin cita
- **WHEN** las referencias incluyen una obra que el documento no cita
- **THEN** la validación informa la entrada

### Requirement: Referencias cruzadas y no repetición
Toda referencia a un punto o anexo SHALL apuntar a un número del índice y los enlaces SHALL resolver, y ningún párrafo de ocho o más palabras SHALL aparecer dos veces en el documento.

#### Scenario: Referencia a punto inexistente
- **WHEN** el texto dice «véase 6.9.1» y el índice no tiene ese punto
- **THEN** la validación informa la referencia

### Requirement: Formatos de salida
El Markdown SHALL ser la fuente del documento; el kit SHALL poder generar un HTML autónomo con el sistema de diseño (con aviso si usa los tokens base) cuyos encabezados coincidan con los del Markdown; las demás conversiones SHALL quedar a elección del usuario fuera de la validación y una vista privada SHALL publicarse solo con confirmación explícita.

#### Scenario: HTML con recurso externo
- **WHEN** el HTML carga una hoja de estilo o fuente externa
- **THEN** la validación informa el recurso

### Requirement: Validación del informe
La validación SHALL comprobar la estructura, los puntos presentes y ausentes, el orden, el historial de versiones, las figuras, las referencias, los faltantes, el HTML opcional, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Punto de un avance posterior
- **WHEN** el avance 1 incluye el punto 5.1
- **THEN** la validación informa que pertenece a un avance posterior

### Requirement: Sin skill de actualización
La skill `19-make-report` NO SHALL tener homóloga `-update`: se vuelve a ejecutar para cada avance, crea una corrida nueva y no modifica las anteriores.

#### Scenario: Avance 2 después del 1
- **WHEN** el usuario arma el avance 2
- **THEN** la corrida del avance 1 queda intacta y se registra la nueva

### Requirement: Texto limpio en el informe
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Marcador de pendiente
- **WHEN** un punto queda con marcador
- **THEN** el texto dice qué paso lo produce sin etiquetas de procedencia
