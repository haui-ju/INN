# Spec Delta

## Purpose

Define cómo se generan los datos del proyecto cuando `modo_datos` es `generado`: las fuentes del brief como archivos CSV reproducibles, con volumen, cifras coherentes con el informe, defectos intencionales y una hoja de respuestas para verificar el trabajo del equipo.

## ADDED Requirements

### Requirement: Una fuente por archivo CSV en data
La generación SHALL escribir un archivo CSV en codificación UTF-8 por cada fuente generada del brief (FUE-nn con origen «Generada») en `data/` en la raíz del repositorio, nombrado con el código de la fuente. Las fuentes abiertas o públicas SHALL NOT generarse como si fueran reales: se declaran con su origen.

#### Scenario: Fuentes del brief
- **WHEN** el brief declara FUE-01 a FUE-05 como generadas y FUE-06 como abierta
- **THEN** `data/` trae un CSV por cada una de las cinco generadas y el boletín de precios se identifica como serie generada a partir de la fuente abierta, no como el dato oficial

#### Scenario: Modo real
- **WHEN** `modo_datos` es `real`
- **THEN** la skill no genera datos y pide al equipo los archivos autorizados

### Requirement: Parámetros visibles antes de generar
La skill SHALL derivar los parámetros de calibración de lo ya escrito en el informe y el brief (periodo, número de locales, canales, productos, ventas anuales, comisiones, merma, margen, precio del insumo), SHALL guardarlos en `data/parametros.json` y SHALL mostrarlos al usuario para su confirmación antes de generar los archivos.

#### Scenario: Parámetros confirmados
- **WHEN** la skill muestra los parámetros y el usuario los confirma
- **THEN** genera los archivos con esos parámetros y deja `parametros.json` junto a ellos

#### Scenario: Cifra del informe sin fuente
- **WHEN** una cifra necesaria no aparece en el informe ni en el brief
- **THEN** la skill pregunta el valor y lo registra en `parametros.json` con su origen

### Requirement: Reproducibilidad
La generación SHALL ser determinista: con los mismos parámetros y la misma semilla SHALL producir archivos idénticos byte a byte. El generador SHALL funcionar solo con la biblioteca estándar.

#### Scenario: Regenerar
- **WHEN** se ejecuta la generación dos veces con el mismo `parametros.json`
- **THEN** los CSV de ambas ejecuciones son idénticos

#### Scenario: Cambiar la semilla
- **WHEN** el usuario cambia la semilla
- **THEN** los datos cambian, pero las cifras calibradas siguen dentro de su tolerancia

### Requirement: Volumen suficiente
La generación SHALL cubrir todo el periodo del brief a una granularidad que permita calcular los KPI por día, canal y turno, y SHALL producir un volumen de líneas de pedido compatible con las ventas anuales del informe, del orden de cien mil líneas para el caso de una pollería con un local y quince meses.

#### Scenario: Cobertura del periodo
- **WHEN** el periodo es de agosto de 2025 a octubre de 2026
- **THEN** hay pedidos en todos los meses y la producción por turno cubre todos los días de operación

#### Scenario: Ventas coherentes
- **WHEN** se suman las ventas del periodo
- **THEN** el total anualizado es coherente con las ventas anuales en UIT de la sección 1.3

### Requirement: Cifras calibradas con el informe
Los datos generados SHALL reproducir, dentro de una tolerancia declarada, las cifras que el informe afirma y que pueden comprobarse en el periodo: margen neto, merma, participación de las aplicaciones, comisiones por aplicación, precio del insumo y crecimiento de ventas.

#### Scenario: Crecimiento interanual
- **WHEN** se comparan las ventas de agosto a octubre de 2026 con las de agosto a octubre de 2025
- **THEN** crecen alrededor de 18 % dentro de la tolerancia

#### Scenario: Margen neto
- **WHEN** se calcula el margen neto mensual con los datos generados
- **THEN** baja de alrededor de 14 % en el primer mes (agosto de 2025) a alrededor de 8 % en el último (octubre de 2026), y el de los últimos tres meses se acerca a 8 % dentro de la tolerancia

#### Scenario: Cifra fuera de tolerancia
- **WHEN** una cifra generada queda fuera de su tolerancia
- **THEN** la skill no entrega los archivos y informa la cifra y su desvío

### Requirement: Defectos intencionales ligados al modelo
Los datos SHALL incluir defectos que el ETL debe tratar y que el modelo ya prevé: registros inválidos (para las medidas de registros válidos y totales), días sin precio del insumo (para el valor imputado), pedidos duplicados en los reportes de las aplicaciones y de WhatsApp, nombres de producto distintos entre fuentes, fechas con formatos mezclados y nulos. Cada tipo de defecto SHALL tener una cantidad registrada.

#### Scenario: Defectos cuantificados
- **WHEN** termina la generación
- **THEN** `data/respuestas/` lista cada tipo de defecto con el número de registros afectados y la regla de calidad que debería tratarlo

#### Scenario: Datos sin defectos
- **WHEN** la generación no produce ningún defecto de un tipo que el modelo usa
- **THEN** la skill lo informa como incumplimiento y no entrega los archivos

### Requirement: Hoja de respuestas para verificar el ETL
La generación SHALL escribir en `data/respuestas/` los totales esperados después de una limpieza correcta (filas por fuente, ventas y comisión por mes y por canal, pollos preparados, vendidos y merma por turno, precio medio por mes y días imputados), en CSV.

#### Scenario: Comparar contra el ETL
- **WHEN** el equipo carga sus tablas y entrega sus totales
- **THEN** cada total se compara con la hoja de respuestas y la diferencia se informa por tabla

### Requirement: Respuestas para comprobar el dashboard
La hoja de respuestas SHALL incluir también los valores esperados que alimentan cada visual del dashboard de referencia: margen de contribución por mes, canal y producto, producción por día de la semana, precio diario del pollo vivo con su marca de imputado y un pronóstico de referencia por día y turno, y SHALL incluir el KPI de precisión del pronóstico en los KPI esperados.

#### Scenario: Margen por canal y producto
- **WHEN** el equipo calcula el margen de contribución de un canal y un producto en un mes
- **THEN** puede compararlo con la fila de ese mes, canal y producto de la hoja de respuestas

#### Scenario: Método del pronóstico
- **WHEN** se consulta el pronóstico de referencia
- **THEN** trae su método declarado (promedio de las cuatro jornadas anteriores del mismo día y turno) y el error porcentual de cada día

### Requirement: Declaración de datos generados
La skill SHALL dejar `data/README.md` con la lista de archivos, su significado, la semilla y la declaración de que los datos son generados para el proyecto, y la sección 3.1 SHALL declararlo.

#### Scenario: Datos generados
- **WHEN** el informe se arma con `modo_datos: generado`
- **THEN** la sección 3.1 dice que los datos fueron generados para el proyecto y cómo se calibraron
