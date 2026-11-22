# Kit compartido de las skills

Carpeta sin `SKILL.md` (no es una skill). Contiene lo que usan todas las skills numeradas del pipeline de Inteligencia de Negocios. Solo biblioteca estándar de Python.

| Archivo | Para qué sirve |
|---|---|
| `pipeline.json` | Orden, verbo, carpeta numerada de corrida, prerrequisitos, si tiene `-update` y las secciones del informe que aporta cada una de las 14 skills (`00` a `13`) |
| `policy.json` | Términos prohibidos en el texto de las corridas y sus excepciones (texto limpio) |
| `projectcfg.py` | Leer, validar y registrar `project/config.yaml`; comprobar prerrequisitos; marcar y consultar las secciones del informe (`informe.secciones`) |
| `html_tpl.py`, `visuales.py` | Plantillas HTML de `common/html/` y lo que las llena: los visuales del informe se registran en `visuales.py` |
| `doc_html.py` | Conversión de Markdown a HTML autónomo con los estilos de `common/document-html/` (lo usan el informe y sus anexos) |
| `report.py` y `rules/report.py` | Armado del informe (`12-make-report`): `plan`, `construir` (solo las secciones disponibles, figuras, referencias, anexos y faltantes), `render` (HTML) y `anexos` (HTML de los anexos, `13-make-annex-html`); `cargar_indice` expone la marca de imagen por punto. El validador se carga por la carpeta `12-report` |
| `diagnostico.py` | Lectura de las secciones de las corridas de los capítulos 1 y 2 (03 a 07) como datos, encabezados exactos del índice y comprobaciones comunes (figuras, citas, marcadores) |
| `brief.py` | Leer el brief del proyecto (`project/01-project-brief/`) y copiar al config su tema y su calendario |
| `runs.py` | Crear la carpeta de corrida y bifurcarla (`-fork`) |
| `validate_run.py` y `rules/` | Validador de coherencia con reglas genéricas y por paso (`rules/<carpeta sin número, con _>.py`) |
| `tests/` | Pruebas: `python3 -m unittest discover -s .claude/skills/_shared/tests` |

Las skills retiradas del pipeline anterior (Design Thinking, Lean, Scrum, Kanban, app) se pueden consultar como molde con `git show pre-bi-pipeline:<ruta>`.

## Cómo crear una skill nueva

1. **Nombre.** `[orden de dos dígitos]-[verbo]-[nombre]` con verbo `make`, `design` o `init`, sin letras intercaladas. Debe existir en `pipeline.json` (con su carpeta numerada, prerrequisitos y secciones). Su homóloga se llama igual con `-update` al final.
2. **Carpeta numerada.** La corrida va en `project/<NN-nombre>/` y el playbook en `common/<NN-nombre>/`, donde `<NN-nombre>` es el nombre de la skill sin el verbo `make` (con `design` se conserva completo).
3. **Frontmatter.** `name` igual al nombre de la carpeta y `description` que diga qué hace y cuándo usarla.
4. **Preguntar y confirmar.** Pide con AskUserQuestion solo lo que el config y el brief no traen, propone valores y espera confirmación del plan o de las propuestas (objetivos, KPI, visuales) antes de escribir.
5. **Playbook y modelos.** Si el contenido necesita método propio, crea `common/<NN-nombre>/guia.md` (reglas, códigos de trazabilidad, rangos) y `common/<NN-nombre>/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`. La skill lee el playbook antes de generar.
6. **Carpeta de corrida.** `python3 .claude/skills/_shared/runs.py new --step <skill>` crea `project/<NN-nombre>/<DD-MM-AAAA-HH-MM-SS>/`. Nunca se escribe sobre una corrida anterior.
7. **README de la corrida.** Es el único lugar donde se anota la procedencia (modo de datos y, en un fork, el origen y los cambios).
8. **Texto limpio.** Ningún otro archivo de la corrida dice que algo es falso, inventado, de prueba o simulado. La regla vive en `policy.json`.
9. **Validar.** Corre `validate_run.py <corrida>`. Si el paso tiene reglas propias, crea `rules/<nombre_sin_numero>.py` (por ejemplo `rules/strategic_analysis.py` para `04-strategic-analysis`); se carga solo.
10. **Registrar.** `projectcfg.py register --step <skill> --run <carpeta>`: agrega al historial, mueve la corrida vigente (salvo que `fijada` sea `true`) y marca como disponibles las secciones del informe de la skill. El usuario puede editar `run` a mano.
11. **Prerrequisitos.** `projectcfg.py check --skill <skill>` al empezar; avisa, no bloquea.
12. **Su `-update`.** Config, base, prerrequisitos, lista de cambios del usuario, plan con confirmación, `runs.py fork`, edición solo de lo afectado, validador y registro (`--no-mover` si hay incidencias). Lleva `references/dependencias.md` con la tabla de qué archivos dependen de qué. Modelo: `01-make-project-brief-update`. `00-init` se cambia con `00-init-update`; `12-make-report` y `13-make-annex-html` no tienen `update`.
13. **Índice.** Si la skill necesita secciones o anexos nuevos en `common/structure/model1.md`, se amplía el índice sin renumerar los capítulos 1 a 5 y se declaran en `pipeline.json`.
