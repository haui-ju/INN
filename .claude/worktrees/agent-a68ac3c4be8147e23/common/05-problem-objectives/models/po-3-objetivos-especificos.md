# Plantilla: Objetivos específicos y matriz de articulación (`secciones/1.10.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.10.md` |
| **Punto** | 1.10. Objetivos específicos |
| **Códigos** | `OE-nn` (del brief); cita `CAU`, `FOR`, `DEB`, `OPO`, `AME`, `FO`, `FA`, `DO`, `DA` y los códigos PESTEL de la corrida vigente de `04` |
| **Entradas** | brief vigente (sección 3.2), corridas vigentes de `03` (Canvas) y `04` (PESTEL, FODA e Ishikawa), causas principales de 1.8 |
| **Salida** | los objetivos específicos copiados del brief y la matriz que articula cada uno con el diagnóstico |

## Instrucciones para el agente
1. La primera línea es `## 1.10. Objetivos específicos`.
2. Una frase y la tabla `Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador` **copiada sin cambios** de la sección 3.2 del brief.
3. **Matriz de articulación.** Una frase y la tabla `Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador` con una fila por `OE`: causas que atiende (al menos una), ítems o estrategias FODA (al menos uno), hallazgos PESTEL o «—», bloques del Canvas por su nombre exacto separados por punto y coma, e indicador igual al del brief.
4. Cada causa principal de 1.8 aparece en al menos una fila.
5. **Lectura de la matriz.** Dos frases: qué atiende cada objetivo y cómo se medirá con los KPI del capítulo 2.

## Formato

```markdown
## 1.10. Objetivos específicos

[Frase que presenta los objetivos específicos.]

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | [del brief] | [del brief] | [del brief] | [del brief] | OG-01 | [del brief] |

**Matriz de articulación.** [Frase que explica cómo se lee la matriz.]

| Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador |
|---|---|---|---|---|---|
| OE-01 | CAU-nn | DEB-nn, DO-nn | TEC-nn o — | [bloque]; [bloque] | [indicador del brief] |

**Lectura de la matriz.** [Qué atiende cada objetivo y cómo se medirá.]
```

## Ejemplo

```markdown
## 1.10. Objetivos específicos

Los objetivos específicos desagregan el objetivo general en resultados medibles al cierre del proyecto.

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | Integrar las ventas, costos y comisiones en un modelo estrella depurado | Registros que pasan las reglas de calidad | 98 % o más | Entrega (30-11-2026) | OG-01 | Calidad de datos del ETL |
| OE-02 | Medir la rentabilidad real de cada canal de venta | Canales con margen calculado | 5 de 5 canales | Entrega (30-11-2026) | OG-01 | Margen neto por canal |
| OE-03 | Identificar los turnos con mayor merma de pollo | Turnos con merma medida | 100 % de los turnos del periodo | Entrega (30-11-2026) | OG-01 | Porcentaje de merma por turno |

**Matriz de articulación.** Cada objetivo específico responde a causas del diagrama de Ishikawa, se apoya en el análisis FODA y PESTEL y actúa sobre bloques concretos del modelo de negocio.

| Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador |
|---|---|---|---|---|---|
| OE-01 | CAU-03, CAU-05, CAU-06 | DEB-03, DO-01 | TEC-01, LEG-01 | Actividades clave; Canales | Calidad de datos del ETL |
| OE-02 | CAU-01, CAU-04 | DEB-01, AME-02, FA-01, DA-01 | ECO-01, TEC-02 | Canales; Estructura de costos; Fuentes de ingresos | Margen neto por canal |
| OE-03 | CAU-02, CAU-07 | DEB-02, DO-02 | — | Actividades clave; Estructura de costos | Porcentaje de merma por turno |

**Lectura de la matriz.** El primer objetivo resuelve la falta de datos integrados, que es condición para los otros dos; el segundo ataca el precio único por canal y el costo del insumo, y el tercero la producción sin pronóstico. Cada uno se medirá con el indicador del brief, que el capítulo 2 convierte en un KPI del dashboard.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] La tabla de objetivos es idéntica a la sección 3.2 del brief vigente.
- [ ] Una fila de la matriz por `OE`, con códigos y bloques que existen en las corridas vigentes.
- [ ] Cada causa principal de 1.8 está atendida por algún objetivo.
- [ ] El indicador de cada fila es el del brief.
