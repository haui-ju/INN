# Playbook del diagnóstico del negocio (secciones 1.1 a 1.4)

Guía para que un agente redacte las cuatro primeras secciones del capítulo 1 del informe de BI (`common/structure/model1.md`): nombre de la empresa, misión y visión, industria y tamaño, y Business Model Canvas. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `03-make-business-diagnosis` (y lo ajusta `03-make-business-diagnosis-update`). Escribe en `project/03-business-diagnosis/<DD-MM-AAAA-HH-MM-SS>/`. La rúbrica pide misión, visión, industria y tamaño de la organización, y un Canvas articulado con la problemática y los objetivos.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. `project/domain.md`: datos generales, reseña, misión, visión, valores, industria, tamaño, clientes y competencia. **Se toman de aquí, no se reescriben de memoria.**
2. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): tema, empresa, problemática, usuarios y fuentes de datos.
3. `project/config.yaml`: nombre, `tipo` (`empresa` o `propio`), `ruc`, `rubro` y `modo_datos`.

### 0.2 Tipo de proyecto
Lee `proyecto.tipo`, muéstralo y confírmalo con el usuario. Con `empresa`, el RUC de 1.1 es el del config y los datos generales vienen de la consulta por RUC que guardó `domain.md`. Con `propio`, la empresa la plantea el equipo: la celda del RUC dice «No aplica (empresa planteada por el equipo)» y nunca se escribe un RUC. Si el usuario corrige el tipo, indica `00-init-update` y no continúes con el dato anterior.

### 0.3 Datos modelados
En `domain.md` un dato sin fuente lleva el marcador `(modelado por el agente, por no contar con X)`. Antes de escribir, **muestra qué secciones salen de datos con marcador** y pregunta si el usuario aporta el dato real. En las secciones el texto va **sin el marcador**; la procedencia queda solo en el `README.md` de la corrida («secciones salidas de datos modelados: …»).

### 0.4 Preguntar y confirmar
Pregunta solo lo que falta (por ejemplo, ventas anuales si `domain.md` no las trae, o el entorno competitivo). Muestra un plan (tipo, fuente de cada sección, categoría de tamaño con su cálculo y los nueve bloques del Canvas en una línea cada uno) y **espera la confirmación** antes de escribir.

### 0.5 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/1.1.md` a `secciones/1.4.md`: la **primera línea** es el encabezado exacto `## <punto>. <título del índice>` (el título es el texto del punto en el índice sin los paréntesis finales; `python3 .claude/skills/_shared/diagnostico.py titulos` los lista). Después, solo texto final del informe: prosa académica y tablas, sin notas de trabajo ni otros encabezados de nivel 1 o 2.
- En 1.4, la figura va en una línea sola: `<!-- figura: bmc -->`. El HTML queda en `visuales/bmc.html` y su explicación en `leer-imagen/bmc.md`; ambos los escribe `visuales.py construir`.
- `referencias.md`: una referencia por línea en APA 7 ([`common/citation-style/APA7.md`](../citation-style/APA7.md)); cada cita del texto, (Autor, año) o Autor (año), tiene su línea.
- `README.md`: procedencia (modo de datos, datos modelados, qué confirmó el usuario). Es el único archivo que puede decir que un dato es generado.

### 0.6 Texto limpio y citas
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado (`.claude/skills/_shared/policy.json`). Máximo una o dos citas por sección, de las **Referencias** de esta guía o de una fuente verificada (norma, institución oficial) que se agrega a `referencias.md`.

### 0.7 Articulación
Cada sección prepara el resto del capítulo: 1.2 cierra con la relación entre la visión y el proyecto; 1.4 cierra con la lectura del modelo, que dice en qué bloques se ve la problemática del brief. La matriz de 1.10 (skill `05`) citará esos bloques por su nombre exacto.

---

## 1. Nombre de la empresa (1.1)

Un párrafo de presentación (qué hace, dónde y por qué canales vende), una tabla `Dato | Valor` con **Razón social, Nombre comercial, RUC, Actividad económica y Ubicación** (y opcionalmente Inicio de actividades y Locales y canales) y una **Reseña** de dos a cuatro frases. El nombre comercial coincide con el de `domain.md`.

## 2. Misión y visión (1.2)

**Misión** y **Visión** se reproducen de `domain.md` (el validador compara el texto). Si no constan, se proponen a partir del tema y el rubro, el usuario las confirma y primero se escriben en `domain.md`. Los **Valores** son opcionales (lista corta). La **Relación con el proyecto** explica en dos o tres frases qué parte de la misión o la visión exige decidir con datos.

