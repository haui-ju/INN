# Plantilla: Plan de páginas del dashboard (`materiales/paginas.json`)

| | |
|---|---|
| **Entregable** | `materiales/paginas.json` en la corrida (material para el equipo; no entra al informe) |
| **Punto** | Previo a 3.2: el plan confirmado del que salen el dashboard de referencia y la guía |
| **Códigos** | `PAG-nn`, `MED-nn`; cita `KPI-nn` y las tablas y campos de `modelo.json` |
| **Entradas** | el plan confirmado con el usuario, `modelo.json`, los usuarios del brief y `data/respuestas/` |
| **Salida** | `dashboard-referencia.html` y `guia-dashboard.md` (`python3 .claude/skills/_shared/dashboard_ref.py construir --run <corrida>`) |

## Instrucciones para el agente
1. Parte del plan por defecto (`dashboard_ref.py plan --run <corrida>` copia `common/09-dashboard/paginas-por-defecto.json`) y ajústalo a lo que el usuario confirmó. No lo escribas sin esa confirmación.
2. El archivo tiene `schema: 1`, `medidas`, `columnas_calculadas` y `paginas`. Cada medida lleva `codigo` (`MED-nn`), `nombre`, `explicacion`, `dax` (solo tablas y campos de `modelo.json`), `kpi` (o vacío) y `tablas`. Los nombres entre corchetes del DAX son nombres de otras medidas.
3. Cada página lleva `codigo`, `nombre`, `usuario` (uno del brief), `pregunta`, `kpis` (tarjetas de la fila superior), `segmentadores` (`Tabla[campo]`) y `visuales`.
4. Cada visual lleva `id`, `tipo` (`linea`, `columnas`, `apiladas`, `apiladas100`, `barras`, `matriz` o `tabla`), `titulo`, `pos` (`[columna, fila, ancho, alto]` en una rejilla de 12 columnas), `x`, `y`, `serie`, `origen` (tablas), `medidas` (códigos `MED-nn`), `filtros`, `unidad`, `lectura` (qué debe ver el equipo), `formato` y `datos`. `datos.fuente` es una de las que conoce `dashboard_ref.py` (`kpi_mensual`, `ventas_canal_mes`, `comision_mes`, `margen_canal`, `margen_canal_producto`, `merma_turno`, `merma_dia`, `prep_vend_dia`, `vendidos_pronostico`, `precio_dia`, `precio_mes`, `tabla_kpi`).
5. **Un solo eje vertical por gráfico.** Dos magnitudes de escala distinta van en dos gráficos alineados, no en un gráfico con dos ejes.
6. Cada columna calculada lleva `tabla`, `columna`, `donde` (Power Query, DAX o Especificar datos), `formula`, `campos`, `archivos` de origen y `explicacion`.
7. Todo KPI del modelo aparece en una página (en `kpis` o por una medida de sus visuales). `dashboard_ref.py construir` rechaza el plan si algo no cuadra con el modelo.
8. Los valores esperados salen de `data/respuestas/`: no se escriben en el plan ni se recalculan aquí.

## Formato

```json
{
  "schema": 1,
  "medidas": [{"codigo": "MED-01", "nombre": "[nombre]", "explicacion": "[cómo se calcula]", "dax": "[DAX]", "kpi": "", "tablas": ["[tabla]"]}],
  "columnas_calculadas": [{"tabla": "[tabla]", "columna": "[columna]", "donde": "Power Query", "formula": "[fórmula]", "campos": ["[campo]"], "archivos": ["[archivo]"], "explicacion": "[para qué sirve]"}],
  "paginas": [{"codigo": "PAG-01", "nombre": "[nombre]", "usuario": "[usuario del brief]", "pregunta": "[pregunta]", "kpis": ["KPI-01"], "segmentadores": ["[Tabla[campo]]"],
    "visuales": [{"id": 1, "tipo": "linea", "titulo": "[título]", "pos": [1, 1, 6, 1], "x": "[Tabla[campo]]", "y": "[[Medida]]", "serie": "", "origen": ["[tabla]"], "medidas": ["MED-01"],
                  "filtros": ["[filtro]"], "datos": {"fuente": "kpi_mensual", "kpi": "KPI-01"}, "unidad": "%", "lectura": "[qué debe ver el equipo]", "formato": "[ajustes de formato]"}]}]
}
```

## Ejemplo

```json
{
  "schema": 1,
  "medidas": [
    {"codigo": "MED-01", "nombre": "Venta bruta", "explicacion": "Suma de la venta bruta de las líneas válidas.", "dax": "SUM ( fPedidos[venta_bruta] )", "kpi": "", "tablas": ["fPedidos"]},
    {"codigo": "MED-02", "nombre": "Merma %", "explicacion": "Pollos de merma entre pollos preparados.", "dax": "DIVIDE ( SUM ( fProduccion[pollos_merma] ), SUM ( fProduccion[pollos_preparados] ) )", "kpi": "KPI-04", "tablas": ["fProduccion"]}
  ],
  "columnas_calculadas": [
    {"tabla": "fPedidos", "columna": "venta_bruta", "donde": "Power Query", "formula": "cantidad × precio_unitario − descuento", "campos": ["cantidad", "precio_unitario", "descuento"], "archivos": ["data/fue-01-caja.csv"], "explicacion": "Un solo importe para todas las fuentes."}
  ],
  "paginas": [
    {"codigo": "PAG-01", "nombre": "Merma por turno", "usuario": "Jefe de cocina", "pregunta": "¿Cuánto pollo se prepara de más en cada turno?", "kpis": ["KPI-04"], "segmentadores": ["dTurno[turno]"],
     "visuales": [
       {"id": 1, "tipo": "columnas", "titulo": "Merma por turno contra la meta", "pos": [1, 1, 12, 1], "x": "dTurno[turno]", "y": "[Merma %]", "serie": "", "origen": ["fProduccion", "dTurno"], "medidas": ["MED-02"],
        "filtros": ["Todo el periodo"], "datos": {"fuente": "merma_turno"}, "unidad": "%", "meta": {"kpi": "KPI-04"}, "lectura": "Los tres turnos pasan de la meta.", "formato": "Meta como línea constante."}
     ]}
  ]
}
```

## Checklist
- [ ] Cada página tiene un usuario del brief, una pregunta y sus KPI.
- [ ] Cada visual tiene tipo, ejes, medidas, tablas de origen, filtros y la fuente de sus valores esperados.
- [ ] El DAX de cada medida cita solo tablas y campos de `modelo.json`.
- [ ] Todo KPI del modelo está en una página y ningún gráfico tiene dos ejes verticales.
- [ ] Cada columna calculada dice dónde se crea, con qué fórmula y de qué archivos sale.
