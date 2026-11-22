# Design

## Context

Las skills del repo siguen un patrón: paso numerado en `pipeline.json`, playbook en `common/<tema>/guia.md` con `models/`, corridas versionadas con `runs.py`, registro con `projectcfg.py`, validación en `_shared/rules/` y homóloga `-update` que bifurca la corrida (specs `skill-pipeline` y `run-versioning`). La definición de la app (PRD, TRD, APP-FLOW, esquema, por componente) la produce el change hermano `add-app-definition-skills`, que aún no tiene artefactos; este diseño supone que cada componente expone esos documentos con códigos estables para sus funcionalidades, flujos y tablas. Motivación en proposal.md.

## Goals / Non-Goals

**Goals:**
- Plan corto (4 a 6 changes) y ordenado por componente, trazable al PRD.
- Datos legibles por máquina para que el cascarón cree los changes de OpenSpec dentro de cada repo.

**Non-Goals:**
- No crea changes de OpenSpec ni repos: eso lo hace el cascarón.
- No escribe proposals, specs, diseños ni tareas de cada change.
- No decide el stack (lo decide el TRD).

## Decisions

**1. Cortes verticales con plantilla de agrupación, no un change por funcionalidad.** El playbook propone una secuencia base por tipo de componente (backend: base y configuración, datos, funcionalidad principal, integraciones, despliegue y CI; frontend: base y sistema de diseño, navegación, pantallas por flujo, integración con el backend, despliegue; database: esquema y migraciones, semillas, acceso y respaldos; openrpa: entorno y configuración, flujo principal, validación y registro, programación). Las funcionalidades del PRD se agrupan en esos cortes. *Alternativa descartada:* un change por funcionalidad; con 15 a 20 funcionalidades produce decenas de changes.

**2. Tope fijo 4 a 6 con excepción justificada.** El validador exige entre 4 y 6; menos solo si el plan trae una justificación escrita. Es una constante del kit. *Alternativa:* tope configurable por proyecto; se descarta para no reabrir el problema de los 20 changes.

**3. Una funcionalidad, un solo change.** El validador exige cobertura exacta (ni huecos ni duplicados). Si una funcionalidad atraviesa varios cortes, se parte en el PRD, no en el plan.

**4. `plan.json` como contrato con el cascarón.** Campos por change: `name`, `goal`, `scope`, `depends_on`, `covers` (`features`, `flows`, `tables`), `acceptance`, `order`; y a nivel de plan: `component`, `cross_component_deps`, `justification` (opcional). Los nombres de campos y de changes van en inglés; el markdown legible, en español.

**5. Ubicación y versionado.** Las corridas siguen `run-versioning`: `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con carpeta `app/implementation-plan`, y dentro un subdirectorio por componente con `implementation-plan.md` y `plan.json`. Se aparta de la ruta `project/app/definition/<component>/implementation-plan.md` pedida originalmente para respetar el versionado y no mezclar documentos de definición editables con salidas generadas; la definición apunta al plan vigente desde su README. Es una decisión a confirmar con el usuario.

**6. Orden y dependencias.** Entre componentes, el orden por defecto es database, backend, openrpa, frontend, declarado como dependencia a nivel de plan y comprobado por el validador (que el componente requerido exista). Dentro del plan, las dependencias solo apuntan hacia atrás.

## Risks / Trade-offs

- [El change `add-app-definition-skills` aún no fija los códigos de funcionalidad y flujo] → La skill fija solo el formato que consume y se ajusta cuando ese change defina sus códigos; el validador referencia los códigos por patrón declarado en el playbook.
- [Cuatro a seis changes grandes pueden ser difíciles de implementar de una vez] → Cada change incluye su criterio de aceptación y el cascarón puede dividirlo después, sin romper la trazabilidad.
- [Una funcionalidad que no cabe en ningún corte base] → El playbook permite un corte extra dentro del tope y la skill pide al usuario aprobarlo.
- [La secuencia de la skill depende del número 23, que supone que el change hermano usa 21 y 22] → El número se asigna al implementar y se ajusta en `pipeline.json` según el orden real de los changes.
- [La secuencia fija de pasos en `skill-pipeline` queda desactualizada] → La actualiza el primer change que agregue pasos de la app; este solo agrega su entrada en `pipeline.json`.

## Open Questions

- Confirmar con el usuario la ubicación de las corridas (decisión 5) frente a `project/app/definition/<component>/implementation-plan.md`; no cambia las specs ni las tareas, solo la ruta de salida.
