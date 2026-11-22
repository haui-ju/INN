# Design

## Context

Ver `proposal.md` (Why). Estado que condiciona el enfoque:

- `pipeline.json` ya declara `12-make-report` (carpeta `12-report`, sin `-update`) y `13-make-annex-html` (sin carpeta). `projectcfg.secciones()` devuelve `[{seccion, skill, estado, run, motivo}]` y degrada a pendiente una sección cuya carpeta de corrida no existe; `run_dir()` da la carpeta de una corrida.
- El índice `common/structure/model1.md` tiene cinco capítulos (puntos `- N.M. Título (detalle) (incluye imagen)`), Referencias y anexos A a D. La spec `report-index-structure` exige `cargar_indice` con `imagen` por punto.
- El molde está en la etiqueta `pre-bi-pipeline` (`19-make-report`, `20-make-annex-html`, `report.py`, `report_prosa.py`, `rules/report.py`, sus pruebas y `common/report/`). Era un armado por avances con 18 pasos, trasladables, anexo G, Design Thinking y Miro.
- `doc_html.py` lee la hoja de estilos del estándar visual de `common/html/pantalla/index.html`, que se retiró en `bi-base-pipeline`; hoy no puede construir ningún HTML.
- Las skills 03 a 05 se construyen en paralelo con el contrato de corrida de la spec `report-assembly`.

## Goals / Non-Goals

**Goals:**
- Un `report.py` pequeño y sin dependencias de lo retirado, que arme el informe desde el registro de secciones y el contrato de corrida.
- Validador por carpeta (`rules/report.py`) y pruebas con corridas propias de 03, 04 y 05, independientes de las skills reales.

**Non-Goals:**
- Redactar contenido de capítulos, pasar tablas a prosa o controlar la densidad de códigos (eran del molde; aquí el contenido lo escribe cada skill).
- Publicar el HTML como vista privada o generar Word o PDF.
- Producir anexos: hoy ninguna skill los escribe.

## Decisions

**D1. Lo que se reutiliza del molde y lo que no.**
Se toman la portada (como control del documento sin versiones), el marcador `(INCLUIR IMAGEN: …)` con «Cómo copiarla» y «Cómo leer la figura», la renumeración de figuras y de sus menciones, `imagenes/INDICE.md`, los faltantes, el render HTML y las comprobaciones genéricas del validador (figuras, imágenes incrustadas, encabezados del HTML). Se descartan avances, sprints, `report_map.json`, trasladables y anexo G, Design Thinking, Miro, lista cerrada de referencias, propósitos de tabla y densidad de códigos. Alternativa: copiar el molde y recortarlo; se descarta porque casi todo su código depende de módulos retirados.

**D2. La fuente de verdad del armado es `projectcfg.secciones()` más el contrato de corrida.**
`report.py` no tiene mapa propio punto → paso: la skill y la corrida salen del registro del config, y el archivo es siempre `secciones/<punto>.md`. Una sección disponible sin su archivo se trata como pendiente con la causa. Alternativa: un `report_map.json` como en el molde; duplica `pipeline.json`.

**D3. Encabezados: el título lo pone el índice.**
El título de un punto es el texto de su línea en el índice sin la marca «(incluye imagen)» ni el detalle final entre paréntesis («1.4. Modelo de negocio: Business Model Canvas»). El encabezado de la fuente se reemplaza por `## <punto>. <título>` (también en 4 y 5) y los subtítulos de la sección conservan su nivel. Si la fuente no abre con el encabezado de su punto, se avisa y se usa el texto completo. Así una diferencia de redacción en el título de la fuente no rompe el informe.

**D4. Estructura del documento.**
`# Informe · <nombre>`, `## Control del documento` (tabla Campo | Dato y la nota de formato Arial 11, interlineado 1.5), `# Capítulo N: <título>` con su introducción, `## <punto>. <título>`, `# Referencias bibliográficas` y, si hay alguno, `# Anexos` con `## Anexo X: <título>`. Los capítulos de un solo punto conservan el encabezado `## 4.` para que la numeración sea uniforme.

**D5. Curso y docente se preguntan; por omisión «Pendiente».**
El índice pide curso y docente en la portada, pero el config no los guarda. La skill los pregunta y los pasa con `--curso` y `--docente`; sin respuesta quedan «Pendiente» y se listan en `faltantes.md` como datos de portada. Alternativa: agregarlos al config; cambia el esquema del config para dos datos que solo usa el informe.

**D6. Introducciones de capítulo desde el playbook.**
`common/12-report/models/rep-1-introducciones.md` tiene una tabla Capítulo | Introducción; el armado añade una frase con las secciones incluidas («Este capítulo desarrolla 1.1 Nombre de la empresa, …»). El armado no redacta nada que no esté en el playbook.

