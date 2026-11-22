# Design

## Context

Ver `proposal.md` (Why). Estado del que parte:

- `pipeline.json` declara `08-make-etl` (sección 3.1, carpeta `08-etl`) y `09-make-dashboard` (3.2, carpeta `09-dashboard`), ambas con `update: true`. El índice marca 3.2 con «(incluye imagen)» y define los anexos A y B (origen 3.1) y C y D (origen 3.2).
- `12-make-report` ya incluye un anexo cuando su corrida trae `anexos/<letra>.md`; hoy no tiene forma de numerar una imagen que no sea un visual generado.
- El capítulo 2 está archivado: `modelo.json` (4 hechos, 5 dimensiones, 9 relaciones y 7 KPI con campos de origen) y la arquitectura (CAP-07 y CAP-08 son el ETL, CAP-09 el modelo) son la entrada.
- `modo_datos` es `generado` y el brief marca FUE-01 a FUE-05 como generadas y FUE-06 como abierta. La carpeta `data/` existe vacía en la raíz.
- El equipo construye el ETL y el dashboard a mano. Una persona usa Power BI en el navegador y otra tiene Windows con Power BI Desktop.

## Goals / Non-Goals

**Goals:**
- Que el equipo parta de datos realistas, con volumen y defectos que justifiquen un ETL, y pueda comprobar que lo limpió bien.
- Que 3.1 y 3.2 y sus cuatro anexos salgan redactados con la evidencia y los valores reales del equipo, validados y armados en el informe.
- Que ninguna cifra del capítulo 3 sea inventada: toda cantidad tiene su origen en la evidencia.

**Non-Goals:**
- Ejecutar Power Query, DAX o Power BI desde la skill, o automatizar la construcción del dashboard.
- Storytelling y conclusiones (capítulos 4 y 5): van en `bi-chapter45-closing`.
- Generar archivos que no sean CSV o conectar fuentes reales.

## Decisions

**D1. Generar los datos dentro de `08-make-etl`, no en una skill aparte.** `skill-pipeline` fija una secuencia consecutiva de skills de `00` a `13`; una `08a` rompería esa regla. La generación es el primer paso de `08`, con su propia capacidad (`synthetic-data-generation`) para que la spec la describa por separado. Alternativa descartada: ampliar el brief para que traiga datos, que mezcla el contenido del informe con material de trabajo.

**D2. Las skills preparan y redactan; el equipo ejecuta.** Cada skill tiene dos mitades. La primera entrega materiales (datos, diccionario, guía y código, o especificación y medidas) y se detiene. La segunda arranca cuando el equipo trae la evidencia, la guarda en la corrida y redacta solo con ella. Sin evidencia, 3.1, 3.2 y los anexos no se escriben (escenarios «Sin evidencia» y «Sin valores»). Alternativa descartada: redactar primero con cifras esperadas y corregir después, que deja cifras inventadas en el informe si nadie las corrige.

**D3. Generador en el kit, solo biblioteca estándar.** `_shared/datagen.py` usa `random` con semilla, `csv` y `json`, como el resto del kit, y recibe `data/parametros.json`. Cien mil líneas se generan en segundos. Alternativa descartada: pandas o numpy, que agregan una dependencia que el kit no tiene.

**D4. Calibración por construcción, no por ajuste iterativo.** El generador fija el precio, la comisión por canal y la participación de aplicaciones por mes (de 15 % a 35 %), y calcula el costo operativo mensual despejándolo para que el margen neto siga la trayectoria de 14 % a 8 %. La merma se fija en 7 % de lo preparado con ruido por turno, y el precio del pollo vivo sube de S/ 6.10 a S/ 6.90 entre el 1 y el 14 de julio. Cada cifra tiene una tolerancia en `parametros.json`; si alguna queda fuera, no se entregan los archivos (escenario «Cifra fuera de tolerancia»).

**D5. Quince meses para que el crecimiento sea interanual.** El informe dice que las ventas crecieron 18 % «en el último año». Los datos cubren de agosto de 2025 a octubre de 2026, de modo que el 18 % se calcula entre agosto a octubre de 2026 y agosto a octubre de 2025, los tres meses que existen en ambos años. La participación de las aplicaciones sube de 15 % a 35 % y el margen neto baja de 14 % a 8 % a lo largo de los quince meses. Alternativa descartada: enero a octubre de 2026, donde el +18 % solo se podía reproducir como octubre contra enero.

**D5b. Alinear el periodo en los capítulos cerrados.** El brief (alcance y FUE-01), 2.3 (justificación de HER-02) y 2.4 (lectura del modelo) dicen «de enero a octubre de 2026». Se corrigen con los `-update` de sus skills antes de generar los datos, y la generación toma el periodo de `parametros.json`, que sale del brief ya corregido. `modelo.json` no cambia: el modelo no declara periodo.

**D12. Guías a la medida del caso con puntos de control.** Las plantillas fijan el formato; la entrega real al equipo es una guía escrita con las cifras de `data/respuestas/`. En el ETL, cada paso cierra con el número de filas esperado, de modo que una diferencia señala el paso que falló. En el dashboard, cada visual y cada KPI traen su valor esperado. Alternativa descartada: una guía genérica con ejemplos, que obliga al equipo a deducir qué limpiar en sus archivos.

