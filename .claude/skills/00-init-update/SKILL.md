---
name: 00-init-update
description: Cambia los datos técnicos del config del proyecto (project/config.yaml) ya creado sin repetir todas las preguntas de 00-init: nombre, rubro, tipo de proyecto, RUC, equipo y roles, modo de datos o qué corrida es la vigente de un paso. El tema y las fechas de inicio y entrega se cambian con 01-make-project-brief-update. Úsala cuando el usuario pida "00-init-update", "cambiar el equipo", "asignar responsabilidades", "cambiar el RUC", "cambiar el nombre o el rubro" o "pasar a modo real".
---

# 00-init-update

Homóloga de `00-init`. Cambia los datos **técnicos** del config (el núcleo vive en el brief y se cambia con `01-make-project-brief-update`). Modifica solo lo que el usuario pida, muestra las diferencias, confirma y valida. El config no es una corrida, así que **no hay `-fork`**: se edita el archivo en su lugar.

## Herramientas

- `python3 .claude/skills/_shared/projectcfg.py show | validate | register | secciones | set-roles | set-diseno`
- Biblioteca: `.claude/skills/_shared/projectcfg.py` (`load`, `save`, `set_roles`). `save` valida y vuelve a escribir los comentarios de cada campo.

## Reglas

- Cambia **solo** lo pedido. Los demás campos quedan igual.
- Muestra siempre el cambio como `antes → después` y **espera confirmación** antes de escribir.
- No guardes credenciales. El texto no dice que algo es falso, inventado, de prueba o simulado.
- **El tema y las fechas de inicio y entrega no se cambian aquí:** si el usuario los pide, remítelo a `01-make-project-brief-update` (el brief manda y el config es su copia).
- Si el usuario cambia `tipo` o `ruc`, actualiza el config y remite a `01-make-project-brief-update` para rehacer `domain.md`; no lo reemplaces sin confirmación.
- `informe.secciones` no se edita a mano aquí: lo actualizan las skills al registrar su corrida. Si el usuario cambia `pasos.<skill>.run`, vuelve a registrar el paso para que sus secciones apunten a la nueva corrida.
- Las corridas ya generadas **no se actualizan solas**: avisa cuáles dependen del dato (por ejemplo el `tipo` afecta al diagnóstico del capítulo 1) y sugiere su skill `-update`.

## Flujo

1. `projectcfg.py validate`. Si no existe, ofrece `00-init`. Si no es YAML válido, muestra el error con su línea y propone corregirlo.
2. Muestra el resumen actual (proyecto, tipo, equipo con roles, modo de datos, corrida vigente de cada paso y secciones disponibles con `projectcfg.py secciones`) y pregunta **qué quiere cambiar** (AskUserQuestion o texto; admite varios cambios).
3. Para cada cambio, valida el valor:
   - `tipo`: `empresa` o `propio`; con `empresa` pide el RUC (11 dígitos); con `propio` el RUC pasa a `null`.
   - `modo_datos`: `generado` o `real`.
   - `equipo`: agregar, quitar o renombrar integrantes.
   - **Roles**: texto libre de hasta 60 caracteres por integrante, con `projectcfg.py set-roles --rol "Nombre=Rol" …`; solo admite personas que ya están en el equipo y cambia solo los nombrados.
   - `pasos.<skill>.run` y `fijada`: solo si el usuario quiere cambiar a mano qué corrida es la vigente; comprueba que la carpeta exista y luego registra el paso con `projectcfg.py register --step <skill> --run <corrida>` para actualizar sus secciones.
4. Si cambió `tipo` o `ruc`: indica que `domain.md` se rehace con `01-make-project-brief-update` (busca de nuevo por RUC con fuente y confirmación). Si el usuario solo quiere corregir un dato de `domain.md` (misión, visión, valores…), edita esa sección y conserva el resto.
5. Muestra el resumen de diferencias y **pide confirmación**.
6. Escribe con `projectcfg.save(cfg)` (o `set_roles`) y, si el usuario corrigió una sección, `project/domain.md`.
7. Valida con `projectcfg.py validate` y responde con lo cambiado, lo que quedó igual y las corridas que conviene actualizar.
