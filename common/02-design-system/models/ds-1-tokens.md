# Plantilla: Tokens

| | |
|---|---|
| **Entregable** | `tokens.json` (fuente única) y su tabla en `DESIGN.md` |
| **Entradas** | Brief confirmado, `references/tokens-base.json` de la skill |
| **Salida** | `tokens.json` válido, claro y oscuro completos, pares con contraste AA |

## Instrucciones para el agente

1. Parte de `references/tokens-base.json` y cambia solo lo que el brief pide (acento, tipografía, radios).
2. Mantén **las mismas claves** en `color.claro` y `color.oscuro` (guía, 1.1).
3. Declara en `pares` las combinaciones a validar. Cada par usa claves que existen y un `tipo`: `normal` (4,5:1), `grande` (3:1) o `interfaz` (3:1).
4. Si cambias un color, recalcula el contraste de sus pares en ambos temas antes de proponerlo; si no cumple AA, ajusta la luminosidad hasta que cumpla.
5. El tema oscuro no es el claro invertido (guía, 1.2).

## Formato

```json
{
  "schema": 1,
  "color": {
    "claro":  {"fondo": "#...", "superficie": "#...", "texto": "#...", "texto-secundario": "#...", "borde": "#...", "acento": "#...", "acento-texto": "#...", "exito": "#...", "alerta": "#...", "error": "#..."},
    "oscuro": {"...": "mismas claves que claro"}
  },
  "pares": [{"texto": "texto", "fondo": "fondo", "tipo": "normal"}],
  "tipografia": {"familia": "...", "familia-mono": "...", "escala": {"xs": "...", "sm": "...", "base": "...", "lg": "...", "xl": "...", "2xl": "..."}, "peso": {"normal": 400, "medio": 500, "fuerte": 600}, "interlineado": {"compacto": 1.25, "normal": 1.5}},
  "espacio": {"1": "4px", "2": "8px", "3": "12px", "4": "16px", "6": "24px", "8": "32px"},
  "radio": {"sm": "...", "md": "...", "lg": "..."},
  "sombra": {"sm": "...", "md": "..."}
}
```

## Ejemplo (fragmento)

```json
{
  "color": {
    "claro": {"fondo": "#FAF9F5", "superficie": "#FFFFFF", "texto": "#141413", "acento": "#D4704F", "acento-texto": "#1F1B16", "acento-fuerte": "#B1472A"}
  },
  "pares": [
    {"texto": "texto", "fondo": "fondo", "tipo": "normal"},
    {"texto": "acento-texto", "fondo": "acento", "tipo": "normal"}
  ]
}
```

## Checklist

- [ ] Claro y oscuro tienen las mismas claves.
- [ ] Cada par existe en ambos temas y cumple su contraste mínimo.
- [ ] Hay un solo acento y los colores de estado solo se usan para estados.
- [ ] Las tres familias (`familia-titulos`, `familia`, `familia-mono`) terminan en fuentes del sistema.
- [ ] `acento-fuerte` cumple AA como texto sobre `fondo` y `superficie`, y `acento-texto` sobre `acento`.
