# Design

## Context

Estado actual, comprobado en el repositorio y en Miro:

- `make-design-thinking` (antes `make-designthinking`) vive en `.claude/skills/make-design-thinking/` con su generador de referencia en `scripts/reference/` (`data.py`, `build.py`). Hoy fija 6 pantallas y declara «Figma, fidelidad media/alta» en los textos generados.
- Cada corrida es `project/design-thinking/<DD-MM-AAAA-HH-MM-SS>/` con `documento.md`, `anexos.md`, `README.md` y `bloques/fase-N-*/`. Las pantallas están en `bloques/fase-4-prototipar/pantallas.md` (tabla `PAN`), los escenarios en `escenarios.md` (`FLU`), los requerimientos en `fase-3-idear/matriz-priorizacion.md` (`REQ`) y los hallazgos en `fase-5-testear/reporte-resultados.md` (`HAL-T`, con la pantalla afectada entre paréntesis en «Cambio propuesto»).
- El plugin `miro@claude-plugins-official` está instalado y autenticado: `user_who_am_i` responde. Las herramientas disponibles incluyen `board_create`, `board_create_format`, `canvas_get_canvas_composer_skill`, `canvas_create_from_svg`, `canvas_update_from_svg`, `canvas_read_as_svg`, `canvas_search`, `comment_*` e `image_*`.
- **Hallazgo:** la documentación de Miro menciona `prototype_create`, pero esa herramienta **no está expuesta** en el plugin instalado. No hay forma verificada de crear un prototipo con clics desde aquí.
- El flujo de Miro exige llamar a `canvas_get_canvas_composer_skill` (paso `design` y luego `dsl`) antes de `canvas_create_from_svg`. Su guía de estilo por defecto («Bright Paper») pide color y relleno; permite sustituirla cuando el usuario pide otro estilo.

Motivación y alcance: ver `proposal.md`. Requisitos: ver `specs/`.

## Goals / Non-Goals

**Goals:**
- Una skill que, dada una corrida, produzca un tablero de Miro legible con las pantallas v1 y v2, y deje el enlace en los documentos.
- Que la cantidad de pantallas sea decisión del usuario por fase, con defaults del playbook.
- Que leer la corrida y parchear los documentos sea determinista y barato en tokens.

**Non-Goals:**
- Prototipo con clics en Miro (no hay herramienta verificada) o integración con Figma.
- Tableros de Miro para las fases 1 a 3.
- Regenerar corridas existentes o cambiar los datos de una corrida.

## Decisions

### D1. Wireframes estáticos con `canvas_create_from_svg`, no `prototype_create`
`prototype_create` no está disponible en el plugin. El SVG del canvas sí lo está y produce elementos editables. **Alternativas:** Figma (no instalado, capacidad de escritura no verificada); HTML como imagen (no editable). **Consecuencia:** las pruebas de la fase 5 pasan a ser recorridos guiados sobre pantallas estáticas, y los textos que decían «prototipo navegable» deben decirlo (ver D5).

### D2. Un tablero por corrida, un frame por pantalla, un solo tamaño de frame
Dos secciones en el mismo tablero: «v1» y «v2». Cada pantalla es un módulo dentro de un frame (ver D9). Una sola dimensión de frame para todos los módulos y una sola dimensión de pantalla (móvil vertical por defecto, porque las personas de la corrida usan celular; escritorio solo si la corrida lo indica). La sección v2 muestra solo la versión nueva de cada pantalla cambiada; el estado anterior sigue en su módulo v1. **Alternativa:** un tablero por fase, descartada por duplicar enlaces y perder la relación v1/v2.

