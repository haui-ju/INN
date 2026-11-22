# Brief del proyecto · Mejora del margen por canal y reducción de la merma con Power BI para Pollerías y Parrilladas San Martín

## 1. Tema y empresa

Una solución de BI en Power BI que integra las ventas de todos los canales, la producción por turno y el precio del pollo vivo para recuperar el margen neto, fijar precios por canal y reducir la merma.

**Empresa.** Pollerías y Parrilladas San Martín S.A.C. (RUC 20537751950), pollería con domicilio fiscal en Magdalena del Mar, Lima.

## 2. Problemática

**Problema principal.** Las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %.

**Quién lo sufre.** El dueño y el jefe de cocina, que deciden precios, producción y compras sin ver la rentabilidad por canal ni la merma.

**Situación actual.** Los precios son iguales en todos los canales, el jefe de cocina decide cuántos pollos hornear por turno según su experiencia y el costo del pollo vivo no se relaciona con el margen ni con los precios.

**Evidencia.**
- Las apps de delivery pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión.
- La merma es de 7 % de los pollos preparados, frente a 3 % o menos recomendable; los domingos falta pollo y los martes sobra.
- El pollo vivo pasó de S/ 6.10 a S/ 6.90 por kilogramo entre el 1 y el 14 de julio de 2026 en Lima Metropolitana (MIDAGRI, julio de 2026).

## 3. Objetivos

### 3.1. Objetivo general

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | Implementar una solución de BI en Power BI que integre las ventas de todos los canales, la producción por turno y el precio del pollo vivo para recuperar el margen neto | Margen neto | 12 % o más, a seis meses de implantada la solución | Entrega (07-12-2026) | Margen neto global |

### 3.2. Objetivos específicos

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | Integrar y depurar las fuentes de ventas (caja, Rappi, PedidosYa y WhatsApp) mediante un proceso ETL en Power Query | Registros que pasan las reglas de calidad | 98 % o más | Entrega (07-12-2026) | OG-01 | Calidad de datos del ETL |
| OE-02 | Medir el margen de contribución por canal y por producto | Canales y productos con margen calculado | 100 % de los canales y productos del periodo | Entrega (07-12-2026) | OG-01 | Margen de contribución por canal y producto |
| OE-03 | Pronosticar la demanda de pollos por día y turno para reducir la merma | Merma sobre los pollos preparados | De 7 % a 3 % o menos | Entrega (07-12-2026) | OG-01 | Porcentaje de merma por turno |
| OE-04 | Monitorear el efecto del precio del pollo vivo en el costo y el margen | Días del periodo con el precio del insumo cruzado con el margen | 100 % de los días | Entrega (07-12-2026) | OG-01 | Precio promedio del pollo vivo por kilogramo |
| OE-05 | Construir un dashboard con KPI, metas y filtros que guíe las decisiones de precio, producción y personal | KPI con meta y semáforo | 100 % de los KPI | Entrega (07-12-2026) | OG-01 | KPI con meta en el dashboard |

## 4. Justificación y alcance

**Justificación.** El dueño podrá fijar precios diferenciados por canal, definir cuántos pollos preparar en cada turno y asignar el personal según la franja horaria con cifras y no por intuición. Recuperar el margen neto de 8 % a 12 % y bajar la merma de 7 % a 3 % tiene un efecto directo en la utilidad de la pollería.

Una solución de BI es adecuada porque integra fuentes dispersas (caja, aplicaciones de delivery, WhatsApp, producción e insumo) con un proceso ETL, las ordena en un modelo dimensional y las presenta en un dashboard con KPI, metas y pronóstico de demanda.

### 4.1. Alcance

| Alcance | Detalle |
|---|---|
| Incluye | Ventas por canal (caja, Rappi, PedidosYa y WhatsApp), producción por turno, comisiones, costo y precio del pollo vivo, de enero a octubre de 2026 |
| No incluye | Contabilidad completa, planillas, otros insumos ni pronóstico de otros productos |
| Herramientas previstas | Power BI Desktop y Power Query para el ETL; almacenamiento Pendiente |

### 4.2. Limitaciones

| Limitación | Detalle |
|---|---|
| Datos | Los datos internos se generan con reglas coherentes con el rubro porque no hay acceso a la caja de la empresa; los precios del insumo vienen de una fuente abierta |
| Tiempo | Una sola entrega el 07-12-2026; se priorizan el margen por canal, la merma y el pronóstico |

## 5. Usuarios y decisiones

**Usuarios.** El dueño, que decide precios y compras, y el jefe de cocina, que ejecuta la producción de cada turno.

**Decisiones que apoyará el dashboard.**
- Fijar precios diferenciados por canal.
- Definir cuántos pollos preparar en cada turno y día de la semana.
- Asignar el personal según la franja horaria.
- Anticipar compras y ajustar precios ante subidas del precio del pollo vivo.

## 6. Fuentes de datos previstas

| Código | Fuente | Tipo | Datos | Acceso |
|---|---|---|---|---|
| FUE-01 | Sistema de caja (salón y para llevar) | Generada | Ventas por ticket, producto, canal y turno, de enero a octubre de 2026 | Autorizado |
| FUE-02 | Reportes de Rappi | Generada | Pedidos y comisiones por pedido | Autorizado |
| FUE-03 | Reportes de PedidosYa | Generada | Pedidos y comisiones por pedido | Autorizado |
| FUE-04 | Pedidos por WhatsApp | Generada | Pedidos del delivery propio | Autorizado |
| FUE-05 | Control de producción por turno | Generada | Pollos preparados, vendidos y merma por turno | Autorizado |
| FUE-06 | Boletín de precios de aves de MIDAGRI | Abierta | Precio diario del pollo vivo en Lima Metropolitana | Público |

## 7. Calendario

| Inicio | Entrega |
|---|---|
| 22-11-2026 | 07-12-2026 |

## 8. Supuestos y riesgos iniciales

| Código | Tipo | Descripción | Cómo se vigila |
|---|---|---|---|
| INI-01 | Supuesto | El dueño y el jefe de cocina usarán el dashboard en su revisión semanal | Se valida con el usuario en la exposición |
| INI-02 | Supuesto | Las cifras del caso (ventas de 18 % más, margen de 14 % a 8 %, apps con 35 % de las ventas y merma de 7 %) son el punto de partida planteado por el equipo y los datos generados las reflejan | Se documentan las reglas de generación en el diccionario de datos |
| INI-03 | Riesgo | El plazo hasta el 07-12-2026 es corto para el ETL, el modelo, el pronóstico y el dashboard | Se prioriza margen y merma y el pronóstico va al final |
| INI-04 | Riesgo | El boletín de MIDAGRI viene en PDF y puede tener días sin dato | Se registran los días imputados en el campo valor_imputado |
