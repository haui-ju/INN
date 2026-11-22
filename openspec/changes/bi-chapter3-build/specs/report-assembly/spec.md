# Spec Delta

## ADDED Requirements

### Requirement: Marcadores de captura
Cada línea `<!-- captura: <id> -->` de una sección SHALL reemplazarse por `(INCLUIR IMAGEN: Figura N: <pie>. Archivo sugerido: <ruta relativa al archivo>)` y una línea «Cómo copiarla» hacia el archivo, numerada junto con las figuras. El archivo SHALL salir de `capturas/<id>.png` de la corrida de la sección y SHALL NOT copiarse al informe: el marcador y `imagenes/INDICE.md` enlazan a él. El pie SHALL salir de `capturas/<id>.md` o, si falta, del título de la sección.

#### Scenario: Captura presente
- **WHEN** la sección 3.2 marca `<!-- captura: pagina-ventas -->` y la corrida trae `capturas/pagina-ventas.png`
- **THEN** el informe trae el marcador numerado como figura con el enlace a la captura, la lista en `imagenes/INDICE.md` y no agrega ningún archivo de imagen a la corrida del informe

#### Scenario: Captura ausente
- **WHEN** la marca `<!-- captura: pagina-ventas -->` no tiene su archivo
- **THEN** el marcador queda, el armado avisa el archivo que falta y la skill que lo produce

### Requirement: Sección con imagen cubierta por capturas
Una sección con la marca «(incluye imagen)» en el índice SHALL considerarse con imagen cuando trae al menos una figura o una captura, y SHALL avisarse solo cuando no trae ninguna.

#### Scenario: Sección con solo capturas
- **WHEN** la sección 3.2 trae capturas y ninguna figura generada
- **THEN** el armado no avisa que falta la imagen
