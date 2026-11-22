# Playbook del dashboard (sección 3.2 y anexos C y D)

Guía para que un agente prepare el dashboard del capítulo 3 del informe de BI (`common/structure/model1.md`) y redacte la sección 3.2 y los anexos C y D con lo que el equipo construyó. Las plantillas están en [`models/`](models/README.md).

Lo ejecuta la skill `09-make-dashboard` (y lo ajusta `09-make-dashboard-update`). Escribe en `project/09-dashboard/<DD-MM-AAAA-HH-MM-SS>/`. **La skill no abre Power BI ni construye el dashboard:** entrega la especificación de páginas y las medidas propuestas, y cuando el equipo trae los valores reales y las capturas, redacta. Nunca inventa un valor.

---

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`): **usuarios** y **decisiones** que apoya el dashboard, y los objetivos `OE-nn`.
2. `modelo.json` y la sección 2.5 de la corrida vigente de `07-make-data-model-kpi`: tablas, campos, KPI con su fórmula, medida propuesta, campos de origen y meta. **Sin `modelo.json` la skill se detiene.**
3. La corrida vigente de `08-make-etl` (qué se cargó y con qué calidad). Si falta, avisa y pregunta si continúa solo con la especificación, sin valores reales.
4. `valores.json` y `capturas/` que entrega el equipo (ver `models/ds-4-valores-json.md`).

### 0.2 Dos mitades
- **Primera mitad (materiales para el equipo):** páginas `PAG-nn` con su pregunta, usuario, visualizaciones, filtros y KPI, y las medidas DAX propuestas (`python3 .claude/skills/_shared/dashboard_dax.py <modelo.json>`). Con el plan confirmado se escribe `materiales/paginas.json` (plantilla `ds-5-paginas-json`; el plan por defecto del caso está en `common/09-dashboard/paginas-por-defecto.json`) y `python3 .claude/skills/_shared/dashboard_ref.py construir --run <corrida>` genera, a partir de él y de `data/respuestas/`, el **dashboard de referencia** (`materiales/dashboard-referencia.html`, con el diseño del proyecto y los valores esperados de cada visual) y la **guía paso a paso** (`materiales/guia-dashboard.md`: cada visual con sus campos, cada medida con su DAX, cada columna calculada con su tabla y sus archivos de origen y los valores esperados para comparar). Termina con una lista de lo que el equipo debe traer: el valor de cada KPI y una captura por página. Sin esa entrega **no se escribe** 3.2 ni los anexos.
- **Segunda mitad (redacción):** con `valores.json` y las capturas en la corrida, se escriben 3.2 y los anexos C y D y se valida.

### 0.3 Preguntar y confirmar
Antes de entregar la especificación, muestra el plan (una fila por página con su usuario y sus KPI) y **espera la confirmación**. Pregunta solo lo que falte: qué página prefiere cada usuario o si hay un filtro que el negocio exige.

### 0.4 Contrato de la corrida (lo lee `12-make-report`)
- `secciones/3.2.md`: la primera línea es el encabezado exacto (`## 3.2. Construcción del dashboard en Power BI`); después, solo texto final, sin notas de trabajo. Cada página marca su captura con `<!-- captura: pag-nn -->` en una línea sola.
- `anexos/C.md` y `anexos/D.md`: abren con `# Anexo C: …` y `# Anexo D: …`; el informe los agrega al final y los convierte en HTML con `13-make-annex-html`.
- `valores.json` y `capturas/pag-nn.png`: entrada del equipo.
- `referencias.md` si se cita y `README.md` con la procedencia (corridas de origen, qué propuso la skill y qué entregó el equipo, metas pendientes).
- **Título de cada tabla:** antes de cada tabla va una línea `Tabla N: título`.

### 0.5 Códigos de trazabilidad
| Código | Qué es | Dónde se define |
|---|---|---|
| `PAG-nn` | Página del dashboard | Primera celda de la tabla de páginas de 3.2 |
| `MED-nn` | Medida (o columna calculada) | Primera celda de la tabla del anexo C |
| `KPI-nn`, `OE-nn` | KPI y objetivo | `modelo.json` y brief (se citan, no se vuelven a definir) |

