# Informe · Mejora del margen por canal y reducción de la merma con Power BI para Pollerías y Parrilladas San Martín

## Control del documento

| Campo | Dato |
|---|---|
| Título del proyecto | Mejora del margen por canal y reducción de la merma con Power BI para Pollerías y Parrilladas San Martín |
| Tema | Una solución de BI en Power BI que integra las ventas de todos los canales, la producción por turno y el precio del pollo vivo para recuperar el margen neto, fijar precios por canal y reducir la merma. |
| Empresa | Pollerías y Parrilladas San Martín S.A.C. (RUC 20537751950), pollería con domicilio fiscal en Magdalena del Mar, Lima. |
| Curso | Pendiente |
| Docente | Pendiente |
| Integrantes | Salim Felix Escovedo, Luis Fernando Melgar Pizarro |
| Fecha de entrega | 07-12-2026 |

**Formato de entrega.** Word o PDF, letra Arial 11, interlineado 1.5 y márgenes estándar. Antes de entregar, cada marcador «(INCLUIR IMAGEN: …)» se reemplaza por su imagen; el dashboard se presenta en Power BI en la exposición.

# Capítulo 1: Diagnóstico estratégico y análisis del negocio

Este capítulo presenta a la empresa, su modelo de negocio y su entorno, y de ese diagnóstico deriva la problemática central y los objetivos que guían la solución de Inteligencia de Negocios. Comprende 1.1 Nombre de la empresa, 1.2 Misión y visión, 1.3 Industria y tamaño, 1.4 Modelo de negocio: Business Model Canvas, 1.5 Análisis PESTEL, 1.6 Matriz FODA, 1.7 Diagrama de la problemática: Ishikawa, 1.8 Problemática central del negocio, 1.9 Objetivo general del proyecto y 1.10 Objetivos específicos.

## 1.1. Nombre de la empresa

Pollerías y Parrilladas San Martín es una pollería con domicilio fiscal en Magdalena del Mar, Lima. Atiende en salón y para llevar, y vende por delivery propio por WhatsApp y por las aplicaciones Rappi y PedidosYa, que pasaron de 15 % a 35 % de sus ventas.

Tabla 1: Datos generales de la empresa

| Dato | Valor |
|---|---|
| Razón social | Pollerías y Parrilladas San Martín S.A.C. |
| Nombre comercial | Pollerías y Parrilladas San Martín |
| RUC | 20537751950 |
| Actividad económica | Actividades de restaurantes y de servicio móvil de comidas (CIIU 5610) |
| Ubicación | Magdalena del Mar, Lima |
| Locales y canales | Un establecimiento registrado; salón, para llevar, delivery propio por WhatsApp, Rappi y PedidosYa |

**Reseña.** La empresa emite comprobantes electrónicos desde julio de 2018. Su oferta se centra en el pollo a la brasa y las parrilladas, que vende en el local y por las aplicaciones de delivery.

## 1.2. Misión y visión

**Misión.** Ofrecer pollo a la brasa y parrilladas de buen sabor, con atención rápida y precios justos para las familias y los trabajadores de la zona, en el local o en su casa.

**Visión.** Ser una pollería rentable y reconocida en Lima, que decide sus precios y su producción con datos.

**Valores.**
- Sabor y calidad constantes.
- Atención rápida y cercana.
- Decisiones basadas en datos.

**Relación con el proyecto.** La visión pide decidir con datos, pero hoy la empresa fija precios y producción sin ver el margen de cada canal ni la merma. Las ventas crecieron 18 % en el último año y el margen neto cayó de 14 % a 8 %; las aplicaciones de delivery pasaron de 15 % a 35 % de las ventas y la merma es de 7 %. La solución de BI mide la rentabilidad por canal y la merma para que las decisiones de precio y producción partan de esas cifras.

## 1.3. Industria y tamaño

La empresa pertenece a la industria de restaurantes, dentro del sector de servicios de comidas y bebidas, y compite con cadenas de pollerías, pollerías independientes y la oferta de las aplicaciones de delivery, que ya reúnen 35 % de sus ventas.

Tabla 2: Industria y entorno competitivo

| Aspecto | Descripción |
|---|---|
| Sector | Servicios de comidas y bebidas (restaurantes) |
| Actividad económica (CIIU) | 5610: actividades de restaurantes y de servicio móvil de comidas |
| Tipo de cliente | Familias, trabajadores y vecinos de Magdalena del Mar y distritos cercanos que compran en el local, para llevar o por delivery |
| Entorno competitivo | Cadenas de pollerías con varios locales, pollerías independientes y otras comidas rápidas en las aplicaciones de delivery |

**Tamaño de la organización.** Con ventas anuales de S/ 2 400 000, equivalentes a unas 436 UIT, la empresa es una pequeña empresa según el artículo 5 de la Ley 30056. Esta norma ubica en esa categoría a las ventas anuales superiores a 150 UIT y hasta 1700 UIT (Congreso de la República del Perú, 2013). La UIT de referencia es la de 2026, fijada en S/ 5 500 (Ministerio de Economía y Finanzas, 2025). La empresa declara 16 trabajadores a la Superintendencia Nacional de Aduanas y Administración Tributaria (SUNAT).

Tabla 3: Tamaño de la empresa según la Ley 30056

| Dato | Valor |
|---|---|
| Ventas anuales | S/ 2 400 000 (2025) |
| UIT de referencia | S/ 5 500 (2026) |
| Ventas en UIT | 436 |
| Trabajadores | 16 |
| Categoría (Ley 30056) | Pequeña empresa |

## 1.4. Modelo de negocio: Business Model Canvas

El Business Model Canvas describe en nueve bloques cómo una organización crea, entrega y captura valor (Osterwalder & Pigneur, 2010). El Business Model Canvas de la pollería muestra un negocio de producto conocido que crece por los canales de delivery.

(INCLUIR IMAGEN: Figura 1: Business Model Canvas. Archivo sugerido: imagenes/bmc.html)

