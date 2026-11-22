## Purpose
Define el plan de implementación de la app: la skill que convierte la definición de cada componente en una lista corta y ordenada de changes de OpenSpec, con trazabilidad completa hacia el PRD y datos legibles por el cascarón.

## ADDED Requirements

### Requirement: Skill de plan de implementación
El repositorio SHALL incluir la skill `23-make-app-implementation-plan` y su homóloga `23-make-app-implementation-plan-update`, registradas en `pipeline.json`, que lee la definición vigente de la app y escribe un plan de implementación por cada componente que exista en ella (`backend`, `frontend`, `database`, `openrpa`). La skill SHALL preguntar al usuario lo que falte, presentar la propuesta de changes de cada componente y esperar su confirmación antes de escribir.

#### Scenario: Componentes sin frontend
- **WHEN** la definición de la app tiene `backend`, `database` y `openrpa` y no tiene `frontend`
- **THEN** la skill genera tres planes y ninguno de frontend

#### Scenario: Propuesta confirmada
- **WHEN** la skill propone cinco changes para el backend
- **THEN** no escribe ningún archivo hasta que el usuario los acepta, rechaza o corrige

#### Scenario: Definición ausente
- **WHEN** no hay corrida vigente de la definición de la app
- **THEN** la skill se detiene e indica qué paso previo ejecutar

### Requirement: Estructura del plan por componente
Cada plan SHALL listar entre 4 y 6 changes de OpenSpec ordenados por dependencia, en cortes verticales coherentes (por ejemplo base y configuración, capa de datos, funcionalidad principal, integraciones, despliegue y CI), y cada change SHALL declarar nombre en kebab-case en inglés, objetivo, alcance, dependencias, funcionalidades del PRD, flujos del APP-FLOW y tablas del esquema que cubre, criterio de aceptación y orden.

#### Scenario: Plan completo
- **WHEN** se genera el plan del backend
- **THEN** cada change lista nombre, objetivo, alcance, dependencias, cobertura, criterio de aceptación y orden

#### Scenario: Componente muy pequeño
- **WHEN** un componente tiene una sola funcionalidad y la skill propone menos de cuatro changes
- **THEN** el plan incluye la justificación escrita y el validador la acepta

#### Scenario: Plan demasiado fragmentado
- **WHEN** la propuesta tiene siete changes para un componente
- **THEN** la skill agrupa el trabajo hasta seis y no lo presenta como válido

### Requirement: Trazabilidad con el PRD
Cada funcionalidad del PRD que corresponda a un componente SHALL estar cubierta por exactamente un change de su plan. Los flujos del APP-FLOW y las tablas del esquema que cubre cada change SHALL existir en los documentos de definición.

#### Scenario: Funcionalidad sin cubrir
- **WHEN** una funcionalidad del PRD del backend no aparece en ningún change del plan
- **THEN** la validación informa la funcionalidad y el componente

#### Scenario: Funcionalidad cubierta dos veces
- **WHEN** dos changes del mismo plan declaran cubrir la misma funcionalidad
- **THEN** la validación informa la funcionalidad y los dos changes

#### Scenario: Referencia inexistente
- **WHEN** un change cita una tabla que no está en el esquema
- **THEN** la validación informa el change y la tabla

### Requirement: Dependencias entre changes
Las dependencias de un change SHALL apuntar a changes del mismo plan que van antes en el orden, y el orden SHALL ser total y sin ciclos. Las dependencias entre componentes (por ejemplo, el backend requiere la base de datos) SHALL declararse a nivel de plan.

#### Scenario: Ciclo
- **WHEN** el change A depende de B y B depende de A
- **THEN** la validación informa el ciclo

#### Scenario: Dependencia posterior
- **WHEN** un change depende de otro que va después en el orden
- **THEN** la validación informa la dependencia

#### Scenario: Dependencia entre componentes
- **WHEN** el plan del backend requiere el esquema del plan de database
- **THEN** el plan del backend declara esa dependencia y la validación comprueba que el plan de database existe

### Requirement: Salidas del plan
La skill SHALL escribir por cada componente `implementation-plan.md`, en español, y `plan.json`, con identificadores en inglés, que contenga los changes con todos sus campos en un formato que el cascarón de la app pueda leer para crear los changes de OpenSpec en cada repo. `plan.json` y `implementation-plan.md` SHALL ser consistentes entre sí.

#### Scenario: Consistencia
- **WHEN** `plan.json` lista cinco changes y `implementation-plan.md` describe cuatro
- **THEN** la validación informa la diferencia

#### Scenario: Uso por el cascarón
- **WHEN** el cascarón lee `plan.json` de un componente
- **THEN** obtiene el nombre, objetivo, alcance, dependencias y criterio de aceptación de cada change para crear sus stubs de OpenSpec

### Requirement: Versionado, update y validación
Cada ejecución SHALL escribir una corrida nueva con fecha y hora y su `README.md`; la homóloga `-update` SHALL bifurcar la corrida vigente, aplicar solo los cambios pedidos (agregar, quitar, reagrupar o reordenar changes, o cambiar su cobertura), dejar sin cambios los archivos no afectados y volver a validar. La validación SHALL comprobar el tope de changes, la trazabilidad, las dependencias, la consistencia entre `plan.json` y el markdown y el texto limpio, e informar archivo y causa de cada incidencia.

#### Scenario: Update de un solo componente
- **WHEN** el usuario pide fusionar dos changes del frontend
- **THEN** el `-update` modifica el plan del frontend, deja idénticos los archivos de los demás componentes y vuelve a validar

#### Scenario: Corrida con incidencias
- **WHEN** la validación del fork falla
- **THEN** el fork se conserva, la corrida vigente no cambia y se informan las incidencias
