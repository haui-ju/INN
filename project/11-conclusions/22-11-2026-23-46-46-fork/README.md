# Corrida 11-make-conclusions

- **Modo de datos:** generado.
- **Corridas de origen:** `07-make-data-model-kpi` 22-11-2026-18-10-31-fork, `09-make-dashboard` 22-11-2026-23-38-12-fork y `10-make-storytelling` 22-11-2026-23-42-21-fork.
- **Estados:** calculados con `rules/conclusions.py estados` a partir de `valores.json` de 09 frente a las metas de 2.5.
- **Valores del equipo:** los de 09 son los del dashboard final de dos páginas, del periodo completo (agosto de 2025 a octubre de 2026). Los estados no cambiaron con ellos.
- **OE-04:** el dashboard final no tiene la página de precio y margen, por lo que CNC-04 declara que el seguimiento diario y el cruce con el margen quedan pendientes.
- **Metas pendientes:** KPI-02 y KPI-06 (sus conclusiones CNC-02 y CNC-04 no concluyen cumplimiento), que se cierran con `07-make-data-model-kpi-update`.

## Origen de esta versión

Copia de la corrida `22-11-2026-20-20-59`. Cambios aplicados:

- Valores reales del dashboard final (periodo completo) en CNC-01 a CNC-03 y en el respaldo
- CNC-04 reescrito: el dashboard final no cruza el precio con el margen
- REC-03 y REC-05 ajustadas al dashboard de dos paginas; limitacion con el periodo completo
