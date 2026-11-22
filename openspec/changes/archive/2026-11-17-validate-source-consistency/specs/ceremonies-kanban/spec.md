## MODIFIED Requirements

### Requirement: Duraciones y fechas de las ceremonias
Las duraciones SHALL no superar los topes de la Guía de Scrum para un sprint de un mes (Planning 8 horas, Daily 15 minutos, Review 4 horas, Retrospective 3 horas); la Planning SHALL caer en el inicio de su sprint, y la Review y la Retrospective dentro de su sprint, la Retrospective no antes que la Review. Ninguna ceremonia SHALL solaparse en horario con otra del mismo día, incluida la Daily Scrum, y las fechas fijas de las ceremonias SHALL caer en día hábil (de lunes a viernes).

#### Scenario: Daily de una hora
- **WHEN** la Daily Scrum dura 60 minutos
- **THEN** la validación informa la duración y el tope

#### Scenario: Retrospective antes de la Review
- **WHEN** la Retrospective del sprint 2 es anterior a su Review
- **THEN** la validación informa las dos fechas

#### Scenario: Planning y Daily en el mismo horario
- **WHEN** la Planning del primer día va de 19:00 a 21:00 y la Daily se fija a las 19:30 ese día
- **THEN** la validación informa las dos ceremonias y el tramo que se solapa

#### Scenario: Ceremonia en fin de semana
- **WHEN** la Planning del sprint 3 cae en domingo
- **THEN** la validación informa la fecha y el día de la semana
