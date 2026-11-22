# Sistema de diseño · Proyecto

## Principios

- **Noche viva:** fondo azul violeta profundo (`color.oscuro.fondo`) con resplandores de las series, superficies un paso más claras (`color.oscuro.superficie`) y un solo acento amarillo, el de Power BI (`color.oscuro.acento`).
- **Color con significado:** cada categoría, factor, capa o cuadrante lleva su serie (`color.oscuro.serie-1` a `color.oscuro.serie-8`); el color da identidad y el texto y el icono dan el significado.
- **Formas amables:** tarjetas redondeadas (`radio.lg`), brillos de color en lugar de sombras negras (`sombra.md`) y diagramas con forma propia (el pez del Ishikawa, la estrella del modelo de datos).
- **Profesional:** una sola familia Segoe UI (`tipografia.familia`), colores de estado solo para estados (`color.oscuro.exito`, `color.oscuro.alerta`, `color.oscuro.error`) y contraste AA en ambos temas.

## Color

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `fondo` | #F4F6FD | #0A0E1F | Fondo de la página (noche azul violeta) |
| `superficie` | #FFFFFF | #141A33 | Tarjetas, tablas, paneles |
| `texto` | #11163A | #EEF1FB | Texto principal |
| `texto-secundario` | #4A5280 | #A8B1D6 | Etiquetas y metadatos |
| `borde` | #D8DDF0 | #2B3560 | Líneas y separadores |
| `acento` | #A67C00 | #F2C811 | Relleno: botón principal, barras de progreso |
| `acento-texto` | #14121A | #0A0E1F | Texto sobre el acento |
| `acento-fuerte` | #7A5F00 | #FFD84A | Texto y líneas de acento: enlaces, fecha de corte |
| `exito` | #0F7B3F | #4FD08A | Estado correcto |
| `alerta` | #8A4B00 | #FFB454 | Estado en riesgo |
| `error` | #B3261E | #FF7A85 | Estado con problema |

### Series

Ocho colores de identidad para categorías, factores, capas y cuadrantes, con la paleta de Power BI como referencia. Se asignan en orden fijo y siempre llevan texto o icono al lado.

| Token | Claro | Oscuro | Color |
|---|---|---|---|
| `serie-1` | #009385 | #00A898 | turquesa |
| `serie-2` | #BF5354 | #E06062 | coral |
| `serie-3` | #3A7BCB | #4390EE | azul |
| `serie-4` | #B36300 | #D27400 | naranja |
| `serie-5` | #8864C0 | #9F75E1 | violeta |
| `serie-6` | #319047 | #37A953 | verde |
| `serie-7` | #B55386 | #D4609D | magenta |
| `serie-8` | #0089B8 | #00A1D8 | cielo |

## Tipografía

Dos familias: `tipografia.familia` (Segoe UI, para titulares, cifras y texto) y `tipografia.familia-mono` (códigos); cada pila termina en fuentes del sistema para funcionar sin conexión. La jerarquía se logra con el peso (`tipografia.peso.fuerte` en titulares) y la escala: `tipografia.escala.xs` 12 px, `sm` 14 px, `base` 16 px, `lg` 20 px, `xl` 26 px y `2xl` 34 px, con interlineado `tipografia.interlineado.normal` en el texto.

## Espacio, radio y sombra

| Grupo | Valores |
|---|---|
| Espacio | `espacio.1` 4 px · `espacio.2` 8 px · `espacio.3` 12 px · `espacio.4` 16 px · `espacio.6` 24 px · `espacio.8` 32 px |
| Radio | `radio.sm` 8 px · `radio.md` 12 px · `radio.lg` 20 px |
| Sombra | `sombra.sm` mínima · `sombra.md` amplia y suave; las tarjetas de color usan además un brillo de su propia serie |

## Componentes

### Encabezado

- **Estados:** normal
- **Tokens:** `tipografia.familia-titulos`, `tipografia.escala.2xl`, `color.oscuro.texto-secundario`, `color.oscuro.acento-fuerte`, `espacio.6`
- **Uso:** título en Segoe UI, subtítulo y la fecha de corte como etiqueta de acento; una sola acción de acento.

### Tarjeta

- **Estados:** normal, enfocada
- **Tokens:** `color.oscuro.superficie`, `color.oscuro.borde`, `radio.lg`, `sombra.sm`, `espacio.4`
- **Uso:** agrupa un tema; no se anidan tarjetas.

### Tabla

- **Estados:** normal, fila resaltada
- **Tokens:** `color.oscuro.superficie`, `color.oscuro.borde`, `color.oscuro.texto-secundario`, `espacio.3`
- **Uso:** encabezado con texto secundario y filas separadas; en teléfono se desplaza dentro de su contenedor.

### Etiqueta de estado

- **Estados:** éxito, alerta, error, neutra
- **Tokens:** `color.oscuro.exito`, `color.oscuro.alerta`, `color.oscuro.error`, `radio.sm`, `tipografia.escala.xs`
- **Uso:** siempre lleva texto; el estado no se comunica solo por color.

### Barra de progreso

- **Estados:** vacía, parcial, completa
- **Tokens:** `color.oscuro.acento`, `color.oscuro.borde`, `espacio.2`
- **Uso:** va acompañada de una fracción o un porcentaje visible.

### Botón

- **Estados:** normal, hover, foco, deshabilitado
- **Tokens:** `color.oscuro.acento`, `color.oscuro.acento-texto`, `radio.md`, `sombra.md`, `espacio.3`
- **Uso:** un botón principal por vista; los demás son secundarios con borde `color.oscuro.borde`.

## Tema claro y oscuro

El tema **oscuro es el predeterminado** (`tema-defecto: "oscuro"` en `tokens.json`, que llega al HTML como la variable `--tema-defecto`; `data-theme="dark"` en la raíz). El claro se activa con `data-theme="light"` (botón de tema) y `prefers-color-scheme: dark` queda como respaldo sin JavaScript. El claro usa fondo azulado muy claro, superficies blancas, series algo más oscuras y un oro más profundo como acento (`color.claro.acento`), porque el amarillo del tema oscuro no tiene contraste suficiente sobre blanco.

## Accesibilidad

Los pares texto y fondo declarados en `tokens.json` cumplen contraste WCAG AA en ambos temas: 4,5:1 para texto normal y 3:1 para elementos de interfaz (Kirkpatrick et al., 2025). El foco visible usa `color.oscuro.acento-fuerte` y el estado nunca se comunica solo por color.

## Cómo usarlo

Leer `diseno` en `project/config.yaml` para obtener la ruta de este archivo, leer `tokens.json` de la misma carpeta y usar las variables `--c-*`, `--espacio-*`, `--radio-*` y `--sombra-*`. No copiar valores a mano.
