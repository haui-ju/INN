---
name: 00-init
description: Crea project/config.yaml (fuente única de los datos técnicos del proyecto de Inteligencia de Negocios, con comentarios por campo): nombre, rubro, si se aplica a una empresa (por RUC) o es propio, equipo con rol opcional, modo de datos y la lista de secciones del informe, todas pendientes. El núcleo del proyecto (tema, problemática, objetivos, alcance, fechas) y project/domain.md los define después 01-make-project-brief. Úsala primero, antes de cualquier otra skill numerada, o cuando el usuario pida "00-init" o "inicializar el proyecto". Para cambiar algo ya creado usa 00-init-update.
---

# 00-init

Crea `project/config.yaml` con los **datos técnicos** del proyecto de BI. El **núcleo** (tema, problemática, objetivos, alcance, usuarios, fuentes de datos previstas y fechas de inicio y entrega) y `project/domain.md` los define el usuario en `01-make-project-brief`, que es la siguiente skill. Todas las skills numeradas leen el config y el brief en lugar de volver a preguntar.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py show | validate | register | check | secciones | current | salida | set-diseno`
- Biblioteca: `.claude/skills/_shared/projectcfg.py` (`new_config`, `load`, `save`). Al guardar, cada campo lleva a su derecha un comentario breve que explica el valor y las otras opciones.
- Orden, prerrequisitos y secciones del informe de cada skill: `.claude/skills/_shared/pipeline.json`.

## Reglas

- Pregunta todo lo necesario con `AskUserQuestion` o en texto y **pide confirmación del resumen antes de escribir**.
- Propone valores cuando puedas deducirlos (desde `apuntes.md` o desde una corrida existente); el usuario los acepta o corrige.
- **No asumas que existe una empresa.** La consigna admite una empresa real o una propia. Pregunta siempre si se aplica a una empresa.
- Si hay empresa, pide **solo el RUC**; no pidas su nombre, sus datos se buscan con el RUC.
- El config **no guarda credenciales** ni enlaces con permisos privados.
- Ningún texto del config dice que algo es falso, inventado, de prueba o simulado; `modo_datos` vale `generado` o `real`.
- **No preguntes el tema ni las fechas, ni crees `domain.md`:** son del brief (`01-make-project-brief`).
- Si `project/config.yaml` ya existe, no lo sobrescribas: ofrece `00-init-update` y detente salvo que el usuario pida rehacerlo.

## Flujo

1. **Revisa el estado.** Si `project/config.yaml` existe y es válido (`projectcfg.py validate`), propone `00-init-update` y no continúa. Si está mal formado o tiene un `schema` anterior, muestra el error y pregunta si lo rehace desde cero.
2. **Reúne contexto** sin preguntar lo que ya está escrito: `apuntes.md` (equipo).
3. **Pregunta lo que falta**, en pocas preguntas y con una propuesta por defecto cuando exista:
   - **Nombre** del proyecto y **rubro** o sector.
   - **¿El proyecto se aplica a una empresa?** Si sí → `tipo: empresa` y pide el **RUC** (11 dígitos). Si no → `tipo: propio` y `ruc: null`.
   - **Equipo**: nombres de los integrantes y, si ya lo saben, la responsabilidad de cada uno (texto libre de hasta 60 caracteres, por ejemplo «Analista de datos» o «Desarrollador Power BI»); si no, el rol queda `null`.
   - **Modo de datos**: `generado` (datos generados para el proyecto, coherentes y realistas) o `real` (datos abiertos o autorizados por la empresa).
4. **Resumen y confirmación.** Muestra una tabla corta con el config. Ajusta hasta que el usuario confirme; recién entonces escribe.
5. **Escribe** `project/config.yaml` con `projectcfg.save(projectcfg.new_config(...))` (valida antes de guardar; incluye los comentarios). El tema queda vacío y el calendario sin fechas; los completa `01-make-project-brief`. `informe.secciones` queda con todas las secciones del informe en `pendiente`.
6. **Verifica** con `projectcfg.py validate` y `projectcfg.py secciones`, muestra la ruta creada y **sugiere `01-make-project-brief`** (define el tema, la problemática, los objetivos y las fechas y crea `domain.md`). Recuerda que `00-init-update` sirve para cambiar los datos técnicos después.

## Esquema (resumen)

Con comentarios por campo en el archivo real; ver `projectcfg.py` (`COMENTARIOS`).

```yaml
schema: 3
proyecto: {nombre, tema, tipo: empresa|propio, ruc: "11 dígitos"|null, rubro}   # tema lo completa 01
equipo: [{nombre, rol: null|"texto libre"}]
calendario: {inicio: null, entrega: null}    # los completa 01
modo_datos: generado|real
diseno: null            # lo completa 02-design-system
dominio: project/domain.md    # lo crea 01
informe:
  secciones:            # una por punto del índice, en orden; la marca cada skill al registrar su corrida
    "1.1": {skill: 03-make-business-diagnosis, run: null, estado: pendiente}
    ...
pasos: {}               # cada skill registra aquí su corrida vigente
```

`pasos.<skill>.run` apunta a la corrida vigente. Cada skill, al terminar, agrega su corrida al `historial` y mueve `run`, salvo que `fijada` sea `true`; además marca como `disponible` sus secciones de `informe.secciones`. El usuario puede editar `run` a mano. `12-make-report` arma el informe solo con las secciones disponibles.
