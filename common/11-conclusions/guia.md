# Playbook de las conclusiones (sección 5)

Cierra el informe: contrasta lo que el dashboard midió con los objetivos del proyecto, recomienda qué hacer y deja lo aprendido. Lo lee la skill `11-make-conclusions` y la actualiza `11-make-conclusions-update`. El formato de la sección está en [`models/cn-1-seccion-5.md`](models/cn-1-seccion-5.md).

**Principio:** una conclusión dice lo que los valores reales permiten decir y nada más. El estado de cada objetivo **se calcula**; no se opina ni se redondea a favor del proyecto.

## 0. Reglas que se aplican siempre

### 0.1 Fuentes, en este orden
1. El brief vigente: el objetivo general `OG-nn`, los específicos `OE-nn` con su indicador, y los usuarios (quién decide).
2. `modelo.json` y la sección 2.5 de la corrida vigente de `07-make-data-model-kpi`: qué KPI mide cada objetivo (`objetivo`), su meta y su sentido (`o más`, `o menos`).
3. `valores.json` de la corrida vigente de `09-make-dashboard`: el valor real de cada KPI. **Sin este archivo no se escribe la sección.**
4. La corrida vigente de `05-make-problem-objectives` (problemática y matriz de articulación) y, si existe, la de `10-make-storytelling` (hallazgos `HLZ-nn` que se pueden citar). Si falta `10`, la skill avisa y sigue con los valores del dashboard.
5. El config (`modo_datos`).

### 0.2 Preguntar y confirmar
La skill muestra primero los estados calculados y el plan (una conclusión por objetivo, las recomendaciones y las lecciones que propone) y **espera la confirmación** antes de escribir.

### 0.3 Contrato de la corrida (lo lee `12-make-report`)
```
project/11-conclusions/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/5.md        (encabezado exacto: ## 5. Conclusiones, recomendaciones y lecciones aprendidas)
├── referencias.md        (solo si cita; APA 7)
└── README.md             (procedencia: corridas de origen y modo de datos)
```
`5.md` solo trae texto final y las tablas, cada una con su línea `Tabla N: título`. La procedencia va solo en `README.md`.

### 0.4 Códigos de trazabilidad
`CNC-nn` (conclusión), `REC-nn` (recomendación) y `LEC-nn` (lección), numerados por prefijo, sin repetir. Reutiliza `OG-nn`, `OE-nn` y `KPI-nn`. Un código eliminado deja su número sin usar. La validación exige que todo código citado esté definido.

### 0.5 Texto limpio
Ningún archivo de la corrida, salvo `README.md`, califica los datos con los términos de `_shared/policy.json`. Decir que los datos «se generaron para el proyecto» es correcto y obligatorio cuando `modo_datos` es `generado`.

## 1. Cómo se calcula el estado

El comando `python3 .claude/skills/_shared/rules/conclusions.py estados` imprime los estados con sus valores. La regla, en tres pasos:

**a) Estado de cada KPI.** Compara el valor real con la meta de 2.5 según su sentido:

| Meta en 2.5 | Cumple cuando |
|---|---|
| «98 % o más» | valor ≥ 98 |
| «3 % o menos» | valor ≤ 3 |
| una cifra sin sentido («100 %») | valor ≥ la cifra |
| «Pendiente» | no hay estado: **Sin meta** |

Un valor «cerca» de la meta **no** cumple: 97.9 % frente a «98 % o más» es `No cumple`.

**b) Estado de cada objetivo específico.** Se toman los KPI de `modelo.json` con ese `OE-nn`:

| Situación | Estado del objetivo |
|---|---|
| Todos los KPI tienen meta y todos cumplen | **Cumplido** |
| Al menos un KPI cumple y otro no cumple, o los que tienen meta cumplen pero otro KPI sigue sin meta | **Parcial** |
| Ningún KPI con meta cumple | **No cumplido** |
| Ningún KPI tiene meta | **Sin meta** (no se puede concluir) |

**c) Estado del objetivo general.** Sale de los estados de los objetivos específicos: todos `Cumplido` → **Cumplido**; todos `No cumplido` → **No cumplido**; todos `Sin meta` → **Sin meta**; cualquier otra combinación → **Parcial**.

