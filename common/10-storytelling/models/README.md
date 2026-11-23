# Plantillas del storytelling

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea de la sección: `## 4. Storytelling con datos`.
- **Columnas y rótulos exactos** (la validación los lee): `Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya`; `**Contexto.**`, `**Hallazgos.**`, `**Qué muestra.**`, `**Qué decisión apoya.**`, `**Prioridades.**` y `**Metas pendientes.**`.
- Cada hallazgo lleva un encabezado `### HLZ-nn. Título` y, la primera vez que se usa una página, su captura con `<!-- captura: pag-nn -->`.
- El ejemplo es el caso Pollería Don Tito: sus KPI y valores son los de las plantillas de `07-make-data-model-kpi` y `09-make-dashboard`, y sus usuarios, los del brief de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [st-1-seccion-4](st-1-seccion-4.md) | `secciones/4.md` |
| [st-2-propuesta](st-2-propuesta.md) | la propuesta de hallazgos que se muestra y se confirma antes de escribir (no se guarda) |

Orden de trabajo: leer `valores.json` y las capturas de 09 → proponer los hallazgos y esperar la confirmación → copiar las capturas → escribir la sección 4 → revisar la redacción → validar.

## Archivos de la corrida

```
project/10-storytelling/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/4.md
├── capturas/pag-nn.png        (copias de las de 09; pag-nn.md con el pie)
├── referencias.md             (solo si cita)
└── README.md
```
