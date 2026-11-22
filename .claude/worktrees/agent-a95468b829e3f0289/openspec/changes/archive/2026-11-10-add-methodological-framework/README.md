# add-methodological-framework: Capítulo 2: marco metodológico

**Cambio 5 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-methodological-framework`).

## Valor
Explica qué metodologías se usan y cómo se integran (Design Thinking → Lean → Scrum y Kanban), con un glosario que crece a medida que se añaden skills.

## Skills
- `04-make-methodological-framework` y `04-make-methodological-framework-update`.

## Prerrequisitos
`00-init` (usa 02 y 03 si existen).

## Playbook
`common/methodological-framework/guia.md` (lo crea este cambio): qué debe cubrir cada metodología (principios, roles, eventos, artefactos, cuándo usarla), criterio de elección, diagrama de integración (qué produce cada una y qué recibe la siguiente), reglas del glosario y **lista cerrada de fuentes citables** (1 o 2 por punto) que se verifica en el proposal.

## Modelos y formularios (`common/methodological-framework/models/`)
- `mar-1-innovacion.md` (2.1), `mar-2-agiles.md` (2.2), `mar-3-integracion.md` (2.3), `mar-4-glosario.md` (2.4), `README.md`.

## Qué pregunta la skill
Profundidad deseada (resumen o detallado), metodologías que el equipo realmente usa, términos del negocio que van al glosario. Lee `pipeline.json` para no describir metodologías que el proyecto no aplica.

## Salida
`project/methodological-framework/<corrida>/`: `capitulo-2.md` y `glosario.md`.

## Índice
Alimenta **2.1 a 2.4**. El glosario (2.4 `[A1+]`) se amplía con términos de capítulos posteriores mediante el `-update`.

## Update
Agregar o quitar un término, ajustar la integración al cambiar el flujo del proyecto.

## Validación
Todo término usado en el capítulo está en el glosario y viceversa, citas dentro de la lista cerrada, coherencia con las skills realmente presentes en el pipeline.

## Fuera de alcance
Aplicar las metodologías (cambios 6, 7, 8 y 9).

## Decisiones abiertas para el proposal
- Lista de fuentes y edición exacta de cada una.
- Si el glosario se mantiene en esta corrida o se genera de nuevo en el armado (cambio 14).

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
