# Playbook del sistema de diseño

Guía para que un agente defina el sistema de diseño de un proyecto: la identidad visual única que reutilizan los tableros HTML, el informe y cualquier pantalla. Complementa a las plantillas de [`models/`](models/README.md): aquí van el método y las reglas; allí el formato de cada entregable.

Lo ejecuta la skill `02-design-system` (y la ajusta `02-design-system-update`). Escribe en `project/02-design-system/<DD-MM-AAAA-HH-MM-SS>/`.

---

## 0. Reglas que se aplican siempre

### 0.1 Un sistema único, definido una vez
Todo valor visual (color, tipografía, espacio, radio, sombra) se define en `tokens.json`. `DESIGN.md` lo documenta y `preview.html` lo muestra. Si un valor aparece distinto en dos archivos, manda `tokens.json`.

### 0.2 Cálido, editorial y profesional
El estilo base es cálido y editorial, de la familia de Claude: marfil, tinta casi negra, **un solo acento terracota** y titulares en serif. Las reglas de uso de los componentes en los HTML están en `common/html/DESIGN.md`.

| Principio | Qué significa aquí | Qué evitar |
|---|---|---|
| Cálido | Neutros con matiz cálido (marfil, arena, carbón cálido) y **un solo** color de acento, sin degradados ni adornos | Grises azulados, más de un acento, fondos con textura, íconos decorativos |
| Editorial | Titulares y cifras en serif, texto en sans, códigos en monoespaciada; radio medio a generoso (6 a 16 px), sombras suaves y mucho aire | Bordes duros, sombras pesadas, mayúsculas en titulares, fuentes ornamentales |
| Profesional | Colores de estado solo para estados; contraste AA; tema por defecto definido en `tema-defecto` (claro si no existe) | Colores saturados de juego, emojis en la interfaz, estados comunicados solo por color |

### 0.3 Preguntar y confirmar
La skill lee el config y `project/domain.md`, y pregunta solo lo que falta (ficha `ds-0-brief`). Propone un sistema completo y **espera la confirmación** antes de escribir archivos. Si el usuario cambia algo, actualiza la propuesta y la muestra de nuevo.

### 0.4 Nombres de tokens
Los tokens se citan con su ruta: `color.claro.acento`, `color.oscuro.fondo`, `espacio.4`, `radio.md`, `sombra.sm`, `tipografia.escala.base`. Esta guía no usa códigos de trazabilidad: la trazabilidad es el nombre del token.

### 0.5 Texto limpio
Ningún archivo de la corrida, salvo su `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Los ejemplos de los componentes usan contenido realista y neutro del proyecto (por ejemplo «Depurar ventas de enero», «Revisar el modelo de datos», «Publicar el dashboard»). La procedencia va solo en `README.md`.

### 0.6 Cantidades de referencia
Son referencias, no normas: 10 a 12 tokens de color por tema, una escala tipográfica de 6 pasos, 6 pasos de espacio, 3 radios, 2 sombras y 6 componentes. La skill avisa en una línea si el usuario se sale del rango y respeta su decisión.

---

## 1. Color

### 1.0 Tema por defecto
`tokens.json` puede declarar `"tema-defecto": "claro"` o `"oscuro"` (opcional; sin él, claro). Es una decisión de tono del usuario (por ejemplo, un sistema oscuro tipo Power BI); ambos temas se definen y validan igual.

### 1.1 Roles semánticos (obligatorios en claro y oscuro)
| Token | Uso |
|---|---|
| `fondo` | Fondo de la página |
| `superficie` | Tarjetas, tablas, paneles |
| `texto` | Texto principal |
| `texto-secundario` | Etiquetas, ayudas, metadatos |
| `borde` | Líneas y separadores |
| `acento` | **Relleno**: botón principal, barras de progreso, elemento activo |
| `acento-texto` | Texto sobre `acento` (oscuro, para cumplir AA) |
| `acento-fuerte` | **Texto y líneas** de acento (enlaces, fecha de corte, etiquetas de marca); variante más oscura en claro y más clara en oscuro, AA sobre `fondo` y `superficie`. Rol recomendado: lo usan las plantillas HTML |
| `exito`, `alerta`, `error` | Solo para estados |

### 1.2 Cómo elegir
1. Si el usuario aporta un color de marca, es el `acento`; se deriva el resto (incluido `acento-fuerte`, más oscuro, hasta cumplir AA como texto).
2. Si no, se usa el tema base: terracota (`#D4704F` de relleno con texto `#1F1B16` y `#B1472A` para texto), sobre marfil `#FAF9F5`.
3. Los neutros llevan un matiz cálido leve. El tema oscuro no es el claro invertido: fondo carbón cálido, acento más luminoso y superficies un paso más claras.

---

## 2. Tipografía, espacio, radio y sombra

