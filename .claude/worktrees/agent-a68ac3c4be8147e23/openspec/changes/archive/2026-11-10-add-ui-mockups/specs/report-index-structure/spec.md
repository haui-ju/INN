## MODIFIED Requirements

### Requirement: Marca de imagen
El índice SHALL marcar con «(incluye imagen)», entre paréntesis en la línea del punto, cada punto que lleva una imagen: las de un visual HTML (1.2, 1.3.2, 3.1.2.2, 3.1.3.2, 3.1.4.2, 3.2.3, 3.2.4, 3.4, 4.1.1, 4.6.2, 4.7, 4.8, 5.3.2, 6.N.2, 6.N.4, 6.4.1 a 6.4.3, D.5) y las que aporta el usuario (3.1.5.3, 6.N.3, 6.N.5, 6.N.7, D.3), y `report.py` SHALL exponer esa marca por punto.

#### Scenario: Punto con visual
- **WHEN** se lee el punto 1.2 del índice
- **THEN** su línea incluye «(incluye imagen)» y `cargar_indice` lo devuelve con `imagen` verdadero

#### Scenario: Punto sin imagen
- **WHEN** se lee un punto de solo texto, como 5.3.1
- **THEN** no lleva la marca y `imagen` es falso

## ADDED Requirements

### Requirement: Pantallas finales en el índice
El índice SHALL dividir 5.3 en 5.3.1 Destino de las pantallas del prototipo y 5.3.2 Pantallas finales, ambos con la marca de avance de 5.3, y SHALL agregar el anexo D.5 Inventario de pantallas finales, sin modificar el orden ni la numeración de los demás puntos.

#### Scenario: Revisión de la numeración
- **WHEN** se revisan los títulos numerados del índice
- **THEN** 5.3.1 y 5.3.2 aparecen una sola vez bajo 5.3 y D.5 sigue a D.4, sin saltos
