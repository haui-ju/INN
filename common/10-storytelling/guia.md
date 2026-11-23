# Playbook del storytelling con datos (sección 4)

Guía para que un agente redacte la sección 4 del informe de BI (`common/structure/model1.md`): la narrativa que convierte los resultados del dashboard en decisiones. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `10-make-storytelling` (y lo ajusta `10-make-storytelling-update`). Escribe en `project/10-storytelling/<DD-MM-AAAA-HH-MM-SS>/`. **La skill no mide nada:** cuenta lo que el equipo midió en el dashboard y entregó en `valores.json` y en las capturas de `09-make-dashboard`. Si falta algo de eso, se detiene.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. `valores.json` y `capturas/` de la corrida vigente de `09-make-dashboard` y su sección 3.2 (qué KPI se ve en qué página). **Sin `valores.json` la skill se detiene** y pide que primero se entreguen los valores del dashboard.
2. `modelo.json` y la sección 2.5 de la corrida vigente de `07-make-data-model-kpi`: nombre, meta con su comparador («o más», «o menos») y objetivo de cada KPI.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): objetivos `OE-nn`, **usuarios** y **decisiones**.
4. Las secciones 1.8 a 1.10 (problemática y objetivos) para el contexto.

### 0.2 Preguntar y confirmar
Antes de escribir, muestra la propuesta (plantilla `st-2-propuesta`): una fila por hallazgo con su objetivo, KPI, valor frente a su meta, captura, quién decide y la decisión. Comprueba que **cada objetivo específico** tiene al menos un hallazgo y **espera la confirmación**. Pregunta solo lo que falte: qué decisión le importa más a cada usuario o si un KPI debe contarse junto con otro.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/4.md`: la primera línea es el encabezado exacto (`## 4. Storytelling con datos`); después, solo texto final. Una captura por hallazgo se marca con `<!-- captura: pag-nn -->` en una línea sola.
- `capturas/pag-nn.png` (y `pag-nn.md` con el pie): copias de las de 09 que la sección cita. `12-make-report` busca la captura en la corrida **de la propia sección**, por eso se copia.
- `referencias.md` si se cita (APA 7) y `README.md` con la procedencia (corridas de 07 y 09 de las que salen los valores).
- **Título de cada tabla:** antes de cada tabla va una línea `Tabla N: título`.

### 0.4 Códigos
`HLZ-nn` (hallazgo): primera celda de la tabla y encabezado `### HLZ-nn. Título` de su narrativa. Se numeran sin repetir. `OE-nn` y `KPI-nn` se citan, no se vuelven a definir.

### 0.5 Texto limpio
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Lo desconocido, como una meta que nadie fijó, dice «Sin meta».

---

## 1. Qué es un hallazgo

Un hallazgo responde, con un dato, a **una pregunta que el usuario tiene que resolver**. Tiene siempre las mismas piezas:

| Pieza | Qué es | De dónde sale |
|---|---|---|
| Objetivo | El `OE-nn` al que contribuye | brief; es el mismo que mide el KPI en `modelo.json` |
| KPI | El indicador que sostiene el hallazgo | `modelo.json` |
| Valor real y meta | Lo que mostró el dashboard frente a lo que se esperaba | `valores.json` y la meta de 2.5, copiada tal cual |
| Estado | `Cumple`, `No cumple` o `Sin meta` | se **calcula** con el comparador de la meta |
| Captura | La página del dashboard que lo muestra | la página de 3.2 donde se ve ese KPI |
| Quién decide | Un usuario del brief | brief |
| Decisión que apoya | Qué hace distinto esa persona al ver el dato | brief (decisiones) |

**Orden de la narrativa:** contexto (por qué importa) → hallazgo (qué muestra el dato) → decisión (qué cambia). Cada hallazgo se escribe en ese orden, en pocas frases.

## 2. Estructura de la sección 4

1. **Declaración de origen.** Con `modo_datos: generado`, el primer párrafo dice que los hallazgos se basan en **datos generados para el proyecto** y medidos por el equipo en el dashboard, y que **no describen el negocio real de una empresa**. Con datos reales, dice de dónde vienen y quién los autorizó.
2. **Contexto.** `**Contexto.**` Un párrafo con la problemática y quién decide, tomado del capítulo 1. Es el único lugar donde pueden aparecer cifras de la problemática; no cites aquí valores del dashboard.
3. **Hallazgos.** `**Hallazgos.**`, la tabla `Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya` con su título `Tabla N: …`, y debajo un bloque `### HLZ-nn. Título` por hallazgo, con su captura (si es la primera vez que aparece) y dos rótulos: `**Qué muestra.**` y `**Qué decisión apoya.**`.
4. **Prioridades.** `**Prioridades.**` Qué decisión se toma primero y por qué, usando solo las brechas entre valor y meta que ya están en la tabla.
5. **Metas pendientes.** `**Metas pendientes.**` Solo si algún hallazgo cuenta un KPI sin meta: nómbralo y di que su meta se propone con su valor real en `09-make-dashboard` y se registra con `07-make-data-model-kpi-update`.

