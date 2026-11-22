# Proposal

## Why

Definida la app (PRD, TRD, APP-FLOW, esquema), falta convertirla en trabajo construible. Cada repo (backend, frontend, base de datos, OpenRPA) tendrá su propio `openspec/`, y necesita sus changes listos y en el orden correcto. Sin un plan, el cascarón arranca vacío, o se generan decenas de changes pequeños e inmanejables. El plan debe agrupar el trabajo en pocos changes verticales por repo y garantizar que ninguna funcionalidad del PRD quede sin construir.

## What Changes

- Nueva skill `23-make-app-implementation-plan` con su `-update`, que lee los documentos de definición de cada componente y escribe un plan de implementación por componente: la lista ordenada de changes de OpenSpec que construyen ese repo.
- **Tope de 4 a 6 changes por componente**, nunca decenas: cortes verticales ordenados por dependencia (base y configuración, capa de datos, funcionalidad principal, integraciones, despliegue y CI).
- Cada change del plan lleva nombre en kebab-case en inglés, objetivo, alcance, dependencias, qué funcionalidades del PRD, flujos del APP-FLOW y tablas del esquema cubre, criterio de aceptación y orden.
- **Trazabilidad:** cada funcionalidad del PRD queda cubierta por exactamente un change del plan; el validador falla si queda alguna sin cubrir, si una se cubre dos veces, si hay más de seis changes o menos de cuatro (salvo un componente muy pequeño justificado) o si una dependencia no existe o forma un ciclo.
- Cada componente produce `implementation-plan.md` (legible, en español) y `plan.json` (datos que la skill de cascarón usa para crear los stubs de changes de OpenSpec dentro de cada repo).
- Solo se generan planes para los componentes que existen en la definición (si no hay frontend, no hay plan de frontend).
- Playbook propio `common/app-plan/guia.md` con modelos, validador en `_shared/rules`, entrada en `pipeline.json` y pruebas. Los identificadores y el código van en inglés; los textos para el usuario y los README, en español.

## Capabilities

### New Capabilities

- `app-implementation-plan`: la skill de plan de implementación de la app y su `-update`: entradas, estructura del plan por componente, tope de changes, trazabilidad con el PRD, `plan.json`, versionado y validación.

### Modified Capabilities

Ninguna. La secuencia de pasos de `skill-pipeline` se amplía en el change que agrega los primeros pasos de la app (`add-app-definition-skills`); este change solo registra su propio paso en `pipeline.json`.

## Impact

- Archivos nuevos: `.claude/skills/23-make-app-implementation-plan/` y su `-update`, `common/app-plan/` (guía y modelos), `_shared/rules/app_plan.py`, esquema de `plan.json`, pruebas en `_shared/tests/`.
- Cambios menores: `_shared/pipeline.json` (nuevo paso con prerrequisito en la definición de la app).
- Depende de la definición de la app (change `add-app-definition-skills`) y alimenta al cascarón (`add-app-scaffold-skill`).
- Sin dependencias externas nuevas.