**D7. Figuras.**
Pie: la viñeta «Pie de foto sugerido» de `leer-imagen/<visual>.md`; sin ella, el título del punto. «Cómo leer la figura» une en un párrafo las viñetas «Para qué sirve», «Qué dice» y «Por qué se resalta» (rótulos desconocidos entran como «Rótulo: texto»). Sin HTML: la línea «Cómo copiarla» pide ejecutar la skill o insertar una captura propia. Los avisos de figura van a `faltantes.md` (tabla aparte) y a la salida de `construir`. El marcador sigue el contrato: sin punto final antes del paréntesis de cierre.

**D8. Tablas.**
Un título de tabla es una línea que empieza con «Tabla N» (con o sin negrita, seguido de `.` o `:`). Cada sección numera desde 1 y el armado renumera de forma global, igual que las figuras, y actualiza sus menciones. Una tabla sin título se avisa, no se inventa su título. Alternativa: insertar títulos automáticos; se descarta porque el armado no redacta.

**D9. Anexos.**
Origen fijo en `report.py`: A y B salen de la corrida de la sección 3.1 (`08-make-etl`), C y D de la de 3.2 (`09-make-dashboard`), en `anexos/<letra>.md`. Un anexo incluido va dentro de `informe.md` (el documento de entrega es uno solo) y además en `anexos/anexo-<letra>.md`, que es lo que convierte `13-make-annex-html`. Las figuras de un anexo usan `../imagenes/` en su archivo propio. Alternativa: declarar los anexos en `pipeline.json`; se descarta para no cambiar su esquema mientras ninguna skill los produce.

**D10. Referencias.**
Una entrada por línea de `referencias.md` (se acepta una viñeta `- ` inicial; se ignoran vacías y encabezados), sin duplicados por texto normalizado y ordenadas alfabéticamente sin tildes. Sin entradas, la sección dice «Pendiente» y se lista en faltantes. No hay lista cerrada: cada skill responde por sus citas.

**D11. CLI.**
`plan` (texto o `--json`), `construir --salida RUN [--curso] [--docente]`, `render RUN/informe.md` (HTML con `doc_html` y los tokens del config) y `anexos [--run] [--comprobar]` (lo usa `13-make-annex-html`, resuelve la corrida vigente y los tokens). `--raiz` o `PROJECT_ROOT` para pruebas.

**D12. `doc_html.py` toma los estilos de `common/html/vista-previa/index.html`.**
Es la plantilla compilada que siempre existe y lleva la misma hoja `<style id="estilos">`. Se usa `pantalla` si vuelve a existir. Además, como el HTML queda en `html/` (un nivel más abajo que su `.md`), `doc_html` reubica los enlaces relativos a archivos que no son `.md` (por ejemplo `../imagenes/<visual>.html` de un anexo) para que resuelvan desde el HTML; sin eso, `comprobar` los marca rotos. Son los únicos cambios fuera del ensamblado y se anotan en `common/document-html/README.md`.

**D13. Validación autocontenida.**
`rules/report.py` compara el informe con su propio `faltantes.md` (cada sección en uno solo) en lugar de recalcular desde el config, para que una corrida vieja siga validando aunque el config avance. La marca «(incluye imagen)» sin marcador en una sección incluida es incidencia: el índice la exige y se corrige con el `-update` de la skill de origen.

**D14. Menciones entre secciones con `{{figura:<visual>}}`.**
Las menciones «Figura k» se interpretan dentro de la sección (contadas desde 1), porque la skill de origen no conoce la numeración final. Para citar una figura de otra sección sin repetirla, el texto puede usar `{{figura:<visual>}}`, que el armado cambia por «Figura N»; es opcional y queda en la guía, no en el contrato obligatorio, para no exigir más a las skills 03 a 05. Una referencia sin resolver es incidencia del validador.

**D15. Defaults sin preguntar al usuario.**
Por indicación del encargo, las decisiones abiertas se resolvieron con valores por omisión: origen de los anexos (D9), curso y docente como «Pendiente» (D5), introducciones fijas (D6), sin lista cerrada de referencias (D10) y avisos en lugar de errores para figuras incompletas (D7). Todas se pueden revisar sin cambiar el contrato de corrida.

## Risks / Trade-offs

- [Las skills 03 a 05 interpretan el contrato distinto] → el armado es tolerante (título reemplazado, rótulos libres en leer-imagen, viñeta opcional en referencias) y avisa en vez de fallar; las pruebas usan fixtures escritos según la spec.
- [Validación que falla por la fuente (marca de imagen sin figura)] → el mensaje nombra la skill de origen y su `-update`.
- [Enlaces relativos dentro de una sección que no resuelven en el informe] → la guía pide no usarlos; `validate_run` los informa como enlaces rotos.
- [Anexo duplicado en `informe.md` y `anexos/`] → ambos salen del mismo texto en la misma ejecución; no se editan a mano.

## Migration Plan

No hay corridas de informe que migrar (el `project/` está vacío). Reversión: borrar las skills 12 y 13, `report.py`, `rules/report.py`, sus pruebas y `common/12-report/`, y restaurar `doc_html.py`.
