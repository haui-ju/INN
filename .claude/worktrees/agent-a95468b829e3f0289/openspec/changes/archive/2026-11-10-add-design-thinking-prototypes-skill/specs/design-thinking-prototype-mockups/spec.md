# Spec Delta

## Purpose

Define cómo la skill `make-design-thinking-prototypes` genera wireframes básicos en Miro a partir de una corrida existente del paquete de Design Thinking y deja el enlace al tablero registrado en los documentos de esa corrida.

## ADDED Requirements

### Requirement: Selección de la corrida
La skill SHALL preguntar sobre cuál corrida de `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` crear los mockups, mostrando las corridas disponibles ordenadas de la más reciente a la más antigua.

#### Scenario: Existen varias corridas
- **WHEN** el usuario invoca la skill y hay dos o más corridas en `project/design-thinking/`
- **THEN** la skill lista las corridas con su fecha y hora y espera que el usuario elija una

#### Scenario: No existe ninguna corrida
- **WHEN** el usuario invoca la skill y `project/design-thinking/` no contiene corridas
- **THEN** la skill informa que no hay corridas, deriva a `make-design-thinking` y no crea tableros ni archivos

### Requirement: Insumos de la corrida
La skill SHALL leer de la corrida elegida las pantallas (`PAN`), los escenarios (`FLU`), los requerimientos (`REQ`) y, si existen, los hallazgos de prueba (`HAL-T`) antes de proponer el plan.

#### Scenario: La corrida no tiene fase 4
- **WHEN** la corrida elegida no contiene el inventario de pantallas de la fase 4
- **THEN** la skill se detiene, explica que faltan las pantallas y deriva a `make-design-thinking` para generar solo la fase 4, sin dibujar nada

#### Scenario: La corrida no tiene fase 5
- **WHEN** la corrida contiene la fase 4 pero no el reporte de la fase 5
- **THEN** la skill propone solo la sección v1 y omite la sección v2

### Requirement: Plan y confirmación antes de dibujar
La skill SHALL presentar un plan con el nombre del tablero, la cantidad de pantallas v1, las pantallas v2 afectadas y el total de frames, y SHALL esperar confirmación del usuario antes de crear el tablero.

#### Scenario: El usuario ajusta la cantidad
- **WHEN** el usuario pide más o menos pantallas que las propuestas
- **THEN** la skill actualiza el plan, vuelve a mostrarlo y solo dibuja tras una nueva confirmación

#### Scenario: Sin confirmación
- **WHEN** el usuario no confirma el plan
- **THEN** la skill no crea el tablero ni modifica archivos de la corrida

### Requirement: Cantidad de pantallas v1
La skill SHALL proponer entre 4 y 6 pantallas para la fase 4, con al menos una pantalla por cada `REQ` (unificando `REQ` que comparten pantalla) y al menos una pantalla de error o estado vacío.

#### Scenario: Cantidad dentro del rango
- **WHEN** la corrida tiene 5 `REQ` y una pantalla de error definida
- **THEN** la skill propone entre 4 y 6 pantallas que cubren todos los `REQ`

#### Scenario: El usuario pide una cantidad fuera del rango
- **WHEN** el usuario pide más de 6 o menos de 4 pantallas
- **THEN** la skill avisa en una línea el motivo del rango y respeta la decisión del usuario si la mantiene

### Requirement: Pantallas v2 por hallazgos
La skill SHALL dibujar en la sección v2 un módulo por cada pantalla cambiada por hallazgos `HAL-T` de severidad 2 o mayor, con la versión nueva de la pantalla; el estado anterior permanece en el módulo v1 con el mismo código.

#### Scenario: Hallazgo de severidad baja
- **WHEN** un hallazgo tiene severidad 1 y no se aplicó ningún cambio
- **THEN** la skill no dibuja ningún módulo v2 por ese hallazgo

#### Scenario: Hallazgo que modifica una pantalla
- **WHEN** un hallazgo de severidad 3 propone un cambio sobre `PAN-05`
- **THEN** la sección v2 contiene el módulo de `PAN-05` con el cambio señalado y el código del hallazgo citado

### Requirement: Tablero único por corrida
La skill SHALL crear un solo tablero de Miro por corrida, con una sección v1 y una sección v2, y SHALL NOT duplicar tableros por omisión.

#### Scenario: Tablero creado
- **WHEN** el usuario confirma el plan
- **THEN** el tablero contiene un módulo por cada pantalla del plan, agrupados en las secciones v1 y v2

### Requirement: Composición de cada pantalla
La skill SHALL dibujar cada pantalla como un módulo dentro de un frame con título `PAN-XX · nombre`, un subtítulo de una línea, la interfaz dentro de un marco de aplicación, llamadas numeradas sobre los elementos clave y un panel de referencias.

#### Scenario: Módulo completo
- **WHEN** se dibuja la pantalla `PAN-04`
- **THEN** su frame contiene título, subtítulo, interfaz, al menos una llamada numerada y un panel con una entrada por cada llamada

#### Scenario: Numeración coherente
- **WHEN** se termina un módulo
- **THEN** cada número de la interfaz tiene exactamente una entrada con ese número en el panel de referencias, y viceversa

### Requirement: Contenido de las referencias
Cada entrada del panel de referencias SHALL tener un título corto, una explicación de una o dos líneas y los códigos de trazabilidad (`REQ`, `FLU` y, cuando apliquen, `PP` o `HAL-T`) tomados de la corrida.

#### Scenario: Entrada trazable
- **WHEN** una llamada señala la venta con un toque
- **THEN** su entrada cita el `REQ` y el `FLU` que la corrida asigna a esa pantalla

