# Plantilla: Componentes

| | |
|---|---|
| **Entregable** | Sección «Componentes» de `DESIGN.md` |
| **Entradas** | `tokens.json`, guía (sección 4) |
| **Salida** | Seis componentes mínimos con estados, tokens y regla de uso |

## Instrucciones para el agente

1. Documenta como mínimo: **Encabezado, Tarjeta, Tabla, Etiqueta de estado, Barra de progreso y Botón**.
2. Cada componente es una subsección `### [Nombre]` con tres líneas: **Estados:**, **Tokens:** y **Uso:**.
3. Los tokens se citan con su ruta entre comillas invertidas (`color.claro.superficie`) y deben existir en `tokens.json`.
4. Si el usuario necesita otro componente, agrégalo con el mismo formato.
5. El ejemplo de cada componente usa contenido neutro del proyecto, sin etiquetas de procedencia.

## Formato

```markdown
### [Nombre del componente]

- **Estados:** [lista de estados]
- **Tokens:** `color.claro.[...]`, `espacio.[...]`, `radio.[...]`
- **Uso:** [regla de una frase]
```

## Ejemplo

```markdown
### Botón

- **Estados:** normal, hover, foco, deshabilitado
- **Tokens:** `color.claro.acento`, `color.claro.acento-texto`, `radio.md`, `espacio.3`
- **Uso:** un botón principal por vista; los demás son secundarios con borde `color.claro.borde`.
```

## Checklist

- [ ] Están los seis componentes mínimos.
- [ ] Cada uno declara estados, tokens y uso.
- [ ] Todos los tokens citados existen.
