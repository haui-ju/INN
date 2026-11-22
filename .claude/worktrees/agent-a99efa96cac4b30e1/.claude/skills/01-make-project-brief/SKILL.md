---
name: 01-make-project-brief
description: Define con el usuario el núcleo del proyecto de Inteligencia de Negocios en project/01-project-brief/ (brief.md): el tema y la empresa, la problemática, los objetivos medibles (OG y OE) con su indicador, la justificación y el alcance, los usuarios y las decisiones que apoyará el dashboard, las fuentes de datos previstas, el calendario (inicio y entrega) y los supuestos y riesgos iniciales; luego crea project/domain.md y copia al config el tema y las fechas. Pregunta sección por sección, propone una redacción, la pule con el usuario y espera su confirmación antes de escribir. Úsala justo después de 00-init, antes de cualquier otra skill, o cuando el usuario pida "01-make-project-brief", "definir el proyecto", "brief", "objetivos del proyecto", "problemática" o "fecha de entrega". Para cambiar algo ya definido usa 01-make-project-brief-update.
---

# 01-make-project-brief

Es el **núcleo del proyecto de BI**: aquí el usuario define de qué trata, qué problema del negocio resuelve, qué objetivos persigue, qué entra y qué no, quiénes usarán el dashboard y qué decisiones apoyará, de qué fuentes saldrán los datos y cuándo se entrega. Todas las demás skills leen este brief y no vuelven a preguntar esos datos.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/01-project-brief/guia.md` (playbook: reglas, preguntas y pulido por sección, objetivos medibles, calendario, `domain.md`, errores).
2. `common/01-project-brief/models/README.md` y `brief-1-nucleo.md` (formato exacto del brief).
3. `project/config.yaml` (`proyecto.nombre`, `tipo`, `ruc`, `rubro`, `equipo`, `modo_datos`) y, si existe, `apuntes.md` para proponer valores; la plantilla `references/domain-plantilla.md`.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `show`, `check`, `current`, `register`, `set-nucleo`)
- `python3 .claude/skills/_shared/brief.py leer | al-config` (datos del brief vigente; copia al config el tema y el calendario).
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `rules/project_brief.py`).

## Reglas

- **Una sección a la vez.** Pregunta lo mínimo, propón una redacción a partir de lo que el usuario cuenta, muéstrala, ajústala con él y pasa a la siguiente solo cuando la confirme.
- **No inventes.** Lo que el usuario no sabe queda **«Pendiente»**; una propuesta tuya se presenta como propuesta y el usuario la acepta, la corrige o la deja pendiente. Con `modo_datos: real` usa solo lo que informa.
- **Objetivos medibles:** un `OG-01` y de 2 a 5 `OE-nn`, cada uno con métrica, meta con cifra o criterio, plazo `Entrega (DD-MM-AAAA)` e indicador (KPI o indicador del negocio); cada `OE` aporta a `OG-01`. El plazo coincide con la entrega del calendario.
- **Fuentes:** cada fuente con tipo (`Interna`, `Abierta` o `Generada`) y acceso (`Autorizado`, `Público` o `Pendiente`). Una empresa real sin autorización usa solo fuentes abiertas o generadas, como pide la consigna.
- **Calendario:** una fila con inicio y entrega en `DD-MM-AAAA` (o «Pendiente»); la entrega no es anterior al inicio.
- **No presupongas una empresa.** Con `tipo: propio` la empresa se describe con lo que el usuario cuente; con `tipo: empresa` el dominio se busca por el RUC.
- **Escribe solo tras confirmar el resumen completo.** El brief manda sobre el config.
- Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config.** `python3 .claude/skills/_shared/projectcfg.py validate`; si falla, detente e indica `00-init`. Si ya hay una corrida (`projectcfg.py current --step 01-make-project-brief`), avisa que se creará otra versión y ofrece `01-make-project-brief-update`.
2. **Insumos.** Lee el config y, si existe, `apuntes.md`; muéstrale al usuario lo que ya sabes (nombre, tipo, rubro, equipo) para que no lo repita.
3. **Sección por sección** (AskUserQuestion o texto), en este orden: 1 Tema y empresa, 2 Problemática, 3 Objetivos, 4 Justificación y alcance, 5 Usuarios y decisiones, 6 Fuentes de datos previstas, 7 Calendario, 8 Supuestos y riesgos iniciales. En cada una: pregunta, propón la redacción (o una meta, un indicador, decisiones, fuentes, 2 o 3 supuestos), ajusta con el usuario y confirma antes de seguir. En la sección 4 pregunta qué herramientas piensan usar además de Power BI (por ejemplo para el ETL o el almacenamiento); si no lo saben, queda «Pendiente».
4. **Resumen.** Muestra el brief completo (y las secciones que quedaron «Pendiente») y **espera la confirmación**; si el usuario pide cambios, vuelve a la sección y repite.
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 01-make-project-brief)` y escribe en `$RUN` el `brief.md` (plantilla `brief-1-nucleo.md`) y el `README.md`: procedencia (modo de datos del config, qué propuso el agente y qué aceptó o corrigió el usuario, lo que quedó pendiente). Es el único lugar donde se anota.
6. **Config.** `python3 .claude/skills/_shared/brief.py al-config --run <corrida>` (copia el tema y las fechas de inicio y entrega; rechaza fechas incoherentes).
7. **`domain.md`.** Con `tipo: empresa`: busca los datos por el RUC (WebSearch y, si hace falta, WebFetch), muéstralos **con su fuente**, pide confirmación y completa lo que no encuentres (reseña, misión, visión, valores, industria y tamaño) a partir del tema y el rubro con el marcador `(modelado por el agente, por no contar con X)`. Con `tipo: propio`: describe la empresa o la solución, su misión, visión y valores con lo del brief. Usa `references/domain-plantilla.md` y escribe `project/domain.md` (si ya existe, muéstralo y pregunta antes de reemplazarlo).
8. **Validar.** `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (secciones, objetivos con indicador y plazo igual a la entrega, fuentes, calendario, coherencia con el config y `domain.md`).
9. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 01-make-project-brief --run <carpeta>`. Si responde `"movido": false` (paso fijado), díselo al usuario.
10. **Cierre.** Entrega la ruta, el resumen del brief, lo que quedó «Pendiente» (y que se completa con `01-make-project-brief-update`), los supuestos que tomaste y sugiere `02-design-system` (opcional) o `03-make-business-diagnosis`.
