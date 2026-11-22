## MODIFIED Requirements

### Requirement: Cumplimiento de los objetivos
El punto 6.4.1 SHALL valorar `OG-01` y cada `OE` del capítulo 1 vigente (objetivo y meta iguales a los del capítulo) con resultado, base de evidencia (Sistema, Piloto, Prototipo o Sin medir), valoración (Cumplido, Parcial, No cumplido o No evaluable) y evidencia con códigos existentes, donde Sin medir corresponde exactamente a No evaluable; la métrica del resultado SHALL ser la del indicador del objetivo, y cuando se mida otra métrica la valoración SHALL ser Parcial con la diferencia dicha.

#### Scenario: Objetivo omitido
- **WHEN** `OE-03` no figura en el cumplimiento
- **THEN** la validación informa el código

#### Scenario: Sin medir con valoración
- **WHEN** un objetivo con base Sin medir se valora Cumplido
- **THEN** la validación informa el código

#### Scenario: Métrica distinta al indicador
- **WHEN** el indicador de `OG-01` es «resultado relevante» y el resultado mide «pedidos interpretados correctamente» y se valora Cumplido
- **THEN** la validación informa el objetivo y las dos métricas

### Requirement: Conclusiones, recomendaciones y trabajos futuros
`conclusiones.md` SHALL listar conclusiones `CNC-nn` con evidencia (códigos existentes), recomendaciones `REC-nn` que citan una conclusión y trabajos futuros `TRF-nn` con motivo y origen existente, de modo que `OG-01` y cada `OE` estén citados por alguna conclusión, y que toda historia con tareas sin avance o diferida aparezca en una conclusión y en un trabajo futuro.

#### Scenario: Conclusión sin evidencia
- **WHEN** `CNC-02` no cita ningún código de evidencia
- **THEN** la validación informa el código

#### Scenario: Objetivo sin conclusión
- **WHEN** ninguna conclusión cita `OE-02`
- **THEN** la validación informa el objetivo

#### Scenario: Componente sin avance omitido
- **WHEN** las tareas de `HU-14` figuran sin avance y ningún trabajo futuro la cita
- **THEN** la validación informa la historia
