# add-final-analysis: Resultados Lean y análisis final

**Cambio 13 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-final-analysis`).

## Valor
Cierra el ciclo: mide lo planificado contra lo real, completa el aprendizaje Lean y entrega conclusiones y recomendaciones con evidencia.

## Skills
- `17-make-lean-results` y su `-update`.
- `18-make-final-analysis` y su `-update`.

## Prerrequisitos
17: `07-make-lean-plan`, `15-make-implementation-log`. 18: `16-make-sprint-report`, `17-make-lean-results`.

## Playbook
`common/final-analysis/guia.md` (lo crea este cambio): cómo comparar contra la línea base, cálculo de métricas acumuladas, cómo evaluar objetivos, discusión honesta de limitaciones, redacción de conclusiones (cada una con evidencia), recomendaciones y trabajos futuros.

Códigos propuestos: `RES-nn` (resultado de experimento), `CNC-nn` (conclusión; no se usa `CON` porque ya es el consentimiento del Design Thinking), `REC-nn` (recomendación), `TRF-nn` (trabajo futuro).

## Modelos y formularios (`common/final-analysis/models/`)
- `fin-1-resultados-lean.md`, `fin-2-cumplimiento-objetivos.md`, `fin-3-metricas-acumuladas.md`, `fin-4-conclusiones.md`, `README.md`.

## Qué pregunta la skill
Resultados de cada experimento, decisión de pivotar o perseverar (la propone con evidencia, el usuario confirma), valoración de cada objetivo, validación con usuarios disponible, limitaciones a declarar.

## Salida
- `project/lean-results/<corrida>/`: `resultados.md`, `decision.md`.
- `project/final-analysis/<corrida>/`: `analisis-consolidado.md` (6.4), `conclusiones.md` (capítulo 7).

## Índice
Alimenta **3.2.3 y 3.2.4** (resultados), **6.4.1 a 6.4.5** y **7.1 a 7.3**.

## Update
Corregir una cifra o una valoración; recalcula métricas acumuladas y las conclusiones que la citan.

## Validación
Cada `OE` evaluado, métricas acumuladas iguales a la suma de los informes de sprint, cada conclusión con evidencia citada.

## Fuera de alcance
Armado del documento (cambio 14).

## Decisiones abiertas para el proposal
- Cómo tratar objetivos medibles solo con un piloto.
- Qué hacer si falta el informe de un sprint (aviso y análisis parcial).

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
