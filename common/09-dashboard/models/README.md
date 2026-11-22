# Plantillas del dashboard

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 3.2. Construcción del dashboard en Power BI`, `# Anexo C: Medidas y cálculos del dashboard` y `# Anexo D: Especificación y capturas del dashboard`.
- **Columnas y rótulos exactos** (la validación los lee): `Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI`; `Código | KPI | Valor real | Meta | Estado | Página`; `Código | Medida | Tipo | KPI | Tablas y campos`; `**Lectura del dashboard.**`, `**Metas pendientes.**`, `**Descripción.**`.
- Las medidas del anexo C llevan un encabezado `### MED-nn. Nombre` y su DAX en un bloque ```` ```dax ````; las páginas del anexo D, un encabezado `### PAG-nn. Nombre`.
- Cada captura se marca en 3.2 con `<!-- captura: pag-nn -->`, y su archivo es `capturas/pag-nn.png`.
- El ejemplo es el caso Pollería Don Tito: sus KPI son los de las plantillas de `07-make-data-model-kpi` y sus usuarios, los del brief de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [ds-1-paginas](ds-1-paginas.md) | `secciones/3.2.md` |
| [ds-2-medidas](ds-2-medidas.md) | `anexos/C.md` |
| [ds-3-especificacion](ds-3-especificacion.md) | `anexos/D.md` |
| [ds-4-valores-json](ds-4-valores-json.md) | `valores.json` y `capturas/` (los entrega el equipo) |
| [ds-5-paginas-json](ds-5-paginas-json.md) | `materiales/paginas.json` (plan de páginas que lee `dashboard_ref.py`) |

Orden de trabajo: especificación de páginas y medidas propuestas (se entregan al equipo) → el equipo construye el dashboard y entrega `valores.json` y las capturas → se escriben 3.2 y los anexos C y D → se valida.

## Archivos de la corrida

```
project/09-dashboard/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/3.2.md
├── anexos/C.md y D.md
├── materiales/                 (paginas.json, dashboard-referencia.html, guia-dashboard.md, paginas.txt y medidas.txt)
├── valores.json                (lo entrega el equipo)
├── capturas/pag-nn.png         (las entrega el equipo; pag-nn.md con el pie es opcional)
├── referencias.md              (solo si cita)
└── README.md
```
