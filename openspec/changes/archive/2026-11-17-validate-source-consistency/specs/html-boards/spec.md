## MODIFIED Requirements

### Requirement: Datos y estado real
`data.json` SHALL contener `schema`, `proyecto`, `fecha_corte`, `diseno`, la línea base copiada sin cambios (`gantt` y `tablero`), el `estado` real (por tarea: avance de 0 a 100 y fechas reales; por tarjeta: columna y fechas de entrada a la primera columna de trabajo y de llegada a la final) y lo `calculado`, y SHALL coincidir con el plan y el tablero vigentes; una tarea con avance 100 SHALL tener todas sus predecesoras con avance 100 y fechas reales anteriores o iguales.

#### Scenario: Línea base desalineada
- **WHEN** el plan vigente tiene una tarea que `data.json` no incluye
- **THEN** la validación informa el código y que hay que resincronizar con el `-update`

#### Scenario: Estado incoherente
- **WHEN** una tarea tiene avance 100 y su tarjeta no está en la columna final
- **THEN** la validación informa la tarea y la tarjeta

#### Scenario: Tarea terminada con predecesora pendiente
- **WHEN** `TAR-37` tiene avance 100 y su predecesora `TAR-42` tiene avance 0
- **THEN** la validación informa las dos tareas y que el estado de la entrega no es coherente con su predecesora
