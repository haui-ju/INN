# Plantillas del ETL

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 3.1. Construcción de la solución ETL`, `# Anexo A: Diccionario de datos y calidad de datos` y `# Anexo B: Scripts del ETL`.
- **Columnas y rótulos exactos** (la validación los lee): `Código | Fuente | Archivo | Filas leídas`; `Código | Paso | Tabla | Resultado`; `Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después`; `Tabla | Filas cargadas`; `Tabla | Mes | Esperado | Obtenido | Diferencia`; en el anexo A, `Fuente | Campo | Tipo | Regla de calidad | Destino`, `Tabla | Campo | Origen` y `Código | Filas antes | Filas después | Diferencia`; rótulos `**Extracción.**`, `**Transformación.**`, `**Reglas de calidad.**`, `**Carga.**`, `**Verificación.**` y `**Lectura del ETL.**`.
- Los tipos de defecto son `registro_invalido`, `duplicado`, `nombre_producto`, `formato_fecha`, `nulo` y `dia_sin_precio`.
- El ejemplo es el caso Pollería Don Tito: sus fuentes son las del brief de ejemplo y sus tablas, las del modelo de ejemplo de `07-make-data-model-kpi`. Las cifras de los ejemplos son coherentes entre sí (sección, anexo A y evidencia).

## Índice

| Plantilla | Genera |
|---|---|
| [etl-1-seccion-3-1](etl-1-seccion-3-1.md) | `secciones/3.1.md` |
| [etl-2-anexo-a](etl-2-anexo-a.md) | `anexos/A.md` |
| [etl-3-anexo-b](etl-3-anexo-b.md) | `anexos/B.md` |
| [etl-4-guia-power-query](etl-4-guia-power-query.md) | `materiales/guia-power-query.md` (para el equipo) |
| [etl-5-evidencia-json](etl-5-evidencia-json.md) | `evidencia.json` (lo trae el equipo) |

Orden de trabajo: datos y guía de Power Query → pausa: el equipo ejecuta y trae la evidencia → `evidencia.json` → comparación con la hoja de respuestas → 3.1 → anexos A y B → validación.

## Archivos de la corrida

```
project/08-etl/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/3.1.md
├── anexos/A.md y B.md
├── materiales/guia-power-query.md
├── evidencia.json
├── capturas/ (opcional, capturas de Power Query)
├── referencias.md (si cita)
└── README.md
```
