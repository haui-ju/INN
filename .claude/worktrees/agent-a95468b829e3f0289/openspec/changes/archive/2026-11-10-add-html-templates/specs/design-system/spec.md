## ADDED Requirements

### Requirement: Tema base estilo Claude
El sistema de diseño base SHALL tener acento naranja para rellenos con texto oscuro y un rol `acento-fuerte` para texto y enlaces, neutros cálidos, titulares en serif, texto en sans y códigos en monoespaciada, tema claro por defecto y oscuro opcional, con todos los pares de texto en AA, y su `tokens-base.json`, la guía, la plantilla de tokens y la vista previa SHALL reflejarlo.

#### Scenario: Texto de acento sobre fondo
- **WHEN** se valida el contraste de `acento-fuerte` sobre `fondo` y `superficie` en claro y oscuro
- **THEN** cumple el mínimo de 4,5 : 1

#### Scenario: Relleno de acento
- **WHEN** se valida `acento-texto` sobre `acento`
- **THEN** cumple el mínimo de 4,5 : 1

### Requirement: Reglas visuales de la biblioteca HTML
El repositorio SHALL documentar en `common/html/DESIGN.md` las reglas visuales de las plantillas (color, tipografía, espacio, forma, componentes, movimiento y accesibilidad) coherentes con los tokens base, y las plantillas SHALL cumplirlas.

#### Scenario: Plantilla nueva
- **WHEN** se agrega una plantilla a `common/html/`
- **THEN** reutiliza los componentes y respeta las reglas de `DESIGN.md`
