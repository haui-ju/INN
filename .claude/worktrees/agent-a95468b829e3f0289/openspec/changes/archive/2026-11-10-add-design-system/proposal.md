# Proposal

## Why

Los tableros HTML (Gantt y Kanban), el informe y cualquier pantalla del proyecto necesitan una identidad visual única. Sin ella, cada HTML se diseña por separado y se ve distinto. Hace falta un sistema de diseño **del proyecto** (minimalista, moderno y profesional), definido una sola vez, con tokens que las demás skills lean, y que se pueda ajustar sin rehacerlo. El campo `diseno` del config ya existe y apunta a un `DESIGN.md` dentro de `project/`, pero ninguna skill lo crea todavía.

## What Changes

- **Nueva skill `01-design-system`** (verbo `design`): propone un sistema de diseño según el tono, las referencias y las preferencias del usuario, lo confirma y escribe `project/design-system/<corrida>/` con `DESIGN.md`, `tokens.json`, `preview.html` y `README.md`. Al terminar registra la corrida y actualiza `diseno` del config.
- **Nueva skill `01-design-system-update`**: cambia un color, una tipografía, un token o un componente de una corrida existente (copia `-fork`), propaga el cambio a los archivos que dependen de él y valida.
- **Nuevo playbook `common/design-system/`**: `guia.md` (principios, tokens, accesibilidad, claro y oscuro, componentes, reglas del HTML autónomo, errores frecuentes, checklist) y `models/` con plantillas por entregable, en el mismo formato que las de Design Thinking.
- **`tokens.json` como fuente única** de los valores; `DESIGN.md` los documenta y `preview.html` los muestra, y las demás skills leen `tokens.json`.
- **Validación propia del paso:** contraste AA de los pares texto/fondo en claro y oscuro, tokens completos y referenciados, texto limpio. Requiere un gancho en `validate_run.py` para reglas por paso que no sean de códigos de trazabilidad.
- **Valores por defecto de estilo:** neutros fríos, un solo acento sobrio, bordes redondeados moderados, sombras suaves y espaciado amplio; el usuario los ajusta al preguntar.

## Capabilities

### New Capabilities
- `design-system`: playbook y modelos del sistema de diseño, skills `01-design-system` y `01-design-system-update`, estructura de salida, tokens, accesibilidad, componentes, vista previa autónoma y validación.

### Modified Capabilities
- Ninguna. El requisito «Sistema de diseño dentro de project» de `project-config` ya cubre la ubicación y la actualización de `diseno`.

## Impact

- **Archivos nuevos:** `common/design-system/guia.md` y `models/`, `.claude/skills/01-design-system/` (con `scripts/` y `references/`), `.claude/skills/01-design-system-update/`, `.claude/skills/_shared/rules/design_system.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (gancho de reglas por paso) y sus pruebas.
- **Consumidores posteriores:** `13-design-html-boards` (cambio 10) y `19-make-report` (cambio 14) leen `diseno` y `tokens.json`.
- **Fuera de alcance:** aplicar el diseño a tableros o informe, crear pantallas del sistema (cambio 11), publicar o explorar en Claude Design (opcional y posterior), ejecutar la skill.
- **Supuestos registrados:** el diseño es solo local (decidido por el usuario); las fuentes del `preview.html` usan pila del sistema para ser autónomo; la paleta por defecto es un punto de partida que el usuario confirma o cambia.
