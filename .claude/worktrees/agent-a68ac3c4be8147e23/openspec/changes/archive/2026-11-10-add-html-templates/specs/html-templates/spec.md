## Purpose
Define la biblioteca de plantillas HTML del proyecto (`common/html/`): plantillas autónomas ya hechas (React, Tailwind y componentes al estilo shadcn/ui compilados a un archivo) con el estilo del sistema de diseño, que se copian sustituyendo solo los tokens y los datos, con botones para obtener la imagen del visual, su `mock.json` y `README.md`, y el script que las copia y comprueba.

## ADDED Requirements

### Requirement: Biblioteca de plantillas
El repositorio SHALL incluir `common/html/` con un `DESIGN.md` de reglas visuales, un `README.md` del contrato, una carpeta `_build/` con las fuentes y la compilación y una carpeta por visual con `index.html`, `README.md` y `mock.json`; cada `index.html` SHALL compilarse a un único archivo autónomo, estar versionado y figurar con su huella en un manifiesto de sincronía.

#### Scenario: Plantilla desactualizada
- **WHEN** una fuente de `_build/` cambia y el `index.html` de un visual no se recompiló
- **THEN** la prueba de sincronía informa el visual sin necesitar `node`

#### Scenario: Carpeta de un visual
- **WHEN** se revisa `common/html/gantt/`
- **THEN** contiene `index.html`, `README.md` y `mock.json`

### Requirement: Pila y estilo de las plantillas
Las plantillas SHALL usar React, Tailwind y componentes al estilo shadcn/ui cuyo tema lee las variables CSS de los tokens, con titulares en una serif abierta, texto en una sans y códigos en monoespaciada incrustadas en el archivo, acento naranja, neutros cálidos y tema claro por defecto, según `DESIGN.md`; el usuario final SHALL NOT necesitar `node` para usarlas.

#### Scenario: Cambio de sistema de diseño
- **WHEN** se copia una plantilla con los tokens de otro sistema de diseño
- **THEN** los componentes adoptan sus colores, tipografía y radios sin recompilar

#### Scenario: Tema por defecto
- **WHEN** se abre una plantilla en un navegador con preferencia de tema oscuro
- **THEN** se muestra en tema claro y el botón de tema permite pasar al oscuro

### Requirement: Contrato de la plantilla
Cada plantilla SHALL ser un único archivo sin recursos externos con exactamente dos bloques sustituibles, el de tokens (variables CSS) y el de datos (JSON embebido), con tema claro y oscuro, adaptación a teléfono sin desplazamiento horizontal de la página, un aviso `<noscript>` y la fecha de corte («al DD-MM-AAAA» o «Línea base») destacada dentro del área de captura cuando el visual tiene fecha.

#### Scenario: Recurso externo en una plantilla
- **WHEN** una plantilla carga un script, una hoja de estilos o una fuente por URL
- **THEN** la prueba de plantillas informa el recurso

### Requirement: Modelo puro de datos
Cada visual SHALL calcular lo que muestra con un modelo puro, sin React ni DOM, que recibe los datos, da formato a los indicadores de `calculado` sin recalcularlos y devuelve un estado vacío «Sin datos» cuando faltan datos, y la vista SHALL limitarse a pintar ese modelo.

#### Scenario: Datos vacíos
- **WHEN** se procesa la versión vaciada del `mock.json` de una plantilla
- **THEN** el resultado indica «Sin datos» y no produce error

#### Scenario: Indicador distinto del cálculo
- **WHEN** `calculado` indica 4 tareas hechas
- **THEN** el visual muestra 4 y no las recuenta

### Requirement: Botones de imagen
Toda plantilla SHALL llevar los botones «Copiar imagen» y «Descargar imagen» y un selector de escala ×2, ×3 y ×4 (×2 por defecto, recordando la última elección), SHALL excluir los botones de la imagen, SHALL nombrar el archivo `<visual>-<fecha de corte>.png` (`<visual>.png` si no hay fecha) y SHALL descargar con un aviso visible cuando no pueda copiar al portapapeles.

#### Scenario: Navegador sin acceso al portapapeles
- **WHEN** el usuario pulsa «Copiar imagen» y el navegador no lo permite
- **THEN** se descarga el PNG y se muestra un aviso de que se descargó