### Requirement: Marco de aplicación consistente
La interfaz de todas las pantallas SHALL compartir el mismo marco (barra superior y navegación inferior con la sección activa resaltada) y los mismos componentes, para que se lean como una sola aplicación.

#### Scenario: Navegación activa
- **WHEN** se dibujan `PAN-01` y `PAN-04`
- **THEN** ambas muestran la misma navegación inferior con una sección distinta resaltada

### Requirement: Flujo entre pantallas
La skill SHALL ordenar los módulos siguiendo el flujo de los escenarios de la corrida y SHALL conectar pantallas consecutivas con flechas etiquetadas con la acción del usuario; el flujo propuesto forma parte del plan y el usuario puede corregirlo.

#### Scenario: Flujo propuesto
- **WHEN** el escenario `FLU-01` recorre Inicio, Ingreso, Ficha, Venta y Consulta
- **THEN** los módulos aparecen en ese orden con una flecha etiquetada entre cada par consecutivo

#### Scenario: El usuario corrige una transición
- **WHEN** el usuario cambia el destino o la etiqueta de una flecha
- **THEN** la skill actualiza el plan y pide una nueva confirmación antes de dibujar

### Requirement: Estado de cada cambio en la sección v2
En la sección v2 la skill SHALL marcar cada llamada como «Existente» o «Cambia», SHALL citar el hallazgo `HAL-T` que origina cada cambio y SHALL indicar en una línea cómo era antes.

#### Scenario: Cambio por hallazgo
- **WHEN** una llamada señala un elemento modificado por `HAL-T-02`
- **THEN** su entrada se marca «Cambia», cita `HAL-T-02` y describe el estado anterior

### Requirement: Densidad y proporciones de la interfaz
La skill SHALL dibujar la interfaz con proporciones de aplicación móvil moderna: controles de entre 32 y 44 px de alto, espaciado de la escala 8, 12 y 16 px, padding interno en los componentes y contenido útil que ocupe al menos el 70% del área disponible de la pantalla.

#### Scenario: Pantalla con poco contenido
- **WHEN** la descripción de una pantalla deja menos del 70% del área de contenido ocupada
- **THEN** la skill no dibuja el módulo y pide enriquecer la pantalla con contenido relevante de la corrida

#### Scenario: Controles proporcionados
- **WHEN** se dibuja una pantalla con botones y campos
- **THEN** ningún botón ni campo supera los 44 px de alto y el texto queda separado de los bordes por un padding de al menos 12 px

### Requirement: Marco de dispositivo
La interfaz SHALL incluir una barra de estado, una barra superior con título y una navegación inferior con iconos y etiquetas, idénticas en estructura en todas las pantallas.

#### Scenario: Estructura común
- **WHEN** se comparan dos pantallas del mismo tablero
- **THEN** ambas tienen la misma barra de estado, barra superior y navegación inferior, con distinta sección activa

### Requirement: Estilo wireframe
La skill SHALL dibujar con neutros de la paleta de Miro, una sola fuente y una única familia de acento (azul) para llamadas, etiquetas «Cambia» y el panel de referencias, sin sombras ni degradados ni colores de marca.

#### Scenario: Acento único
- **WHEN** se revisa un tablero terminado
- **THEN** los colores usados pertenecen a los neutros de la paleta y a la familia azul

### Requirement: Registro del enlace y de la correspondencia
La skill SHALL escribir `bloques/fase-4-prototipar/miro.md` con la URL del tablero y la correspondencia entre cada `PAN` y su frame, y SHALL referenciar esa URL en `pantallas.md`, `escenarios.md`, `documento.md` (punto 3.1.5.3) y `anexos.md` (D.3).

#### Scenario: Enlace visible desde los documentos
- **WHEN** termina el dibujo
- **THEN** los cuatro documentos citados contienen el enlace al tablero y `miro.md` lista cada `PAN` con su frame

### Requirement: Coherencia de la herramienta declarada
La skill SHALL reemplazar en los documentos de la corrida la declaración de herramienta y fidelidad por la realmente usada (Miro, fidelidad baja o media) o conservar la declaración original cuando el usuario indique que el prototipo navegable sigue en otra herramienta.

#### Scenario: Se usa Miro
- **WHEN** el usuario confirma el uso de Miro como herramienta de mockups
- **THEN** los documentos que mencionaban otra herramienta pasan a indicar Miro y la fidelidad correspondiente

### Requirement: Texto limpio
La skill SHALL NOT añadir avisos de procedencia o de simulación en los documentos de la corrida ni en el tablero, y SHALL NOT modificar `README.md`.

#### Scenario: Revisión del texto
- **WHEN** la skill termina de escribir los archivos
- **THEN** ninguno de ellos contiene etiquetas como «simulado», «ilustrativo» o «ejemplo» añadidas por la skill

### Requirement: Disponibilidad de Miro
La skill SHALL comprobar que las herramientas de Miro están disponibles y autenticadas antes de crear el tablero, y SHALL detenerse con instrucciones de autenticación si no lo están, sin escribir archivos parciales.

#### Scenario: Miro no autenticado
- **WHEN** la comprobación de identidad de Miro falla
- **THEN** la skill indica cómo autenticar el plugin y no crea tablero ni archivos

### Requirement: Corrida que ya tiene un tablero
La skill SHALL detectar si la corrida ya contiene `miro.md` y preguntar si se actualiza el tablero existente o se crea uno nuevo, sin duplicar tableros por omisión.

#### Scenario: Segunda ejecución
- **WHEN** la corrida elegida ya contiene `miro.md`
- **THEN** la skill pregunta si actualizar el tablero existente o crear uno nuevo y actúa según la respuesta
