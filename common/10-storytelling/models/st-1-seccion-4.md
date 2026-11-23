# Plantilla: Storytelling con datos (`secciones/4.md`)

| | |
|---|---|
| **Entregable** | `secciones/4.md` y `capturas/pag-nn.png` (copiadas de 09) |
| **Punto** | 4. Storytelling con datos (incluye imagen) |
| **Códigos** | `HLZ-nn`; cita `OE-nn` del brief y `KPI-nn` de `modelo.json` |
| **Entradas** | `valores.json` y capturas de `09-make-dashboard`, 3.2 (qué KPI se ve en qué página), `modelo.json` (meta y objetivo de cada KPI), brief (objetivos, usuarios y decisiones) |
| **Salida** | una narrativa de hallazgos, cada uno con su valor real frente a su meta, la captura que lo muestra y la decisión que apoya |

## Instrucciones para el agente
1. La primera línea es `## 4. Storytelling con datos`. Escribe esta sección **solo cuando la corrida vigente de 09 trae `valores.json` y las capturas** y el usuario confirmó la propuesta de hallazgos.
2. **Primer párrafo.** Con `modo_datos: generado`, di que los hallazgos se basan en datos generados para el proyecto y medidos por el equipo en el dashboard, y que no describen el negocio real de una empresa. Añade una frase sobre cómo se leen: del indicador a su meta y a la decisión.
3. **Contexto.** Un párrafo que empieza con `**Contexto.**`: la problemática y quién decide, del capítulo 1. Sin cifras del dashboard.
4. **Hallazgos.** `**Hallazgos.**`, una frase que presenta la tabla y la tabla `Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya`: una fila por hallazgo `HLZ-nn`; el objetivo es el que mide el KPI en `modelo.json`; el valor es el de `valores.json` con sus decimales; la meta es la de 2.5, copiada tal cual; el estado es `Cumple`, `No cumple` o `Sin meta` (se calcula con el comparador de la meta); la captura es `pag-nn` de la página donde se ve el KPI; quien decide es un usuario del brief.
5. **Narrativa.** Por cada hallazgo, un encabezado `### HLZ-nn. Título` (el título dice la conclusión, no el nombre del KPI), la línea `<!-- captura: pag-nn -->` si es la primera vez que se usa esa captura, y dos párrafos: `**Qué muestra.**` (el dato frente a su meta, con `{{figura:pag-nn}}`) y `**Qué decisión apoya.**` (qué puede hacer distinto esa persona). Cada cifra con unidad es un valor, una meta o la diferencia entre ambos.
6. **Prioridades.** `**Prioridades.**` Qué decisión va primero y por qué, usando las brechas de la tabla.
7. **Metas pendientes.** `**Metas pendientes.**` Solo si un hallazgo cuenta un KPI sin meta: nómbralo y di que su meta se propone con su valor real en 09 y se registra con `07-make-data-model-kpi-update`.
8. Cada tabla lleva antes una línea `Tabla N: título`. Sin comentarios ni notas: solo texto final y las marcas de captura.

## Formato

```markdown
## 4. Storytelling con datos

[Declaración: datos generados para el proyecto, medidos en el dashboard, sin describir el negocio real; cómo se leen los hallazgos.]

**Contexto.** [Problemática y quién decide, sin cifras del dashboard.]

**Hallazgos.** [Frase que presenta la tabla.]

Tabla 1: Hallazgos del dashboard

| Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya |
|---|---|---|---|---|---|---|---|---|
| HLZ-01 | OE-01 | KPI-01 | [valor de valores.json] | [meta de modelo.json] | [Cumple, No cumple o Sin meta] | pag-01 | [usuario del brief] | [decisión] |

### HLZ-01. [Título con la conclusión]

<!-- captura: pag-01 -->

**Qué muestra.** [El dato frente a su meta, con {{figura:pag-01}}.]

**Qué decisión apoya.** [Qué puede hacer distinto el usuario.]

**Prioridades.** [Qué decisión va primero y por qué.]

**Metas pendientes.** [Solo si hay un KPI sin meta.]
```

## Ejemplo

