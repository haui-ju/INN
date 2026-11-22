# project-config Specification

## Purpose
Define el archivo `project/config.yaml` (con comentarios por campo) como fuente única de verdad del proyecto (datos generales, tipo de proyecto, equipo, calendario de entrega, secciones del informe y corrida vigente de cada paso), el archivo `project/domain.md` con los datos de la empresa o de la solución, y el comportamiento de las skills `00-init` y `00-init-update` que los crean y los mantienen.

## Requirements

### Requirement: Ubicación y formato del config
El proyecto SHALL tener un único archivo `project/config.yaml`, en YAML UTF-8 con un campo entero `schema`, y las skills SHALL rechazar con un aviso claro un config cuyo `schema` no conozcan o que no sea YAML válido.

#### Scenario: Config con versión desconocida
- **WHEN** una skill lee un config con un `schema` que no soporta
- **THEN** se detiene, indica la versión encontrada y no escribe nada

#### Scenario: Config con YAML inválido
- **WHEN** una skill lee un config que no se puede interpretar
- **THEN** muestra la línea con el problema, no lo sobrescribe y pide corregirlo o ejecutar `00-init-update`

### Requirement: Valor neutro de modo de datos
El campo `modo_datos` SHALL aceptar solo los valores `generado` y `real`, y ningún campo del config SHALL usar palabras como «simulado», «inventado», «falso» o «prueba» para describir los datos.

#### Scenario: Valor no permitido
- **WHEN** se escribe un `modo_datos` distinto de `generado` o `real`
- **THEN** la escritura se rechaza y se informa de los valores válidos

### Requirement: Skill 00-init
La skill `00-init` SHALL preguntar nombre, rubro, si el proyecto se aplica a una empresa (y, si sí, solo su RUC, no su nombre), integrantes y modo de datos, mostrar un resumen y pedir confirmación antes de escribir `project/config.yaml`; no SHALL preguntar tema ni fechas ni crear `domain.md`, y SHALL sugerir `01-make-project-brief`.

#### Scenario: Primera ejecución
- **WHEN** el usuario ejecuta `00-init` y no existe `project/config.yaml`
- **THEN** la skill pregunta cada dato técnico, presenta el resumen, escribe el config solo tras la confirmación y sugiere `01-make-project-brief`

#### Scenario: Config ya existente
- **WHEN** el usuario ejecuta `00-init` y ya existe el config
- **THEN** la skill propone usar `00-init-update`, muestra su contenido y no lo sobrescribe sin confirmación

### Requirement: Corrida vigente por paso
Cada entrada de `pasos` SHALL tener `run` (carpeta de la corrida vigente), `fijada` (booleano) e `historial` (lista de corridas del paso), y toda skill SHALL registrar su corrida nueva en `historial` al terminar.

#### Scenario: Corrida nueva sin fijar
- **WHEN** una skill termina una corrida y `fijada` es `false` o no existe
- **THEN** `run` pasa a ser la corrida nueva y esta se agrega a `historial`

#### Scenario: Corrida nueva con versión fijada
- **WHEN** una skill termina una corrida y `fijada` es `true`
- **THEN** la corrida se agrega a `historial`, `run` no cambia y la skill avisa que la nueva no es la vigente

### Requirement: Edición manual respetada
El usuario SHALL poder editar `project/config.yaml` a mano para elegir otra versión vigente, y las skills SHALL usar siempre el valor de `run` que encuentren, sin sobrescribirlo salvo por el registro de una corrida nueva sin `fijada`.

#### Scenario: Versión elegida a mano
- **WHEN** el usuario cambia `run` a una corrida anterior y pone `fijada` en `true`
- **THEN** las skills posteriores leen esa corrida como base

### Requirement: Corrida vigente inexistente
Si la carpeta indicada en `run` no existe, la skill SHALL avisarlo, mostrar las corridas disponibles del paso y pedir al usuario cuál usar, sin continuar con datos ausentes.

#### Scenario: Carpeta borrada
- **WHEN** el config apunta a una carpeta que ya no existe
- **THEN** la skill lo informa y pregunta cuál corrida usar

### Requirement: Sin secretos en el config
El config SHALL NOT almacenar contraseñas, tokens ni credenciales; solo datos del proyecto y rutas o enlaces.

#### Scenario: Herramienta que pide credenciales
- **WHEN** una skill necesita guardar el acceso a una herramienta externa
- **THEN** guarda como máximo el enlace público y nunca la credencial

### Requirement: Tipo de proyecto y RUC
`proyecto.tipo` SHALL valer `empresa` o `propio`. Con `empresa`, el config SHALL guardar el `ruc` (11 dígitos) y no el nombre de la empresa; con `propio`, el `ruc` SHALL quedar vacío y el proyecto se trata como una solución propia o innovadora sin empresa.

#### Scenario: Proyecto aplicado a una empresa
- **WHEN** el usuario indica que el proyecto es para una empresa
- **THEN** la skill pide solo el RUC y rechaza un valor que no tenga 11 dígitos

#### Scenario: Proyecto propio
- **WHEN** el usuario indica que no hay empresa
- **THEN** `tipo` es `propio`, `ruc` queda vacío y las skills posteriores no asumen una empresa

