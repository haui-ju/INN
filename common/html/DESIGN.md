# DESIGN.md · Reglas visuales de la biblioteca HTML

Reglas de las plantillas de `common/html/`. Los valores salen de `tokens.json` del sistema de diseño del proyecto (o de los tokens base de `02-design-system`); aquí se fija **cómo se usan**. Estilo: noche viva, con color y con forma propia. Fondo azul violeta profundo con resplandores de color, un solo acento amarillo (el de Power BI) y ocho colores de serie para dar identidad a cada categoría; todo con tarjetas redondeadas y diagramas dibujados (el pez del Ishikawa, la estrella del modelo de datos), no con cajas grises.

## 1. Principios
1. **Un solo acento.** El amarillo marca lo principal (botón primario, la cabeza del pez, los hechos del modelo, barras de avance). Nada más lleva color de marca.
2. **Color con significado.** Cada categoría, factor, capa o cuadrante lleva un color de serie (`serie-1` a `serie-8`, en orden fijo). El color da identidad; el texto y el icono dan el significado, así que nunca se depende solo del color.
3. **Forma propia.** Si el dato tiene una forma natural, se dibuja: un pez para las causas, una estrella para el modelo, capas conectadas para la arquitectura, un balance para el entorno. Se evita el simple listado de cajas.
4. **Profundidad con luz, no con negro.** Resplandores de la propia serie, bordes teñidos y degradados suaves; sin sombras negras pesadas ni ilustraciones decorativas.
5. **El color de estado es solo para estados.** Éxito, alerta y error nunca se usan como decoración, y el estado nunca depende solo del color (siempre hay texto o flecha).
6. **Tema por defecto según los tokens.** Sin `tema-defecto` abre en claro; con `tema-defecto: "oscuro"` abre en oscuro (el caso del proyecto). El otro tema es opcional, no es el invertido y se activa con el botón; la elección se recuerda.

## 2. Color (roles)
| Token | Uso |
|---|---|
| `fondo` | Fondo de página y del área de captura |
| `superficie` | Tarjetas, tablas y paneles |
| `texto` / `texto-secundario` | Texto principal / etiquetas, ayudas y metadatos |
| `borde` | Líneas finas y separadores |
| `acento` + `acento-texto` | **Relleno** (botón primario, barras de progreso) con texto oscuro encima |
| `acento-fuerte` | **Texto y líneas** de acento (fecha de corte, etiquetas de marca, línea de corte, hitos) |
| `exito`, `alerta`, `error` | Estados: terminada, en riesgo, bloqueada o límite superado |
| `serie-1` a `serie-8` | Identidad de categorías (turquesa, coral, azul, naranja, violeta, verde, magenta, cielo), en ese orden; validadas contra la superficie para visión normal y daltonismo |

Todos los pares de texto cumplen AA (4,5 : 1) en claro y oscuro; los elementos de interfaz, 3 : 1. `acento` nunca se usa como color de texto.

## 3. Tipografía
| Rol | Fuente | Uso |
|---|---|---|
| Titulares, cifras y texto | Segoe UI (con respaldo del sistema) | `h1` a `h4`, títulos de tarjeta, párrafos, tablas, botones, etiquetas |
| Códigos | Monoespaciada del sistema | `OE-01`, `CAU-04`, `fPedidos`, tokens |

Escala: `xs` 12, `sm` 14, `base` 16, `lg` 20, `xl` 26, `2xl` 34 px. El título principal en peso 750 y los demás titulares en 650, con interletrado ligeramente negativo; nunca en mayúsculas gritadas. Las etiquetas de sección van en `xs`, mayúsculas y con interletrado amplio. Una cifra con «%» usa espacio duro para no partirse en dos líneas.

