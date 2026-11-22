# Design

## Context

Estado observado: `pipeline.json` define `14-make-system-design` (requiere `06-make-design-thinking-prototypes` y `09-make-requirements`, con `update`). La corrida de requerimientos aporta `rf.md` (`RF-nn`, prioridad, `REQ`), `rnf.md` (`RNF-nn` con categoría, métrica y meta) y su matriz; la de historias aporta `historias/HU-nn.md` con criterios `CA-nn`; el Design Thinking aporta los `PAN-nn` (inventario de pantallas, 4 a 6). El índice define 5.1 a 5.3, 5.5.1 y D.4, y marca 5.4 y sus dos subpuntos como `[A2+]`. `rules/user_stories.py` ya sabe leer la corrida vigente de requerimientos; `validate_run.defined_codes` lee los códigos del Design Thinking. La regla de texto limpio prohíbe, entre otras, la expresión «datos de prueba». Python de la biblioteca estándar; no hay herramienta para dibujar diagramas en el kit.

## Goals / Non-Goals

**Goals:** un diseño completo y trazable a los requerimientos, las historias y el prototipo; decisiones con alternativas; un plan de pruebas ligado a los criterios de aceptación; diagramas versionables.

**Non-Goals:** escribir código, la bitácora de implementación, los resultados de las pruebas, renderizar los diagramas, ejecutar las skills.

## Decisions

### D1. Salida
`arquitectura.md` (5.1), `modelo-datos.md` (5.2), `interfaz.md` (5.3), `plan-pruebas.md` (5.5.1), `diagramas/` y `README.md`. Cada documento lleva un título `# … · [proyecto]` y su sección `## 5.n. …` con el punto tras el número.

### D2. Arquitectura (`arquitectura.md`)
`## 5.1. Arquitectura del sistema`, una frase de resumen y tres tablas:
- **Decisiones:** `Código | Decisión | Alternativas consideradas | Motivo | RNF o contexto`, con `ADR-nn`. La skill propone al menos dos alternativas por decisión con ventajas y desventajas; el usuario elige. Incluye al menos las de stack y alojamiento.
- **Componentes:** `Componente | Responsabilidad | Tecnología | RF que cubre | RNF que atiende | Tablas`.
- Una línea `**Diagrama.** diagramas/componentes.mmd`.
Reglas: todo `RF` de la corrida vigente aparece en ≥1 componente; todo `RNF` aparece en ≥1 decisión o componente; los `RF`, `RNF` y `TBL` citados existen.

### D3. Modelo de datos (`modelo-datos.md`)
`## 5.2. Modelo de datos`: tabla de tablas `Código | Tabla | Descripción | Campos principales | Componente` (`TBL-nn`, campos como `nombre (tipo)` con `(PK)` en la clave primaria, al menos 2 campos) y tabla de relaciones `Tabla origen | Relación | Tabla destino | Cardinalidad` (`1:1`, `1:N` o `N:M`). Todo `Componente` existe en la arquitectura y toda tabla la cita algún componente.

### D4. Interfaz (`interfaz.md`)
`## 5.3. Diseño de interfaz`: tabla `PAN | Destino | Motivo` (destino `Se conserva`, `Se modifica` o `Se descarta`; todo `PAN` del Design Thinking vigente aparece) y tabla de pantallas finales `Código | Pantalla | PAN de origen | Historias | Cambios` (`UI-nn`; origen `—` en pantallas nuevas, que deben citar una historia; las pantallas de un `PAN` descartado no existen). Las historias citadas existen en la corrida vigente. Una línea `**Sistema de diseño.**` con la ruta de `diseno` del config o «Sin definir». Sin mockups de `06` se trabaja con los `PAN` del Design Thinking.

### D5. Plan de pruebas (`plan-pruebas.md`)
`## 5.5.1. Plan de pruebas`: `**Tipos de prueba.**` (Unidad, Integración, Sistema, Aceptación), `**Entorno.**` y la tabla `Código | Caso | Tipo | CA | RNF | Datos de entrada | Resultado esperado` (`CP-nn`). Cada caso cita ≥1 `CA` o `RNF` existentes; todo `CA` y todo `RNF` tienen ≥1 caso o figuran en la tabla opcional `### Sin caso de prueba` (`Código | Motivo`). **Se usa «Datos de entrada», nunca «datos de prueba»**, para respetar la regla de texto limpio.

