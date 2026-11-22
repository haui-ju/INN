# add-system-design: Diseño del sistema

**Cambio 11 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-system-design`).

## Valor
Documenta cómo se construye el sistema: arquitectura, datos, interfaz y plan de pruebas, trazados a los requerimientos y a las pantallas del Design Thinking.

## Skills
- `14-make-system-design` y `14-make-system-design-update`.

## Prerrequisitos
`06-make-design-thinking-prototypes`, `09-make-requirements`.

## Playbook
`common/system-design/guia.md` (lo crea este cambio): decisiones de arquitectura con alternativas (`ADR`), diagrama de componentes, modelo entidad-relación, lista de interfaces, cómo evolucionan los `PAN` del Design Thinking a pantallas finales, plan de pruebas (casos ligados a criterios de aceptación). Los diagramas se escriben como texto (por ejemplo Mermaid) para poder versionarlos.

Códigos propuestos: `ADR-nn`, `TBL-nn`, `CP-nn`; cita `RF`, `RNF`, `HU`, `CA` y `PAN`. (No usar `ENT`: ya lo emplea el Design Thinking.)

## Modelos y formularios (`common/system-design/models/`)
- `sis-1-arquitectura.md`, `sis-2-modelo-datos.md`, `sis-3-interfaz.md`, `sis-4-plan-pruebas.md`, `README.md`.

## Qué pregunta la skill
Stack (propone con alternativas y espera elección), alojamiento, restricciones de la empresa, módulos del sistema (inventario digital y fichas de tallaje u otros según el tema), qué pantallas del prototipo se conservan.

## Salida
`project/system-design/<corrida>/`: `arquitectura.md`, `modelo-datos.md`, `interfaz.md`, `plan-pruebas.md`, `diagramas/`.

## Índice
Alimenta **5.1, 5.2, 5.3, 5.5.1** y el **Anexo D.4**. **Este cambio corrige la marca de 5.4 a `[A1+]`** (la implementación avanza desde el primer sprint).

## Update
Cambiar una decisión de arquitectura, agregar una tabla o un caso de prueba; propaga a diagramas, interfaz y plan de pruebas.

## Validación
Cada `RF` mapeado a un componente, cada tabla referenciada por un componente, cada `CP` ligado a un `CA`, cada `PAN` usado tiene destino.

## Fuera de alcance
Escribir el código del sistema; la bitácora de implementación (cambio 12).

## Decisiones abiertas para el proposal
- Herramienta para renderizar los diagramas.
- Si `06` es prerrequisito duro o solo aviso cuando el usuario no usó Miro.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
