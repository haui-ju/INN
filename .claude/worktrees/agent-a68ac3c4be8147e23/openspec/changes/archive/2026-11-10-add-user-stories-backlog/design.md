# Design

## Context

Estado observado: no existe `common/user-stories/`; `pipeline.json` define `10-make-user-stories` (requiere `09-make-requirements`, con `update`). La corrida de requerimientos aporta `rf.md` (`RF-nn`, prioridad `Debe`/`Debería`/`Podría`, `REQ` de origen), `rnf.md` y la matriz. `08-make-scrum-setup` aporta el Product Owner y el compromiso «Definition of Done» del Incremento. El índice define 4.4.1 (historias con su REQ de origen), 4.4.2 (backlog priorizado) y 4.5 (criterios de aceptación y Definition of Done), y los informes de sprint usan pies de foto «HU-XX nombre (REQ-XX)». El validador admite `PREFIJOS`, `validar(run)` y `RULES`; `rules/requirements.py` ya lee la corrida vigente de requerimientos con `projectcfg.current_run`. El plan de sprints (cambio 9) usará el backlog.

## Goals / Non-Goals

**Goals:** una cadena trazable REQ → RF → HU → CA verificable por script; un backlog ordenado con reglas objetivas; un acuerdo explícito con el usuario antes de generar criterios.

**Non-Goals:** asignar historias a sprints, capacidad, ceremonias, ejecutar las skills.

## Decisions

### D1. Una historia por archivo
`historias/HU-nn.md` con título `# HU-nn · [Título]` (el código del nombre de archivo coincide con el del título), `**Historia.** Como…, quiero…, para…`, `**Origen.** RF-nn[, RF-mm] (REQ-nn[, REQ-mm])`, `**RNF aplicables.** RNF-nn, … | Ninguno` y la sección `## Criterios de aceptación` con tabla `Código | Escenario | Dado | Cuando | Entonces`. El punto 4.4.1 del informe lo arma `19-make-report` a partir de estos archivos. **Alternativa:** un solo `historias.md`; descartada porque el `-update` edita una historia sin tocar las demás.

### D2. Trazabilidad contra requerimientos
`Origen` cita ≥1 `RF` de la corrida vigente de `09-make-requirements`; los `REQ` entre paréntesis deben ser exactamente los `REQ` de esos RF según `rf.md`. Los `RNF` citados deben existir en `rnf.md`. Todo `RF` tiene historia o figura en la tabla opcional `### RF sin historia` (`RF | Motivo`) del backlog.

### D3. Criterios de aceptación
Formato Dado/Cuando/Entonces; de 2 a 5 por historia (mínimo 2 validado); `CA-nn` con numeración única en toda la corrida. Los RNF no se vinculan a cada criterio: se citan en la historia y entran por la Definition of Done («cumple los RNF aplicables»).

### D4. Backlog
`## 4.4.2. Product Backlog priorizado` con `**Escala de estimación.**` (por defecto «Puntos de historia (1, 2, 3, 5, 8, 13)»; alternativa «Tallas (XS, S, M, L, XL)») y `**Criterio de orden.**`, y la tabla `Orden | HU | Historia | RF | Prioridad | Estimación`. Reglas: orden 1..N sin repetir; `Historia` igual al título; `RF` igual al origen de la historia; `Prioridad` igual a la más alta de sus RF (Debe > Debería > Podría); el orden no puede poner una prioridad menor antes de una mayor (dentro de un nivel decide el Product Owner); estimación dentro de la escala. No hay sprint tentativo: eso es del cambio 9.

### D5. Criterios y Definition of Done
`criterios-dod.md`: `## 4.5. Criterios de aceptación y Definition of Done`; `### Criterios de aceptación` con una frase de formato y la tabla `HU | Criterios` (lista de `CA` que debe coincidir con los archivos de historias); `### Definition of Done` con al menos 5 condiciones observables en lista (por ejemplo: criterios verificados con el Product Owner, pruebas de la historia pasan, cumple los RNF aplicables, integrado sin errores, registrado en la bitácora). Es el compromiso del Incremento de `08-make-scrum-setup`.

### D6. Dos confirmaciones
Primero el **acuerdo de historias** (lista con título, quién, qué y para qué, derivada de los RF); luego los criterios de las historias acordadas; una confirmación final del conjunto (historias, criterios, backlog y DoD) antes de escribir. Una historia nueva sin RF no se crea: se propone agregarla a los requerimientos.

### D7. Fuentes
Lista cerrada, **verificada por búsqueda antes de citar**: Cohn (2004) para el formato de historias, Wake (2003) para INVEST, North (2006) para Dado/Cuando/Entonces y Schwaber y Sutherland (2020) para la Definition of Done (ya verificada). Una fuente de estimación (Cohn, 2005) solo si se confirma. Máximo 1 o 2 citas por archivo.

### D8. Validación
`rules/user_stories.py`: `PREFIJOS = ["HU", "CA"]`; `validar(run)` lee con `projectcfg.current_run` la corrida vigente de requerimientos (`rf.md`, `rnf.md`) y comprueba historias (formato, origen, REQ derivados, RNF), criterios (mínimo, códigos únicos), cobertura de RF, backlog (orden, prioridad, escala, coincidencia con historias) y `criterios-dod.md` (resumen igual a los archivos, DoD ≥ 5 condiciones). Sin requerimientos vigentes informa un aviso.

### D9. `-update`
Patrón del cambio 1. Modos: historias (agregar con RF, quitar, corregir), criterios, orden/prioridad/estimación, Definition of Done y «RF sin historia». Quitar una historia quita su archivo, su fila del backlog y su fila del resumen; reorganiza el campo `Orden` pero no renumera los `HU`. `references/dependencias.md` relaciona cada código con los archivos que lo citan y avisa de las corridas posteriores.

## Risks / Trade-offs

- [Historias genéricas copiadas de los RF] → El acuerdo previo y la regla «Como…, quiero…, para…» con beneficio propio del proyecto.
- [Backlog que cambia al editar los requerimientos] → La validación detecta RF nuevos sin historia y prioridades desalineadas.
- [Demasiadas historias para tres sprints] → Cantidad de referencia y aviso; la capacidad se evalúa en el plan de sprints.
- [Fuentes mal citadas] → Lista cerrada verificada por búsqueda.
- [El Product Owner no decide realmente el orden] → La skill lo nombra desde la configuración de Scrum y registra su decisión en `README.md`.

## Migration Plan

Sin migración: el paso es nuevo.

## Open Questions

- Si la estimación debería hacerse en una sesión con el equipo (por ahora la propone la skill y el usuario la ajusta).
- Si los criterios de aceptación deben enlazar directamente con los casos de prueba del diseño del sistema (lo decide el cambio 11).
