# Plantilla: Introducción de cada capítulo

| | |
|---|---|
| **Entregable** | Párrafo que abre cada capítulo de `informe.md` |
| **Punto** | Capítulos 1 a 5 del índice |
| **Códigos** | No define códigos |
| **Entradas** | La tabla de abajo y las secciones disponibles del capítulo |
| **Salida** | Una frase fija por capítulo más la lista de las secciones que se incluyen |

## Instrucciones para el agente

1. El armado (`report.py construir`) toma la frase del capítulo de la tabla y le agrega «Comprende …» con las secciones incluidas, con su número y su título del índice.
2. Un capítulo sin secciones disponibles no aparece, así que no lleva introducción.
3. Si cambias una frase, cámbiala aquí: el armado no redacta introducciones propias. Mantén una o dos frases, sin cifras (las cifras van en las secciones, con su fecha o su fuente).

## Introducciones

| Capítulo | Introducción |
|---|---|
| 1 | Este capítulo presenta a la empresa, su modelo de negocio y su entorno, y de ese diagnóstico deriva la problemática central y los objetivos que guían la solución de Inteligencia de Negocios. |
| 2 | Este capítulo describe la solución de Inteligencia de Negocios que responde a la problemática: su arquitectura, las herramientas, el modelo de datos y los indicadores con que se medirán los objetivos. |
| 3 | Este capítulo explica cómo se construyeron el proceso ETL y el dashboard en Power BI, y qué reglas de calidad aseguran que los datos sean confiables. |
| 4 | Este capítulo cuenta, con los datos del dashboard, qué está pasando en el negocio y qué decisiones conviene tomar. |
| 5 | Este capítulo cierra el informe con las conclusiones frente a cada objetivo, las recomendaciones para la empresa y las lecciones que deja el proyecto. |

## Formato

```markdown
# Capítulo [N]: [título del índice]

[frase de la tabla] Comprende [N.1 título], [N.2 título] y [N.3 título].
```

## Ejemplo

```markdown
# Capítulo 1: Diagnóstico estratégico y análisis del negocio

Este capítulo presenta a la empresa, su modelo de negocio y su entorno, y de ese diagnóstico deriva la problemática central y los objetivos que guían la solución de Inteligencia de Negocios. Comprende 1.1 Nombre de la empresa, 1.2 Misión y visión y 1.3 Industria y tamaño.
```

## Checklist

- [ ] Cada capítulo del informe abre con su frase y la lista de sus secciones incluidas.
- [ ] La lista no nombra secciones pendientes.
- [ ] Ningún capítulo sin secciones aparece en el informe.
