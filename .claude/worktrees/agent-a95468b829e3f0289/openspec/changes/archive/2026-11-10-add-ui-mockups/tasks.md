## 1. Pipeline, nombre y diseño de interfaz
- [x] 1.1 Agregar `14b-make-ui-mockups` a `pipeline.json` (orden 15, desplazar los siguientes, requiere 06, 10 y 14, update verdadero) y ajustar `test_pipeline.py` (nombre con letra, 21 pasos); sumarla al aviso `requiere_por_avance` de 19
- [x] 1.2 Numerar `### 5.3.1.` y `### 5.3.2.` en `sis-3-interfaz.md`, en `check_interfaz`, en las skills 14 y su update y en sus pruebas

## 2. Playbook y datos
- [x] 2.1 Crear `common/ui-mockups/` (guía, `README.md`, `ui-1-pantallas.md`, `ui-2-inventario.md`) con la lista cerrada de bloques y el esquema de `pantallas.json`
- [x] 2.2 Crear `mockups.py` (leer la tabla `UI` y los destinos de `interfaz.md`, validar el esquema, construir pantallas, galería, `leer-imagen/` e `inventario-ui.md`)
- [x] 2.3 Crear `rules/ui_mockups.py`, registrarla en `validate_run.py` y probar construcción y validación

## 3. Plantillas HTML
- [x] 3.1 Fuentes de `pantalla` y `galeria-pantallas` en `_build/src/visuales/` (modelo puro, Vista, bloques con componentes shadcn), `mock.json` y `README.md` en `common/html/`
- [x] 3.2 Compilar, actualizar el manifiesto, revisar en claro, oscuro y 360 px y agregar pruebas de modelo y montaje (datos y vacío)

## 4. Skills
- [x] 4.1 Crear `14b-make-ui-mockups` (fuentes, propuesta y confirmación, escritura, validación, registro) y `14b-make-ui-mockups-update` con su `references/dependencias.md`
- [x] 4.2 Prueba de que el `-update` solo cambia lo que depende del dato

## 5. Índice e informe
- [x] 5.1 `model1.md`: 5.3.1, 5.3.2 `(incluye imagen)`, D.5 `(incluye imagen)` y quitar la marca de 5.3
- [x] 5.2 `report_map.json` y `report.py`: fuente de D.5, marcador de la galería en 5.3.2 y de cada `UI-nn` en D.5 con su explicación; pruebas
- [x] 5.3 Actualizar `common/html/README.md` y `DESIGN.md`, `common/report/guia.md` y las pruebas del índice

## 6. Cierre
- [x] 6.1 Ejecutar la suite completa, `openspec validate add-ui-mockups --strict` y `openspec validate --specs --strict`
