# Plantilla: Industria y tamaño (`secciones/1.3.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.3.md` |
| **Punto** | 1.3. Industria y tamaño |
| **Entradas** | `domain.md` (industria, tamaño, clientes y competencia), config (`rubro`), UIT del año (decreto supremo del MEF) |
| **Salida** | sector, actividad, tipo de cliente, entorno competitivo y categoría de tamaño según la Ley 30056 |

## Instrucciones para el agente
1. La primera línea es `## 1.3. Industria y tamaño`.
2. Un párrafo que sitúa a la empresa en su industria.
3. Tabla `Aspecto | Descripción` con **Sector, Actividad económica (CIIU), Tipo de cliente y Entorno competitivo** (competidores directos e indirectos, por tipo).
4. **Tamaño de la organización.** Un párrafo con el cálculo y la categoría, citando la Ley 30056, y la tabla `Dato | Valor` con **Ventas anuales, UIT de referencia, Ventas en UIT, Trabajadores (opcional) y Categoría (Ley 30056)**.
5. Ventas en UIT = ventas anuales ÷ UIT, redondeado. Categoría: hasta 150 UIT, Microempresa; hasta 1700, Pequeña empresa; hasta 2300, Mediana empresa; más, Gran empresa (guía, sección 3).
6. Montos con espacio de miles (`S/ 2 400 000`) y el año entre paréntesis. Si no hay ventas, «Pendiente» en ventas y en ventas en UIT, y la categoría con su fuente.

## Formato

```markdown
## 1.3. Industria y tamaño

[Párrafo que sitúa a la empresa en su industria.]

| Aspecto | Descripción |
|---|---|
| Sector | [sector] |
| Actividad económica (CIIU) | [código: descripción] |
| Tipo de cliente | [quién compra, cómo y cuándo] |
| Entorno competitivo | [competidores directos e indirectos] |

**Tamaño de la organización.** [Cálculo en UIT y categoría según la Ley 30056, con cita.]

| Dato | Valor |
|---|---|
| Ventas anuales | S/ [monto] ([año]) |
| UIT de referencia | S/ [UIT] ([año]) |
| Ventas en UIT | [ventas ÷ UIT] |
| Trabajadores | [número] |
| Categoría (Ley 30056) | [Microempresa, Pequeña empresa, Mediana empresa o Gran empresa] |
```

## Ejemplo

```markdown
## 1.3. Industria y tamaño

Pollería Don Tito pertenece a la industria de restaurantes, dentro del sector de servicios de comidas y bebidas. Compite en un mercado de alta rotación, sensible al precio y con fuerte presencia de las aplicaciones de delivery.

| Aspecto | Descripción |
|---|---|
| Sector | Servicios de comidas y bebidas (restaurantes) |
| Actividad económica (CIIU) | 5610: actividades de restaurantes y de servicio móvil de comidas |
| Tipo de cliente | Familias y trabajadores de San Juan de Lurigancho que compran en el local, para llevar o por delivery, sobre todo en almuerzos y fines de semana |
| Entorno competitivo | Cadenas de pollerías con presencia nacional, pollerías independientes del distrito y otras comidas rápidas en las aplicaciones de delivery |

**Tamaño de la organización.** Con ventas anuales de S/ 2 400 000, equivalentes a unas 436 UIT, la empresa es una pequeña empresa según el artículo 5 de la Ley 30056, que ubica en esa categoría a las ventas anuales superiores a 150 UIT y hasta 1700 UIT (Congreso de la República del Perú, 2013). Cuenta con 22 trabajadores entre cocina, salón, caja, reparto y administración.

| Dato | Valor |
|---|---|
| Ventas anuales | S/ 2 400 000 (2025) |
| UIT de referencia | S/ 5 500 (2026) |
| Ventas en UIT | 436 |
| Trabajadores | 22 |
| Categoría (Ley 30056) | Pequeña empresa |
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Los cuatro aspectos de la industria están descritos.
- [ ] Ventas en UIT = ventas ÷ UIT (± 1) y la categoría corresponde a la Ley 30056.
- [ ] La UIT es la del año indicado y la ley está citada en `referencias.md`.
