# Proposal

## Why

Con los requerimientos, las historias y el plan de sprints definidos, falta decidir **cómo se construye** el sistema: su arquitectura (5.1), el modelo de datos (5.2), el diseño de interfaz (5.3) y el plan de pruebas (5.5.1), más los diagramas técnicos (D.4). Hoy ninguna skill lo produce, y sin él la implementación (cambio 12) no tiene contra qué registrarse y las pruebas no se pueden trazar a los criterios de aceptación. Además, las pantallas del Design Thinking (`PAN`) son un prototipo: hay que decidir cuáles pasan al sistema, cuáles cambian y cuáles se descartan.

## What Changes

- **Nueva skill `14-make-system-design`**: propone, a partir de los RF, RNF, historias, `PAN` del prototipo y el contexto del proyecto, la arquitectura (decisiones con alternativas, componentes), el modelo de datos, el destino de cada pantalla y el plan de pruebas; **pide al usuario el stack, el alojamiento y las restricciones** con alternativas y espera su elección; escribe `project/system-design/<corrida>/` con `arquitectura.md`, `modelo-datos.md`, `interfaz.md`, `plan-pruebas.md`, `diagramas/` y `README.md`. Registra la corrida.
- **Nueva skill `14-make-system-design-update`**: cambia una decisión, un componente, una tabla, una pantalla o un caso de prueba y propaga a lo que depende (copia `-fork`, plan con confirmación, validación).
- **Nuevo playbook `common/system-design/`**: `guia.md` (decisiones de arquitectura con alternativas, componentes, modelo de datos, destino de las pantallas, plan de pruebas, diagramas como texto, errores frecuentes, checklist, referencias) y `models/` con `sis-1-arquitectura`, `sis-2-modelo-datos`, `sis-3-interfaz`, `sis-4-plan-pruebas` y un `README.md`.
- **Códigos de trazabilidad propios:** `ADR-nn` (decisión de arquitectura), `TBL-nn` (tabla), `UI-nn` (pantalla final) y `CP-nn` (caso de prueba). No se usa `ENT`, que ya es del Design Thinking.
- **Trazabilidad verificable:** todo `RF` está cubierto por un componente; todo `RNF` lo atiende una decisión o un componente; toda tabla pertenece a un componente; todo `PAN` del prototipo tiene destino; todo `CA` y todo `RNF` tienen al menos un caso de prueba (o figuran como «sin caso» con motivo).
- **Diagramas como texto** (Mermaid, en `diagramas/`): componentes y modelo entidad-relación obligatorios, secuencias opcionales. El kit no los dibuja: la validación comprueba que sean archivos de texto del tipo correcto y que mencionen todos los componentes y tablas; los visores con soporte Mermaid los muestran.
- **Marcas del índice** (`common/structure/model1.md`): 5.4, 5.4.1 y 5.4.2 pasan a `[A1+]`, porque la implementación avanza desde el primer sprint.
- **Prerrequisitos:** `14-make-system-design` pasa a requerir también `10-make-user-stories` en `pipeline.json` (los casos de prueba se ligan a los criterios de aceptación); sin mockups de `06` solo avisa, porque los `PAN` existen en el Design Thinking.
- **Validación propia del paso** (`rules/system_design.py`).

## Capabilities

### New Capabilities
- `system-design`: playbook y modelos del diseño del sistema, skills `14-make-system-design` y su `-update`, arquitectura, modelo de datos, destino de pantallas, plan de pruebas, diagramas y su validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/system-design/`, `.claude/skills/14-make-system-design/`, `.claude/skills/14-make-system-design-update/`, `.claude/skills/_shared/rules/system_design.py` y sus pruebas.
- **Archivos modificados:** `common/structure/model1.md` (tres marcas), `.claude/skills/_shared/pipeline.json` (prerrequisito de la skill 14), `.claude/skills/_shared/validate_run.py` (registra la carpeta `system-design`).
- **Consumidores:** `15-make-implementation-log` (módulos y tablas), `16-make-sprint-report`, `18-make-final-analysis` (resultados de pruebas), `19-make-report` (5.1, 5.2, 5.3, 5.5.1 y D.4).
- **Índice:** alimenta 5.1, 5.2, 5.3, 5.5.1 y D.4; corrige las marcas de 5.4.
- **Fuera de alcance:** escribir el código, la bitácora de implementación, los resultados de las pruebas, renderizar los diagramas, ejecutar las skills.
- **Supuestos registrados:** las alternativas de stack las propone la skill pero la elección es del usuario; los tipos de prueba son Unidad, Integración, Sistema y Aceptación; las categorías de calidad de los RNF son las de `common/requirements/`; las fuentes (formato de decisiones de arquitectura) se verifican antes de citarlas.
