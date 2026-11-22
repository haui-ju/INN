# Contratos de archivos del capítulo 3

Notas de trabajo del apply. Fijan los nombres y las columnas para que el generador, las skills 08 y 09 y el armado del informe se construyan por separado. Si una pieza necesita cambiar un contrato, lo dice antes de cambiarlo.

## `data/` (raíz del repositorio; ignorada por git salvo README y parámetros)

| Archivo | Contenido |
|---|---|
| `parametros.json` | `{schema: 1, semilla, periodo: {inicio: "2025-08-01", fin: "2026-10-31"}, locales: 1, ventas_anuales_uit, valor_uit, canales: [{nombre, comision_pct, participacion_inicial, participacion_final}], productos: [{nombre, categoria, precio, costo}], merma_pct, margen_neto: {inicial, final}, precio_pollo: {inicial, julio_antes, julio_despues}, crecimiento_interanual, tolerancias: {cifra: valor}, origen: {cifra: "dónde sale"}}` |
| `README.md` | Archivos, semilla, declaración de datos generados |
| `fue-01-caja.csv` | `ticket_id, fecha, hora, turno, canal, producto, cantidad, precio_unitario, descuento, estado` |
| `fue-02-rappi.csv` | `pedido_id, fecha_hora, producto, cantidad, monto, comision, estado` |
| `fue-03-pedidosya.csv` | `nro_pedido, fecha (con hora), item, cant, total, comision_pct, estado` (nombres distintos a propósito) |
| `fue-04-whatsapp.csv` | `pedido, fecha (con hora), telefono, producto, cantidad, monto, tipo_entrega` (el teléfono se anonimiza en el ETL) |
| `fue-05-produccion.csv` | `fecha, turno, pollos_preparados, pollos_vendidos, pollos_merma, responsable` |
| `fue-06-precios-pollo.csv` | `fecha, precio_kg` (hay días sin precio: el día no tiene fila) |
| `apoyo-catalogo-productos.csv` | `producto, categoria, precio_lista, pollos_equivalentes, kg_pollo_vivo, costo_otros, alias` (alias separados por `\|`) |
| `apoyo-costos-operativos.csv` | `mes, planilla, alquiler, servicios, otros, total` |
| `respuestas/filas-por-fuente.csv` | `fuente, filas_brutas, filas_validas` |
| `respuestas/ventas-mes-canal.csv` | `mes (AAAA-MM), canal, lineas, ventas, comision` (sobre registros válidos) |
| `respuestas/produccion-mes-turno.csv` | `mes, turno, preparados, vendidos, merma` |
| `respuestas/precio-mes.csv` | `mes, precio_medio, dias_imputados` |
| `respuestas/defectos.csv` | `fuente, defecto, registros, regla_sugerida` |
| `respuestas/kpi-esperados.csv` | `kpi (KPI-nn), mes, valor, unidad` |
| `salida/<tabla>.csv` | Tablas que el equipo exporta de Power BI (`fPedidos`, `fProduccion`, `fPrecioInsumo`, `fMetaKpi`, `dCalendario`, ...). Opcional: sin ellas, el equipo teclea los totales |

El costo estimado de cada línea es `cantidad × (kg_pollo_vivo × precio_kg del día + costo_otros)`, con el último precio disponible cuando falta el día; el costo operativo de cada línea es el `total` del mes repartido en proporción a la venta del mes. Las fechas con barras son día/mes/año.

Los nombres de canal son `Salón`, `Para llevar`, `WhatsApp`, `Rappi`, `PedidosYa`; los turnos, `Mañana`, `Tarde`, `Noche`. Los tipos de defecto (columna `defecto`) son: `registro_invalido`, `duplicado`, `nombre_producto`, `formato_fecha`, `nulo`, `dia_sin_precio`.

## Corrida de `08-make-etl` (`project/08-etl/<corrida>/`)

`secciones/3.1.md`, `anexos/A.md`, `anexos/B.md`, `referencias.md` (si cita), `README.md` y los de entrada del equipo:

- `evidencia.json`: `{schema: 1, reglas: [{codigo: "REG-01", filas_antes, filas_despues}], tablas: [{nombre, filas}], totales: {ventas_total, comision_total, lineas_total}, verificacion: {estado: "coincide" | "diferencias", diferencias: [{tabla, mes, esperado, obtenido}]}}`.
- `capturas/<id>.png` (opcional): capturas de Power Query.

Códigos: `REG-nn` (regla de calidad), `PAS-nn` (paso de Power Query).

## Corrida de `09-make-dashboard` (`project/09-dashboard/<corrida>/`)

`secciones/3.2.md`, `anexos/C.md`, `anexos/D.md`, `referencias.md` (si cita), `README.md` y los de entrada del equipo:

- `valores.json`: `{schema: 1, kpis: [{codigo: "KPI-01", valor, unidad, meta, periodo}], medidas: [{codigo: "MED-01", valor}]}`. `meta` es `null` si el KPI sigue sin meta.
- `capturas/pag-<nn>.png` y `capturas/pag-<nn>.md` (una línea con el pie de la captura). El id coincide con el código de la página `PAG-<nn>` en minúscula; la sección marca cada una con `<!-- captura: pag-<nn> -->`.

Códigos: `PAG-nn` (página) y `MED-nn` (medida).

## Marcador de captura (`12-make-report`)

`<!-- captura: <id> -->` en una línea sola. Se busca `capturas/<id>.png` en la corrida de la sección; el pie sale de `capturas/<id>.md` o, si falta, del título de la sección. Se numera junto con las figuras y se copia a `imagenes/<id>.png`.

## Reparto de archivos entre piezas

Para no pisarse, cada pieza escribe solo en lo suyo:

| Pieza | Escribe en |
|---|---|
| Generador | `_shared/datagen.py`, `_shared/tests/test_datagen.py`, `data/` |
| Capturas en el informe | `_shared/report.py`, `_shared/tests/test_report.py` (clase nueva), `common/12-report/guia.md`, `12-make-report/SKILL.md` |
| Skill 08 | `.claude/skills/08-make-etl*`, `common/08-etl/`, `_shared/rules/etl.py`, `_shared/etl_verificacion.py`, `_shared/tests/test_etl.py` y `etl_fixtures.py` |
| Skill 09 | `_shared/dashboard_dax.py` (módulo puro de las medidas DAX), `.claude/skills/09-make-dashboard*`, `common/09-dashboard/`, `_shared/rules/dashboard.py`, `_shared/tests/test_dashboard.py` y `dashboard_fixtures.py` |
| Integración (al final) | Los archivos compartidos: `diagnostico.py`, `visuales.py`, `validate_run.py`, `tests/report_fixtures.py` y `diagnostico_fixtures.py` |