### Requirement: Archivo domain.md
`project/domain.md` SHALL reunir lo conocido del dominio: datos generales, reseña, misión, visión, valores, objetivos y contexto, y SHALL crearlo `01-make-project-brief` después de definir el tema. Con empresa se busca por el RUC; con proyecto propio describe la solución. Todo dato sin fuente se marca «(modelado por el agente, por no contar con X)».

#### Scenario: Datos encontrados por el RUC
- **WHEN** la búsqueda por RUC devuelve datos de la empresa
- **THEN** la skill los muestra con su fuente, pide confirmación y los escribe en `domain.md`

#### Scenario: Dato no encontrado
- **WHEN** no hay misión publicada para la empresa
- **THEN** la skill plantea una a partir del rubro y el tema del brief y la marca «(modelado por el agente, por no contar con misión publicada)»

#### Scenario: Config sin domain.md
- **WHEN** se ejecuta una skill y no existe `domain.md`
- **THEN** el kit avisa que falta y remite a `01-make-project-brief`

### Requirement: Sistema de diseño dentro de project
El sistema de diseño SHALL vivir dentro de `project/` (`project/02-design-system/<corrida>/DESIGN.md`) y `diseno` SHALL apuntar a la versión vigente, que la skill de diseño actualiza al terminar.

#### Scenario: Diseño creado
- **WHEN** la skill de diseño termina una corrida
- **THEN** `diseno` apunta al `DESIGN.md` de esa corrida salvo que el paso esté fijado

### Requirement: Calendario único de entrega
El config SHALL guardar `calendario` con una fecha de inicio y una fecha de entrega en `DD-MM-AAAA`, que pueden quedar vacías hasta que el usuario las confirme en `01-make-project-brief`, con entrega posterior o igual al inicio.

#### Scenario: Fecha pendiente
- **WHEN** el usuario aún no conoce la fecha de entrega
- **THEN** el config la guarda vacía y las skills posteriores la tratan como pendiente

#### Scenario: Entrega anterior al inicio
- **WHEN** se escribe una entrega anterior al inicio
- **THEN** la escritura se rechaza e informa las dos fechas

### Requirement: Roles del equipo
Cada integrante de `equipo` SHALL poder llevar un rol opcional de texto libre, y la función del kit que asigna roles SHALL aceptar solo integrantes que ya existan en el equipo y rechazar un reparto que nombre a una persona ausente.

#### Scenario: Reparto válido
- **WHEN** se asignan roles a integrantes del equipo
- **THEN** el config guarda el rol de cada uno y conserva sus comentarios

#### Scenario: Persona ausente
- **WHEN** se intenta asignar un rol a alguien que no está en el equipo
- **THEN** la escritura se rechaza, el config no cambia y se informa la causa

### Requirement: Campos del config de BI
El config SHALL contener `proyecto` (nombre, tema, tipo `empresa` o `propio`, `ruc` solo si es empresa, y rubro), `equipo` (nombre y rol opcional), `calendario` (inicio y fecha de entrega), `modo_datos`, `diseno`, `dominio`, `informe` y `pasos`; el tema y las fechas SHALL ser copia del brief.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** el config contiene todos esos campos, con `calendario` vacío, `informe.secciones` pendientes y `pasos` vacío

#### Scenario: Integrante sin rol
- **WHEN** se escribe un integrante sin rol
- **THEN** la escritura se acepta y el rol queda vacío

### Requirement: Comentarios por campo del config
Cada campo de `project/config.yaml` SHALL llevar a su derecha un comentario breve que diga qué significa, qué valor tiene y qué otras opciones existen, y toda escritura de las skills SHALL conservar esos comentarios.

#### Scenario: Campo modo_datos
- **WHEN** el usuario abre el config
- **THEN** junto a `modo_datos: generado` ve que significa datos generados para el proyecto y que `real` indica datos abiertos o autorizados

#### Scenario: Registro de una corrida
- **WHEN** una skill registra una corrida en `pasos`
- **THEN** el archivo conserva los comentarios de todos los campos

### Requirement: Cambios del config con 00-init-update
La skill `00-init-update` SHALL cambiar los datos técnicos de `project/config.yaml` (nombre, rubro, tipo, RUC, equipo y modo de datos): preguntar qué cambiar, mostrar los cambios, pedir confirmación antes de escribir, conservar los comentarios y validar; ante un cambio de tema o de fechas SHALL remitir a `01-make-project-brief-update`.

#### Scenario: Cambio de equipo
- **WHEN** el usuario agrega un integrante
- **THEN** la skill muestra el cambio, espera confirmación, actualiza solo el equipo y valida el config

#### Scenario: Cambio de la fecha de entrega
- **WHEN** el usuario pide cambiar la fecha de entrega
- **THEN** la skill indica que las fechas se definen en el brief y remite a `01-make-project-brief-update`

#### Scenario: Cambio de RUC o de tipo de proyecto
- **WHEN** el usuario cambia el RUC o pasa de `empresa` a `propio`
- **THEN** la skill actualiza el config y remite a `01-make-project-brief-update` para rehacer `domain.md`