- **Familias (tres roles):** `familia-titulos` (serif, para titulares y cifras), `familia` (sans, para el texto) y `familia-mono` (códigos). Las plantillas de `common/html/` incrustan **Newsreader** (serif) e **Instrument Sans** (sans), ambas de código abierto (licencia OFL), y usan la monoespaciada del sistema; cada pila termina en fuentes del sistema para que el HTML funcione sin conexión. Si el usuario pide otra fuente, se declara con la pila del sistema como respaldo y se avisa de que no se incrusta.
- **Escala:** `xs`, `sm`, `base`, `lg`, `xl`, `2xl` (razón aproximada 1,25), con `base` en 16 px.
- **Espacio:** base de 4 px: `1`=4, `2`=8, `3`=12, `4`=16, `6`=24, `8`=32.
- **Radio:** `sm`, `md`, `lg`.
- **Sombra:** `sm` y `md`, suaves, de baja opacidad; en el tema oscuro se sustituyen por borde.

---

## 3. Accesibilidad de color

Norma de referencia: WCAG 2.1, criterios 1.4.3 y 1.4.11 (Kirkpatrick et al., 2025).

| Tipo de par | Contraste mínimo |
|---|---|
| Texto normal | 4,5 : 1 |
| Texto grande (≥ 24 px, o ≥ 18,66 px en negrita) | 3 : 1 |
| Elemento de interfaz (borde de campo, ícono, barra) | 3 : 1 |

El contraste es (L1 + 0,05) / (L2 + 0,05), con L la luminancia relativa del color (L1 el más claro). `tokens.json` declara en `pares` qué combinaciones se validan (por ejemplo `texto` sobre `fondo`) y su tipo. Se validan **en claro y en oscuro**.

Además: el estado nunca se comunica solo por color (la etiqueta lleva texto), y el foco visible usa `acento`.

---

## 4. Componentes mínimos

Cada componente declara **estados**, **tokens** y una **regla de uso**.

| Componente | Estados mínimos | Regla de uso |
|---|---|---|
| Encabezado | normal | Título de página, subtítulo y acción principal; una sola acción de acento |
| Tarjeta | normal, enfocada | Agrupa un tema; sin tarjetas dentro de tarjetas |
| Tabla | normal, fila resaltada | Encabezado fijo y filas con separador; en teléfono se desplaza dentro de su contenedor |
| Etiqueta de estado | éxito, alerta, error, neutra | Siempre con texto; color de fondo suave y texto de contraste AA |
| Barra de progreso | vacía, parcial, completa | Con porcentaje o fracción visible |
| Botón | normal, hover, foco, deshabilitado | Un botón principal por vista; los demás secundarios |

---

## 5. HTML autónomo (`preview.html` y todo HTML que use el sistema)

- Un único archivo; **sin recursos externos** (ni scripts, ni hojas de estilo, ni fuentes por URL).
- Los tokens son variables CSS (`--c-fondo`, `--c-acento`, …, `--espacio-4`, `--radio-md`).
- Tema por defecto según `tema-defecto` de `tokens.json` (`claro` si no existe; llega al HTML como la variable CSS `--tema-defecto`), con `data-theme="light"` o `data-theme="dark"` en la raíz (botón de tema) y `prefers-color-scheme: dark` como respaldo sin JavaScript.
- Todo HTML parte de una plantilla de `common/html/` (React, Tailwind y componentes al estilo shadcn/ui, compilados a un archivo): solo se sustituyen el bloque de tokens y el de datos.
- `<meta name="viewport" content="width=device-width, initial-scale=1">`; sin desplazamiento horizontal de página en 360 px de ancho.
- Fondo explícito en `body` y títulos con jerarquía clara.

---

## 6. Cómo lo consumen otras skills

1. Leen `diseno` en `project/config.yaml` (ruta al `DESIGN.md` vigente).
2. Leen `tokens.json` de la misma carpeta; no copian valores a mano.
3. Si `diseno` es `null`, avisan y proponen ejecutar `02-design-system`.

---

## 7. Errores frecuentes y checklist

**Errores:** más de un acento; texto secundario con poco contraste en el tema oscuro; sombras pesadas; componentes sin estados; colores inventados en el HTML que no están en `tokens.json`; fuentes por URL; texto que dice que el contenido es de prueba.

**Checklist:**
- [ ] `tokens.json` tiene las mismas claves en claro y oscuro.
- [ ] Todos los pares declarados cumplen su contraste mínimo en ambos temas.
- [ ] `DESIGN.md` cita solo tokens que existen y documenta los 6 componentes con estados.
- [ ] `preview.html` abre sin conexión, alterna claro y oscuro y no tiene recursos externos.
- [ ] La propuesta fue confirmada por el usuario antes de escribir.
- [ ] Ningún archivo, salvo `README.md`, menciona la procedencia.

---

## Referencias

Kirkpatrick, A., O'Connor, J., Campbell, A., & Cooper, M. (Eds.). (2025). *Web Content Accessibility Guidelines (WCAG) 2.1*. W3C. https://www.w3.org/TR/WCAG21/

*(Lista cerrada: máximo 1 o 2 citas por punto, solo de aquí. Formato APA 7, ver `common/citation-style/APA7.md`.)*
