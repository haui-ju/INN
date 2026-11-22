# Design

## Context

Estado observado: no existe `common/company/` ni skill de capítulo; `pipeline.json` define `03-make-company-chapter` (verbo `make`, carpeta `company-chapter`, requiere `00-init` y `02-make-initial-lean-canvas`, con `update`). El config guarda `proyecto.tipo` (empresa o propio) y `ruc`; `project/domain.md` (plantilla en `00-init/references/domain-plantilla.md`) reúne datos generales, reseña, misión, visión, valores, objetivos y contexto, con el marcador «(modelado por el agente, …)» en lo que no tiene fuente. La spec archivada `lean-canvas-initial` define el canvas v0: `canvas.md` con la línea «Problema principal: PRB-01 · <frase>», nueve bloques `## N. Nombre` y la sección «Supuestos de mayor riesgo», y `cinco-porques.md` con una sección `## POR-nn · PRB-nn` por problema. El índice `model1.md` define 1.1 a 1.6 (1.3.1 y 1.3.2 vienen del canvas). El validador admite `PREFIJOS`, el gancho opcional `validar(run)` y `RULES` (carpeta de paso → módulo de reglas), implementados por `add-design-system`, ya archivado. El cambio 13 evaluará los objetivos en 6.4.1.

## Goals / Non-Goals

**Goals:** un capítulo 1 listo para pegar, coherente con el config, `domain.md` y el canvas; objetivos medibles que el análisis final pueda evaluar; funcionar con o sin empresa.

**Non-Goals:** el marco metodológico, la evaluación de objetivos, el canvas, ejecutar la skill, cambiar `model1.md`.

## Decisions

### D1. Salida
`capitulo-1.md` (puntos 1.1 a 1.6, con el 1.3 reproducido del canvas), `bloques/` con `1-1-presentacion.md`, `1-2-diagnostico.md`, `1-4-objetivos.md`, `1-5-justificacion.md` y `1-6-alcances-limitaciones.md`, y `README.md`. `capitulo-1.md` se arma a partir de los bloques para que el `-update` edite el bloque y el capítulo juntos. **Alternativa:** solo `capitulo-1.md`; descartada porque dificulta editar un punto sin tocar los demás.

