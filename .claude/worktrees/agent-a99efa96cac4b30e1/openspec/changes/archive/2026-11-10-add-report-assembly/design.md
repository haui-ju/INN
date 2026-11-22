# Design

## Context

Estado observado: `pipeline.json` define `19-make-report` (requiere `18-make-final-analysis`, sin `update`). El índice marca cada punto con `[A1]`, `[A2]` o `[A3]` (un `+` indica que se actualiza en los siguientes) y define el historial de versiones, la portada del control del documento y las reglas de contenido (no repetir, figuras con pie de foto con código, cifras con fecha, no renumerar 3.1.x ni los anexos B, D, E y F). Cada skill escribe sus archivos con encabezados que llevan el número del punto (`## 4.2.`, `## 5.1.`, `## 6.1.3.`…); el Design Thinking entrega `documento.md` y `anexos.md`; el análisis final, `analisis-consolidado.md` y `conclusiones.md`; los informes de sprint, `informe-avance-N.md` y `acta-review-retro.md` con evidencias en la bitácora; los tableros, HTML y `data.json`. `projectcfg.check` revisa los prerrequisitos de `requiere` sin distinguir avances. `boards.py` ya tiene utilidades de tokens y fechas. Python de la biblioteca estándar.

## Goals / Non-Goals

**Goals:** documento por avance completo, ordenado y trazable; saber qué falta antes de entregar; cero redacción manual del armado.

**Non-Goals:** redactar contenido de los capítulos, manual de usuario, conversión a Word o PDF, ejecutar las skills.

## Decisions

### D1. Documento acumulado
`informe-avance-N.md` incluye todos los puntos del índice cuya primera marca es ≤ N (los `+` se incluyen desde su primera marca y se toman de la corrida vigente, que puede estar actualizada). Un punto de un avance posterior **no** aparece. Las versiones previas no se tocan: cada ejecución crea una corrida nueva.

### D2. Correspondencia punto → paso (`report_map.json`)
Cada fuente se declara con su paso, sus archivos y, donde aplica, el sprint: `03` → `capitulo-1.md` (1.x); `04` → `capitulo-2.md` y `referencias.md` (2.x); `05` → `documento.md` (3.1.x) y `anexos.md` (anexos B, D.1 a D.3, E y F); `07` → `seccion-3-2.md`, `seccion-3-3.md` y `canvas-v1.md` (3.2 a 3.4); `17` → `resultados.md` y `decision.md` (se añaden a 3.2.3 y 3.2.4); `08` → `equipo-scrum.md` y `artefactos.md` (4.1.x); `09` → `rf.md`, `rnf.md` (4.2 y 4.3); `10` → historias, `backlog.md` y `criterios-dod.md` (4.4 y 4.5); `11` → `plan-sprints.md` y `gantt-linea-base.md` (4.6.x); `12` → `ceremonias.md` y `kanban.md` (4.7 y 4.8); `14` → `arquitectura.md`, `modelo-datos.md`, `interfaz.md`, `plan-pruebas.md` (5.1 a 5.3 y 5.5.1) y `diagramas/` (D.4); `15` → `bitacora.md` (5.4.x); `16` (por sprint) → `informe-avance-N.md` (6.N.x) y `acta-review-retro.md` (A.3); `18` → `analisis-consolidado.md` (6.4.x) y `conclusiones.md` (7.x); `13` → HTML y `data.json` (A.1 y A.2, por referencia). El bloque de un punto es el texto desde su encabezado numerado hasta el siguiente de igual o menor nivel.

### D3. Puntos derivados y sin fuente
Derivados mecánicos: **5.5.2** (tabla de resultados de pruebas de la bitácora) y **5.5.3** (remisión a 3.1.6 y 6.4.4). Sin skill y por tanto siempre en `faltantes.md` salvo que el usuario aporte un archivo en `anexos/`: **A.4** y **anexo C**.

