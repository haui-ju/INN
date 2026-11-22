# Plantillas HTML (`common/html/`)

Visuales ya hechos, autónomos y con el estilo de [`DESIGN.md`](DESIGN.md). Una skill **no genera** HTML: **copia** la plantilla y solo sustituye dos bloques.

| Plantilla | Para qué | Datos |
|---|---|---|
| [`vista-previa/`](vista-previa/) | Vista previa del sistema de diseño | proyecto y `tokens.json` |
| [`foda/`](foda/) | Matriz FODA en cuatro cuadrantes (1.6) | se registra con la skill del capítulo 1 que la produce |

Los visuales del pipeline de BI (Business Model Canvas, PESTEL, Ishikawa, arquitectura, modelo de datos y maqueta del dashboard) se agregan aquí con la skill que los produce.

Cada carpeta tiene `index.html` (la plantilla), `README.md` (qué se cambia, esquema y captura) y `mock.json` (datos de ejemplo con el esquema completo: lo que se ve al abrir `index.html`).

**Los datos de ejemplo no se usan en un proyecto.** La skill parte de la versión vacía del mock (`html_tpl.py limpiar --visual <nombre>`: mismas claves, sin contenido) y la rellena con los datos reales.

## Contrato de una plantilla
1. **Un solo archivo, sin recursos externos.** React, Tailwind, componentes y fuentes van incrustados.
2. **Dos bloques sustituibles, nada más:**
   - **Tokens:** `/*tokens:inicio*/ … /*tokens:fin*/` dentro de `<style id="tokens">`: variables CSS de color claro y oscuro, tipografía, espacio, radio y sombra. Los componentes las leen a través del tema de Tailwind, así que cambiar de sistema de diseño es cambiar este bloque.
   - **Datos:** `<script type="application/json" id="datos">…</script>`.
3. **Tema claro por defecto**; el oscuro se activa con el botón y se recuerda.
4. **Botones de imagen:** «Copiar imagen» y «Descargar imagen», con selector ×2, ×3 y ×4. El PNG se llama `<visual>.png` (o `<visual>-<fecha>.png` si el visual tiene fecha de corte). Los botones no salen en la imagen. Si el navegador no permite copiar, descarga y lo avisa.
5. **Fecha visible** dentro del área de captura cuando el visual muestra datos a una fecha.
6. **Los indicadores son los de `calculado`:** el visual da formato, nunca recalcula.

## Cómo se usa (desde Python)
```
python3 .claude/skills/_shared/html_tpl.py copiar --visual foda --datos datos.json --tokens base|<tokens.json> --salida foda.html
python3 .claude/skills/_shared/html_tpl.py limpiar --visual foda   # el mock sin datos
python3 .claude/skills/_shared/html_tpl.py comprobar      # ¿las plantillas coinciden con sus fuentes?
```
`render_preview.py` y `visuales.py construir` lo hacen por ti. Los visuales de datos del informe se extraen del markdown de las corridas con `visuales.py extraer` (ver `visuales.py disponibles`).

## Cómo se reconstruyen (solo desarrollo)
Las fuentes están en `_build/src/` (React, Tailwind y componentes al estilo shadcn/ui). Hace falta `node`:
```
cd common/html/_build && npm install && npm run build
```
`npm run build` compila cada visual, deja en cada `index.html` los tokens base y su `mock.json` y actualiza `_build/manifiesto.json`. `node_modules` no se versiona. Una prueba falla si cambias una fuente y no recompilas.

## Cómo agregar un visual
1. Crea `_build/src/visuales/<nombre>/` con `meta.json`, `modelo.js` (puro: datos → modelo, con el formato de los indicadores), `Vista.jsx` (pinta el modelo con los componentes de `_build/src/ui/`) e `index.jsx` (monta la app).
2. Crea `common/html/<nombre>/mock.json` (datos de ejemplo con el esquema completo; `limpiar` los vacía) y `README.md`.
3. Compila con `npm run build`, revisa el visual en claro, oscuro y 360 px, y agrega sus pruebas.
4. Respeta [`DESIGN.md`](DESIGN.md): componentes existentes, colores y tipografías solo por token.