### D2. Datos y marcador
Fuentes en orden: `domain.md` (reseña, misión, visión, valores, objetivos de la empresa y contexto), canvas v0 (1.3 y el problema), config (tema, rubro, resultado esperado, fechas de avances). Al armar el plan, la skill lista las secciones cuyo origen en `domain.md` lleva el marcador y pregunta si el usuario aporta el dato real. La skill detecta el marcador por su texto literal «(modelado por el agente,» dentro de cada sección de `domain.md`.

Correspondencia de secciones de `domain.md` (plantilla de `00-init`) con el capítulo:

| Punto del capítulo | `tipo: empresa` | `tipo: propio` |
|---|---|---|
| 1.1 (datos generales) | «Datos generales» | «Descripción de la solución» |
| 1.1.1 | «Reseña histórica» | «Origen del proyecto» (de «Descripción de la solución» y «Problema que resuelve») |
| 1.1.2 | «Misión» | «Propósito (misión del proyecto)» |
| 1.1.3 | «Visión» | «Visión» |
| 1.1.4 | «Valores» | «Valores» |
| 1.4 (propuesta de objetivos) | «Objetivos de la empresa» | «Objetivos» |
| 1.2 y 1.6 (contexto) | «Clientes y competencia», «Contexto del proyecto» | «Usuarios y beneficiarios», «Alcance y contexto» |

El texto del capítulo no lleva el marcador; el `README.md` de la corrida anota «secciones salidas de datos modelados: …».

### D3. Tipo de proyecto
La skill lee `proyecto.tipo`, lo confirma y, si el usuario lo corrige, deriva a `00-init-update`. Con `propio`: 1.1 «Presentación del proyecto» con subpuntos 1.1.1 «Origen del proyecto», 1.1.2 «Propósito», 1.1.3 «Visión» y 1.1.4 «Valores»; el diagnóstico es del entorno del problema (microentorno: usuarios, recursos del equipo, alternativas actuales; macroentorno: contexto tecnológico, normativo, económico). Se conserva la numeración para no romper referencias.

### D4. FODA
Cuatro cuadros con códigos `FOR`, `DEB`, `OPO`, `AME`; cada ítem con enunciado y evidencia o fuente. Sin puntaje (decidido: basta el código y la evidencia). Referencia de 3 a 5 ítems por cuadro. Los códigos se definen en la primera celda de la tabla para que el validador genérico los reconozca.

### D5. Objetivos
`OG-01` y de tres a cinco `OE-nn`, en tabla: código, objetivo (verbo + qué), métrica, meta, plazo, aporta a. El plazo usa las fechas de `avances` del config. Los `OE` deben poder evaluarse con las métricas que el proyecto produce (Kanban, pruebas, validación con usuarios), de modo que 6.4.1 pueda calificar cada uno.

### D6. Justificación, alcances y limitaciones
1.5 con tres dimensiones (práctica, social o económica, y metodológica) en prosa corta y con 1 o 2 citas de la lista cerrada. 1.6 con tabla de alcances (incluye y excluye) y limitaciones (tiempo de tres sprints, equipo de cuatro, datos disponibles), coherente con `resultado_esperado`.

### D7. Playbook
`common/company/guia.md`: 0 (reglas comunes: tipo de proyecto, marcador, códigos, cantidades de referencia, texto limpio), 1 (presentación), 2 (diagnóstico), 3 (objetivos), 4 (justificación y alcances), 5 (adaptación a proyecto propio), 6 (referencias APA7 de lista cerrada verificada en la implementación, máximo 1 o 2 por punto), 7 (errores frecuentes y checklist). `models/`: las cuatro plantillas y el `README.md`.

### D8. Validación
`rules/company.py`: `PREFIJOS = ["FOR", "DEB", "OPO", "AME", "OG", "OE"]`; `validar(run)` comprueba secciones 1.1 a 1.6, que 1.1 se titule según el tipo, ítems del FODA con evidencia, objetivos con métrica, meta y plazo, `OE` ligado a `OG-01`, y que 1.3 coincida con el canvas vigente. El canvas se resuelve con `projectcfg.current_run('02-make-initial-lean-canvas', root=<raíz>)`, donde la raíz es `run.parents[2]` de la corrida validada. La comparación normaliza espacios y exige que cada sección `POR-nn` de `cinco-porques.md` aparezca en 1.3.1, que cada uno de los nueve bloques de `canvas.md` aparezca en 1.3.2 y que la frase de «Problema principal» (`PRB-01`) aparezca en el capítulo. Si no hay canvas vigente, informa el aviso en lugar de fallar.

### D9. `-update`
Patrón del cambio 1. `references/dependencias.md`: qué bloque y qué parte de `capitulo-1.md` dependen de cada código (`FOR`…`OE`), qué citas de `OE` existen en otras corridas y cómo se relaciona 1.3 con el canvas. Cambiar `tipo` no se hace aquí (`00-init-update`).

## Risks / Trade-offs

- [Datos de empresa mal modelados que parezcan reales] → La skill los muestra antes de escribir; el `README.md` los lista; el usuario puede reemplazarlos.
- [Canvas cambia después de generar el capítulo] → La validación detecta que 1.3 ya no coincide; se corrige con el `-update`.
- [Objetivos que no se pueden evaluar al final] → Se exige métrica y meta y se alinean con las métricas del proyecto.
- [Referencias bibliográficas incorrectas] → Lista cerrada, verificada en la implementación.

## Migration Plan

Sin migración: el paso es nuevo.

## Open Questions

- Si el FODA debería priorizarse más adelante (por ahora, no).
- Si la adaptación del título de 1.1 para proyecto propio debe reflejarse también en `model1.md` (por ahora, solo en el capítulo generado).
