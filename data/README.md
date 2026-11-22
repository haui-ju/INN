# Datos del proyecto

**Estos datos son generados** para el proyecto (`modo_datos: generado`): no provienen de una empresa real. Se calibraron con las cifras
del informe y se generan con una semilla fija, de modo que se pueden regenerar con `python3 .claude/skills/_shared/datagen.py generar`.
Esta carpeta no se versiona en git, salvo este archivo y `parametros.json`.

Semilla: 2026. Periodo: 2025-08-01 a 2026-10-31.

| Archivo | Contenido |
|---|---|
| `fue-01-caja.csv` | Líneas de venta del salón y para llevar (FUE-01) |
| `fue-02-rappi.csv` | Reporte de Rappi (FUE-02) |
| `fue-03-pedidosya.csv` | Reporte de PedidosYa (FUE-03), con nombres de columna distintos; la fecha lleva la hora |
| `fue-04-whatsapp.csv` | Pedidos del delivery propio (FUE-04), con el teléfono del cliente; la fecha lleva la hora |
| `fue-05-produccion.csv` | Producción por día y turno (FUE-05) |
| `fue-06-precios-pollo.csv` | Precio diario del pollo vivo (FUE-06); faltan algunos días |
| `apoyo-catalogo-productos.csv` | Lista de precios y receta de cada producto, con los nombres alternativos que usan las fuentes |
| `apoyo-costos-operativos.csv` | Costo operativo de cada mes (planilla, alquiler, servicios y otros) |
| `respuestas/` | Totales esperados tras una limpieza correcta (para verificar el ETL) y valores esperados de cada visual del dashboard |
| `salida/` | Tablas que el equipo exporta de Power BI (opcional) |

Las fuentes traen defectos a propósito (registros inválidos, duplicados, nombres de producto distintos, fechas con formatos mezclados,
nulos y días sin precio). Las fechas con barras son día/mes/año. Cada defecto está contado en `respuestas/defectos.csv`.
