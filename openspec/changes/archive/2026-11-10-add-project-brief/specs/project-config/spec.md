## MODIFIED Requirements

### Requirement: Campos del config
El config SHALL contener `proyecto` (nombre, tema, tipo `empresa` o `propio`, `ruc` solo si es empresa, y rubro), `enfoque` (A, B o C), `resultado_esperado`, `equipo` (nombre y rol opcional, que si existe es `Product Owner`, `Scrum Master` o `Equipo de desarrollo`), `avances` (tres entradas con número, sprint, inicio y fecha de entrega), `modo_datos`, `diseno`, `dominio` y `pasos`; tema, enfoque, resultado y fechas SHALL ser copia del brief.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** el config contiene todos esos campos, con `avances` de longitud 3, el núcleo con valores neutros y `pasos` vacío

#### Scenario: Rol no permitido
- **WHEN** se escribe un rol distinto de los tres de Scrum
- **THEN** la escritura se rechaza y se informa de los valores válidos

### Requirement: Skill 00-init
La skill `00-init` SHALL preguntar nombre, rubro, si el proyecto se aplica a una empresa (y, si sí, solo su RUC, no su nombre), integrantes y modo de datos, mostrar un resumen y pedir confirmación antes de escribir `project/config.yaml`; no SHALL preguntar tema, enfoque, resultado ni fechas ni crear `domain.md`, y SHALL sugerir `00b-make-project-brief`.

#### Scenario: Primera ejecución
- **WHEN** el usuario ejecuta `00-init` y no existe `project/config.yaml`
- **THEN** la skill pregunta cada dato técnico, presenta el resumen, escribe el config solo tras la confirmación y sugiere `00b-make-project-brief`

#### Scenario: Config ya existente
- **WHEN** el usuario ejecuta `00-init` y ya existe el config
- **THEN** la skill propone usar `00-init-update`, muestra su contenido y no lo sobrescribe sin confirmación

### Requirement: Avances y sprints
Los tres avances del config SHALL corresponder a tres sprints (avance N = sprint N), cada uno con un inicio y una fecha de entrega que pueden quedar vacíos hasta que el usuario los confirme en `00b-make-project-brief`.

#### Scenario: Fecha pendiente
- **WHEN** el usuario aún no conoce la fecha del avance 2
- **THEN** el config la guarda vacía y las skills posteriores la tratan como pendiente

### Requirement: Archivo domain.md
`project/domain.md` SHALL reunir lo conocido del dominio: datos generales, reseña, misión, visión, valores, objetivos y contexto, y SHALL crearlo `00b-make-project-brief` después de definir el tema. Con empresa se busca por el RUC; con proyecto propio describe la solución. Todo dato sin fuente se marca «(modelado por el agente, por no contar con X)».

#### Scenario: Datos encontrados por el RUC
- **WHEN** la búsqueda por RUC devuelve datos de la empresa
- **THEN** la skill los muestra con su fuente, pide confirmación y los escribe en `domain.md`

#### Scenario: Dato no encontrado
- **WHEN** no hay misión publicada para la empresa
- **THEN** la skill plantea una a partir del rubro y el tema del brief y la marca «(modelado por el agente, por no contar con misión publicada)»

#### Scenario: Config sin domain.md
- **WHEN** se ejecuta una skill y no existe `domain.md`
- **THEN** el kit avisa que falta y remite a `00b-make-project-brief`

### Requirement: Skill 00-init-update
La skill `00-init-update` SHALL cambiar los datos técnicos de `project/config.yaml` (nombre, rubro, tipo, RUC, equipo y modo de datos): preguntar qué cambiar, mostrar los cambios, pedir confirmación antes de escribir, conservar los comentarios y validar; ante un cambio de tema, enfoque, resultado o fechas SHALL remitir a `00b-make-project-brief-update`.

#### Scenario: Cambio de equipo
- **WHEN** el usuario agrega un integrante
- **THEN** la skill muestra el cambio, espera confirmación, actualiza solo el equipo y valida el config

#### Scenario: Cambio de fecha de un avance
- **WHEN** el usuario pide cambiar la fecha del avance 2
- **THEN** la skill indica que las fechas se definen en el brief y remite a `00b-make-project-brief-update`

#### Scenario: Cambio de RUC o de tipo de proyecto
- **WHEN** el usuario cambia el RUC o pasa de `empresa` a `propio`
- **THEN** la skill actualiza el config y remite a `00b-make-project-brief-update` para rehacer `domain.md`
