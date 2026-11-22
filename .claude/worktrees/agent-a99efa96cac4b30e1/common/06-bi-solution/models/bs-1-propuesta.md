# Plantilla: Propuesta de solución en BI (`secciones/2.1.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.1.md` |
| **Punto** | 2.1. Propuesta de solución en BI |
| **Códigos** | cita `OE-nn` (del brief), `CAP-nn` (de 2.2) y `CAU-nn` (causas principales de 1.8) |
| **Entradas** | brief vigente (usuarios, decisiones, objetivos), corrida vigente de `05` (problemática y causas principales), componentes de 2.2 |
| **Salida** | qué decisiones apoya la solución, para quién y cómo responde a la problemática y a cada objetivo |

## Instrucciones para el agente
1. La primera línea es `## 2.1. Propuesta de solución en BI`. Esta sección no lleva figura.
2. Un párrafo que presenta la solución: qué fuentes integra, qué produce y para quién.
3. **Decisiones que apoya.** Viñetas con las decisiones de la sección 5 del brief, con su verbo.
4. **Usuarios.** Quién usa el dashboard y quién decide, como en el brief.
5. **Respuesta a la problemática.** Dos o tres frases: el problema central de 1.8 y cómo la solución actúa sobre sus causas principales, citadas por su código `CAU-nn`. Sin corrida de `05`, se apoya en el problema principal del brief y no cita causas.
6. La tabla `Objetivo | Componentes | Cómo lo atiende` con una fila por cada `OE` del brief: los `CAP` de 2.2 que lo atienden (separados por coma) y una frase con el resultado.

## Formato

```markdown
## 2.1. Propuesta de solución en BI

[Párrafo que presenta la solución.]

**Decisiones que apoya.**
- [decisión del brief]

**Usuarios.** [quién usa el dashboard y quién decide]

**Respuesta a la problemática.** [problema central y cómo la solución actúa sobre CAU-nn]

Tabla 1: Objetivos específicos y componentes de la solución

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-nn, CAP-nn | [resultado que lo hace posible] |
```

## Ejemplo

```markdown
## 2.1. Propuesta de solución en BI

La solución integra en un modelo dimensional las ventas de la caja, los reportes de las aplicaciones de delivery, el control de producción de cocina y el precio del pollo vivo, y los presenta en un dashboard de Power BI para que la gerencia de Pollería Don Tito vea cuánto deja cada canal y cuánto pollo se pierde por turno.

**Decisiones que apoya.**
- Ajustar el precio de los combos en las apps de delivery.
- Definir cuántos pollos hornear por turno y día de la semana.
- Anticipar compras ante subidas del precio del pollo vivo.

**Usuarios.** El gerente general, que decide precios y compras, y el jefe de cocina, que ejecuta la producción por turno.

**Respuesta a la problemática.** El margen neto cayó de 14 % a 8 % mientras las ventas crecían, y hoy nadie puede ver dónde se pierde. La solución une los tres registros de ventas que no se cruzan (CAU-06), calcula el margen de cada canal después de la comisión (CAU-01), mide la merma de cada turno (CAU-02) y sigue el precio del insumo (CAU-04).

Tabla 1: Objetivos específicos y componentes de la solución

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-05, CAP-06 | El proceso ETL aplica las reglas de calidad y deja en el repositorio un modelo estrella con los registros depurados |
| OE-02 | CAP-01, CAP-02, CAP-07, CAP-08 | El modelo une ventas y comisiones por canal y el dashboard muestra el margen neto de los cinco canales |
| OE-03 | CAP-04, CAP-07, CAP-08 | El control de producción se cruza con las ventas por turno y el dashboard muestra la merma de cada turno |
```

## Checklist
- [ ] Encabezado exacto en la primera línea y sin figura.
- [ ] Las decisiones y los usuarios son los del brief.
- [ ] La respuesta a la problemática cita las causas principales de 1.8.
- [ ] Una fila por cada `OE` del brief, con componentes que existen en 2.2.
