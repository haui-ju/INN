# Tasks

## 1. Prueba corta en Miro (decide D1 a D3)

- [x] 1.1 Crear un tablero de prueba con `board_create` y dibujar 1 pantalla con `canvas_create_from_svg` tras cargar la guía del composer (pasos `design` y `dsl`); verificar con `canvas_read_as_svg` que el frame existe, es legible y sus elementos son editables
- [x] 1.2 Dibujar una segunda pantalla con un par antes/después y verificar que las dos secciones (v1 y v2) quedan separadas y con un solo tamaño de frame
- [x] 1.3 Registrar los parámetros que exige `board_create` (equipo o espacio) y si la creación devuelve identificadores de frame utilizables; verificar anotando el resultado en `design.md` (Open Questions) y cerrando las dos preguntas
- [x] 1.4 Medir el costo aproximado en tokens por pantalla durante la prueba y verificar que queda anotado para decidir si se dibuja por sección o por pantalla
- [ ] 1.5 Borrar el tablero de prueba y verificar que ya no aparece en `board_search_boards`

## 2. Estructura de la skill nueva

- [x] 2.1 Crear `.claude/skills/make-design-thinking-prototypes/` con `SKILL.md` en inglés (frontmatter `name: make-design-thinking-prototypes`, descripción con los disparadores) y verificar que la skill aparece en la lista de skills disponibles
- [x] 2.2 Escribir en `SKILL.md` el flujo de D4 (preflight, selección de corrida, plan y confirmación, dibujo, verificación, escritura) y las reglas de las specs; verificar que cada requisito de `design-thinking-prototype-mockups` tiene una instrucción correspondiente
- [x] 2.3 Crear `references/wireframe-kit.md` con los patrones SVG validados en el paso 1 (barra superior, campo, botón, lista, tarjeta, aviso de error, estado vacío) y verificar que cada patrón fue usado al menos una vez en la prueba

## 3. Lectura de la corrida

- [x] 3.1 Crear `scripts/read_run.py` que reciba la ruta de una corrida y emita JSON con `PAN`, `FLU`, `REQ`, `HAL-T` (con severidad y pantalla afectada) y la herramienta declarada; verificar ejecutándolo sobre `project/design-thinking/10-11-2026-00-00-46` y comprobando 6 `PAN`, 3 `FLU`, 5 `REQ` y 5 `HAL-T`
- [x] 3.2 Hacer que el script reporte con un error claro la ausencia de la fase 4 o de la fase 5; verificar con copias temporales de la corrida sin esos archivos
- [x] 3.3 Añadir `scripts/find_runs.sh` que liste las corridas de la más reciente a la más antigua; verificar su salida ordenada contra `ls`

## 4. Parcheo de documentos

- [x] 4.1 Crear `scripts/patch_run.py` con la tabla de reemplazos de D5 y la escritura de `bloques/fase-4-prototipar/miro.md`; verificar sobre una copia temporal que el enlace aparece en `pantallas.md`, `escenarios.md`, `documento.md` (3.1.5.3) y `anexos.md` (D.3)
- [x] 4.2 Hacer el script idempotente y que reporte las cadenas esperadas que no encuentre sin modificar nada; verificar ejecutándolo dos veces y comparando con `diff`
- [x] 4.3 Comprobar el requisito de texto limpio: buscar con `grep` las palabras «simulado», «ilustrativo», «ejemplo» e «inventado» en los archivos parcheados y verificar que no aparecen, y que `README.md` no cambió
- [x] 4.4 Documentar el uso de los scripts en un `README` al mismo nivel que la skill y verificar que los comandos documentados se ejecutan tal como están escritos

## 5. Integración de la skill con Miro

- [x] 5.1 Implementar en la skill el preflight con `user_who_am_i` y el mensaje de autenticación; verificar el comportamiento simulando la falta de autenticación y comprobando que no se escribe ningún archivo
- [x] 5.2 Probar la ejecución completa sobre una copia temporal de la corrida existente con el plan por defecto (6 pantallas v1 y las pantallas v2 con severidad 2 o más); verificar que el tablero tiene el número de frames del plan y que `miro.md` lista cada `PAN`
- [x] 5.3 Probar un plan modificado (3 pantallas v1) y un caso fuera de rango (8 pantallas); verificar que se muestra el aviso y que se respeta la decisión del usuario
- [x] 5.4 Probar la segunda ejecución sobre una corrida con `miro.md`; verificar que la skill pregunta entre actualizar o crear un tablero nuevo
- [x] 5.5 Probar con una corrida sin fase 4; verificar que la skill deriva a `make-design-thinking` y no crea tablero