## 4. Espacio, forma y elevación
- **Espacio** (4 px de base): `1`=4, `2`=8, `3`=12, `4`=16, `6`=24, `8`=32. Entre bloques, `5` a `6` (20 a 24 px); dentro de tarjetas, `4` a `5`.
- **Radio:** `sm` 8 px (marcas), `md` 12 px (campos y fichas), `lg` 20 px (tarjetas y paneles; los paneles grandes llegan a 24 px).
- **Elevación:** brillo de la serie de cada tarjeta (`shadow` teñido con `--k`) y `sombra.md` amplia y suave solo en lo que flota. El lienzo de captura lleva tres resplandores radiales de las series.

## 5. Componentes
Todos los visuales usan estos componentes (estilo shadcn/ui, en `_build/src/ui/`); un visual nuevo no crea otros equivalentes.

| Componente | Estados | Regla de uso |
|---|---|---|
| Encabezado | normal | Etiqueta con la firma de series, título grande con barra de acento, subtítulo con el proyecto y, a la derecha, la fecha de corte («al DD-MM-AAAA» o «Línea base») como etiqueta de marca. Siempre dentro del área de captura |
| Indicador | normal | Icono en un recuadro tintado, cifra grande y rótulo pequeño. Muestra el valor de `calculado` tal cual; el tono del icono es de marca, de éxito (terminadas) o de error (atrasadas) |
| Tarjeta | normal | Agrupa un tema; sin tarjetas dentro de tarjetas |
| Panel (`Panel`) | normal | Tarjeta con identidad de color: `k` es la serie (borde, fondo y brillo teñidos), icono en círculo sólido, contador y, opcional, una letra grande de marca de agua (`marca`) |
| Etiqueta de serie (`Chip`) | normal | Código o categoría con punto del color de su serie; el texto va en tinta |
| Tabla | normal, fila resaltada | Encabezado en mayúsculas pequeñas; en teléfono se desplaza dentro de su contenedor |
| Etiqueta (`Badge`) | neutra, marca, éxito, alerta, error | Siempre con texto; fondo suave y texto de contraste AA. `mono` para códigos |
| Barra de progreso | vacía, parcial, completa | Relleno `acento`, pista `borde`; con porcentaje o fracción visible |
| Botón | normal, hover, foco, deshabilitado | Un solo botón primario por vista (Copiar imagen); los demás, contorno o fantasma |
| Selector | normal, foco | Nativo con estilo; para escala de imagen y filtros |
| Avatar | normal | Iniciales del responsable en un círculo tintado de marca; siempre con el nombre al lado o en `title` |
| Chip de prioridad | Debe, Debería, Podría | Con bandera: `Debe` relleno de acento, `Debería` con borde de acento, `Podría` neutro. Solo si el dato existe |

## 6. Proporción de la imagen (diapositivas)
Las imágenes se pegan en diapositivas. Cada visual tiene un **ancho de diseño fijo** y su proporción ancho : alto queda **entre 1,6 y 2,0** (la de una diapositiva 16:9 es 1,78): ni demasiado vertical ni demasiado ancha. La captura sale igual sin importar el tamaño de la ventana, porque los visuales no usan puntos de corte y se arma siempre al ancho de diseño.

**Texto legible.** En una diapositiva de 13,3 pulgadas el texto de cuerpo debe quedar en 10 pt o más: en una imagen de 1600 a 1700 px eso es **16 px como mínimo** (17 px para lo principal y 13 a 14 px solo para fuentes y notas). Si el contenido no cabe sin apretar, no se reduce el texto: se reparte en **láminas**.

**Láminas.** Un visual con mucho contenido (PESTEL, FODA) se dibuja en dos láminas dentro del **mismo HTML**, apiladas y separadas por un espacio del color de la página. Cada lámina es una diapositiva en sí misma: tiene su fondo, su título y la proporción de diapositiva. Se copia la captura entera y se recorta la que haga falta, sin abrir otros archivos. En el código, `Lamina` y `Laminas` (`_build/src/ui/lamina.jsx`) y `export const laminas = true` en el `modelo.js` del visual.