### D3. Estilo wireframe sustituye al estilo de marca por defecto
Se dibujan cajas, texto y botones en neutros de la paleta de Miro (`#ffffff`, `#f7f7f7`, `#e7e7e7`, `#b0b0b0`, `#313131`, `#1a1a1a`, `#595959`), una sola fuente (Noto Sans) y tamaños de la escala, sin sombras ni degradados. Esto es una sustitución deliberada porque el usuario pide wireframes; se aplica la regla de la guía de que lo pedido por el usuario prevalece. Una única familia de acento (azul de la paleta de Miro) se usa para las llamadas numéricas, el panel de referencias y las etiquetas «Cambia».

### D4. Flujo de la skill, con extracción por script
```
preflight Miro (who_am_i)
   -> read_run.py <corrida>   (JSON: PAN, FLU, REQ, HAL-T, herramienta declarada)
   -> pregunta corrida (si no se indicó) y plan + confirmación
   -> board_create
   -> composer skill (design, dsl)
   -> canvas_create_from_svg   (una llamada por sección)
   -> canvas_read_as_svg       (verifica nº de frames = plan)
   -> escribe miro.md y parchea documentos
```
`read_run.py` analiza las tablas Markdown de la corrida. **Por qué un script:** es determinista, ahorra tokens frente a leer ocho archivos y permite probar el parser sin Miro. **Alternativa:** que el modelo lea los archivos; descartada por costo y variabilidad.

### D5. Parcheo de documentos con tabla de reemplazos explícita
La skill modifica solo cadenas conocidas, sin marcadores visibles (el texto debe quedar limpio): la línea «Herramienta y fidelidad» de `escenarios.md`, la columna «Captura» y la línea final de `pantallas.md`, 3.1.5.1 y 3.1.5.3 de `documento.md` y D.3 de `anexos.md`. `miro.md` actúa como el registro de que la corrida ya fue procesada (detección de segunda ejecución). Si una cadena esperada no se encuentra, la skill lo reporta y no adivina.

### D6. Cantidad de pantallas en `make-design-thinking`
El plan de la skill existente añade una pregunta por fase con pantallas (fase 4 v1; fase 5 v2). El generador de referencia deja de fijar «6»: `build.py` deriva los conteos, las tablas y el texto («seis pantallas», rangos de `PAN`, filas de la iteración v2) de las listas de datos, y comprueba con `assert` que cada `REQ` queda cubierto por al menos una pantalla. **Alternativa:** dejar el número fijo y que la nueva skill recorte o amplíe; descartada porque el paquete quedaría incoherente.

### D7. Idioma y recursos
`SKILL.md` en inglés (pedido del usuario); los archivos que escribe en la corrida, en el idioma de la corrida (español). Recursos al mismo nivel: `scripts/read_run.py`, `scripts/patch_run.py` (reemplazos de D5) y `references/wireframe-kit.md` (patrones SVG reutilizables: barra superior, campo, botón, lista, tarjeta, aviso de error, estado vacío).

### D8. Puerta de calidad antes de escribir
La skill no crea ni parchea nada si Miro no responde o si el número de frames verificado no coincide con el plan. **Alternativa:** escribir primero y corregir después; descartada porque deja enlaces rotos en los documentos.

### D9. Cada pantalla es un módulo: interfaz + llamadas numeradas + referencias
Referencia de calidad aportada por el usuario: un módulo con título grande, subtítulo de una línea, la interfaz dentro de un marco de aplicación a la izquierda y un panel «Referencias» a la derecha, con círculos numerados sobre la interfaz que remiten a entradas con título, explicación y códigos de trazabilidad.

