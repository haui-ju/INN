## Purpose
Define el análisis final del proyecto (puntos 6.4.1 a 6.4.5 y capítulo 7 del informe): el playbook y sus modelos, las skills que lo generan y lo ajustan, la comparación de lo real con lo planificado con cifras trazables, las valoraciones de objetivos, las conclusiones con evidencia y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos del análisis final
El repositorio SHALL incluir `common/final-analysis/guia.md` y `common/final-analysis/models/` con `fin-1` a `fin-5` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir la línea base, las métricas acumuladas, la valoración de objetivos, la validación con usuarios, la discusión y las conclusiones.

#### Scenario: Skill que necesita el formato
- **WHEN** `18-make-final-analysis` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos del análisis
La skill `18-make-final-analysis` SHALL leer la corrida vigente de resultados Lean, la del capítulo 1 (objetivos), los informes de sprint registrados con su `data.json`, la bitácora, el Design Thinking, el config y `project/domain.md`; si falta algún informe de sprint, los resultados Lean o el capítulo 1 SHALL avisarlo y preguntar si continúa.

#### Scenario: Informe del sprint 3 ausente
- **WHEN** el config no tiene informe del sprint 3
- **THEN** la skill lo avisa, ofrece `16-make-sprint-report` y, si el usuario continúa, el análisis declara los avances incluidos y es parcial

### Requirement: Valoraciones y confirmación antes de escribir
La skill SHALL proponer la valoración de cada objetivo con su resultado y base de evidencia, pedir al usuario la validación con usuarios disponible, las limitaciones, las conclusiones, las recomendaciones y los trabajos futuros, usar solo lo que el usuario aporta cuando `modo_datos` es `real`, y mostrar el análisis completo y esperar confirmación antes de crear archivos.

#### Scenario: Objetivo sin medición
- **WHEN** el usuario no tiene ninguna medición de un objetivo específico
- **THEN** la skill lo valora como No evaluable con motivo y no propone un resultado

### Requirement: Estructura de salida del análisis
La skill SHALL crear cada corrida en `project/final-analysis/<DD-MM-AAAA-HH-MM-SS>/` con `analisis-consolidado.md` (6.4.1 a 6.4.5), `conclusiones.md` (7.1 a 7.3) y `README.md`, y SHALL registrarla en el paso `18-make-final-analysis` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el análisis
- **THEN** la corrida contiene los dos documentos y el `README.md`, y el config la registra

### Requirement: Cumplimiento de los objetivos
El punto 6.4.1 SHALL valorar `OG-01` y cada `OE` del capítulo 1 vigente (objetivo y meta iguales a los del capítulo) con resultado, base de evidencia (Sistema, Piloto, Prototipo o Sin medir), valoración (Cumplido, Parcial, No cumplido o No evaluable) y evidencia con códigos existentes, donde Sin medir corresponde exactamente a No evaluable.

#### Scenario: Objetivo omitido
- **WHEN** `OE-03` no figura en el cumplimiento
- **THEN** la validación informa el código

#### Scenario: Sin medir con valoración
- **WHEN** un objetivo con base Sin medir se valora Cumplido
- **THEN** la validación informa el código

### Requirement: Gantt real y métricas acumuladas
Los puntos 6.4.2 y 6.4.3 SHALL declarar los avances incluidos y el corte, y sus cifras SHALL ser iguales a las que calcula el kit sobre el `data.json` de cada informe de sprint incluido: por sprint tareas, terminadas, avance, fin planificado y fin real; por avance tareas hechas, nuevas, tiempo de ciclo y rendimiento, con un acumulado cuya suma de nuevas iguale las hechas al último corte.

#### Scenario: Cifra distinta del kit
- **WHEN** el análisis dice 9 tareas hechas y el último `data.json` calcula 10
- **THEN** la validación informa ambas cifras

#### Scenario: Avances incluidos distintos de los informes
- **WHEN** el análisis dice 1, 2, 3 y el config solo registra los informes de los sprints 1 y 2
- **THEN** la validación informa la diferencia

### Requirement: Validación con usuarios y discusión
El punto 6.4.4 SHALL listar las fuentes de validación con usuarios (Design Thinking, Sistema piloto o Sistema usuarios finales), su n, su resultado y su evidencia, y el 6.4.5 SHALL dar la discusión y una tabla de limitaciones con su efecto, que SHALL tener al menos una fila cuando alguna base de 6.4.1 no sea Sistema o falte la validación del sistema.

#### Scenario: Piloto sin limitación
- **WHEN** un objetivo se valora con base Piloto y no hay limitaciones
- **THEN** la validación informa que falta declarar la limitación

### Requirement: Conclusiones, recomendaciones y trabajos futuros
`conclusiones.md` SHALL listar conclusiones `CNC-nn` con evidencia (códigos existentes), recomendaciones `REC-nn` que citan una conclusión y trabajos futuros `TRF-nn` con motivo y origen existente, de modo que `OG-01` y cada `OE` estén citados por alguna conclusión.

#### Scenario: Conclusión sin evidencia
- **WHEN** `CNC-02` no cita ningún código de evidencia
- **THEN** la validación informa el código

#### Scenario: Objetivo sin conclusión
- **WHEN** ninguna conclusión cita `OE-02`
- **THEN** la validación informa el objetivo

### Requirement: Validación del análisis final
La validación SHALL comprobar la estructura, las cifras contra los informes de sprint, los objetivos contra el capítulo 1, las evidencias y los códigos citados, las citas permitidas (Ries 2011, Little 2014 y Doran 1981, máximo dos por archivo), los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Código inexistente
- **WHEN** una conclusión cita `RES-09` y los resultados Lean vigentes no lo definen
- **THEN** la validación informa el código

### Requirement: Skill 18-make-final-analysis-update
La skill `18-make-final-analysis-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (una valoración, una cifra, la validación con usuarios, una limitación, una conclusión, una recomendación o un trabajo futuro), resincronizar las cifras con los informes vigentes si el usuario lo pide, mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Cambiar una valoración
- **WHEN** el usuario cambia la valoración de `OE-02` a Parcial
- **THEN** la copia actualiza el cumplimiento, las limitaciones y las conclusiones que la citan, y deja el resto idéntico a la base

#### Scenario: Informe final que cita el análisis
- **WHEN** el informe final ya se armó con el análisis vigente
- **THEN** la skill sugiere volver a ejecutar `19-make-report` y no lo modifica

### Requirement: Texto limpio en el análisis final
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos como falsos, inventados, de prueba o simulados.

#### Scenario: Discusión
- **WHEN** se redactan las limitaciones
- **THEN** se usa el lenguaje del proyecto sin etiquetas de procedencia
