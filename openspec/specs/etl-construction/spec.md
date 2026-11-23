# etl-construction Specification

## Purpose
Define la skill `08-make-etl` y su `-update`, que preparan el trabajo del equipo (diccionario de datos y guía de Power Query), verifican la evidencia que este trae y redactan la sección 3.1 del informe y los anexos A y B, sin ejecutar nada en Power BI ni inventar resultados.

## Requirements

### Requirement: Playbook y modelos del ETL
El repositorio SHALL incluir `common/08-etl/guia.md` (extracción, transformación, reglas de calidad, carga, evidencia a conservar y errores frecuentes) y `common/08-etl/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `08-make-etl` va a escribir una sección o un anexo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

### Requirement: Fuentes de la skill del ETL
La skill SHALL leer el brief vigente (fuentes y objetivos), la corrida vigente de `06-make-bi-solution` (componentes de ETL y herramientas) y la de `07-make-data-model-kpi` (`modelo.json`), y SHALL avisar sin bloquear cuando falte alguna.

#### Scenario: Sin modelo
- **WHEN** no hay corrida vigente de `07-make-data-model-kpi`
- **THEN** la skill avisa que falta el modelo y no continúa, porque no puede definir las tablas de destino

### Requirement: Diccionario de datos de las fuentes y del modelo
La skill SHALL entregar un diccionario con cada tabla de entrada y de destino, sus campos, tipos, su regla de calidad asociada y su correspondencia con una tabla del modelo, y cada tabla y campo del modelo SHALL tener al menos un origen o un cálculo declarado.

#### Scenario: Campo del modelo sin origen
- **WHEN** un campo de `modelo.json` no tiene origen ni cálculo en el diccionario
- **THEN** la validación informa el campo y la tabla

### Requirement: Reglas de calidad trazadas
La sección 3.1 SHALL definir cada regla de calidad `REG-nn` con el defecto que trata, la tabla donde se aplica y el criterio de aceptación, y toda regla SHALL tener un número de registros afectados declarado en la evidencia.

#### Scenario: Regla sin evidencia
- **WHEN** una regla `REG-nn` no tiene cifras de filas antes y después
- **THEN** la validación informa la regla

#### Scenario: Defecto sin regla
- **WHEN** la hoja de respuestas lista un tipo de defecto que ninguna regla trata
- **THEN** la skill informa el defecto y la regla que falta

### Requirement: Guía paso a paso para el equipo
La skill SHALL entregar una guía ordenada de pasos `PAS-nn` en Power Query (importar, tipar, depurar, homologar, anexar, calcular y cargar) con el código propuesto para pegar, y SHALL decir explícitamente que lo ejecuta el equipo.

#### Scenario: Paso con código
- **WHEN** la guía describe un paso
- **THEN** indica la tabla, el resultado esperado y el código propuesto, y no afirma que el paso se ejecutó

### Requirement: Guía explicada con puntos de control
La guía para el equipo SHALL estar escrita para los archivos del caso: por cada fuente, qué columnas tiene, qué defectos trae y cuántos (según la hoja de respuestas), por qué se tratan, cómo se tratan y cuántas filas deben quedar después de cada paso como punto de control, y SHALL explicar cómo se calculan el costo estimado y el costo operativo.

#### Scenario: Punto de control
- **WHEN** el equipo termina un paso de la guía
- **THEN** la guía le dice cuántas filas debería tener la tabla y por qué, de modo que una diferencia revele el paso que falló

#### Scenario: Defecto explicado
- **WHEN** la guía trata un tipo de defecto
- **THEN** dice qué es, cuántos registros afecta en cada fuente, qué pasaría si no se trata y cómo se corrige

### Requirement: Evidencia que aporta el equipo
Antes de redactar, la skill SHALL pedir al equipo la evidencia del trabajo hecho (filas antes y después de cada regla, los scripts finales y las capturas), SHALL guardarla en la corrida y SHALL redactar solo con ella.

#### Scenario: Sin evidencia
- **WHEN** el equipo aún no entregó la evidencia
- **THEN** la skill entrega solo los materiales del equipo y deja 3.1 y los anexos sin escribir

#### Scenario: Cifra sin origen
- **WHEN** 3.1 cita una cantidad de filas que no está en la evidencia
- **THEN** la validación informa la cifra

### Requirement: Verificación contra la hoja de respuestas
La skill SHALL comparar los totales que entrega el equipo con `data/respuestas/` e informar por tabla la diferencia, y SHALL registrar en 3.1 el resultado de la comparación sin ocultar las diferencias.

#### Scenario: Totales distintos
- **WHEN** las ventas de un mes cargadas por el equipo difieren de lo esperado
- **THEN** la skill informa el mes, el desvío y la regla probable que lo causa antes de redactar

### Requirement: Sección 3.1 y anexos A y B
La corrida SHALL escribir `secciones/3.1.md` (extracción, transformación, reglas de calidad, carga y declaración de datos generados), `anexos/A.md` (tablas, campos, tipos, reglas y resultados de calidad) y `anexos/B.md` (los scripts o pasos completos del equipo), con títulos de tabla `Tabla N: …` y sin marcado de procedencia.

#### Scenario: Corrida completa
- **WHEN** la skill termina con evidencia
- **THEN** la corrida trae las tres piezas, el validador no informa incidencias y `12-make-report` incluye 3.1 y los anexos A y B

### Requirement: Registro y actualización
La skill SHALL registrar la sección 3.1 con `register` y SHALL tener una homóloga `08-make-etl-update` que copia la corrida vigente como «-fork», cambia solo lo pedido (una regla, un paso, una cifra de evidencia o el volumen de datos) y deja el resto idéntico.

#### Scenario: Corregir una cifra
- **WHEN** el equipo corrige las filas descartadas de una regla
- **THEN** el fork cambia 3.1 y el anexo A, y deja idéntico el anexo B si el script no cambió

#### Scenario: Regenerar los datos
- **WHEN** el usuario pide más volumen o otra semilla
- **THEN** el fork regenera `data/` y marca como desactualizada la evidencia anterior hasta que el equipo repita el ETL
