# Proposal

## Why

El paquete de Design Thinking describe las pantallas (`PAN-XX`) solo con texto: nombre, qué muestra y qué `REQ` cubre. Para entender y revisar el prototipo hace falta verlo. Además, la skill `make-design-thinking` fija el número de pantallas (6 en la fase 4) sin dejar que el usuario lo decida por fase.

## What Changes

- **Nueva skill `make-design-thinking-prototypes`** (nombre y contenido en inglés), hermana de `make-design-thinking`:
  - Pregunta sobre cuál corrida de `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` crear los mockups.
  - Lee de esa corrida las pantallas (`PAN`), los escenarios (`FLU`), los requerimientos (`REQ`) y los hallazgos de prueba (`HAL-T`).
  - Presenta un plan con la cantidad de pantallas y espera confirmación antes de dibujar.
  - Dibuja **wireframes básicos en Miro**, en un tablero por corrida con dos secciones: «v1» (fase 4) y «v2 antes/después» (fase 5, solo las pantallas que cambian por hallazgos de severidad 2 o más).
  - Guarda el **enlace al tablero** en la corrida: `bloques/fase-4-prototipar/miro.md` (enlace y relación `PAN` → frame) y lo referencia desde `pantallas.md`, `escenarios.md`, `documento.md` (3.1.5.3) y `anexos.md` (D.3).
  - Si la corrida no tiene fase 4, se detiene y deriva a `make-design-thinking` para generar solo esa fase.
- **Ajuste de `make-design-thinking`:** en el paso del plan, pregunta cuántas pantallas quiere el usuario en cada fase que tenga pantallas (fase 4 v1; fase 5 v2) y adapta `pantallas.md`, `escenarios.md`, `documento.md` y `anexos.md` a esas cantidades. Defaults: 4 a 6 en fase 4 (mínimo una por `REQ` y una de error o estado vacío) y solo las que cambien en fase 5.
- **Coherencia de herramienta:** el texto generado hoy dice «Figma, fidelidad media/alta». La skill nueva reemplaza esa referencia por la herramienta realmente usada (Miro, fidelidad baja o media) o conserva Figma si el usuario lo elige.
- **Plugin de Miro:** ya instalado (`miro@claude-plugins-official`, alcance de usuario). Falta autenticación OAuth, que hace el usuario.
- Contexto ya aplicado fuera de este cambio: renombre de `make-designthinking` a `make-design-thinking` y traslado de las plantillas a `common/design-thinking/models/`.

## Capabilities

### New Capabilities
- `design-thinking-prototype-mockups`: generación de wireframes básicos en Miro a partir de una corrida existente (selección de corrida, plan con cantidad de pantallas, tablero por corrida, enlace registrado en los documentos, manejo de corridas sin fase 4).
- `design-thinking-package-generation`: generación del paquete de Design Thinking por fases (plan con cantidades editables por fase, incluidas las pantallas de fase 4 y fase 5; selección de fases; continuación de corridas existentes; texto limpio y `README.md` de procedencia). Hoy está implementada en la skill pero no existe una spec que la describa.

### Modified Capabilities
<!-- Ninguna: el proyecto aún no tiene specs en openspec/specs/. -->

## Impact

- **Archivos nuevos:** `.claude/skills/make-design-thinking-prototypes/` (SKILL.md y recursos propios a su mismo nivel).
- **Archivos modificados:** `.claude/skills/make-design-thinking/SKILL.md` y su generador de referencia (`scripts/reference/`), para el conteo de pantallas por fase y la mención de herramienta.
- **Dependencias:** cuenta de Miro con acceso al plugin y autenticación OAuth del usuario. Sin ella la skill no puede dibujar.
- **Riesgos y puntos a verificar antes de fijar el diseño:**
  - Comprobar con una prueba corta (1 o 2 pantallas) que `canvas_create_from_svg` dibuja wireframes legibles y editables.
  - Comprobar si `prototype_create` (pantallas HTML) da un prototipo con clics; de ello depende que Miro sirva también para las pruebas de la fase 5 o que el prototipo navegable siga en Figma.
  - El costo en tokens de dibujar cada pantalla no está medido; se registrará en la prueba corta.
- **Fuera de alcance:** tableros de Miro para las fases 1 a 3 (mapa de empatía, journey map, ideación, `FLO-01`), integración con Figma, y regenerar el paquete ya creado (`10-11-2026-00-00-46`).
