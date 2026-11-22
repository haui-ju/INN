# Design

## Context

Estado observado: no existen `common/scrum/` ni `common/requirements/`; `pipeline.json` define `08-make-scrum-setup` (requiere `00-init` y `05`) y `09-make-requirements` (requiere `05` y `08`), ambas con `update`. El config tiene `equipo[].rol` opcional sin validación de valores; `00-init` deja el rol en `null` y `00-init-update` remite a `08-make-scrum-setup`. `avances` trae tres fechas (sprint N = avance N). El Design Thinking define los `REQ` (en `matriz-priorizacion.md`, con alcance 3.1.4.3), `PP`, `HAL-E` y `HAL-T`. El plan Lean (`lean-plan`) define el MVP textual. El índice `model1.md` define 4.1.1, 4.1.2, 4.2 y 4.3. El validador admite `PREFIJOS`, `validar(run)` y `RULES`, y `rules/design_thinking.py` y `lean_canvas.py` ofrecen funciones reutilizables (`defined_codes`, lectura de tablas). La spec `skill-pipeline` define que los prerrequisitos solo avisan.

## Goals / Non-Goals

**Goals:** roles confirmados y guardados en el config; una configuración de Scrum y unos requerimientos trazables y comprobables; una base clara para historias y plan de sprints.

**Non-Goals:** historias, criterios de aceptación, Definition of Done, planificación y ceremonias (cambios 8 y 9), ejecutar las skills.

## Decisions

### D1. Roles en el config
`equipo[].rol` pasa a validarse: `null` o uno de `Product Owner`, `Scrum Master`, `Equipo de desarrollo`. Nueva función `projectcfg.set_roles(roles, root)` (con comando `set-roles --rol "Nombre=Rol"` repetible) que exige un reparto **completo**: todos los integrantes con rol, exactamente un Product Owner, exactamente un Scrum Master, al menos un Equipo de desarrollo, y nombres que existan en el equipo; si algo falla no escribe. Las skills 08 y `00-init-update` usan la misma función. **Alternativa:** guardar los roles solo en la corrida de 08; descartada porque el plan de sprints y el informe necesitan leerlos del config. **Alternativa:** varios roles por persona; descartada, el config guarda el rol principal y `equipo-scrum.md` registra si «también desarrolla» (la Guía de Scrum 2020 no impide que el Product Owner o el Scrum Master desarrollen).

### D2. Reparto propuesto
Con cuatro personas: 1 Product Owner, 1 Scrum Master y 2 Equipo de desarrollo. Con otro tamaño, un reparto válido y un aviso. La skill pregunta qué integrantes también desarrollan y si hay un interesado externo; el usuario confirma o reasigna.

### D3. Salida de 08
`equipo-scrum.md` (título `# Equipo Scrum · [proyecto]` y `## 4.1.1. Configuración del equipo Scrum`): tabla `Integrante | Rol | También desarrolla | Responsabilidades`, tabla de cadencia `Sprint | Avance | Fecha de entrega` (tres filas con las fechas del config) y línea opcional `**Interesado externo.**`. `artefactos.md` (`## 4.1.2. Artefactos de Scrum`): `**Objetivo del producto.**` derivado de `resultado_esperado` y tabla `Artefacto | Compromiso | Responsable | Dónde en el informe` con Product Backlog → Objetivo del producto, Sprint Backlog → Objetivo del sprint e Incremento → Definition of Done (Schwaber y Sutherland, 2020). «Dónde» cita puntos del índice.

### D4. Salida de 09
`rf.md` (`## 4.2. Requerimientos funcionales`): `Código | Requerimiento | Prioridad | REQ de origen | Criterio de verificación`. Redacción «El sistema debe…». Prioridad `Debe`, `Debería` o `Podría`; la propuesta usa `Debe` para los `REQ` incluidos en el MVP del plan Lean (si existe) y `Debería` para el resto. `rnf.md` (`## 4.3. Requerimientos no funcionales`): `Código | Categoría | Requerimiento | Métrica | Meta | Origen | Cómo se verifica`. `matriz-trazabilidad.md`: `REQ | Funcionalidad | RF | Motivo si no hay RF`, con todos los `REQ` del Design Thinking vigente.

### D5. Categorías de RNF y fuentes
Las categorías salen del modelo de calidad de producto ISO/IEC 25010 (edición y nombres exactos por confirmar antes de escribirlos) y se fijan en la guía y en el módulo de reglas; una prueba comprueba que ambas listas coinciden. Candidatas a citar, a **verificar por búsqueda** antes de usarlas: ISO/IEC 25010 y ISO/IEC/IEEE 29148 (calidad de la redacción de requisitos), además de Schwaber y Sutherland (2020), ya verificada. Si una norma no se puede confirmar, no se cita y la guía lo dice. Máximo 1 o 2 citas por punto, de la lista cerrada.

### D6. Validación cruzada
`rules/scrum_setup.py` lee el config de `run.parents[2]` y compara nombres, roles y fechas con `equipo-scrum.md`; valida los puntos de «Dónde» contra `model1.md`. `rules/requirements.py` resuelve con `projectcfg.current_run` la corrida vigente de Design Thinking y comprueba los `REQ` y demás códigos citados, la cobertura y la coincidencia entre `rf.md` y la matriz. Sin config o sin Design Thinking vigente informa un aviso por cada comprobación imposible.

### D7. Playbooks
`common/scrum/guia.md`: 0 (reglas: preguntar y confirmar, roles en el config, tres sprints = tres avances, sin presuponer empresa), 1 (roles y reparto), 2 (artefactos y compromisos), 3 (cadencia), 4 (errores y checklist), reservado para planificación y ceremonias, y Referencias. `common/requirements/guia.md`: 0 (reglas), 1 (RF), 2 (RNF y categorías), 3 (matriz), 4 (errores y checklist) y Referencias. Plantillas `scr-1`, `scr-2`, `req-1`, `req-2`, `req-3` y dos `README.md`.

### D8. `-update`
Patrón del cambio 1. `08-…-update`: roles (usa `set_roles` y actualiza `equipo-scrum.md`), quién también desarrolla, responsabilidades y artefactos; las fechas del config no se cambian aquí. `09-…-update`: agregar, quitar o corregir RF y RNF, prioridad y criterio; propaga a la matriz y avisa de las historias de usuario que citan un RF. Cada uno con `references/dependencias.md`.

## Risks / Trade-offs

- [Un solo rol por persona simplifica el config pero no refleja que PO o SM también desarrollen] → La columna «También desarrolla» lo registra; es una limitación explícita.
- [Normas ISO no accesibles para verificar el texto] → Solo se citan edición y título confirmados; las categorías se presentan como adaptación de la norma, sin citar su contenido literal.
- [Cambio en el Design Thinking deja `REQ` inexistentes] → La validación lo detecta; se corrige con el `-update`.
- [Cambio del config desalinea `equipo-scrum.md`] → La validación compara con el config y lo informa.
- [Change grande (dos skills, dos playbooks)] → Dos capacidades independientes con tareas separadas; se pueden aplicar en orden y archivar juntas.

## Migration Plan

Se endurece la validación de `rol` en el config. Como ningún config existente tiene roles distintos de `null`, no hay migración de datos.

## Open Questions

- Si el config debería admitir más adelante varios roles por persona (por ahora no).
- Si los RNF deben vincularse a los criterios de aceptación de las historias (se decide en el cambio 8).
