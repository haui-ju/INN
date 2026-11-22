# Proposal

## Why

El config en JSON no admite comentarios, así que valores como `"enfoque": "B"` no dicen qué significa B ni qué otras opciones existen. Además, el diseño actual da por hecho que todo proyecto se aplica a una empresa y pide su nombre, cuando el proyecto puede ser propio o innovador, sin empresa. Y `00-init` no tiene homóloga de actualización, así que cambiar un dato obliga a editar el archivo a mano. Conviene corregirlo antes de crear el resto de skills, que dependen de estos datos.

## What Changes

- **Config en YAML con comentarios:** `project/config.json` pasa a `project/config.yaml` (`schema: 2`). Cada campo lleva a la derecha un comentario breve (qué significa, valor actual y otras opciones). Las skills conservan los comentarios al escribir. El lector/escritor usa solo la biblioteca estándar (un subconjunto de YAML acotado).
- **Tipo de proyecto:** `proyecto.tipo` vale `empresa` o `propio`. Con `empresa` solo se guarda el `ruc` (no el nombre); con `propio` el proyecto es una solución propia o innovadora sin empresa. Desaparece el campo `empresa`.
- **`project/domain.md`:** reúne todo lo conocido del dominio (datos generales, reseña, misión, visión, valores, objetivos, contexto). Con RUC, se busca la empresa por el RUC; con proyecto propio describe la solución. Lo que no se encuentra se plantea a partir del contexto y se marca al lado «(modelado por el agente, por no contar con X)».
- **Nueva skill `00-init-update`:** cambia datos del config y de `domain.md` ya creados, pregunta qué cambiar, muestra los cambios y confirma antes de escribir.
- **`00-init` ajustada:** pregunta si el proyecto se aplica a una empresa y, si sí, solo el RUC; crea el config y `domain.md`.
- **Diseño dentro de `project/`:** el sistema de diseño (`DESIGN.md`) vive en `project/design-system/<corrida>/` y el campo `diseno` del config apunta al vigente.
- **Migración diferida:** el `project/config.json` existente se convierte a `project/config.yaml` cuando el usuario ejecute `00-init` o `00-init-update` (aporta `tipo` y `ruc`); el JSON antiguo no se borra.

## Capabilities

### Modified Capabilities
- `project-config`: formato YAML con comentarios, tipo de proyecto y RUC, `domain.md`, `00-init` ajustada, `00-init-update` y ubicación del diseño.
- `skill-pipeline`: `00-init` pasa a tener homóloga `-update`; `19-make-report` sigue sin ella.
- `design-thinking-package-generation`: la recogida de información lee `project/config.yaml` y el contexto de `project/domain.md`.

## Impact

- **Código del kit:** `projectcfg.py` (YAML, esquema 2, comentarios, RUC), nuevo `yamlmini.py`, `pipeline.json`, pruebas.
- **Skills:** `00-init` (reescrita), nueva `00-init-update`, y menciones de `config.json` en `05-make-design-thinking`, `06-make-design-thinking-prototypes`, `05-make-design-thinking-update` y `_shared/README.md`.
- **Datos:** `project/config.yaml` y `project/domain.md` no se crean en este cambio: los generan `00-init` o `00-init-update` cuando el usuario las ejecute; `project/config.json` queda sin tocar.
- **Cambios pendientes:** se ajustan `add-company-chapter` (lee `domain.md` y pregunta el tipo de proyecto), `add-design-system` (ubicación en `project/`) y `ROADMAP.md`.
- **Fuera de alcance:** ejecutar `00-init` o `00-init-update`; consultar el RUC (lo hace la skill al ejecutarse, con búsqueda web y confirmación del usuario).
