# Dependencias entre archivos de una corrida de sistema de diseño

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/02-design-system/<corrida>/`). Verifica siempre con `grep -n "<token>" <corrida>/DESIGN.md`.

| Cambio | `tokens.json` | `DESIGN.md` | `preview.html` | Validación a mirar |
|---|---|---|---|---|
| Color (cualquier clave de `color.claro` o `color.oscuro`) | `color.*` | Tabla «Color»; componentes que citan el token | Regenerar (variable `--c-<clave>`) | Contraste de los `pares` que usan esa clave, en ambos temas |
| Acento | `color.*.acento`, `color.*.acento-texto` | Principios, tabla «Color», Botón, Barra de progreso, Accesibilidad | Regenerar | `acento-texto` sobre `acento`; `acento` sobre `fondo` y `superficie` |
| Colores de estado | `color.*.exito`, `alerta`, `error` | Tabla «Color», Etiqueta de estado | Regenerar | Cada estado sobre `superficie` |
| Tipografía (familia, escala, peso, interlineado) | `tipografia.*` | Sección «Tipografía», Encabezado | Regenerar | Familia con pila del sistema como respaldo |
| Espacio, radio o sombra | `espacio.*`, `radio.*`, `sombra.*` | Sección «Espacio, radio y sombra»; componentes que los citan | Regenerar | Tokens citados existentes |
| Componente existente (estados, tokens, regla) | — | Su subsección `###` en «Componentes» | Regenerar solo si cambia un token | Estados, Tokens y Uso presentes; tokens existentes |
| Componente nuevo | — (si necesita tokens nuevos, también `tokens.json`) | Nueva subsección `###` | No aparece en la vista previa (muestra los seis mínimos) | Estados, Tokens y Uso presentes |
| Tema claro/oscuro (cómo se alterna) | — | «Tema claro y oscuro» | Regenerar | `prefers-color-scheme` y `data-theme` presentes |
| `pares` de contraste | `pares` | «Accesibilidad» (lista de pares) | — | Pares con claves existentes y tipo válido |

## Cadenas típicas

- **Cambiar el acento:** `tokens.json` → tabla «Color» y componentes que lo citan → regenerar `preview.html` → recalcular contraste de los pares con `acento`.
- **Cambiar la tipografía:** `tokens.json` → sección «Tipografía» y Encabezado → regenerar `preview.html`.
- **Agregar un componente:** subsección `###` en `DESIGN.md` con Estados, Tokens y Uso; si usa tokens nuevos, primero `tokens.json`.
- **Contraste insuficiente tras el cambio:** ajustar la luminosidad del color hasta cumplir AA o conservar el fork con incidencias y `--no-mover`.
