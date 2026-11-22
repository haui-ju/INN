# Design

## Context

Ver `proposal.md` (Why). Estado de partida (commit de `bi-base-pipeline`):

- `pipeline.json` ya declara `03-make-business-diagnosis` (1.1 a 1.4), `04-make-strategic-analysis` (1.5 a 1.7) y `05-make-problem-objectives` (1.8 a 1.10) con sus carpetas numeradas; `projectcfg.py register` marca esas secciones como disponibles.
- `validate_run.py` carga `rules/<carpeta sin número, con _>.py` y aplica `PREFIJOS` (códigos citados sin definir dentro de la corrida) y `validar(run)`.
- `visuales.py` tiene los registros vacíos a propósito; sus extractores leían antes un `capitulo-1.md` del pipeline viejo (etiqueta `pre-bi-pipeline`) y no aceptaban una corrida concreta.
- `common/html/` conserva `foda` (cuatro cuadrantes, mock de innovación) y `vista-previa` (textos de sprints). `_build` compila con `npm install && npm run build` (en este entorno funcionó).
- `12-make-report` se construye en paralelo con un contrato fijo: `secciones/<punto>.md`, `<!-- figura: <visual> -->`, `visuales/<visual>.html`, `leer-imagen/<visual>.md`, `referencias.md` opcional y `README.md`.

## Goals / Non-Goals

**Goals:**
- Tres skills de contenido con su `-update`, playbook, plantillas, validador y pruebas, que producen exactamente el contrato de secciones.
- Articulación verificable del capítulo: el Ishikawa parte del problema del brief, la problemática toma sus causas del Ishikawa y la matriz vincula cada `OE` con causas, FODA, PESTEL, Canvas e indicador.
- Cuatro visuales HTML compilados que cumplen el contrato de `common/html/`.

**Non-Goals:**
- Ensamblar el informe, numerar figuras o resolver `<!-- figura -->` (es de `12-make-report`).
- Cambiar `pipeline.json`, el índice o `_shared/README.md`.
- Buscar fuentes en la web desde el kit: la skill lo hace con sus herramientas y el kit solo valida forma y coherencia.

## Decisions

**D1. Un módulo compartido de lectura del capítulo 1 (`_shared/diagnostico.py`).**
Lee el índice para obtener los títulos exactos, parsea las secciones de las corridas de `03`, `04` y `05` a datos estructurados y ofrece las comprobaciones comunes (encabezado, figuras, marcador de datos modelados, citas contra `referencias.md`). Lo usan los tres validadores, los extractores de `visuales.py` (importación diferida para evitar el ciclo con `brief.py`) y las skills por CLI (`diagnostico.py leer --paso …`). Alternativa: repetir el parseo en cada regla; se descarta porque `05` necesita leer `03` y `04` con el mismo criterio que sus validadores.

**D2. Título exacto del índice = texto del punto sin los paréntesis finales.**
`- 1.4. Modelo de negocio: Business Model Canvas (los nueve bloques del lienzo) (incluye imagen)` da `## 1.4. Modelo de negocio: Business Model Canvas`. Es la lectura natural del contrato y no exige tocar el índice. *Para revisar:* si `12-make-report` usa otro criterio, ambos deben alinearse a este.

**D3. Las tablas de las secciones son la fuente de datos (sin archivos intermedios).**
Cada sección lleva tablas con encabezados fijos (por ejemplo `| Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente |`); el validador, los extractores y la skill `05` leen esas tablas. Alternativa: un JSON aparte por sección; se descarta porque duplicaría la fuente de verdad y el informe debe mostrar las tablas de todos modos.

**D4. Códigos de trazabilidad.**
PESTEL: `POL`, `ECO`, `SOC`, `TEC`, `AMB` (ecológico/ambiental, para no chocar con `ECO`) y `LEG`. FODA: `FOR`, `DEB`, `OPO`, `AME`. Estrategias cruzadas: `FO`, `FA`, `DO`, `DA` (el código es el tipo). Ishikawa: `CAU`. Los objetivos conservan `OG` y `OE` del brief. En `05`, `PREFIJOS` solo incluye `OG` y `OE` (definidos en su corrida); los códigos de `04` se validan contra la corrida vigente de `04`.

