---
name: 10-make-storytelling
description: Redacta la sección 4 del informe de Inteligencia de Negocios en project/10-storytelling/ (secciones/4.md y capturas/): una narrativa de hallazgos HLZ-nn construida solo con el valor real de cada KPI (valores.json) y las capturas de 09-make-dashboard, con cada objetivo específico del brief contado al menos una vez, el valor frente a su meta con su estado calculado, la captura que lo muestra y la decisión que apoya el dueño o el jefe de cocina. Propone los hallazgos y espera la confirmación antes de escribir, declara que los datos son generados para el proyecto y valida cada cifra contra valores.json. Se detiene si la corrida de 09 no trae valores.json. Úsala después de 09-make-dashboard, cuando el equipo ya entregó los valores y las capturas, o cuando el usuario pida "10-make-storytelling", "storytelling", "hallazgos del dashboard", "narrativa de resultados" o "sección 4". Para cambiar uno ya creado usa 10-make-storytelling-update.
---

# 10-make-storytelling

Redacta la sección 4: cuenta qué mostró el dashboard y qué decisión apoya cada resultado. **La skill no mide nada:** todo lo que cita sale de `valores.json` y de las capturas que el equipo entregó a `09-make-dashboard`. **Nunca escribe una cifra que no esté ahí.**

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/10-storytelling/guia.md` (playbook: fuentes, hallazgo, estructura de la sección, captura, cifras, lenguaje con datos generados, errores y checklist).
2. `common/10-storytelling/models/README.md` y las plantillas `st-1-seccion-4.md` y `st-2-propuesta.md`.
3. La corrida vigente de `09-make-dashboard`: `valores.json`, `capturas/` y `secciones/3.2.md` (qué KPI se ve en qué página).
4. `modelo.json` y 2.5 de la corrida vigente de `07-make-data-model-kpi` (meta, comparador y objetivo de cada KPI), el brief vigente (`python3 .claude/skills/_shared/brief.py leer`: objetivos, usuarios y decisiones), las secciones 1.8 a 1.10, `project/domain.md` y el config.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/brief.py leer` y `python3 .claude/skills/_shared/diagnostico.py leer --paso 07-make-data-model-kpi`
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/storytelling.py`, que reutiliza el comparador de metas de `rules/dashboard.py`).

## Reglas

- **No mides ni estimas.** Si falta `valores.json` en la corrida vigente de 09, **te detienes** y dices que primero hay que entregar los valores del dashboard (con `09-make-dashboard`). Una cifra que no esté en `valores.json` no entra.
- **Toda cifra con unidad (`%`, `S/`, «puntos porcentuales») es un valor real, una meta o la diferencia entre ambos**, con los decimales que trae el dashboard. Nada de proyecciones ni promedios propios.
- **El estado se calcula**, no se opina: con «o más» cumple si el valor es mayor o igual que la meta; con «o menos», si es menor o igual. Un KPI sin meta es `Sin meta` y el hallazgo no dice si es alto o bajo.
- **Cada objetivo específico del brief tiene al menos un hallazgo**, y cada hallazgo cita un KPI que mide ese objetivo en `modelo.json`.
- **Cada hallazgo tiene su captura:** la de la página de 3.2 donde se ve su KPI, copiada sin modificar a `capturas/` de tu corrida y marcada **una sola vez** con `<!-- captura: pag-nn -->`. Sin captura, no hay hallazgo: se pide al equipo.
- **Datos generados:** con `modo_datos: generado`, el primer párrafo dice que los hallazgos se basan en datos generados para el proyecto y medidos por el equipo en el dashboard, y que no describen el negocio real de una empresa. Habla de lo que mostró el dashboard, no de lo que «pasa en la empresa».
- **Cada hallazgo termina en una decisión** de un usuario del brief (dueño o jefe de cocina), redactada como lo que esa persona puede hacer con el dato.
- **Escribe solo tras confirmar la propuesta.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.
- **Códigos** `HLZ-nn`: numerados sin repetir. **Contrato de la corrida:** `secciones/4.md` empieza con `## 4. Storytelling con datos` y solo tiene texto final; las citas van a `referencias.md` (APA 7).

## Flujo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 10-make-storytelling` y muestra los avisos. **Si la corrida vigente de `09-make-dashboard` no existe o no trae `valores.json`, detente:** «primero hay que entregar los valores del dashboard». Si faltan `modelo.json` o el brief, detente también. Si ya hay una corrida de este paso, avisa que se creará otra y que `10-make-storytelling-update` cambia solo lo pedido.
2. **Insumos.** Lee de `valores.json` el valor, la unidad, la meta y el periodo de cada KPI; de 3.2 de 09, en qué página se ve cada KPI; de `modelo.json`, el nombre, la meta con su comparador y el objetivo de cada KPI; del brief, los `OE-nn`, los usuarios y las decisiones; de 1.8 a 1.10, la problemática para el contexto.
3. **Preguntas** (AskUserQuestion), solo lo que falte: qué decisión le importa más a cada usuario y si un KPI debe contarse junto con otro.
4. **Propuesta y confirmación.** Muestra la tabla de la plantilla `st-2-propuesta`: una fila por hallazgo (código, objetivo, KPI, valor real, meta, estado calculado, captura, quién decide, decisión) y el orden de prioridad. Comprueba que **todos los objetivos** tienen hallazgo. **Espera la confirmación.**
5. **Corrida y capturas.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 10-make-storytelling)`. Copia a `$RUN/capturas/` cada `pag-nn.png` (y su `pag-nn.md` si existe) que citarán los hallazgos, desde la corrida de 09, sin modificarlas.
6. **Escritura.** Escribe `$RUN/secciones/4.md` con la plantilla `st-1-seccion-4.md`, `$RUN/referencias.md` si hay citas y `$RUN/README.md` (modo de datos, corridas de origen de `07` y `09`, qué se contó y qué metas siguen pendientes).
7. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole la ruta de `$RUN/secciones/4.md` y los datos propios del caso (los valores de `valores.json`); aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después, `python3 .claude/skills/_shared/validate_run.py $RUN` hasta que no haya incidencias.
8. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 10-make-storytelling --run <carpeta>` (marca la sección 4 como disponible). Si responde `"movido": false`, díselo al usuario.
9. **Cierre.** Entrega la ruta, un resumen (hallazgos con su valor, estado y decisión), las metas pendientes y la skill que las cierra, y recuerda que cada captura se pega en su marcador del informe. Sugiere `11-make-conclusions` y, para ver el avance, `12-make-report`.
