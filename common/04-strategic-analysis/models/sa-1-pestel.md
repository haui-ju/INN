# Plantilla: Análisis PESTEL (`secciones/1.5.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.5.md` y la figura `pestel` |
| **Punto** | 1.5. Análisis PESTEL |
| **Códigos** | `POL-nn`, `ECO-nn`, `SOC-nn`, `TEC-nn`, `AMB-nn`, `LEG-nn` |
| **Entradas** | brief (tema, problemática, fuentes), diagnóstico del negocio (industria, Canvas), fuentes externas verificadas |
| **Salida** | hallazgos del entorno por factor, con su efecto en el negocio, su tipo y su fuente |

## Instrucciones para el agente
1. La primera línea es `## 1.5. Análisis PESTEL`.
2. Un párrafo que presenta el análisis con su cita (Aguilar, 1967) y la marca `<!-- figura: pestel -->` en una línea sola.
3. Tabla `Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente`, ordenada por factor (Político, Económico, Social, Tecnológico, Ecológico, Legal). El prefijo del código corresponde al factor (`AMB` es el ecológico).
4. Al menos un hallazgo por factor. El **efecto** dice qué le pasa a esta empresa; el **tipo** es Oportunidad o Amenaza; la **fuente** lleva autor o institución y año (o una fuente interna con su año). Cada fuente externa va a `referencias.md`.
5. Busca y verifica cada cifra externa antes de escribirla; si no la encuentras, reformula el hallazgo sin cifra.
6. **Síntesis.** Dos frases: qué factores pesan más y qué se traslada al FODA.
7. Después de escribir: `python3 .claude/skills/_shared/visuales.py construir --visual pestel --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 1.5. Análisis PESTEL

[Párrafo que presenta el análisis, con su cita.]

<!-- figura: pestel -->

Tabla 1: Análisis PESTEL

| Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente |
|---|---|---|---|---|---|
| POL-01 | Político | [hecho del entorno] | [qué le pasa a la empresa] | Oportunidad o Amenaza | [Autor o institución (año)] |

**Síntesis.** [Qué factores pesan más y qué pasa al FODA.]
```

## Ejemplo

```markdown
## 1.5. Análisis PESTEL

El análisis PESTEL examina los factores políticos, económicos, sociales, tecnológicos, ecológicos y legales del entorno que la empresa no controla pero que condicionan sus resultados (Aguilar, 1967). Para Pollería Don Tito se identificaron los siguientes hallazgos, cada uno con su efecto en el negocio.

<!-- figura: pestel -->

Tabla 1: Análisis PESTEL

| Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente |
|---|---|---|---|---|---|
| POL-01 | Político | La Ley 30056 promueve a la micro y pequeña empresa con un régimen tributario y laboral simplificado | La pollería mantiene costos laborales y tributarios acordes con su tamaño | Oportunidad | Congreso de la República del Perú (2013) |
| ECO-01 | Económico | El precio del pollo vivo en Lima Metropolitana varía de una semana a otra | El costo del insumo principal cambia sin que la pollería ajuste sus precios | Amenaza | MIDAGRI (2026) |
| ECO-02 | Económico | La inflación de Lima Metropolitana se mantiene dentro del rango meta del banco central, de 1 % a 3 % | Permite planificar precios y compras con menos incertidumbre | Oportunidad | BCRP (2026) |
| SOC-01 | Social | Los clientes del distrito piden cada vez más comida por aplicaciones y por WhatsApp | Crece la demanda de delivery, que ya es el 35 % de las ventas | Oportunidad | Registro de ventas por canal de la empresa, 2026 |
| TEC-01 | Tecnológico | Power BI Desktop es de uso gratuito y permite integrar y visualizar datos de varias fuentes | La empresa puede construir su dashboard sin invertir en licencias de escritorio | Oportunidad | Microsoft (2026) |
| TEC-02 | Tecnológico | Las aplicaciones de delivery concentran los pedidos en línea y cobran comisiones de 25 % a 30 % | Cada venta por aplicación deja menos margen que una venta en salón | Amenaza | Contratos de la empresa con Rappi y PedidosYa, 2026 |
| AMB-01 | Ecológico | La Ley 30884 regula el plástico de un solo uso y los envases descartables | Sube el costo de los envases para llevar y delivery | Amenaza | Congreso de la República del Perú (2018) |
| LEG-01 | Legal | La Ley 29733 exige consentimiento para tratar datos personales de los clientes | Los datos de clientes de WhatsApp deben anonimizarse en el modelo de datos | Amenaza | Congreso de la República del Perú (2011) |

**Síntesis.** El entorno económico y tecnológico es el que más pesa: el precio del pollo y las comisiones de las aplicaciones presionan el margen, mientras que la demanda de delivery y las herramientas de BI de bajo costo abren oportunidades. Estos hallazgos pasan al FODA como oportunidades y amenazas.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: pestel -->`.
- [ ] Los seis factores con al menos un hallazgo; el prefijo del código coincide con el factor.
- [ ] Cada hallazgo tiene efecto en la empresa, tipo y fuente con año.
- [ ] Las fuentes externas están en `referencias.md` y sus cifras se verificaron.
- [ ] Hay síntesis.
