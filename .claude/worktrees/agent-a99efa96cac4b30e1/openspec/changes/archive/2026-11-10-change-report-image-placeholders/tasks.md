## 1. Marcadores en el armado
- [x] 1.1 Definir el formato del marcador (una sola expresión regular) y reemplazar `_convertir_informe` para que las líneas «Pegar» generen marcadores con su pie y su archivo sugerido (sin `![…](…)`, sin `reun.evid`)
- [x] 1.2 Declarar en `report_map.json` el visual de cada punto con imagen (`imagen_visual`) y generar el marcador de los puntos con marca de imagen que no tienen línea «Pegar» (visual de 13 o título y código del punto)
- [x] 1.3 Copiar bajo el marcador de un visual los puntos de `leer-imagen/<visual>.md` (sin título ni pie) tras «Cómo leer la figura:»; si falta, avisar sin bloquear ni listar en faltantes
- [x] 1.4 Renumerar los marcadores de forma consecutiva y actualizar las menciones «Figura n»
- [x] 1.5 Quitar la carpeta `evidencias/`, la copia de archivos y el aviso de evidencias ausentes

## 2. HTML y validación
- [x] 2.1 `md_a_html`: mostrar el marcador como recuadro «Incluir imagen» y no generar `<img>`
- [x] 2.2 `rules/report.py`: validar marcadores (numeración, pie con código o fecha, punto con imagen sin marcador, `![…](…)`, `evidencias/`, explicación cuando hay 13) y mantener faltantes solo para puntos sin fuente

## 3. Skill, playbook y pruebas
- [x] 3.1 Actualizar `19-make-report/SKILL.md` (reglas, flujo, cierre: qué imágenes preparar y que 13 aporta las explicaciones) y `common/report/guia.md` y `models/README.md`
- [x] 3.2 Ajustar fixtures y pruebas del reporte y agregar las de marcadores, explicación, numeración, HTML y validación
- [x] 3.3 Ejecutar la suite completa, `openspec validate change-report-image-placeholders --strict` y `openspec validate --specs --strict`
