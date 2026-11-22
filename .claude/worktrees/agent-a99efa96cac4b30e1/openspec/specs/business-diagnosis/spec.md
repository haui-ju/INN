# business-diagnosis Specification

## Purpose
Produce las secciones 1.1 a 1.4 del informe de BI (empresa, misión y visión, industria y tamaño, y Business Model Canvas) con la skill `03-make-business-diagnosis` y su `-update`, a partir de `domain.md` y del brief.

## Requirements

### Requirement: Playbook y modelos del diagnóstico del negocio
El repositorio SHALL incluir `common/03-business-diagnosis/guia.md` (fuentes, reglas, tamaño por UIT, Canvas, errores y checklist) y `common/03-business-diagnosis/models/` con un `README.md` y una plantilla por sección (1.1 a 1.4), cada una con ficha, instrucciones para el agente, formato, ejemplo y checklist.

#### Scenario: La skill lee el playbook
- **WHEN** se ejecuta `03-make-business-diagnosis`
- **THEN** lee la guía y las plantillas antes de preguntar o escribir

#### Scenario: El ejemplo de cada plantilla valida
- **WHEN** se arma una corrida con los ejemplos de las cuatro plantillas
- **THEN** el validador del paso no informa incidencias

### Requirement: Fuentes del diagnóstico del negocio
La skill SHALL tomar el nombre, la reseña, la misión, la visión, la industria y el tamaño de `project/domain.md` y el tema y la problemática del brief vigente, SHALL preguntar solo lo que falte y SHALL mostrar un plan y esperar la confirmación antes de escribir.

#### Scenario: Dato modelado en domain.md
- **WHEN** una sección de `domain.md` lleva el marcador «(modelado por el agente, …)»
- **THEN** la skill pregunta si el usuario aporta el dato real, el texto del informe va sin el marcador y la procedencia queda solo en el `README.md`

#### Scenario: Misión copiada de domain.md
- **WHEN** `domain.md` tiene una misión o una visión
- **THEN** la sección 1.2 la reproduce sin reescribirla y el validador informa si difiere

### Requirement: Secciones de la corrida del diagnóstico del negocio
Cada corrida SHALL contener `secciones/1.1.md`, `1.2.md`, `1.3.md` y `1.4.md`, cada una con el encabezado `## <punto>. <título del índice>` como primera línea y solo texto final del informe; la 1.4 SHALL marcar la figura con la línea `<!-- figura: bmc -->`, con `visuales/bmc.html` y `leer-imagen/bmc.md` en la misma corrida; `referencias.md` y `README.md` completan la corrida.

#### Scenario: Encabezado distinto del índice
- **WHEN** `secciones/1.3.md` empieza con otro título
- **THEN** el validador informa el archivo y el encabezado esperado

#### Scenario: Figura sin visual
- **WHEN** la sección 1.4 marca la figura `bmc` y falta `visuales/bmc.html` o `leer-imagen/bmc.md`
- **THEN** el validador informa cuál falta

### Requirement: Datos de la empresa
La sección 1.1 SHALL tener una tabla con razón social, nombre comercial, RUC, actividad económica y ubicación, y una reseña; con `tipo: empresa` el RUC SHALL coincidir con el del config y con `tipo: propio` SHALL decir «No aplica».

#### Scenario: RUC distinto del config
- **WHEN** la tabla de 1.1 trae un RUC distinto de `proyecto.ruc`
- **THEN** el validador lo informa

### Requirement: Tamaño según la Ley 30056
La sección 1.3 SHALL describir sector, actividad económica, tipo de cliente y entorno competitivo, y SHALL calcular el tamaño con las ventas anuales, la UIT de referencia, las ventas en UIT y la categoría de la Ley 30056 (micro hasta 150 UIT, pequeña hasta 1700, mediana hasta 2300 y gran empresa por encima).

#### Scenario: Categoría incoherente
- **WHEN** las ventas equivalen a 436 UIT y la categoría dice «Mediana empresa»
- **THEN** el validador informa que corresponde «Pequeña empresa»

#### Scenario: Cálculo en UIT erróneo
- **WHEN** las ventas en UIT difieren en más de una unidad de ventas anuales entre la UIT
- **THEN** el validador lo informa con el valor esperado

### Requirement: Business Model Canvas de nueve bloques
La sección 1.4 SHALL presentar los nueve bloques del Canvas (segmentos de clientes, propuesta de valor, canales, relaciones con clientes, fuentes de ingresos, recursos clave, actividades clave, socios clave y estructura de costos), cada uno con contenido, y una lectura que relacione el modelo con la problemática.

#### Scenario: Falta un bloque
- **WHEN** la tabla del Canvas no tiene «Socios clave»
- **THEN** el validador informa el bloque que falta

### Requirement: Validación del diagnóstico del negocio
El validador del paso SHALL comprobar encabezados, figuras, datos de la empresa, misión y visión, tamaño, Canvas, que no se copie el marcador de datos modelados y que cada cita en texto tenga su entrada en `referencias.md`, e informar cada incidencia con archivo y causa.

#### Scenario: Cita sin referencia
- **WHEN** 1.4 cita (Osterwalder & Pigneur, 2010) y `referencias.md` no la tiene
- **THEN** el validador informa la cita sin referencia

### Requirement: Skill 03-make-business-diagnosis-update
La skill `03-make-business-diagnosis-update` SHALL bifurcar la corrida vigente, editar solo las secciones afectadas por el cambio pedido, volver a construir el visual si cambió el Canvas, validar, registrar e indicar con `references/dependencias.md` qué skills `-update` siguen.

#### Scenario: Cambio de un bloque del Canvas
- **WHEN** el usuario cambia los canales del Canvas
- **THEN** el fork cambia solo `secciones/1.4.md`, el visual `bmc` y el `README.md`, y la skill sugiere `05-make-problem-objectives-update` si la matriz cita ese bloque