### D6. Diagramas (`diagramas/`)
Mermaid como texto. Obligatorios: `componentes.mmd` (tipo `flowchart` o `graph`, menciona todos los componentes) y `modelo-datos.mmd` (`erDiagram`, menciona todas las tablas). Opcionales: `secuencia-*.mmd` (`sequenceDiagram`). La validación comprueba que cada archivo empiece con un tipo de diagrama Mermaid y que mencione los componentes o las tablas; no valida la sintaxis completa porque el kit no tiene un intérprete. Se ven con cualquier visor con soporte Mermaid; el `README.md` lo indica. El kit no genera imágenes.

### D7. Códigos
`ADR-nn`, `TBL-nn`, `UI-nn`, `CP-nn`. Se definen en la primera celda de tablas. Sin choque con los de Design Thinking (`ENT`, `CON`…), canvas, empresa, plan Lean, requerimientos, historias y plan de sprints.

### D8. Marcas del índice y prerrequisitos
En `model1.md`: 5.4, 5.4.1 y 5.4.2 → `[A1+]` (la implementación comienza en el primer sprint y se actualiza). En `pipeline.json`: `14-make-system-design` requiere además `10-make-user-stories`; el aviso de prerrequisitos ya no bloquea ni cambia otras skills.

### D9. Fuentes
Lista cerrada verificada por búsqueda antes de citar: el formato de registro de decisiones de arquitectura de Nygard (2011) y ISO/IEC 25010:2023 (ya verificada) para las categorías de calidad de los RNF. Máximo 1 o 2 citas por archivo. No se citan herramientas ni el modelo C4 salvo que se verifiquen.

### D10. Validación
`rules/system_design.py` (`PREFIJOS = ["ADR", "TBL", "UI", "CP"]`): resuelve con `projectcfg.current_run` los requerimientos (`rf.md`, `rnf.md`) y las historias (códigos `HU`/`CA`), y el Design Thinking (`PAN`), y comprueba estructura, cobertura (RF, RNF, tablas, `PAN`, `CA`), existencia de los códigos citados, coherencia documento↔diagrama y las citas. Sin una corrida vigente de requerimientos, de historias o de Design Thinking, un aviso por cada comprobación imposible.

### D11. `-update`
Patrón del cambio 1. Modos: decisiones y componentes, tablas y relaciones, pantallas, casos de prueba y diagramas. Todo cambio en un documento se refleja en el diagrama correspondiente (componentes, ER). Avisa de la bitácora de implementación y de los informes que citen los códigos afectados. `references/dependencias.md` relaciona cada código con los archivos que lo citan.

### D12. Playbook
`common/system-design/guia.md`: 0 reglas, 1 arquitectura, 2 modelo de datos, 3 interfaz, 4 plan de pruebas, 5 diagramas, 6 errores y checklist y Referencias. Plantillas `sis-1` a `sis-4` y `README.md`.

## Risks / Trade-offs

- [El diseño sale genérico] → La skill pregunta stack, alojamiento y restricciones, y las decisiones exigen alternativas y motivo ligados a RNF.
- [Diagramas con sintaxis inválida sin que el kit lo note] → Se valida tipo y contenido; el `README.md` indica abrirlos en un visor Mermaid; es una limitación explícita.
- [Plan de pruebas enorme] → Un caso por criterio de aceptación como mínimo, no más; la validación no exige casos extra.
- [«Datos de prueba» en el plan de pruebas choca con el texto limpio] → La guía y la plantilla usan «Datos de entrada»; la validación genérica lo detecta si se cuela.
- [Cambios en requerimientos o historias dejan el diseño desalineado] → La validación compara con las corridas vigentes y el `-update` corrige.

## Migration Plan

Se editan tres marcas de `model1.md` y el prerrequisito de la skill 14 en `pipeline.json`. Sin migración de datos: el paso es nuevo.

## Open Questions

- Si más adelante conviene un visor local de los diagramas (por ahora no).
- Si el modelo de datos debe incluir tipos y restricciones detalladas o basta con los campos principales (por ahora basta).
