# Spec Delta

## Purpose

Describe el comportamiento de la skill `make-design-thinking` al generar el paquete de Design Thinking de un proyecto: recogida de datos, plan con cantidades editables por fase (incluidas las pantallas), generación por fases y reglas sobre el texto y los datos.

## ADDED Requirements

### Requirement: Recogida de información
La skill SHALL recoger el tema del proyecto, el enfoque (A, B o C), el resultado esperado, el contexto, si existen datos reales y el alcance por fases antes de proponer el plan, sin repetir lo que el usuario ya indicó.

#### Scenario: Información incompleta
- **WHEN** el usuario invoca la skill sin indicar el enfoque
- **THEN** la skill pregunta el enfoque y no lo asume

### Requirement: Plan y confirmación antes de escribir
La skill SHALL presentar un resumen y una tabla con la cantidad de formularios por fase y el total de archivos, y SHALL esperar confirmación del usuario antes de crear archivos.

#### Scenario: Plan sin confirmar
- **WHEN** el usuario aún no confirma el plan
- **THEN** la skill no crea carpetas ni archivos

### Requirement: Cantidades editables por fase
La skill SHALL permitir al usuario agregar, quitar o cambiar la cantidad de formularios de cada fase y SHALL validar cada cantidad contra el rango del playbook, avisando cuando quede fuera.

#### Scenario: Cantidad fuera de rango
- **WHEN** el usuario pide 12 entrevistas y el rango del playbook es de 5 a 8
- **THEN** la skill avisa el rango y, si el usuario mantiene su elección, la registra en las limitaciones del documento

### Requirement: Cantidad de pantallas por fase
La skill SHALL preguntar cuántas pantallas quiere el usuario en cada fase que las incluye (fase 4 para la versión v1 y fase 5 para las pantallas v2 modificadas) y SHALL ajustar a esas cantidades el inventario de pantallas, los escenarios, el documento y los anexos.

#### Scenario: El usuario define cantidades distintas por fase
- **WHEN** el usuario pide 3 pantallas en la fase 4 y 2 en la fase 5
- **THEN** el paquete generado contiene 3 pantallas `PAN` en la fase 4 y 2 pantallas v2 en la fase 5, y el documento y los anexos reflejan esos números

#### Scenario: El usuario no indica cantidades
- **WHEN** el usuario acepta los valores propuestos
- **THEN** la skill usa de 4 a 6 pantallas en la fase 4 (al menos una por `REQ` y una de error o estado vacío) y solo las pantallas que cambian por hallazgos en la fase 5

### Requirement: Selección y continuación de fases
La skill SHALL generar todas las fases por defecto, SHALL permitir generar solo algunas y SHALL escribir una fase N mayor que 1 únicamente cuando exista una corrida con las fases anteriores o cuando el usuario acepte generarlas.

#### Scenario: Solo la fase 2 con corrida previa
- **WHEN** el usuario pide solo la fase 2 y existe una corrida con la fase 1
- **THEN** la skill pregunta cuál corrida continuar, escribe dentro de ella y actualiza solo las secciones de esa fase

#### Scenario: Solo la fase 2 sin corrida previa
- **WHEN** el usuario pide solo la fase 2 y no hay corridas con la fase 1
- **THEN** la skill informa que faltan los insumos y ofrece generar también las fases anteriores

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` con `README.md`, `documento.md`, `anexos.md` y una carpeta `bloques/` con una subcarpeta por fase generada.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma un plan para todas las fases
- **THEN** la corrida contiene `README.md`, `documento.md`, `anexos.md` y las subcarpetas `fase-0` a `fase-5` dentro de `bloques/`

### Requirement: Fidelidad a las plantillas y al índice
La skill SHALL usar el formato de las plantillas de `common/design-thinking/models/` para cada formulario y SHALL seguir los puntos 3.1.x de `common/structure/model1.md` en `documento.md` y los Anexos B, D, E y F en `anexos.md`.

#### Scenario: Formulario de observación
- **WHEN** se genera una hoja de observación
- **THEN** conserva los campos de la plantilla `dt-1b-hoja-observacion.md`

### Requirement: Datos y texto limpio
La skill SHALL usar literalmente los datos reales que aporte el usuario; cuando no los haya, SHALL generar datos coherentes entre fases y SHALL NOT incluir avisos de simulación en `documento.md`, `anexos.md` ni `bloques/`, dejando la procedencia solo en `README.md`.

#### Scenario: Sin datos reales
- **WHEN** el usuario no aporta datos
- **THEN** el paquete contiene datos coherentes y `README.md` es el único archivo que indica que se trata de una simulación didáctica

#### Scenario: Con datos reales
- **WHEN** el usuario aporta una ruta con entrevistas reales
- **THEN** la skill las usa sin modificarlas y no genera datos sobre ellas

### Requirement: Trazabilidad y coherencia
La skill SHALL asignar códigos de evidencia según el playbook y SHALL mantener consistentes las cifras, fracciones y referencias entre fases, documento y anexos.

#### Scenario: Cifra repetida en dos fases
- **WHEN** una cifra de la fase 1 se cita en la fase 2
- **THEN** ambas coinciden y la fase 2 cita el código de evidencia de origen

### Requirement: Citas bibliográficas
La skill SHALL citar como máximo 1 o 2 fuentes por fase y solo las listadas en la sección de referencias del playbook.

#### Scenario: Fase con citas
- **WHEN** se redacta una fase que cita fuentes
- **THEN** el texto tiene como máximo dos citas y cada una figura en las referencias del playbook