## 2. Conclusiones (tablas 1 y 2)

- **Una por objetivo:** una `CNC-nn` por cada `OE-nn` del brief y una por el `OG-nn`. En la columna `Objetivo` va solo el código.
- **El estado es el calculado.** La validación lo recalcula y compara.
- **La conclusión explica, no repite.** Una o dos frases: qué mostró el indicador, frente a qué meta y por qué importa para la problemática (punto 1.8). Una cifra citada es la de `valores.json`.
- **Sin meta no se concluye.** Si algún KPI del objetivo no tiene meta, la conclusión dice que su cumplimiento no se puede concluir porque la meta está pendiente. Se cierra con `07-make-data-model-kpi-update` (la meta la propone `09-make-dashboard` desde el valor real) y después se actualiza esta sección con `11-make-conclusions-update`.
- **El objetivo general** cita las conclusiones `CNC-nn` de los específicos de los que sale su estado.
- **Respaldo:** una fila por cada KPI de cada objetivo específico, con el valor y la meta tal como están en `valores.json` y en 2.5.

## 3. Recomendaciones (tabla 3)

- Toda conclusión que **no** sea `Cumplido` tiene al menos una `REC-nn` (incluida `Sin meta`: la recomendación es fijar la meta).
- Una recomendación es una **acción**: «Ajustar el precio de los combos en las aplicaciones», no «mejorar la rentabilidad».
- **Quién decide** es un usuario del brief (dueño, gerente, jefe de cocina…), el que toma la decisión que apoya el dashboard.
- **El KPI que lo mostrará** es uno de `modelo.json`: vuelve a medirse y dice si la acción funcionó.

## 4. Lecciones y limitaciones

- **Lecciones (tabla 4):** aprendizajes del proceso, no del negocio: calidad de datos, la herramienta, el trabajo en equipo, el orden del trabajo. Cada una dice dónde se vio (un punto del informe).
- **Limitaciones:** con `modo_datos: generado`, el párrafo `**Limitaciones.**` dice que los datos se generaron para el proyecto y que los resultados dependen de esa calibración; no se afirma nada sobre una empresa real.

## 5. Errores frecuentes

| Error | Cómo evitarlo |
|---|---|
| Concluir «cumplido» porque el valor «casi» llega a la meta | Se compara el número: sin redondear |
| Inventar la meta de un KPI pendiente para poder concluir | Se declara que no se puede concluir y se recomienda fijar la meta |
| Una conclusión para el proyecto entero y ninguna por objetivo | Una `CNC-nn` por cada `OE-nn` y una por el `OG-nn` |
| Recomendaciones genéricas («mejorar el margen») | Acción concreta, usuario del brief y KPI que la mide |
| Una cifra que no está en `valores.json` | Se cita solo lo que el equipo midió |
| Decir que los resultados describen a una empresa real | Se declara la limitación de los datos generados |

## 6. Validación

`python3 .claude/skills/_shared/validate_run.py <corrida>` aplica `rules/conclusions.py`: encabezado exacto, una conclusión por objetivo, el estado recalculado, el respaldo contra `valores.json` y 2.5, la meta pendiente declarada, las recomendaciones (conclusión, usuario del brief, KPI del modelo, una por cada conclusión que no cumple), las lecciones, la limitación de datos generados, los códigos citados y los títulos de tabla. Antes de validar, la skill invoca al agente `revisor-redactor` con las rutas de `secciones/5.md` (reglas en `common/redaccion/guia.md`).

## 7. Checklist
- [ ] Encabezado exacto y una conclusión por `OE-nn` y por `OG-nn`.
- [ ] Estado de cada conclusión calculado; respaldo con valores de `valores.json` y metas de 2.5.
- [ ] KPI sin meta declarado; la meta no se inventa.
- [ ] Recomendaciones ligadas a una conclusión, con usuario del brief y KPI del modelo.
- [ ] Lecciones del proceso y limitaciones (datos generados).
- [ ] Todas las tablas con `Tabla N: título`; sin términos de `policy.json`.
