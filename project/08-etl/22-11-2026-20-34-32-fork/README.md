# Corrida 08-make-etl

- **Modo de datos:** generado (semilla 2026, de `data/parametros.json`).
- **Corridas de origen:** `06-make-bi-solution` 22-11-2026-18-10-23-fork y `07-make-data-model-kpi` 22-11-2026-18-10-31-fork.
- **Qué propuso el agente:** los materiales (`materiales/guia-power-query.md`), la redacción de 3.1 y de los anexos A y B.
- **Qué trajo el equipo:** nada todavía. `evidencia.json` y el código del anexo B son **valores provisionales**: las cifras salen de la hoja de respuestas (`data/respuestas/`) y el código es el propuesto en la guía. El equipo los reemplaza con sus resultados de Power Query y vuelve a redactar con `08-make-etl-update`.
- **Pendiente de reemplazar:** `evidencia.json` (filas por regla, fuente y tabla; totales), el código de cada paso en `anexos/B.md` y, si las hay, las capturas de Power Query en `capturas/`.

## Origen de esta versión

Copia de la corrida `22-11-2026-18-44-14`. Cambios aplicados:

- Agregar data/limpio con los CSV ya limpios (etl_limpio.py) para que el equipo solo cree las columnas del modelo

## Cambios del fork 22-11-2026-20-34-32

- Se agregó `data/limpio/` (fuera de la corrida) con los CSV ya limpios, generados con `.claude/skills/_shared/etl_limpio.py`: pedidos unificados con las copias y los inválidos marcados, producción depurada, precios diarios completos y los archivos de apoyo. El equipo solo crea las columnas del modelo; la lista con sus fórmulas está en `data/limpio/README.md`.
- La evidencia, la sección 3.1 y los anexos no cambian: las cifras de `data/limpio/` coinciden con ellas (91 297 filas, 674 duplicadas, 89 888 válidas, 886 clientes, 20 días imputados).
