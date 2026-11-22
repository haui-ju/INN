# Plantilla: Matriz FODA (`secciones/1.6.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.6.md` y la figura `foda` |
| **Punto** | 1.6. Matriz FODA |
| **Códigos** | `FOR-nn`, `DEB-nn`, `OPO-nn`, `AME-nn`; estrategias `FO-nn`, `FA-nn`, `DO-nn`, `DA-nn` |
| **Entradas** | Canvas y tamaño (1.3 y 1.4), PESTEL (1.5), brief (problemática y evidencia), `domain.md` (clientes y competencia) |
| **Salida** | los cuatro cuadros con evidencia y las estrategias cruzadas |

## Instrucciones para el agente
1. La primera línea es `## 1.6. Matriz FODA`.
2. Un párrafo que presenta la matriz con su cita (Gürel & Tat, 2017) y la marca `<!-- figura: foda -->` en una línea sola.
3. Cuatro tablas, en este orden: `Código | Fortaleza | Evidencia o fuente`, `Código | Debilidad | …`, `Código | Oportunidad | …` y `Código | Amenaza | …`. Referencia: de tres a cinco ítems por cuadro.
4. Fortalezas y debilidades citan en su evidencia un hecho interno (Canvas, registros de la empresa con su año). Oportunidades y amenazas citan el código PESTEL del que salen o una fuente con su año.
5. **Estrategias cruzadas.** Una frase y la tabla `Código | Tipo | Estrategia | Combina`, con al menos una estrategia FO, FA, DO y DA. El código lleva el tipo como prefijo; **Combina** lista los códigos de los dos cuadros que el tipo indica (FO: FOR y OPO; FA: FOR y AME; DO: DEB y OPO; DA: DEB y AME).
6. Después de escribir: `python3 .claude/skills/_shared/visuales.py construir --visual foda --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 1.6. Matriz FODA

[Párrafo que presenta la matriz, con su cita.]

<!-- figura: foda -->

Tabla 1: Fortalezas

| Código | Fortaleza | Evidencia o fuente |
|---|---|---|
| FOR-01 | [fortaleza] | [hecho interno] |

Tabla 2: Debilidades

| Código | Debilidad | Evidencia o fuente |
|---|---|---|
| DEB-01 | [debilidad] | [hecho interno] |

Tabla 3: Oportunidades

| Código | Oportunidad | Evidencia o fuente |
|---|---|---|
| OPO-01 | [oportunidad] | [código PESTEL o fuente con año] |

Tabla 4: Amenazas

| Código | Amenaza | Evidencia o fuente |
|---|---|---|
| AME-01 | [amenaza] | [código PESTEL o fuente con año] |

**Estrategias cruzadas.** [Una frase que presenta el cruce.]

Tabla 5: Estrategias cruzadas FO, FA, DO y DA

| Código | Tipo | Estrategia | Combina |
|---|---|---|---|
| FO-01 | FO | [estrategia] | FOR-01, OPO-01 |
| FA-01 | FA | [estrategia] | FOR-01, AME-01 |
| DO-01 | DO | [estrategia] | DEB-01, OPO-01 |
| DA-01 | DA | [estrategia] | DEB-01, AME-01 |
```

## Ejemplo

```markdown
## 1.6. Matriz FODA

La matriz FODA organiza en cuatro cuadros los factores internos y externos que favorecen o dificultan el logro de los objetivos de la organización (Gürel & Tat, 2017). Los factores internos salen del modelo de negocio y de los registros de la pollería; los externos, del análisis PESTEL.

<!-- figura: foda -->

Tabla 1: Fortalezas

| Código | Fortaleza | Evidencia o fuente |
|---|---|---|
| FOR-01 | Producto reconocido en el distrito por su sabor casero | Clientes frecuentes y reseñas en las aplicaciones, 2026 |
| FOR-02 | Dos locales con hornos propios y reparto con motorizados propios | Recursos clave del Canvas |
| FOR-03 | Ventas en crecimiento: 18 % más en el último año | Registro de caja de 2025 y 2026 |

Tabla 2: Debilidades

| Código | Debilidad | Evidencia o fuente |
|---|---|---|
| DEB-01 | Precios iguales en todos los canales, sin considerar la comisión | Lista de precios única de la empresa, 2026 |
| DEB-02 | Producción por turno decidida por experiencia, con una merma de 7 % | Control de producción de cocina, 2026 |
| DEB-03 | Ventas de caja, aplicaciones y WhatsApp registradas en sistemas que no se cruzan | Revisión de las fuentes de datos de la empresa, 2026 |

Tabla 3: Oportunidades

| Código | Oportunidad | Evidencia o fuente |
|---|---|---|
| OPO-01 | Herramientas de BI de bajo costo para integrar y analizar los datos | TEC-01 |
| OPO-02 | Más pedidos de delivery en el distrito | SOC-01 |
| OPO-03 | Inflación controlada que permite planificar precios y compras | ECO-02 |

Tabla 4: Amenazas

| Código | Amenaza | Evidencia o fuente |
|---|---|---|
| AME-01 | Precio del pollo vivo volátil | ECO-01 |
| AME-02 | Comisiones de 25 % a 30 % de las aplicaciones de delivery | TEC-02 |
| AME-03 | Normas de envases y de datos personales que elevan costos y exigencias | AMB-01, LEG-01 |
| AME-04 | Cadenas de pollerías con promociones frecuentes en las aplicaciones | Revisión de las aplicaciones de delivery, 2026 |

**Estrategias cruzadas.** Del cruce de los cuadros internos con los externos salen las estrategias que orientan el proyecto; las que dependen de medir, integrar o pronosticar con datos son las que la solución de BI hace posibles.

Tabla 5: Estrategias cruzadas FO, FA, DO y DA

| Código | Tipo | Estrategia | Combina |
|---|---|---|---|
| FO-01 | FO | Usar un dashboard de BI para identificar los canales y productos que más dejan y reforzar en ellos la marca | FOR-01, OPO-01 |
| FO-02 | FO | Impulsar el delivery propio por WhatsApp con los motorizados propios para captar la demanda que crece | FOR-02, OPO-02 |
| FA-01 | FA | Fijar precios diferenciados en las aplicaciones apoyados en el reconocimiento de la marca | FOR-01, AME-02 |
| DO-01 | DO | Integrar caja, aplicaciones y WhatsApp en un modelo de datos con herramientas de BI de bajo costo | DEB-03, OPO-01 |
| DO-02 | DO | Planificar la producción por turno con la demanda histórica | DEB-02, OPO-01 |
| DA-01 | DA | Monitorear el precio del pollo vivo y su efecto en el margen para ajustar precios y compras | DEB-01, AME-01 |
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: foda -->`.
- [ ] Cuatro cuadros con código y evidencia; oportunidades y amenazas citan el PESTEL o una fuente con año.
- [ ] Al menos una estrategia FO, FA, DO y DA, y cada una combina los cuadros de su tipo.
- [ ] Ningún código se repite ni cita un ítem que no existe.
- [ ] La cita de Gürel y Tat (2017) está en `referencias.md`.