**D5. Valores por defecto tomados sin consultar (para revisión del usuario).**
- *Categorías del Ishikawa:* las 6M fijas (Método, Mano de obra, Materiales, Maquinaria, Medición, Medio ambiente); mínimo seis causas en al menos cuatro categorías.
- *Cantidades:* PESTEL al menos un hallazgo por factor (referencia 1 a 3); FODA al menos un ítem por cuadro (referencia 3 a 5) y al menos una estrategia por tipo; causas principales en 1.8 entre dos y cuatro.
- *Tamaño:* rangos de la Ley 30056 (micro hasta 150 UIT, pequeña hasta 1700, mediana hasta 2300; por encima, gran empresa); tolerancia de una UIT en el cálculo. La UIT del ejemplo es S/ 5 500 (2026), tomada del caso de `chat.md`; la guía pide confirmarla con el decreto supremo del año. Las ventas pueden quedar «Pendiente» solo si la categoría se declara con su fuente.
- *Misión y visión:* se reproducen de `domain.md`; el validador exige igualdad normalizada cuando `domain.md` las tiene.
- *RUC con `tipo: propio`:* la celda empieza con «No aplica».
- *Oportunidades y amenazas:* cada una cita un código PESTEL o una fuente (Autor, año).
- *Matriz de articulación:* en 1.10, columnas `Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador`; PESTEL admite «—»; FODA admite ítems y estrategias; cada causa principal debe quedar cubierta.
- *Citas:* se comprueba que cada cita (Autor, año) o Autor (año) tenga en `referencias.md` una línea con ese año y el primer apellido; si el autor es una sigla (INEI, BCRP), basta una entrada con ese año (validación tolerante para autores corporativos).
- *Visual FODA:* se amplía con `estrategias` (lista con `codigo`, `tipo`, `texto`, `combina`); el mock pasa al caso Pollería Don Tito.
- *Visual BMC e Ishikawa:* ancho completo y `anchoImagen` 1560; PESTEL y FODA, ancho fijo 1120.
- *Ejemplos:* caso Pollería Don Tito de `chat.md` con `tipo: propio` (sin RUC), para no publicar un RUC que podría pertenecer a otra empresa.

**D6. Las pruebas usan los ejemplos de las plantillas como corridas.**
Como `brief_fixtures.py`, un fixture arma `03`, `04` y `05` con el último bloque ```markdown``` de cada plantilla, construye los visuales y registra las corridas. Así los ejemplos documentados siempre validan. Alternativa: fixtures escritos aparte; se descarta porque se desincronizan de las plantillas.

**D7. Extracción por corrida (`--run`).**
Los extractores aceptan el nombre de la corrida; sin él usan la vigente. La skill construye los visuales antes de registrar, cuando el config aún apunta a la corrida anterior. Los visuales se generan siempre con `visuales.py construir`, nunca a mano.

**D8. Visuales compilados con React y SVG/CSS propio.**
El Ishikawa se dibuja con una rejilla (categorías arriba y abajo, espina central con flecha y cabeza con el efecto) y líneas SVG por token, sin librerías; en teléfono se desplaza dentro de su cuadro. El BMC usa la disposición clásica de diez columnas en escritorio y una columna en teléfono. Se reutilizan `Panel`, `Badge`, `Encabezado` y `SinDatos`.

**D9. Vista previa del sistema de diseño con ejemplos de BI.**
Se reemplazan los textos de sprints (tareas, historias, avance) por ejemplos de BI (KPI, ETL, dashboard) sin cambiar la estructura de la vista.

## Risks / Trade-offs

- [El ensamblado paralelo interpreta distinto el título o la marca de figura] → D2 y el contrato quedan en las specs; los validadores comprueban el encabezado exacto.
- [Validación de citas tolerante con siglas] → puede dejar pasar una referencia corporativa mal escrita; se acepta a cambio de no exigir un formato no estándar en APA.
- [Igualdad estricta de misión y visión con `domain.md`] → obliga a corregir primero `domain.md`; se documenta en la guía y en las dependencias del `-update`.
- [Cambiar el esquema del mock de `foda`] → la prueba de `limpiar` y el README se actualizan; ningún proyecto usa aún el visual.
- [Recompilar cambia los hashes de `foda` y `vista-previa`] → se recompila todo y se actualiza el manifiesto con `npm run build`.

## Migration Plan

No hay corridas previas de estas skills. Se implementa por grupos (kit común, `03`, `04`, `05`, visuales) con pruebas en cada uno; al final, `unittest`, `npm run check:pipeline` y `html_tpl.py comprobar` en verde. Reversión: revertir el commit del change.
