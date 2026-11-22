## Purpose
Define el sistema de diseño del proyecto: el playbook con sus modelos, las skills que lo crean y lo ajustan, los tokens como fuente única, las reglas de accesibilidad y la vista previa autónoma que consumen los tableros HTML y el informe.

## ADDED Requirements

### Requirement: Playbook y modelos del sistema de diseño
El repositorio SHALL incluir `common/design-system/guia.md` (principios, tokens, accesibilidad, tema claro y oscuro, componentes, reglas del HTML autónomo, errores frecuentes y checklist) y `common/design-system/models/` con una plantilla por entregable y un `README.md`, con la estructura de las plantillas de Design Thinking: ficha, instrucciones para el agente, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `01-design-system` va a escribir un entregable
- **THEN** lee antes la guía y la plantilla del entregable y respeta su formato

#### Scenario: Plantilla sin ejemplo
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Recogida de preferencias de diseño
La skill `01-design-system` SHALL leer el config, preguntar solo lo que no conste (tono, dos o tres referencias visuales, colores y tipografías que ya use el proyecto, si quiere modo oscuro) y proponer valores por defecto minimalistas, modernos y profesionales para que el usuario los acepte o cambie.

#### Scenario: Usuario sin preferencias
- **WHEN** el usuario no tiene colores ni referencias
- **THEN** la skill propone una paleta, una tipografía y un tono coherentes con el rubro y el tipo de proyecto

#### Scenario: Usuario con colores definidos
- **WHEN** el usuario aporta un color de marca
- **THEN** la skill lo usa como acento y deriva el resto de la paleta

### Requirement: Plan y confirmación antes de escribir
La skill SHALL presentar un resumen del sistema propuesto (paleta clara y oscura, tipografía, escala de espacio y radio, componentes incluidos) y esperar la confirmación del usuario antes de crear archivos, ajustando la propuesta hasta que la confirme.

#### Scenario: Propuesta rechazada
- **WHEN** el usuario pide otro acento de color
- **THEN** la skill actualiza la propuesta, la muestra de nuevo y no escribe nada hasta la confirmación

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/design-system/<DD-MM-AAAA-HH-MM-SS>/` con `DESIGN.md`, `tokens.json`, `preview.html` y `README.md`, SHALL registrarla en el paso `01-design-system` del config y SHALL actualizar `diseno` para que apunte al `DESIGN.md` de esa corrida, salvo que el paso esté fijado.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma la propuesta
- **THEN** la corrida contiene los cuatro archivos y el config apunta a su `DESIGN.md`

#### Scenario: Paso fijado
- **WHEN** el paso `01-design-system` está fijado y se crea otra corrida
- **THEN** la corrida se agrega al historial, `diseno` no cambia y la skill lo avisa

### Requirement: Tokens como fuente única
`tokens.json` SHALL contener los tokens de color (paleta clara y oscura con nombres semánticos), tipografía, espacio, radio y sombra, y SHALL ser la única fuente de valores: `DESIGN.md` y `preview.html` SHALL coincidir con él, y las demás skills SHALL leer los valores de `tokens.json`.

#### Scenario: Skill consumidora
- **WHEN** una skill de HTML necesita el color de acento
- **THEN** lo lee de `tokens.json` de la corrida a la que apunta `diseno`

#### Scenario: Archivos desalineados
- **WHEN** `preview.html` usa un valor distinto del de `tokens.json`
- **THEN** la validación lo informa

### Requirement: Accesibilidad de color
Los pares de texto y fondo declarados en `tokens.json` SHALL cumplir contraste WCAG AA (al menos 4,5:1 para texto normal y 3:1 para texto grande y elementos de interfaz), tanto en el tema claro como en el oscuro.

#### Scenario: Par con poco contraste
- **WHEN** el texto secundario sobre el fondo tiene 3,2:1
- **THEN** la validación informa el par, la razón calculada y el mínimo exigido

### Requirement: Componentes mínimos
`DESIGN.md` SHALL especificar como mínimo encabezado, tarjeta, tabla, etiqueta de estado, barra de progreso y botón, cada uno con sus estados, tokens usados y una regla de uso, y `preview.html` SHALL mostrarlos.

#### Scenario: Componente sin estados
- **WHEN** un componente no declara estados
- **THEN** la validación lo informa

### Requirement: Vista previa autónoma
`preview.html` SHALL ser un único archivo que funciona sin conexión y sin recursos externos, usa los tokens como variables, alterna entre tema claro y oscuro y se adapta a pantalla de teléfono sin desplazamiento horizontal.

#### Scenario: Recurso externo
- **WHEN** `preview.html` carga un script, hoja de estilos o fuente desde una dirección externa
- **THEN** la validación lo informa

### Requirement: Validación del sistema de diseño
La validación SHALL comprobar que `tokens.json` es completo (claro y oscuro con las mismas claves), que `DESIGN.md` y `preview.html` solo usan tokens existentes, el contraste AA, los enlaces y el texto limpio, y SHALL informar cada incidencia con archivo y causa.

#### Scenario: Token inexistente
- **WHEN** `DESIGN.md` cita `color.acento-fuerte` y no existe
- **THEN** la validación informa el archivo y el token

### Requirement: Skill 01-design-system-update
La skill `01-design-system-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (color, tipografía, token o componente), editar solo los archivos afectados, volver a validar y registrar el resultado.

#### Scenario: Cambio de color de acento
- **WHEN** el usuario cambia el acento
- **THEN** la copia actualiza `tokens.json`, la tabla de `DESIGN.md` y las variables de `preview.html`, comprueba el contraste y deja el resto idéntico a la base

#### Scenario: Cambio que rompe el contraste
- **WHEN** el nuevo color no cumple AA
- **THEN** la skill lo informa, propone un ajuste y conserva el fork sin mover la corrida vigente mientras haya incidencias

### Requirement: Texto limpio en el sistema de diseño
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Ejemplo en DESIGN.md
- **WHEN** `DESIGN.md` muestra un ejemplo de tabla
- **THEN** usa contenido realista del proyecto sin etiquetas de procedencia