**D13. Dashboard de referencia en HTML generado desde Python.** `_shared/dashboard_ref.py` toma las páginas confirmadas (`materiales/paginas.json`), los valores esperados de `data/respuestas/` y los tokens del proyecto y escribe un HTML autónomo con gráficos en SVG, sin React ni bibliotecas externas, como el resto del kit. Alternativa descartada: una plantilla compilada con React en `common/html/`, que exige recompilar y no aporta nada a un documento de referencia.

**D6. Defectos cuantificados y atados al modelo.** Cada defecto responde a algo que el modelo ya mide: registros inválidos para `registro_valido` y `registro_total`, días sin precio para `valor_imputado`, duplicados en los reportes de las aplicaciones y de WhatsApp para la regla de duplicados, y nombres de producto y fechas con formatos mezclados para `dProducto` y `dCalendario`. La cantidad de cada uno queda en `data/respuestas/defectos.csv` con la regla que debe tratarlo, y la validación de 3.1 exige que cada defecto tenga su `REG-nn`.

**D6b. Hoja de respuestas.** `data/respuestas/` trae, en CSV, los totales esperados tras una limpieza correcta. El equipo puede exportar sus tablas cargadas a `data/salida/<tabla>.csv` y la skill calcula sus totales y los compara; si no exporta, escribe los totales a mano. La comparación se informa por tabla y se registra en 3.1.

**D7. Evidencia como archivos de la corrida.** `evidencia.json` (filas antes y después de cada regla, totales entregados) y `capturas/` (PNG) en la corrida de 08; `valores.json` (valor real de cada KPI y de cada medida) y `capturas/` en la de 09. Son entradas del equipo, no texto del informe, y los validadores comparan lo redactado con ellas.

**D8. Códigos de trazabilidad.** `REG-nn` (reglas de calidad), `PAS-nn` (pasos de Power Query), `PAG-nn` (páginas) y `MED-nn` (medidas). Reutiliza `FUE`, `CAP`, `FCT`, `DIM`, `KPI` y `OE`, y no choca con los prefijos actuales (`OE`, `OG`, `FUE`, `CAP`, `HER`, `FCT`, `DIM`, `REL`, `KPI`, `CAU`, `DEB`, `FOR`, `OPO`, `AME`). Se agregan a `PREFIJOS` de cada validador.

**D9. Capturas como figuras numeradas del informe.** `<!-- captura: <id> -->` reutiliza la numeración y el marcador «(INCLUIR IMAGEN: …)» de las figuras, con el archivo en `capturas/<id>.png` en lugar de un HTML generado. El informe no copia la imagen (su validador prohíbe archivos de imagen en la corrida): el marcador y el índice enlazan al archivo de la corrida que la produjo. Así 3.2 no queda con aviso y el equipo pega cada captura donde corresponde. Alternativa descartada: incrustar las imágenes en el informe, que `report-assembly` prohíbe.

**D10. Medidas DAX propuestas con los nombres del modelo.** La medida de cada KPI sale de la fórmula y los campos de origen de 2.5; el validador comprueba que toda tabla y campo citados existen en `modelo.json`. La que cuenta es la que el equipo ejecutó: el anexo C conserva la final y la skill no afirma que su propuesta funcione.

**D11. Metas pendientes se cierran con el `-update` del modelo.** `09` propone las metas de KPI-02 y KPI-06 a partir de los valores reales, pero no edita 2.5: eso lo hace `07-make-data-model-kpi-update`, que ya mantiene 2.5 y `modelo.json` juntos.

## Risks / Trade-offs

- **El equipo trabaja en Power BI en el navegador, con menos control sobre Power Query** → las guías dan el paso a paso para Desktop y para la web, el anexo B acepta «pasos» además de código, y la evidencia se pide por resultado (filas y totales), no por herramienta.
- **El equipo entrega totales que no coinciden y no sabe por qué** → la comparación informa la tabla, el mes y la regla probable; es un error del ETL que se corrige antes de redactar, no algo que ocultar.
- **Calibrar cifras hace que los datos parezcan demasiado perfectos** → el ruido por día y turno, los defectos y las tolerancias evitan curvas lisas; la declaración de datos generados va en 3.1.
- **`data/` pesa y se versiona sin querer** → se ignora en git salvo el README y `parametros.json`; los CSV se regeneran con la semilla.
- **Cifras del informe cambian después de generar** → `08-make-etl-update` regenera `data/` y marca la evidencia anterior como desactualizada hasta que el equipo repita el ETL.

## Migration Plan

No hay corridas previas ni datos. Se aplica sobre el capítulo 2 archivado. Primero la skill `08` con su generador y sus pruebas, luego `09`, luego el soporte de capturas en `report.py`, y al final la integración con el informe de ejemplo.

## Open Questions

Ninguna. Decididas por el usuario: `data/` no se versiona y los datos cubren de agosto de 2025 a octubre de 2026.