## 3. Industria y tamaño (1.3)

- Tabla `Aspecto | Descripción` con **Sector**, **Actividad económica (CIIU)**, **Tipo de cliente** y **Entorno competitivo**.
- **Tamaño de la organización**: un párrafo y una tabla `Dato | Valor` con **Ventas anuales**, **UIT de referencia**, **Ventas en UIT**, **Trabajadores** (opcional) y **Categoría (Ley 30056)**.
- **Cálculo:** ventas en UIT = ventas anuales ÷ UIT (se redondea; tolerancia de una UIT). Categoría según el artículo 5 de la Ley 30056: **Microempresa** hasta 150 UIT; **Pequeña empresa** más de 150 y hasta 1700 UIT; **Mediana empresa** más de 1700 y hasta 2300 UIT; **Gran empresa** por encima de 2300 UIT. Desde esa ley el tamaño se define solo por ventas; los trabajadores se informan como dato de contexto.
- **UIT:** usa la del año que fija el decreto supremo del MEF y cítala con su año (el ejemplo usa S/ 5 500 de 2026). Confírmala con una búsqueda antes de escribir.
- **Montos:** `S/ 2 400 000` (espacio como separador de miles, coma decimal).
- Si no hay ventas anuales y el usuario no las da, `Ventas anuales` y `Ventas en UIT` pueden quedar «Pendiente» solo si la categoría se declara con su fuente (por ejemplo, la consulta RUC). Con `modo_datos: generado` las ventas se plantean coherentes con el rubro y el tamaño, y se anota en el `README.md`.

## 4. Business Model Canvas (1.4)

Los nueve bloques de Osterwalder y Pigneur (2010), con estos nombres exactos (la tabla y el visual los leen así): **Segmentos de clientes, Propuesta de valor, Canales, Relaciones con clientes, Fuentes de ingresos, Recursos clave, Actividades clave, Socios clave y Estructura de costos**.

- Un párrafo que presenta el lienzo (con su cita), la marca `<!-- figura: bmc -->` y la tabla `Bloque | Contenido`, con los elementos de cada bloque separados por punto y coma (de dos a cinco por bloque).
- Los elementos salen de `domain.md` y del brief (por ejemplo, los canales del brief, los costos que menciona la problemática). Nada se agrega de memoria.
- **Lectura del modelo**: dos o tres frases que dicen en qué bloques aparece la problemática del brief (por ejemplo, canales con comisión que la estructura de costos absorbe).

---

## 5. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/business_diagnosis.py`: encabezados exactos, figura `bmc` con su visual y su explicación válida, filas obligatorias de 1.1, RUC según el tipo, misión y visión iguales a `domain.md`, aspectos de 1.3, cálculo en UIT y categoría coherentes, nueve bloques con contenido, lectura del modelo, sin el marcador de datos modelados y citas con su referencia.

## 6. Errores frecuentes y checklist

**Errores:** escribir un RUC con `tipo: propio`; reescribir la misión en lugar de copiarla; categoría de tamaño por número de trabajadores; dividir las ventas por la UIT de otro año sin decirlo; nombres de bloques distintos a los nueve; un Canvas genérico que no muestra dónde está el problema; copiar el marcador «(modelado por el agente, …)» al informe; agregar una nota de trabajo en una sección.

**Checklist:**
- [ ] El tipo de proyecto fue confirmado y la celda del RUC le corresponde.
- [ ] Cada `secciones/<punto>.md` empieza con su encabezado exacto.
- [ ] Misión y visión son las de `domain.md`.
- [ ] Ventas en UIT y categoría son coherentes con la Ley 30056.
- [ ] El Canvas tiene los nueve bloques y su lectura nombra los bloques donde está la problemática.
- [ ] La figura `bmc` está construida (`visuales/bmc.html`, `leer-imagen/bmc.md`).
- [ ] Cada cita tiene su línea en `referencias.md`; la procedencia está solo en `README.md`.
- [ ] El usuario confirmó el plan antes de escribir.

---

## Referencias

Congreso de la República del Perú. (2013, 2 de julio). Ley N.° 30056, Ley que modifica diversas leyes para facilitar la inversión, impulsar el desarrollo productivo y el crecimiento empresarial. *Diario Oficial El Peruano*.

Osterwalder, A., & Pigneur, Y. (2010). *Business model generation: A handbook for visionaries, game changers, and challengers*. John Wiley & Sons.

*(Formato APA 7, ver `common/citation-style/APA7.md`. Otra fuente solo si se verifica y se agrega a `referencias.md`.)*
