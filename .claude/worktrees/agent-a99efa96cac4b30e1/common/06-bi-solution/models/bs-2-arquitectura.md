# Plantilla: Arquitectura de BI (`secciones/2.2.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.2.md` y la figura `arquitectura-bi` |
| **Punto** | 2.2. Arquitectura de Inteligencia de Negocios |
| **Códigos** | `CAP-nn` (componentes); cita `FUE-nn` (del brief) y `HER-nn` (de 2.3) |
| **Entradas** | fuentes previstas del brief (sección 6), herramientas de 2.3, alcance del brief |
| **Salida** | los componentes de las cuatro capas, en orden, con su función, entrada y salida |

## Instrucciones para el agente
1. La primera línea es `## 2.2. Arquitectura de Inteligencia de Negocios`.
2. Un párrafo que presenta la arquitectura con su cita (Kimball & Ross, 2013) y la marca `<!-- figura: arquitectura-bi -->` en una línea sola.
3. La tabla `Código | Capa | Componente | Función | Entrada | Salida`, ordenada por capa: Fuentes, ETL, Almacenamiento y Visualización (nombres exactos), con al menos un componente por capa.
4. En la capa de fuentes, un componente por fuente del brief con su código entre paréntesis (`Sistema de caja de los locales (FUE-01)`). Una fuente que el brief no prevé se nombra sin código y se sugiere agregarla al brief.
5. En ETL y almacenamiento, la función nombra la herramienta de 2.3 por su código (`HER-02`); si está «Pendiente», dice «con la herramienta que se defina».
6. **Flujo de los datos.** Dos o tres frases que recorren la arquitectura de las fuentes al dashboard y dicen con qué frecuencia se actualiza.
7. Después de escribir 2.2 y 2.3: `python3 .claude/skills/_shared/visuales.py construir --visual arquitectura-bi --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 2.2. Arquitectura de Inteligencia de Negocios

[Párrafo que presenta la arquitectura, con su cita.]

<!-- figura: arquitectura-bi -->

Tabla 1: Componentes de la arquitectura de BI

| Código | Capa | Componente | Función | Entrada | Salida |
|---|---|---|---|---|---|
| CAP-01 | Fuentes | [fuente] (FUE-01) | [qué registra] | [qué datos entran] | [archivo o consulta que entrega] |
| CAP-02 | ETL | [proceso] | [qué transforma, con HER-nn] | CAP-01 | [tablas limpias] |
| CAP-03 | Almacenamiento | [repositorio] | [qué guarda, con HER-nn] | CAP-02 | [tablas del modelo] |
| CAP-04 | Visualización | [dashboard] | [qué muestra, con HER-nn] | CAP-03 | [dashboard para los usuarios] |

**Flujo de los datos.** [Recorrido de las fuentes al dashboard y frecuencia de actualización.]
```

## Ejemplo

```markdown
## 2.2. Arquitectura de Inteligencia de Negocios

La arquitectura sigue el enfoque dimensional de Kimball y Ross (2013): los datos se extraen de sus fuentes, se limpian e integran en un proceso ETL, se guardan como tablas de hechos y dimensiones y se analizan en un modelo semántico con su dashboard. La figura muestra las cuatro capas de la solución de Pollería Don Tito y sus componentes.

<!-- figura: arquitectura-bi -->

Tabla 1: Componentes de la arquitectura de BI

| Código | Capa | Componente | Función | Entrada | Salida |
|---|---|---|---|---|---|
| CAP-01 | Fuentes | Sistema de caja de los locales (FUE-01) | Registra cada venta por ticket, canal y turno, incluidos los pedidos de WhatsApp | Ventas en salón, para llevar y delivery propio | Exportación mensual de tickets en CSV |
| CAP-02 | Fuentes | Reportes de las apps de delivery (FUE-02) | Detalla los pedidos y la comisión que cobra cada aplicación | Pedidos de Rappi y PedidosYa | Reportes mensuales en Excel |
| CAP-03 | Fuentes | Precios del pollo vivo en Lima Metropolitana (FUE-03) | Publica el precio diario del pollo vivo por kilogramo | Precios del mercado mayorista | Serie diaria descargada en CSV |
| CAP-04 | Fuentes | Control de producción de cocina | Anota los pollos preparados y sobrantes de cada turno | Conteo del jefe de cocina al cierre del turno | Hoja de cálculo diaria |
| CAP-05 | ETL | Proceso de extracción, limpieza e integración | Unifica canales, productos y fechas, aplica las reglas de calidad y calcula el costo del pollo y la merma, con la herramienta que se defina (HER-02) | CAP-01, CAP-02, CAP-03 y CAP-04 | Tablas depuradas de hechos y dimensiones y registro de calidad de cada carga |
| CAP-06 | Almacenamiento | Repositorio del modelo estrella | Guarda las tablas depuradas del modelo con la herramienta que se defina (HER-03) | CAP-05 | Tablas de hechos y dimensiones listas para Power BI |
| CAP-07 | Visualización | Modelo semántico en Power BI | Relaciona las tablas y calcula las medidas de los KPI con HER-04 | CAP-06 | Medidas de margen, merma, precio del insumo y calidad de datos |
| CAP-08 | Visualización | Dashboard de rentabilidad y merma | Presenta los KPI por canal, turno, local y periodo con filtros, con HER-04 | CAP-07 | Páginas para la gerencia y el jefe de cocina |

**Flujo de los datos.** Cada mes se exportan las ventas de la caja y los reportes de las aplicaciones, se descarga la serie de precios y se reúne el control de producción. El proceso ETL los limpia, los integra y deja las tablas del modelo en el repositorio, desde donde Power BI actualiza el modelo semántico y el dashboard que revisa la gerencia en su reunión semanal.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: arquitectura-bi -->`.
- [ ] Las cuatro capas, en orden, cada una con al menos un componente.
- [ ] Cada `FUE` del brief está en un componente de la capa de fuentes.
- [ ] Cada componente tiene función, entrada y salida.
- [ ] La cita de Kimball y Ross (2013) está en `referencias.md`.
