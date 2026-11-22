# Spec Delta

## Purpose

Define el archivo `project/config.json` como fuente única de verdad del proyecto (datos generales, equipo, avances y corrida vigente de cada paso) y el comportamiento de la skill `00-init` que lo crea y lo mantiene.

## ADDED Requirements

### Requirement: Ubicación y formato del config
El proyecto SHALL tener un único archivo `project/config.json`, en JSON UTF-8, con un campo entero `schema` que identifica la versión del formato, y las skills SHALL rechazar con un aviso claro un config cuyo `schema` no conozcan.

#### Scenario: Config con versión desconocida
- **WHEN** una skill lee un config con un `schema` que no soporta
- **THEN** se detiene, indica la versión encontrada y no escribe nada

### Requirement: Campos del config
El config SHALL contener `proyecto` (nombre, tema, empresa y rubro), `enfoque` (A, B o C), `resultado_esperado`, `equipo` (lista de integrantes con nombre y rol opcional), `avances` (tres entradas con número, sprint y fecha), `modo_datos` (`generado` o `real`), `diseno` (ruta al sistema de diseño) y `pasos`.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** el config contiene todos esos campos, con `avances` de longitud 3 y `pasos` vacío

### Requirement: Valor neutro de modo de datos
El campo `modo_datos` SHALL aceptar solo los valores `generado` y `real`, y ningún campo del config SHALL usar palabras como «simulado», «inventado», «falso» o «prueba» para describir los datos.

#### Scenario: Valor no permitido
- **WHEN** se escribe un `modo_datos` distinto de `generado` o `real`
- **THEN** la escritura se rechaza y se informa de los valores válidos

### Requirement: Skill 00-init
La skill `00-init` SHALL preguntar al usuario tema, empresa, rubro, enfoque, resultado esperado, integrantes del equipo y fechas de los tres avances, mostrar un resumen y pedir confirmación antes de escribir `project/config.json`.

#### Scenario: Primera ejecución
- **WHEN** el usuario ejecuta `00-init` y no existe `project/config.json`
- **THEN** la skill pregunta cada dato, presenta el resumen y escribe el config solo tras la confirmación

#### Scenario: Config ya existente
- **WHEN** el usuario ejecuta `00-init` y ya existe el config
- **THEN** la skill muestra su contenido, pregunta qué desea cambiar y no lo sobrescribe sin confirmación

### Requirement: Avances y sprints
Los tres avances del config SHALL corresponder a tres sprints (avance N = sprint N), cada uno con una fecha de entrega que puede quedar vacía hasta que el usuario la confirme.

#### Scenario: Fecha pendiente
- **WHEN** el usuario aún no conoce la fecha del avance 2
- **THEN** `00-init` guarda la fecha vacía y las skills posteriores la tratan como pendiente

### Requirement: Corrida vigente por paso
Cada entrada de `pasos` SHALL tener `run` (carpeta de la corrida vigente), `fijada` (booleano) e `historial` (lista de corridas del paso), y toda skill SHALL registrar su corrida nueva en `historial` al terminar.

#### Scenario: Corrida nueva sin fijar
- **WHEN** una skill termina una corrida y `fijada` es `false` o no existe
- **THEN** `run` pasa a ser la corrida nueva y esta se agrega a `historial`

#### Scenario: Corrida nueva con versión fijada
- **WHEN** una skill termina una corrida y `fijada` es `true`
- **THEN** la corrida se agrega a `historial`, `run` no cambia y la skill avisa que la nueva no es la vigente

### Requirement: Edición manual respetada
El usuario SHALL poder editar `project/config.json` a mano para elegir otra versión vigente, y las skills SHALL usar siempre el valor de `run` que encuentren, sin sobrescribirlo salvo por el registro de una corrida nueva sin `fijada`.

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
