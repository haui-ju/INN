# Design

## Context

Estado observado: no existe `common/lean/` ni skill de canvas; `pipeline.json` define `02-make-initial-lean-canvas` (verbo `make`, carpeta `initial-lean-canvas`, requiere `00-init`, con `update`). El kit tiene `projectcfg.py` (tipo de proyecto, `domain.md`, `register`), `runs.py` (corridas y forks) y `validate_run.py`, que valida códigos por `rules/<modulo>.py` (`PREFIJOS`) y admite el gancho opcional `validar(run)` (implementado por `add-design-system`, ya archivado, junto con `RULES`, que asigna una carpeta de paso a su módulo de reglas). `common/design-thinking/` es el modelo de playbook y plantillas. El índice `model1.md` define 1.3.1 (5 porqués a las problemáticas del Lean Canvas) y 1.3.2 (canvas inicial v0, contrastado con 3.4). Los playbooks de Design Thinking citan «el problema del Lean Canvas» sin fuente. `common/citation-style/` tiene APA7 e IEEE para las citas.

## Goals / Non-Goals

**Goals:** una fuente única del problema de partida, con trazabilidad (`PRB` → `POR` → `SUP`); un playbook `common/lean/` ampliable; un `-update` barato.

**Non-Goals:** canvas validado v1, hipótesis y experimentos (cambio 6), capítulo 1 completo (cambio 4), tablero visual, ejecutar la skill.

## Decisions

### D1. Salida en markdown con tres archivos
`canvas.md` (nueve bloques, versión v0, problema principal resumido en una frase), `cinco-porques.md` (una cadena por `PRB`) y `README.md` (procedencia). **Alternativa:** un solo archivo; descartada porque el capítulo 1 cita los porqués (1.3.1) y el canvas (1.3.2) por separado. **Alternativa:** tablero visual; queda para un cambio posterior.

### D2. Códigos
`PRB-nn`, `POR-nn` y `SUP-nn`, sin choque con los de Design Thinking (`PP`, `PRO`, `PER`…). `PRB-01` es el problema principal. `SUP-nn` lleva bloque, riesgo y pista de validación. Se definen en un título o en la primera celda de una tabla para que el validador genérico los reconozca.

### D3. Riesgo del supuesto
Escala alto, medio o bajo según impacto si el supuesto es falso y nivel de incertidumbre (se explica en el playbook). La lista se ordena de mayor a menor riesgo. **Alternativa:** puntaje numérico; descartada por exceso de precisión para un v0.

### D4. Cinco porqués
Entre tres y cinco niveles; cada nivel responde «¿por qué ocurre lo anterior?» con una afirmación verificable; se corta en una causa accionable (que la solución pueda atacar). Cada cadena cita su `PRB` y su fuente de evidencia si existe; en v0 casi todo es hipótesis, por lo que `SUP` recoge lo que falta comprobar.

### D5. Cantidades de referencia
Uno a tres problemas (el Lean Canvas recomienda priorizar los tres principales), tres a seis supuestos. Son referencias, no normas; la skill avisa y respeta la decisión del usuario, como en Design Thinking (sección 0.7).

### D6. Fuentes de datos de la skill
Lee el config (`tema`, `rubro`, `proyecto.tipo`, `resultado_esperado`) y `domain.md` (contexto, objetivos). Con `tipo: propio` el segmento y la propuesta de valor se redactan sin una empresa previa. Si hay una corrida de Design Thinking con `ENF-01`, la usa solo para proponer; el canvas v0 no depende de ella.

### D7. Playbook `common/lean/`
`guia.md`: 0 (reglas comunes: versionado v0, códigos, texto limpio, cantidades), 1 (Lean Canvas: los nueve bloques, cómo redactar cada uno, errores frecuentes, checklist), 2 (5 porqués), 3 (referencias citables en formato APA7, máximo 1 o 2 por sección, lista cerrada y verificada en la implementación), y encabezados reservados para «Lean Startup» y «Lean Change» que completa el cambio 6. `models/`: `lean-0-cinco-porques.md`, `lean-1-canvas.md`, `README.md`.

### D8. Validación
`rules/lean_canvas.py`: `PREFIJOS = ["PRB", "POR", "SUP"]`; `validar(run)` comprueba los nueve bloques no vacíos y en orden, la declaración de versión v0, que cada `PRB` tenga cadena `POR` de tres a cinco niveles, que `SUP` tenga bloque válido y riesgo en la escala, y el orden por riesgo. Texto limpio, enlaces y códigos citados los cubre el validador genérico.

### D9. `-update` y dependencias
Patrón del cambio 1: base del config, plan con confirmación, fork, edición de lo afectado, validador, registro (con `--no-mover` si hay incidencias). `references/dependencias.md` relaciona cada `PRB`, `POR` y `SUP` con los archivos que los citan. Avisa de las corridas de Design Thinking y del plan Lean que citen un código modificado, sin tocarlas.

## Risks / Trade-offs

- [El v0 se redacta sin evidencia y suena a hecho] → Los `SUP` marcan lo que falta validar y el playbook exige formularlos como hipótesis.
- [El canvas cambia después de que el Design Thinking lo cita] → El `-update` avisa de las citas en otras corridas; el v1 (cambio 6) documenta las diferencias.
- [Referencias bibliográficas incorrectas] → Lista cerrada, con edición y autor verificados en la implementación antes de citar.

## Migration Plan

Sin migración: el paso es nuevo. Las corridas de Design Thinking existentes no se tocan; `05-make-design-thinking` avisa si falta el canvas.

## Open Questions

- Si el canvas v0 se ofrece además como tablero visual con el sistema de diseño (posterior).
- Qué hacer si el usuario no tiene ninguna evidencia ni conocimiento del problema (la skill propone y marca `SUP` de riesgo alto).
