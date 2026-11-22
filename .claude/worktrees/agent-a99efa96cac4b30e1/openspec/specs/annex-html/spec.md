# annex-html Specification

## Purpose
Define la conversión de los anexos del informe vigente (`13-make-annex-html`) a documentos HTML autónomos con el estándar de `common/document-html/` y el sistema de diseño del proyecto, sin corrida propia.

## Requirements

### Requirement: Anexos de la corrida vigente del informe
La skill SHALL convertir los Markdown de `anexos/` de la corrida vigente de `12-make-report` en `anexos/html/` de esa misma corrida, un HTML por cada `.md` más `index.html`, sin crear una corrida propia ni modificar ningún `.md`.

#### Scenario: Informe con anexos
- **WHEN** la corrida vigente del informe tiene `anexos/anexo-a.md` y `anexos/anexo-b.md`
- **THEN** quedan `anexos/html/anexo-a.html`, `anexos/html/anexo-b.html` e `anexos/html/index.html` en esa corrida

#### Scenario: Informe sin anexos
- **WHEN** la corrida vigente no tiene la carpeta `anexos/`
- **THEN** la skill no escribe nada e indica qué sección de origen falta para tener anexos

#### Scenario: Sin informe
- **WHEN** `12-make-report` no tiene corrida vigente
- **THEN** la skill se detiene e indica ejecutar `12-make-report`

### Requirement: HTML autónomo con el sistema de diseño
Cada HTML SHALL ser autónomo (sin recursos externos), con los tokens del `tokens.json` junto al `DESIGN.md` del config o los tokens base si no hay sistema de diseño, y SHALL coincidir con lo que se genera hoy desde su `.md`.

#### Scenario: Comprobación
- **WHEN** se comprueban los HTML después de construirlos
- **THEN** la comprobación responde sin incidencias

#### Scenario: Markdown cambiado
- **WHEN** un `.md` del anexo cambió después de construir su HTML
- **THEN** la comprobación informa que el HTML no coincide con lo que se genera desde su Markdown
