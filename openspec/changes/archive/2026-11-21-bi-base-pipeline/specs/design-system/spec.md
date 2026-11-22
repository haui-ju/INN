# Spec Delta

## MODIFIED Requirements

### Requirement: Playbook y modelos del sistema de diseño
El repositorio SHALL incluir `common/02-design-system/guia.md` (principios, tokens, accesibilidad, tema claro y oscuro, componentes, reglas del HTML autónomo, errores frecuentes y checklist) y `common/02-design-system/models/` con una plantilla por entregable y un `README.md`, cada plantilla con ficha, instrucciones para el agente, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `02-design-system` va a escribir un entregable
- **THEN** lee antes la guía y la plantilla del entregable y respeta su formato

#### Scenario: Plantilla sin ejemplo
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/02-design-system/<DD-MM-AAAA-HH-MM-SS>/` con `DESIGN.md`, `tokens.json`, `preview.html` y `README.md`, SHALL registrarla en el paso `02-design-system` del config y SHALL actualizar `diseno` para que apunte al `DESIGN.md` de esa corrida, salvo que el paso esté fijado.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma la propuesta
- **THEN** la corrida contiene los cuatro archivos y el config apunta a su `DESIGN.md`

#### Scenario: Paso fijado
- **WHEN** el paso `02-design-system` está fijado y se crea otra corrida
- **THEN** la corrida se agrega al historial, `diseno` no cambia y la skill lo avisa

### Requirement: Skill 01-design-system-update
La skill `02-design-system-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (color, tipografía, token o componente), editar solo los archivos afectados, volver a validar y registrar el resultado.

#### Scenario: Cambio de color de acento
- **WHEN** el usuario cambia el acento
- **THEN** la copia actualiza `tokens.json`, la tabla de `DESIGN.md` y las variables de `preview.html`, comprueba el contraste y deja el resto idéntico a la base

#### Scenario: Cambio que rompe el contraste
- **WHEN** el nuevo color no cumple AA
- **THEN** la skill lo informa, propone un ajuste y conserva el fork sin mover la corrida vigente mientras haya incidencias
