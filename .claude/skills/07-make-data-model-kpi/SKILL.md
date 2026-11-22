---
name: 07-make-data-model-kpi
description: Redacta las secciones 2.4 y 2.5 del informe de Inteligencia de Negocios en project/07-data-model-kpi/ (secciones/2.4.md y 2.5.md y modelo.json): el modelo de datos en estrella (tablas de hechos con granularidad y medidas, dimensiones con atributos y jerarquías, relaciones con cardinalidad y dirección de filtro) con su figura HTML modelo-datos, y los KPI con fórmula, medida propuesta, campos de origen, meta, frecuencia, objetivo que miden y decisión que apoyan, trazados a los objetivos del brief. Propone el modelo y los KPI y espera la confirmación antes de escribir. Úsala después de 06-make-bi-solution o cuando el usuario pida "07-make-data-model-kpi", "modelo de datos", "modelo estrella", "hechos y dimensiones", "KPI" o "indicadores clave". Para cambiar uno ya creado usa 07-make-data-model-kpi-update.
---

# 07-make-data-model-kpi

Cierra el diseño técnico del capítulo 2: define cómo se modelan los datos (2.4) y cómo se miden los objetivos (2.5). La rúbrica pide hechos, dimensiones y relaciones bien definidos y KPI justificados y articulados a los objetivos; el capítulo 3 (ETL y dashboard) construye lo que aquí se diseña a partir de `modelo.json`.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/07-data-model-kpi/guia.md` (playbook: fuentes, contrato de la corrida, códigos, `modelo.json`, estrella, KPI, errores y checklist).
2. `common/07-data-model-kpi/models/README.md` y las plantillas `dm-1-modelo.md`, `dm-2-kpi.md` y `dm-3-modelo-json.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`), las corridas vigentes de `05-make-problem-objectives` y `06-make-bi-solution` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution`), `project/domain.md` y el config.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/diagnostico.py` (`titulos`, `leer --paso …`)
- `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <corrida> --carpeta <corrida>/visuales [--diseno <tokens.json>]`
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/data_model_kpi.py`).

## Reglas

- **Estrella por defecto**, con nombres `f<Nombre>` y `d<Nombre>`; un copo de nieve solo si se justifica. Cada hecho declara su **granularidad** y medidas con agregación (`suma`, `promedio`, `conteo`, `conteo distinto`, `mínimo` o `máximo`); un porcentaje no es una medida del hecho sino un KPI.
- **Toda dimensión se relaciona con algún hecho** y toda relación cita tablas que existen. Si algún KPI tiene frecuencia por periodo, hay una dimensión de tiempo.
- **Trazabilidad:** cada `OE` del brief tiene al menos un KPI y uno de ellos se llama como su indicador en el brief; todo campo de origen (`tabla.campo`) existe en el modelo; la meta lleva cifra y comparador o «Pendiente»; la decisión es una de las del brief.
- **Las fuentes salen de la arquitectura:** los campos que el modelo necesita deben poder venir de las fuentes de `06`; si un KPI exige un dato que ninguna fuente aporta, avísalo al usuario antes de escribirlo.
- **`modelo.json` repite las secciones** (mismos códigos, nombres, medidas, claves, atributos, relaciones y KPI); se escribe después de ellas y se actualiza junto con ellas.
- **Códigos** `FCT`, `DIM`, `REL` y `KPI`: numerados por prefijo, sin repetir.
- **Contrato de la corrida:** cada `secciones/<punto>.md` empieza con su encabezado exacto y solo tiene texto final; solo 2.4 lleva figura, la línea `<!-- figura: modelo-datos -->`; el HTML se genera con `visuales.py` a partir de `modelo.json`, nunca a mano; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar el plan.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 07-make-data-model-kpi` y muestra los avisos. Si falta la corrida de `06-make-bi-solution`, avisa que el modelo no podrá apoyarse en la arquitectura y pregunta si continúa solo con las fuentes del brief; si falta la de `05`, avisa que no habrá matriz de articulación para comprobar las causas. Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `07-make-data-model-kpi-update`.
2. **Insumos.** Lee del brief los `OE-nn` con su indicador y meta, las fuentes con sus datos y las decisiones; de `06` los componentes y el almacenamiento; del dominio, los nombres de canales, turnos, locales o productos.
3. **Preguntas** (AskUserQuestion), solo lo que falte: el grano de los hechos si no es evidente, las metas que el brief no fija (o «Pendiente») y la frecuencia con que la gerencia revisa cada indicador.
4. **Plan y confirmación.** Muestra en líneas cortas: los hechos (código, nombre, granularidad, medidas), las dimensiones (código, nombre, clave, atributos), las relaciones y una fila por KPI (código, nombre, objetivo, meta, frecuencia, origen). Comprueba la cobertura de los `OE`. **Espera la confirmación.**
5. **Escritura.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 07-make-data-model-kpi)` y escribe en `$RUN/secciones/` los archivos `2.4.md` y `2.5.md` con las plantillas, luego `$RUN/modelo.json` copiado de ellas, `$RUN/referencias.md` si hay citas y `$RUN/README.md` (modo de datos, corridas de origen de `01`, `05` y `06`, qué propuso el agente y qué confirmó el usuario, metas pendientes).
6. **Figura.** `python3 .claude/skills/_shared/visuales.py construir --visual modelo-datos --run <corrida> --carpeta $RUN/visuales` (con `--diseno` si hay sistema de diseño vigente).
7. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole las rutas de `$RUN/secciones/*.md` y los datos propios del caso; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; no debe quedar ningún aviso bloqueante y, si falta un dato, pregúntaselo al usuario). Después, `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (estructura del modelo, relaciones, trazabilidad de los KPI y coincidencia de `modelo.json`); si cambias el modelo, actualiza `modelo.json` y vuelve a construir la figura.
8. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 07-make-data-model-kpi --run <carpeta>` (marca 2.4 y 2.5 como disponibles). Si responde `"movido": false`, díselo al usuario.
9. **Cierre.** Entrega la ruta, un resumen (hechos, dimensiones, relaciones y KPI con su objetivo y meta), cómo abrir el HTML de la figura para copiar la imagen, las metas «Pendiente» y que el capítulo 2 queda completo (`projectcfg.py secciones`). El capítulo 3 todavía no tiene skill; sugiere `12-make-report` para ver el avance del informe.
