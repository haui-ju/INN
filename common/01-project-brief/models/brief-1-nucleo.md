# Plantilla: Brief del proyecto (`brief.md`)

| | |
|---|---|
| **Entregable** | `brief.md` |
| **Entradas** | respuestas del usuario sección por sección, `project/config.yaml` (nombre, tipo, rubro, equipo, modo de datos) |
| **Salida** | el núcleo del proyecto de Inteligencia de Negocios: lo leen todas las demás skills |

## Instrucciones para el agente
1. Recorre las secciones **en orden**, una por una; en cada una pregunta lo mínimo necesario, propón una redacción a partir de lo que el usuario cuenta y ajústala con él hasta que la confirme (guía, sección 1).
2. Los títulos de nivel 2 y 3 son exactos (la validación los lee). La justificación es un solo rótulo de uno o dos párrafos.
3. Lo que el usuario no sabe queda **«Pendiente»** (en una celda o como texto de la sección); nunca lo redactes como hecho. Con `modo_datos: real` usa solo lo que el usuario informa.
4. Los plazos de los objetivos son `Entrega (DD-MM-AAAA)` y esa fecha es la entrega de la sección 7 (o `Entrega (Pendiente)` si aún no hay fecha).
5. Cada objetivo dice en la columna **Indicador** con qué KPI del dashboard o indicador del negocio se medirá; los KPI se definen después en `07-make-data-model-kpi` y deben poder medirlo.
6. En la sección 6, cada fuente lleva su **Tipo** (`Interna`, `Abierta` o `Generada`) y su **Acceso** (`Autorizado`, `Público` o `Pendiente`). Una empresa real sin autorización solo usa fuentes `Abierta` o `Generada`.
7. Las fechas van en `DD-MM-AAAA`. Los códigos son `OG-01`, `OE-nn`, `FUE-nn` e `INI-nn`.

## Formato

```markdown
# Brief del proyecto · [nombre]

## 1. Tema y empresa

[tema en una frase: problema del negocio y solución de BI]

**Empresa.** [nombre comercial, giro y tamaño, o «Proyecto propio»]

## 2. Problemática

**Problema principal.** [qué duele al negocio]

**Quién lo sufre.** [áreas o personas afectadas]

**Situación actual.** [cómo se decide hoy, con qué datos]

**Evidencia.**
- [dato, observación o fuente]

## 3. Objetivos

### 3.1. Objetivo general

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | [verbo + qué + para qué] | [métrica] | [meta con cifra] | Entrega ([fecha]) | [KPI o indicador] |

### 3.2. Objetivos específicos

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | [verbo + qué] | [métrica] | [meta con cifra] | Entrega ([fecha]) | OG-01 | [KPI o indicador] |

## 4. Justificación y alcance

**Justificación.** [Uno o dos párrafos: qué decisión mejora y para quién, qué impacto tiene en ventas, costos o margen y por qué una solución de BI (datos, ETL, modelo y dashboard).]

### 4.1. Alcance

| Alcance | Detalle |
|---|---|
| Incluye | [procesos, áreas y periodo de datos que entran] |
| No incluye | [qué queda fuera] |
| Herramientas previstas | [Power BI y otras, o Pendiente] |

### 4.2. Limitaciones

| Limitación | Detalle |
|---|---|
| [limitación] | [efecto y cómo se maneja] |

## 5. Usuarios y decisiones

**Usuarios.** [quiénes usarán el dashboard y quién decide]

**Decisiones que apoyará el dashboard.**
- [decisión concreta]

## 6. Fuentes de datos previstas

| Código | Fuente | Tipo | Datos | Acceso |
|---|---|---|---|---|
| FUE-01 | [sistema, archivo o portal] | Interna, Abierta o Generada | [qué datos y periodo] | Autorizado, Público o Pendiente |

## 7. Calendario

| Inicio | Entrega |
|---|---|
| [DD-MM-AAAA o Pendiente] | [DD-MM-AAAA o Pendiente] |

## 8. Supuestos y riesgos iniciales

| Código | Tipo | Descripción | Cómo se vigila |
|---|---|---|---|
| INI-01 | Supuesto o Riesgo | [descripción] | [cómo se vigila] |
```

## Ejemplo

