# Sistema de diseño · Proyecto

## Principios

- **Serio y oscuro:** carbón neutro como fondo (`color.oscuro.fondo`), superficies un paso más claras (`color.oscuro.superficie`) y un solo acento amarillo, el de Power BI (`color.oscuro.acento`); sin degradados ni adornos.
- **Sobrio:** una sola familia sans, Segoe UI (`tipografia.familia`), para titulares y texto, y monoespaciada para códigos (`tipografia.familia-mono`); radios contenidos (`radio.sm`, `radio.md`) y jerarquía dada por el borde y la superficie más que por la sombra (`sombra.sm`).
- **Profesional:** colores de estado solo para estados (`color.oscuro.exito`, `color.oscuro.alerta`, `color.oscuro.error`) y contraste AA en todos los pares de texto, en ambos temas.

## Color

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `fondo` | #F3F2F1 | #1F1E1D | Fondo de la página |
| `superficie` | #FFFFFF | #292827 | Tarjetas, tablas, paneles |
| `texto` | #201F1E | #F3F2F1 | Texto principal |
| `texto-secundario` | #605E5C | #BEBBB8 | Etiquetas y metadatos |
| `borde` | #D2D0CE | #484644 | Líneas y separadores |
| `acento` | #A67C00 | #F2C811 | Relleno: botón principal, barras de progreso |
| `acento-texto` | #141312 | #1F1E1D | Texto sobre el acento |
| `acento-fuerte` | #7A5F00 | #FFDC4D | Texto y líneas de acento: enlaces, fecha de corte |
| `exito` | #107C10 | #92C353 | Estado correcto |
| `alerta` | #8A4B00 | #FFAA44 | Estado en riesgo |
| `error` | #A4262C | #FF8A8A | Estado con problema |

## Tipografía

Dos familias: `tipografia.familia` (Segoe UI, para titulares, cifras y texto) y `tipografia.familia-mono` (códigos); cada pila termina en fuentes del sistema para funcionar sin conexión. La jerarquía se logra con el peso (`tipografia.peso.fuerte` en titulares) y la escala: `tipografia.escala.xs` 12 px, `sm` 14 px, `base` 16 px, `lg` 20 px, `xl` 26 px y `2xl` 34 px, con interlineado `tipografia.interlineado.normal` en el texto.

## Espacio, radio y sombra

| Grupo | Valores |
|---|---|
| Espacio | `espacio.1` 4 px · `espacio.2` 8 px · `espacio.3` 12 px · `espacio.4` 16 px · `espacio.6` 24 px · `espacio.8` 32 px |
| Radio | `radio.sm` 4 px · `radio.md` 6 px · `radio.lg` 8 px |
| Sombra | `sombra.sm` mínima · `sombra.md` solo para elementos elevados; en oscuro la jerarquía la dan el borde y la superficie |

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

El tema **oscuro es el predeterminado** (`tema-defecto: "oscuro"` en `tokens.json`, que llega al HTML como la variable `--tema-defecto`; `data-theme="dark"` en la raíz). El claro se activa con `data-theme="light"` (botón de tema) y `prefers-color-scheme: dark` queda como respaldo sin JavaScript. El claro usa gris cálido muy claro de fondo, superficies blancas y un oro más profundo como acento (`color.claro.acento`), porque el amarillo del tema oscuro no tiene contraste suficiente sobre blanco.

## Accesibilidad

Los pares texto y fondo declarados en `tokens.json` cumplen contraste WCAG AA en ambos temas: 4,5:1 para texto normal y 3:1 para elementos de interfaz (Kirkpatrick et al., 2025). El foco visible usa `color.oscuro.acento-fuerte` y el estado nunca se comunica solo por color.

## Cómo usarlo

Leer `diseno` en `project/config.yaml` para obtener la ruta de este archivo, leer `tokens.json` de la misma carpeta y usar las variables `--c-*`, `--espacio-*`, `--radio-*` y `--sombra-*`. No copiar valores a mano.