```
+--------------------------------------------------------------+
| PAN-04 · Consulta de disponibilidad                          |
| Busca por nombre y muestra el stock por talla (REQ-03)       |
|  +----------------+   +------------------------------------+ |
|  | Inventario     |   | Referencias                        | |
|  | [1] buscador   |   | (1) Buscador   - explicacion       | |
|  | [2] tallas     |   |     REQ-03 · FLU-01                | |
|  | nav inferior   |   | (2) Stock por talla ...            | |
|  +----------------+   +------------------------------------+ |
+--------------------------------------------------------------+
```
- **Marco de aplicación común** (barra superior y navegación inferior con la sección activa en azul) para que todas las pantallas se lean como una sola aplicación.
- **Las referencias salen de la corrida:** título y explicación a partir de «qué muestra» y de los escenarios; trazabilidad con los `REQ`, `FLU`, `PP` y `HAL-T` de la corrida. En v2 cada entrada lleva la etiqueta «Existente» o «Cambia», el hallazgo y una línea «Antes: …».
- **Renderizador determinista:** `scripts/render_svg.py` recibe una descripción compacta en JSON de cada pantalla (elementos, llamadas, referencias, flechas) y produce el SVG con la geometría ya calculada: mismo marco en todas, sin solapamientos, un máximo de 7 llamadas por pantalla y comprobaciones de que el texto cabe. **Trade-off:** el SVG hay que leerlo y reenviarlo a Miro, lo que duplica su costo en tokens frente a escribirlo a mano; se acepta a cambio de consistencia y de poder validar la geometría antes de dibujar. **Alternativa:** que el modelo escriba el SVG completo; descartada por errores de layout en pantallas con muchos elementos.

### D9b. Densidad y proporciones (tras la revisión visual del usuario)
Las primeras versiones tenían botones enormes, zonas vacías y textos pegados a los bordes. El renderizador pasa a una **maquetación automática** (los elementos se apilan con la escala de espaciado 8, 12 y 16; no hay coordenadas manuales) y a un **vocabulario de componentes de aplicación real**: tarjetas de resumen (KPI), listas con miniatura, subtítulo y valor, cuadrícula de tallas, filtros en forma de píldora, control segmentado, selector de cantidad, avisos y resúmenes clave-valor. Controles de 32 a 44 px, texto con padding mínimo de 12 px y marco de dispositivo con barra de estado, barra superior y navegación con iconos. **Comprobación dura:** el renderizador rechaza una pantalla cuyo contenido ocupe menos del 70% del área disponible o se salga de ella; quien describe la pantalla debe llenarla con contenido relevante de la corrida (resúmenes, listas, filtros), no con espacio.

### D10. Flujo entre pantallas con puertos y conectores
Los módulos se ordenan de izquierda a derecha en filas de tres siguiendo el flujo del escenario principal (`FLU-01`). Cada módulo tiene un puerto de entrada y uno de salida (círculos pequeños en el borde del frame), y los conectores con flecha unen los puertos de módulos consecutivos con la acción del usuario como etiqueta. Los conectores deben apuntar a elementos, no a frames, de ahí los puertos; el cruce de frames se acepta porque el usuario pide ver el flujo. Las transiciones las propone el modelo a partir de las tablas `FLU` y `pantallas.md` y forman parte del plan que el usuario confirma.

## Risks / Trade-offs

- [No se puede ver el render desde esta sesión, así que la estética no se verifica visualmente] → Comprobaciones geométricas en el renderizador (límites, solapamientos, texto que cabe) y revisión visual del usuario como tarea final.
- [Costo en tokens de módulos con unos 50 elementos, leídos y reenviados] → Medir en el grupo 8, máximo 7 llamadas por pantalla y una sección por llamada.
- [Los wireframes SVG salen desordenados o poco legibles] → Prueba corta con 1 o 2 pantallas antes de generalizar, y `wireframe-kit.md` con patrones validados.
- [Costo en tokens de dibujar 6 a 10 frames] → Una llamada por sección, kit de patrones reutilizable y medición registrada durante la prueba corta.
- [Pantallas estáticas debilitan la prueba de usabilidad de la fase 5] → Se declara como limitación en el documento y se ofrece mantener Figma para el prototipo navegable.
- [El parcheo de textos rompe un documento editado a mano] → Reemplazos exactos, reporte de cadenas no encontradas y no sobrescribir lo que no coincide.
- [El plugin pierde la autenticación o cambia sus herramientas] → Preflight con `user_who_am_i` y mensaje de reautenticación; no hay escritura parcial (D8).
- [`build.py` parametrizado introduce errores de coherencia] → Los `assert` existentes se amplían y se ejecuta una generación de comprobación en una carpeta temporal.

