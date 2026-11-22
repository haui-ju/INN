# Proposal

## Why

El pipeline actual de skills produce un informe de innovación (Design Thinking, Lean, Scrum y Kanban, con tres avances y una app). El nuevo proyecto es un informe de Inteligencia de Negocios con Power BI, de una sola entrega, con la estructura y la rúbrica de la consigna del curso. Todas las skills nuevas dependen de una base común (índice del informe, orden y nombres de skills, config y brief), así que esa base debe cambiar primero y lo que ya no aplica debe retirarse antes de construir los capítulos.

## What Changes

- **Índice nuevo del informe** (`common/structure/`): cinco capítulos de BI (diagnóstico estratégico, diseño técnico BI, ETL y dashboard en Power BI, storytelling con datos, conclusiones y lecciones) sin marcas de avance, sin historial de versiones acumuladas y con la numeración de la consigna.
- **Numeración nueva y única de las skills**: de `00-init` a `13-make-annex-html`. Cada skill y la carpeta que produce (en `project/` y en `common/`) llevan el mismo número, sin letras intercaladas (`00b` y `14b` desaparecen). `pipeline.json` define el orden, los prerrequisitos y las secciones que aporta cada skill.
- **Registro de secciones del informe en el config**: `project/config.yaml` lista `informe.secciones` (derivadas de `pipeline.json`); al terminar, cada skill numerada las marca como disponibles con su corrida vigente mediante `register`. El ensamblado (change posterior) arma el informe solo con lo disponible.
- **Config y brief adaptados a BI**: el config deja de llevar avances, sprints y roles de Scrum; el brief pasa a ser la skill `01-make-project-brief` y define el núcleo del proyecto de BI (empresa, problemática, OG y OE, justificación, alcance y calendario único).
- **Skills base renumeradas y ajustadas**: `00-init`, `01-make-project-brief` y `02-design-system`, cada una con su `-update`.
- **Retiro de lo que no aplica** (**BREAKING**): skills `02` a `18` y `21` a `24` del pipeline viejo, sus carpetas en `common/` (Design Thinking, Lean, Scrum, Kanban, sprints, historias, requerimientos, diseño de sistema, mockups, bitácora, informes de sprint, análisis final, app) y los visuales HTML que ya no se usan (Gantt, Kanban, journey map, mapa de empatía, etc.). Los módulos de `_shared` y sus validadores y tests que dependían de lo retirado se eliminan o se adaptan. Las skills viejas sirven de molde para las nuevas de los changes siguientes, así que se consultan antes de borrarlas (ver design).
- `19-make-report` y los validadores del informe se reescriben en otro change; este deja el esquema listo para ellos.

## Capabilities

### New Capabilities

- `report-section-registry`: lista de secciones del informe en `project/config.yaml` (`informe.secciones`), su derivación desde `pipeline.json`, el registro de secciones disponibles cuando una skill hace `register` y la consulta de qué secciones tienen corrida.

### Modified Capabilities

- `skill-pipeline`: nuevo esquema de nombres (número de dos dígitos sin letra, carpeta de salida con el mismo número), nueva secuencia de `00` a `13` y secciones aportadas por cada skill en `pipeline.json`.
- `project-config`: campos del config para BI (sin `avances`, `enfoque` de Design Thinking ni roles de Scrum, con `informe.secciones` y calendario único) y comportamiento de `00-init` y `00-init-update`.
- `project-brief`: skill `01-make-project-brief` y su `-update`, brief orientado a BI (problemática, OG y OE medibles, justificación, alcance, calendario único, supuestos y riesgos).
- `design-system`: renumeración a `02-design-system` y a la carpeta `project/02-design-system/` con su `-update`; el resto de sus requisitos se conserva.
- `run-versioning`: las corridas se escriben en carpetas con el número de la skill (`project/<NN-nombre>/<DD-MM-AAAA-HH-MM-SS>/`); el resto del versionado se conserva.
- `report-index-structure`: el índice maestro pasa a los cinco capítulos de BI, sin marcas de avance ni numeración protegida de Design Thinking.

## Impact

- **Skills** (`.claude/skills/`): se renombran y ajustan `00-init`, `00b-make-project-brief`, `01-design-system` y sus `-update`; se eliminan las skills retiradas; las demás (`openspec-*`, `redaccion-academica`) no cambian.
- **Kit compartido** (`.claude/skills/_shared/`): `pipeline.json`, `projectcfg.py` (nuevo esquema de config y `register` ampliado), `runs.py` y `validate_run.py` (rutas numeradas), `report_map.json` (se vacía o se rehace en el change de ensamblado); se retiran los módulos y reglas de lo eliminado y sus tests.
- **Playbooks** (`common/`): se renombran `project-brief` y `design-system` con su número, se reescribe `common/structure/model1.md` y se eliminan las carpetas retiradas; `common/html/` conserva lo reutilizable (por ejemplo, FODA) y se limpia el resto.
- **Specs** (`openspec/specs/`): seis specs se modifican, una se crea y las de las capacidades retiradas (design-thinking, lean, scrum, kanban, sprints, historias, requerimientos, diseño de sistema, mockups, bitácora, informes de sprint, análisis final, app, tableros y visuales viejos y ensamblado actual) se retiran al archivar este change.
- **Dependencias entre changes**: bloquea a `bi-chapter1-diagnosis`, `bi-chapter2-design` y `bi-report-assembly`; los changes de los capítulos 3 a 5 siguen congelados.
- **Proyecto en curso**: `project/` ya está vacío en el árbol de trabajo (los archivos figuran borrados), así que no hay corridas que migrar.
