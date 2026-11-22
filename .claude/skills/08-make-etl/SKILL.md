---
name: 08-make-etl
description: Prepara el ETL del capítulo 3 del informe de Inteligencia de Negocios y redacta la sección 3.1 y los anexos A y B en project/08-etl/ (secciones/3.1.md, anexos/A.md y anexos/B.md): genera los datos del proyecto en CSV dentro de data/ con la hoja de respuestas, entrega al equipo el diccionario de datos y una guía paso a paso de Power Query, y cuando el equipo trae la evidencia de lo que hizo (evidencia.json) la compara con la hoja de respuestas, avisa de las diferencias y redacta 3.1 (extracción, transformación, reglas de calidad, carga y verificación), el anexo A (diccionario, origen de los campos del modelo y resultado de las reglas) y el anexo B (los scripts que el equipo ejecutó). No ejecuta Power Query ni inventa una cifra. Úsala después de 07-make-data-model-kpi o cuando el usuario pida "08-make-etl", "ETL", "generar los datos", "limpieza de datos", "Power Query", "diccionario de datos" o "calidad de datos". Para cambiar uno ya creado usa 08-make-etl-update.
---

# 08-make-etl

Abre el capítulo 3: prepara el trabajo del equipo (datos, diccionario y guía de Power Query) y, cuando el equipo trae la evidencia de lo que hizo, redacta 3.1 y los anexos A y B. La rúbrica pide un ETL con reglas de calidad y resultados medibles.

**La skill no ejecuta Power Query ni Power BI.** Genera los materiales, se detiene, y redacta solo con lo que el equipo trae. Nunca escribe una cifra que no esté en `evidencia.json` ni dice que un paso «se ejecutó» sin esa evidencia.

## Fuentes obligatorias (léelas antes de preguntar o escribir)

1. `common/08-etl/guia.md` (playbook: dos mitades, datos, evidencia, verificación, contrato de la corrida, códigos y checklist).
2. `common/08-etl/models/README.md` y las plantillas `etl-1-seccion-3-1.md`, `etl-2-anexo-a.md`, `etl-3-anexo-b.md`, `etl-4-guia-power-query.md` y `etl-5-evidencia-json.md`.
3. El brief vigente (`python3 .claude/skills/_shared/brief.py leer`), la corrida vigente de `06-make-bi-solution` (`python3 .claude/skills/_shared/diagnostico.py leer --paso 06-make-bi-solution`), el `modelo.json` de la corrida vigente de `07-make-data-model-kpi`, `data/` y el config (`modo_datos`).

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py` (`validate`, `check`, `current`, `register`)
- `python3 .claude/skills/_shared/datagen.py` (`parametros`, `generar --confirmar`, `verificar`): genera los CSV de `data/`, la hoja de respuestas y los archivos de apoyo.
- `python3 .claude/skills/_shared/etl_verificacion.py comparar [--raiz .] [--evidencia <ruta>] [--actualizar]`: compara los totales del equipo (`data/salida/` o los de la evidencia) con `data/respuestas/`.
- Kit compartido: `runs.py`, `validate_run.py` (reglas en `.claude/skills/_shared/rules/etl.py`).

## Reglas

- **Dos mitades, una pausa.** Primero materiales; después de que el equipo trae la evidencia, la redacción. Sin evidencia no se escribe 3.1 ni los anexos.
- **Solo la evidencia.** Cada cifra de filas sale de `evidencia.json`. Si falta una, se pide al equipo; no se estima ni se completa con lo esperado.
- **Las diferencias no se ocultan.** Si la comparación con la hoja de respuestas las encuentra, se informan (tabla, mes, desvío y regla probable) y se pide corregir el ETL antes de redactar; si el equipo decide entregar igual, 3.1 las muestra.
- **Cada defecto tiene su regla.** Todo tipo de `data/respuestas/defectos.csv` necesita un `REG-nn` en 3.1.
- **Códigos** `REG` (regla de calidad) y `PAS` (paso de Power Query), numerados por prefijo y sin repetir; cita los `FUE` del brief y las tablas del modelo.
- **Datos generados:** con `modo_datos: generado`, 3.1 lo declara y dice cómo se calibraron. Con `real`, no se generan datos: se piden al equipo los archivos autorizados.
- **Contrato de la corrida:** `secciones/3.1.md` empieza con `## 3.1. Construcción de la solución ETL` y solo tiene texto final; `anexos/A.md` y `anexos/B.md` abren con su encabezado; antes de cada tabla va `Tabla N: título`; `materiales/guia-power-query.md` y `evidencia.json` completan la corrida; las citas van a `referencias.md` (APA 7).
- **Escribe solo tras confirmar.** Texto limpio: ningún archivo, salvo `README.md`, dice que el contenido es falso, inventado, de prueba o simulado.

## Flujo

### Primera mitad: materiales para el equipo

