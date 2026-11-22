# Dependencias del diagnóstico del negocio

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/03-business-diagnosis/<corrida>/`). Las skills de `08` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y a quién llega

| Archivo | Viene de | Lo leen |
|---|---|---|
| `secciones/1.1.md` (datos de la empresa, reseña) | `domain.md`, config (`tipo`, `ruc`) | 12 (informe), visual `bmc` (nombre comercial) |
| `secciones/1.2.md` (misión, visión, valores, relación con el proyecto) | `domain.md`, brief | 12 |
| `secciones/1.3.md` (industria, tipo de cliente, competencia, tamaño) | `domain.md`, UIT del año | 04 (FODA y PESTEL), 12 |
| `secciones/1.4.md` (Canvas y lectura del modelo) | `domain.md`, brief | 04 (fortalezas y debilidades), 05 (columna Canvas de la matriz), visual `bmc`, 12 |
| `visuales/bmc.html`, `bmc.json`, `leer-imagen/bmc.md` | `secciones/1.4.md` y 1.1 (`visuales.py construir`) | 12 |
| `referencias.md` | citas de las secciones | 12 |

## Qué afecta cada cambio

| Cambio | Edición en la corrida | Antes | Skills `-update` a ejecutar después |
|---|---|---|---|
| Razón social, nombre comercial, actividad, ubicación o reseña | `secciones/1.1.md` (y la figura `bmc` si cambia el nombre comercial) | corregir `domain.md` | — |
| Misión, visión o valores | `secciones/1.2.md` | corregir `domain.md` | — |
| Sector, tipo de cliente o entorno competitivo | `secciones/1.3.md` | — | `04-make-strategic-analysis-update` (FODA y PESTEL que lo citen) |
| Ventas anuales, UIT o categoría de tamaño | `secciones/1.3.md` (ventas en UIT y categoría se recalculan) y `referencias.md` si cambia la UIT | — | — |
| Un bloque del Canvas o la lectura del modelo | `secciones/1.4.md` y la figura `bmc` | — | `04-make-strategic-analysis-update` si cambia una fortaleza o debilidad que se apoya en ese bloque; `05-make-problem-objectives-update` si la matriz de articulación cita ese bloque |
| Completar algo «Pendiente» | la celda pendiente | según la fila | las de la fila que corresponda |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Tipo de proyecto o RUC | `00-init-update` y luego `01-make-project-brief-update` (rehace `domain.md`) |
| Tema, problemática u objetivos | `01-make-project-brief-update` |
| PESTEL, FODA o Ishikawa | `04-make-strategic-analysis-update` |
| Colores o tipografía del visual | `02-design-system-update` y volver a construir la figura |
