# Design

## Context

Cada skill tiene un módulo en `.claude/skills/_shared/rules/<paso>.py` con funciones `check_*` y un `validar(run)` que devuelve incidencias `(archivo, causa)`, y sus pruebas en `_shared/tests/test_<paso>.py` con fixtures. Las inconsistencias del informe del avance 3 pasan esas validaciones porque comprueban estructura y códigos, no coherencia entre pasos ni dentro de un mismo dato. Ver proposal.md para el motivo y la lista.

## Goals / Non-Goals

**Goals:**
- Cada inconsistencia encontrada falla en la validación de la skill que la produce, con mensaje que indique qué `-update` ejecutar.
- Cada regla tiene una prueba con el caso real encontrado.

**Non-Goals:**
- No se corrigen datos de corridas existentes ni se ejecutan `-update`.
- No se cambia el formato de salida de ninguna skill salvo una columna o campo mínimo cuando una regla lo necesita (zona «Iterar si», «Cierre anticipado», base de medición).
- No se valida semántica de texto libre.

## Decisions

**1. Reglas donde nace el dato, no en el informe.** Cada regla se agrega al validador del paso que produce la información (por ejemplo, el solape de ceremonias en `ceremonies_kanban.py`), y la validación del informe (19) ya las hereda porque solo ensambla corridas vigentes. *Alternativa descartada:* chequear todo en `rules/report.py`; avisa tarde y contradice la regla de que el informe no se corrige a mano.

**2. Reglas entre pasos usan la corrida vigente del otro paso.** Las comprobaciones cruzadas (estado del canvas v1 contra decisiones de 17; `Iterar si` del plan contra la decisión; plazo del objetivo frente a su base) leen la corrida vigente del paso fuente con las mismas utilidades que ya usan los validadores (`projectcfg.current`). Si la corrida fuente no existe, la regla se omite y no falla.

**3. Zona «Iterar» explícita en el plan.** El plan Lean pasa a tener tres umbrales por hipótesis (Perseverar si, Iterar si, Pivotar si). Es un cambio mínimo en la tabla del punto 3.2.4 y en el modelo de la skill 07; sin él no se puede comprobar que no haya huecos. *Alternativa descartada:* seguir llamándolo «zona de iterar» sin umbral; es precisamente el hueco detectado.

**4. Cinco porqués: cinco niveles o cierre justificado.** Se mantiene la libertad de cerrar antes solo con motivo registrado (`Cierre anticipado`), y el nombre «cinco porqués» solo se usa si todas las cadenas llegan a cinco. *Alternativa descartada:* obligar siempre a cinco; fuerza niveles artificiales.

**5. Predecesoras en el estado real.** La regla vive en `html_boards.py` porque ahí se combina la línea base (predecesoras) con el estado real (avance y fechas). La regla de predecesoras ya existe para la línea base; aquí se extiende al avance.

**6. Casos de prueba sin ejecutar.** La bitácora (15) exige un resultado por cada caso de una historia terminada y un «No ejecutado» con motivo para los de historias sin avance; así el informe (6.x y 5.5.2) puede decir qué no se probó sin inventarlo.

**7. Objetivo, métrica y base.** El brief (00b) añade a cada objetivo la base de medición, y el análisis final (18) compara la métrica medida con el indicador del brief. Un objetivo medido con otra métrica queda Parcial, no Cumplido.

**8. Mensajes que guían la corrección.** Cada incidencia nueva termina indicando el `-update` que corrige la causa, en español, con el mismo estilo de las existentes.

## Risks / Trade-offs

- [Corridas existentes empiezan a fallar al validarse] → Es lo buscado: la implementación termina con una lista de qué `-update` ejecutar, y se hace después de implementar, no dentro de este change.
- [Falsos positivos de duplicados de casos de prueba] → La regla exige mismo tipo, misma verificación y mismos datos; lo ambiguo queda como aviso, no como error.
- [Falsos positivos con la regla de fin de semana en proyectos con jornadas especiales] → La regla es comprobable porque el calendario viene del config; se informa la fecha y el día para que el usuario decida.
- [Añadir campos a los modelos obliga a tocar las plantillas de 00b y 07] → Se acota a un campo cada una y las corridas viejas siguen siendo válidas salvo en esas reglas.

## Open Questions

- Ninguna que cambie las specs o las tareas.
