# Sistema de diseño · Proyecto

## Principios

- **Cálido:** neutros con matiz cálido (marfil, arena, carbón) y un solo acento terracota (`color.claro.acento`); sin degradados ni adornos.
- **Editorial:** titulares y cifras en serif (`tipografia.familia-titulos`), texto en sans (`tipografia.familia`) y códigos en monoespaciada (`tipografia.familia-mono`); radio medio a generoso (`radio.md`, `radio.lg`), sombras suaves (`sombra.sm`) y espacio amplio (`espacio.4`, `espacio.6`).
- **Profesional:** colores de estado solo para estados (`color.claro.exito`, `color.claro.alerta`, `color.claro.error`) y contraste AA en todos los pares de texto.

## Color

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `fondo` | #FAF9F5 | #262624 | Fondo de la página |
| `superficie` | #FFFFFF | #30302E | Tarjetas, tablas, paneles |
| `texto` | #141413 | #F5F4EE | Texto principal |
| `texto-secundario` | #6B675C | #B7B3A6 | Etiquetas y metadatos |
| `borde` | #E3E0D5 | #4A4944 | Líneas y separadores |
| `acento` | #D4704F | #E0795A | Relleno: botón principal, barras de progreso |
| `acento-texto` | #1F1B16 | #141413 | Texto sobre el acento |
| `acento-fuerte` | #B1472A | #F0A488 | Texto y líneas de acento: enlaces, fecha de corte |
| `exito` | #2F6B45 | #86C99A | Estado correcto |
| `alerta` | #8A5A00 | #E3B25A | Estado en riesgo |
| `error` | #B3261E | #F28B82 | Estado con problema |

## Tipografía

Tres roles: `tipografia.familia-titulos` (serif, titulares y cifras), `tipografia.familia` (sans, texto) y `tipografia.familia-mono` (códigos); cada pila termina en fuentes del sistema para funcionar sin conexión. Escala `tipografia.escala.xs` a `tipografia.escala.2xl`, con `tipografia.escala.base` en 16 px. Pesos `tipografia.peso.normal`, `tipografia.peso.medio` y `tipografia.peso.fuerte`; interlineado `tipografia.interlineado.normal` para texto corrido y `tipografia.interlineado.compacto` para titulares.

## Espacio, radio y sombra

| Grupo | Valores |
|---|---|
| Espacio | `espacio.1` 4 px · `espacio.2` 8 px · `espacio.3` 12 px · `espacio.4` 16 px · `espacio.6` 24 px · `espacio.8` 32 px |
| Radio | `radio.sm` 6 px · `radio.md` 10 px · `radio.lg` 16 px |
| Sombra | `sombra.sm` suave · `sombra.md` para elementos elevados |

## Componentes

### Encabezado

- **Estados:** normal
- **Tokens:** `tipografia.familia-titulos`, `tipografia.escala.2xl`, `color.claro.texto-secundario`, `color.claro.acento-fuerte`, `espacio.6`
- **Uso:** título serif, subtítulo y la fecha de corte como etiqueta de acento; una sola acción de acento.

### Tarjeta

- **Estados:** normal, enfocada
- **Tokens:** `color.claro.superficie`, `color.claro.borde`, `radio.lg`, `sombra.sm`, `espacio.4`
- **Uso:** agrupa un tema; no se anidan tarjetas.

### Tabla

- **Estados:** normal, fila resaltada
- **Tokens:** `color.claro.superficie`, `color.claro.borde`, `color.claro.texto-secundario`, `espacio.3`
- **Uso:** encabezado con texto secundario y filas separadas; en teléfono se desplaza dentro de su contenedor.

### Etiqueta de estado

- **Estados:** éxito, alerta, error, neutra
- **Tokens:** `color.claro.exito`, `color.claro.alerta`, `color.claro.error`, `radio.sm`, `tipografia.escala.xs`
- **Uso:** siempre lleva texto; el estado no se comunica solo por color.

### Barra de progreso

- **Estados:** vacía, parcial, completa
- **Tokens:** `color.claro.acento`, `color.claro.borde`, `espacio.2`
- **Uso:** va acompañada de una fracción o un porcentaje visible.

### Botón

- **Estados:** normal, hover, foco, deshabilitado
- **Tokens:** `color.claro.acento`, `color.claro.acento-texto`, `radio.md`, `sombra.md`, `espacio.3`
- **Uso:** un botón principal por vista; los demás son secundarios con borde `color.claro.borde`.

## Tema claro y oscuro

El tema **claro es el predeterminado** (`data-theme="light"` en la raíz). El oscuro se activa con `data-theme="dark"` (botón de tema) y `prefers-color-scheme: dark` queda como respaldo sin JavaScript. El oscuro usa carbón cálido, sube la luminosidad del acento y sube un paso las superficies; no es el claro invertido.

## Accesibilidad

Los pares texto y fondo declarados en `tokens.json` cumplen contraste WCAG AA en ambos temas: 4,5:1 para texto normal y 3:1 para elementos de interfaz (Kirkpatrick et al., 2025). El foco visible usa `color.claro.acento-fuerte` y el estado nunca se comunica solo por color.

## Cómo usarlo

Leer `diseno` en `project/config.yaml` para obtener la ruta de este archivo, leer `tokens.json` de la misma carpeta y usar las variables `--c-*`, `--espacio-*`, `--radio-*` y `--sombra-*`. No copiar valores a mano.
