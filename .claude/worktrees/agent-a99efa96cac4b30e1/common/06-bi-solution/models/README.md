# Plantillas de la solución de BI

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 2.1. Propuesta de solución en BI`, `## 2.2. Arquitectura de Inteligencia de Negocios` y `## 2.3. Herramientas utilizadas`.
- **Columnas y rótulos exactos** (la validación y el visual los leen): `**Decisiones que apoya.**`, `**Usuarios.**`, `**Respuesta a la problemática.**` y `Objetivo | Componentes | Cómo lo atiende`; `Código | Capa | Componente | Función | Entrada | Salida` y `**Flujo de los datos.**`; `Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada`.
- **Capas** con su nombre exacto: Fuentes, ETL, Almacenamiento y Visualización.
- El ejemplo es el caso Pollería Don Tito: sus objetivos y fuentes son los del brief de ejemplo y sus causas, las de la problemática de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [bs-1-propuesta](bs-1-propuesta.md) | `secciones/2.1.md` |
| [bs-2-arquitectura](bs-2-arquitectura.md) | `secciones/2.2.md` y la figura `arquitectura-bi` |
| [bs-3-herramientas](bs-3-herramientas.md) | `secciones/2.3.md` (sus herramientas también salen en la figura) |

Orden de trabajo: componentes de la arquitectura (2.2) → herramientas de cada capa (2.3) → propuesta que vincula cada objetivo con sus componentes (2.1). Con la confirmación del plan se escriben las tres secciones, `referencias.md` y `README.md`; luego se construye la figura con `--run` y se valida.

## Archivos de la corrida

```
project/06-bi-solution/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/2.1.md, 2.2.md y 2.3.md
├── visuales/arquitectura-bi.html (y su .json)
├── leer-imagen/arquitectura-bi.md
├── referencias.md
└── README.md
```

Ejemplo de `referencias.md` (una referencia por línea, APA 7, orden alfabético):

```markdown
Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). John Wiley & Sons.
Microsoft. (2026). *Power BI Desktop* [Software].
```
