# Design

## Context

Estado observado: `common/lean/` existe (guía y modelos `lean-0` y `lean-1` del Lean Canvas inicial, con la sección 4 reservada para este cambio) y define `PRB`, `POR` y `SUP`. La skill `02-make-initial-lean-canvas` escribe `canvas.md` (nueve bloques `## N. Nombre`, tabla de supuestos con riesgo) y `cinco-porques.md`. Las skills `05` y `06` escriben el Design Thinking (códigos `HAL-E`, `PP`, `POV`, `HMW`, `IDE`, `REQ`, `FLU`, `PAN`, `TST`, `HAL-T`…; `REQ` definidos en `matriz-priorizacion.md`; alcance del MVP en 3.1.4.3). `pipeline.json` define `07-make-lean-plan` (requiere `02` y `05`, con `update`). El validador admite `PREFIJOS`, `validar(run)` y `RULES`, y `projectcfg.current_run` resuelve la corrida vigente de otro paso. `model1.md` marca 3.2 a 3.4 como `[A1]`. `lean_canvas.py` ya sabe leer bloques y supuestos del canvas.

## Goals / Non-Goals

**Goals:** convertir supuestos en hipótesis comprobables con trazabilidad completa; un MVP textual; un plan de cambio con actores; un canvas v1 que muestre qué cambió y por qué.

**Non-Goals:** resultados y decisión final (cambio 13), el Design Thinking, ejecutar la skill.

## Decisions

### D1. Salida
`seccion-3-2.md` (3.2.1 a 3.2.4), `seccion-3-3.md` (3.3.1 a 3.3.3), `canvas-v1.md` (3.4) y `README.md` con las corridas base usadas (canvas v0 y Design Thinking). Encabezados `## 3.N.` / `### 3.N.M.` con el punto tras el número, como en el capítulo 1.

### D2. Códigos
`HIP-nn`, `MET-nn`, `EXP-nn`, `CAM-nn`, `INS-nn`, `OPC-nn`, `ACT-nn`; se definen en la primera celda de tablas. Sin choque con `PRB/POR/SUP`, `FOR/DEB/OPO/AME/OG/OE` ni los de Design Thinking. `EXP` se usa para experimentos de negocio (3.2.3) y de cambio (3.3.2); se distinguen por la sección donde se definen y por la columna `Tipo`.

### D3. Hipótesis (3.2.1)
Tabla `Código | Hipótesis | Supuesto | Evidencia previa | Métrica | Criterio de éxito`. Redacción falsable: «Creemos que… Lo sabremos cuando… (umbral)». Cada `HIP` cita ≥1 `SUP` del canvas v0 y una `MET`; la evidencia previa cita códigos del Design Thinking o «ninguna». Todo `SUP` de riesgo alto debe estar cubierto por una `HIP`.

### D4. MVP textual (3.2.2)
Tres listas/tablas: **Incluye** (`REQ` tomados de 3.1.4.3), **No incluye** (lo pospuesto) y **Cómo prueba las hipótesis** (`REQ | Funcionalidad | HIP`). Cada `REQ` incluido prueba ≥1 `HIP`. Es alcance, no software v0.1.

### D5. Ciclo y experimentos (3.2.3)
Tabla `Código | Experimento | Pone a prueba | Método | Métrica | Criterio de éxito | Avance` (Avance 1, 2 o 3 según `avances` del config) y tabla de métricas `MET-nn | Métrica | Cómo se mide | Umbral | Fuente`. Cada `HIP` es puesta a prueba por ≥1 `EXP`; el método es una técnica realista (prueba de usuario, entrevista de pago, prototipo, piloto). Cantidad de referencia: 2 a 4 de negocio, máximo 2 por avance.

### D6. Criterios de decisión (3.2.4)
Tabla `Hipótesis | Perseverar si | Pivotar si`, con umbral numérico o condición observable, antes de ejecutar. Los criterios se redactan en el avance 1; la decisión final y su justificación las añade `17-make-lean-results` en el avance final. Por eso el punto se marca `[A1+]`.

