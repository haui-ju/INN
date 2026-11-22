# Spec Delta

## Purpose

Produce las secciones 1.5 a 1.7 del informe de BI (PESTEL, FODA con estrategias cruzadas e Ishikawa) con la skill `04-make-strategic-analysis` y su `-update`, articuladas entre sí y con la problemática del brief.

## ADDED Requirements

### Requirement: Playbook y modelos del análisis estratégico
El repositorio SHALL incluir `common/04-strategic-analysis/guia.md` (factores PESTEL, códigos, FODA y estrategias cruzadas, categorías 6M del Ishikawa, fuentes y citas, errores y checklist) y `common/04-strategic-analysis/models/` con un `README.md` y una plantilla por sección (1.5, 1.6 y 1.7) con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: El ejemplo de cada plantilla valida
- **WHEN** se arma una corrida con los ejemplos de las tres plantillas
- **THEN** el validador del paso no informa incidencias

### Requirement: Secciones de la corrida del análisis estratégico
Cada corrida SHALL contener `secciones/1.5.md`, `1.6.md` y `1.7.md` con el encabezado `## <punto>. <título del índice>` como primera línea y solo texto final; cada una SHALL marcar su figura (`pestel`, `foda`, `ishikawa`) con `<!-- figura: <visual> -->` y tener `visuales/<visual>.html` y `leer-imagen/<visual>.md` en la misma corrida.

#### Scenario: Corrida completa
- **WHEN** la skill termina sin incidencias
- **THEN** la corrida tiene las tres secciones, los tres visuales con su explicación, `referencias.md` y `README.md`

### Requirement: PESTEL con efecto y fuente
La sección 1.5 SHALL tener al menos un hallazgo por cada factor (político, económico, social, tecnológico, ecológico y legal), cada uno con código (`POL`, `ECO`, `SOC`, `TEC`, `AMB`, `LEG`), hallazgo, efecto en el negocio, tipo (Oportunidad o Amenaza) y fuente con su año.

#### Scenario: Factor sin hallazgo
- **WHEN** la tabla PESTEL no tiene ningún hallazgo ecológico
- **THEN** el validador informa el factor que falta

#### Scenario: Hallazgo sin fuente
- **WHEN** un hallazgo no tiene fuente
- **THEN** el validador lo informa por su código

### Requirement: FODA con evidencia
La sección 1.6 SHALL tener los cuatro cuadros (`FOR`, `DEB`, `OPO`, `AME`), cada ítem con código y evidencia o fuente, y cada oportunidad o amenaza SHALL citar un hallazgo PESTEL o una fuente.

#### Scenario: Oportunidad sin respaldo externo
- **WHEN** una oportunidad no cita un código PESTEL ni una fuente
- **THEN** el validador la informa

### Requirement: Estrategias cruzadas
La sección 1.6 SHALL incluir al menos una estrategia de cada tipo (FO, FA, DO y DA), con código del tipo (`FO-nn`, `FA-nn`, `DO-nn`, `DA-nn`), y cada una SHALL combinar ítems FODA existentes del cuadro interno y externo que su tipo indica.

#### Scenario: Estrategia mal combinada
- **WHEN** una estrategia FO combina una debilidad
- **THEN** el validador informa que una estrategia FO combina fortalezas con oportunidades

### Requirement: Ishikawa de la problemática
La sección 1.7 SHALL declarar como efecto el problema principal del brief vigente y SHALL agrupar al menos seis causas con código `CAU-nn` y evidencia en al menos cuatro categorías 6M (Método, Mano de obra, Materiales, Maquinaria, Medición y Medio ambiente).

#### Scenario: Efecto distinto del brief
- **WHEN** el efecto del Ishikawa no coincide con el problema principal del brief
- **THEN** el validador lo informa y remite a `01-make-project-brief-update` o a corregir el efecto

#### Scenario: Categoría desconocida
- **WHEN** una causa usa una categoría fuera de las 6M
- **THEN** el validador la informa con las categorías válidas

### Requirement: Validación del análisis estratégico
El validador del paso SHALL comprobar encabezados, figuras, códigos citados sin definir, PESTEL, FODA, estrategias cruzadas, Ishikawa, el marcador de datos modelados y las citas contra `referencias.md`, e informar cada incidencia con archivo y causa.

#### Scenario: Código citado sin definir
- **WHEN** una estrategia combina `OPO-07` y esa oportunidad no existe
- **THEN** el validador informa el código

### Requirement: Skill 04-make-strategic-analysis-update
La skill `04-make-strategic-analysis-update` SHALL bifurcar la corrida vigente, editar solo las secciones afectadas, renumerar sin reutilizar códigos, reconstruir los visuales de las secciones cambiadas, validar, registrar e indicar con `references/dependencias.md` qué skills `-update` siguen.

#### Scenario: Se elimina una causa
- **WHEN** el usuario elimina `CAU-04`
- **THEN** el código no se reutiliza, se reconstruye el visual `ishikawa` y la skill sugiere `05-make-problem-objectives-update` si la matriz lo citaba
