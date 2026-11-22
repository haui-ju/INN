## ADDED Requirements

### Requirement: Marca de imagen
El índice SHALL marcar con «(incluye imagen)», entre paréntesis en la línea del punto, cada punto que lleva una imagen: las de un visual HTML (1.2, 1.3.2, 3.1.2.2, 3.1.3.2, 3.1.4.2, 3.2.3, 3.2.4, 3.4, 4.1.1, 4.6.2, 4.7, 4.8, 6.N.2, 6.N.4, 6.4.1 a 6.4.3) y las que aporta el usuario (3.1.5.3, 5.3, 6.N.3, 6.N.5, 6.N.7, D.3), y `report.py` SHALL exponer esa marca por punto.

#### Scenario: Punto con visual
- **WHEN** se lee el punto 1.2 del índice
- **THEN** su línea incluye «(incluye imagen)» y `cargar_indice` lo devuelve con `imagen` verdadero

#### Scenario: Punto sin imagen
- **WHEN** se lee un punto de solo texto
- **THEN** no lleva la marca y `imagen` es falso