Los códigos se numeran por prefijo y **no se reutilizan** si se elimina un ítem.

### 0.6 Texto limpio
Ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. Lo desconocido, como una meta que nadie fijó, dice «Pendiente» o «Sin meta».

---

## 1. Páginas (3.2)

- **Una pregunta de negocio por página**, ligada a una decisión del brief. Una página para el dueño y otra para el jefe de cocina rara vez es la misma: elige el usuario de cada una entre los del brief.
- **Tipo de visual según la pregunta:** tarjeta para el valor frente a la meta, barras para comparar categorías (canal, turno), línea para la evolución en el tiempo, columnas para un patrón por día o turno, tabla solo para el detalle.
- **Filtros:** los de las dimensiones del modelo (`dCalendario`, `dCanal`, `dTurno`, …); los que se compartan entre páginas, sincronizados.
- **Todo KPI del modelo aparece en una página**, y se ve con su meta (semáforo: cumple, no cumple, sin meta).
- Pocas páginas, claras: cuatro a seis para un dashboard de este alcance.

## 2. Medidas DAX (anexo C)

- Una **medida base** por cada campo de un hecho que usa un KPI, con la agregación del modelo (`Suma de venta_bruta`), y una **medida de KPI** con el nombre de la «Medida propuesta» de 2.5.
- Patrones: razón con `DIVIDE(numerador, denominador)`; filtro con `CALCULATE(medida, dimension[atributo] = "valor")`; promedio con `AVERAGE`. Un porcentaje se calcula siempre con `DIVIDE`.
- El DAX cita **solo** tablas y campos de `modelo.json`; el validador lo comprueba. Si un KPI necesita un campo que el modelo no tiene, el cambio se hace en `07-make-data-model-kpi-update`, no aquí.
- **La skill propone; el equipo prueba y escribe la final.** El anexo conserva la medida que se ejecutó, y no deja marcas `revisar`.

## 3. Valores y capturas

- El valor de cada KPI en 3.2 sale solo de `valores.json`, con los decimales que muestra el dashboard.
- El estado se calcula contra la meta de 2.5 y su comparador («o más», «o menos»); sin meta es `Sin meta`.
- **Metas pendientes:** con el valor real de un KPI sin meta, la skill propone una meta con su justificación, pide la confirmación del usuario y avisa que se registra con `07-make-data-model-kpi-update` (no edita 2.5). Si el equipo ya cerró la meta en 2.5, `valores.json` la trae y el estado se recalcula.
- Una captura por página, en `capturas/pag-nn.png`. Un valor que muestra una página sin captura no se cita.

## 4. Errores frecuentes
- Un KPI que no aparece en ninguna página, o una página sin usuario del brief.
- Un valor de 3.2 que no coincide con `valores.json`, o un estado que no concuerda con la meta.
- Medidas que citan una tabla o un campo que no existen en el modelo, o marcas `revisar` sin resolver.
- Una captura marcada que el equipo no entregó, o la misma captura marcada en 3.2 y en el anexo D.
- Escribir 3.2 antes de que el equipo entregue los valores.

## 5. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/dashboard.py`: encabezados, tabla de páginas con usuario del brief, KPI en alguna página, capturas marcadas y entregadas, `valores.json` (un valor por KPI y la meta de 2.5), valores y estados de 3.2 coherentes, lectura del dashboard y metas pendientes, anexo C (medidas con DAX que cita solo el modelo, una por KPI, sin `revisar`), anexo D (una descripción por página) y títulos de tabla. Corrige hasta que no haya incidencias.

## 6. Checklist
- [ ] Hay una página por pregunta de negocio, con usuario del brief, visualizaciones y filtros.
- [ ] Cada KPI de `modelo.json` está en una página.
- [ ] `valores.json` y `capturas/pag-nn.png` están en la corrida y 3.2 cita solo esos valores.
- [ ] El anexo C define la medida de cada KPI con la versión final del equipo.
- [ ] El anexo D describe cada página sin repetir la marca de captura.
- [ ] Las metas pendientes están nombradas y apuntan a `07-make-data-model-kpi-update`.
- [ ] `validate_run.py` no informa incidencias.
