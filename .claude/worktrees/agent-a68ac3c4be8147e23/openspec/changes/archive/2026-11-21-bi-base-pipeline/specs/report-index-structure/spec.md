# Spec Delta

## MODIFIED Requirements

### Requirement: Títulos sin notas de trabajo
Los títulos del índice SHALL ser limpios, sin erratas y sin decisiones de trabajo entre paréntesis; las decisiones pendientes SHALL registrarse en `apuntes.md`.

#### Scenario: Decisión sobre una herramienta
- **WHEN** el equipo aún no decide qué herramienta usar para el ETL
- **THEN** la decisión figura en `apuntes.md` y el título del índice solo nombra el contenido

### Requirement: Marca de imagen
El índice SHALL marcar con «(incluye imagen)», entre paréntesis en la línea del punto, cada punto que lleva una imagen: 1.4 (Business Model Canvas), 1.5 (PESTEL), 1.6 (FODA), 1.7 (Ishikawa), 2.2 (arquitectura), 2.4 (modelo de datos), 3.2 (dashboard) y 4 (visualizaciones del relato), y `report.py` SHALL exponer esa marca por punto.

#### Scenario: Punto con visual
- **WHEN** se lee el punto 1.6 del índice
- **THEN** su línea incluye «(incluye imagen)» y `cargar_indice` lo devuelve con `imagen` verdadero

#### Scenario: Punto sin imagen
- **WHEN** se lee un punto de solo texto, como 1.1
- **THEN** no lleva la marca y `imagen` es falso

## REMOVED Requirements

### Requirement: Design Thinking y Lean en el capítulo de innovación
**Reason**: Design Thinking y Lean salen del informe.
**Migration**: Ninguna; el diagnóstico estratégico vive en el capítulo 1.

### Requirement: Secciones estables para las skills
**Reason**: Los puntos 3.1.1 a 3.1.8 y los anexos B, D, E y F eran de Design Thinking, que se retira.
**Migration**: Las skills citan los puntos por su número en `pipeline.json`.

### Requirement: Referencias cruzadas vigentes
**Reason**: Las referencias al orden de siete capítulos dejan de existir.
**Migration**: Citar solo los puntos del índice de cinco capítulos.

### Requirement: Marcas de avance
**Reason**: Hay una sola entrega y no hay avances.
**Migration**: El avance del informe lo marca `informe.secciones` del config.

### Requirement: Historial de versiones del documento
**Reason**: Ya no hay tres avances ni versiones acumuladas.
**Migration**: Ninguna; el control del documento solo registra datos del equipo y la fecha.

### Requirement: Plantilla de avance
**Reason**: Los puntos 6.1 a 6.3 de avance desaparecen con los sprints.
**Migration**: Ninguna.

### Requirement: Reglas de contenido de los avances
**Reason**: Hablaba de avances; se reemplaza por reglas del informe único.
**Migration**: Ver «Reglas de contenido del informe».

### Requirement: Pantallas finales en el índice
**Reason**: Las pantallas de app se retiran del pipeline.
**Migration**: Las capturas del dashboard van en el punto 3.2.

### Requirement: Anexo G de detalle de tablas del informe
**Reason**: Dependía de bloques trasladables de Scrum y de diseño de sistema que se retiran.
**Migration**: Los anexos se definen en «Anexos del informe».

### Requirement: Bloques trasladables declarados en el índice
**Reason**: Los bloques trasladables (historias, casos de prueba, Gantt y glosario) se retiran.
**Migration**: Lo extenso va al anexo correspondiente.

### Requirement: Orden y numeración de capítulos
**Reason**: Se reemplaza por «Capítulos del informe de BI» porque cambian su texto y sus escenarios al pasar al pipeline de BI.
**Migration**: Usar el requisito «Capítulos del informe de BI».

## ADDED Requirements

### Requirement: Reglas de contenido del informe
El índice SHALL declarar que el contenido no se repite entre secciones (se cita la figura anterior), que lo extenso va a los anexos, que toda captura o figura lleva pie de foto y que toda cifra lleva su fecha o su fuente.

#### Scenario: Figura ya mostrada
- **WHEN** una figura ya apareció en una sección anterior
- **THEN** la sección siguiente la cita por su número de figura en lugar de repetirla

### Requirement: Anexos del informe
El índice SHALL incluir los anexos A Diccionario de datos y calidad de datos, B Scripts del ETL, C Medidas y cálculos del dashboard y D Especificación y capturas del dashboard, además de Referencias, y SHALL poder omitirlos del informe armado cuando su sección de origen está pendiente.

#### Scenario: Revisión de los anexos
- **WHEN** se revisan los títulos de los anexos
- **THEN** aparecen A a D una sola vez y en ese orden

#### Scenario: Anexo sin sección de origen
- **WHEN** la sección de origen de un anexo está pendiente
- **THEN** el informe armado omite el anexo y lo lista como faltante

### Requirement: Control del documento sin versiones
El índice SHALL abrir con un control del documento con los datos de la portada (título, empresa, integrantes, curso y fecha de entrega) sin historial de versiones ni marcas de avance.

#### Scenario: Control del documento
- **WHEN** se lee el inicio del índice
- **THEN** muestra los datos de la portada y no contiene una tabla de versiones por avance

### Requirement: Capítulos del informe de BI
El índice SHALL tener cinco capítulos numerados de forma consecutiva, sin saltos ni números repetidos: 1 Diagnóstico estratégico y análisis del negocio (1.1 a 1.10), 2 Diseño técnico de solución en Inteligencia de Negocios (2.1 a 2.5), 3 Construcción y calidad del dashboard en Power BI (3.1 y 3.2), 4 Storytelling con datos y 5 Conclusiones, recomendaciones y lecciones aprendidas, seguidos de Referencias y Anexos.

#### Scenario: Revisión de la numeración
- **WHEN** se revisan todos los títulos numerados del índice
- **THEN** cada número de capítulo, sección y subsección aparece una sola vez y la secuencia no tiene huecos

#### Scenario: Puntos del capítulo 1
- **WHEN** se lee el capítulo 1 del índice
- **THEN** lista 1.1 Nombre de la empresa, 1.2 Misión y visión, 1.3 Industria y tamaño, 1.4 Modelo de negocio (Business Model Canvas), 1.5 Análisis PESTEL, 1.6 Matriz FODA, 1.7 Diagrama de Ishikawa, 1.8 Problemática central, 1.9 Objetivo general y 1.10 Objetivos específicos

#### Scenario: Puntos de los capítulos 2 y 3
- **WHEN** se leen los capítulos 2 y 3
- **THEN** el 2 lista propuesta de solución, arquitectura (fuentes, ETL, almacenamiento y visualización), herramientas, modelado de datos (hechos, dimensiones y relaciones) y KPI, y el 3 lista la construcción del ETL y la del dashboard
