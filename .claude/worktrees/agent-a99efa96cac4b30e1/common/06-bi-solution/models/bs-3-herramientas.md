# Plantilla: Herramientas utilizadas (`secciones/2.3.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.3.md` (sus herramientas también aparecen en la figura `arquitectura-bi`) |
| **Punto** | 2.3. Herramientas utilizadas |
| **Códigos** | `HER-nn` |
| **Entradas** | componentes de 2.2, herramientas previstas del brief (alcance), decisión del usuario sobre ETL y almacenamiento |
| **Salida** | cada herramienta con su capa, función, justificación y alternativa descartada |

## Instrucciones para el agente
1. La primera línea es `## 2.3. Herramientas utilizadas`. Esta sección no lleva figura.
2. Un párrafo con los criterios de selección: costo, curva de aprendizaje, compatibilidad con las fuentes y con Power BI, y la consigna del curso.
3. La tabla `Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada`, con al menos una herramienta para ETL, almacenamiento y visualización. La capa usa los nombres de 2.2.
4. **Power BI** va en la capa de visualización (consigna del curso).
5. Si el usuario aún no decide la herramienta de ETL o la de almacenamiento: **Herramienta** «Pendiente», **Justificación** «Pendiente: se decide con la construcción del capítulo 3» y **Alternativa descartada** «—». Ninguna otra capa admite «Pendiente».
6. Cierra con una frase: qué herramientas faltan decidir y que se completan antes de la entrega.
7. Si cambia una herramienta, vuelve a construir la figura `arquitectura-bi`, que muestra las herramientas de cada capa.

## Formato

```markdown
## 2.3. Herramientas utilizadas

[Criterios de selección.]

Tabla 1: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | [herramienta] | [capa] | [qué hace en el proyecto] | [por qué se eligió] | [opción evaluada y por qué no] |
| HER-02 | Pendiente | ETL | [qué hará] | Pendiente: se decide con la construcción del capítulo 3 | — |

[Frase sobre las herramientas pendientes, si las hay.]
```

## Ejemplo

```markdown
## 2.3. Herramientas utilizadas

Las herramientas se eligen por su costo, por lo fácil que es aprenderlas en el plazo del proyecto, por su compatibilidad con los archivos que ya produce la empresa y con Power BI, y por la consigna del curso, que fija Power BI para el dashboard.

Tabla 1: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | Microsoft Excel | Fuentes | Recibir y revisar las exportaciones de la caja, las aplicaciones y el control de producción | La empresa ya lo usa y abre los archivos CSV y Excel de sus sistemas sin costo adicional | Google Sheets, que obliga a subir los registros de ventas a una cuenta en la nube |
| HER-02 | Pendiente | ETL | Extraer, limpiar e integrar las cuatro fuentes y registrar la calidad de cada carga | Pendiente: se decide con la construcción del capítulo 3 | — |
| HER-03 | Pendiente | Almacenamiento | Guardar las tablas depuradas del modelo estrella | Pendiente: se decide con la construcción del capítulo 3 | — |
| HER-04 | Power BI Desktop | Visualización | Relacionar las tablas, calcular las medidas DAX de los KPI y publicar el dashboard | Lo exige la consigna del curso; modela en estrella, conecta con archivos y bases de datos y su versión de escritorio no tiene costo | Tableau Public, que publica los datos en abierto y no responde a la consigna |

Las herramientas de ETL y de almacenamiento se definen con la construcción de la solución, antes de la entrega; la arquitectura ya fija qué debe hacer cada una.
```

## Checklist
- [ ] Encabezado exacto en la primera línea y sin figura.
- [ ] Al menos una herramienta en ETL, almacenamiento y visualización.
- [ ] Cada herramienta decidida tiene función, justificación y alternativa descartada.
- [ ] «Pendiente» solo en ETL o almacenamiento, con su motivo.
- [ ] Power BI está en la capa de visualización.
