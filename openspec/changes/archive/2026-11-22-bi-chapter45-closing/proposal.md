# Proposal

## Why

Los capítulos 4 («Storytelling con datos») y 5 («Conclusiones, recomendaciones y lecciones aprendidas») cierran el informe: el primero convierte los resultados del dashboard en una narrativa para decidir, y el segundo contrasta lo logrado con los objetivos del proyecto. Hoy `pipeline.json` declara las skills `10-make-storytelling` (sección 4) y `11-make-conclusions` (sección 5), pero ninguna existe, así que `12-make-report` las lista como pendientes. Ambas dependen de los valores reales del dashboard que entrega `bi-chapter3-build`.

La condición que las define es la misma del capítulo 3: los datos son generados y el dashboard lo construye el equipo, de modo que estas skills solo pueden contar lo que el equipo midió. Un relato o una conclusión con una cifra que no salió del dashboard es lo único que no deben producir.

## What Changes

- **Nueva skill `10-make-storytelling`** (y su `-update`): redacta la sección 4 como una narrativa de hallazgos `HLZ-nn`, cada uno con el valor real del KPI frente a su meta, la captura del dashboard que lo muestra y la decisión que el dueño o el jefe de cocina puede tomar. Cubre al menos un hallazgo por objetivo específico y usa un lenguaje condicionado a los datos generados.
- **Nueva skill `11-make-conclusions`** (y su `-update`): redacta la sección 5 con una conclusión `CNC-nn` por objetivo específico (cumplido, parcial o no cumplido según el KPI real frente a su meta), recomendaciones `REC-nn` accionables ligadas a una conclusión, y lecciones aprendidas `LEC-nn` del proceso (calidad de datos, uso de datos generados, herramienta, trabajo en equipo).
- **Trazabilidad:** objetivo específico (`OE`) → KPI (`KPI`) → valor real → hallazgo → conclusión → recomendación. El validador rechaza cifras que no estén en `valores.json` de `09-make-dashboard` y objetivos sin hallazgo o sin conclusión.
- Ambas siguen el contrato de las corridas de contenido (`secciones/<punto>.md`, `capturas/`, `referencias.md`) y registran su sección con `register`, de modo que `12-make-report` las incluye en cuanto existen.
- Playbooks en `common/10-storytelling/` y `common/11-conclusions/`, validadores en `_shared/rules/` y pruebas.

## Capabilities

### New Capabilities

- `data-storytelling`: skill `10-make-storytelling` y su `-update`; narrativa de hallazgos con valor real, meta, captura y decisión, trazada a los objetivos (sección 4).
- `report-conclusions`: skill `11-make-conclusions` y su `-update`; conclusiones por objetivo, recomendaciones y lecciones aprendidas (sección 5).

### Modified Capabilities

(ninguna: las secciones ya están declaradas en `pipeline.json` y en el índice; el marcador de captura que usa la sección 4 lo agrega `bi-chapter3-build`)

## Impact

- **Skills:** `.claude/skills/10-make-storytelling`, `10-make-storytelling-update`, `11-make-conclusions`, `11-make-conclusions-update`.
- **Kit:** `_shared/rules/storytelling.py` y `_shared/rules/conclusions.py` y pruebas en `_shared/tests/`.
- **Playbooks:** `common/10-storytelling/` y `common/11-conclusions/` con guía y plantillas.
- **Dependencias:** requiere `bi-chapter3-build` aplicado: lee `valores.json` y las capturas de `09-make-dashboard`, y usa el marcador `<!-- captura: <id> -->` de `report-assembly`. Con estas dos skills el informe queda completo, con sus cinco capítulos y los anexos A a D.
