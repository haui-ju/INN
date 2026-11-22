# Plantilla: Arquitectura de Inteligencia de Negocios (`secciones/2.2.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.2.md` y la figura `arquitectura-bi` |
| **Punto** | 2.2. Arquitectura de Inteligencia de Negocios |
| **Códigos** | `CAP-nn`; cita `FUE-nn` del brief |
| **Entradas** | fuentes de datos del brief, objetivos, alcance y herramientas previstas |
| **Salida** | los componentes de la solución en cuatro capas (fuentes, ETL, almacenamiento y visualización) y su figura |

## Instrucciones para el agente
1. La primera línea es `## 2.2. Arquitectura de Inteligencia de Negocios`.
2. Un párrafo que presenta las cuatro capas **en este orden**: Fuentes, ETL, Almacenamiento y Visualización, con su cita (por ejemplo, Kimball y Ross, 2013).
3. La marca `<!-- figura: arquitectura-bi -->` en una línea sola.
4. Tabla `Código | Capa | Componente | Función | Entrada y salida`, ordenada por capa (nombres exactos: Fuentes, ETL, Almacenamiento, Visualización). **Un componente de Fuentes por cada `FUE-nn` del brief**, con su código en el nombre del componente; al menos un componente en cada una de las otras tres capas.
5. El nombre del componente describe su función, no la herramienta; si el usuario ya decidió la herramienta, el nombre puede nombrarla (por ejemplo, «Transformación con Power Query»).
6. **Lectura de la arquitectura.** Una o dos frases: cómo fluye el dato desde la fuente hasta la decisión.
7. Después de escribir 2.2 y 2.3: `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 2.2. Arquitectura de Inteligencia de Negocios

[Párrafo que presenta las cuatro capas, con su cita.]

<!-- figura: arquitectura-bi -->

Tabla 1: Componentes de la arquitectura de BI

| Código | Capa | Componente | Función | Entrada y salida |
|---|---|---|---|---|
| CAP-01 | Fuentes | [fuente] (FUE-01) | [qué aporta] | [entrada] → [salida] |
| CAP-nn | ETL | [componente] | [qué hace] | [entrada] → [salida] |
| CAP-nn | Almacenamiento | [componente] | [qué guarda] | [entrada] → [salida] |
| CAP-nn | Visualización | [componente] | [qué muestra] | [entrada] → [salida] |

**Lectura de la arquitectura.** [Cómo fluye el dato hasta la decisión.]
```

## Ejemplo

```markdown
## 2.2. Arquitectura de Inteligencia de Negocios

La arquitectura de la solución sigue las cuatro capas de un sistema de inteligencia de negocios: las fuentes que generan los datos, el proceso ETL que los extrae, depura y transforma, el almacenamiento donde queda el modelo dimensional y la visualización donde se consulta (Kimball & Ross, 2013). Cada capa tiene componentes con una función definida y las herramientas se eligen en el punto 2.3.

<!-- figura: arquitectura-bi -->

Tabla 1: Componentes de la arquitectura de BI

| Código | Capa | Componente | Función | Entrada y salida |
|---|---|---|---|---|
| CAP-01 | Fuentes | Sistema de caja de los locales (FUE-01) | Aporta las ventas por ticket, canal y turno | Registro de caja → archivos de ventas |
| CAP-02 | Fuentes | Reportes de las apps de delivery (FUE-02) | Aporta los pedidos y las comisiones por aplicación | Reportes de las apps → archivos de pedidos |
| CAP-03 | Fuentes | Precios del pollo vivo en Lima Metropolitana (FUE-03) | Aporta el costo diario del insumo | Portal de precios → archivo de precios diarios |
| CAP-04 | ETL | Proceso ETL (herramienta pendiente) | Extrae, depura, homologa y anexa las tres fuentes, y descarta duplicados | Archivos de las tres fuentes → tablas limpias |
| CAP-05 | Almacenamiento | Modelo dimensional | Guarda los hechos y las dimensiones que consume el dashboard | Tablas limpias → modelo en estrella |
| CAP-06 | Visualización | Dashboard de rentabilidad y merma | Muestra los KPI, el margen por canal y la merma por turno | Modelo en estrella → páginas e indicadores |

**Lectura de la arquitectura.** El dato viaja desde la caja, las aplicaciones y el portal de precios hasta un modelo único, y de ahí a un dashboard que la gerencia consulta antes de decidir precios, producción y compras.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: arquitectura-bi -->` una sola vez.
- [ ] Las cuatro capas aparecen en el orden Fuentes, ETL, Almacenamiento y Visualización.
- [ ] Cada `FUE-nn` del brief tiene su componente en la capa de fuentes.
- [ ] Cada fila tiene función y entrada y salida.
- [ ] La figura y su explicación están construidas con `visuales.py construir`.
