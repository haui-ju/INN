## MODIFIED Requirements

### Requirement: Fuentes y datos modelados
La skill SHALL tomar del brief vigente el tema, los objetivos, la justificación y el alcance, y del config, de `project/domain.md` y del canvas v0 vigente todo lo que ya conste, preguntar solo lo que falte, y antes de escribir SHALL mostrar qué secciones salen de datos marcados «(modelado por el agente, …)» en `domain.md` y permitir al usuario reemplazarlos.

#### Scenario: Misión modelada
- **WHEN** la misión de `domain.md` está marcada como modelada
- **THEN** la skill lo informa y pregunta si el usuario aporta la misión real o conserva la propuesta

#### Scenario: Sin canvas
- **WHEN** no existe corrida del canvas inicial
- **THEN** la skill avisa que falta `02-make-initial-lean-canvas` y pregunta si continúa sin el punto 1.3

#### Scenario: Sin brief
- **WHEN** no existe corrida de `00b-make-project-brief`
- **THEN** la skill avisa que falta el brief y pregunta si continúa

### Requirement: Objetivos medibles y trazables
El capítulo SHALL reproducir sin cambios el objetivo general `OG-01` y los objetivos específicos `OE-nn` de la sección 3 del brief vigente, cada uno con métrica, meta y plazo alineado con las fechas de los avances, y cada `OE` SHALL indicar a qué `OG` aporta.

#### Scenario: Objetivo sin métrica
- **WHEN** un `OE` no tiene métrica ni meta
- **THEN** la validación informa el código y la causa

#### Scenario: Objetivo distinto del brief
- **WHEN** `OE-02` del capítulo difiere del `OE-02` del brief
- **THEN** la validación informa el código y que se corrige en `00b-make-project-brief-update`

#### Scenario: Evaluación posterior
- **WHEN** el análisis final evalúa el cumplimiento
- **THEN** encuentra cada `OE` definido con su métrica en este capítulo
