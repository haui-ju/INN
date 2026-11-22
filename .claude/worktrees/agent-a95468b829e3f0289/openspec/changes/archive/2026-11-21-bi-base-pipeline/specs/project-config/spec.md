# Spec Delta

## MODIFIED Requirements

### Requirement: Skill 00-init
La skill `00-init` SHALL preguntar nombre, rubro, si el proyecto se aplica a una empresa (y, si sí, solo su RUC, no su nombre), integrantes y modo de datos, mostrar un resumen y pedir confirmación antes de escribir `project/config.yaml`; no SHALL preguntar tema ni fechas ni crear `domain.md`, y SHALL sugerir `01-make-project-brief`.

#### Scenario: Primera ejecución
- **WHEN** el usuario ejecuta `00-init` y no existe `project/config.yaml`
- **THEN** la skill pregunta cada dato técnico, presenta el resumen, escribe el config solo tras la confirmación y sugiere `01-make-project-brief`

#### Scenario: Config ya existente
- **WHEN** el usuario ejecuta `00-init` y ya existe el config
- **THEN** la skill propone usar `00-init-update`, muestra su contenido y no lo sobrescribe sin confirmación

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

## REMOVED Requirements

### Requirement: Avances y sprints
**Reason**: El proyecto tiene una sola entrega; ya no hay tres avances ni sprints.
**Migration**: Usar el calendario único (`calendario`) definido en el requisito «Calendario único de entrega».

### Requirement: Roles Scrum del equipo
**Reason**: Scrum se retira del pipeline; los roles ya no son los de Product Owner, Scrum Master y desarrollo.
**Migration**: Usar el rol opcional de texto libre de cada integrante, definido en «Roles del equipo».

### Requirement: Campos del config
**Reason**: Se reemplaza por «Campos del config de BI» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Campos del config de BI».

### Requirement: Comentarios explicativos del config
**Reason**: Se reemplaza por «Comentarios por campo del config» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Comentarios por campo del config».

### Requirement: Skill 00-init-update
**Reason**: Se reemplaza por «Cambios del config con 00-init-update» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Cambios del config con 00-init-update».

## ADDED Requirements

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
