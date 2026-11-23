# Contratos del cierre (capítulos 4 y 5)

Notas de trabajo del apply. Si una pieza necesita cambiar un contrato, lo dice antes de cambiarlo.

## Entradas que ya existen (capítulo 3, archivado)

- `valores.json` de la corrida vigente de `09-make-dashboard` (`project/09-dashboard/<corrida>/`): `{schema: 1, kpis: [{codigo, valor, unidad, meta, periodo}], medidas: [{codigo, valor}]}`; `meta` es `null` si el KPI sigue sin meta. Los KPI y sus metas y comparadores (≥ o ≤) salen de `modelo.json` y 2.5 de `07-make-data-model-kpi`.
- Capturas del equipo: `capturas/pag-<nn>.png` y `capturas/pag-<nn>.md` (pie, una línea) en la corrida de 09. Sección 3.2 de 09 las marca con `<!-- captura: pag-nn -->`.
- `_shared/rules/dashboard.py` trae `_comparador(meta)` y la lógica de estado `Cumple / No cumple / Sin meta`; reutilízala importándola, no la copies.
- `12-make-report` busca `capturas/<id>.png` en la corrida **de la propia sección** (la de 10 para la sección 4). Por eso la skill 10 copia a su corrida las capturas que cita (con su `.md` de pie) y marca cada una con `<!-- captura: pag-nn -->`.

## Corrida de `10-make-storytelling` (`project/10-storytelling/<corrida>/`)

`secciones/4.md` (encabezado exacto del índice), `capturas/` (las copiadas), `referencias.md` (APA 7, si cita), `README.md`. Códigos `HLZ-nn`. Cada hallazgo: `OE-nn`, KPI, valor real frente a la meta (con el estado), la captura que lo muestra y la decisión que apoya (dueño o jefe de cocina, según el brief).

## Corrida de `11-make-conclusions` (`project/11-conclusions/<corrida>/`)

`secciones/5.md` (encabezado exacto del índice), `referencias.md` (si cita), `README.md`. Códigos `CNC-nn` (una por `OE` y una del `OG`), `REC-nn` (ligada a una conclusión, con quién decide y el KPI que mostrará si funcionó) y `LEC-nn`. Estado de cada conclusión: cumplido, parcial o no cumplido, calculado del valor real frente a la meta según el sentido del indicador; sin meta se declara que no se puede concluir.

## Reparto de archivos entre piezas

| Pieza | Escribe en |
|---|---|
| Skill 10 | `.claude/skills/10-make-storytelling*`, `common/10-storytelling/`, `_shared/rules/storytelling.py`, `_shared/tests/test_storytelling.py` y `storytelling_fixtures.py` |
| Skill 11 | `.claude/skills/11-make-conclusions*`, `common/11-conclusions/`, `_shared/rules/conclusions.py`, `_shared/tests/test_conclusions.py` y `conclusions_fixtures.py` |
| Integración (al final) | Los archivos compartidos y `tasks.md` |
