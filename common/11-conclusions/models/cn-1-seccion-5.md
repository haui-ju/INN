# Plantilla: Conclusiones, recomendaciones y lecciones aprendidas (`secciones/5.md`)

| | |
|---|---|
| **Entregable** | `secciones/5.md` |
| **Punto** | 5. Conclusiones, recomendaciones y lecciones aprendidas |
| **Códigos** | `CNC-nn`, `REC-nn` y `LEC-nn`; cita `OG-nn`, `OE-nn` y `KPI-nn` |
| **Entradas** | el brief (objetivos y usuarios), `modelo.json` (KPI con su meta), `valores.json` de la corrida vigente de `09-make-dashboard` y, si existe, la sección 4 |
| **Salida** | una conclusión por objetivo con su estado calculado, su respaldo en cifras, recomendaciones accionables y lecciones del proceso |

## Instrucciones para el agente
1. La primera línea es `## 5. Conclusiones, recomendaciones y lecciones aprendidas`. Escribe esta sección **solo con los valores reales de `valores.json`**; sin ellos, detente.
2. Un párrafo que dice qué se contrasta: el valor real de cada indicador (punto 3.2) frente a su meta (punto 2.5) y el objetivo que mide (punto 1.10).
3. **Conclusiones.** Tabla `Código | Objetivo | Estado | Conclusión`. Una fila `CNC-nn` por cada `OE-nn` del brief y una por el `OG-nn`. En `Objetivo` va solo el código. El `Estado` **no se opina: se calcula** con `python3 .claude/skills/_shared/rules/conclusions.py estados` (regla de la guía, punto 1) y es `Cumplido`, `Parcial`, `No cumplido` o `Sin meta`. La conclusión explica qué mostró el indicador y por qué, en una o dos frases; la del objetivo general cita las conclusiones `CNC-nn` de los objetivos específicos.
4. **Respaldo.** Tabla `Conclusión | KPI | Valor real | Meta | Estado del KPI`. Una fila por cada KPI de cada objetivo específico (los de `modelo.json` con ese `OE-nn`). El valor es el de `valores.json`, con sus decimales; la meta se copia tal cual de 2.5; el estado del KPI es `Cumple`, `No cumple` o `Sin meta`.
5. **Metas pendientes.** Si un KPI no tiene meta, la conclusión de su objetivo **dice que no se puede concluir su cumplimiento** porque la meta está pendiente y no la inventa.
6. **Recomendaciones.** Tabla `Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará`. Una fila `REC-nn` por recomendación, ligada a una `CNC-nn`. Toda conclusión que no sea `Cumplido` tiene al menos una. Quién decide es un usuario del brief; el KPI es uno de `modelo.json`.
7. **Lecciones aprendidas.** Tabla `Código | Lección | Dónde se vio`: al menos una `LEC-nn` sobre el proceso (calidad de datos, herramienta, trabajo en equipo), con el punto del informe donde se vio.
8. **Limitaciones.** Un párrafo `**Limitaciones.**`. Con `modo_datos: generado`, dice que los datos se generaron para el proyecto y que los resultados dependen de esa calibración.
9. Cada tabla lleva antes una línea `Tabla N: título`. Sin comentarios ni notas: solo texto final.

## Formato

```markdown
## 5. Conclusiones, recomendaciones y lecciones aprendidas

[Párrafo: qué se contrasta y de dónde salen los valores.]

**Conclusiones.** [Frase que presenta la tabla.]

Tabla 1: Conclusiones por objetivo

| Código | Objetivo | Estado | Conclusión |
|---|---|---|---|
| CNC-01 | [OE-nn] | [Cumplido, Parcial, No cumplido o Sin meta] | [Qué mostró el indicador y por qué.] |
| CNC-nn | [OG-nn] | [Estado calculado] | [Conclusión que cita las CNC-nn de los OE.] |

**Respaldo.** [Frase que presenta la tabla.]

Tabla 2: Respaldo de las conclusiones

| Conclusión | KPI | Valor real | Meta | Estado del KPI |
|---|---|---|---|---|
| CNC-01 | [KPI-nn] | [valor] | [meta de 2.5] | [Cumple, No cumple o Sin meta] |

**Recomendaciones.** [Frase que presenta la tabla.]

Tabla 3: Recomendaciones

| Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará |
|---|---|---|---|---|
| REC-01 | [CNC-nn] | [Acción concreta.] | [Usuario del brief] | [KPI-nn] |

**Lecciones aprendidas.** [Frase que presenta la tabla.]

Tabla 4: Lecciones aprendidas

| Código | Lección | Dónde se vio |
|---|---|---|
| LEC-01 | [Lección del proceso.] | [Punto del informe] |

**Limitaciones.** [Párrafo: datos generados para el proyecto y su efecto en los resultados.]
```

