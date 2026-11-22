# Playbook · Armado del informe

Guía para armar el informe de Inteligencia de Negocios de **una sola entrega** con lo que ya produjeron las skills de contenido (`03` a `11`). Lo ejecuta la skill `12-make-report` con `.claude/skills/_shared/report.py` y escribe en `project/12-report/<DD-MM-AAAA-HH-MM-SS>/`. Las partes que el armado escribe por sí mismo están en [`models/`](models/README.md).

**El armado no redacta contenido de los capítulos**: junta, ordena, numera y señala lo que falta. Si un texto está mal, se corrige con el `-update` de la skill que lo produjo y se vuelve a armar el informe.

---

## 0. Reglas que se aplican siempre

1. **Solo lo disponible.** Entran las secciones con estado `disponible` en `informe.secciones` del config (`projectcfg.py secciones`), en el orden del índice (`common/structure/model1.md`). Las pendientes no aparecen en el informe: van a `faltantes.md` con la skill que las produce. No se pregunta si poner un marcador u omitirlas.
2. **El índice manda en los títulos.** Cada sección sale con el número y el título del índice («1.4. Modelo de negocio: Business Model Canvas»), sin el detalle entre paréntesis ni la marca «(incluye imagen)». Los subtítulos de la sección pasan a nivel 3 o más.
3. **Una sola entrega.** El control del documento no lleva historial de versiones ni marcas de avance.
4. **Nada se inventa.** Curso y docente los informa el usuario; lo que falte queda «Pendiente» y se lista en `faltantes.md`. Las introducciones de capítulo salen de [`models/rep-1-introducciones.md`](models/rep-1-introducciones.md).
5. **El informe no lleva imágenes.** Cada figura es un marcador que el equipo reemplaza a mano antes de entregar.
6. **Texto limpio.** Ningún archivo, salvo el `README.md` de la corrida, dice que el contenido es falso, inventado, de prueba o simulado.

## 1. Contrato con las skills de contenido

Cada corrida de una skill que aporta secciones contiene:

| Archivo | Qué es | Cómo lo usa el informe |
|---|---|---|
| `secciones/<punto>.md` | Texto final de una sección. Abre con `## <punto>. <título del índice>`; los capítulos 4 y 5 usan `secciones/4.md` y `secciones/5.md` con `## 4. …` y `## 5. …` | Se copia bajo el encabezado del índice; el encabezado propio se reemplaza |
| `<!-- figura: <visual> -->` | Línea sola donde va una figura | Se reemplaza por el marcador de imagen (sección 3) |
| `visuales/<visual>.html` | HTML autónomo de la figura | Se copia a `imagenes/<visual>.html` |
| `leer-imagen/<visual>.md` | Viñetas «Para qué sirve», «Qué dice», opcional «Por qué se resalta» y «Pie de foto sugerido» | Da el pie y el párrafo «Cómo leer la figura» |
| `referencias.md` | Opcional: una entrada APA 7 por línea | Se combina en las referencias |
| `anexos/<letra>.md` | Contenido de un anexo (A a D), en la corrida de la skill de su sección de origen | Se agrega como anexo (sección 6) |
| `README.md` | Procedencia de la corrida | **No se copia nada** al informe |

Además, dentro de una sección:
- **Títulos de tabla:** una línea `Tabla N: título` (o `**Tabla N.** título`) justo antes de la tabla. Cada sección numera sus tablas desde 1; el armado las renumera en todo el informe. Una tabla sin título se avisa.
- **Menciones:** «Figura k» y «Tabla k» se refieren a las figuras y tablas de la **misma sección**, contadas desde 1; el armado las cambia por el número final.
- **Figura de otra sección:** `{{figura:<visual>}}` se reemplaza por «Figura N» de esa figura (por ejemplo, «como muestra la {{figura:foda}}»). Así no se repite una figura: se cita por su número.
- **Sin enlaces relativos** a archivos de la corrida de origen: no resuelven desde el informe.

## 2. Portada y control del documento

Plantilla: [`models/rep-0-control-documento.md`](models/rep-0-control-documento.md). Datos: título y tema (`proyecto` del config), empresa (brief vigente, `brief.py leer`), curso y docente (los informa el usuario), integrantes con su rol (`equipo`) y fecha de entrega (`calendario.entrega`). Cierra con la nota de formato: Word o PDF, Arial 11, interlineado 1.5 y márgenes estándar.

