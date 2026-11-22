# add-lean-plan: Plan Lean: Lean Startup, Lean Change y canvas validado

**Cambio 6 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-lean-plan`).

## Valor
Convierte la evidencia del Design Thinking en hipótesis, MVP y experimentos, y entrega el canvas validado v1 con la evidencia que lo justifica. Es el puente entre innovación y gestión ágil.

## Skills
- `07-make-lean-plan` y `07-make-lean-plan-update`.

## Prerrequisitos
`02-make-initial-lean-canvas`, `05-make-design-thinking`.

## Playbook
Amplía `common/lean/guia.md` (creado en el cambio 3) con Lean Startup y Lean Change: hipótesis falsables, MVP **textual** (qué incluye y qué no, sin software v0.1), ciclo construir-medir-aprender con métricas de aprendizaje, criterio de pivotar o perseverar, ciclo de cambio (insights, opciones, experimentos), actores y resistencias.

Códigos propuestos: `HIP-nn`, `EXP-nn`, `MET-nn`, `ACT-nn`; reutiliza `SUP-nn` del canvas v0 y cita `HAL-E`, `PP` y `REQ` del Design Thinking.

## Modelos y formularios (`common/lean/models/`)
- `lean-2-hipotesis-supuestos.md`, `lean-3-mvp.md`, `lean-4-ciclo-medir-aprender.md` (experimentos, métricas, criterios), `lean-5-gestion-cambio.md`, `lean-6-canvas-validado.md` (v1 con tabla de cambios contra v0).

## Qué pregunta la skill
Qué supuestos priorizar, cuántos experimentos son viables en 3 sprints, criterio de éxito de cada métrica, actores afectados en el negocio. Propone todo desde el canvas v0 y el Design Thinking; el usuario confirma.

## Salida
`project/lean-plan/<corrida>/`: `seccion-3-2.md`, `seccion-3-3.md`, `canvas-v1.md`.

## Índice
Alimenta **3.2, 3.3 y 3.4**. **Este cambio corrige las marcas del índice**: 3.2.3, 3.2.4, 3.3 y 3.4 pasan a `[A1+]`: el plan y los criterios de decisión se redactan en el avance 1 y los resultados y la decisión final se añaden después (cambio 13).

## Update
Agregar o quitar una hipótesis o un experimento; cambiar una métrica; actualizar el canvas v1 y su tabla de cambios.

## Validación
Cada `HIP` con métrica y criterio de decisión; cada elemento del canvas v1 que cambió cita evidencia existente en la corrida vigente de Design Thinking; tabla de cambios v0→v1 coherente con ambos canvas.

## Fuera de alcance
Resultados de los experimentos (cambio 13).

## Decisiones abiertas para el proposal
- Cómo validar entre corridas (leer la corrida de Design Thinking del config) y qué hacer si ese código ya no existe tras un `update`.
- Cantidad de hipótesis y experimentos recomendada.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
