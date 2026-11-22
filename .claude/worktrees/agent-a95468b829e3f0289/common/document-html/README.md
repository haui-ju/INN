# Estándar de documento HTML (`common/document-html/`)

Cómo se convierte cada Markdown de una carpeta de anexos (por ejemplo `anexos/dashboard/`) en un HTML autónomo con la **misma cabecera y los mismos estilos** que los visuales de `common/html/`. El conversor es `.claude/skills/_shared/doc_html.py`.

## Qué comparte con el estándar visual
- **Cabecera:** la barra del estándar visual (`common/html/pantalla/index.html` si existe; si no, `common/html/vista-previa/index.html`, que lleva la misma hoja) (escala ×2/×3/×4, «Copiar imagen», «Descargar imagen», tema claro/oscuro y aviso de estado). Se copia el mismo marcado y las mismas clases.
- **Estilos:** la hoja `<style id="estilos">` de esa misma plantilla (botones, selectores, tipografías incrustadas) se lee al construir, así que cambiar el estándar visual cambia también los documentos.
- **Tokens:** el bloque `/*tokens:inicio*/ … /*tokens:fin*/` de `<style id="tokens">` recibe las variables del `tokens.json` del sistema de diseño vigente (claro y oscuro).
- **Captura:** «Copiar imagen» y «Descargar imagen» rasterizan el área `main#captura` igual que los visuales, sin el botón de la barra.

## Lo que añade para documentos
- `documento.css`: estilo de texto (títulos en serif, párrafos, listas, casillas, tablas, citas, código), solo con variables de token.
- Ruta de migas, navegación al documento anterior y siguiente de la misma carpeta, y pie con la ruta de origen.
- Un HTML por cada `.md`, con la misma ruta relativa bajo `html/`, y `html/index.html` con el árbol completo.

## Reglas
1. **Un HTML por cada `.md`**: `dashboard/paginas/resumen.md` pasa a `dashboard/html/paginas/resumen.html`.
2. **Autónomo:** un solo archivo, sin recursos externos (`src`, `<link>`, `@import`). Los enlaces a sitios externos que ya están en el texto se conservan.
3. **Título:** `<title>` es el primer encabezado `#` del `.md`.
4. **Enlaces entre documentos:** los enlaces relativos a `.md` pasan a `.html`, conservando el ancla.
5. **Saltos de línea:** cada línea de un párrafo se conserva como línea (`<br>`), porque los registros usan una línea por campo.
6. **Elementos:** encabezados con `id`, párrafos, listas anidadas, listas numeradas, casillas `[ ]` y `[x]` (solo lectura), tablas, citas, bloques de código, línea horizontal, negrita, cursiva, código y enlaces.
7. **Accesibilidad:** idioma `es`, encabezados jerárquicos, tablas con `<th scope="col">`, foco visible, enlace «Saltar al contenido» y versión imprimible sin barra.
8. **Enlaces a otros archivos:** los enlaces relativos que no van a un `.md` (por ejemplo `../imagenes/foda.html`) se reubican para que resuelvan desde la carpeta `html/`.
9. **El texto no se modifica.** El HTML refleja el `.md`; si algo está mal se corrige en el `.md` de origen y se regenera.

## Cómo se genera
- Con el informe: `13-make-annex-html` (o `report.py anexos`) escribe los HTML de los anexos de la corrida vigente de `12-make-report`.
- Por separado: `doc_html.py construir --origen <carpeta> --salida <carpeta>/html --tokens <tokens.json|base> --raiz . --nombre "<título>"`, y `comprobar` con los mismos argumentos.

## Qué se comprueba
Que haya un HTML por cada `.md` y ninguno de más, que cada HTML coincida con lo que se genera hoy desde su `.md`, que no cargue recursos externos y que todo enlace relativo apunte a un archivo que existe.

## Tamaño
Cada página lleva las fuentes incrustadas (unos 150 KB), así que es autónoma pero pesa. Es la contrapartida de no depender de nada externo.
