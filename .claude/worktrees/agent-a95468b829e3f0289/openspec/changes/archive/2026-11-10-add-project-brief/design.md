# Design

## Context

Estado observado: `00-init` pregunta nombre, tema, rubro, tipo y RUC, enfoque, resultado esperado, equipo, las tres fechas de entrega y el modo de datos, y escribe `project/config.yaml` y `project/domain.md` (con datos modelados para misión, visión, valores y objetivos de la empresa a partir del tema). `02` lee tema, rubro, tipo y resultado del config y pregunta el problema; `03` propone `OG-01` y `OE-nn` desde `domain.md`; `08`, `11`, `12`, `13` y `19` leen las fechas del config y `11` pregunta además el inicio del proyecto. `avances[]` guarda `n`, `sprint` y `fecha` (entrega). Cada skill usa corridas versionadas (`project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/`), `-fork` en su `-update`, `projectcfg.py register` y un módulo `rules/` para validar; `projectcfg.py check` avisa sin bloquear si faltan prerrequisitos. El esquema de nombres ya admite una letra tras los dos dígitos.

## Goals / Non-Goals

**Goals:** un solo documento núcleo definido por el usuario con ayuda guiada; que todas las skills lo lean; fechas de los tres sprints definidas una vez; evitar preguntas repetidas.

**Non-Goals:** cambiar el formato de los entregables de las demás skills, ejecutar las skills, migrar corridas (no hay).

## Decisions

### D1. La skill `00b-make-project-brief`
Entra con `orden` 1 en `pipeline.json` (los siguientes suben uno), `carpeta` `project-brief`, `verbo` `make`, `update` verdadero y `requiere` `00-init`. Flujo: lee el config (nombre, tipo, rubro, equipo) y cualquier insumo existente (`apuntes.md`, `ENF-01` de un Design Thinking), recorre las secciones **una por una** (AskUserQuestion o texto), propone una redacción por sección a partir de lo que el usuario cuenta, la pule con él hasta que la confirma y solo entonces escribe. Lo que el usuario no sabe queda `Pendiente` y no se redacta como hecho; con `modo_datos: real` solo se usa lo que el usuario informa.

### D2. El brief (`brief.md`)
Encabezado `# Brief del proyecto · <nombre>` y ocho secciones con título exacto:
1. `## 1. Tema` (nombre del proyecto y tema en una frase).
2. `## 2. Problemática` (**Problema principal**, **Quién lo sufre**, **Situación actual** y **Evidencia** como lista).
3. `## 3. Objetivos`: `### 3.1. Objetivo general` (tabla `OG-01`) y `### 3.2. Objetivos específicos` (tabla `OE-nn`), con las columnas del formato de `emp-3` (código, objetivo, métrica, meta, plazo y, en los `OE`, «Aporta a»).
4. `## 4. Justificación y alcance`: justificación práctica, social o económica y metodológica, tabla de alcance (incluye y no incluye) y tabla de limitaciones.
5. `## 5. Usuarios y enfoque`: **Enfoque** (A, B o C) y **Usuarios** (quiénes usan la solución y quién decide).
6. `## 6. Resultado esperado`: **Resultado**, **Métrica** y **Meta**.
7. `## 7. Calendario`: tabla `Sprint | Avance | Inicio | Entrega` (tres filas, fechas `DD-MM-AAAA`).
8. `## 8. Supuestos y riesgos iniciales`: tabla `Código | Tipo | Descripción | Cómo se vigila`, con `INI-nn` y tipo `Supuesto` o `Riesgo`.
Los códigos `OG-01` y `OE-nn` son los mismos que usan `03` y `18`, que los toman de aquí.

### D3. `domain.md` pasa a crearlo 00b
Las secciones modeladas de `domain.md` (misión, visión, valores, objetivos de la empresa) se plantean a partir del tema, que ahora se define en 00b. Por eso 00b, tras confirmar el brief, crea `project/domain.md` con la plantilla actual y su regla del marcador «(modelado por el agente, …)»: con `tipo: empresa` busca los datos por el RUC (con su fuente); con `tipo: propio` describe la solución con lo del brief. El problema, los usuarios y los objetivos de una solución propia salen del brief y no se duplican en `domain.md`. `00-init` ya no escribe `domain.md`; `projectcfg.py check` avisa si falta.

### D4. Config y calendario
`avances[]` gana `inicio` (`DD-MM-AAAA` o `null`). `projectcfg.py set-nucleo` escribe `proyecto.tema`, `resultado_esperado`, `enfoque` y `avances[].inicio` y `fecha` con validación y conserva los comentarios. El brief es la fuente: la validación exige que el config coincida con la sección 1 (tema), 5 (enfoque), 6 (resultado) y 7 (fechas). `11-make-sprint-plan` toma el inicio del sprint 1 de `avances[0].inicio` (si es `null`, avisa e indica `00b-make-project-brief-update`) y los inicios siguientes siguen siendo el día posterior a la entrega anterior; si el brief ya fija los inicios, la validación de 11 exige que coincidan.

