# Plantillas del modelo de datos y los KPI

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones` y `## 2.5. Indicadores clave de rendimiento`.
- **Columnas y rótulos exactos** (la validación y el visual los leen): `Código | Tabla de hechos | Granularidad | Medidas | Claves`; `Código | Dimensión | Clave | Atributos | Jerarquías`; `Código | Desde | Hacia | Campos | Cardinalidad | Filtro`; `Código | KPI | Fórmula | Medida propuesta | Origen`; `Código | Meta | Frecuencia | Objetivo | Decisión que apoya`; `**Lectura del modelo.**` y `**Lectura de los KPI.**`.
- Las medidas se escriben `nombre (agregación)` separadas por punto y coma, y el origen de un KPI `tabla.campo` separado por punto y coma.
- El ejemplo es el caso Pollería Don Tito: sus objetivos son los del brief de ejemplo y sus fuentes, las de la arquitectura de ejemplo de `06-make-bi-solution`.

## Índice

| Plantilla | Genera |
|---|---|
| [dm-1-modelo](dm-1-modelo.md) | `secciones/2.4.md` y la figura `modelo-datos` |
| [dm-2-kpi](dm-2-kpi.md) | `secciones/2.5.md` |
| [dm-3-modelo-json](dm-3-modelo-json.md) | `modelo.json` (el mismo modelo y los mismos KPI como datos) |

Orden de trabajo: modelo (2.4) → KPI (2.5, que usa campos del modelo) → `modelo.json` (copia de ambos) → figura. Con la confirmación del plan se escriben las secciones, `modelo.json`, `referencias.md` y `README.md`; luego se construye la figura con `--run` y se valida.

## Archivos de la corrida

```
project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/2.4.md y 2.5.md
├── modelo.json
├── visuales/modelo-datos.html (y su .json)
├── leer-imagen/modelo-datos.md
├── referencias.md
└── README.md
```

Ejemplo de `referencias.md` (una referencia por línea, APA 7, orden alfabético):

```markdown
Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). Wiley.
```
