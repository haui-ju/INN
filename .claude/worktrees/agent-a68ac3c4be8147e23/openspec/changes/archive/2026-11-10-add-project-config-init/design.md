# Design

## Context

Estado observado: existen dos skills (`make-design-thinking` y `make-design-thinking-prototypes`), cada una con sus scripts (`new_run.sh`, `find_runs.sh`, `read_run.py`, `patch_run.py`) que resuelven la raíz del repositorio con una ruta relativa de cuatro niveles; no hay `project/config.json`; `project/` solo tiene `design-thinking/` con una corrida (`10-11-2026-00-00-46`); las specs principales y varios textos nombran las skills por su nombre actual (SKILL.md, README, scripts, `dt-4b-inventario-pantallas.md` y las specs `design-thinking-*`). El cambio `reorder-report-index` sigue activo y no se solapa (no toca skills). El equipo está en `apuntes.md` con cuatro integrantes. Motivación y alcance: ver `proposal.md`; requisitos: ver `specs/`.

## Goals / Non-goals

**Goals:**
- Una fuente única (`project/config.json`) que evite repetir preguntas y diga qué corrida está vigente en cada paso.
- Un kit compartido pequeño y sin dependencias externas para corridas, forks, config y validación.
- Un patrón de `update` barato (copiar y editar) que se pueda replicar en cada skill futura.
- Nombres con orden de ejecución claro.

**Non-goals:**
- Crear las skills `01` a `04` y `07` a `19` o sus playbooks (cambios propios).
- El `update` de la skill 06 (edita tableros de Miro; se trata con el cambio de los tableros).
- Cambiar el contenido de las corridas, el índice del informe o el generador de Design Thinking.

## Decisions

### D1. `project/config.json`, versionado por `schema`
```json
{
  "schema": 1,
  "proyecto": {"nombre": "", "tema": "", "empresa": "", "rubro": ""},
  "enfoque": "B",
  "resultado_esperado": "",
  "equipo": [{"nombre": "", "rol": null}],
  "avances": [{"n": 1, "sprint": 1, "fecha": null}, {"n": 2, "sprint": 2, "fecha": null}, {"n": 3, "sprint": 3, "fecha": null}],
  "modo_datos": "generado",
  "diseno": "common/design-system/DESIGN.md",
  "pasos": {
    "05-make-design-thinking": {"run": "10-11-2026-00-00-46", "fijada": false, "historial": ["10-11-2026-00-00-46"]}
  }
}
```
Los roles del equipo se confirman más adelante en la skill de Scrum (`08`); `00-init` solo recoge los nombres. Una entrada de `pasos` puede traer `salidas` (por ejemplo el enlace del tablero de Miro del paso 06). El paso `16-make-sprint-report` guarda una entrada por sprint (`sprints: {"1": {...}}`). **Alternativa:** YAML, descartada porque los scripts usan solo la biblioteca estándar de Python.

### D2. Kit compartido en `.claude/skills/_shared/`
Carpeta sin `SKILL.md` (no es una skill) con módulos de Python con la biblioteca estándar:

| Archivo | Función |
|---|---|
| `projectcfg.py` | Leer y validar el config, registrar una corrida (`register`), comprobar prerrequisitos (`check`) |
| `runs.py` | Crear la carpeta de corrida (`new`), bifurcar (`fork`), localizar la corrida vigente |
| `validate_run.py` | Validador genérico con reglas por skill (`rules/`) |
| `pipeline.json` | Orden, verbo, carpeta y prerrequisitos de las 20 skills |
| `policy.json` | Lista de términos prohibidos y excepciones (texto limpio) |
| `README.md` | Cómo escribir una skill nueva y su `update` |

Las skills los invocan por ruta relativa al repositorio. **Alternativa:** copiar los scripts en cada skill; descartada por la duplicación.

### D3. Regla del puntero de corrida
`register` agrega la corrida al `historial`; si `fijada` no es `true`, `run` apunta a la nueva. El usuario cambia de versión editando `run` a mano y, si no quiere que otra corrida lo reemplace, pone `fijada` en `true`. Las skills lo avisan cuando no mueven el puntero. **Alternativa:** siempre mover el puntero; descartada porque el usuario pidió poder preferir una versión.

### D4. Fork
`runs.py fork` copia la corrida base a `<DD-MM-AAAA-HH-MM-SS>-fork` en la misma carpeta de paso, deja la base intacta y agrega al `README.md` de la copia el origen y la lista de cambios pedidos. No hay cadenas de nombre (`-fork-fork`): el origen vive en el README.

