# Dependencias del dashboard

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/09-dashboard/<corrida>/`). Menciona un `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y quién lo lee

| Archivo | Se origina en | Lo leen |
|---|---|---|
| `secciones/3.2.md` (páginas `PAG`, valores de los KPI) | brief (usuarios), `modelo.json` (KPI y metas), `valores.json` y capturas del equipo | `10-make-storytelling` (cifras y capturas), `11-make-conclusions` (valor frente a meta), 12 |
| `anexos/C.md` (medidas `MED`) | `modelo.json` y las medidas finales del equipo | 12 (anexo C), 13 |
| `anexos/D.md` (descripción por página) | tabla de páginas de 3.2 | 12 (anexo D), 13 |
| `materiales/paginas.json`, `dashboard-referencia.html` y `guia-dashboard.md` | el plan confirmado, `modelo.json`, los tokens del diseño y `data/respuestas/` (`dashboard_ref.py construir`) | el equipo (para construir y comparar) |
| `valores.json` | el equipo (valor real de cada KPI) | `10-make-storytelling`, `11-make-conclusions` |
| `capturas/pag-nn.png` | el equipo | 12 (marcadores de captura de 3.2), `10-make-storytelling` |

## Qué afecta cada cambio

| Cambio | Edición | Qué debe traer el equipo | Skills `-update` a ejecutar después |
|---|---|---|---|
| Cambiar el valor real de un KPI | fila de 3.2 (valor, estado), `valores.json` y la lectura que lo cite | el valor y su captura | `10-make-storytelling-update` y `11-make-conclusions-update` |
| Cambiar una captura | `capturas/pag-nn.png` (y su pie) | la captura nueva | — |
| Agregar o quitar una página | fila de 3.2, marca de captura, anexo D, `capturas/`, `materiales/paginas.json` (y regenerar el HTML y la guía) | la captura de la página | — |
| Cambiar usuario, visuales o filtros de una página | fila de 3.2 y descripción del anexo D | la captura actualizada | — |
| Cambiar una medida | anexo C (tabla y bloque DAX); valores y estado si cambia el resultado | la medida final y los valores recalculados | `10` y `11` si cambió un valor |
| Cerrar una meta pendiente | `valores.json` (`meta`), fila de 3.2, «Metas pendientes» | — (la meta se cierra antes en 2.5) | `07-make-data-model-kpi-update` primero; después `11-make-conclusions-update` |
| Cambió un KPI o el modelo (después de `07-make-data-model-kpi-update`) | páginas y medidas que lo citan | valores y capturas de lo afectado | `10` y `11` |
| Cambió la carga (después de `08-make-etl-update`) | valores de los KPI y capturas | todo lo medido de nuevo | `10` y `11` |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Agregar un campo, un KPI o su fórmula | `07-make-data-model-kpi-update` |
| Cambiar la meta de un KPI en 2.5 | `07-make-data-model-kpi-update` |
| Cambiar cómo se limpian o cargan los datos | `08-make-etl-update` |
| Colores o tipografía de los visuales del informe | `02-design-system-update` |
