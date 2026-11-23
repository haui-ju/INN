# Corrida 09-make-dashboard

- **Modo de datos:** generado (semilla 2026).
- **Corridas de origen:** `01-make-project-brief` 22-11-2026-18-10-13-fork, `07-make-data-model-kpi` 22-11-2026-18-10-31-fork y `08-make-etl` 22-11-2026-18-44-14.
- **Qué propuso la skill:** las páginas, las medidas DAX (`materiales/paginas.json`), el dashboard de referencia y la guía de construcción. En el anexo C los nombres de las medidas de KPI siguen los de la sección 2.5.
- **Qué entregó el equipo:** las capturas de las dos páginas del dashboard final (`capturas/pag-01.png` y `pag-02.png`) y los valores de los siete KPI, leídos de esas capturas. Son del **periodo completo** (agosto de 2025 a octubre de 2026), no de octubre, porque las tarjetas y la tabla del dashboard no filtran el último mes. `valores.json` usa los valores de la tabla de KPI (un decimal; KPI-06 con dos). KPI-07 sigue en 71,4 % (5 de 7 KPI con meta).
- **Medidas de texto en el anexo C (MED-18 a MED-35):** son las que el equipo creó para el chip, la meta y el color de las tarjetas y de la tabla de KPI. Los nombres de las medidas de cifras siguen los de la sección 2.5. `Mes de referencia` se documenta con `SWITCH` sobre `dCalendario[fecha]`, que da el mismo texto («oct 26») que la medida del equipo, porque `mes_anio` no es un campo de la sección 2.4.
- **Metas pendientes:** KPI-02 (margen de contribución) y KPI-06 (precio del pollo vivo). Propuesta para confirmar: KPI-02 «60 % o más» (el nivel de agosto y septiembre de 2025, antes de la caída) y KPI-06 «S/ 6.50 por kg o menos» (por encima del precio de 6.10 de antes de julio de 2026). Se registran con `07-make-data-model-kpi-update`.

## Origen de esta versión

Copia de la corrida `22-11-2026-18-39-12`. Cambios aplicados:

- Valores reales del dashboard final (periodo completo ago 2025 a oct 2026) en valores.json y 3.2
- Dashboard final de 2 paginas (PAG-03 y PAG-04 eliminadas; PAG-01 y PAG-02 redefinidas) con sus capturas pag-01 y pag-02
- Anexo D de 2 paginas y anexo C con las medidas de texto de tarjetas y tabla
