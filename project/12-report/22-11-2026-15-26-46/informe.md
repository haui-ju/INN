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

(INCLUIR IMAGEN: Figura 1: Figura X: Business Model Canvas. Archivo sugerido: imagenes/bmc.html)

**Cómo copiarla.** Abrir [imagenes/bmc.html](imagenes/bmc.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra en una sola vista cómo la empresa crea, entrega y captura valor. El modelo atiende 2 segmentos de clientes por 5 canales y sostiene 3 fuentes de ingresos frente a 4 partidas de costos.

Tabla 4: Bloques del Business Model Canvas

| Bloque | Contenido |
|---|---|
| Segmentos de clientes | Familias y trabajadores de Magdalena del Mar y distritos cercanos; clientes de delivery |
| Propuesta de valor | Pollo a la brasa y parrilladas; atención rápida; precios justos; pedido en el local, para llevar o a domicilio |
| Canales | Salón; para llevar; delivery propio por WhatsApp; Rappi; PedidosYa |
| Relaciones con clientes | Atención personal en el local; pedidos por WhatsApp con clientes frecuentes; reseñas en las aplicaciones |
| Fuentes de ingresos | Venta de pollos, parrilladas y combos; bebidas y adicionales; cargo por delivery propio |
| Recursos clave | Cocina y hornos del local; marca y recetas; equipo de cocina, salón y reparto; sistema de caja |
| Actividades clave | Compra y preparación del pollo; producción por turno; atención y despacho de pedidos |
| Socios clave | Proveedores de pollo vivo y de insumos; Rappi y PedidosYa; proveedor del sistema de caja |
| Estructura de costos | Pollo vivo y otros insumos; comisiones de 25 % a 30 % de las aplicaciones; planilla; alquiler y servicios del local |

**Lectura del modelo.** El crecimiento llega por el bloque de canales: las aplicaciones pasaron de 15 % a 35 % de las ventas. Sin embargo, suman a la estructura de costos una comisión de 25 % a 30 % que el precio no refleja, porque los precios son iguales en todos los canales. Además, el jefe de cocina decide la producción por turno, una actividad clave, según su experiencia, y la merma llega a 7 %. La problemática se ubica así entre canales, actividades clave y estructura de costos.

## 1.5. Análisis PESTEL

El análisis PESTEL examina los factores políticos, económicos, sociales, tecnológicos, ecológicos y legales del entorno que la empresa no controla, pero que condicionan sus resultados (Aguilar, 1967). Para Pollerías y Parrilladas San Martín se identificaron nueve hallazgos, cada uno con su efecto en el negocio y su fuente.

(INCLUIR IMAGEN: Figura 2: Figura X: Análisis PESTEL. Archivo sugerido: imagenes/pestel.html)

**Cómo copiarla.** Abrir [imagenes/pestel.html](imagenes/pestel.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Resume los factores del entorno que favorecen o amenazan al negocio. De 9 hallazgos del entorno, 4 son oportunidades y 5 son amenazas, y las amenazas se concentran en el factor económico.

Tabla 5: Análisis PESTEL

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

(INCLUIR IMAGEN: Figura 3: Figura X: Matriz FODA. Archivo sugerido: imagenes/foda.html)

**Cómo copiarla.** Abrir [imagenes/foda.html](imagenes/foda.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Resume la situación de la empresa para decidir qué aprovechar y qué proteger. Por dentro fortalezas y debilidades se equilibran (4 frente a 4) y por fuera las amenazas superan a las oportunidades (3 frente a 5), y de su cruce salen 7 estrategias.

Tabla 6: Fortalezas

| Código | Fortaleza | Evidencia o fuente |
|---|---|---|
| FOR-01 | Cuatro canales de venta en operación: salón, para llevar, delivery propio por WhatsApp y aplicaciones | Canales del Canvas, sección 1.4 |
| FOR-02 | Cocina y hornos propios, con un equipo de 16 trabajadores | Recursos clave del Canvas y trabajadores declarados, 2026 |
| FOR-03 | Ventas en crecimiento: 18 % más en el último año | Registro de caja de 2025 y 2026 |
| FOR-04 | Comprobantes electrónicos desde 2018, que dejan un registro digital de las ventas | Padrón de contribuyentes, 2026 |

Tabla 7: Debilidades

| Código | Debilidad | Evidencia o fuente |
|---|---|---|
| DEB-01 | Precios iguales en todos los canales, sin considerar la comisión | Lista de precios única de la empresa, 2026 |
| DEB-02 | Producción por turno decidida por experiencia, con una merma de 7 % | Control de producción de cocina, 2026 |
| DEB-03 | Ventas de caja, aplicaciones y WhatsApp registradas en sistemas que no se cruzan | Revisión de las fuentes de datos de la empresa, 2026 |
| DEB-04 | El costo del pollo vivo no se relaciona con el margen ni con los precios de venta | Registro de compras de la empresa, 2026 |

Tabla 8: Oportunidades

| Código | Oportunidad | Evidencia o fuente |
|---|---|---|
| OPO-01 | Herramientas de BI de bajo costo para integrar y analizar los datos | TEC-01 |
| OPO-02 | Demanda de delivery de pollo en crecimiento | SOC-01 |
| OPO-03 | Demanda concentrada en días y horas conocidos, que permite pronosticar la producción | SOC-02 |

Tabla 9: Amenazas

| Código | Amenaza | Evidencia o fuente |
|---|---|---|
| AME-01 | Precio del pollo vivo volátil | ECO-01 |
| AME-02 | Comisiones de 25 % a 30 % de las aplicaciones de delivery | TEC-02 |
| AME-03 | Inflación que eleva los costos de operación | ECO-02 |
| AME-04 | Normas de envases y de datos personales que elevan costos y exigencias | AMB-01, LEG-01 |
| AME-05 | Cadenas de pollerías y otras cadenas de comida que compiten en las mismas aplicaciones | KFC Perú y McDonald's figuran entre las aplicaciones de comida más descargadas, Delgado Tong (2026); entorno competitivo, sección 1.3 |

**Estrategias cruzadas.** Del cruce de los cuadros internos con los externos salen las estrategias que orientan el proyecto. Cinco de las siete dependen de medir, integrar o pronosticar con datos (FO-01, DO-01, DO-02, DA-01 y DA-02), y son las que la solución de BI hace posibles.

Tabla 10: Estrategias cruzadas FO, FA, DO y DA

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

(INCLUIR IMAGEN: Figura 4: Figura X: Diagrama de Ishikawa. Archivo sugerido: imagenes/ishikawa.html)

**Cómo copiarla.** Abrir [imagenes/ishikawa.html](imagenes/ishikawa.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Ordena por categorías las causas que explican el problema central del negocio. El problema «Las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %» se explica por 8 causas en 6 categorías, con más peso en método y medio ambiente (2 causas cada una).

Tabla 11: Causas del diagrama de Ishikawa

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

Tabla 12: Causas principales de la problemática

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

Tabla 13: Objetivo general del proyecto

| Código | Objetivo | Métrica | Meta | Plazo | Indicador |
|---|---|---|---|---|---|
| OG-01 | Implementar una solución de BI en Power BI que integre las ventas de todos los canales, la producción por turno y el precio del pollo vivo para recuperar el margen neto | Margen neto | 12 % o más, a seis meses de implantada la solución | Entrega (07-12-2026) | Margen neto global |

## 1.10. Objetivos específicos

Los objetivos específicos desagregan el objetivo general en cinco resultados medibles al cierre del proyecto.

Tabla 14: Objetivos específicos

| Código | Objetivo | Métrica | Meta | Plazo | Aporta a | Indicador |
|---|---|---|---|---|---|---|
| OE-01 | Integrar y depurar las fuentes de ventas (caja, Rappi, PedidosYa y WhatsApp) mediante un proceso ETL en Power Query | Registros que pasan las reglas de calidad | 98 % o más | Entrega (07-12-2026) | OG-01 | Calidad de datos del ETL |
| OE-02 | Medir el margen de contribución por canal y por producto | Canales y productos con margen calculado | 100 % de los canales y productos del periodo | Entrega (07-12-2026) | OG-01 | Margen de contribución por canal y producto |
| OE-03 | Pronosticar la demanda de pollos por día y turno para reducir la merma | Merma sobre los pollos preparados | De 7 % a 3 % o menos | Entrega (07-12-2026) | OG-01 | Porcentaje de merma por turno |
| OE-04 | Monitorear el efecto del precio del pollo vivo en el costo y el margen | Días del periodo con el precio del insumo cruzado con el margen | 100 % de los días | Entrega (07-12-2026) | OG-01 | Precio promedio del pollo vivo por kilogramo |
| OE-05 | Construir un dashboard con KPI, metas y filtros que guíe las decisiones de precio, producción y personal | KPI con meta y semáforo | 100 % de los KPI | Entrega (07-12-2026) | OG-01 | KPI con meta en el dashboard |

**Matriz de articulación.** Cada objetivo específico responde a causas del diagrama de Ishikawa (1.7), se apoya en el análisis PESTEL (1.5) y en la matriz FODA (1.6) y actúa sobre bloques concretos del modelo de negocio.

Tabla 15: Matriz de articulación de los objetivos específicos

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

Tabla 16: Componentes de la solución que atienden cada objetivo específico

| Objetivo | Componentes | Cómo lo atiende |
|---|---|---|
| OE-01 | CAP-07, CAP-08, CAP-09 | Power Query depura y cruza las fuentes, aplica las reglas de calidad y las deja en un modelo en estrella |
| OE-02 | CAP-09, CAP-10 | El modelo calcula el margen de contribución por canal y producto y el dashboard lo muestra frente a la meta |
| OE-03 | CAP-09, CAP-11 | El modelo cruza lo preparado con lo vendido por turno y el pronóstico estima la demanda por día y turno |
| OE-04 | CAP-06, CAP-09, CAP-10 | El boletín de precios entra al modelo y el dashboard lo cruza con el costo y el margen |
| OE-05 | CAP-10, CAP-12 | El dashboard reúne los KPI con su meta y sus filtros y se publica para el dueño y el jefe de cocina |

## 2.2. Arquitectura de Inteligencia de Negocios

La arquitectura de la solución sigue las cuatro capas de un sistema de inteligencia de negocios. Son las fuentes que generan los datos, el proceso ETL que los extrae, depura y transforma, el almacenamiento donde queda el modelo dimensional y la visualización donde se consulta (Kimball & Ross, 2013). Cada capa tiene componentes con una función definida, y las herramientas que los construyen se detallan en el punto 2.3.

(INCLUIR IMAGEN: Figura 5: Figura X: Arquitectura de BI. Archivo sugerido: imagenes/arquitectura-bi.html)

**Cómo copiarla.** Abrir [imagenes/arquitectura-bi.html](imagenes/arquitectura-bi.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra cómo viaja el dato desde las fuentes hasta el dashboard en cuatro capas. Los datos pasan de 6 fuentes por 2 componentes de ETL y 1 de almacenamiento hasta 3 componentes de visualización.

Tabla 17: Componentes de la arquitectura de BI

| Código | Capa | Componente | Función | Entrada y salida |
|---|---|---|---|---|
| CAP-01 | Fuentes | Sistema de caja, salón y para llevar (FUE-01) | Aporta las ventas por ticket, producto, canal y turno | Registro de caja → archivo de ventas |
| CAP-02 | Fuentes | Reportes de Rappi (FUE-02) | Aporta los pedidos y la comisión de cada pedido | Reporte de la aplicación → archivo de pedidos |
| CAP-03 | Fuentes | Reportes de PedidosYa (FUE-03) | Aporta los pedidos y la comisión de cada pedido | Reporte de la aplicación → archivo de pedidos |
| CAP-04 | Fuentes | Pedidos por WhatsApp (FUE-04) | Aporta los pedidos del delivery propio | Registro de pedidos → archivo de pedidos |
| CAP-05 | Fuentes | Control de producción por turno (FUE-05) | Aporta los pollos preparados, vendidos y la merma de cada turno | Registro de cocina → archivo de producción |
| CAP-06 | Fuentes | Boletín de precios de aves del Ministerio de Desarrollo Agrario y Riego (FUE-06) | Aporta el precio diario del pollo vivo en Lima Metropolitana | Boletín en PDF → archivo de precios diarios |
| CAP-07 | ETL | Extracción y transformación con Power Query | Combina los archivos de las seis fuentes, asigna tipos de dato, homologa productos y canales y calcula columnas | Archivos de las fuentes → tablas transformadas |
| CAP-08 | ETL | Reglas de calidad y homologación | Quita duplicados, trata nulos, anonimiza los datos de clientes y cuenta los registros descartados | Tablas transformadas → tablas limpias |
| CAP-09 | Almacenamiento | Modelo dimensional | Guarda los hechos y las dimensiones que consume el dashboard | Tablas limpias → modelo en estrella |
| CAP-10 | Visualización | Dashboard de rentabilidad, merma y precio del insumo | Muestra los KPI, el margen por canal y producto, la merma por turno y el precio del pollo vivo | Modelo en estrella → páginas e indicadores |
| CAP-11 | Visualización | Pronóstico de demanda por día y turno | Estima cuántos pollos preparar según el patrón de ventas | Modelo en estrella → serie con su pronóstico |
| CAP-12 | Visualización | Publicación del dashboard | Pone el dashboard a disposición del dueño y del jefe de cocina en el navegador | Dashboard terminado → informe publicado |

**Lectura de la arquitectura.** El dato viaja desde la caja (CAP-01), las aplicaciones (CAP-02 y CAP-03), WhatsApp (CAP-04), la cocina (CAP-05) y el boletín de precios (CAP-06) hasta un modelo único (CAP-09). De ahí pasa al dashboard (CAP-10), que el dueño consulta antes de decidir precios, producción y compras.

## 2.3. Herramientas utilizadas

Las herramientas (HER-01 a HER-04) se eligieron por su integración con Power BI, por su costo y por el tamaño de los datos del proyecto (Microsoft, s. f.). Todas forman parte del ecosistema de Power BI, de modo que el equipo trabaja con una sola plataforma de punta a punta.

Tabla 18: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | Power Query | ETL | Extraer, depurar, homologar y anexar las seis fuentes y registrar cada paso | Viene integrada en Power BI Desktop, deja cada paso registrado y repetible y es la herramienta que prevé el objetivo OE-01 | Scripts de Python, que exigen más mantenimiento y no se integran con el modelo |
| HER-02 | Modelo semántico de Power BI | Almacenamiento | Guardar el modelo en estrella y sus medidas | El volumen del proyecto, de enero a octubre de 2026 y un solo local, cabe en un modelo por importación y no exige un servidor ni costo adicional | SQL Server Express, que agrega administración sin necesidad para este volumen |
| HER-03 | Power BI Desktop | Visualización | Modelar los datos, escribir las medidas y construir el dashboard con su pronóstico | Es la herramienta de visualización que pide la consigna del proyecto y reúne la preparación, el modelado, las medidas DAX y el pronóstico en un solo programa gratuito (Microsoft, s. f.) | Excel con tablas dinámicas, que limita la interacción entre páginas y los filtros |
| HER-04 | Power BI Service | Visualización | Publicar el dashboard para que el dueño lo consulte desde el navegador | Permite que el dueño y el jefe de cocina vean el dashboard sin instalar el programa de escritorio | Compartir el archivo .pbix, que obliga a abrirlo en un equipo con Power BI Desktop |

## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones

El modelo sigue un esquema en estrella con varios hechos que comparten dimensiones, es decir, una constelación de hechos (Kimball & Ross, 2013). Tiene cuatro tablas de hechos y cinco dimensiones, de modo que las ventas, la producción, el precio del insumo y las metas de los KPI se pueden cruzar por fecha, canal y turno.

(INCLUIR IMAGEN: Figura 6: Figura X: Modelo de datos en estrella. Archivo sugerido: imagenes/modelo-datos.html)

**Cómo copiarla.** Abrir [imagenes/modelo-datos.html](imagenes/modelo-datos.html) en el navegador, elegir la escala y pulsar «Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.

**Cómo leer la figura.** Muestra las tablas de hechos, las dimensiones y las relaciones sobre las que se calculan los indicadores. El modelo tiene 4 tablas de hechos y 5 dimensiones unidas por 9 relaciones, y fPedidos es el hecho con más ejes de análisis (4 claves).

**Tablas de hechos.** Cada hecho tiene un grano propio y sus medidas se suman, promedian o cuentan a ese nivel.

Tabla 19: Tablas de hechos

| Código | Tabla de hechos | Granularidad | Medidas | Claves |
|---|---|---|---|---|
| FCT-01 | fPedidos | Una fila por línea de pedido, canal y día | cantidad (suma); venta_bruta (suma); comision (suma); costo_estimado (suma); costo_operativo (suma); pollos_equivalentes (suma); registro_valido (suma); registro_total (conteo) | fecha_key; producto_key; canal_key; turno_key |
| FCT-02 | fProduccion | Una fila por turno y día | pollos_preparados (suma); pollos_vendidos (suma); pollos_merma (suma) | fecha_key; turno_key |
| FCT-03 | fPrecioInsumo | Una fila por día | precio_kg (promedio); valor_imputado (suma) | fecha_key |
| FCT-04 | fMetaKpi | Una fila por KPI y mes | meta (promedio); valor_real (promedio) | kpi_key; fecha_key |

**Dimensiones.** Las dimensiones se comparten entre los hechos para que los filtros de una página afecten a todos los visuales.

Tabla 20: Dimensiones

| Código | Dimensión | Clave | Atributos | Jerarquías |
|---|---|---|---|---|
| DIM-01 | dCalendario | fecha_key | fecha; anio; mes; nombre_mes; dia_semana; es_feriado | Año > Mes > Fecha |
| DIM-02 | dProducto | producto_key | producto; categoria | Categoría > Producto |
| DIM-03 | dCanal | canal_key | canal; tipo_canal; comision_pct | — |
| DIM-04 | dTurno | turno_key | turno; hora_inicio; hora_fin | — |
| DIM-05 | dKpi | kpi_key | kpi; objetivo; tiene_meta; frecuencia | — |

**Relaciones.** Todas las relaciones son de varios a uno, desde el hecho hacia la dimensión, y filtran en un solo sentido.

Tabla 21: Relaciones del modelo

| Código | Desde | Hacia | Campos | Cardinalidad | Filtro |
|---|---|---|---|---|---|
| REL-01 | fPedidos | dCalendario | fecha_key | *:1 | Simple |
| REL-02 | fPedidos | dProducto | producto_key | *:1 | Simple |
| REL-03 | fPedidos | dCanal | canal_key | *:1 | Simple |
| REL-04 | fPedidos | dTurno | turno_key | *:1 | Simple |
| REL-05 | fProduccion | dCalendario | fecha_key | *:1 | Simple |
| REL-06 | fProduccion | dTurno | turno_key | *:1 | Simple |
| REL-07 | fPrecioInsumo | dCalendario | fecha_key | *:1 | Simple |
| REL-08 | fMetaKpi | dKpi | kpi_key | *:1 | Simple |
| REL-09 | fMetaKpi | dCalendario | fecha_key | *:1 | Simple |

**Lectura del modelo.** Con este modelo se calcula el margen de cada canal y producto por mes, con la comisión de 25 % a 30 % de las aplicaciones ya descontada (FCT-01). Se compara lo preparado con lo vendido en cada turno (FCT-02). También se contrasta el precio del pollo vivo (FCT-03) con el margen de enero a octubre de 2026 y cada KPI con su meta (FCT-04).

## 2.5. Indicadores clave de rendimiento (KPI)

Los indicadores se eligieron con dos criterios: que midan el logro de un objetivo específico y que sostengan una decisión del dueño. Son siete (KPI-01 a KPI-07): cinco llevan el mismo nombre que el indicador de su objetivo en el punto 1.10 (OE-01 a OE-05) y todos se calculan con campos del modelo de datos.

**Definición.** Cada indicador se define con su fórmula, la medida que lo calcula en Power BI y los campos del modelo de los que sale.

Tabla 22: Definición de los KPI

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

Tabla 23: Meta, frecuencia y decisión de cada KPI

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
