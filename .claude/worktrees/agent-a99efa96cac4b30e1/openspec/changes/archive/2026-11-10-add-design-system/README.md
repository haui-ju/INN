# add-design-system: Sistema de diseño

**Cambio 2 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-design-system`).

## Valor
Una identidad visual única, minimalista, moderna y profesional que reutilizan los tableros HTML (cambio 10), el informe y cualquier pantalla que se genere. Sin ella cada HTML se diseñaría por separado y se vería distinto.

## Skills
- `01-design-system` (verbo `design`) y `01-design-system-update`.

## Prerrequisitos
`00-init`.

## Playbook
`common/design-system/guia.md` (lo crea este cambio; es el playbook, no el diseño del proyecto): principios (minimalista, moderno, profesional), tokens (color, tipografía, espacio, radio, sombra), accesibilidad (contraste AA), tema claro y oscuro, componentes mínimos (tabla, tarjeta, etiqueta de estado, barra de progreso, encabezado), reglas para HTML autónomo (un archivo, sin dependencias externas salvo fuentes).

## Modelos y formularios (`common/design-system/models/`)
- `ds-0-brief.md`: brief de marca (sector, tono, referencias visuales, colores y tipografías preferidos).
- `ds-1-tokens.md`: tabla de tokens con valor claro y oscuro.
- `ds-2-componentes.md`: especificación de cada componente con estados.
- `ds-design-md.md`: plantilla de `DESIGN.md`.
- `README.md` de los modelos.

## Qué pregunta la skill
Sector y tono (formal, cercano), 2 o 3 referencias visuales, colores y tipografías que ya use la empresa, si quiere modo oscuro, si desea usar Claude Design para explorar y publicar una vista privada (opcional).

## Salida
`project/design-system/<corrida>/`: `DESIGN.md`, `tokens.json`, `preview.html` (muestra de los componentes), `README.md`. Todo vive dentro de `project/`, porque es del proyecto. Al terminar, la skill actualiza el campo `diseno` del config (`projectcfg.py set-diseno`) para que apunte al `DESIGN.md` vigente, salvo que el paso esté fijado.

## Índice
No alimenta puntos del informe; lo consumen los cambios 10 (tableros HTML) y 14 (armado).

## Update
Cambiar un color, una tipografía o un token: edita `tokens.json`, `DESIGN.md` y `preview.html`; el resto queda igual.

## Validación
Contraste AA de los pares texto/fondo declarados, todos los tokens usados en componentes existen, claro y oscuro completos, texto limpio.

## Fuera de alcance
Aplicar el diseño a tableros o al informe (cambios 10 y 14); crear pantallas del sistema (cambio 11).

## Decisiones abiertas para el proposal
- **Decidido:** el diseño es local, dentro de `project/design-system/<corrida>/`, y `diseno` del config se actualiza (spec `project-config`, cambio `use-config-yaml-and-domain`).
- ¿Además se explora o publica una vista privada con Claude Design? Opcional; depende de las herramientas disponibles.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
