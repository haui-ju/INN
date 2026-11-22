# Plantillas de la problemática y los objetivos

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 1.8. Problemática central del negocio`, `## 1.9. Objetivo general del proyecto` y `## 1.10. Objetivos específicos`.
- **Rótulos y columnas exactos** (la validación los lee): `**Enunciado.**`, `**Afectados.**`, `**Causas principales.**`, `**Evidencia.**`, `**Matriz de articulación.**`, `**Lectura de la matriz.**`; las tablas de objetivos del brief y `Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador`.
- El ejemplo es el caso Pollería Don Tito: sus objetivos son los del brief de ejemplo y sus códigos, los del análisis estratégico de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [po-1-problematica](po-1-problematica.md) | `secciones/1.8.md` |
| [po-2-objetivo-general](po-2-objetivo-general.md) | `secciones/1.9.md` |
| [po-3-objetivos-especificos](po-3-objetivos-especificos.md) | `secciones/1.10.md` (objetivos y matriz de articulación) |

Orden de trabajo: se leen el brief y las corridas vigentes de `03` y `04`, se proponen las causas principales y la matriz, se confirman con el usuario y se escriben las tres secciones y el `README.md` (y `referencias.md` si hay citas); luego se valida.

## Archivos de la corrida

```
project/05-problem-objectives/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/1.8.md, 1.9.md y 1.10.md
├── referencias.md      (solo si hay citas)
└── README.md
```