## Ejemplo

```markdown
## 5. Conclusiones, recomendaciones y lecciones aprendidas

Este capítulo contrasta lo que midió el dashboard con los objetivos del proyecto. Cada conclusión compara el valor real de su indicador, registrado en el punto 3.2, con la meta fijada en el punto 2.5 para el objetivo que mide en el punto 1.10.

**Conclusiones.** Cada objetivo tiene una conclusión con un estado calculado a partir de sus indicadores.

Tabla 1: Conclusiones por objetivo

| Código | Objetivo | Estado | Conclusión |
|---|---|---|---|
| CNC-01 | OE-01 | No cumplido | La calidad de datos del ETL quedó en 97.2 %, por debajo de la meta de 98 %: parte de los registros sin cantidad o con el nombre del producto distinto llegó al modelo sin tratarse. |
| CNC-02 | OE-02 | Parcial | La participación del canal directo cumplió su meta, pero el margen neto global quedó en 8.4 % frente al 12 % esperado. El precio del pollo vivo sigue con la meta pendiente, por lo que no se puede concluir su cumplimiento. |
| CNC-03 | OE-03 | No cumplido | La merma por turno fue de 6.9 %, más del doble de la meta de 3 %: la producción de cada turno todavía no sigue una referencia de datos. |
| CNC-04 | OG-01 | Parcial | Con CNC-01, CNC-02 y CNC-03 el objetivo general se cumplió solo en parte: el dashboard ya muestra la rentabilidad por canal y la merma, pero los indicadores todavía no alcanzan sus metas. |

**Respaldo.** La tabla repite, por cada objetivo específico, el valor real y la meta de cada indicador que lo mide.

Tabla 2: Respaldo de las conclusiones

| Conclusión | KPI | Valor real | Meta | Estado del KPI |
|---|---|---|---|---|
| CNC-01 | KPI-01 | 97.2 % | 98 % o más | No cumple |
| CNC-02 | KPI-02 | 8.4 % | 12 % o más en el margen neto global | No cumple |
| CNC-02 | KPI-04 | 71.0 % | 70 % o más | Cumple |
| CNC-02 | KPI-05 | S/ 6.55 | Pendiente | Sin meta |
| CNC-03 | KPI-03 | 6.9 % | 3 % o menos | No cumple |

**Recomendaciones.** Cada recomendación nombra quién decide y el indicador que mostrará si funcionó.

Tabla 3: Recomendaciones

| Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará |
|---|---|---|---|---|
| REC-01 | CNC-01 | Revisar las reglas de calidad del ETL con los registros descartados de cada carga y volver a medir. | Gerente general | KPI-01 |
| REC-02 | CNC-02 | Ajustar el precio de los combos en las aplicaciones de delivery para compensar la comisión. | Gerente general | KPI-02 |
| REC-03 | CNC-02 | Fijar la meta del precio del pollo vivo con la serie completa de precios. | Gerente general | KPI-05 |
| REC-04 | CNC-03 | Definir cuántos pollos hornear por turno y día de la semana a partir de lo vendido. | Jefe de cocina | KPI-03 |
| REC-05 | CNC-04 | Repetir la medición con los datos propios de la empresa antes de decidir cambios de precio. | Gerente general | KPI-02 |

**Lecciones aprendidas.** El proceso dejó tres aprendizajes.

Tabla 4: Lecciones aprendidas

| Código | Lección | Dónde se vio |
|---|---|---|
| LEC-01 | La calidad de los datos se mide desde la carga y no al final: cada regla de limpieza necesita su conteo de filas antes y después. | Punto 3.1 |
| LEC-02 | Una meta pendiente impide concluir un objetivo: conviene fijarla antes de construir el dashboard. | Punto 2.5 |

**Limitaciones.** Los datos se generaron para el proyecto y se calibraron con las cifras del informe, por lo que los resultados dependen de esa calibración y no describen a una empresa real.
```

## Checklist
- [ ] Una conclusión `CNC-nn` por cada `OE-nn` del brief y una por el `OG-nn`.
- [ ] El estado de cada conclusión es el calculado, y la tabla de respaldo tiene una fila por KPI de cada objetivo específico.
- [ ] Los valores y las metas de la tabla de respaldo son los de `valores.json` y 2.5.
- [ ] Si un KPI no tiene meta, su conclusión lo dice y no concluye el cumplimiento.
- [ ] Toda conclusión que no es `Cumplido` tiene una recomendación, con un usuario del brief y un KPI del modelo.
- [ ] Hay al menos una lección y el párrafo de limitaciones (datos generados).
