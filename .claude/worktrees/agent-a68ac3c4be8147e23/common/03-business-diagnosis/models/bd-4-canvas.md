# Plantilla: Business Model Canvas (`secciones/1.4.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.4.md` y la figura `bmc` |
| **Punto** | 1.4. Modelo de negocio: Business Model Canvas |
| **Entradas** | `domain.md` (productos, clientes, competencia), brief (tema, problemática, usuarios y fuentes) |
| **Salida** | los nueve bloques del lienzo, su figura y la lectura del modelo frente a la problemática |

## Instrucciones para el agente
1. La primera línea es `## 1.4. Modelo de negocio: Business Model Canvas`.
2. Un párrafo que presenta el lienzo con su cita (Osterwalder & Pigneur, 2010).
3. La marca de figura en una línea sola: `<!-- figura: bmc -->`.
4. Tabla `Bloque | Contenido` con los nueve bloques **con estos nombres exactos y en este orden**: Segmentos de clientes, Propuesta de valor, Canales, Relaciones con clientes, Fuentes de ingresos, Recursos clave, Actividades clave, Socios clave y Estructura de costos. Los elementos se separan con punto y coma (de dos a cinco por bloque).
5. **Lectura del modelo.** Dos o tres frases que nombran los bloques donde aparece la problemática del brief.
6. Después de escribir: `python3 .claude/skills/_shared/visuales.py construir --visual bmc --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 1.4. Modelo de negocio: Business Model Canvas

[Párrafo que presenta el lienzo, con su cita.]

<!-- figura: bmc -->

| Bloque | Contenido |
|---|---|
| Segmentos de clientes | [elemento]; [elemento] |
| Propuesta de valor | [elemento]; [elemento] |
| Canales | [elemento]; [elemento] |
| Relaciones con clientes | [elemento]; [elemento] |
| Fuentes de ingresos | [elemento]; [elemento] |
| Recursos clave | [elemento]; [elemento] |
| Actividades clave | [elemento]; [elemento] |
| Socios clave | [elemento]; [elemento] |
| Estructura de costos | [elemento]; [elemento] |

**Lectura del modelo.** [En qué bloques aparece la problemática.]
```

## Ejemplo

```markdown
## 1.4. Modelo de negocio: Business Model Canvas

El Business Model Canvas describe en nueve bloques cómo una organización crea, entrega y captura valor (Osterwalder & Pigneur, 2010). El lienzo de Pollería Don Tito muestra un negocio de producto conocido que crece por los canales de delivery.

<!-- figura: bmc -->

| Bloque | Contenido |
|---|---|
| Segmentos de clientes | Familias de San Juan de Lurigancho; trabajadores que almuerzan cerca de los locales; clientes de delivery del distrito |
| Propuesta de valor | Pollo a la brasa de sabor casero; atención rápida; precios justos; pedido en el local, para llevar o a domicilio |
| Canales | Salón; para llevar; delivery propio por WhatsApp; Rappi; PedidosYa |
| Relaciones con clientes | Atención personal en el local; pedidos por WhatsApp con clientes frecuentes; reseñas en las aplicaciones |
| Fuentes de ingresos | Venta de pollos y combos; bebidas y adicionales; cargo por delivery propio |
| Recursos clave | Hornos y cocina de los dos locales; receta y marca conocida en el distrito; equipo de cocina y cuatro motorizados |
| Actividades clave | Compra y preparación del pollo; producción por turno; atención y despacho de pedidos |
| Socios clave | Proveedores de pollo vivo y de insumos; Rappi y PedidosYa; proveedor del sistema de caja |
| Estructura de costos | Pollo y otros insumos; comisiones de 25 % a 30 % de las aplicaciones; planilla; alquiler y servicios de los locales |

**Lectura del modelo.** El crecimiento llega por el bloque de canales, pero las aplicaciones suman a la estructura de costos una comisión que el precio no refleja. Además, la producción por turno, que es una actividad clave, se decide sin datos, por lo que la problemática se ubica entre canales, actividades clave y estructura de costos.
```

## Checklist
- [ ] Encabezado exacto y marca `<!-- figura: bmc -->` en una línea sola.
- [ ] Nueve bloques con su nombre exacto, cada uno con contenido.
- [ ] La lectura del modelo nombra los bloques donde está la problemática.
- [ ] `visuales/bmc.html` y `leer-imagen/bmc.md` construidos con `visuales.py`.
- [ ] La cita del lienzo está en `referencias.md`.