## 3. Figuras

Cada `<!-- figura: <visual> -->` pasa a:

```markdown
(INCLUIR IMAGEN: Figura N: <pie>. Archivo sugerido: imagenes/<visual>.html)

**Cómo copiarla.** Abrir [imagenes/<visual>.html](imagenes/<visual>.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** <Para qué sirve>. <Qué dice>. <Por qué se resalta>.
```

- El **pie** es la viñeta «Pie de foto sugerido»; sin ella, el título del punto.
- **Sin HTML:** queda el marcador y «Cómo copiarla» pide ejecutar el `-update` de la skill o insertar una captura propia.
- **Sin explicación:** queda el marcador sin «Cómo leer la figura».
- En ambos casos el armado lo avisa y lo lista en la tabla «Figuras incompletas» de `faltantes.md`.
- Las figuras se **numeran de forma consecutiva** en todo el informe (anexos incluidos) y los HTML se copian a `imagenes/` con su `imagenes/INDICE.md` (archivo, figura, dónde va y skill de origen).
- Un punto con «(incluye imagen)» en el índice debe traer al menos una figura; si no, se avisa y la validación lo informa con el `-update` que lo corrige.

## 4. Capítulos e introducciones

Un capítulo aparece solo si tiene al menos una sección disponible. Abre con la frase de `rep-1-introducciones.md` y «Comprende …» con las secciones incluidas, sin nombrar las pendientes.

## 5. Referencias bibliográficas

Se reúnen las entradas de `referencias.md` de las corridas usadas, una por línea, sin duplicados y en orden alfabético, según `common/citation-style/APA7.md`. Plantilla: [`models/rep-9-referencias.md`](models/rep-9-referencias.md). Si ninguna corrida aporta referencias, la sección dice «Pendiente» y `faltantes.md` lo anota.

## 6. Anexos

| Anexo | Sección de origen | Skill |
|---|---|---|
| A Diccionario de datos y calidad de datos | 3.1 | `08-make-etl` |
| B Scripts del ETL | 3.1 | `08-make-etl` |
| C Medidas y cálculos del dashboard | 3.2 | `09-make-dashboard` |
| D Especificación y capturas del dashboard | 3.2 | `09-make-dashboard` |

Un anexo entra solo si su sección de origen está disponible y su corrida trae `anexos/<letra>.md`; si no, va a `faltantes.md`. Cada anexo incluido va al final de `informe.md` (`# Anexos`, `## Anexo X: título`) y además en `anexos/anexo-<letra>.md`, que es lo que `13-make-annex-html` convierte a HTML.

## 7. Faltantes y procedencia

`faltantes.md` tiene cuatro tablas (secciones, anexos, datos de portada y figuras incompletas) y una nota de referencias. Cada sección del índice está en el informe o en `faltantes.md`, nunca en ambos. El `README.md` de la corrida anota la procedencia: modo de datos, sistema de diseño, corridas usadas por skill, curso y docente informados y los avisos del armado. Es el único lugar donde se anota.

## 8. Formatos de salida

- **Markdown** (`informe.md`): siempre.
- **HTML** (`report.py render`): opcional, autónomo, con los tokens del sistema de diseño del config (o los base, con aviso) y la plantilla de `common/document-html/`.
- **Anexos en HTML:** `13-make-annex-html` (`report.py anexos`).
- **Word o PDF:** los genera el equipo a partir del Markdown con sus herramientas; no se validan.

## 9. Errores frecuentes y checklist

**Errores:** editar a mano el informe en vez de corregir la skill de origen; pegar imágenes en el Markdown; copiar el `README.md` de una corrida; poner un marcador «Pendiente» en lugar de dejar la sección en faltantes; repetir una figura en vez de citarla por su número; numerar tablas a mano en todo el informe.

**Checklist:**
- [ ] Solo hay secciones disponibles, en el orden y con los títulos del índice.
- [ ] Cada pendiente está en `faltantes.md` con su skill.
- [ ] El control del documento tiene los siete datos (o «Pendiente») y no tiene versiones.
- [ ] Cada figura tiene su marcador consecutivo, «Cómo copiarla» y, si hay explicación, «Cómo leer la figura».
- [ ] Las tablas con título están numeradas de forma consecutiva.
- [ ] Las referencias no se repiten y están en orden alfabético.
- [ ] `validate_run.py` responde «sin incidencias».