## 3. Elegir la captura

- **Una captura por hallazgo:** la de la página de 3.2 donde se ve el KPI. La tabla de 3.2 (`Código | KPI | Valor real | Meta | Estado | Página`) te dice cuál.
- **Cada captura se marca una sola vez**, en el primer hallazgo que la usa. Si otro hallazgo usa la misma página, lo cita en la columna `Captura` y en el texto con `{{figura:pag-nn}}`; el informe lo convierte en «Figura N».
- Copia `capturas/pag-nn.png` (y su `pag-nn.md`) desde la corrida de 09 a la de 10, sin modificarlas.
- Un hallazgo sin captura de su página no se escribe: pídela al equipo (se entrega con 09).

## 4. Las cifras

- **Toda cifra con unidad (`%`, `S/`, «puntos porcentuales») sale de `valores.json`:** el valor real de un KPI, su meta o la **diferencia entre ambos**. No estimes, no completes y no redondees de modo que cambie la cifra: usa los decimales que trae el dashboard.
- **La tabla repite el valor tal cual** (`97,2 %`) y la **meta tal cual está en 2.5** (`98 % o más`).
- **El estado se calcula, no se opina:** con «o más», cumple si el valor es mayor o igual que la meta; con «o menos», si es menor o igual. Sin meta, el estado es `Sin meta` y el hallazgo **no dice si el valor es alto o bajo**.
- Una cifra que no esté en `valores.json` (un promedio propio, una proyección) no entra. Si un hallazgo la necesita, el equipo la agrega al dashboard y a `valores.json`.

## 5. Lenguaje con datos generados

- Declara el origen al empezar (punto 2.1) y no lo repitas en cada párrafo.
- Habla de **lo que mostró el dashboard**, no de «lo que pasa en la empresa»: «el dashboard muestra una merma de 6,9 %», no «la empresa pierde pollo por mala gestión».
- No afirmes que los hallazgos describen el negocio real. La validación marca una frase con «negocio real» que no esté negada.
- Las decisiones se redactan como **lo que el usuario puede hacer** con el dato, no como un hecho cumplido.

## 6. Errores frecuentes
- Un objetivo del brief sin ningún hallazgo.
- Un hallazgo que cita un KPI de otro objetivo.
- Un valor de la tabla distinto del de `valores.json`, o un estado que no concuerda con la meta.
- Una cifra de la narrativa que no está en `valores.json` (por ejemplo, una proyección).
- Una captura marcada dos veces, o citada pero no copiada a la corrida.
- Decir si un KPI «sin meta» es bueno o malo.
- Una decisión sin su responsable, o un responsable que no es usuario del brief.
- Escribir el capítulo antes de que el equipo entregue los valores del dashboard.

## 7. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/storytelling.py`: encabezado, declaración de datos generados, tabla de hallazgos (objetivo del brief, KPI de `modelo.json` que mide ese objetivo, valor y estado calculados contra `valores.json` y la meta, captura de la página correcta, usuario del brief), cada objetivo con hallazgo, narrativa de cada hallazgo, cifras con unidad presentes en `valores.json`, capturas marcadas una vez y copiadas, y texto limpio.

## 8. Checklist
- [ ] El primer párrafo declara que los datos son generados para el proyecto (si `modo_datos` es `generado`).
- [ ] Cada objetivo específico del brief tiene al menos un hallazgo.
- [ ] Cada hallazgo cita un KPI que mide su objetivo, con su valor real, su meta y su estado.
- [ ] Cada hallazgo tiene su captura copiada y marcada una sola vez.
- [ ] Toda cifra con unidad está en `valores.json` o es la diferencia entre un valor y su meta.
- [ ] Cada hallazgo termina en una decisión de un usuario del brief.
- [ ] Hay «Contexto» y «Prioridades» y, si falta alguna meta, «Metas pendientes».
- [ ] Cada tabla tiene su título `Tabla N: …`.
- [ ] `validate_run.py` no informa incidencias.