#### Scenario: Escala elegida
- **WHEN** el usuario elige ×3 y descarga
- **THEN** el PNG tiene tres veces el ancho y el alto del área de captura

### Requirement: Imagen sin generación en el kit
El kit SHALL NOT generar imágenes: el PNG lo produce el navegador del usuario al pulsar los botones, y la función que arma el SVG de la captura SHALL ser pura y estar probada.

#### Scenario: Skill que entrega tableros
- **WHEN** una skill termina de copiar un HTML
- **THEN** indica al usuario que obtenga la imagen con los botones y no entrega ningún PNG

### Requirement: Mock con datos de ejemplo y README
Cada plantilla SHALL tener un `mock.json` con datos de ejemplo y el esquema completo, que son los que muestra `index.html` al abrirse, y un `README.md` que indica qué se cambia (solo los bloques de tokens y de datos), qué no se toca, el esquema, cómo obtener la imagen y los límites del navegador.

#### Scenario: Mock válido
- **WHEN** se carga el `mock.json` de una plantilla
- **THEN** es JSON válido con el esquema de datos del visual y datos de ejemplo

### Requirement: Versión vacía del mock
El kit SHALL ofrecer `html_tpl.py limpiar`, que devuelve el mock con las mismas claves y sin contenido, y una skill SHALL partir siempre de esa versión vacía y nunca usar los datos de ejemplo como datos del proyecto.

#### Scenario: Versión vacía
- **WHEN** se ejecuta `html_tpl.py limpiar` sobre una plantilla
- **THEN** el resultado tiene las mismas claves que el mock, sin contenido, y la plantilla lo muestra como «Sin datos»

#### Scenario: Skill que rellena una plantilla
- **WHEN** una skill prepara los datos de un tablero
- **THEN** parte de la versión vacía y la completa con los datos reales

### Requirement: Script de copia y comprobación
El kit SHALL incluir `html_tpl.py` con `copiar`, que copia una plantilla sustituyendo solo el bloque de tokens (por los del sistema de diseño vigente o los base) y el de datos, y `comprobar`, que verifica el manifiesto de sincronía, y `boards.py render` y `render_preview.py` SHALL usarlo.

#### Scenario: Copia sin otros cambios
- **WHEN** se copia la plantilla `gantt` con unos datos y unos tokens
- **THEN** el resultado es idéntico a la plantilla salvo el bloque de tokens y el de datos

#### Scenario: Sin sistema de diseño
- **WHEN** `diseno` está vacío
- **THEN** la copia usa los tokens base y lo avisa

### Requirement: Plantillas iniciales
La biblioteca SHALL incluir las plantillas `gantt`, `kanban` y `vista-previa` con el mismo contenido que los HTML que hoy se generan y el estilo de `DESIGN.md`: el Gantt con sprints, barras con avance real, hitos, predecesoras, responsable, historia y marca de corte; el Kanban con columnas, tarjetas, contador frente al WIP con indicación de superado y métricas; y la vista previa con tokens, tipografía, espaciado y los seis componentes del sistema de diseño.

#### Scenario: Tarjeta del tablero
- **WHEN** se dibuja el Kanban con una tarjeta `TAR-05`
- **THEN** aparece con su código, su título y su responsable en la columna que le corresponde

### Requirement: Pruebas del modelo y de la vista
Las pruebas del repositorio SHALL ejecutar con `node` el modelo de cada visual sobre su `mock.json` y sobre datos de ejemplo y comprobar que coincide con el cálculo del kit, y, si las dependencias de `_build/` están instaladas, SHALL renderizar la vista en servidor y comprobar su contenido; sin `node` o sin dependencias SHALL omitirse con aviso sin afectar al resto del kit.

#### Scenario: Node no instalado
- **WHEN** las pruebas corren en una máquina sin `node`
- **THEN** las pruebas del modelo y de la vista se omiten con aviso y el resto pasa

### Requirement: Texto limpio en las plantillas
Ningún texto de las plantillas, de sus `mock.json` ni de sus `README.md` SHALL calificar los datos como falsos, inventados, de prueba o simulados, aunque los datos de ejemplo sean solo para ver la plantilla.

#### Scenario: Estado vacío
- **WHEN** una plantilla se muestra sin datos
- **THEN** dice «Sin datos» sin etiquetas de procedencia
