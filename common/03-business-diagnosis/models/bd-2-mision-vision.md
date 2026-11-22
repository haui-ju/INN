# Plantilla: Misión y visión (`secciones/1.2.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.2.md` |
| **Punto** | 1.2. Misión y visión |
| **Entradas** | `domain.md` (misión, visión, valores), brief (tema y problemática) |
| **Salida** | misión, visión y valores de la empresa, y su relación con el proyecto de BI |

## Instrucciones para el agente
1. La primera línea es `## 1.2. Misión y visión`.
2. **Misión.** y **Visión.** se copian de `domain.md` sin el marcador (el validador compara el texto). Si `domain.md` no las tiene, propón una redacción, confírmala con el usuario y escríbela primero en `domain.md`.
3. **Valores.** Lista corta (opcional), de `domain.md`.
4. **Relación con el proyecto.** Dos o tres frases: qué parte de la misión o la visión exige decidir con datos y cómo la solución de BI responde a esa brecha.

## Formato

```markdown
## 1.2. Misión y visión

**Misión.** [misión de domain.md]

**Visión.** [visión de domain.md]

**Valores.**
- [valor]

**Relación con el proyecto.** [qué exige decidir con datos y cómo responde la solución de BI]
```

## Ejemplo

```markdown
## 1.2. Misión y visión

**Misión.** Servir el mejor pollo a la brasa de San Juan de Lurigancho, con sabor casero, atención rápida y precios justos para las familias del distrito, en el local o en su casa.

**Visión.** Al 2029, ser la pollería de referencia de Lima Este, con cuatro locales y una operación rentable guiada por datos.

**Valores.**
- Sabor casero y constante.
- Atención rápida y amable.
- Precios justos.

**Relación con el proyecto.** La visión pide una operación rentable guiada por datos, pero hoy la empresa decide precios y producción sin ver el margen por canal ni la merma. La solución de BI responde a esa brecha: sin rentabilidad medida, crecer a cuatro locales multiplicaría el problema.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Misión y visión iguales a `domain.md`, sin el marcador.
- [ ] La relación con el proyecto conecta la visión con la problemática del brief.
