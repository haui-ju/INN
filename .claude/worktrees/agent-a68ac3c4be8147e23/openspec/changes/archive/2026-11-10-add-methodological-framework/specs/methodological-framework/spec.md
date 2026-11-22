## Purpose
Define el capítulo 2 del informe (marco metodológico): su playbook y modelos, las skills que lo generan y lo ajustan, la estructura de cada metodología, la integración entre ellas, el glosario ampliable, las citas de lista cerrada y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos del marco metodológico
El repositorio SHALL incluir `common/methodological-framework/guia.md` (qué cubre cada metodología, criterio de elección, integración, glosario, errores frecuentes, checklist y lista cerrada de referencias verificadas) y `common/methodological-framework/models/` con `mar-1-innovacion.md`, `mar-2-agiles.md`, `mar-3-integracion.md`, `mar-4-glosario.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `04-make-methodological-framework` va a escribir una sección
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Metodologías aplicadas y profundidad
La skill SHALL proponer las metodologías que el proyecto aplica a partir de `pipeline.json` (por defecto Design Thinking, Lean Startup, Lean Change Management, Scrum y Kanban), preguntar la profundidad (resumen o detallado) y los términos del negocio para el glosario, y esperar la confirmación del usuario antes de escribir.

#### Scenario: Metodología quitada
- **WHEN** el usuario indica que no usa Kanban
- **THEN** la skill lo quita del capítulo, de la integración y del glosario y muestra el plan actualizado

### Requirement: Estructura de cada metodología
Cada metodología SHALL ir en una subsección sin numerar de 2.1 (innovación) o 2.2 (ágiles) con las etiquetas «Qué es», «Principios», «Cuándo se usa» y «En este proyecto», más las propias: Design Thinking «Fases»; Lean Startup y Lean Change «Ciclo»; Scrum «Roles», «Eventos» y «Artefactos»; Kanban «Prácticas» y «Métricas».

#### Scenario: Etiqueta ausente
- **WHEN** la subsección de Scrum no tiene «Eventos»
- **THEN** la validación informa la metodología y la etiqueta

### Requirement: Integración de las metodologías
El punto 2.3 SHALL incluir el flujo entre las metodologías aplicadas y una tabla `Metodología | Recibe | Produce | Dónde en el informe`, en el orden del flujo, cuyas metodologías SHALL coincidir con las de 2.1 y 2.2 y cuyos puntos del informe SHALL existir en `common/structure/model1.md`.

#### Scenario: Punto inexistente
- **WHEN** la tabla remite al punto 7.9
- **THEN** la validación informa que no existe en el índice

#### Scenario: Metodología sin fila
- **WHEN** Scrum figura en 2.2 y no en la tabla de 2.3
- **THEN** la validación lo informa

### Requirement: Glosario con términos obligatorios
El glosario SHALL tener los términos obligatorios de cada metodología aplicada (definidos en el playbook), ordenados alfabéticamente y sin repetir, cada uno con definición, origen (una metodología, «Negocio» o «Proyecto») y los puntos del informe donde se usa, y SHALL ser idéntico en `glosario.md` y en 2.4 de `capitulo-2.md`.

#### Scenario: Término obligatorio ausente
- **WHEN** el glosario no define «Sprint» y Scrum está aplicado
- **THEN** la validación informa el término faltante

#### Scenario: Glosario desalineado
- **WHEN** `glosario.md` difiere de la sección 2.4
- **THEN** la validación lo informa

### Requirement: Términos del negocio
La skill SHALL proponer de tres a seis términos del negocio o del proyecto tomados del config, de `project/domain.md` y del Lean Canvas vigente, y SHALL pedir confirmación; con `tipo: propio` SHALL NOT presuponer una empresa.

#### Scenario: Proyecto propio
- **WHEN** el config indica `tipo: propio`
- **THEN** los términos de origen «Negocio» describen el problema y no una empresa

### Requirement: Citas de lista cerrada
El capítulo SHALL citar como máximo dos fuentes por metodología y dos en cada uno de los puntos 2.3 y 2.4, solo de la lista cerrada del playbook, y `referencias.md` SHALL contener la entrada completa de cada fuente citada y ninguna que no se cite.

#### Scenario: Fuente fuera de la lista
- **WHEN** el capítulo cita un autor que no está en el playbook
- **THEN** la validación informa el punto y la cita

#### Scenario: Más de dos citas
- **WHEN** la subsección de Scrum cita tres fuentes distintas
- **THEN** la validación informa la metodología

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/methodological-framework/<DD-MM-AAAA-HH-MM-SS>/` con `capitulo-2.md` (puntos 2.1 a 2.4), `glosario.md`, `referencias.md` y `README.md`, y SHALL registrarla en el paso `04-make-methodological-framework` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene los cuatro archivos y el config la registra

### Requirement: Validación del marco metodológico
La validación SHALL comprobar las secciones 2.1 a 2.4, la estructura de cada metodología, la integración, el glosario, las citas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Sección ausente
- **WHEN** falta el punto 2.3
- **THEN** la validación informa el archivo y la sección

### Requirement: Skill 04-make-methodological-framework-update
La skill `04-make-methodological-framework-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (términos, metodologías aplicadas, texto de una metodología o ampliación del glosario), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Ampliar el glosario
- **WHEN** el usuario pide añadir términos de capítulos posteriores
- **THEN** la skill propone candidatos desde las corridas vigentes, espera la confirmación y actualiza `glosario.md` y 2.4 manteniendo el orden alfabético

#### Scenario: Cambio de metodologías
- **WHEN** el usuario quita una metodología aplicada
- **THEN** la copia actualiza su subsección, la tabla y el flujo de 2.3, el glosario y `referencias.md`, y deja el resto idéntico a la base

### Requirement: Texto limpio en el marco metodológico
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Ejemplo de aplicación
- **WHEN** «En este proyecto» describe cómo se aplica la metodología
- **THEN** usa el contenido real del proyecto sin etiquetas de procedencia
