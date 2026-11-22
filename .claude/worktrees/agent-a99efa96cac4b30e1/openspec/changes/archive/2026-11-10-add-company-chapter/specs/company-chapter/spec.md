## Purpose
Define el capítulo 1 del informe (la empresa o el proyecto, su diagnóstico, objetivos, justificación y alcances): su playbook y modelos, las skills que lo generan y lo ajustan, su adaptación a proyectos con o sin empresa y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos del capítulo 1
El repositorio SHALL incluir `common/company/guia.md` (presentación, FODA, objetivos medibles, justificación, alcances y limitaciones, adaptación a proyecto propio, errores frecuentes, checklist y referencias citables) y `common/company/models/` con las plantillas `emp-1-presentacion.md`, `emp-2-diagnostico.md`, `emp-3-objetivos.md`, `emp-4-justificacion-alcance.md` y un `README.md`, cada una con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `03-make-company-chapter` va a escribir una sección
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Confirmación del tipo de proyecto
Al ejecutarse, la skill SHALL leer `proyecto.tipo` del config, mostrarlo al usuario y confirmar si el proyecto se aplica a una empresa o es propio, sin presuponer una empresa; si el usuario lo corrige, SHALL proponer `00-init-update` y no continuar con el dato anterior.

#### Scenario: Tipo correcto
- **WHEN** el config indica `empresa` y el usuario lo confirma
- **THEN** la skill continúa con los datos de `project/domain.md`

#### Scenario: Tipo desactualizado
- **WHEN** el config indica `empresa` y el usuario dice que el proyecto es propio
- **THEN** la skill propone ejecutar `00-init-update` antes de generar el capítulo

### Requirement: Fuentes y datos modelados
La skill SHALL tomar del config, de `project/domain.md` y del canvas v0 vigente todo lo que ya conste, preguntar solo lo que falte, y antes de escribir SHALL mostrar qué secciones salen de datos marcados «(modelado por el agente, …)» en `domain.md` y permitir al usuario reemplazarlos.

#### Scenario: Misión modelada
- **WHEN** la misión de `domain.md` está marcada como modelada
- **THEN** la skill lo informa y pregunta si el usuario aporta la misión real o conserva la propuesta

#### Scenario: Sin canvas
- **WHEN** no existe corrida del canvas inicial
- **THEN** la skill avisa que falta `02-make-initial-lean-canvas` y pregunta si continúa sin el punto 1.3

### Requirement: Plan y confirmación antes de escribir
La skill SHALL presentar un resumen del capítulo (tipo de proyecto, secciones, cantidad de ítems del FODA y de objetivos, fuentes de cada sección) y esperar la confirmación del usuario antes de crear archivos.

#### Scenario: Cantidad de objetivos
- **WHEN** el usuario pide seis objetivos específicos
- **THEN** la skill avisa que el rango de referencia es de tres a cinco y respeta su decisión

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/company-chapter/<DD-MM-AAAA-HH-MM-SS>/` con `capitulo-1.md`, `bloques/` (un archivo por modelo) y `README.md`, y SHALL registrarla en el paso `03-make-company-chapter` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene `capitulo-1.md` con los puntos 1.1 a 1.6, los bloques y el `README.md`, y el config la registra

### Requirement: Adaptación a proyecto propio
Con `tipo: propio`, el capítulo SHALL conservar la numeración 1.1 a 1.6, titular 1.1 «Presentación del proyecto» y adaptar sus subpuntos (origen, propósito, visión y valores), y SHALL NOT mencionar una empresa que no existe.

#### Scenario: Proyecto sin empresa
- **WHEN** el config indica `tipo: propio`
- **THEN** 1.1 describe el proyecto, su origen y propósito, y el diagnóstico se centra en el entorno del problema

### Requirement: Diagnóstico con códigos
El diagnóstico SHALL separar el microentorno (fortalezas `FOR-nn` y debilidades `DEB-nn`) del macroentorno (oportunidades `OPO-nn` y amenazas `AME-nn`), cada ítem con su evidencia o fuente, y SHALL citar solo códigos definidos.

#### Scenario: Ítem sin evidencia
- **WHEN** una debilidad no indica fuente ni evidencia
- **THEN** la validación lo informa

### Requirement: Objetivos medibles y trazables
El capítulo SHALL definir un objetivo general `OG-01` y objetivos específicos `OE-nn`, cada uno con verbo, qué se logra, métrica, meta y plazo (alineado con las fechas de los avances), y cada `OE` SHALL indicar a qué `OG` aporta.

#### Scenario: Objetivo sin métrica
- **WHEN** un `OE` no tiene métrica ni meta
- **THEN** la validación informa el código y la causa

#### Scenario: Evaluación posterior
- **WHEN** el análisis final evalúa el cumplimiento
- **THEN** encuentra cada `OE` definido con su métrica en este capítulo

### Requirement: Coherencia con el canvas inicial
El punto 1.3 SHALL reproducir sin modificar los puntos 1.3.1 y 1.3.2 de la corrida vigente del canvas inicial, y el problema del capítulo SHALL coincidir con el problema principal `PRB-01` del canvas.

#### Scenario: Canvas modificado
- **WHEN** el canvas vigente cambia después de generar el capítulo
- **THEN** la validación informa que 1.3 ya no coincide

### Requirement: Validación del capítulo 1
La validación SHALL comprobar las secciones 1.1 a 1.6, los códigos del FODA y de los objetivos, la medibilidad de los objetivos, la coherencia con el canvas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Sección ausente
- **WHEN** falta el punto 1.6
- **THEN** la validación informa el archivo y la sección

### Requirement: Procedencia solo en el README
El capítulo y sus bloques SHALL copiar los datos de `domain.md` sin el marcador «(modelado por el agente, …)», y el `README.md` de la corrida SHALL registrar qué secciones salieron de datos modelados como única mención de procedencia.

#### Scenario: Dato modelado
- **WHEN** la visión proviene de un dato modelado
- **THEN** el texto del capítulo no lo marca y el `README.md` lista «visión» entre las secciones modeladas

### Requirement: Skill 03-make-company-chapter-update
La skill `03-make-company-chapter-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (dato de la empresa o del proyecto, ítem del FODA, objetivo, justificación o alcance), mostrar el plan con los archivos y citas afectados, esperar confirmación, editar solo lo afectado y validar.

#### Scenario: Cambio de un objetivo específico
- **WHEN** el usuario cambia la meta de `OE-02`
- **THEN** la copia actualiza el bloque de objetivos, `capitulo-1.md` y las citas de `OE-02`, y deja el resto idéntico a la base

#### Scenario: Objetivo evaluado en otra corrida
- **WHEN** el usuario quita `OE-03` y el análisis final lo cita
- **THEN** la skill lo avisa en el plan y no modifica esa corrida

### Requirement: Texto limpio en el capítulo
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Dato de ejemplo
- **WHEN** el capítulo describe la reseña de la empresa
- **THEN** usa contenido realista sin etiquetas de procedencia
