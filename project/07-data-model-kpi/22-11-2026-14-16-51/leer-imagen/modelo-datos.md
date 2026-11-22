# Leer la imagen · Modelo de datos en estrella

- **Para qué sirve.** Muestra las tablas de hechos, las dimensiones y las relaciones sobre las que se calculan los indicadores.
- **Qué dice.** El modelo tiene 4 tablas de hechos y 5 dimensiones unidas por 9 relaciones, y fPedidos es el hecho con más ejes de análisis (4 claves).
- **Qué debes entender.** Las cuatro tablas de hechos no se unen entre sí: se cruzan a través de las dimensiones que comparten. dCalendario las une a las cuatro, así que un filtro por mes afecta a ventas, producción, precio del pollo y metas a la vez, y dTurno une pedidos con producción para comparar lo preparado con lo vendido. En cambio, canal y producto solo existen en fPedidos, por eso el margen por canal y producto se calcula únicamente desde los pedidos, con la comisión de 25 % a 30 % de las aplicaciones ya descontada. Cada hecho tiene su propio grano, por ejemplo un pedido por día frente a un KPI por mes, y sus medidas no se suman entre tablas distintas.
- **Pie de foto sugerido.** Figura X: Modelo de datos en estrella.