**Cómo copiarla.** Abrir [imagenes/bmc.html](imagenes/bmc.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra en una sola vista cómo la empresa crea, entrega y captura valor. Los nueve bloques se leen como una cadena: a quién se atiende, por qué canal le llega el pollo y cuánto queda después de los costos. El negocio crece por el canal que menos deja: las aplicaciones de delivery pasaron de 15 % a 35 % de las ventas, pero cobran de 25 % a 30 % de comisión y venden al mismo precio que el salón. Además, el jefe de cocina decide la producción de cada turno por experiencia y la merma llega a 7 %. Por eso la problemática del proyecto se concentra en tres bloques: canales, actividades clave y estructura de costos.

**Lectura del modelo.** El crecimiento llega por el bloque de canales: las aplicaciones pasaron de 15 % a 35 % de las ventas. Sin embargo, suman a la estructura de costos una comisión de 25 % a 30 % que el precio no refleja, porque los precios son iguales en todos los canales. Además, el jefe de cocina decide la producción por turno, una actividad clave, según su experiencia, y la merma llega a 7 %. La problemática se ubica así entre canales, actividades clave y estructura de costos.

## 1.5. Análisis PESTEL

El análisis PESTEL examina los factores políticos, económicos, sociales, tecnológicos, ecológicos y legales del entorno que la empresa no controla, pero que condicionan sus resultados (Aguilar, 1967). Para Pollerías y Parrilladas San Martín se identificaron nueve hallazgos, cada uno con su efecto en el negocio y su fuente.

(INCLUIR IMAGEN: Figura 2: Análisis PESTEL. Archivo sugerido: imagenes/pestel.html)

**Cómo copiarla.** Abrir [imagenes/pestel.html](imagenes/pestel.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Resume los factores del entorno que favorecen o amenazan al negocio. El entorno pesa más en contra que a favor: de nueve hallazgos, cinco son amenazas y cuatro, oportunidades. Las amenazas que más golpean el margen son el precio del pollo vivo, que subió de S/ 6.10 a S/ 6.90 por kilogramo en dos semanas, la inflación y las comisiones de las aplicaciones. A favor están la demanda de delivery, que lidera el pollo, y las herramientas de BI de costo bajo, como Power BI Desktop, que la empresa puede usar sin pagar licencia. Estos hallazgos pasan a la matriz FODA como oportunidades y amenazas.

Tabla 4: Análisis PESTEL

| Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente |
|---|---|---|---|---|---|
| POL-01 | Político | La Ley 30056, que busca impulsar el desarrollo productivo y el crecimiento empresarial, clasifica como pequeña empresa a la que vende más de 150 UIT y hasta 1700 UIT al año | Con 436 UIT de ventas anuales, la pollería queda clasificada como pequeña empresa dentro de ese marco | Oportunidad | Congreso de la República del Perú (2013) |
| ECO-01 | Económico | El precio del pollo vivo en Lima pasó de S/ 6.10 a S/ 6.90 por kilogramo entre el 1 y el 14 de julio de 2026 | El costo del insumo principal subió en dos semanas sin que los precios de venta cambiaran | Amenaza | Expreso (2026) |
| ECO-02 | Económico | La inflación de Lima Metropolitana fue de 5.25 % en los doce meses a octubre de 2026 | Suben los costos de insumos, servicios y transporte, y el margen se reduce si los precios no se ajustan | Amenaza | Andina (2026), con datos del Instituto Nacional de Estadística e Informática |
| SOC-01 | Social | La categoría de pollo y alitas lidera el volumen de pedidos de comida por delivery | La demanda de delivery favorece a una pollería, y las ventas por aplicaciones pasaron de 15 % a 35 % del total | Oportunidad | Vera (2026) |
| SOC-02 | Social | El domingo concentra más de 18 % de las órdenes semanales de delivery y el pico diario es a las 8:00 p. m. | La demanda sigue un patrón por día y hora que permite pronosticar la producción por turno | Oportunidad | Vera (2026) |
| TEC-01 | Tecnológico | Power BI Desktop es de uso gratuito y permite conectar varias fuentes de datos, prepararlas con Power Query y crear informes con medidas DAX y previsión | La empresa puede construir su dashboard sin pagar licencias de escritorio | Oportunidad | Microsoft (s. f.), consultado en noviembre de 2026 |
| TEC-02 | Tecnológico | Las aplicaciones de delivery cobran a la empresa entre 25 % y 30 % de cada venta | Cada venta por aplicación deja menos margen que una venta en el local | Amenaza | Comisiones por aplicación de la empresa, 2026 |
| AMB-01 | Ecológico | La Ley 30884 prohíbe los envases y vasos de poliestireno expandido (tecnopor) para alimentos y bebidas de consumo humano, y su reglamento fija la progresividad | Los envases para llevar y delivery deben ser de otro material, lo que puede elevar su costo | Amenaza | Congreso de la República del Perú (2018) |
| LEG-01 | Legal | El Ejecutivo aprobó en noviembre de 2024 el nuevo reglamento de la Ley 29733, de Protección de Datos Personales (Decreto Supremo N.° 016-2024-JUS) | Los datos de los clientes de WhatsApp y de las aplicaciones deben tratarse conforme a esa ley y anonimizarse en el modelo de datos | Amenaza | El Peruano (2024) |

**Síntesis.** Los factores económicos y tecnológicos concentran cuatro de los nueve hallazgos. El precio del pollo (ECO-01), la inflación (ECO-02) y las comisiones de las aplicaciones (TEC-02) presionan el margen. La demanda de delivery (SOC-01) y las herramientas de BI de bajo costo (TEC-01) abren oportunidades. Estos hallazgos pasan a la matriz FODA (fortalezas, oportunidades, debilidades y amenazas) como oportunidades y amenazas.

## 1.6. Matriz FODA

La matriz FODA organiza en cuatro cuadros los factores internos y externos que favorecen o dificultan el logro de los objetivos de la organización (Gürel & Tat, 2017). Los factores internos salen del modelo de negocio y de los registros de la pollería; los externos, del análisis PESTEL.

(INCLUIR IMAGEN: Figura 3: Matriz FODA. Archivo sugerido: imagenes/foda.html)

**Cómo copiarla.** Abrir [imagenes/foda.html](imagenes/foda.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Resume la situación de la empresa para decidir qué aprovechar y qué proteger. Lo importante es el cruce de los cuadros y no cada uno por separado. Por dentro, la pollería tiene con qué crecer: cuatro canales de venta, cocina propia, ventas que subieron 18 % y un registro digital de cada venta. Sus debilidades son de gestión: precios iguales en todos los canales, producción por experiencia con 7 % de merma, sistemas que no se cruzan y un costo del pollo que no se relaciona con el margen. Por fuera, las amenazas superan a las oportunidades, cinco frente a tres. Del cruce salen siete estrategias y cinco dependen de medir, integrar o pronosticar con datos, que es lo que la solución de BI hace posible.

Tabla 5: Fortalezas

| Código | Fortaleza | Evidencia o fuente |
|---|---|---|
| FOR-01 | Cuatro canales de venta en operación: salón, para llevar, delivery propio por WhatsApp y aplicaciones | Canales del Canvas, sección 1.4 |
| FOR-02 | Cocina y hornos propios, con un equipo de 16 trabajadores | Recursos clave del Canvas y trabajadores declarados, 2026 |
| FOR-03 | Ventas en crecimiento: 18 % más en el último año | Registro de caja de 2025 y 2026 |
| FOR-04 | Comprobantes electrónicos desde 2018, que dejan un registro digital de las ventas | Padrón de contribuyentes, 2026 |

Tabla 6: Debilidades

| Código | Debilidad | Evidencia o fuente |
|---|---|---|
| DEB-01 | Precios iguales en todos los canales, sin considerar la comisión | Lista de precios única de la empresa, 2026 |
| DEB-02 | Producción por turno decidida por experiencia, con una merma de 7 % | Control de producción de cocina, 2026 |
| DEB-03 | Ventas de caja, aplicaciones y WhatsApp registradas en sistemas que no se cruzan | Revisión de las fuentes de datos de la empresa, 2026 |
| DEB-04 | El costo del pollo vivo no se relaciona con el margen ni con los precios de venta | Registro de compras de la empresa, 2026 |

Tabla 7: Oportunidades

| Código | Oportunidad | Evidencia o fuente |
|---|---|---|
| OPO-01 | Herramientas de BI de bajo costo para integrar y analizar los datos | TEC-01 |
| OPO-02 | Demanda de delivery de pollo en crecimiento | SOC-01 |
| OPO-03 | Demanda concentrada en días y horas conocidos, que permite pronosticar la producción | SOC-02 |

Tabla 8: Amenazas

| Código | Amenaza | Evidencia o fuente |
|---|---|---|
| AME-01 | Precio del pollo vivo volátil | ECO-01 |
| AME-02 | Comisiones de 25 % a 30 % de las aplicaciones de delivery | TEC-02 |
| AME-03 | Inflación que eleva los costos de operación | ECO-02 |
| AME-04 | Normas de envases y de datos personales que elevan costos y exigencias | AMB-01, LEG-01 |
| AME-05 | Cadenas de pollerías y otras cadenas de comida que compiten en las mismas aplicaciones | KFC Perú y McDonald's figuran entre las aplicaciones de comida más descargadas, Delgado Tong (2026); entorno competitivo, sección 1.3 |

**Estrategias cruzadas.** Del cruce de los cuadros internos con los externos salen las estrategias que orientan el proyecto. Cinco de las siete dependen de medir, integrar o pronosticar con datos (FO-01, DO-01, DO-02, DA-01 y DA-02), y son las que la solución de BI hace posibles.

Tabla 9: Estrategias cruzadas FO, FA, DO y DA

| Código | Tipo | Estrategia | Combina |
|---|---|---|---|
| FO-01 | FO | Usar un dashboard de BI para identificar los canales y productos que más dejan y reforzar en ellos la venta | FOR-01, OPO-01 |
| FO-02 | FO | Impulsar el delivery propio por WhatsApp para captar la demanda de delivery que crece | FOR-01, OPO-02 |
| FA-01 | FA | Fijar precios diferenciados por canal, apoyados en los canales propios, para compensar las comisiones | FOR-01, AME-02 |
| DO-01 | DO | Integrar caja, aplicaciones y WhatsApp en un modelo de datos con herramientas de BI de bajo costo | DEB-03, OPO-01 |
| DO-02 | DO | Pronosticar la producción por día y turno con el patrón de demanda | DEB-02, OPO-03 |
| DA-01 | DA | Monitorear el precio del pollo vivo y su efecto en el margen para ajustar precios y compras | DEB-04, AME-01 |
| DA-02 | DA | Medir el margen de cada canal después de la comisión para corregir los precios iguales | DEB-01, AME-02 |

## 1.7. Diagrama de la problemática: Ishikawa

El diagrama de causa y efecto organiza por categorías las causas posibles de un problema para distinguir las principales de las secundarias (Ishikawa, 1986). Se usan las seis categorías del método 6M y el efecto es la problemática definida en el brief del proyecto.

**Efecto.** Las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %.

(INCLUIR IMAGEN: Figura 4: Diagrama de Ishikawa. Archivo sugerido: imagenes/ishikawa.html)

**Cómo copiarla.** Abrir [imagenes/ishikawa.html](imagenes/ishikawa.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Ordena por categorías las causas que explican el problema central del negocio. El problema no tiene una sola causa: las ocho se reparten en seis categorías, y las que más pesan nacen dentro del negocio. Dos son de método, porque los precios son iguales en todos los canales y se produce sin pronóstico de demanda. Dos son de medio ambiente, las comisiones de 25 % a 30 % de las aplicaciones y la inflación de 5.25 %, que el negocio no controla y solo puede compensar con mejores decisiones. Las otras cuatro, de mano de obra, materiales, maquinaria y medición, repiten la misma falta: no se mide el margen por canal ni la merma por turno, y los registros no se cruzan.

Tabla 10: Causas del diagrama de Ishikawa

| Código | Categoría | Causa | Evidencia |
|---|---|---|---|
| CAU-01 | Método | Precios iguales en todos los canales, sin considerar la comisión | DEB-01 |
| CAU-02 | Método | No hay un pronóstico de demanda por día y turno: los domingos falta pollo y los martes sobra | DEB-02, OPO-03 |
| CAU-03 | Mano de obra | El jefe de cocina decide cuántos pollos hornear según su experiencia, sin una referencia de datos | DEB-02 |
| CAU-04 | Materiales | El precio del pollo vivo es volátil y no se monitorea | AME-01, DEB-04 |
| CAU-05 | Maquinaria | Los registros de caja, aplicaciones y WhatsApp no están integrados | DEB-03 |
| CAU-06 | Medición | No se mide el margen por canal ni la merma por turno | DEB-01, DEB-02 |
| CAU-07 | Medio ambiente | Las aplicaciones cobran comisiones de 25 % a 30 % de la venta | AME-02 |
| CAU-08 | Medio ambiente | La inflación de 5.25 % eleva los costos de operación | AME-03 |

**Lectura del diagrama.** Las causas de método y de medición (CAU-01, CAU-02 y CAU-06) muestran que se fijan precios y se produce sin datos, y los registros que existen no se cruzan (CAU-05). Las ventas por canal, la producción por turno y el precio del insumo permiten medir estas causas, y la solución de BI los integrará (OE-02, OE-03 y OE-04 del brief).

## 1.8. Problemática central del negocio

**Enunciado.** Pollerías y Parrilladas San Martín vende más, pero gana menos: las ventas crecieron 18 % en el último año y el margen neto cayó de 14 % a 8 %. El dueño y el jefe de cocina deciden sin ver cuánto deja cada canal ni cuánto pollo se pierde por turno.

**Afectados.** El dueño y el jefe de cocina, que deciden precios, producción y compras sin ver la rentabilidad por canal ni la merma.

**Causas principales.** Del diagrama de Ishikawa se priorizan las cuatro causas que más pesan en el margen y que una solución de BI puede medir y corregir con datos.

Tabla 11: Causas principales de la problemática

| Código | Causa principal | Categoría | Evidencia |
|---|---|---|---|
| CAU-01 | Precios iguales en todos los canales, sin considerar la comisión | Método | Las aplicaciones de delivery pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión, según el registro de ventas de 2026 |
| CAU-02 | No hay un pronóstico de demanda por día y turno: los domingos falta pollo y los martes sobra | Método | Merma de 7 % de los pollos preparados frente a 3 % o menos recomendable, según el control de producción de 2026 |
| CAU-04 | El precio del pollo vivo es volátil y no se monitorea | Materiales | El pollo vivo pasó de S/ 6.10 a S/ 6.90 por kilogramo entre el 1 y el 14 de julio de 2026 en Lima Metropolitana (Expreso, 2026) |
| CAU-05 | Los registros de caja, aplicaciones y WhatsApp no están integrados | Maquinaria | Cada canal registra sus ventas en un sistema que no se cruza con los demás, según la revisión de las fuentes de datos de la empresa, 2026 |

**Evidencia.**
- Las aplicaciones de delivery pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión.
- La merma es de 7 % de los pollos preparados, frente a 3 % o menos recomendable; los domingos falta pollo y los martes sobra.
- El pollo vivo pasó de S/ 6.10 a S/ 6.90 por kilogramo entre el 1 y el 14 de julio de 2026 en Lima Metropolitana (Expreso, 2026).

## 1.9. Objetivo general del proyecto

El objetivo general OG-01 responde a la problemática central: dar al dueño la información de rentabilidad por canal y de merma que hoy no tiene. Con ella podrá recuperar el margen neto de 8 % a 12 % mediante decisiones de precio y de producción.

Tabla 12: Objetivo general del proyecto

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | Implementar una solución de BI en Power BI que integre las ventas de todos los canales, la producción por turno y el precio del pollo vivo para recuperar el margen neto | Margen neto | 12 % o más, a seis meses de implantada la solución | Entrega (07-12-2026) | Margen neto global |

## 1.10. Objetivos específicos

Los objetivos específicos desagregan el objetivo general en cinco resultados medibles al cierre del proyecto.

Tabla 13: Objetivos específicos

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | Integrar y depurar las fuentes de ventas (caja, Rappi, PedidosYa y WhatsApp) mediante un proceso ETL en Power Query | Registros que pasan las reglas de calidad | 98 % o más | Entrega (07-12-2026) | OG-01 | Calidad de datos del ETL |
| OE-02 | Medir el margen de contribución por canal y por producto | Canales y productos con margen calculado | 100 % de los canales y productos del periodo | Entrega (07-12-2026) | OG-01 | Margen de contribución por canal y producto |
| OE-03 | Pronosticar la demanda de pollos por día y turno para reducir la merma | Merma sobre los pollos preparados | De 7 % a 3 % o menos | Entrega (07-12-2026) | OG-01 | Porcentaje de merma por turno |
| OE-04 | Monitorear el efecto del precio del pollo vivo en el costo y el margen | Días del periodo con el precio del insumo cruzado con el margen | 100 % de los días | Entrega (07-12-2026) | OG-01 | Precio promedio del pollo vivo por kilogramo |
| OE-05 | Construir un dashboard con KPI, metas y filtros que guíe las decisiones de precio, producción y personal | KPI con meta y semáforo | 100 % de los KPI | Entrega (07-12-2026) | OG-01 | KPI con meta en el dashboard |

**Matriz de articulación.** Cada objetivo específico responde a causas del diagrama de Ishikawa (1.7), se apoya en el análisis PESTEL (1.5) y en la matriz FODA (1.6) y actúa sobre bloques concretos del modelo de negocio.

Tabla 14: Matriz de articulación de los objetivos específicos

| Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador |
|---|---|---|---|---|---|
| OE-01 | CAU-05, CAU-06 | DEB-03, DO-01 | TEC-01, LEG-01 | Actividades clave; Canales | Calidad de datos del ETL |
| OE-02 | CAU-01, CAU-06, CAU-07 | DEB-01, AME-02, FA-01, DA-02 | TEC-02 | Canales; Fuentes de ingresos; Estructura de costos | Margen de contribución por canal y producto |
| OE-03 | CAU-02, CAU-03 | DEB-02, OPO-03, DO-02 | SOC-02 | Actividades clave; Recursos clave | Porcentaje de merma por turno |
| OE-04 | CAU-04, CAU-08 | DEB-04, AME-01, AME-03, DA-01 | ECO-01, ECO-02 | Estructura de costos; Socios clave | Precio promedio del pollo vivo por kilogramo |
| OE-05 | CAU-03, CAU-06 | OPO-01, FO-01, DO-01 | TEC-01 | Propuesta de valor; Actividades clave | KPI con meta en el dashboard |

**Lectura de la matriz.** El primer objetivo resuelve la falta de datos integrados, condición de los demás; el segundo ataca los precios iguales y las comisiones, el tercero la producción sin pronóstico y el cuarto el costo del insumo. Por último, el quinto reúne todo en el dashboard. El capítulo 2 convierte el indicador de cada objetivo en un KPI.

# Capítulo 2: Diseño técnico de solución en Inteligencia de Negocios

Este capítulo describe la solución de Inteligencia de Negocios que responde a la problemática: su arquitectura, las herramientas, el modelo de datos y los indicadores con que se medirán los objetivos. Comprende 2.1 Propuesta de solución en BI, 2.2 Arquitectura de Inteligencia de Negocios, 2.3 Herramientas utilizadas, 2.4 Diseño del modelado de datos: hechos, dimensiones y relaciones y 2.5 Indicadores clave de rendimiento (KPI).

## 2.1. Propuesta de solución en BI

**Decisiones que apoya.**
- Fijar precios diferenciados por canal (OE-02).
- Definir cuántos pollos preparar en cada turno y día de la semana (OE-03).
- Asignar el personal según la franja horaria (OE-05).
- Anticipar compras y ajustar precios ante subidas del pollo vivo (OE-04).

**Usuarios.** El dueño, que decide precios y compras, y el jefe de cocina, que ejecuta la producción de cada turno.

**Respuesta a la problemática.** La solución reúne en un solo modelo las ventas de caja, de Rappi, de PedidosYa y de WhatsApp, la producción por turno y el precio del pollo vivo, que hoy están en registros separados. Con ellos calcula el margen de cada canal y producto después de comisiones (25 % a 30 % en las aplicaciones) y costos, y la merma de cada turno. Así el dueño deja de fijar el mismo precio en todos los canales y la cocina deja de producir sin referencia. Son las causas principales de la caída del margen neto de 14 % a 8 % (punto 1.8), junto con la falta de un registro integrado y el costo del pollo sin monitoreo.

El dashboard responde a cada objetivo específico con componentes concretos de la arquitectura, que se describe en el punto siguiente.

Tabla 15: Componentes de la solución que atienden cada objetivo específico

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-07, CAP-08, CAP-09 | Power Query depura y cruza las fuentes, aplica las reglas de calidad y las deja en un modelo en estrella |
| OE-02 | CAP-09, CAP-10 | El modelo calcula el margen de contribución por canal y producto y el dashboard lo muestra frente a la meta |
| OE-03 | CAP-09, CAP-11 | El modelo cruza lo preparado con lo vendido por turno y el pronóstico estima la demanda por día y turno |
| OE-04 | CAP-06, CAP-09, CAP-10 | El boletín de precios entra al modelo y el dashboard lo cruza con el costo y el margen |
| OE-05 | CAP-10, CAP-12 | El dashboard reúne los KPI con su meta y sus filtros y se publica para el dueño y el jefe de cocina |

## 2.2. Arquitectura de Inteligencia de Negocios

La arquitectura de la solución sigue las cuatro capas de un sistema de inteligencia de negocios. Son las fuentes que generan los datos, el proceso ETL que los extrae, depura y transforma, el almacenamiento donde queda el modelo dimensional y la visualización donde se consulta (Kimball & Ross, 2013). Cada capa tiene componentes con una función definida, y las herramientas que los construyen se detallan en el punto 2.3.

(INCLUIR IMAGEN: Figura 5: Arquitectura de BI. Archivo sugerido: imagenes/arquitectura-bi.html)

**Cómo copiarla.** Abrir [imagenes/arquitectura-bi.html](imagenes/arquitectura-bi.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra cómo viaja el dato desde las fuentes hasta el dashboard en cuatro capas. Hoy los datos están en seis lugares que no se cruzan: la caja, Rappi, PedidosYa, WhatsApp, el control de producción y el boletín de precios. La arquitectura los lleva en un solo sentido por cuatro capas: Power Query los extrae y depura, las reglas de calidad los homologan y todo queda en un único modelo dimensional (CAP-09). De ese modelo salen el dashboard, el pronóstico de demanda y su publicación, de modo que el margen, la merma y el precio del pollo se miden siempre con los mismos datos. Todo se construye con Power BI, sin servidor ni costo adicional, y el dueño y el jefe de cocina lo consultan desde el navegador.

**Lectura de la arquitectura.** El dato viaja desde la caja (CAP-01), las aplicaciones (CAP-02 y CAP-03), WhatsApp (CAP-04), la cocina (CAP-05) y el boletín de precios (CAP-06) hasta un modelo único (CAP-09). De ahí pasa al dashboard (CAP-10), que el dueño consulta antes de decidir precios, producción y compras.

## 2.3. Herramientas utilizadas

Las herramientas (HER-01 a HER-04) se eligieron por su integración con Power BI, por su costo y por el tamaño de los datos del proyecto (Microsoft, s. f.). Todas forman parte del ecosistema de Power BI, de modo que el equipo trabaja con una sola plataforma de punta a punta.

Tabla 16: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | Power Query | ETL | Extraer, depurar, homologar y anexar las seis fuentes y registrar cada paso | Viene integrada en Power BI Desktop, deja cada paso registrado y repetible y es la herramienta que prevé el objetivo OE-01 | Scripts de Python, que exigen más mantenimiento y no se integran con el modelo |
| HER-02 | Modelo semántico de Power BI | Almacenamiento | Guardar el modelo en estrella y sus medidas | El volumen del proyecto, de agosto de 2025 a octubre de 2026 y un solo local, cabe en un modelo por importación y no exige un servidor ni costo adicional | SQL Server Express, que agrega administración sin necesidad para este volumen |
| HER-03 | Power BI Desktop | Visualización | Modelar los datos, escribir las medidas y construir el dashboard con su pronóstico | Es la herramienta de visualización que pide la consigna del proyecto y reúne la preparación, el modelado, las medidas DAX y el pronóstico en un solo programa gratuito (Microsoft, s. f.) | Excel con tablas dinámicas, que limita la interacción entre páginas y los filtros |
| HER-04 | Power BI Service | Visualización | Publicar el dashboard para que el dueño lo consulte desde el navegador | Permite que el dueño y el jefe de cocina vean el dashboard sin instalar el programa de escritorio | Compartir el archivo .pbix, que obliga a abrirlo en un equipo con Power BI Desktop |

## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

El modelo sigue un esquema en estrella con varios hechos que comparten dimensiones, es decir, una constelación de hechos (Kimball & Ross, 2013). Tiene cuatro tablas de hechos y cinco dimensiones, de modo que las ventas, la producción, el precio del insumo y las metas de los KPI se pueden cruzar por fecha, canal y turno.

(INCLUIR IMAGEN: Figura 6: Modelo de datos en estrella. Archivo sugerido: imagenes/modelo-datos.html)

**Cómo copiarla.** Abrir [imagenes/modelo-datos.html](imagenes/modelo-datos.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra las tablas de hechos, las dimensiones y las relaciones sobre las que se calculan los indicadores. Las cuatro tablas de hechos no se unen entre sí: se cruzan a través de las dimensiones que comparten. dCalendario las une a las cuatro, así que un filtro por mes afecta a ventas, producción, precio del pollo y metas a la vez, y dTurno une pedidos con producción para comparar lo preparado con lo vendido. En cambio, canal y producto solo existen en fPedidos, por eso el margen por canal y producto se calcula únicamente desde los pedidos, con la comisión de 25 % a 30 % de las aplicaciones ya descontada. Cada hecho tiene su propio grano, por ejemplo un pedido por día frente a un KPI por mes, y sus medidas no se suman entre tablas distintas.

**Tablas de hechos.** Cada hecho tiene un grano propio y sus medidas se suman, promedian o cuentan a ese nivel.

Tabla 17: Tablas de hechos

| Código | Tabla de hechos | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | fPedidos | Una fila por línea de pedido, canal y día | cantidad (suma); venta_bruta (suma); comision (suma); costo_estimado (suma); costo_operativo (suma); pollos_equivalentes (suma); registro_valido (suma); registro_total (conteo) | fecha_key; producto_key; canal_key; turno_key |
| FCT-02 | fProduccion | Una fila por turno y día | pollos_preparados (suma); pollos_vendidos (suma); pollos_merma (suma) | fecha_key; turno_key |
| FCT-03 | fPrecioInsumo | Una fila por día | precio_kg (promedio); valor_imputado (suma) | fecha_key |
| FCT-04 | fMetaKpi | Una fila por KPI y mes | meta (promedio); valor_real (promedio) | kpi_key; fecha_key |

**Dimensiones.** Las dimensiones se comparten entre los hechos para que los filtros de una página afecten a todos los visuales.

Tabla 18: Dimensiones

| Código | Dimensión | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | dCalendario | fecha_key | fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Año > Mes > Fecha |
| DIM-02 | dProducto | producto_key | producto; categoria | Categoría > Producto |
| DIM-03 | dCanal | canal_key | canal; tipo_canal; comision_pct | — |
| DIM-04 | dTurno | turno_key | turno; hora_inicio; hora_fin | — |
| DIM-05 | dKpi | kpi_key | kpi; objetivo; tiene_meta; frecuencia | — |

**Relaciones.** Todas las relaciones son de varios a uno, desde el hecho hacia la dimensión, y filtran en un solo sentido.

**Lectura del modelo.** Con este modelo se calcula el margen de cada canal y producto por mes, con la comisión de 25 % a 30 % de las aplicaciones ya descontada (FCT-01). Se compara lo preparado con lo vendido en cada turno (FCT-02). También se contrasta el precio del pollo vivo (FCT-03) con el margen de agosto de 2025 a octubre de 2026 y cada KPI con su meta (FCT-04).

## 2.5. Indicadores clave de rendimiento (KPI)

Los indicadores se eligieron con dos criterios: que midan el logro de un objetivo específico y que sostengan una decisión del dueño. Son siete (KPI-01 a KPI-07): cinco llevan el mismo nombre que el indicador de su objetivo en el punto 1.10 (OE-01 a OE-05) y todos se calculan con campos del modelo de datos.

**Definición.** Cada indicador se define con su fórmula, la medida que lo calcula en Power BI y los campos del modelo de los que sale.

Tabla 19: Definición de los KPI

| Código | KPI | Fórmula | Medida propuesta | Origen |
|---|---|---|---|---|
| KPI-01 | Calidad de datos del ETL | Registros válidos entre registros cargados | % Registros válidos | fPedidos.registro_valido; fPedidos.registro_total |
| KPI-02 | Margen de contribución por canal y producto | (Venta bruta menos comisión menos costo estimado) entre venta bruta, por canal y producto | Margen de contribución % | fPedidos.venta_bruta; fPedidos.comision; fPedidos.costo_estimado; dCanal.canal; dProducto.producto |
| KPI-03 | Margen neto global | (Venta bruta menos comisión, costo estimado y costo operativo) entre venta bruta | Margen neto % | fPedidos.venta_bruta; fPedidos.comision; fPedidos.costo_estimado; fPedidos.costo_operativo |
| KPI-04 | Porcentaje de merma por turno | Pollos de merma entre pollos preparados, por turno | % Merma | fProduccion.pollos_merma; fProduccion.pollos_preparados; dTurno.turno |
| KPI-05 | Precisión del pronóstico de demanda | Error porcentual absoluto medio entre los pollos vendidos y los pronosticados por día y turno | Error del pronóstico % | fProduccion.pollos_vendidos; dCalendario.fecha; dTurno.turno |
| KPI-06 | Precio promedio del pollo vivo por kilogramo | Promedio del precio diario por kilogramo en el periodo | Precio pollo vivo | fPrecioInsumo.precio_kg; dCalendario.fecha |
| KPI-07 | KPI con meta en el dashboard | KPI con meta definida entre KPI del dashboard | % KPI con meta | dKpi.kpi_key; dKpi.tiene_meta |

**Gestión.** Cada indicador tiene una meta, una frecuencia de revisión, el objetivo que mide y la decisión que apoya.

Tabla 20: Meta, frecuencia y decisión de cada KPI

| Código | Meta | Frecuencia | Objetivo | Decisión que apoya |
|---|---|---|---|---|
| KPI-01 | 98 % o más | Por carga | OE-01 | Confiar en las cifras del dashboard antes de decidir |
| KPI-02 | Pendiente | Mensual | OE-02 | Fijar precios diferenciados por canal |
| KPI-03 | 12 % o más | Mensual | OE-02 | Fijar precios diferenciados por canal |
| KPI-04 | 3 % o menos | Diaria | OE-03 | Definir cuántos pollos preparar en cada turno y día de la semana |
| KPI-05 | 15 % o menos | Semanal | OE-03 | Definir cuántos pollos preparar en cada turno y día de la semana, y asignar el personal según la franja horaria |
| KPI-06 | Pendiente | Semanal | OE-04 | Anticipar compras y ajustar precios ante subidas del pollo vivo |
| KPI-07 | 100 % | Por carga | OE-05 | Revisar cada decisión del dashboard frente a su meta |

**Lectura de los KPI.** El semáforo del dashboard compara cada indicador con su meta. Si el margen neto (KPI-03) se aleja del 12 % o la merma (KPI-04) supera el 3 %, el dueño sabe qué decisión revisar; hoy el margen neto es de 8 % y la merma, de 7 %. Las metas del margen de contribución (KPI-02) y del precio del pollo vivo (KPI-06) se fijan cuando se conozcan los márgenes reales y la serie completa de precios.

# Capítulo 3: Construcción y calidad del dashboard en Power BI

Este capítulo explica cómo se construyeron el proceso ETL y el dashboard en Power BI, y qué reglas de calidad aseguran que los datos sean confiables. Comprende 3.1 Construcción de la solución ETL y 3.2 Construcción del dashboard en Power BI.

## 3.1. Construcción de la solución ETL

El equipo construyó el ETL con Power Query, dentro de Power BI Desktop, a partir de seis fuentes en archivos CSV y de dos archivos de apoyo (el catálogo de productos y los costos operativos de cada mes). Los datos son generados para el proyecto: se calibraron con las cifras del informe, cubren de agosto de 2025 a octubre de 2026 y traen defectos a propósito (copias duplicadas entre filas, nombres de producto distintos, fechas con formatos mezclados, vacíos, pedidos cancelados y días sin precio) para que el ETL tenga qué corregir.

**Extracción.** Cada fuente se importó con su archivo CSV en codificación UTF-8, sin dejar que Power BI detecte el tipo de las columnas, y su número de filas se anotó antes de transformarla.

Tabla 21: Fuentes extraídas

| Código | Fuente | Archivo | Filas leídas |
|---|---|---|---|
| FUE-01 | Sistema de caja (salón y para llevar) | fue-01-caja.csv | 59134 |
| FUE-02 | Reportes de Rappi | fue-02-rappi.csv | 13448 |
| FUE-03 | Reportes de PedidosYa | fue-03-pedidosya.csv | 9737 |
| FUE-04 | Pedidos por WhatsApp | fue-04-whatsapp.csv | 8978 |
| FUE-05 | Control de producción por turno | fue-05-produccion.csv | 1374 |
| FUE-06 | Boletín de precios de aves de MIDAGRI | fue-06-precios-pollo.csv | 437 |

**Transformación.** Dieciséis pasos llevan las fuentes a las nueve tablas del modelo; el código de cada uno está en el anexo B. Las cuatro fuentes de venta se llevan a un esquema común y se anexan en una sola tabla de pedidos. Los duplicados y los registros inválidos se marcan en lugar de borrarse, de modo que el modelo conserva todas las filas leídas y puede medir cuántas son válidas. El costo estimado de cada línea resulta de la cantidad por los kilos de pollo vivo del producto, por el precio por kilogramo del día, más sus otros costos del catálogo de productos. Luego, el costo operativo de cada mes se reparte entre sus líneas en proporción a la venta del mes. Antes de cargar el modelo, el teléfono del cliente de WhatsApp se reemplaza por un código, porque el análisis solo necesita saber si el cliente se repite y el número identifica a una persona (Ley 29733).

Tabla 22: Pasos del ETL en Power Query

| Código | Paso | Tabla | Resultado |
|---|---|---|---|
| PAS-01 | Crear el parámetro de la ruta de datos y las funciones auxiliares | Consultas de ayuda | Seis consultas de ayuda, sin tablas cargadas |
| PAS-02 | Importar el catálogo, los alias de producto y los costos operativos | Catálogo; Alias; CostosOperativos | Tres consultas de apoyo con los encabezados en la primera fila |
| PAS-03 | Importar y limpiar la caja | FUE-01 | Fuente en el esquema común con las fechas convertidas (REG-01) |
| PAS-04 | Importar y limpiar Rappi | FUE-02 | Fuente en el esquema común, con los cancelados marcados (REG-04) |
| PAS-05 | Importar y limpiar PedidosYa | FUE-03 | Fuente en el esquema común, con la comisión en monto |
| PAS-06 | Importar WhatsApp y reemplazar el teléfono por un código | FUE-04 | Fuente en el esquema común sin datos personales |
| PAS-07 | Anexar las cuatro fuentes de venta | Pedidos_bruto | Una sola tabla con 91 297 filas |
| PAS-08 | Homologar los nombres de producto con el catálogo | Pedidos_homologado | Ninguna fila sin producto del catálogo (REG-02) |
| PAS-09 | Marcar los duplicados y los registros válidos | Pedidos_homologado | 90 623 filas tras los duplicados y 89 888 válidas (REG-03 y REG-04) |
| PAS-10 | Crear el calendario, las dimensiones y las claves | dCalendario; dProducto; dCanal; dTurno; dKpi | Cinco dimensiones con su clave |
| PAS-11 | Armar el precio diario del pollo vivo e imputar los días sin precio | fPrecioInsumo | Un precio por cada día del periodo (REG-06) |
| PAS-12 | Calcular las medidas de los pedidos | fPedidos | Tabla de hechos con ventas, comisión y costos |
| PAS-13 | Construir la producción por turno | fProduccion | Una fila por día y turno |
| PAS-14 | Construir las metas de los KPI | fMetaKpi | Una fila por KPI y mes |
| PAS-15 | Cargar el modelo y crear las relaciones | Todas las del modelo | Nueve relaciones de varios a uno |
| PAS-16 | Verificar los totales contra la hoja de respuestas | fPedidos | Los totales coinciden |

**Reglas de calidad.** Seis reglas tratan los defectos de las fuentes. Las reglas de fecha, de nombre de producto y de vacíos corrigen valores sin cambiar el número de filas; las de duplicados y de registros inválidos las marcan para no contarlas, y la de días sin precio agrega los días que faltaban en la serie de precios.

Tabla 23: Reglas de calidad y su resultado

| Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después |
|---|---|---|---|---|---|---|
| REG-01 | Convertir todas las fechas a un solo formato, leyendo las que tienen barras como día, mes y año | `formato_fecha` | fPedidos | Ninguna fecha queda como texto ni cambia de mes | 91297 | 91297 |
| REG-02 | Homologar el nombre de cada producto contra el catálogo y sus alias | `nombre_producto` | fPedidos | Todo producto coincide con uno de los ocho del catálogo | 91297 | 91297 |
| REG-03 | Marcar las copias duplicadas para no contarlas | `duplicado` | fPedidos | Una sola línea válida por pedido y producto | 91297 | 90623 |
| REG-04 | Marcar los registros sin cantidad o monto y los pedidos cancelados | `registro_invalido` | fPedidos | Toda línea válida tiene cantidad y monto positivos | 90623 | 89888 |
| REG-05 | Completar los vacíos que se pueden deducir: el turno desde la hora y el descuento vacío como cero | `nulo` | fPedidos | Ninguna línea queda sin turno ni sin descuento | 89888 | 89888 |
| REG-06 | Imputar el último precio publicado en los días sin precio y marcarlos | `dia_sin_precio` | fPrecioInsumo | Un precio por cada día del periodo | 437 | 457 |

**Carga.** El modelo en estrella quedó cargado con las cuatro tablas de hechos y las cinco dimensiones del diseño de la sección 2.4, y las relaciones se crearon de varios a uno con filtro en un solo sentido.

Tabla 24: Tablas cargadas al modelo

| Tabla | Filas cargadas |
|---|---|
| fPedidos | 91297 |
| fProduccion | 1366 |
| fPrecioInsumo | 457 |
| fMetaKpi | 105 |
| dCalendario | 457 |
| dProducto | 8 |
| dCanal | 5 |
| dTurno | 3 |
| dKpi | 7 |

**Verificación.** Los totales del modelo cargado coinciden con los de la hoja de respuestas: las ventas, la comisión y las líneas válidas de pedido no tienen diferencias.

**Lectura del ETL.** Con las seis reglas aplicadas, 89 888 de las 91 297 filas de pedidos quedan como válidas, de modo que el porcentaje de registros válidos de los KPI se mide sobre todas las filas leídas y las cifras del dashboard excluyen los duplicados, los cancelados y los registros sin monto.

## 3.2. Construcción del dashboard en Power BI

El dashboard lo consultan el dueño, que decide los precios por canal y las compras, y el jefe de cocina, que decide cuántos pollos preparar en cada turno. Se construyó en Power BI sobre el modelo en estrella de la sección 2.4, con cuatro páginas, una por cada pregunta de negocio que esas decisiones necesitan responder.

**Páginas.** Cada página responde una pregunta con sus visualizaciones y sus filtros, y muestra los KPI que la contestan junto con su meta.

Tabla 25: Páginas del dashboard

| Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI |
|---|---|---|---|---|---|---|
| PAG-01 | Resumen del negocio | ¿Gana el negocio lo que debería y qué indicadores están fuera de su meta? | Dueño | Tarjetas de los KPI con su meta, línea del margen neto mensual contra la meta, columnas apiladas de las ventas por canal y tabla de los KPI contra su meta | Año, mes y canal | KPI-01; KPI-02; KPI-03; KPI-04; KPI-06; KPI-07 |
| PAG-02 | Rentabilidad por canal y producto | ¿Qué canales y productos dejan margen después de la comisión? | Dueño | Barras del margen de contribución por canal, matriz por canal y producto, columnas apiladas al 100 % de la participación de las ventas y línea de la comisión pagada | Año, mes y categoría de producto | KPI-02 |
| PAG-03 | Producción y merma por turno | ¿Cuánto pollo se prepara de más o de menos en cada turno y día? | Jefe de cocina | Columnas de la merma por turno y por día de la semana, columnas de pollos preparados y vendidos y línea de lo vendido contra el pronóstico de referencia | Año, mes y turno | KPI-04; KPI-05 |
| PAG-04 | Precio del pollo vivo y margen | ¿Cómo se mueve el precio del pollo vivo y cómo afecta al margen? | Dueño | Líneas del precio diario del pollo vivo, del margen neto mensual y del precio promedio mensual | Año y mes | KPI-06 |

(INCLUIR IMAGEN: Figura 7: Construcción del dashboard en Power BI. Archivo sugerido: ../../09-dashboard/22-11-2026-18-39-12/capturas/pag-01.png)

**Cómo copiarla.** Abrir [../../09-dashboard/22-11-2026-18-39-12/capturas/pag-01.png](../../09-dashboard/22-11-2026-18-39-12/capturas/pag-01.png) y pegar la imagen en el lugar del marcador.

(INCLUIR IMAGEN: Figura 8: Construcción del dashboard en Power BI. Archivo sugerido: ../../09-dashboard/22-11-2026-18-39-12/capturas/pag-02.png)

**Cómo copiarla.** Abrir [../../09-dashboard/22-11-2026-18-39-12/capturas/pag-02.png](../../09-dashboard/22-11-2026-18-39-12/capturas/pag-02.png) y pegar la imagen en el lugar del marcador.

(INCLUIR IMAGEN: Figura 9: Construcción del dashboard en Power BI. Archivo sugerido: ../../09-dashboard/22-11-2026-18-39-12/capturas/pag-03.png)

**Cómo copiarla.** Abrir [../../09-dashboard/22-11-2026-18-39-12/capturas/pag-03.png](../../09-dashboard/22-11-2026-18-39-12/capturas/pag-03.png) y pegar la imagen en el lugar del marcador.

(INCLUIR IMAGEN: Figura 10: Construcción del dashboard en Power BI. Archivo sugerido: ../../09-dashboard/22-11-2026-18-39-12/capturas/pag-04.png)

**Cómo copiarla.** Abrir [../../09-dashboard/22-11-2026-18-39-12/capturas/pag-04.png](../../09-dashboard/22-11-2026-18-39-12/capturas/pag-04.png) y pegar la imagen en el lugar del marcador.

**Valor real de los KPI.** La tabla compara el valor que mostró el dashboard en octubre de 2026 con la meta de cada indicador.

Tabla 26: Valor real de cada KPI frente a su meta

| Código | KPI | Valor real | Meta | Estado | Página |
|---|---|---|---|---|---|
| KPI-01 | Calidad de datos del ETL | 98,3 % | 98 % o más | Cumple | PAG-01 |
| KPI-02 | Margen de contribución por canal y producto | 54,4 % | Pendiente | Sin meta | PAG-02 |
| KPI-03 | Margen neto global | 8,0 % | 12 % o más | No cumple | PAG-01 |
| KPI-04 | Porcentaje de merma por turno | 6,4 % | 3 % o menos | No cumple | PAG-03 |
| KPI-05 | Precisión del pronóstico de demanda | 28,2 % | 15 % o menos | No cumple | PAG-03 |
| KPI-06 | Precio promedio del pollo vivo por kilogramo | S/ 6,82 | Pendiente | Sin meta | PAG-04 |
| KPI-07 | KPI con meta en el dashboard | 71,4 % | 100 % | No cumple | PAG-01 |

**Lectura del dashboard.** En PAG-01, el margen neto sigue por debajo de su meta y solo la calidad de datos la cumple, de modo que el dueño sabe qué indicador revisar primero. PAG-02 apoya la decisión de fijar precios distintos por canal. En PAG-03, la merma supera el doble de su meta y el pronóstico no alcanza la precisión pedida. PAG-04 permite al dueño ver cuándo anticipar compras.

**Metas pendientes.** KPI-02 y KPI-06 no tienen meta en la sección 2.5: se propone una con su valor real de octubre de 2026 y se registra con 07-make-data-model-kpi-update.

# Capítulo 4: Storytelling con datos

Este capítulo cuenta, con los datos del dashboard, qué está pasando en el negocio y qué decisiones conviene tomar. Comprende 4 Storytelling con datos.

## 4. Storytelling con datos

Los hallazgos de este capítulo se basan en datos generados para el proyecto y medidos por el equipo en el dashboard de Power BI; no describen el negocio real de una empresa. Cada hallazgo parte de un indicador, lo compara con su meta y termina en una decisión del dueño o del jefe de cocina.

**Contexto.** La pollería vende más, sobre todo por las aplicaciones de delivery, pero su margen neto se estrecha. El dueño fija los mismos precios en todos los canales y compra sin ver el efecto del precio del pollo vivo, y el jefe de cocina decide cuántos pollos prepara por experiencia. El dashboard reúne las ventas, la producción y el precio del insumo para que esas decisiones se tomen con datos.

**Hallazgos.** La tabla resume siete hallazgos, uno por indicador, con su objetivo, el valor frente a la meta y la decisión que apoyan; debajo se cuenta cada uno con la captura que lo muestra.

Tabla 27: Hallazgos del dashboard

| Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya |
|---|---|---|---|---|---|---|---|---|
| HLZ-01 | OE-01 | KPI-01 | 98,3 % | 98 % o más | Cumple | pag-01 | Dueño | Confiar en las cifras del dashboard para decidir precios y compras |
| HLZ-02 | OE-02 | KPI-03 | 8,0 % | 12 % o más | No cumple | pag-01 | Dueño | Fijar precios diferenciados por canal para acercar el margen neto a su meta |
| HLZ-03 | OE-02 | KPI-02 | 54,4 % | Pendiente | Sin meta | pag-02 | Dueño | Comparar el margen de cada canal y producto para decidir dónde ajustar el precio |
| HLZ-04 | OE-03 | KPI-04 | 6,4 % | 3 % o menos | No cumple | pag-03 | Jefe de cocina | Ajustar cuántos pollos prepara en cada turno y día de la semana |
| HLZ-05 | OE-03 | KPI-05 | 28,2 % | 15 % o menos | No cumple | pag-03 | Jefe de cocina | Mantener el pronóstico como referencia y no como regla hasta que mejore su precisión |
| HLZ-06 | OE-04 | KPI-06 | S/ 6,82 | Pendiente | Sin meta | pag-04 | Dueño | Anticipar compras cuando el precio del pollo vivo suba |
| HLZ-07 | OE-05 | KPI-07 | 71,4 % | 100 % | No cumple | pag-01 | Dueño | Fijar las metas que faltan para que cada indicador tenga su semáforo |

### HLZ-01. Las cifras del dashboard se pueden usar para decidir

(INCLUIR IMAGEN: Figura 11: Storytelling con datos. Archivo sugerido: ../../10-storytelling/22-11-2026-20-20-29/capturas/pag-01.png)

**Cómo copiarla.** Abrir [../../10-storytelling/22-11-2026-20-20-29/capturas/pag-01.png](../../10-storytelling/22-11-2026-20-20-29/capturas/pag-01.png) y pegar la imagen en el lugar del marcador.

**Qué muestra.** La Figura 7 muestra que el 98,3 % de las filas cargadas de las cuatro fuentes de venta es válido, 0,3 puntos porcentuales por encima de la meta de 98 %. Las filas duplicadas, canceladas o sin monto quedan marcadas y no suman a las ventas.

**Qué decisión apoya.** El dueño puede apoyarse en las demás páginas para decidir precios y compras, sin rehacer las cuentas a mano.

### HLZ-02. El margen neto queda por debajo de lo esperado

**Qué muestra.** Según la Figura 7, el margen neto global es de 8,0 %, 4,0 puntos porcentuales por debajo de la meta de 12 %.

**Qué decisión apoya.** El dueño puede fijar precios distintos según el canal y seguir en la misma página si el margen neto se acerca a su meta.

### HLZ-03. El margen de contribución ya se puede comparar por canal y producto

(INCLUIR IMAGEN: Figura 12: Storytelling con datos. Archivo sugerido: ../../10-storytelling/22-11-2026-20-20-29/capturas/pag-02.png)

**Cómo copiarla.** Abrir [../../10-storytelling/22-11-2026-20-20-29/capturas/pag-02.png](../../10-storytelling/22-11-2026-20-20-29/capturas/pag-02.png) y pegar la imagen en el lugar del marcador.

**Qué muestra.** La Figura 8 muestra un margen de contribución de 54,4 % después de la comisión y del costo estimado. Como el indicador no tiene meta, el dashboard no dice si ese valor es alto o bajo, pero sí permite comparar un canal o un producto con otro.

**Qué decisión apoya.** El dueño puede identificar los canales y productos con menos margen y ajustar su precio, y usar este valor como punto de partida para fijar la meta del indicador.

### HLZ-04. La cocina prepara más pollo del que vende

(INCLUIR IMAGEN: Figura 13: Storytelling con datos. Archivo sugerido: ../../10-storytelling/22-11-2026-20-20-29/capturas/pag-03.png)

**Cómo copiarla.** Abrir [../../10-storytelling/22-11-2026-20-20-29/capturas/pag-03.png](../../10-storytelling/22-11-2026-20-20-29/capturas/pag-03.png) y pegar la imagen en el lugar del marcador.

**Qué muestra.** La Figura 9 muestra una merma de 6,4 %, 3,4 puntos porcentuales por encima de la meta de 3 %. Es más del doble de lo recomendable y se ve turno por turno y día por día.

**Qué decisión apoya.** El jefe de cocina puede ajustar cuántos pollos prepara en cada turno según el día de la semana y comprobar el efecto en la misma página.

### HLZ-05. El pronóstico aún no es lo bastante preciso para guiar la producción

**Qué muestra.** Como se ve en la Figura 9, el error del pronóstico de demanda es de 28,2 %, 13,2 puntos porcentuales por encima de la meta de 15 %.

**Qué decisión apoya.** El jefe de cocina puede usar el pronóstico como referencia junto con su experiencia, y el equipo puede mejorarlo antes de usarlo para asignar el personal por franja horaria.

### HLZ-06. El precio del pollo vivo todavía no tiene una referencia

(INCLUIR IMAGEN: Figura 14: Storytelling con datos. Archivo sugerido: ../../10-storytelling/22-11-2026-20-20-29/capturas/pag-04.png)

**Cómo copiarla.** Abrir [../../10-storytelling/22-11-2026-20-20-29/capturas/pag-04.png](../../10-storytelling/22-11-2026-20-20-29/capturas/pag-04.png) y pegar la imagen en el lugar del marcador.

**Qué muestra.** La Figura 10 muestra un precio promedio de S/ 6,82 por kilogramo de pollo vivo en octubre de 2026. Como el indicador no tiene meta, el dashboard no dice si ese precio es alto o bajo, pero sí lo pone junto al margen neto del mes.

**Qué decisión apoya.** El dueño puede anticipar compras y ajustar precios cuando el precio suba, y usar este valor como punto de partida para fijar la meta del indicador.

### HLZ-07. Dos indicadores del dashboard todavía no tienen meta

**Qué muestra.** En la Figura 7, el 71,4 % de los indicadores del dashboard tiene meta, 28,6 puntos porcentuales menos que la meta de 100 %. Los que faltan son el margen de contribución y el precio del pollo vivo.

**Qué decisión apoya.** El dueño puede fijar esas dos metas con los valores que ya muestra el dashboard, de modo que todo indicador tenga su semáforo.

**Prioridades.** La decisión más urgente es la de producción (HLZ-04), porque la merma queda 3,4 puntos porcentuales por encima de su meta y la cocina puede corregirla sin depender de nadie. Le sigue el precio por canal (HLZ-02), con el margen neto 4,0 puntos porcentuales por debajo de la suya. El pronóstico (HLZ-05) y las metas que faltan (HLZ-03, HLZ-06 y HLZ-07) acompañan esas dos decisiones, y la calidad de los datos (HLZ-01) respalda todas.

**Metas pendientes.** KPI-02 y KPI-06 no tienen meta: se propone con su valor real en 09-make-dashboard y se registra con 07-make-data-model-kpi-update.

# Capítulo 5: Conclusiones, recomendaciones y lecciones aprendidas

Este capítulo cierra el informe con las conclusiones frente a cada objetivo, las recomendaciones para la empresa y las lecciones que deja el proyecto. Comprende 5 Conclusiones, recomendaciones y lecciones aprendidas.

## 5. Conclusiones, recomendaciones y lecciones aprendidas

Este capítulo contrasta lo que midió el dashboard con los objetivos del proyecto. Cada conclusión compara el valor real de su indicador, registrado en el punto 3.2, con la meta fijada en el punto 2.5 para el objetivo que mide en el punto 1.10.

**Conclusiones.** Cada objetivo tiene una conclusión con un estado calculado a partir de sus indicadores; el del objetivo general sale de los estados de los específicos.

Tabla 28: Conclusiones por objetivo

| Código | Objetivo | Estado | Conclusión |
|---|---|---|---|
| CNC-01 | OE-01 | Cumplido | La calidad de datos del ETL quedó en 98,3 %, por encima de la meta de 98 % o más: las fuentes de venta se integraron y depuraron, de modo que las cifras del dashboard se calculan sobre filas válidas. |
| CNC-02 | OE-02 | No cumplido | El margen neto global quedó en 8,0 % frente a la meta de 12 % o más, lo que confirma la caída del margen de la problemática. El margen de contribución por canal y producto ya se mide, pero su meta está pendiente y no se puede concluir su cumplimiento. |
| CNC-03 | OE-03 | No cumplido | La merma por turno fue de 6,4 % frente a la meta de 3 % o menos, y el error del pronóstico de demanda de 28,2 % frente a 15 % o menos: la producción de cada turno todavía no sigue una referencia con la precisión pedida. |
| CNC-04 | OE-04 | Sin meta | El precio promedio del pollo vivo se monitorea en el dashboard junto con el margen, pero su meta está pendiente y no se puede concluir su cumplimiento. |
| CNC-05 | OE-05 | No cumplido | El 71,4 % de los indicadores del dashboard tiene meta, frente a la meta de 100 %: el margen de contribución y el precio del pollo vivo siguen sin ella. |
| CNC-06 | OG-01 | Parcial | Con CNC-01, CNC-02, CNC-03, CNC-04 y CNC-05 el objetivo general se cumplió solo en parte: la solución integra las ventas, la producción y el precio del pollo vivo, pero el margen neto y la merma todavía no alcanzan sus metas. |

**Respaldo.** La tabla repite, por cada objetivo específico, el valor real y la meta de cada indicador que lo mide.

Tabla 29: Respaldo de las conclusiones

| Conclusión | KPI | Valor real | Meta | Estado del KPI |
|---|---|---|---|---|
| CNC-01 | KPI-01 | 98,3 % | 98 % o más | Cumple |
| CNC-02 | KPI-02 | 54,4 % | Pendiente | Sin meta |
| CNC-02 | KPI-03 | 8,0 % | 12 % o más | No cumple |
| CNC-03 | KPI-04 | 6,4 % | 3 % o menos | No cumple |
| CNC-03 | KPI-05 | 28,2 % | 15 % o menos | No cumple |
| CNC-04 | KPI-06 | S/ 6,82 | Pendiente | Sin meta |
| CNC-05 | KPI-07 | 71,4 % | 100 % | No cumple |

**Recomendaciones.** Cada recomendación nombra quién decide y el indicador que mostrará si funcionó; toda conclusión que no se cumplió tiene al menos una.

Tabla 30: Recomendaciones

| Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará |
|---|---|---|---|---|
| REC-01 | CNC-02 | Fijar un precio distinto en las aplicaciones de delivery para compensar su comisión y volver a medir el margen neto. | Dueño | KPI-03 |
| REC-02 | CNC-02 | Fijar la meta del margen de contribución por canal y producto con el valor que ya muestra el dashboard. | Dueño | KPI-02 |
| REC-03 | CNC-03 | Definir cuántos pollos preparar en cada turno y día de la semana a partir de lo vendido, empezando por el turno con más merma. | Jefe de cocina | KPI-04 |
| REC-04 | CNC-03 | Usar el pronóstico como referencia junto con la experiencia de cocina y mejorar su precisión antes de asignar el personal con él. | Jefe de cocina | KPI-05 |
| REC-05 | CNC-04 | Fijar la meta del precio del pollo vivo con la serie de precios del dashboard y anticipar compras cuando suba. | Dueño | KPI-06 |
| REC-06 | CNC-05 | Fijar las dos metas que faltan para que todo indicador tenga su semáforo. | Dueño | KPI-07 |
| REC-07 | CNC-06 | Repetir la medición con los datos propios de la empresa antes de cambiar los precios definitivos. | Dueño | KPI-03 |

**Lecciones aprendidas.** El proceso dejó cuatro aprendizajes.

Tabla 31: Lecciones aprendidas

| Código | Lección | Dónde se vio |
|---|---|---|
| LEC-01 | La calidad de los datos se mide desde la carga: marcar los registros inválidos en lugar de borrarlos permite contar cuántos hay y mostrar su porcentaje en el dashboard. | Punto 3.1 |
| LEC-02 | Una meta pendiente impide concluir un objetivo: conviene fijarla antes de construir el dashboard. | Punto 2.5 |
| LEC-03 | Cada medida del dashboard debe tener su nombre definido en el modelo desde el diseño, para que el código de Power BI y los indicadores usen los mismos términos. | Punto 3.2 |
| LEC-04 | Cada paso del trabajo se apoya en el anterior: un cambio en el modelo de datos obliga a revisar el ETL, el dashboard y las conclusiones. | Punto 2.4 |

**Limitaciones.** Los datos se generaron para el proyecto y se calibraron con las cifras del informe, por lo que los resultados dependen de esa calibración y no describen a una empresa real. Los valores del dashboard corresponden a octubre de 2026 y las metas pendientes limitan lo que se puede concluir sobre dos indicadores.

# Referencias bibliográficas

Aguilar, F. J. (1967). *Scanning the business environment*. Macmillan.

Andina. (2026, 1 de noviembre). INEI: inflación en Lima Metropolitana fue de 0.57 % en octubre de 2026. *Agencia Andina*. https://andina.pe/agencia/noticia-inei-inflacion-lima-metropolitana-fue-057-octubre-2026-1098147.aspx

Congreso de la República del Perú. (2013, 2 de julio). Ley N.° 30056, Ley que modifica diversas leyes para facilitar la inversión, impulsar el desarrollo productivo y el crecimiento empresarial. *Diario Oficial El Peruano*.

Congreso de la República del Perú. (2013, 2 de julio). Ley N.° 30056, Ley que modifica diversas leyes para facilitar la inversión, impulsar el desarrollo productivo y el crecimiento empresarial. *Diario Oficial El Peruano*. https://busquedas.elperuano.pe/dispositivo/NL/956689-1

Congreso de la República del Perú. (2018, 19 de diciembre). Ley N.° 30884, Ley que regula el plástico de un solo uso y los recipientes o envases descartables. *Diario Oficial El Peruano*. https://busquedas.elperuano.pe/dispositivo/NL/1724734-1

Delgado Tong, A. (2026, 1 de abril). Estas son las apps de delivery más utilizadas en Perú: ¿por qué se han expandido tanto? *Infobae*. https://www.infobae.com/peru/2026/04/01/estas-son-las-apps-de-delivery-mas-utilizadas-en-peru-por-que-se-han-expandido-tanto/

El Peruano. (2024, 30 de noviembre). Protección de datos personales: Ejecutivo aprueba nuevo reglamento de la Ley N° 29733. *El Peruano*. https://elperuano.pe/noticia/258993-proteccion-de-datos-personales-ejecutivo-aprueba-nuevo-reglamento-de-la-ley-n-29733

Expreso. (2026). Precio del pollo repunta en julio tras registrar nivel bajo: reportes del Midagri reflejan cambios en mercado avícola. *Expreso*. https://www.expreso.com.pe/economia/precio-del-pollo-repunta-en-julio-tras-registrar-nivel-bajo-reportes-del-midagri-reflejan-cambios-en-mercado-avicola-ministerio-de-desarrollo-agrario-y-riego-noticia/1301534/

Gürel, E., & Tat, M. (2017). SWOT analysis: A theoretical review. *The Journal of International Social Research, 10*(51), 994-1006. https://doi.org/10.17719/jisr.2017.1832

Ishikawa, K. (1986). *Guide to quality control* (2.ª ed.). Asian Productivity Organization.

Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). Wiley.

Microsoft. (s. f.). *Power BI Desktop* [Software]. https://www.microsoft.com/es-es/power-platform/products/power-bi/desktop

Ministerio de Economía y Finanzas. (2025). Decreto Supremo N.° 301-2025-EF, Decreto Supremo que aprueba el valor de la Unidad Impositiva Tributaria durante el año 2026. *Diario Oficial El Peruano*. https://busquedas.elperuano.pe/api/visor_html/2469116-1

Osterwalder, A., & Pigneur, Y. (2010). *Business model generation: A handbook for visionaries, game changers, and challengers*. John Wiley & Sons.

Vera, C. (2026, 25 de octubre). ¿Qué pide Lima por delivery? El pollo lidera, pero estos platos «dan la pelea». *Gestión*. https://gestion.pe/economia/gastronomia-peruana-que-pide-lima-por-delivery-el-pollo-lidera-pero-estos-platos-dan-la-pelea-noticia/

# Anexos

## Anexo A: Diccionario de datos y calidad de datos

Este anexo lista los campos de las seis fuentes y de los dos archivos de apoyo, el origen de cada campo del modelo y el resultado de cada regla de calidad.

Tabla 32: Diccionario de los campos de entrada

| Fuente | Campo | Tipo | Regla de calidad | Destino |
|---|---|---|---|---|
| FUE-01 | ticket_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-01 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-01 | hora | texto | REG-05 | fPedidos.turno_key |
| FUE-01 | turno | texto | REG-05 | dTurno.turno |
| FUE-01 | canal | texto | — | dCanal.canal |
| FUE-01 | producto | texto | REG-02 | dProducto.producto |
| FUE-01 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-01 | precio_unitario | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-01 | descuento | decimal | REG-05 | fPedidos.venta_bruta |
| FUE-01 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-02 | pedido_id | texto | REG-03 | fPedidos.registro_valido |
| FUE-02 | fecha_hora | fecha | REG-01 | dCalendario.fecha |
| FUE-02 | producto | texto | REG-02 | dProducto.producto |
| FUE-02 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-02 | monto | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-02 | comision | decimal | — | fPedidos.comision |
| FUE-02 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-03 | nro_pedido | texto | REG-03 | fPedidos.registro_valido |
| FUE-03 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-03 | item | texto | REG-02 | dProducto.producto |
| FUE-03 | cant | entero | REG-04 | fPedidos.cantidad |
| FUE-03 | total | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-03 | comision_pct | decimal | — | fPedidos.comision |
| FUE-03 | estado | texto | REG-04 | fPedidos.registro_valido |
| FUE-04 | pedido | texto | REG-03 | fPedidos.registro_valido |
| FUE-04 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-04 | telefono | texto | — | — |
| FUE-04 | producto | texto | REG-02 | dProducto.producto |
| FUE-04 | cantidad | entero | REG-04 | fPedidos.cantidad |
| FUE-04 | monto | decimal | REG-04 | fPedidos.venta_bruta |
| FUE-04 | tipo_entrega | texto | — | dCanal.canal |
| FUE-05 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-05 | turno | texto | REG-03 | dTurno.turno |
| FUE-05 | pollos_preparados | entero | REG-04 | fProduccion.pollos_preparados |
| FUE-05 | pollos_vendidos | entero | REG-04 | fProduccion.pollos_vendidos |
| FUE-05 | pollos_merma | entero | — | fProduccion.pollos_merma |
| FUE-05 | responsable | texto | REG-05 | — |
| FUE-06 | fecha | fecha | REG-01 | dCalendario.fecha |
| FUE-06 | precio_kg | decimal | REG-06 | fPrecioInsumo.precio_kg |
| Apoyo: catálogo de productos | producto | texto | REG-02 | dProducto.producto |
| Apoyo: catálogo de productos | categoria | texto | — | dProducto.categoria |
| Apoyo: catálogo de productos | precio_lista | decimal | — | — |
| Apoyo: catálogo de productos | pollos_equivalentes | decimal | — | fPedidos.pollos_equivalentes |
| Apoyo: catálogo de productos | kg_pollo_vivo | decimal | — | fPedidos.costo_estimado |
| Apoyo: catálogo de productos | costo_otros | decimal | — | fPedidos.costo_estimado |
| Apoyo: catálogo de productos | alias | texto | REG-02 | dProducto.producto |
| Apoyo: costos operativos | mes | texto | — | dCalendario.mes |
| Apoyo: costos operativos | planilla | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | alquiler | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | servicios | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | otros | decimal | — | fPedidos.costo_operativo |
| Apoyo: costos operativos | total | decimal | — | fPedidos.costo_operativo |

Tabla 33: Origen de los campos del modelo

| Tabla | Campo | Origen |
|---|---|---|
| fPedidos | fecha_key; producto_key; canal_key; turno_key | Cálculo: clave sustituta que se busca en cada dimensión con la fecha, el producto homologado, el canal y el turno de la fuente |
| fPedidos | cantidad | FUE-01.cantidad; FUE-02.cantidad; FUE-03.cant; FUE-04.cantidad |
| fPedidos | venta_bruta | FUE-01.precio_unitario; FUE-01.descuento; FUE-02.monto; FUE-03.total; FUE-04.monto |
| fPedidos | comision | FUE-02.comision; FUE-03.comision_pct; Cálculo: total por el porcentaje de comisión entre cien en PedidosYa |
| fPedidos | costo_estimado | apoyo-catalogo-productos.kg_pollo_vivo; apoyo-catalogo-productos.costo_otros; FUE-06.precio_kg; Cálculo: cantidad por los kilos de pollo vivo por el precio del día más otros costos |
| fPedidos | costo_operativo | apoyo-costos-operativos.total; Cálculo: total del mes repartido en proporción a la venta del mes |
| fPedidos | pollos_equivalentes | apoyo-catalogo-productos.pollos_equivalentes |
| fPedidos | registro_valido; registro_total | Cálculo: uno si la línea no es duplicada ni inválida y uno por cada fila leída |
| fProduccion | fecha_key; turno_key | Cálculo: clave sustituta que se busca en dCalendario y dTurno |
| fProduccion | pollos_preparados; pollos_vendidos; pollos_merma | FUE-05.pollos_preparados; FUE-05.pollos_vendidos; FUE-05.pollos_merma |
| fPrecioInsumo | fecha_key | Cálculo: clave sustituta que se busca en dCalendario |
| fPrecioInsumo | precio_kg | FUE-06.precio_kg; Cálculo: último precio publicado en los días sin precio |
| fPrecioInsumo | valor_imputado | Cálculo: uno si el día no tenía precio |
| fMetaKpi | kpi_key; fecha_key | Cálculo: clave de dKpi y primer día de cada mes |
| fMetaKpi | meta; valor_real | Cálculo: metas de la sección 2.5 y medidas del dashboard |
| dCalendario | fecha_key; fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Cálculo: una fila por cada día del periodo y lista de feriados |
| dProducto | producto_key; producto; categoria | apoyo-catalogo-productos.producto; apoyo-catalogo-productos.categoria; Cálculo: número de fila como clave |
| dCanal | canal_key; canal; tipo_canal; comision_pct | FUE-01.canal; Cálculo: lista de canales con su tipo y su comisión de 30 % en Rappi y 25 % en PedidosYa |
| dTurno | turno_key; turno; hora_inicio; hora_fin | FUE-05.turno; Cálculo: horario de cada turno |
| dKpi | kpi_key; kpi; objetivo; tiene_meta; frecuencia | Cálculo: KPI de la sección 2.5 |

Tabla 34: Resultado de las reglas de calidad

| Código | Filas antes | Filas después | Diferencia |
|---|---|---|---|
| REG-01 | 91297 | 91297 | 0 |
| REG-02 | 91297 | 91297 | 0 |
| REG-03 | 91297 | 90623 | -674 |
| REG-04 | 90623 | 89888 | -735 |
| REG-05 | 89888 | 89888 | 0 |
| REG-06 | 437 | 457 | 20 |

## Anexo B: Scripts del ETL

Este anexo reúne el código de Power Query y DAX de cada paso de la sección 3.1, en el orden en que se ejecuta.

**PAS-01.** Crear el parámetro de la ruta de datos y las funciones auxiliares

```m
(archivo as text) as table =>
let
    Origen = Csv.Document(File.Contents(RutaDatos & archivo), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

```m
(t as nullable text) as nullable date =>
let
    s = Text.Trim(Text.Start(t ?? "", 10))
in
    if s = "" then null
    else if Text.Contains(s, "/") then
        try Date.FromText(s, [Format = "dd/MM/yyyy", Culture = "es-PE"]) otherwise null
    else
        try Date.FromText(s, [Format = "yyyy-MM-dd", Culture = "en-US"]) otherwise null
```

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? "")
in
    if s = "" then null else try Number.FromText(s, "en-US") otherwise null
```

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? ""),
    h = if Text.Contains(s, " ") then Text.AfterDelimiter(s, " ", {0, RelativePosition.FromEnd}) else s
in
    if Text.Length(h) >= 4 and Text.Middle(h, 2, 1) = ":" then try Number.FromText(Text.Start(h, 2), "en-US") otherwise null else null
```

```m
(h as nullable number) as text =>
    if h = null then "Sin hora"
    else if h >= 11 and h < 15 then "Mañana"
    else if h >= 15 and h < 19 then "Tarde"
    else if h >= 19 and h < 23 then "Noche"
    else "Fuera de turno"
```

**PAS-02.** Importar el catálogo, los alias de producto y los costos operativos

```m
// Consulta Catalogo
let
    Enc = LeerCsv("apoyo-catalogo-productos.csv"),
    Tipos = Table.TransformColumnTypes(Enc, {{"precio_lista", type number}, {"pollos_equivalentes", type number},
                                            {"kg_pollo_vivo", type number}, {"costo_otros", type number}}, "en-US")
in
    Tipos
```

```m
// Consulta Alias
let
    ConAlias = Table.AddColumn(Catalogo, "nombre_fuente", each Text.Split([alias], "|") & {[producto]}, type list),
    Expandida = Table.ExpandListColumn(ConAlias, "nombre_fuente"),
    Alias = Table.SelectColumns(Expandida, {"nombre_fuente", "producto"})
in
    Alias
```

```m
// Consulta CostosOperativos (el costo del local de cada mes)
let
    Enc = LeerCsv("apoyo-costos-operativos.csv"),
    Tipos = Table.TransformColumnTypes(Enc, {{"planilla", type number}, {"alquiler", type number}, {"servicios", type number},
                                            {"otros", type number}, {"total", type number}}, "en-US")
in
    Tipos
```

**PAS-03.** Importar y limpiar la caja

```m
let
    Origen = LeerCsv("fue-01-caja.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                precio = NumTexto(f[precio_unitario]),
                dscto = NumTexto(f[descuento]) ?? 0,
                invalido = (cant = null) or (cant <= 0) or (precio = null),
                h = HoraTexto(f[hora])
            in
                [fuente = "FUE-01", pedido = f[ticket_id], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = f[canal], producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else Number.Round(cant * precio - dscto, 2), comision = 0,
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-04.** Importar y limpiar Rappi

```m
let
    Origen = LeerCsv("fue-02-rappi.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (monto_n = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha_hora])
            in
                [fuente = "FUE-02", pedido = f[pedido_id], fecha = FechaTexto(f[fecha_hora]), hora = h, turno = TurnoDeHora(h),
                 canal = "Rappi", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n,
                 comision = if invalido then 0 else (NumTexto(f[comision]) ?? 0),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-05.** Importar y limpiar PedidosYa

```m
let
    Origen = LeerCsv("fue-03-pedidosya.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cant]),
                total = NumTexto(f[total]),
                pct = NumTexto(f[comision_pct]) ?? 0,
                invalido = (total = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-03", pedido = f[nro_pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "PedidosYa", producto_fuente = f[item], cantidad = cant ?? 0,
                 monto = if invalido then 0 else total,
                 comision = if invalido then 0 else Number.Round(total * pct / 100, 2),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```

**PAS-06.** Importar WhatsApp y reemplazar el teléfono por un código

```m
let
    Origen = LeerCsv("fue-04-whatsapp.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (cant = null) or (cant <= 0) or (monto_n = null),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-04", pedido = f[pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "WhatsApp", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n, comision = 0,
                 es_invalido = invalido, telefono = f[telefono]]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, telefono = nullable text])
in
    Filas
```

```m
// Consulta Clientes
let
    Distintos = Table.Distinct(Table.SelectColumns(WhatsApp, {"telefono"})),
    Indice = Table.AddIndexColumn(Distintos, "n", 1, 1, Int64.Type),
    Codigo = Table.AddColumn(Indice, "cliente_id", each "C-" & Text.PadStart(Text.From([n]), 4, "0"), type text)
in
    Codigo
```

```m
// Al final de la consulta WhatsApp: reemplaza telefono por cliente_id
    Unido = Table.NestedJoin(Filas, {"telefono"}, Clientes, {"telefono"}, "c", JoinKind.LeftOuter),
    Anonimo = Table.ExpandTableColumn(Unido, "c", {"cliente_id"}),
    Resultado = Table.RemoveColumns(Anonimo, {"telefono"})
```

**PAS-07.** Anexar las cuatro fuentes de venta

```m
// Consulta Pedidos_bruto
let
    Union = Table.Combine({Caja, Rappi, PedidosYa, WhatsApp_anonimo})
in
    Union
```

**PAS-08.** Homologar los nombres de producto con el catálogo

```m
// Consulta Pedidos_homologado (usa la consulta Alias del PAS-02)
let
    Cruce = Table.NestedJoin(Pedidos_bruto, {"producto_fuente"}, Alias, {"nombre_fuente"}, "a", JoinKind.LeftOuter),
    Producto = Table.ExpandTableColumn(Cruce, "a", {"producto"})
in
    Producto
```

**PAS-09.** Marcar los duplicados y los registros válidos

```m
// Consulta Pedidos_marcado
let
    Clave = Table.AddColumn(Pedidos_homologado, "clave", each [pedido] & "|" & [producto], type text),
    Grupos = Table.Group(Clave, {"clave"}, {{"filas", each Table.AddIndexColumn(_, "ord", 0, 1, Int64.Type), type table}}),
    Planas = Table.ExpandTableColumn(Grupos, "filas", List.RemoveItems(Table.ColumnNames(Clave), {"clave"}) & {"ord"}),
    Duplicado = Table.AddColumn(Planas, "es_duplicado", each [ord] > 0, type logical),
    Valido = Table.AddColumn(Duplicado, "registro_valido", each if [es_duplicado] or [es_invalido] then 0 else 1, Int64.Type)
in
    Valido
```

**PAS-10.** Crear el calendario, las dimensiones y las claves

```m
// Consulta Feriados (lista de referencia: ajústala con el calendario oficial)
{ #date(2025, 8, 30), #date(2025, 10, 8), #date(2025, 11, 1), #date(2025, 12, 8), #date(2025, 12, 25), #date(2026, 1, 1), #date(2026, 4, 2), #date(2026, 4, 3), #date(2026, 5, 1), #date(2026, 6, 29), #date(2026, 7, 28), #date(2026, 7, 29), #date(2026, 8, 30), #date(2026, 10, 8) }
```

```m
// Consulta dCalendario
let
    Inicio = #date(2025, 8, 1),
    Fin = #date(2026, 10, 31),
    Dias = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),
    Tabla = Table.FromList(Dias, Splitter.SplitByNothing(), {"fecha"}, null, ExtraValues.Error),
    Tipada = Table.TransformColumnTypes(Tabla, {{"fecha", type date}}),
    Clave = Table.AddColumn(Tipada, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    Anio = Table.AddColumn(Clave, "anio", each Date.Year([fecha]), Int64.Type),
    Mes = Table.AddColumn(Anio, "mes", each Date.Month([fecha]), Int64.Type),
    NombreMes = Table.AddColumn(Mes, "nombre_mes", each {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"}{Date.Month([fecha]) - 1}, type text),
    DiaSemana = Table.AddColumn(NombreMes, "dia_semana", each {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"}{Date.DayOfWeek([fecha], Day.Monday)}, type text),
    AnioMes = Table.AddColumn(DiaSemana, "anio_mes", each Date.Year([fecha]) * 100 + Date.Month([fecha]), Int64.Type),
    MesAnio = Table.AddColumn(AnioMes, "mes_anio", each {"ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"}{Date.Month([fecha]) - 1} & " " & Text.End(Text.From(Date.Year([fecha])), 2), type text),
    Feriado = Table.AddColumn(MesAnio, "es_feriado", each List.Contains(Feriados, [fecha]), type logical)
in
    Feriado
```

```m
// Consulta dProducto
let
    Cols = Table.SelectColumns(Catalogo, {"producto", "categoria"}),
    Clave = Table.AddIndexColumn(Cols, "producto_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dCanal
let
    Datos = #table(type table [canal = text, tipo_canal = text, comision_pct = number],
        {{"Salón", "Presencial", 0}, {"Para llevar", "Presencial", 0}, {"WhatsApp", "Delivery propio", 0}, {"Rappi", "Aplicación", 30}, {"PedidosYa", "Aplicación", 25}}),
    Clave = Table.AddIndexColumn(Datos, "canal_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dTurno
let
    Datos = #table(type table [turno = text, hora_inicio = time, hora_fin = time],
        {{"Mañana", #time(11, 0, 0), #time(15, 0, 0)}, {"Tarde", #time(15, 0, 0), #time(19, 0, 0)}, {"Noche", #time(19, 0, 0), #time(23, 0, 0)}}),
    Clave = Table.AddIndexColumn(Datos, "turno_key", 1, 1, Int64.Type)
in
    Clave
```

```m
// Consulta dKpi: los indicadores de 2.5
let
    Datos = #table(type table [kpi = text, objetivo = text, tiene_meta = logical, frecuencia = text],
        {{"Calidad de datos del ETL", "OE-01", true, "Por carga"},
         {"Margen de contribución por canal y producto", "OE-02", false, "Mensual"},
         {"Margen neto global", "OE-02", true, "Mensual"},
         {"Porcentaje de merma por turno", "OE-03", true, "Diaria"},
         {"Precisión del pronóstico de demanda", "OE-03", true, "Semanal"},
         {"Precio promedio del pollo vivo por kilogramo", "OE-04", false, "Semanal"},
         {"KPI con meta en el dashboard", "OE-05", true, "Por carga"}}),
    Clave = Table.AddIndexColumn(Datos, "kpi_key", 1, 1, Int64.Type)
in
    Clave
```

**PAS-11.** Armar el precio diario del pollo vivo e imputar los días sin precio

```m
// Consulta PrecioDia (de ella sale fPrecioInsumo)
let
    Origen = LeerCsv("fue-06-precios-pollo.csv"),
    Publicado = Table.FromRecords(
        Table.TransformRows(Origen, (f) => [fecha = FechaTexto(f[fecha]), precio_kg = NumTexto(f[precio_kg])]),
        type table [fecha = date, precio_kg = nullable number]),
    Dias = Table.SelectColumns(dCalendario, {"fecha"}),
    Cruce = Table.NestedJoin(Dias, {"fecha"}, Publicado, {"fecha"}, "p", JoinKind.LeftOuter),
    Precio = Table.ExpandTableColumn(Cruce, "p", {"precio_kg"}),
    Orden = Table.Sort(Precio, {{"fecha", Order.Ascending}}),
    Marca = Table.AddColumn(Orden, "valor_imputado", each if [precio_kg] = null then 1 else 0, Int64.Type),
    Relleno = Table.FillDown(Marca, {"precio_kg"}),
    Tipos = Table.TransformColumnTypes(Relleno, {{"precio_kg", type number}})
in
    Tipos
```

**PAS-12.** Calcular las medidas de los pedidos

```m
// Consulta fPedidos
let
    // 1. Catálogo (equivalentes, kilos de pollo y otros insumos) y precio del pollo del día
    ConCat = Table.NestedJoin(Pedidos_marcado, {"producto"}, Catalogo, {"producto"}, "c", JoinKind.LeftOuter),
    ExpCat = Table.ExpandTableColumn(ConCat, "c", {"pollos_equivalentes", "kg_pollo_vivo", "costo_otros"}, {"eq", "kg", "otros"}),
    ConPrecio = Table.NestedJoin(ExpCat, {"fecha"}, PrecioDia, {"fecha"}, "p", JoinKind.LeftOuter),
    ExpPrecio = Table.ExpandTableColumn(ConPrecio, "p", {"precio_kg"}),
    // 2. Mes de la venta y venta válida de cada mes (para repartir el costo operativo)
    Mes = Table.AddColumn(ExpPrecio, "mes", each Date.ToText([fecha], [Format = "yyyy-MM", Culture = "en-US"]), type text),
    Venta = Table.AddColumn(Mes, "venta_bruta", each [monto] * [registro_valido], type number),
    VentaMes = Table.Group(Venta, {"mes"}, {{"venta_mes", each List.Sum([venta_bruta]), type number}}),
    ConMes = Table.NestedJoin(Venta, {"mes"}, VentaMes, {"mes"}, "vm", JoinKind.LeftOuter),
    ExpMes = Table.ExpandTableColumn(ConMes, "vm", {"venta_mes"}),
    ConOper = Table.NestedJoin(ExpMes, {"mes"}, CostosOperativos, {"mes"}, "co", JoinKind.LeftOuter),
    ExpOper = Table.ExpandTableColumn(ConOper, "co", {"total"}, {"total_mes"}),
    // 3. Medidas por línea (0 si el registro no es válido)
    Comision = Table.AddColumn(ExpOper, "comision_v", each [comision] * [registro_valido], type number),
    Cantidad = Table.AddColumn(Comision, "cantidad_v", each [cantidad] * [registro_valido], type number),
    Equivalentes = Table.AddColumn(Cantidad, "pollos_equivalentes", each [cantidad] * [eq] * [registro_valido], type number),
    CostoEst = Table.AddColumn(Equivalentes, "costo_estimado", each [registro_valido] * [cantidad] * ([kg] * [precio_kg] + [otros]), type number),
    CostoOp = Table.AddColumn(CostoEst, "costo_operativo", each if [venta_mes] = 0 then 0 else [total_mes] * [venta_bruta] / [venta_mes], type number),
    Total = Table.AddColumn(CostoOp, "registro_total", each 1, Int64.Type),
    // 4. Claves hacia las dimensiones
    KFecha = Table.AddColumn(Total, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KProd = Table.NestedJoin(KFecha, {"producto"}, dProducto, {"producto"}, "d1", JoinKind.LeftOuter),
    KProd2 = Table.ExpandTableColumn(KProd, "d1", {"producto_key"}),
    KCanal = Table.NestedJoin(KProd2, {"canal"}, dCanal, {"canal"}, "d2", JoinKind.LeftOuter),
    KCanal2 = Table.ExpandTableColumn(KCanal, "d2", {"canal_key"}),
    KTurno = Table.NestedJoin(KCanal2, {"turno"}, dTurno, {"turno"}, "d3", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "d3", {"turno_key"}),
    // 5. Solo las columnas del modelo
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "producto_key", "canal_key", "turno_key", "cantidad_v", "venta_bruta", "comision_v",
                                        "costo_estimado", "costo_operativo", "pollos_equivalentes", "registro_valido", "registro_total"}),
    Nombres = Table.RenameColumns(Sel, {{"cantidad_v", "cantidad"}, {"comision_v", "comision"}})
in
    Nombres
```

**PAS-13.** Construir la producción por turno

```m
// Consulta fProduccion
let
    Origen = LeerCsv("fue-05-produccion.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                prep = NumTexto(f[pollos_preparados]),
                ven = NumTexto(f[pollos_vendidos]),
                mer = NumTexto(f[pollos_merma])
            in
                [fecha = FechaTexto(f[fecha]), turno = f[turno], pollos_preparados = prep, pollos_vendidos = ven, pollos_merma = mer,
                 es_invalido = (prep = null) or (ven = null) or (ven > prep)]),
        type table [fecha = nullable date, turno = text, pollos_preparados = nullable number, pollos_vendidos = nullable number,
                    pollos_merma = nullable number, es_invalido = logical]),
    SinCopias = Table.Distinct(Filas, {"fecha", "turno"}),
    Validas = Table.SelectRows(SinCopias, each not [es_invalido]),
    KFecha = Table.AddColumn(Validas, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KTurno = Table.NestedJoin(KFecha, {"turno"}, dTurno, {"turno"}, "t", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "t", {"turno_key"}),
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "turno_key", "pollos_preparados", "pollos_vendidos", "pollos_merma"})
in
    Sel
```

**PAS-14.** Construir las metas de los KPI

```m
// Consulta fMetaKpi
let
    Meses = List.Transform({0..14}, each Date.AddMonths(#date(2025, 8, 1), _)),
    Metas = #table(type table [kpi_key = Int64.Type, meta = nullable number], {{1, 98.0}, {2, null}, {3, 12.0}, {4, 3.0}, {5, 15.0}, {6, null}, {7, 100.0}}),
    Cruce = Table.AddColumn(Metas, "fecha", each Meses, type list),
    Expandida = Table.ExpandListColumn(Cruce, "fecha"),
    Clave = Table.AddColumn(Expandida, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + 1, Int64.Type),
    Real = Table.AddColumn(Clave, "valor_real", each null, type nullable number),
    Sel = Table.SelectColumns(Real, {"kpi_key", "fecha_key", "meta", "valor_real"})
in
    Sel
```

**PAS-15.** Cargar el modelo y crear las relaciones

1. En Inicio, elegir Cerrar y aplicar, con solo las nueve tablas del modelo habilitadas para la carga.
2. En la vista de modelo, crear las nueve relaciones de varios a uno y de un solo sentido: fPedidos con dCalendario, dProducto, dCanal y dTurno; fProduccion con dCalendario y dTurno; fPrecioInsumo con dCalendario; fMetaKpi con dKpi y dCalendario.
3. Marcar dCalendario como tabla de fechas con la columna fecha y ordenar nombre_mes por mes.

**PAS-16.** Verificar los totales contra la hoja de respuestas

```dax
Ventas = SUM(fPedidos[venta_bruta])
Comisión = SUM(fPedidos[comision])
Costo estimado = SUM(fPedidos[costo_estimado])
Costo operativo = SUM(fPedidos[costo_operativo])
Margen neto % = DIVIDE([Ventas] - [Comisión] - [Costo estimado] - [Costo operativo], [Ventas])
Filas leídas = SUM(fPedidos[registro_total])
Filas válidas = SUM(fPedidos[registro_valido])
```

## Anexo C: Medidas y cálculos del dashboard

El dashboard usa 17 medidas: las base, que suman o promedian un campo de los hechos, y las de KPI, que se apoyan en ellas. Se escribieron y probaron en Power BI.

Tabla 35: Medidas del dashboard

| Código | Medida | Tipo | KPI | Tablas y campos |
|---|---|---|---|---|
| MED-01 | Venta bruta | Medida |  | fPedidos |
| MED-02 | Comisión pagada | Medida |  | fPedidos |
| MED-03 | Costo estimado | Medida |  | fPedidos |
| MED-04 | Costo operativo | Medida |  | fPedidos |
| MED-05 | Margen de contribución % | Medida | KPI-02 | fPedidos |
| MED-06 | Margen neto % | Medida | KPI-03 | fPedidos |
| MED-07 | % Registros válidos | Medida | KPI-01 | fPedidos |
| MED-08 | Pollos preparados | Medida |  | fProduccion |
| MED-09 | Pollos vendidos | Medida |  | fProduccion |
| MED-10 | Pollos de merma | Medida |  | fProduccion |
| MED-11 | % Merma | Medida | KPI-04 | fProduccion |
| MED-12 | Precio pollo vivo | Medida | KPI-06 | fPrecioInsumo |
| MED-13 | Pronóstico de referencia | Medida |  | fProduccion; dCalendario; dTurno |
| MED-14 | Error del pronóstico % | Medida | KPI-05 | fProduccion; dCalendario; dTurno |
| MED-15 | Participación de ventas % | Medida |  | fPedidos; dCanal |
| MED-16 | % KPI con meta | Medida | KPI-07 | dKpi |
| MED-17 | Meta del KPI | Medida |  | fMetaKpi; dKpi |

#### MED-01. Venta bruta

```dax
SUM ( fPedidos[venta_bruta] )
```

#### MED-02. Comisión pagada

```dax
SUM ( fPedidos[comision] )
```

#### MED-03. Costo estimado

```dax
SUM ( fPedidos[costo_estimado] )
```

#### MED-04. Costo operativo

```dax
SUM ( fPedidos[costo_operativo] )
```

#### MED-05. Margen de contribución %

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado], [Venta bruta] )
```

#### MED-06. Margen neto %

```dax
DIVIDE ( [Venta bruta] - [Comisión pagada] - [Costo estimado] - [Costo operativo], [Venta bruta] )
```

#### MED-07. % Registros válidos

```dax
DIVIDE ( SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] ) )
```

#### MED-08. Pollos preparados

```dax
SUM ( fProduccion[pollos_preparados] )
```

#### MED-09. Pollos vendidos

```dax
SUM ( fProduccion[pollos_vendidos] )
```

#### MED-10. Pollos de merma

```dax
SUM ( fProduccion[pollos_merma] )
```

#### MED-11. % Merma

```dax
DIVIDE ( [Pollos de merma], [Pollos preparados] )
```

#### MED-12. Precio pollo vivo

```dax
AVERAGE ( fPrecioInsumo[precio_kg] )
```

#### MED-13. Pronóstico de referencia

```dax
VAR fechaActual = MAX ( dCalendario[fecha] )
VAR diaSemana = WEEKDAY ( fechaActual, 2 )
VAR anteriores =
    TOPN (
        4,
        FILTER ( ALL ( dCalendario ), dCalendario[fecha] < fechaActual && WEEKDAY ( dCalendario[fecha], 2 ) = diaSemana ),
        dCalendario[fecha], DESC
    )
RETURN
    AVERAGEX ( anteriores, CALCULATE ( [Pollos vendidos] ) )
```

#### MED-14. Error del pronóstico %

```dax
AVERAGEX (
    CROSSJOIN ( VALUES ( dCalendario[fecha] ), VALUES ( dTurno[turno] ) ),
    IF ( NOT ISBLANK ( [Pronóstico de referencia] ) && [Pollos vendidos] > 0,
        DIVIDE ( ABS ( [Pollos vendidos] - [Pronóstico de referencia] ), [Pollos vendidos] ) )
)
```

#### MED-15. Participación de ventas %

```dax
DIVIDE ( [Venta bruta], CALCULATE ( [Venta bruta], ALL ( dCanal[canal] ) ) )
```

#### MED-16. % KPI con meta

```dax
DIVIDE ( CALCULATE ( COUNTROWS ( dKpi ), dKpi[tiene_meta] = TRUE () ), COUNTROWS ( dKpi ) )
```

#### MED-17. Meta del KPI

```dax
AVERAGE ( fMetaKpi[meta] )
```

## Anexo D: Especificación y capturas del dashboard

El dashboard tiene cuatro páginas. Cada una se describe aquí con sus visuales y sus filtros; la captura de cada página está en la sección 3.2.

#### PAG-01. Resumen del negocio

**Descripción.** Reúne los siete KPI con su meta, la evolución mensual del margen neto y las ventas de cada canal. Se lee de arriba abajo: primero qué indicadores están fuera de su meta y después cuánto y desde cuándo. Apoya la decisión del dueño de qué indicador atacar primero. La captura de esta página está en la sección 3.2.

**Visuales.**
- Tarjetas: valor del mes de cada KPI frente a su meta, con su estado.
- Línea: margen neto mensual contra la meta.
- Columnas apiladas: ventas mensuales por canal.
- Tabla: los KPI del dashboard contra su meta.

**Filtros.** Año, mes y canal.

#### PAG-02. Rentabilidad por canal y producto

**Descripción.** Compara el margen de contribución de cada canal y producto después de la comisión, la participación de cada canal en las ventas y la comisión pagada. Se lee comparando las barras: el canal con menos margen es el candidato a un precio distinto. Apoya la decisión de fijar precios diferenciados por canal. La captura de esta página está en la sección 3.2.

**Visuales.**
- Barras: margen de contribución por canal.
- Matriz: margen de contribución por canal y producto.
- Columnas apiladas al 100 %: participación de las ventas por canal.
- Línea: comisión pagada por mes.

**Filtros.** Año, mes y categoría de producto.

#### PAG-03. Producción y merma por turno

**Descripción.** Muestra cuántos pollos se preparan de más en cada turno y día de la semana y cómo se compara lo vendido con el pronóstico de referencia. Se lee turno por turno y día por día contra la línea de la meta. Apoya la decisión del jefe de cocina de cuántos pollos preparar. La captura de esta página está en la sección 3.2.

**Visuales.**
- Columnas: merma por turno contra la meta.
- Columnas: merma por día de la semana.
- Columnas agrupadas: pollos preparados y vendidos por día de la semana.
- Línea: pollos vendidos contra el pronóstico de referencia de los últimos 28 días.

**Filtros.** Año, mes y turno.

#### PAG-04. Precio del pollo vivo y margen

**Descripción.** Sigue el precio por kilogramo del pollo vivo y lo pone junto al margen neto del mes. Se lee buscando los meses en que el precio sube y el margen baja. Apoya la decisión del dueño de anticipar compras y ajustar precios ante una subida. La captura de esta página está en la sección 3.2.

**Visuales.**
- Línea: precio diario del pollo vivo por kilogramo.
- Línea: margen neto mensual.
- Línea: precio promedio mensual del pollo vivo.

**Filtros.** Año y mes.
