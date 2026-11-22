# Plantilla: Herramientas utilizadas (`secciones/2.3.md`)

| | |
|---|---|
| **Entregable** | `secciones/2.3.md` |
| **Punto** | 2.3. Herramientas utilizadas |
| **Códigos** | `HER-nn` |
| **Entradas** | componentes de 2.2, herramientas previstas en el alcance del brief, lo que el usuario decide |
| **Salida** | cada herramienta con su capa, su función, su justificación y la alternativa descartada |

## Instrucciones para el agente
1. La primera línea es `## 2.3. Herramientas utilizadas`.
2. Una frase que presenta la tabla (con la cita de la herramienta principal si la hay, por ejemplo Microsoft, 2026).
3. Tabla `Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada`, con **Power BI en la capa Visualización** y al menos una fila en cada capa de ETL, almacenamiento y visualización (las fuentes no llevan herramienta).
4. La justificación compara con un criterio (costo, curva de aprendizaje, integración, volumen de datos o requisito de la consigna) y no dice solo «es popular» o «es gratuita».
5. **Pendiente.** Si el usuario aún no decide la herramienta de **ETL** o de **Almacenamiento**, la fila lleva «Pendiente» en la columna `Herramienta`, el motivo en la justificación («se decide al construir el capítulo 3») y las alternativas que se están evaluando en la última columna. En otras capas «Pendiente» no se acepta.
6. Después de escribir la tabla, indica al usuario que lo pendiente se completa con `06-make-bi-solution-update`.

## Formato

```markdown
## 2.3. Herramientas utilizadas

[Frase que presenta la tabla.]

Tabla 1: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | [herramienta o Pendiente] | ETL | [qué hace aquí] | [criterio de elección o motivo de lo pendiente] | [alternativa] |
| HER-nn | Power BI Desktop | Visualización | [qué hace aquí] | [criterio] | [alternativa] |
```

## Ejemplo

```markdown
## 2.3. Herramientas utilizadas

Las herramientas se eligieron por su integración con Power BI, por su costo y por el tamaño de los datos del proyecto (Microsoft, 2026). La herramienta del proceso ETL se decide al construir el capítulo 3.

Tabla 1: Herramientas de la solución de BI

| Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada |
|---|---|---|---|---|---|
| HER-01 | Pendiente | ETL | Extraer, depurar, homologar y anexar las tres fuentes | Se decide al construir el capítulo 3, según el tiempo disponible y la facilidad de documentar cada paso | Power Query y scripts de Python, en evaluación |
| HER-02 | Modelo semántico de Power BI | Almacenamiento | Guardar el modelo en estrella y sus medidas | El volumen del proyecto cabe en un modelo por importación y no exige un servidor ni costo adicional | SQL Server Express, que agrega administración sin necesidad |
| HER-03 | Power BI Desktop | Visualización | Modelar los datos, escribir las medidas y construir el dashboard | Es la herramienta que exige el curso y se conecta a las fuentes del proyecto sin conectores adicionales | Excel con tablas dinámicas, que limita la interacción entre páginas |
| HER-04 | Power BI Service | Visualización | Publicar el dashboard y programar la actualización | Permite que la gerencia lo consulte desde el navegador sin instalar nada | Compartir el archivo .pbix, que no actualiza solo |
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Power BI figura en la capa de visualización.
- [ ] Cada herramienta tiene función, justificación con criterio y alternativa descartada.
- [ ] «Pendiente» solo aparece en ETL o Almacenamiento y con su motivo.
- [ ] Hay al menos una fila (o «Pendiente») en cada capa de ETL, almacenamiento y visualización.
