## MODIFIED Requirements

### Requirement: Ubicación y formato del config
El proyecto SHALL tener un único archivo `project/config.yaml`, en YAML UTF-8 con un campo entero `schema`, y las skills SHALL rechazar con un aviso claro un config cuyo `schema` no conozcan o que no sea YAML válido.

#### Scenario: Config con versión desconocida
- **WHEN** una skill lee un config con un `schema` que no soporta
- **THEN** se detiene, indica la versión encontrada y no escribe nada

#### Scenario: Config con YAML inválido
- **WHEN** una skill lee un config que no se puede interpretar
- **THEN** muestra la línea con el problema, no lo sobrescribe y pide corregirlo o ejecutar `00-init-update`

### Requirement: Campos del config
El config SHALL contener `proyecto` (nombre, tema, tipo `empresa` o `propio`, `ruc` solo si es empresa, y rubro), `enfoque` (A, B o C), `resultado_esperado`, `equipo` (nombre y rol opcional), `avances` (tres entradas con número, sprint y fecha), `modo_datos` (`generado` o `real`), `diseno` (ruta dentro de `project/` o vacío), `dominio` (ruta a `project/domain.md`) y `pasos`.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** el config contiene todos esos campos, con `avances` de longitud 3 y `pasos` vacío

### Requirement: Skill 00-init
La skill `00-init` SHALL preguntar tema, rubro, si el proyecto se aplica a una empresa (y, si sí, solo su RUC, no su nombre), enfoque, resultado esperado, integrantes y fechas de los tres avances, mostrar un resumen y pedir confirmación antes de escribir `project/config.yaml` y `project/domain.md`.

#### Scenario: Primera ejecución
- **WHEN** el usuario ejecuta `00-init` y no existe `project/config.yaml`
- **THEN** la skill pregunta cada dato, presenta el resumen y escribe el config y `domain.md` solo tras la confirmación

#### Scenario: Config ya existente
- **WHEN** el usuario ejecuta `00-init` y ya existe el config
- **THEN** la skill propone usar `00-init-update`, muestra su contenido y no lo sobrescribe sin confirmación

### Requirement: Edición manual respetada
El usuario SHALL poder editar `project/config.yaml` a mano para elegir otra versión vigente, y las skills SHALL usar siempre el valor de `run` que encuentren, sin sobrescribirlo salvo por el registro de una corrida nueva sin `fijada`.

#### Scenario: Versión elegida a mano
- **WHEN** el usuario cambia `run` a una corrida anterior y pone `fijada` en `true`
- **THEN** las skills posteriores leen esa corrida como base

## ADDED Requirements

### Requirement: Comentarios explicativos del config
Cada campo de `project/config.yaml` SHALL llevar a su derecha un comentario breve que diga qué significa, qué valor tiene y qué otras opciones existen, y toda escritura de las skills SHALL conservar esos comentarios.

#### Scenario: Campo enfoque
- **WHEN** el usuario abre el config
- **THEN** junto a `enfoque: B` ve que B significa dueño u operario del negocio y que A es el comprador final y C ambos

#### Scenario: Registro de una corrida
- **WHEN** una skill registra una corrida en `pasos`
- **THEN** el archivo conserva los comentarios de todos los campos

### Requirement: Tipo de proyecto y RUC
`proyecto.tipo` SHALL valer `empresa` o `propio`. Con `empresa`, el config SHALL guardar el `ruc` (11 dígitos) y no el nombre de la empresa; con `propio`, el `ruc` SHALL quedar vacío y el proyecto se trata como una solución propia o innovadora sin empresa.

#### Scenario: Proyecto aplicado a una empresa
- **WHEN** el usuario indica que el proyecto es para una empresa
- **THEN** la skill pide solo el RUC y rechaza un valor que no tenga 11 dígitos

#### Scenario: Proyecto propio
- **WHEN** el usuario indica que no hay empresa
- **THEN** `tipo` es `propio`, `ruc` queda vacío y las skills posteriores no asumen una empresa

### Requirement: Archivo domain.md
`project/domain.md` SHALL reunir lo conocido del dominio: datos generales, reseña, misión, visión, valores, objetivos y contexto. Con empresa se busca por el RUC; con proyecto propio describe la solución. Todo dato sin fuente se plantea a partir del contexto y se marca a su lado «(modelado por el agente, por no contar con X)».

#### Scenario: Datos encontrados por el RUC
- **WHEN** la búsqueda por RUC devuelve datos de la empresa
- **THEN** la skill los muestra con su fuente, pide confirmación y los escribe en `domain.md`

#### Scenario: Dato no encontrado
- **WHEN** no hay misión publicada para la empresa
- **THEN** la skill plantea una a partir del rubro y el tema y la marca «(modelado por el agente, por no contar con misión publicada)»

### Requirement: Skill 00-init-update
La skill `00-init-update` SHALL cambiar datos de `project/config.yaml` y `project/domain.md` ya creados: preguntar qué cambiar, mostrar los cambios, pedir confirmación antes de escribir, conservar los comentarios y validar el resultado.

#### Scenario: Cambio de fecha de un avance
- **WHEN** el usuario pide cambiar la fecha del avance 2
- **THEN** la skill muestra el cambio, espera confirmación, actualiza solo ese campo y valida el config

#### Scenario: Cambio de RUC o de tipo de proyecto
- **WHEN** el usuario cambia el RUC o pasa de `empresa` a `propio`
- **THEN** la skill propone rehacer `domain.md` y no lo reemplaza sin confirmación

### Requirement: Sistema de diseño dentro de project
El sistema de diseño SHALL vivir dentro de `project/` (`project/design-system/<corrida>/DESIGN.md`) y `diseno` SHALL apuntar a la versión vigente, que la skill de diseño actualiza al terminar.

#### Scenario: Diseño creado
- **WHEN** la skill de diseño termina una corrida
- **THEN** `diseno` apunta al `DESIGN.md` de esa corrida salvo que el paso esté fijado
