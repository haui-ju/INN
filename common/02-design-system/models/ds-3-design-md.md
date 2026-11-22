# Plantilla: DESIGN.md

| | |
|---|---|
| **Entregable** | `DESIGN.md` |
| **Entradas** | `tokens.json` confirmado, brief, componentes |
| **Salida** | Documento del sistema de diseño que el config referencia en `diseno` |

## Instrucciones para el agente

1. Copia la estructura de abajo; no cambies los títulos de nivel 2 (otras skills los leen).
2. Las tablas de color, tipografía y espacio **repiten** los valores de `tokens.json`; no inventes valores nuevos.
3. Cada token citado lleva su ruta completa entre comillas invertidas.
4. Termina con «Cómo usarlo» para que otras skills sepan leer `tokens.json`.
5. Referencia WCAG con el formato APA 7 de la guía, máximo una vez.

## Formato

```markdown
# Sistema de diseño · [nombre del proyecto]

## Principios
[cálido, editorial y profesional: qué implican en este proyecto]

## Color
| Token | Claro | Oscuro | Uso |
|---|---|---|---|

## Tipografía
[familia, escala, pesos, interlineado]

## Espacio, radio y sombra
[tablas de valores]

## Componentes
[subsecciones ### según la plantilla ds-2]

## Tema claro y oscuro
[cómo se alterna y qué cambia]

## Accesibilidad
[contraste AA, pares validados, estados no solo por color]

## Cómo usarlo
Leer `diseno` en `project/config.yaml`; leer `tokens.json` de esa carpeta; usar variables `--c-*`, `--espacio-*`, `--radio-*`.
```

## Ejemplo

Ver `.claude/skills/02-design-system/references/design-base.md`.

## Checklist

- [ ] Están las ocho secciones de nivel 2, en este orden.
- [ ] Las tablas coinciden con `tokens.json`.
- [ ] Los seis componentes mínimos están documentados con estados.
- [ ] No hay etiquetas de procedencia fuera de `README.md`.