```markdown
## 4. Storytelling con datos

Los hallazgos de este capítulo se basan en datos generados para el proyecto y medidos por el equipo en el dashboard de Power BI; no describen el negocio real de una empresa. Cada hallazgo parte de un indicador, lo compara con su meta y termina en una decisión del gerente general o del jefe de cocina.

**Contexto.** La pollería vende cada vez más por las aplicaciones de delivery, pero el margen se estrecha y el jefe de cocina hornea por experiencia. El dashboard reúne ventas, producción y precio del pollo para que esas decisiones dejen de tomarse sin datos.

**Hallazgos.** La tabla resume cinco hallazgos con su objetivo, el indicador que los sostiene, el valor frente a la meta y la decisión que apoyan; debajo se cuenta cada uno con la captura que lo muestra.

Tabla 1: Hallazgos del dashboard

| Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya |
|---|---|---|---|---|---|---|---|---|
| HLZ-01 | OE-01 | KPI-01 | 97,2 % | 98 % o más | No cumple | pag-01 | Gerente general | Revisar los registros rechazados antes de fijar precios con diferencias pequeñas |
| HLZ-02 | OE-02 | KPI-02 | 8,4 % | 12 % o más en el margen neto global | No cumple | pag-02 | Gerente general | Fijar un precio distinto en las aplicaciones para compensar la comisión |
| HLZ-03 | OE-02 | KPI-04 | 71,0 % | 70 % o más | Cumple | pag-02 | Gerente general | Mantener el impulso al canal directo mientras se corrige el precio de las aplicaciones |
| HLZ-04 | OE-03 | KPI-03 | 6,9 % | 3 % o menos | No cumple | pag-03 | Jefe de cocina | Ajustar cuántos pollos se hornean en cada turno según el día de la semana |
| HLZ-05 | OE-02 | KPI-05 | S/ 6,55 | Pendiente | Sin meta | pag-04 | Gerente general | Anticipar compras cuando el precio suba y fijar la meta de este indicador |

### HLZ-01. Las cifras sirven para las tendencias, pero todavía no para los detalles

<!-- captura: pag-01 -->

**Qué muestra.** La {{figura:pag-01}} muestra que el 97,2 % de los registros cargados es válido, 0,8 puntos porcentuales por debajo de la meta de 98 %. La diferencia es pequeña, pero cada registro descartado es una venta que no entra en el margen.

**Qué decisión apoya.** El gerente general puede confiar en las tendencias de los demás hallazgos, pero conviene revisar qué fuente descarta más registros antes de fijar un precio con una diferencia pequeña.

### HLZ-02. El margen por canal queda por debajo de lo esperado

<!-- captura: pag-02 -->

**Qué muestra.** La {{figura:pag-02}} muestra un margen neto de 8,4 %, 3,6 puntos porcentuales por debajo de la meta de 12 %. Los precios son iguales en todos los canales y las aplicaciones cobran comisión, de modo que cada pedido por delivery deja menos que uno del salón.

**Qué decisión apoya.** El gerente general puede fijar un precio distinto en las aplicaciones y medir en el mismo dashboard si el margen se acerca a su meta.

### HLZ-03. El canal directo ya cumple su meta

**Qué muestra.** Como se ve en la {{figura:pag-02}}, el canal directo concentra el 71,0 % de las ventas, 1,0 puntos porcentuales sobre la meta de 70 %. Es el único indicador de esa página que cumple.

**Qué decisión apoya.** El gerente general puede mantener el impulso al canal directo mientras corrige el precio de las aplicaciones, sin perder lo ganado.

### HLZ-04. La cocina prepara más pollo del que vende

<!-- captura: pag-03 -->

**Qué muestra.** La {{figura:pag-03}} muestra una merma de 6,9 %, 3,9 puntos porcentuales por encima de la meta de 3 %. Es más del doble de lo recomendable y se ve turno por turno.

**Qué decisión apoya.** El jefe de cocina puede ajustar cuántos pollos hornea en cada turno según el día de la semana y seguir el efecto en la misma página.

### HLZ-05. El precio del pollo vivo todavía no tiene una referencia

<!-- captura: pag-04 -->

**Qué muestra.** La {{figura:pag-04}} muestra un precio promedio de S/ 6,55 por kilogramo de pollo vivo. Como el indicador no tiene meta, no se puede decir si ese precio es alto o bajo.

**Qué decisión apoya.** El gerente general puede anticipar compras cuando el precio suba y usar este valor como punto de partida para fijar la meta del indicador.

**Prioridades.** La decisión más urgente es la de producción (HLZ-04), porque la merma es la mayor distancia frente a su meta y la cocina puede corregirla sin depender de nadie. Le sigue el precio por canal (HLZ-02), que el gerente general decide con el margen a la vista. La calidad de los datos (HLZ-01) y el precio del pollo (HLZ-05) acompañan esas dos decisiones.

**Metas pendientes.** KPI-05 no tiene meta: se propone con su valor real en 09-make-dashboard y se registra con 07-make-data-model-kpi-update.
```

## Checklist
- [ ] Encabezado exacto en la primera línea y primer párrafo con la declaración de datos generados.
- [ ] Cada objetivo del brief tiene al menos un hallazgo y cada KPI mide el objetivo de su hallazgo.
- [ ] Valor, meta y estado de cada fila coinciden con `valores.json` y con 2.5.
- [ ] Cada captura está copiada a `capturas/` y marcada una sola vez.
- [ ] Toda cifra con unidad es un valor, una meta o la diferencia entre ambos.
- [ ] Cada hallazgo tiene narrativa con «Qué muestra» y «Qué decisión apoya».
- [ ] Hay «Contexto» y «Prioridades» y, si falta alguna meta, «Metas pendientes».
- [ ] Cada tabla tiene su título `Tabla N: …`.
