# Plantilla: Especificación y capturas del dashboard (`anexos/D.md`)

| | |
|---|---|
| **Entregable** | `anexos/D.md` (anexo D del informe) |
| **Punto** | Anexo D: Especificación y capturas del dashboard (una captura por página con su descripción) |
| **Códigos** | `PAG-nn` |
| **Entradas** | la tabla de páginas de 3.2 y las capturas `capturas/pag-nn.png` que entrega el equipo |
| **Salida** | la especificación de cada página con su descripción, que acompaña a su captura de la sección 3.2 |

## Instrucciones para el agente
1. La primera línea es `# Anexo D: Especificación y capturas del dashboard`.
2. Un párrafo corto: cuántas páginas hay y que cada captura está en la sección 3.2.
3. Para cada página de 3.2, un encabezado `### PAG-nn. Nombre de la página` y debajo `**Descripción.**` con qué muestra, cómo se lee y qué decisión apoya; luego las viñetas `**Visuales.**` con el tipo de visual y lo que muestra, y una línea `**Filtros.**`.
4. **No repitas la marca `<!-- captura: … -->`**: las capturas se marcan en 3.2 y la descripción remite a ellas con «la captura de esta página está en la sección 3.2». Así cada imagen entra una sola vez al informe.
5. Cada página de 3.2 tiene su descripción y no hay páginas que 3.2 no tenga. Si hay tablas, cada una lleva antes una línea `Tabla N: título`.

## Formato

```markdown
# Anexo D: Especificación y capturas del dashboard

[Párrafo: cuántas páginas tiene y dónde están las capturas.]

### PAG-01. [Nombre de la página]

**Descripción.** [Qué muestra la página, cómo se lee y qué decisión apoya. La captura de esta página está en la sección 3.2.]

**Visuales.**
- [Tipo de visual]: [qué muestra].

**Filtros.** [Filtros de la página.]
```

## Ejemplo

```markdown
# Anexo D: Especificación y capturas del dashboard

El dashboard tiene cuatro páginas. Cada una se describe aquí con sus visuales y sus filtros; la captura de cada página está en la sección 3.2.

### PAG-01. Calidad de datos

**Descripción.** Muestra qué parte de los registros cargados pasó las reglas de calidad y de qué canal vienen los que no. Se lee primero: si el porcentaje de registros válidos cae, las demás páginas no deben usarse para decidir. La captura de esta página está en la sección 3.2.

**Visuales.**
- Tarjeta: porcentaje de registros válidos frente a su meta.
- Barras: registros cargados por canal.

**Filtros.** Mes y canal.

### PAG-02. Margen por canal

**Descripción.** Compara el margen neto de cada canal después de la comisión y la participación del canal directo en las ventas. Apoya la decisión de ajustar el precio de los combos en las aplicaciones de delivery. La captura de esta página está en la sección 3.2.

**Visuales.**
- Tarjetas: margen neto y participación del canal directo.
- Barras: margen neto por canal.

**Filtros.** Mes, canal y local.

### PAG-03. Producción y merma

**Descripción.** Muestra cuántos pollos de lo preparado se pierden en cada turno y día de la semana. Apoya la decisión de cuántos pollos hornear. La captura de esta página está en la sección 3.2.

**Visuales.**
- Tarjeta: porcentaje de merma frente a su meta.
- Columnas: merma por turno y día de la semana.

**Filtros.** Mes, turno y local.

### PAG-04. Precio del pollo vivo

**Descripción.** Sigue el precio por kilogramo del pollo vivo semana a semana. Apoya la decisión de anticipar compras ante una subida. La captura de esta página está en la sección 3.2.

**Visuales.**
- Tarjeta: precio promedio por kilogramo.
- Línea: precio por semana.

**Filtros.** Mes.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Cada página de 3.2 tiene su `### PAG-nn.` con su `**Descripción.**`.
- [ ] No hay marcas `<!-- captura: … -->` en el anexo.
- [ ] No describe páginas que 3.2 no tiene.