| Visual | Ancho de diseño | Láminas | Proporción de cada una (con título) |
|---|---|---|---|
| Ishikawa (`ishikawa`) | 1640 px | 1 | 2,0 |
| PESTEL (`pestel`) | 1700 px | 2 (tres factores cada una) | 2,0 |
| Matriz FODA (`foda`) | 1700 px | 2 (matriz de cuatro cuadros y estrategias cruzadas) | 1,6 y 1,8 |
| Business Model Canvas (`bmc`) | 1600 px | 1 | 1,8 |
| Arquitectura de BI (`arquitectura-bi`) | 1600 px | 1 | 1,7 |
| Modelo de datos (`modelo-datos`) | 1440 px | 1 | 1,6 |

El interruptor **«Título en la imagen»** de la barra quita el encabezado de cada lámina; el ancho se mantiene y las proporciones suben a 1,9 o más.

Reglas para un visual nuevo: define `anchoImagen` en su `modelo.js`; usa columnas fijas (`grid-cols-N`) y no `sm:` ni `lg:`; si el contenido es muy alto, divídelo en láminas o quita lo que ya dice la tabla del informe (la tabla de relaciones del modelo de datos, la evidencia de cada ítem del FODA); mide la proporción con datos reales.

## 7. Accesibilidad y adaptación
- Foco visible con `acento-fuerte` (2 px, desfase 2 px). Los íconos acompañan a un texto o llevan `aria-label`.
- Sin desplazamiento horizontal de la página en 360 px: las tablas anchas y los tableros se desplazan dentro de su contenedor (`data-scroll`).
- `role="status"` para los avisos de copiar y descargar; `<noscript>` avisa que el visual necesita JavaScript.

## 7. Movimiento
Mínimo: transiciones de 150 ms en color y sombra de los botones. Sin animaciones de entrada; la captura de imagen debe ser idéntica a lo que se ve.

## 8. Captura de imagen
- El área capturada es `[data-captura]`; lo marcado con `[data-no-captura]` (botones, filtros) queda fuera. Lo que se desplaza se marca con `[data-scroll]` para que la imagen salga completa.
- La explicación que acompaña a la imagen en el informe (`leer-imagen/<visual>.md`) tiene 2 a 3 frases: para qué sirve la figura, qué dice y, solo si resalta algo, por qué se resalta (cuadrante sombreado, etapa en rojo, columna sobre su límite). Se deriva de los datos y no se redacta a mano.
- La imagen lleva el encabezado con la fecha de corte; el nombre del archivo es `<visual>-<fecha>.png`.

## 9. Qué evitar
Más de un color de acento; degradados; sombras pesadas; mayúsculas en titulares; emojis; ilustraciones decorativas; tarjetas dentro de tarjetas; texto naranja de relleno (`acento`) sobre fondo claro; estados comunicados solo por color; colores o tipografías escritos a mano en un visual (siempre por token).

## 10. Visuales anchos
- Los visuales con rejilla o diagrama amplio (por ejemplo el Business Model Canvas, el diagrama de Ishikawa o la arquitectura de BI) ocupan **todo el ancho** de la ventana (`ancho: "completo"`) y la imagen se arma con un **ancho mínimo** (`anchoImagen`, 1560 px) para que salga igual de nítida y ordenada en cualquier pantalla; el resto usa ancho fijo y 1120.

## 11. Visuales del informe
- **Cuadrantes y bloques:** una tarjeta por cuadrante o bloque (`Panel`) con barra superior del tono del contenido (éxito, alerta, error, acento o neutro), icono, título en serif y contador; los ítems son tarjetas internas con código en mono y evidencia en texto secundario.
- **Gráficos propios en SVG**, sin librerías (por ejemplo las espinas del Ishikawa o las cajas y flechas de una arquitectura). Colores y textos del SVG por variable de token (`var(--c-…)`).
- **Estados con tono y texto**: cumplido o favorable (éxito), parcial (alerta), no cumplido o desfavorable (error); nunca solo color.
- **Teléfono:** las rejillas pasan a una columna; los diagramas anchos se desplazan en horizontal dentro de su cuadro.
