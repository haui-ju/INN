## MODIFIED Requirements

### Requirement: Criterios de pivotar o perseverar
El punto 3.2.4 SHALL fijar para cada hipótesis, antes de ejecutar los experimentos, cuándo se persevera, cuándo se itera y cuándo se pivota, con umbrales numéricos contiguos que no dejen huecos ni se solapen, y SHALL dejar la decisión final para los resultados (punto de `17-make-lean-results`).

#### Scenario: Hipótesis sin criterio
- **WHEN** una `HIP` no aparece en la tabla de criterios
- **THEN** la validación lo informa

#### Scenario: Hueco entre umbrales
- **WHEN** una hipótesis persevera con 90 % o más, pivota con menos de 60 % y no define qué ocurre entre 60 % y 90 %
- **THEN** la validación informa la hipótesis y el tramo sin criterio

#### Scenario: Zonas que se solapan
- **WHEN** una hipótesis persevera con 70 % o más e itera entre 60 % y 75 %
- **THEN** la validación informa el solape
