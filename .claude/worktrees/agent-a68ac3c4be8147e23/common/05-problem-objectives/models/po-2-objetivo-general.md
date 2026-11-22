# Plantilla: Objetivo general del proyecto (`secciones/1.9.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.9.md` |
| **Punto** | 1.9. Objetivo general del proyecto |
| **Códigos** | `OG-01` (del brief) |
| **Entradas** | brief vigente, sección 3.1 |
| **Salida** | el objetivo general, copiado del brief, con su métrica, meta, plazo e indicador |

## Instrucciones para el agente
1. La primera línea es `## 1.9. Objetivo general del proyecto`.
2. Una frase que vincula el objetivo con la problemática de 1.8.
3. La tabla `Código | Objetivo | Métrica | Meta | Plazo | Indicador` **copiada sin cambios** de la sección 3.1 del brief.
4. Si el usuario quiere cambiar el objetivo, indícale `01-make-project-brief-update`; aquí no se edita.

## Formato

```markdown
## 1.9. Objetivo general del proyecto

[Frase que vincula el objetivo con la problemática.]

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | [del brief] | [del brief] | [del brief] | [del brief] | [del brief] |
```

## Ejemplo

```markdown
## 1.9. Objetivo general del proyecto

El objetivo general responde a la problemática central: dar a la gerencia la información de rentabilidad por canal y de merma que hoy no tiene para decidir precios y producción.

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | Diseñar e implementar una solución de BI que muestre la rentabilidad por canal y la merma para apoyar las decisiones de la gerencia | Decisiones de precio y producción respaldadas por el dashboard | 3 decisiones documentadas | Entrega (30-11-2026) | Margen neto por canal |
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] La fila de `OG-01` es idéntica a la del brief vigente.
