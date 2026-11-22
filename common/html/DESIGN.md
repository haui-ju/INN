# DESIGN.md · Reglas visuales de la biblioteca HTML

Reglas de las plantillas de `common/html/`. Los valores salen de `tokens.json` del sistema de diseño del proyecto (o de los tokens base de `02-design-system`); aquí se fija **cómo se usan**. Estilo: cálido, editorial y sobrio, inspirado en Claude: marfil, tinta casi negra, un único acento terracota y titulares en serif. Evita la apariencia genérica de interfaz «de plantilla»: poco borde, mucho aire, jerarquía clara y color con intención.

## 1. Principios
1. **Un solo acento.** El naranja terracota marca lo principal (botón primario, barras de avance, fecha de corte). Nada más lleva color de marca.
2. **Calidez, no frialdad.** Neutros con matiz cálido (marfil, arena, carbón cálido); nunca grises azulados.
3. **Editorial.** Titulares y cifras grandes en serif; el texto de apoyo, en sans; los códigos, en monoespaciada.
4. **Aire antes que adorno.** Espacio generoso, bordes finos, sombras muy suaves; sin degradados, sin ilustraciones, sin íconos decorativos.
5. **El color de estado es solo para estados.** Éxito, alerta y error nunca se usan como decoración, y el estado nunca depende solo del color (siempre hay texto).
6. **Tema por defecto según los tokens.** Sin `tema-defecto` abre en claro; con `tema-defecto: "oscuro"` abre en oscuro. El otro tema es opcional, no es el invertido y se activa con el botón; la elección se recuerda.

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

Todos los pares de texto cumplen AA (4,5 : 1) en claro y oscuro; los elementos de interfaz, 3 : 1. `acento` nunca se usa como color de texto.

## 3. Tipografía
| Rol | Fuente | Uso |
|---|---|---|
| Titulares y cifras | Newsreader (serif, incrustada) | `h1` a `h4`, títulos de tarjeta, números grandes de los indicadores |
| Texto | Instrument Sans (sans, incrustada) | Párrafos, tablas, botones, etiquetas |
| Códigos | Monoespaciada del sistema | `TAR-05`, `HU-02`, `RF-01`, tokens |

Escala: `xs` 12, `sm` 14, `base` 16, `lg` 20, `xl` 26, `2xl` 34 px. Titulares en peso 500 con interletrado ligeramente negativo; nunca en negrita pesada ni en mayúsculas gritadas. Etiquetas de columna en `xs`, mayúsculas con interletrado amplio, color secundario.

## 4. Espacio, forma y elevación
- **Espacio** (4 px de base): `1`=4, `2`=8, `3`=12, `4`=16, `6`=24, `8`=32. Entre bloques, `6`; dentro de tarjetas, `4`.
- **Radio:** `sm` 6 px (barras, marcas), `md` 10 px (botones, campos, fichas), `lg` 16 px (tarjetas y paneles).
- **Sombra:** `sm` en reposo, `md` solo al pasar el cursor. En el tema oscuro la jerarquía la dan el borde y la superficie.

## 5. Componentes
Todos los visuales usan estos componentes (estilo shadcn/ui, en `_build/src/ui/`); un visual nuevo no crea otros equivalentes.

| Componente | Estados | Regla de uso |
|---|---|---|
| Encabezado | normal | Título serif, subtítulo con el proyecto y, a la derecha, la fecha de corte («al DD-MM-AAAA» o «Línea base») como etiqueta de marca. Siempre dentro del área de captura |
| Indicador | normal | Icono en un recuadro tintado, cifra grande en serif y rótulo pequeño. Muestra el valor de `calculado` tal cual; el tono del icono es de marca, de éxito (terminadas) o de error (atrasadas) |
| Tarjeta | normal | Agrupa un tema; sin tarjetas dentro de tarjetas |
| Tabla | normal, fila resaltada | Encabezado en mayúsculas pequeñas; en teléfono se desplaza dentro de su contenedor |
| Etiqueta (`Badge`) | neutra, marca, éxito, alerta, error | Siempre con texto; fondo suave y texto de contraste AA. `mono` para códigos |
| Barra de progreso | vacía, parcial, completa | Relleno `acento`, pista `borde`; con porcentaje o fracción visible |
| Botón | normal, hover, foco, deshabilitado | Un solo botón primario por vista (Copiar imagen); los demás, contorno o fantasma |
| Selector | normal, foco | Nativo con estilo; para escala de imagen y filtros |
| Avatar | normal | Iniciales del responsable en un círculo tintado de marca; siempre con el nombre al lado o en `title` |
| Chip de prioridad | Debe, Debería, Podría | Con bandera: `Debe` relleno de acento, `Debería` con borde de acento, `Podría` neutro. Solo si el dato existe |

## 6. Accesibilidad y adaptación
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
