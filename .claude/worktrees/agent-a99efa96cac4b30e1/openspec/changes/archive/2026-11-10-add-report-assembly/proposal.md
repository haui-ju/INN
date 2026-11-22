# Proposal

## Why

Las skills 01 a 18 producen cada capítulo del informe en su propia corrida, pero nadie los junta: el documento que se entrega en cada avance (versión 1, 2 y final) hay que armarlo a mano, con el riesgo de olvidar un punto, numerar mal, repetir figuras o citar fuentes que no están en las referencias. El índice (`common/structure/model1.md`) ya dice qué punto entra en qué avance, pero ninguna skill lo aplica ni avisa qué falta antes de entregar.

## What Changes

- **Nueva skill `19-make-report`** (sin `-update`: se vuelve a ejecutar para cada avance): pregunta el avance (1, 2 o final), cómo tratar los puntos sin fuente (marcador de pendiente u omitirlos), el formato de salida y los cambios principales de esta versión; muestra el plan (puntos incluidos, fuente de cada uno, faltantes) y, con la confirmación, arma el documento acumulado en `project/report/<corrida>/` con `informe-avance-N.md`, `anexos/`, `evidencias/`, `faltantes.md` y `README.md`.
- **Armado determinista** con un script del kit (`report.py`: `plan`, `construir` y `render`): toma de cada corrida vigente los bloques que corresponden a cada punto del índice, los ordena, vuelve a numerar y titular los encabezados según el índice, renumera las figuras de forma consecutiva, copia las evidencias y compila las referencias bibliográficas. La skill no redacta contenido de los capítulos.
- **Tabla de correspondencia punto → paso** (`report_map.json`) y **prerrequisitos por avance**: `pipeline.json` gana `requiere_por_avance` para la skill 19 y `projectcfg.py check --skill 19-make-report --avance N` avisa solo de los pasos que alimentan ese avance (sin bloquear).
- **`faltantes.md`**: todo punto con marca de ese avance que no tiene corrida fuente, con el paso que lo produce; coincide con lo que el documento marca como pendiente u omite.
- **Portada y control del documento**: título, historial de versiones con las fechas de `avances` del config, capítulos que cambian según el índice y los cambios principales que informa el usuario.
- **Referencias bibliográficas** compiladas de una lista cerrada y verificada (`rep-9-referencias.md`): toda cita del documento tiene entrada y toda entrada está citada.
- **Formato de entrega:** el Markdown es la fuente; un HTML autónomo con el sistema de diseño es opcional (`report.py render`); otras conversiones (Word, PDF, Docs) las elige el usuario con herramientas propias y quedan fuera de la validación; una vista privada se publica solo con confirmación explícita.
- **Nuevo playbook `common/report/`**: `guia.md` (orden, marcas de avance, versiones acumuladas, figuras, referencias cruzadas, faltantes, formatos, errores, checklist) y `models/` con `rep-0-control-documento`, `rep-9-referencias` y `README.md`.
- **Validación propia del paso** (`rules/report.py`).

## Capabilities

### New Capabilities
- `report-assembly`: playbook y modelos del armado, skill `19-make-report`, tabla de correspondencia, documento acumulado por avance, faltantes, figuras, referencias, formatos de salida y su validación.

### Modified Capabilities
- `skill-pipeline`: prerrequisitos por avance para las skills que alimentan documentos acumulados (nuevo requisito; no cambia los existentes).

## Impact

- **Archivos nuevos:** `common/report/`, `.claude/skills/19-make-report/`, `.claude/skills/_shared/report.py`, `report_map.json`, `rules/report.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/pipeline.json` (campo `requiere_por_avance` de la skill 19), `projectcfg.py` (`check --avance`) y `validate_run.py` (registra la carpeta `report`).
- **Índice:** aplica todos los puntos y marcas de `common/structure/model1.md`; no se cambia ninguna marca.
- **Fuera de alcance:** generar el contenido de los capítulos (cambios 1 a 13), el manual de usuario (anexo C) y las capturas de herramientas de gestión (A.4), que no tienen skill y aparecen en `faltantes.md`; convertir a Word o PDF; ejecutar las skills.
- **Supuestos registrados:** cada versión es el documento acumulado (todo lo marcado hasta ese avance); el usuario aporta las evidencias gráficas; las fuentes bibliográficas se limitan a las ya verificadas en los playbooks.
