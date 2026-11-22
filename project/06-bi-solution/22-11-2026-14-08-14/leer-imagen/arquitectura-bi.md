# Leer la imagen · Arquitectura de BI

- **Para qué sirve.** Muestra cómo viaja el dato desde las fuentes hasta el dashboard en cuatro capas.
- **Qué dice.** Los datos pasan de 6 fuentes por 2 componentes de ETL y 1 de almacenamiento hasta 3 componentes de visualización.
- **Qué debes entender.** Hoy los datos están en seis lugares que no se cruzan: la caja, Rappi, PedidosYa, WhatsApp, el control de producción y el boletín de precios. La arquitectura los lleva en un solo sentido por cuatro capas: Power Query los extrae y depura, las reglas de calidad los homologan y todo queda en un único modelo dimensional (CAP-09). De ese modelo salen el dashboard, el pronóstico de demanda y su publicación, de modo que el margen, la merma y el precio del pollo se miden siempre con los mismos datos. Todo se construye con Power BI, sin servidor ni costo adicional, y el dueño y el jefe de cocina lo consultan desde el navegador.
- **Pie de foto sugerido.** Figura X: Arquitectura de BI.
