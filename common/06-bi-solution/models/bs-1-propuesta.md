# Plantilla: Propuesta de solución en BI (`secciones/2.1.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.1.md` |
| **Punto** | 2.1. Propuesta de solución en BI |
| **Códigos** | cita `OE-nn` (del brief) y `CAP-nn` (de 2.2) |
| **Entradas** | brief vigente (usuarios, decisiones, objetivos), corrida vigente de `05-make-problem-objectives` (problemática y causas principales) |
| **Salida** | qué decisiones apoya la solución, quién la usa, cómo responde a la problemática y qué componente atiende cada objetivo específico |

## Instrucciones para el agente
1. La primera línea es `## 2.1. Propuesta de solución en BI`.
2. **Decisiones que apoya.** Viñetas con las decisiones del brief (sección 5), sin agregar otras.
3. **Usuarios.** Quién usa la solución y qué decide cada uno.
4. **Respuesta a la problemática.** Un párrafo de tres a cinco frases: qué ofrece la solución frente a la problemática central y sus causas principales (1.8). No repite el diagnóstico.
5. Una frase de enlace y la tabla `Objetivo | Componentes | Cómo lo atiende` con **una fila por cada `OE` del brief**: sus `CAP-nn` de 2.2 (al menos uno) y una frase de cómo lo atienden. No se agregan objetivos que el brief no tenga.
6. Escribe 2.1 después de 2.2 si necesitas fijar los `CAP-nn`; los códigos de la tabla deben existir en 2.2.

## Formato

```markdown
## 2.1. Propuesta de solución en BI

**Decisiones que apoya.**
- [decisión del brief]

**Usuarios.** [quién usa la solución y qué decide].

**Respuesta a la problemática.** [Tres a cinco frases.]

[Frase que presenta la tabla.]

Tabla 1: Componentes de la solución que atienden cada objetivo específico

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-nn, CAP-nn | [una frase] |
```

## Ejemplo

```markdown
## 2.1. Propuesta de solución en BI

**Decisiones que apoya.**
- Ajustar el precio de los combos en las apps de delivery.
- Definir cuántos pollos hornear por turno y día de la semana.
- Anticipar compras ante subidas del precio del pollo vivo.

**Usuarios.** El gerente general, que decide precios y compras, y el jefe de cocina, que ejecuta la producción de cada turno.

**Respuesta a la problemática.** La solución reúne en un solo modelo las ventas de caja, los reportes de las aplicaciones y los precios del pollo vivo, que hoy están separados. Con ellos calcula el margen de cada canal después de comisiones y costos y la merma de cada turno. Así la gerencia deja de fijar precios iguales en todos los canales y la cocina deja de producir sin referencia, que son las causas que más pesan en la caída del margen.

El dashboard responde a cada objetivo específico con componentes concretos de la arquitectura, que se describe en el punto siguiente.

Tabla 1: Componentes de la solución que atienden cada objetivo específico

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-04, CAP-05 | El proceso ETL depura y cruza las tres fuentes y las deja en un modelo en estrella |
| OE-02 | CAP-05, CAP-06 | El modelo calcula el margen por canal y el dashboard lo muestra frente a la meta |
| OE-03 | CAP-05, CAP-06 | El modelo cruza lo preparado con lo vendido por turno y el dashboard muestra la merma |
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Las decisiones y los usuarios son los del brief.
- [ ] Una fila de la tabla por cada `OE` del brief, con al menos un `CAP-nn` que existe en 2.2.
- [ ] El texto no repite el diagnóstico y no promete lo que el alcance excluye.