## Findings from the spike (tarea 1)

Resueltas las dos preguntas abiertas y confirmada la decisión D1:

- **Creación del tablero:** `board_create` solo exige `name`; sin `parent_space_url` crea el tablero en la raíz del equipo del usuario autenticado. No hace falta elegir equipo ni espacio. La herramienta indica que no se puede deshacer y que se confirme antes de crear (la skill ya lo cubre con el plan y la confirmación). **Miro no ofrece herramienta para borrar tableros:** quien quiera eliminar uno lo hace a mano.
- **Identificadores de frame:** `canvas_create_from_svg` devuelve `result_svg` con `data-miro-id` por elemento; el frame de cada pantalla trae el suyo. El enlace directo a una pantalla es `<url del tablero>?moveToWidget=<id del frame>`.
- **Lectura de vuelta:** `canvas_read_as_svg` con el id del frame devuelve sus elementos como formas con texto editables (`data-content`, relleno, trazo), lo que permite verificar el número de frames del plan.
- **Prototipo con clics:** el formato admite un contenedor de prototipo con pantallas HTML, pero la creación fue rechazada con «`prototyping_container` is not available for your organization». Queda confirmado D1: wireframes estáticos en frames. Si la organización habilita la función, podría añadirse después.
- **Reglas del SVG que afectan a los wireframes:** el trazo debe ser mayor que 1 (se usa 2); los frames no admiten borde ni esquinas redondeadas; las etiquetas van en `data-content` de la forma, no en texto superpuesto; los títulos del frame van dentro de su `data-frame`.
- **Costo en tokens (estimado, caracteres ÷ 3,5):** la guía del formato (`canvas_get_canvas_composer_skill`, paso `dsl`) pesa unos 75 500 caracteres, del orden de 20 000 tokens, una sola vez por conversación; el paso `design` pesa unos 6 000 caracteres. Un frame de pantalla ocupa unos 2 500 a 3 000 caracteres de SVG (del orden de 800 tokens) y su respuesta repite el SVG con identificadores (otros 1 000 a 1 300 tokens), es decir unos 2 000 tokens por pantalla de ida y vuelta. Un tablero de 6 pantallas v1 y 4 pares v2 ronda los 25 000 tokens más el costo fijo de la guía. **Decisión:** una llamada por sección (v1, v2) y no una por pantalla, para pagar una sola vez el encabezado del SVG y la repetición de la respuesta.

- **Costo medido del diseño por módulos (grupo 8):** cada sección de 5 o 6 módulos pesa unos 35 000 caracteres de SVG (unos 10 000 tokens para leerlo y otros 10 000 para enviarlo) y la respuesta repite el SVG con identificadores (unos 20 000 tokens). Un tablero completo (6 módulos v1 con 5 flechas y 5 módulos v2) ronda los 80 000 tokens, además de los 20 000 de la guía del formato. El tablero resultante tiene 11 módulos nuevos, 413 elementos y 5 conectores.
- **Verificación:** `canvas_search` confirma frames y flechas por patrón; las flechas se crean unidas a los puertos de los frames (conectores entre widgets, no entre frames).
- **Borrado:** el protocolo de Miro exige confirmar con el usuario antes de enviar `data-deleted="true"`; la skill nunca borra sin preguntar.
- **Limitación:** desde esta sesión no se ve el render, así que la estética se valida con comprobaciones geométricas y con la revisión visual del usuario (tarea 8.6).

## Open Questions

- Si conviene guardar en `miro.md` el enlace directo a cada frame (`?moveToWidget=`) además del tablero; se decide al escribir `patch_run.py` sin cambiar las specs.