### D5. Patrón de las skills `-update`
```
config -> corrida base -> prerrequisitos
   -> lista de cambios del usuario (agrega, quita, corrige)
   -> PLAN: archivos que se tocan y efectos en cadena -> confirmación
   -> fork -> edición solo de lo afectado -> validador
   -> registro en el config -> informe de cambios e incidencias
```
El plan con confirmación antes de editar es lo que mantiene el costo bajo y evita olvidar efectos en cadena. Cada `update` lleva en `references/` la tabla de dependencias de su corrida (qué archivos dependen de qué códigos). **Decisión del usuario:** el `update` edita la copia y valida con scripts; no regenera desde datos.

### D6. Validador de coherencia
Genérico: enlaces relativos que resuelven, términos prohibidos fuera del `README.md`, códigos citados que están definidos (un código está definido si aparece como título o primera celda de tabla en `bloques/`), fracciones «N de M» con N ≤ M y porcentajes coherentes con las fracciones que los acompañan. Las reglas específicas de cada skill viven en `rules/<paso>.py`; en este cambio, las del Design Thinking (prefijos `OBS`, `ENT`, `HAL-E`, `PER`, `PP`, `POV`, `HMW`, `IDE`, `REQ`, `FLO`, `FLU`, `PAN`, `PRO`, `TST`, `HAL-T`, `CON`, `ENF`). El validador termina con código distinto de cero si hay incidencias.

### D7. `pipeline.json` y prerrequisitos
Cada entrada: `orden`, `nombre`, `verbo`, `carpeta`, `requiere`. `check` consulta el config y solo avisa de prerrequisitos **que ya existen como skill** (carpeta presente en `.claude/skills/`), para que la skill 05 no avise de un canvas aún inexistente. Es un aviso, no un bloqueo. Carpetas de paso: `design-system`, `initial-lean-canvas`, `company-chapter`, `methodological-framework`, `design-thinking`, `lean-plan`, `scrum-setup`, `requirements`, `user-stories`, `sprint-plan`, `ceremonies-kanban`, `html-boards`, `system-design`, `implementation-log`, `sprint-report`, `lean-results`, `final-analysis` y `report`; la skill 06 trabaja dentro de la corrida de Design Thinking y no tiene carpeta propia.

### D8. Renombre
`git mv` de las dos carpetas; actualizar el `name:` del SKILL.md, README, scripts, la plantilla `dt-4b-inventario-pantallas.md` y las menciones. Los identificadores de las specs (`design-thinking-package-generation`, `design-thinking-prototype-mockups`) no cambian. Los textos «Purpose» de las dos specs principales nombran las skills antiguas; no se pueden cambiar por delta y se corrigen directamente tras archivar.

### D9. Registro de la corrida existente
La corrida `10-11-2026-00-00-46` se registra como vigente del paso 05. Los datos del proyecto (tema, enfoque, resultado esperado) se proponen desde su `ENF-01` y el usuario los confirma al ejecutar `00-init`; el equipo y las fechas los responde el usuario.

### D10. Skill 06 sobre la corrida del config
La skill de mockups toma como base la corrida del paso 05, se la muestra al usuario para confirmarla y solo lista corridas si la rechaza. Al terminar registra su paso con la corrida parcheada y el enlace del tablero en `salidas`.

## Risks / Trade-offs

- [Nombres que empiezan con dígitos podrían no funcionar como comando de skill] → Se verifica con la lista de skills tras crear `00-init`; si falla, se anteponen letras (`a00-`) sin cambiar el orden.
- [Falsos positivos del texto limpio (por ejemplo «falso positivo» en un texto técnico)] → `policy.json` admite excepciones por patrón.
- [El `update` omite un efecto en cadena] → Plan con confirmación antes de editar y validador después; la tabla de dependencias de cada skill se mantiene en sus `references/`.
- [Config editado a mano con JSON inválido] → Lectura con mensaje claro y sin sobrescribir.
- [Renombre que deja referencias viejas] → `grep` final de los nombres antiguos fuera de lo archivado y del cambio activo.
- [El kit crece sin control] → Solo biblioteca estándar y un módulo por responsabilidad.

## Open Questions

- Nombres y roles de los cuatro integrantes: los responde el usuario al ejecutar `00-init` (no cambia el diseño).
- Fechas de los tres avances: pueden quedar vacías hasta conocerse.
