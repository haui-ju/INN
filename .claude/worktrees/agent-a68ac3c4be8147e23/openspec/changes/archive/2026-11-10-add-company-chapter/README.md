# add-company-chapter: Capítulo 1: la empresa y el problema

**Cambio 4 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-company-chapter`).

## Valor
Entrega el capítulo 1 del informe listo para pegar: presentación de la empresa (o del proyecto, si es propio), diagnóstico, objetivos y justificación, coherente con el canvas v0. **No da por hecho que existe una empresa**: lee `proyecto.tipo` del config y lo confirma con el usuario al ejecutarse. Los objetivos que define (`OG`, `OE`) los evalúa al final el cambio 13.

## Skills
- `03-make-company-chapter` y `03-make-company-chapter-update`.

## Prerrequisitos
`00-init` (config y `project/domain.md`), `02-make-initial-lean-canvas`.

## Playbook
`common/company/guia.md` (lo crea este cambio): cómo redactar reseña, misión, visión y valores; FODA dividido en micro y macroentorno; objetivos medibles (verbo + qué + métrica + plazo); justificación (teórica, práctica, social); alcances y limitaciones. Citas permitidas (1 o 2 por punto).

Códigos propuestos: `FOR-nn`, `DEB-nn` (microentorno), `OPO-nn`, `AME-nn` (macroentorno), `OG-nn`, `OE-nn`.

## Modelos y formularios (`common/company/models/`)
- `emp-1-presentacion.md` (1.1.1 a 1.1.4)
- `emp-2-diagnostico.md` (FODA con códigos)
- `emp-3-objetivos.md` (OG y OE medibles)
- `emp-4-justificacion-alcance.md` (1.5 y 1.6)
- `README.md` de los modelos.

## Qué pregunta la skill
Primero confirma **si el proyecto se aplica a una empresa o es propio** (lo toma de `proyecto.tipo`; si el usuario lo corrige, sugiere `00-init-update`). Con empresa: usa los datos de `project/domain.md` (obtenidos por RUC), confirma lo que falte (historia relevante, misión, visión y valores; si no constan, propone y confirma), proveedores/competidores/clientes, contexto económico y regulatorio, qué queda dentro y fuera del proyecto. Con proyecto propio: adapta 1.1 a la presentación del proyecto y su equipo, y el diagnóstico al entorno del problema. Usa también el canvas v0.

## Salida
`project/company-chapter/<corrida>/`: `capitulo-1.md` (puntos 1.1 a 1.6) y `bloques/` con un archivo por modelo; 1.3 se resume desde el canvas v0 sin duplicarlo.

## Índice
Alimenta **1.1, 1.2, 1.4, 1.5 y 1.6**, y enlaza **1.3**. Sin cambios al índice.

## Update
Corregir un dato de la empresa, un ítem del FODA o un objetivo: toca el archivo origen, `capitulo-1.md` y cualquier cita `OG`/`OE`.

## Validación
Objetivos con verbo, métrica y plazo; cada ítem FODA citado está definido; 1.3 coincide con el canvas v0; los `OE` aportan al `OG`.

## Fuera de alcance
Marco metodológico (cambio 5), evaluación de objetivos (cambio 13).

## Decisiones abiertas para el proposal
- Si el FODA lleva puntuación o priorización.
- Cuántos objetivos específicos son razonables (rango del playbook).
- Cómo se adapta el índice cuando el proyecto es propio (1.1 «Presentación de la empresa» pasaría a «Presentación del proyecto»; mismo número, otro título) y si el título se ajusta en `model1.md`.
- Los datos de `domain.md` marcados «(modelado por el agente, …)» se copian al capítulo **sin** el marcador, que solo consta en `domain.md`.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