### D5. Validación del brief
`rules/project_brief.py` comprueba: las ocho secciones y subsecciones en su orden; `OG-01` único; al menos dos `OE` con métrica, meta y plazo y «Aporta a» = `OG-01`; el plazo de cada objetivo es «Avance N (fecha)» con N de 1 a 3 y esa fecha igual a la entrega del calendario; el calendario tiene tres sprints en orden, sin solaparse, con la entrega dentro de su sprint (entre inicio y fin del sprint, y el inicio posterior a la entrega anterior); enfoque válido; `INI-nn` con tipo válido; tema, enfoque, resultado y fechas iguales a los del config; secciones no vacías (o `Pendiente` explícito); texto limpio; y que `domain.md` exista tras la confirmación.

### D6. Todas las demás skills leen el brief
- Cada `SKILL.md` de `02` a `19` lista `project/project-brief/<corrida>/brief.md` en sus fuentes obligatorias, con lo que toma de él (tabla abajo). Las skills de `-update` heredan de su base.
- El kit lo exige: `projectcfg.py check` avisa, para toda skill a partir de la `02`, si no hay corrida vigente del brief; una prueba comprueba que cada `SKILL.md` de `02` a `19` lo cite.

| Skill | Toma del brief |
|---|---|
| 02 | Tema, problemática, resultado esperado, usuarios |
| 03 | `OG-01` y `OE-nn` (copia), justificación y alcance (1.5 y 1.6), tema |
| 04 | Tema y enfoque (para el glosario y la integración) |
| 05 | Enfoque, usuarios, problemática (hipótesis de partida) |
| 07 | Resultado esperado, supuestos y riesgos iniciales |
| 08 | Calendario, equipo y alcance |
| 09 y 10 | Objetivos, alcance y usuarios |
| 11 | Calendario (inicio y entrega de cada sprint) |
| 12 y 13 | Calendario (ceremonias, cortes de los tableros) |
| 14 y 14b | Alcance y limitaciones |
| 15 y 16 | Calendario y objetivos del avance |
| 17 | Resultado esperado y supuestos |
| 18 | Objetivos (cumplimiento) y resultado esperado |
| 19 | Tema, equipo, calendario y objetivos para la portada y el control del documento |

### D7. `00b-make-project-brief-update`
Bifurca la corrida, edita solo la sección o la fila afectada, copia al config lo que cambie (`set-nucleo`), regenera `domain.md` solo si cambió el tema, el tipo o el RUC y valida. Su `references/dependencias.md` dice qué `-update` correr después según lo que cambió: tema o problemática → `02` y `03`; objetivos → `03` y `18`; justificación o alcance → `03`; enfoque o usuarios → `05`; resultado esperado → `07`, `17` y `18`; calendario → `11`, `12` y `13`; supuestos → `07`.

### D8. `00-init` y `00-init-update`
`00-init` pregunta nombre, rubro, tipo (con RUC si es empresa), equipo y modo de datos, escribe el config con valores neutros para el núcleo (tema vacío, enfoque `B`, resultado vacío, avances sin fechas) y sugiere `00b-make-project-brief`. `00-init-update` cambia esos datos técnicos y, ante un cambio de tema, enfoque, resultado o fechas, remite a `00b-make-project-brief-update`.

### D9. Pruebas
Parsing y validación del brief (secciones, objetivos, calendario, coherencia con el config), `set-nucleo`, el aviso de brief ausente, el cambio en `11` (inicio del config), el flujo `00-init` → `00b` en un proyecto de ejemplo, la prueba de que toda skill de `02` a `19` cita el brief y las de pipeline (22 pasos, `00b` tras `00-init`).

## Risks / Trade-offs

- [Cambiar 00-init y varias skills a la vez] → cada cambio es leer el brief en lugar de preguntar; las pruebas de flujo y de pipeline lo cubren.
- [El usuario no conoce una fecha o un dato] → queda `Pendiente`, las skills posteriores lo tratan como pendiente y `00b-update` lo completa.
- [Dos lugares con el mismo dato (brief y config)] → el brief manda, 00b copia y la validación exige igualdad.
- [domain.md ahora depende de 00b] → el aviso del kit lo señala y `00-init` ya no lo menciona como creado.

## Migration Plan

Se agregan la skill, el kit y las pruebas, se ajusta `00-init` y se actualizan las fuentes de las demás skills. No hay corridas en `project/` que migrar.

## Open Questions

- Si más adelante conviene un modo de importar el brief desde un documento existente del usuario.