### D4. Numeración y niveles
Cada encabezado numerado se reemplaza por el número y el título del índice, con el nivel `#` correspondiente a su profundidad (capítulo `#`, punto `##`, subpunto `###`…); los encabezados sin número del bloque conservan su nivel relativo. Los puntos salen en el orden del índice.

### D5. Figuras y evidencias
Las líneas «Pegar» de los informes de sprint se convierten en imágenes con pie `Figura X: …` y las evidencias se copian a `evidencias/`; «Sin captura» queda como nota. Las figuras se renumeran de forma consecutiva en todo el documento y las menciones «Figura k» de cada bloque se actualizan. Todo pie lleva un código de trazabilidad (`HU-02`, `REQ-02`…) o una fecha `DD-MM-AAAA`.

### D6. Faltantes y pendientes
`faltantes.md` (`Punto | Título | Paso que lo produce | Qué hacer`) lista todo punto con marca ≤ N sin fuente. Con `--pendientes marcador`, el punto aparece con su encabezado y `**Pendiente.** …`; con `omitir`, no aparece. En ambos casos figura en `faltantes.md`, y un punto con fuente nunca figura.

### D7. Portada y control del documento (`rep-0-control-documento.md`)
`# Informe · [proyecto]`, datos de portada (tema, equipo, avance) y la tabla de historial de versiones con una fila por versión ≤ N: avance, fecha (la de `avances` del config), capítulos que cambian (los del índice) y cambios principales (lo informa el usuario).

### D8. Referencias bibliográficas (`rep-9-referencias.md`)
Lista cerrada de las referencias verificadas de los playbooks (formato APA). El armado compila `Referencias bibliográficas` con las que el texto cita; la validación exige que toda cita tenga entrada y toda entrada esté citada. Una cita fuera de la lista cerrada es una incidencia.

### D9. Referencias cruzadas y no repetición
Toda referencia «punto X.Y», «véase X.Y» o «anexo A.n» apunta a un número del índice; los enlaces a anexos y evidencias resuelven. Ningún párrafo de ocho o más palabras aparece dos veces en el documento.

### D10. Salida y formatos
Markdown siempre. `report.py render` genera un HTML autónomo con los tokens del sistema de diseño (`diseno` del config o los base, con aviso), sin recursos externos. Otras conversiones las elige el usuario con herramientas propias y no se validan. La vista privada solo se publica con confirmación explícita y su enlace va en el `README.md` de la corrida.

### D11. Prerrequisitos por avance
`pipeline.json` añade a la skill 19 `requiere_por_avance` (`"1"`, `"2"`, `"3"`: los pasos que alimentan cada avance según el índice) y `projectcfg.py check --skill 19-make-report --avance N` avisa solo de esos; sin `--avance` usa la unión. El campo es opcional para las demás skills.

### D12. Validación
`rules/report.py` (`PREFIJOS` vacío: el armado no define códigos) comprueba la estructura, todos los puntos con marca ≤ N presentes (o en `faltantes.md`), ninguno posterior, títulos y orden del índice, historial de versiones con las fechas del config, figuras, referencias bibliográficas, referencias cruzadas, no repetición, que `faltantes.md` coincida con lo que se calcula y, si hay HTML, que sea autónomo y contenga los mismos encabezados.

## Risks / Trade-offs

- [Fuente con encabezados sin número] → el armado informa el archivo y el punto como faltante en vez de adivinar.
- [Documento acumulado enorme] → lo extenso ya va a los anexos desde los pasos anteriores; el armado no duplica.
- [Cambió una corrida después de armar] → la skill avisa en el `README.md` qué corridas usó; para actualizar se vuelve a ejecutar.
- [Citas que las fuentes escriben distinto] → la lista cerrada y la validación detectan cualquier diferencia.
- [Anexo C y A.4 sin skill] → quedan en `faltantes.md` de forma explícita.

## Migration Plan

Se agrega un campo opcional a `pipeline.json`, un argumento a `projectcfg.py check` y una carpeta registrada en `validate_run.py`. Sin migración de datos.

## Open Questions

- Si más adelante conviene una skill para el manual de usuario (anexo C).
