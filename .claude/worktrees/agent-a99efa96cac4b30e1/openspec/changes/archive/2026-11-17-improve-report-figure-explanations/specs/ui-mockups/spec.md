## MODIFIED Requirements

### Requirement: Explicación de cada imagen
La skill SHALL escribir `leer-imagen/<UI-nn>.md` y `leer-imagen/galeria.md` derivados solo de `pantallas.json`, con una explicación de 2 a 3 frases que diga para qué sirve la pantalla en el recorrido del usuario, qué historias y requerimientos resuelve con su `PAN` de origen y qué cambió (la conclusión, no un listado de sus elementos), y por qué se destaca la acción principal; la galería SHALL indicar cuántas pantallas se conservan, se modifican o son nuevas y por qué importa esa proporción.

#### Scenario: Pantalla modificada
- **WHEN** `UI-02` viene de `PAN-02` con destino «se modifica»
- **THEN** su explicación dice para qué sirve en el recorrido, cita `PAN-02` y explica qué cambió y por qué

#### Scenario: Galería
- **WHEN** la galería tiene 3 pantallas, de las cuales 2 se conservan y 1 es nueva
- **THEN** `leer-imagen/galeria.md` indica esa proporción y qué implica para el trabajo de interfaz