### D7. Lean Change (3.3)
3.3.1: `CAM-nn | Qué cambia | Antes | Después | Actor`. 3.3.2: tres tablas: insights (`INS-nn | Insight | Evidencia`), opciones (`OPC-nn | Opción | Insight | Actor`) y experimentos de cambio (`EXP-nn | Experimento | Opción | Métrica | Criterio de éxito`). 3.3.3: `ACT-nn | Actor | Cómo lo afecta | Resistencia esperada | Acción de acompañamiento`. Con `tipo: propio`, los actores son los usuarios y el equipo.

### D8. Canvas v1 (3.4)
`canvas-v1.md`: `Versión: v1`, «Problema principal», los nueve bloques, `## Supuestos: estado` (`Código | Estado | Evidencia o hipótesis`, estados `validado`, `refutado`, `pendiente`; validado/refutado citan código del Design Thinking, pendiente cita una `HIP`) y `## Cambios respecto al v0` (`Bloque | v0 | v1 | Evidencia`). La validación compara los bloques con el v0 normalizando espacios y encabezados: el conjunto de bloques distintos debe ser exactamente el de la tabla de cambios.

### D9. Validación entre corridas
`rules/lean_plan.py` resuelve con `projectcfg.current_run` (raíz = `run.parents[2]`) el canvas v0 vigente (`02-make-initial-lean-canvas`) y la corrida vigente de Design Thinking (`05-make-design-thinking`). Los códigos `SUP`, `PRB` salen del canvas (con las funciones de `lean_canvas.py`); los `HAL-E`, `PP` y `REQ` salen de los `bloques/` de Design Thinking (reglas de `validate_run.defined_codes`). Un código citado que ya no exista, por ejemplo tras un `-update` del Design Thinking, se informa como incidencia de esta corrida y se corrige con el `-update` del plan. Sin canvas o sin Design Thinking vigente se informa un aviso por cada comprobación que no se puede hacer.

### D10. Marcas del índice
Se cambian en `model1.md`: 3.2.3, 3.2.4, 3.3 y 3.4 → `[A1+]`. Los subpuntos de 3.3 mantienen `[A1]`. No se modifica el historial de versiones.

### D11. Playbook
`common/lean/guia.md`: se reemplaza la sección 4 reservada por **4. Lean Startup**, **5. Lean Change Management**, **6. Canvas validado v1** y **7. Errores frecuentes y checklist del plan**; se amplían 0.3 (códigos) y 0.4 (cantidades) y las Referencias con Ries (2011) y Little (2014). Las secciones 1 a 3 no cambian. Modelos: `lean-2` (hipótesis y supuestos), `lean-3` (MVP), `lean-4` (ciclo y criterios), `lean-5` (gestión del cambio), `lean-6` (canvas v1).

### D12. `-update`
Patrón del cambio 1. Modos: hipótesis (agregar/quitar/corregir: toca experimentos, métricas, criterios, MVP y supuestos del v1), experimentos y métricas, cambio (actores, insights, opciones), y canvas v1. `references/dependencias.md` relaciona cada código con los archivos que lo citan y avisa de `lean-results` (cambio 13) y de las corridas de requisitos e historias.

## Risks / Trade-offs

- [Hipótesis que suenan a certezas] → Redacción falsable obligatoria con umbral; la validación exige métrica y criterio.
- [Canvas v1 que cambia sin evidencia] → Cada cambio debe citar un código existente del Design Thinking vigente.
- [Códigos del Design Thinking que desaparecen tras un `-update`] → La validación los detecta contra la corrida vigente; el `-update` del plan los corrige.
- [Plan demasiado grande para tres sprints] → Cantidades de referencia, máximo 2 experimentos por avance y asignación explícita.
- [Mezcla de experimentos de negocio y de cambio con el mismo código] → Se distinguen por sección y columna `Tipo`; la validación comprueba que cada uno cite lo que corresponde.

## Migration Plan

Se amplía el playbook existente (sin tocar sus secciones 1 a 3) y se corrigen cuatro marcas del índice. Sin migración de datos: el paso es nuevo.

## Open Questions

- Cómo representar una hipótesis que depende de datos que solo existirán en un sprint posterior (por ahora: `pendiente` en el canvas v1 y experimento en el avance correspondiente).
- Si conviene reservar en el índice un punto para los resultados de los experimentos (por ahora los reciben 3.2.3 y 3.2.4 mediante `17-make-lean-results`).