## 6. Ajustes en `make-design-thinking`

- [x] 6.1 Parametrizar `scripts/reference/build.py` para que los conteos y textos de pantallas (fase 4 y v2 de fase 5) salgan de las listas de datos y añadir `assert` de cobertura de cada `REQ`; verificar generando en una carpeta temporal con 3 pantallas y con el valor por defecto, y comprobando que los documentos coinciden con el número elegido
- [x] 6.2 Actualizar `SKILL.md` de `make-design-thinking`: pregunta de pantallas por fase en el plan, fila de pantallas en la tabla de cantidades y referencia a la skill nueva; verificar que la tabla del plan coincide con `specs/design-thinking-package-generation`
- [x] 6.3 Actualizar `scripts/reference/README.md` y la plantilla `common/design-thinking/models/dt-4b-inventario-pantallas.md` para que no fijen una herramienta y admitan un enlace al tablero; verificar que los enlaces relativos siguen resolviendo con el chequeo de enlaces usado en el proyecto

## 7. Verificación final

- [x] 7.1 Ejecutar `openspec validate add-design-thinking-prototypes-skill --strict` y verificar que no reporta errores
- [x] 7.2 Recorrer el flujo completo desde el nombre `make-design-thinking-prototypes` hasta el enlace en los cuatro documentos de una copia de la corrida, y verificar cada escenario de `design-thinking-prototype-mockups` contra el resultado
- [x] 7.3 Confirmar que ninguna ruta del repositorio sigue refiriéndose al nombre anterior `make-designthinking` o a `common/structure/models`, con `grep` sin coincidencias

## 8. Diseño profesional de los mockups (pedido tras la revisión del usuario)

- [x] 8.1 Renombrar `LEEME.md` a `README.md` en el paquete existente, el generador, las skills y los artefactos del cambio; verificar con `grep -rn LEEME` sin coincidencias y regenerando el paquete en una carpeta temporal sin diferencias con el existente
- [x] 8.2 Actualizar las specs y `design.md` con la composición de módulo, el flujo con flechas y las etiquetas v2; verificar con `openspec validate add-design-thinking-prototypes-skill --strict`
- [x] 8.3 Implementar `scripts/render_svg.py` (JSON de pantallas a SVG con marco de aplicación, llamadas, panel de referencias, puertos y conectores) con comprobaciones geométricas; verificar generando los módulos de la corrida actual sin errores de límites ni solapamientos
- [x] 8.4 Dibujar en el tablero de prueba los 6 módulos v1 con sus flechas y los módulos v2 de la corrida actual; verificar con `canvas_search` el número de frames, que cada llamada tiene su entrada de referencia y que los conectores existen
- [x] 8.5 Actualizar `SKILL.md`, `references/wireframe-kit.md`, `plan_run.py` (total de frames: v1 más un módulo por pantalla v2), `patch_run.py` (sección v2 sin pares) y el README; verificar ejecutando los scripts sobre una copia y comprobando el plan y `miro.md`
- [x] 8.6 Revisión visual del usuario del tablero y confirmación del estilo; verificar con su respuesta (esta tarea no la puede cerrar el agente)

## 9. Densidad y detalle profesional (segunda revisión visual)

- [x] 9.1 Reescribir `render_svg.py` con maquetación automática, escala de espaciado, componentes de aplicación (KPI, lista, tallas, filtros, segmentado, selector, aviso, resumen), marco de dispositivo y comprobación de densidad mínima del 70%; verificar renderizando las muestras sin errores y con un caso de prueba que debe fallar por pantalla vacía
- [x] 9.2 Reescribir `references/sample/v1.json` y `v2.json` con contenido denso y relevante; verificar que las 11 pantallas pasan la comprobación de densidad y que ningún control supera los 44 px
- [ ] 9.3 Dibujar la nueva versión en el tablero de prueba en un área libre; verificar con `canvas_search` los frames y las flechas
- [x] 9.4 Actualizar `screen-spec.md` y `wireframe-kit.md` con el nuevo vocabulario y reglas; verificar que cada componente del renderizador está documentado
- [x] 9.5 Revisión visual del usuario de la nueva versión; verificar con su respuesta (esta tarea no la puede cerrar el agente)

## Workflow follow-up

- Archivar el cambio cuando se cumplan los requisitos de revisión del proyecto, de modo que las dos capacidades pasen a `openspec/specs/`.
- Verificar el resultado archivado.
