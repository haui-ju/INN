# Spec Delta

## Purpose

Define el contrato del índice maestro del informe (`common/structure/model1.md`): orden y numeración de capítulos, secciones estables que usan las skills, marcas de avance, historial de versiones, plantilla de avance y reglas de contenido para un documento que se actualiza en tres avances.

## ADDED Requirements

### Requirement: Orden y numeración de capítulos
El índice SHALL tener siete capítulos numerados de forma consecutiva, sin saltos ni números repetidos: 1 La empresa y el problema, 2 Marco metodológico, 3 Innovación, 4 Gestión ágil (lo planificado), 5 Desarrollo del sistema, 6 Resultados y avance (lo real) y 7 Conclusiones y recomendaciones, seguidos de Referencias y Anexos.

#### Scenario: Revisión de la numeración
- **WHEN** se revisan todos los títulos numerados del índice
- **THEN** cada número de capítulo, sección y subsección aparece una sola vez y la secuencia no tiene huecos

#### Scenario: Lo planificado separado de lo real
- **WHEN** se busca dónde va el Gantt y el tablero Kanban
- **THEN** su diseño y línea base están en el capítulo 4 y su avance real, en el capítulo 6

### Requirement: Design Thinking y Lean en el capítulo de innovación
El capítulo 3 SHALL contener Design Thinking en 3.1, Lean Startup en 3.2, Lean Change Management en 3.3 y el Lean Canvas validado en 3.4, mientras que el Lean Canvas inicial y los 5 porqués permanecen en el capítulo 1.

#### Scenario: Dos versiones del canvas
- **WHEN** se compara el modelo de negocio inicial con el validado
- **THEN** el inicial está en 1.3 como hipótesis y el validado en 3.4 con los hallazgos del Design Thinking que lo cambiaron

### Requirement: Secciones estables para las skills
El índice SHALL conservar los puntos `3.1.1` a `3.1.8` del Design Thinking y las letras de anexo B, D, E y F con sus subpuntos, porque las skills de generación los leen, los citan y los parchean por su numeración.

#### Scenario: Reordenamiento sin romper las skills
- **WHEN** se reordenan los demás capítulos
- **THEN** la numeración de 3.1.x y de los anexos B, D, E y F no cambia y las skills siguen encontrando sus puntos

### Requirement: Referencias cruzadas vigentes
Los textos del índice y los documentos generados SHALL citar los puntos del nuevo orden: requerimientos en 4.2, diseño de interfaz en 5.3 y pruebas del sistema en 5.5, y SHALL NOT citar puntos del orden anterior.

#### Scenario: Búsqueda de referencias antiguas
- **WHEN** se buscan `5.1`, `5.2.3` y `5.4.2` como referencias a capítulos del informe
- **THEN** no aparecen en el índice, en el generador ni en el paquete generado

### Requirement: Marcas de avance
Cada punto del índice SHALL llevar una marca `[A1]`, `[A2]` o `[A3]` con el avance en que se completa, y `+` (por ejemplo `[A1+]`) cuando se actualiza en avances posteriores, y el índice SHALL incluir una leyenda de estas marcas.

#### Scenario: Qué falta en un avance
- **WHEN** el equipo prepara el avance 2
- **THEN** los puntos marcados `[A2]` y los marcados con `+` de avances anteriores indican lo que hay que escribir o actualizar

### Requirement: Historial de versiones del documento
El índice SHALL incluir un historial de versiones con una fila por avance (versión, avance, fecha y cambios principales) para registrar las tres actualizaciones del documento.

#### Scenario: Registro de una actualización
- **WHEN** se entrega un avance
- **THEN** se completa la fila de ese avance con su fecha y los capítulos que cambiaron

### Requirement: Plantilla de avance
Los puntos 6.1, 6.2 y 6.3 SHALL tener los mismos nueve bloques: resumen, Gantt actualizado, incremento del sistema, tablero Kanban, Sprint Review, retrospectiva, pruebas, riesgos y cambios, y plan del siguiente avance, cada uno con una nota breve de qué pegar y qué texto escribir.

#### Scenario: Avance con la misma estructura
- **WHEN** se compara el punto 6.1 con el 6.3
- **THEN** ambos tienen los mismos nueve bloques en el mismo orden

### Requirement: Reglas de contenido de los avances
El índice SHALL declarar que el contenido no se repite entre avances (se cita la figura anterior), que lo extenso va a anexos, que toda captura lleva pie de foto con su código de trazabilidad y que toda cifra lleva su fecha.

#### Scenario: Captura ya mostrada
- **WHEN** una captura ya apareció en un avance anterior
- **THEN** el avance siguiente la cita por su número de figura en lugar de repetirla

### Requirement: Títulos sin notas de trabajo
Los títulos del índice SHALL ser limpios, sin erratas y sin decisiones de trabajo entre paréntesis; las decisiones pendientes SHALL registrarse en `apuntes.md`.

#### Scenario: Decisión sobre una herramienta
- **WHEN** el equipo aún no decide qué herramienta usar para el Gantt o el tablero Kanban
- **THEN** la decisión figura en `apuntes.md` y el título del índice solo nombra el contenido
