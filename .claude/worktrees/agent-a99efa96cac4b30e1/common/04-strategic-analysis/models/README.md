# Plantillas del análisis estratégico

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, códigos, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea: `## 1.5. Análisis PESTEL`, `## 1.6. Matriz FODA` y `## 1.7. Diagrama de la problemática: Ishikawa`.
- **Columnas y rótulos exactos** (la validación y los visuales los leen): `Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente`; `Código | Fortaleza | Evidencia o fuente` (y Debilidad, Oportunidad, Amenaza); `Código | Tipo | Estrategia | Combina`; `Código | Categoría | Causa | Evidencia`; `**Síntesis.**`, `**Estrategias cruzadas.**`, `**Efecto.**` y `**Lectura del diagrama.**`.
- El ejemplo es el caso Pollería Don Tito, el mismo del brief y del diagnóstico del negocio de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [sa-1-pestel](sa-1-pestel.md) | `secciones/1.5.md` y la figura `pestel` |
| [sa-2-foda](sa-2-foda.md) | `secciones/1.6.md` y la figura `foda` |
| [sa-3-ishikawa](sa-3-ishikawa.md) | `secciones/1.7.md` y la figura `ishikawa` |

Orden de trabajo: PESTEL (el entorno) → FODA (lo interno con el Canvas y lo externo con el PESTEL) → Ishikawa (las causas del problema del brief, con la evidencia del FODA). Con la confirmación del plan se escriben las tres secciones, `referencias.md` y `README.md`; luego se construyen las tres figuras con `--run` y se valida.

## Archivos de la corrida

```
project/04-strategic-analysis/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/1.5.md, 1.6.md y 1.7.md
├── visuales/pestel.html, foda.html, ishikawa.html (y sus .json)
├── leer-imagen/pestel.md, foda.md, ishikawa.md
├── referencias.md
└── README.md
```

Ejemplo de `referencias.md` (una referencia por línea, APA 7, orden alfabético):

```markdown
Aguilar, F. J. (1967). *Scanning the business environment*. Macmillan.
Banco Central de Reserva del Perú. (2026). *Inflación de Lima Metropolitana* [Serie estadística]. BCRPData.
Congreso de la República del Perú. (2011, 3 de julio). Ley N.° 29733, Ley de protección de datos personales. *Diario Oficial El Peruano*.
Congreso de la República del Perú. (2013, 2 de julio). Ley N.° 30056, Ley que modifica diversas leyes para facilitar la inversión, impulsar el desarrollo productivo y el crecimiento empresarial. *Diario Oficial El Peruano*.
Congreso de la República del Perú. (2018, 19 de diciembre). Ley N.° 30884, Ley que regula el plástico de un solo uso y los recipientes o envases descartables. *Diario Oficial El Peruano*.
Gürel, E., & Tat, M. (2017). SWOT analysis: A theoretical review. *The Journal of International Social Research, 10*(51), 994-1006. https://doi.org/10.17719/jisr.2017.1832
Ishikawa, K. (1986). *Guide to quality control* (2.ª ed.). Asian Productivity Organization.
Microsoft. (2026). *Power BI Desktop* [Software].
Ministerio de Desarrollo Agrario y Riego. (2026). *Precios de pollo vivo en Lima Metropolitana* [Base de datos]. Sistema de Abastecimiento y Precios.
```
