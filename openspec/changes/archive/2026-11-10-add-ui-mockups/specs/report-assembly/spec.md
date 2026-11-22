## ADDED Requirements

### Requirement: Marcadores de pantallas finales
El armado SHALL poner en 5.3.2 el marcador de la galería de pantallas y en D.5 un marcador por cada `UI-nn`, con archivo sugerido `galeria-pantallas.png` y `<UI-nn>.png`, tomar el inventario de D.5 de `inventario-ui.md` de la corrida vigente de `14b-make-ui-mockups`, y copiar bajo cada marcador la explicación de `leer-imagen/` solo si coincide con `pantallas.json` y con la tabla `UI` vigentes.

#### Scenario: Galería en 5.3.2
- **WHEN** existe la corrida vigente de `14b-make-ui-mockups`
- **THEN** 5.3.2 lleva `(INCLUIR IMAGEN: Figura X: Pantallas finales (datos al DD-MM-AAAA). Archivo sugerido: galeria-pantallas.png.)` y su explicación

#### Scenario: Una imagen por pantalla en D.5
- **WHEN** la tabla `UI` tiene cuatro pantallas
- **THEN** D.5 lleva cuatro marcadores consecutivos, cada uno con el código de su pantalla en el pie

#### Scenario: Sin mockups
- **WHEN** el config no tiene corrida de `14b-make-ui-mockups`
- **THEN** 5.3.2 lleva su marcador sin explicación, D.5 queda en `faltantes.md` con ese paso como el que lo produce y el kit avisa que falta
