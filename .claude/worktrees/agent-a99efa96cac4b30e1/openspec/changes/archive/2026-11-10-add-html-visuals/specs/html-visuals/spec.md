## ADDED Requirements

### Requirement: Plantillas de visuales
`common/html/` SHALL incluir diez carpetas de plantilla (`foda`, `lean-canvas`, `mapa-empatia`, `journey-map`, `matriz-priorizacion`, `equipo-scrum`, `calendario-ceremonias`, `panel-avance`, `resultados-lean`, `cumplimiento-objetivos`), cada una con `index.html`, `README.md` y `mock.json` de ejemplo, con el mismo mecanismo que `gantt` y `kanban` (tokens y datos como únicos bloques variables, botones de imagen y ancho completo cuando es grande).

#### Scenario: Plantilla completa
- **WHEN** se revisa una carpeta de visual
- **THEN** tiene `index.html`, `README.md` y `mock.json`, y el HTML es autónomo y muestra el ejemplo de `mock.json`

#### Scenario: Visual con botones de imagen
- **WHEN** se abre cualquier plantilla
- **THEN** ofrece «Copiar imagen» y «Descargar imagen» con selector de escala ×2, ×3 y ×4

### Requirement: Datos extraídos del markdown
El kit SHALL extraer los datos de cada visual de las tablas de las corridas vigentes de su skill de origen (`foda` de 03, `lean-canvas` de 02 y 07, `mapa-empatia`, `journey-map` y `matriz-priorizacion` de 05, `equipo-scrum` de 08, `calendario-ceremonias` de 12 y 11, `panel-avance` del `data.json` de los tableros, `resultados-lean` de 17 y `cumplimiento-objetivos` de 18); SHALL incluir un dato opcional solo si el origen lo trae y SHALL fallar con un mensaje claro si falta la fuente o una tabla.

#### Scenario: Fuente ausente
- **WHEN** el config no tiene corrida de `05-make-design-thinking`
- **THEN** la extracción de `mapa-empatia` informa que falta esa fuente y no genera datos

#### Scenario: Dato opcional
- **WHEN** el backlog no trae prioridad para una tarjeta
- **THEN** el dato no se incluye y el visual no muestra chip de prioridad

### Requirement: Generación condicionada a la fuente
`13-design-html-boards` SHALL listar qué visuales tienen fuente, preguntar cuáles generar (por defecto, todos los disponibles) y escribir cada uno en `visuales/<visual>.html` con su `visuales/<visual>.json`; un visual cuya fuente aún no existe, como los de 17 y 18, SHALL sumarse con `13-design-html-boards-update` cuando esa fuente exista.

#### Scenario: Fuente tardía
- **WHEN** `17-make-lean-results` se ejecuta después del paso 13
- **THEN** `13-design-html-boards-update` agrega `resultados-lean` sin alterar los visuales ya generados

#### Scenario: Visual no elegido
- **WHEN** el usuario no quiere el `foda`
- **THEN** la corrida no contiene `visuales/foda.html` ni `visuales/foda.json`

### Requirement: Contenido de los visuales de diagnóstico e innovación
`foda` SHALL mostrar sus cuatro cuadrantes con código, ítem y evidencia; `lean-canvas`, sus nueve bloques (en v1, los cambiados resaltados con «v0 → v1»); `mapa-empatia`, sus cuatro cuadrantes, dolores y ganancias; `journey-map`, las etapas con la curva de emoción de −2 a +2 y los puntos de dolor; `matriz-priorizacion`, las ideas según impacto y factibilidad con las del MVP destacadas.

#### Scenario: Elemento ausente
- **WHEN** una debilidad del FODA de origen no aparece en `foda.html`
- **THEN** la validación informa el código porque los datos no coinciden con la fuente

#### Scenario: Curva de emoción
- **WHEN** el journey map tiene cinco etapas con emociones entre −2 y +2
- **THEN** el visual dibuja la curva con un punto por etapa y señala las de dolor

### Requirement: Contenido de los visuales de gestión y resultados
`equipo-scrum` SHALL mostrar los roles, integrantes y sprints; `calendario-ceremonias`, las ceremonias de cada sprint en su fecha; `panel-avance`, los indicadores de `calculado`; `resultados-lean`, cada resultado contra su criterio con la decisión; `cumplimiento-objetivos`, cada objetivo con meta, resultado y valoración.

#### Scenario: Resultado contra criterio
- **WHEN** un experimento tiene criterio de 20 % y resultado de 14 %
- **THEN** `resultados-lean` muestra ambos valores, el semáforo de incumplimiento y la decisión

### Requirement: Validación de los visuales
La validación SHALL exigir que cada `visuales/<visual>.json` sea igual a la extracción hecha hoy de las corridas vigentes, que cada `<visual>.html` sea la plantilla con solo el bloque de tokens del diseño y el de datos de su JSON, y que no haya un HTML sin su JSON; SHALL informar archivo y causa de cada incidencia.

#### Scenario: Fuente cambiada
- **WHEN** el FODA de 03 cambió después de generar `foda.json`
- **THEN** la validación informa que `foda.json` difiere de la fuente y que debe actualizarse con el `-update`

#### Scenario: HTML sin JSON
- **WHEN** existe `visuales/foda.html` y no `visuales/foda.json`
- **THEN** la validación informa el archivo faltante

### Requirement: Calidad y alcance de las plantillas
Cada plantilla SHALL respetar `common/html/DESIGN.md`, usar gráficos propios en SVG sin librerías externas, calcular posiciones en un modelo puro con pruebas y funcionar tanto con datos de ejemplo como vacíos.

#### Scenario: Datos vacíos
- **WHEN** se monta una plantilla con su `mock.json` limpio
- **THEN** se muestra el estado vacío sin errores

### Requirement: Explicación de cada imagen
Por cada tablero y visual generado, el kit SHALL escribir `leer-imagen/<visual>.md`: una lista de puntos cortos y claros (qué muestra, cómo leerla, qué transmite y un pie de foto sugerido), derivados solo de los datos de la imagen y sin texto escrito a mano, para pegarse junto a la imagen en el informe.

#### Scenario: Explicación del FODA
- **WHEN** se construye el visual `foda` con 3 fortalezas, 3 debilidades, 2 oportunidades y 2 amenazas
- **THEN** `leer-imagen/foda.md` indica esas cantidades, cómo leer los cuadrantes y un pie de foto sugerido

#### Scenario: Explicación del Gantt
- **WHEN** se genera `gantt.html` desde `data.json`
- **THEN** `leer-imagen/gantt.md` resume tareas, sprints, avance global, atrasadas y la fecha de corte

### Requirement: Cambio de un dato de un visual
Un dato que se ve en un visual SHALL cambiarse en la fuente: el `-update` de la skill de origen modifica solo ese dato y `13-design-html-boards-update` vuelve a extraer los visuales y regenera sus explicaciones sin alterar los visuales cuya fuente no cambió; `visuales.py origen` SHALL indicar la skill, el archivo y el `-update` de cada visual.

#### Scenario: Corregir un porcentaje
- **WHEN** el usuario pide que un resultado sea 50 % en lugar de 25 %
- **THEN** `17-make-lean-results-update` cambia ese dato y, tras `13-design-html-boards-update`, solo `resultados-lean` y lo que depende del dato quedan distintos

#### Scenario: Editar el JSON de un visual a mano
- **WHEN** alguien cambia un valor en `visuales/<visual>.json`
- **THEN** la validación informa que difiere de la fuente y que debe actualizarse con el `-update`

