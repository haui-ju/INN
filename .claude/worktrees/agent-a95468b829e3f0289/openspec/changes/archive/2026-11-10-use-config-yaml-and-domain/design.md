# Design

## Context

Estado observado: `projectcfg.py` lee y escribe `project/config.json` (`schema: 1`) con `json`; `pipeline.json` marca `00-init` sin `update`; `00-init/SKILL.md` pregunta empresa por nombre; `project/config.json` existe con los datos del proyecto; las skills 05, 06 y 05-update mencionan `config.json`; `validate_run.py` y `runs.py` importan `projectcfg`. Python 3.14 sin PyYAML y la restricción es biblioteca estándar. El cambio 1 está archivado; este lo corrige antes de crear más skills.

## Goals / Non-goals

**Goals:** config legible con comentarios por campo; modelar proyectos con o sin empresa; un `domain.md` único para el dominio; poder cambiar datos sin repetir `00-init`.

**Non-goals:** ejecutar `00-init` o `00-init-update`; implementar la consulta del RUC fuera de la skill; crear `domain.md` ahora; cambiar el contenido de las corridas.

## Decisions

### D1. YAML mínimo propio en `yamlmini.py`
Sin PyYAML (no está instalado y el kit usa solo biblioteca estándar). El módulo lee y escribe un **subconjunto** de YAML: mapas anidados por sangría de 2 espacios, listas con `- ` (de escalares o de mapas), escalares (texto con o sin comillas, enteros, `true`/`false`, `null`), `{}` y `[]` vacíos, y comentarios `#`. Rechaza con línea y causa todo lo demás (anclas, flujos con contenido, multilínea). **Alternativa:** pedir PyYAML; descartada por la dependencia. **Alternativa:** TOML; descartada porque el usuario pidió YAML.

### D2. Comentarios definidos por esquema
`projectcfg.py` tiene una tabla `COMENTARIOS` (ruta del campo → texto breve). Al guardar, el escritor emite cada línea con su comentario a la derecha (`enfoque: B  # A comprador final · B dueño/operario · C ambos`), de modo que siempre estén y se conservan en cualquier escritura de las skills. **Límite:** comentarios propios que el usuario añada en el archivo no sobreviven a una escritura de una skill; los explicativos sí. Se avisa en el comentario de cabecera del archivo.

### D3. Esquema 2
```yaml
schema: 2
proyecto:
  nombre: ...
  tema: ...
  tipo: empresa | propio
  ruc: "20123456789" | null
  rubro: ...
enfoque: B
resultado_esperado: ...
equipo: [{nombre, rol}]
avances: [{n, sprint, fecha}] x3
modo_datos: generado | real
diseno: project/design-system/<corrida>/DESIGN.md | null
dominio: project/domain.md
pasos: {...}
```
`ruc`: 11 dígitos, solo con `tipo: empresa`; con `propio` debe ser `null`. Se elimina `empresa`. El lector rechaza `schema: 1`.

### D4. `domain.md`
Estructura: *Datos generales*, *Reseña*, *Misión*, *Visión*, *Valores*, *Objetivos*, *Productos o soluciones*, *Contexto*. Con `empresa`: datos de la búsqueda por RUC (razón social, estado, domicilio fiscal, actividad, inicio de actividades) con su fuente. Con `propio`: descripción de la solución, problema, usuarios, propósito y alcance. Cada dato sin fuente se plantea y se marca «(modelado por el agente, por no contar con X)». Los capítulos derivados (como el 1) copian el contenido **sin** el marcador, de modo que este solo consta en `domain.md`.

### D5. Búsqueda del RUC en la skill
`00-init` y `00-init-update` usan búsqueda web (WebSearch/WebFetch) con el RUC, muestran lo hallado con su fuente y piden confirmación; si no hay acceso o no hay resultados, plantean los datos y los marcan. No se guardan credenciales.

### D6. `00-init-update`
Sin fork (el config no es una corrida): lee el config, pregunta qué cambia, muestra un resumen de diferencias (antes → después), confirma, escribe con `projectcfg.save` y valida. Si cambian `tipo` o `ruc`, propone rehacer `domain.md` y confirma. Se añade `update: true` a `00-init` en `pipeline.json`.

### D7. Diseño dentro de `project/`
`diseno` apunta a `project/design-system/<corrida>/DESIGN.md`; `projectcfg.py set-diseno` lo actualiza (respeta `fijada` del paso `01-design-system`). Hasta que exista, vale `null`.

### D8. Migración (diferida)
La conversión de `project/config.json` a `project/config.yaml` la hace `00-init` o `00-init-update` cuando el usuario las ejecute, porque `tipo` y `ruc` son datos que solo él aporta. El JSON no se borra (el usuario pidió no borrar nada); `projectcfg.py` solo lee el YAML.

## Risks / Trade-offs

- [El YAML mínimo no cubre todo YAML] → Solo lee lo que escribe; rechaza lo demás con línea y causa; pruebas de ida y vuelta.
- [Se pierden comentarios propios del usuario al escribir] → Documentado en la cabecera; los explicativos se regeneran.
- [Búsqueda del RUC sin resultados o con datos distintos] → Confirmación del usuario y marcador «(modelado por el agente…)».
- [Quedan menciones de `config.json`] → `grep` final fuera de lo archivado.
- [`domain.md` aún no existe para el proyecto actual] → `check` lo avisa; se crea al ejecutar la skill.

## Migration Plan

1. Implementar `yamlmini.py` y `projectcfg.py` con sus pruebas.
2. Reescribir `00-init`, crear `00-init-update`, actualizar `pipeline.json`.
3. Reemplazar las menciones y verificar con `grep`.

## Open Questions

- Comentarios propios del usuario: ¿basta con el límite documentado o se requiere conservarlos? (por defecto, basta).