```markdown
# Brief del proyecto · Rentabilidad por canal de Pollería Don Tito

## 1. Tema y empresa

Un dashboard en Power BI para que la gerencia de una pollería vea cuánto deja realmente cada canal de venta y cuánto pollo se pierde por turno, y decida precios, producción y compras con datos.

**Empresa.** Pollería Don Tito, restaurante de pollo a la brasa con dos locales en San Juan de Lurigancho; pequeña empresa.

## 2. Problemática

**Problema principal.** Las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %.

**Quién lo sufre.** La gerencia y el jefe de cocina, que deciden precios, producción y compras sin ver la rentabilidad por canal ni la merma.

**Situación actual.** Los precios son iguales en todos los canales, la producción se decide por experiencia y el costo del insumo no se monitorea.

**Evidencia.**
- Las apps de delivery pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión.
- La merma es de 7 % de los pollos preparados, frente a un 3 % de referencia.

## 3. Objetivos

### 3.1. Objetivo general

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | Diseñar e implementar una solución de BI que muestre la rentabilidad por canal y la merma para apoyar las decisiones de la gerencia | Decisiones de precio y producción respaldadas por el dashboard | 3 decisiones documentadas | Entrega (30-11-2026) | Margen neto por canal |

### 3.2. Objetivos específicos

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | Integrar las ventas, costos y comisiones en un modelo estrella depurado | Registros que pasan las reglas de calidad | 98 % o más | Entrega (30-11-2026) | OG-01 | Calidad de datos del ETL |
| OE-02 | Medir la rentabilidad real de cada canal de venta | Canales con margen calculado | 5 de 5 canales | Entrega (30-11-2026) | OG-01 | Margen neto por canal |
| OE-03 | Identificar los turnos con mayor merma de pollo | Turnos con merma medida | 100 % de los turnos del periodo | Entrega (30-11-2026) | OG-01 | Porcentaje de merma por turno |

## 4. Justificación y alcance

**Justificación.** La gerencia podrá fijar precios por canal y ajustar la producción por turno con cifras y no por intuición. Recuperar parte del margen perdido en las apps y reducir la merma tiene un efecto directo en la utilidad del negocio.

Una solución de BI integra fuentes dispersas con un proceso ETL, las ordena en un modelo dimensional y las presenta en un dashboard interactivo orientado a la decisión.

### 4.1. Alcance

| Alcance | Detalle |
|---|---|
| Incluye | Ventas por canal, costos de insumos, comisiones y producción por turno de los dos locales, de enero a octubre de 2026 |
| No incluye | Contabilidad completa, planillas ni predicción de demanda |
| Herramientas previstas | Power BI Desktop; herramienta de ETL Pendiente |

### 4.2. Limitaciones

| Limitación | Detalle |
|---|---|
| Datos | Los datos internos se generan con reglas coherentes con el rubro; los precios del insumo vienen de fuentes abiertas |
| Tiempo | Una sola entrega; se priorizan los KPI de margen y merma |

## 5. Usuarios y decisiones

**Usuarios.** Gerente general (decide) y jefe de cocina (ejecuta la producción).

**Decisiones que apoyará el dashboard.**
- Ajustar el precio de los combos en las apps de delivery.
- Definir cuántos pollos hornear por turno y día de la semana.
- Anticipar compras ante subidas del precio del pollo vivo.

## 6. Fuentes de datos previstas

| Código | Fuente | Tipo | Datos | Acceso |
|---|---|---|---|---|
| FUE-01 | Sistema de caja de los locales | Generada | Ventas por ticket, canal y turno, enero a octubre de 2026 | Autorizado |
| FUE-02 | Reportes de las apps de delivery | Generada | Pedidos y comisiones por app | Autorizado |
| FUE-03 | Precios del pollo vivo en Lima Metropolitana | Abierta | Precio diario por kilogramo | Público |

## 7. Calendario

| Inicio | Entrega |
|---|---|
| 01-11-2026 | 30-11-2026 |

## 8. Supuestos y riesgos iniciales

| Código | Tipo | Descripción | Cómo se vigila |
|---|---|---|---|
| INI-01 | Supuesto | La gerencia usará el dashboard en su reunión semanal | Se revisa con el usuario en la exposición |
| INI-02 | Riesgo | Las fuentes abiertas de precios no cubren todo el periodo | Se registra la cobertura en el diccionario de datos |
```

## Plantilla de `domain.md`
Es la de `.claude/skills/01-make-project-brief/references/domain-plantilla.md`; la crea `01-make-project-brief` después de confirmar el brief.

## Checklist
- [ ] Las ocho secciones están, con sus títulos exactos.
- [ ] `OG-01` y al menos dos `OE`, cada uno con métrica, meta, plazo `Entrega (fecha)` e indicador.
- [ ] Los plazos coinciden con la entrega de la sección 7.
- [ ] Hay al menos una decisión que apoyará el dashboard y una fuente de datos con tipo y acceso válidos.
- [ ] La entrega no es anterior al inicio.
- [ ] Lo desconocido dice «Pendiente»; nada se redactó como hecho.
