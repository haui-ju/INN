# add-report-assembly: Armado del informe por avance

**Cambio 14 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-report-assembly`).

## Valor
Ensambla el documento de cada entrega (avance 1, avance 2 y avance final) a partir de las corridas vigentes, siguiendo las marcas `[A1]`, `[A2]` y `[A3]` del índice. Muestra qué falta antes de entregar.

## Skills
- `19-make-report`. **No tiene `-update`**: se vuelve a ejecutar para cada avance.

## Prerrequisitos
`18-make-final-analysis` en el pipeline; para los avances 1 y 2 solo se exige lo que ese avance incluye (ver decisiones abiertas).

## Playbook
No crea uno nuevo: el contrato es `common/structure/model1.md` (marcas de avance, reglas de contenido, historial de versiones). Se añade `common/report/guia.md` breve con las reglas de armado (orden, referencias cruzadas, numeración de figuras, historial de versiones).

## Modelos y formularios (`common/report/models/`)
- `rep-0-control-documento.md` (portada, historial de versiones con las fechas de `avances` del config), `rep-9-referencias.md`, `README.md`.

## Qué pregunta la skill
Qué avance armar (1, 2 o final), formato de salida (markdown por defecto; HTML con el sistema de diseño o conversión a otro formato a elección, el formato es libre), si omitir puntos sin fuente o dejar un marcador de pendiente.

## Salida
`project/report/<corrida>/`: `informe-avance-N.md` (o HTML), `anexos/` y `faltantes.md` (puntos con marca de ese avance que no tienen corrida fuente).

## Índice
Usa todos los puntos del índice. Cualquier ajuste del índice que haga falta se aplica aquí o en el cambio que lo origina.

## Update
No aplica.

## Validación
Cada punto marcado para ese avance tiene una fuente en una corrida vigente o aparece en `faltantes.md`; las referencias cruzadas resuelven; las figuras siguen la regla de pie de foto con código; no se repite contenido entre avances.

## Fuera de alcance
Generar el contenido de los capítulos (cambios 3 a 13).

## Decisiones abiertas para el proposal
- Prerrequisitos por avance: `pipeline.json` solo conoce un prerrequisito (`18`); hace falta una tabla de qué skills alimentan cada avance.
- Formato de entrega final y si se publica una vista privada.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