1. **Config y prerrequisitos.** `projectcfg.py validate`; si falla, detente e indica `00-init`. `projectcfg.py check --skill 08-make-etl` y muestra los avisos. Si falta la corrida de `07-make-data-model-kpi` (o su `modelo.json`), detente: no se pueden definir las tablas de destino. Si falta la de `06`, avisa que no hay arquitectura de la que partir. Si ya hay una corrida de este paso, avisa que se creará otra versión y ofrece `08-make-etl-update`.
2. **Datos.** Con `modo_datos: generado`: `python3 .claude/skills/_shared/datagen.py parametros` deriva y deja `data/parametros.json`; **muéstraselo al usuario** (periodo, canales, comisiones, ventas, margen, merma, precio del pollo, tolerancias, semilla y de dónde sale cada cifra) y pregunta cualquier cifra sin origen. **Solo tras su confirmación**: `python3 .claude/skills/_shared/datagen.py generar --confirmar` y `datagen.py verificar` (confirma tolerancias y cuenta los defectos). Si una cifra queda fuera de tolerancia no se entregan los archivos: informa la cifra y el desvío. Con `real`, pide al equipo los archivos y salta al paso 3.
3. **Crear la corrida.** `RUN=$(python3 .claude/skills/_shared/runs.py new --step 08-make-etl)`.
4. **Materiales.** Genera la guía a la medida del caso con `python3 .claude/skills/_shared/etl_guia.py construir --run <corrida>`: escribe `$RUN/materiales/guia-power-query.md` con, por cada fuente, sus columnas, sus defectos con su cantidad, por qué se tratan y cómo (código M propuesto), el punto de control de filas de cada paso (salen de `etl_referencia.py`, la limpieza de referencia que coincide con `data/respuestas/`), el cálculo de `costo_estimado` y `costo_operativo`, los totales a comparar, una tabla «si tu número no coincide», lo que el equipo debe anotar y el diccionario de datos. La plantilla `etl-4` fija el formato; la guía generada es la que se entrega. Revisa que los puntos de control de la guía coinciden con `data/respuestas/` (`python3 .claude/skills/_shared/etl_referencia.py`). Dile al usuario dónde están los CSV, la hoja de respuestas y los archivos de apoyo, y que **lo ejecuta el equipo**: la skill no abre Power BI.
5. **Pausa.** Entrega los materiales y detente: «Cuando terminen el ETL, tráeme la evidencia». Sugiere que exporten sus tablas cargadas a `data/salida/<tabla>.csv` para comparar por mes y canal.

### Segunda mitad: evidencia y redacción

6. **Evidencia.** Con `AskUserQuestion` pide solo lo que falte, una pregunta por cosa: filas antes y después de cada regla, filas leídas de cada fuente, filas cargadas de cada tabla del modelo y los totales de ventas, comisión y líneas del modelo. Guarda lo que el equipo responde en `$RUN/evidencia.json` (plantilla `etl-5`), sin corregirlo. Guarda sus capturas de Power Query en `$RUN/capturas/` si las traen.
7. **Verificación.** `python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia $RUN/evidencia.json --actualizar`. Si hay diferencias, muestra cada una (tabla, mes, esperado, obtenido, desvío y regla probable) y pregunta si el equipo corrige el ETL (vuelves al paso 6) o entrega con ellas.
8. **Plan y confirmación.** Muestra en líneas cortas: fuentes con sus filas, los pasos, una fila por regla (código, defecto, tabla, filas antes y después), las tablas cargadas y el resultado de la verificación. Pide el código final que ejecutó el equipo para el anexo B; si no trae el de un paso, no lo inventes. **Espera la confirmación.**
9. **Escritura.** En `$RUN`: `secciones/3.1.md` (plantilla `etl-1`), `anexos/A.md` (plantilla `etl-2`), `anexos/B.md` (plantilla `etl-3`, con el código del equipo tal cual), `referencias.md` si hay citas y `README.md` (modo de datos, corridas de origen de `06` y `07`, semilla de `data/parametros.json`, qué trajo el equipo y qué propuso el agente).
10. **Revisar la redacción y validar.** Antes de validar, invoca con el Agent tool al agente `revisor-redactor` (subagent_type `revisor-redactor`) pasándole las rutas de `$RUN/secciones/3.1.md` y de los anexos y los datos propios del caso; aplica con Edit solo lo que el usuario apruebe (reglas en `common/redaccion/guia.md`; sin avisos bloqueantes). Después, `python3 .claude/skills/_shared/validate_run.py $RUN`. Corrige hasta que no haya incidencias (cifras iguales a la evidencia, cada defecto con su regla, campos del modelo con origen, pasos con su código, datos generados declarados).
11. **Registrar.** `python3 .claude/skills/_shared/projectcfg.py register --step 08-make-etl --run <carpeta>` (marca 3.1 como disponible). Si responde `"movido": false`, díselo al usuario.
12. **Cierre.** Entrega la ruta, un resumen (fuentes, reglas con sus cifras, tablas cargadas y resultado de la verificación), que 3.1 y los anexos A y B quedan listos, y que sigue `09-make-dashboard`. Sugiere `12-make-report` para ver el avance del informe.
