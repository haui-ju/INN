# Tasks

## 1. YAML y config

- [x] 1.1 Implementar `.claude/skills/_shared/yamlmini.py` (leer y escribir el subconjunto de YAML con comentarios) con pruebas; verificar con `python3 -m unittest` la ida y vuelta de un config completo, el rechazo con línea y causa de una construcción no soportada y la conservación de los comentarios
- [x] 1.2 Migrar `projectcfg.py` a `project/config.yaml` con `schema: 2`, `proyecto.tipo` y `ruc` (11 dígitos, solo con `empresa`), `dominio`, `diseno` y la tabla `COMENTARIOS`; añadir `set-diseno` y el aviso de `domain.md` ausente en `check`; actualizar sus pruebas y las de `runs.py` y `validate_run.py`; verificar que todas pasan y que un config con `schema: 1` se rechaza
- [x] 1.3 Marcar `update: true` en `00-init` de `pipeline.json` y verificar que sigue siendo JSON válido, con 20 pasos y orden intacto

## 2. Skills

- [x] 2.1 Reescribir `00-init/SKILL.md` (pregunta si hay empresa y, si sí, solo el RUC; busca por RUC con confirmación; crea `config.yaml` y `domain.md` con el marcador de datos modelados); verificar que cubre cada requisito de `project-config`
- [x] 2.2 Crear `00-init-update/SKILL.md` (qué cambiar, diferencias antes→después, confirmación, comentarios conservados, validación y propuesta de rehacer `domain.md`); verificar que aparece en la lista de skills y cubre su requisito

## 3. Referencias

- [x] 3.1 Reemplazar las menciones de `config.json` por `config.yaml` en `05-make-design-thinking`, `06-make-design-thinking-prototypes`, `05-make-design-thinking-update`, `_shared/README.md` y los README de los cambios pendientes; ajustar `add-company-chapter` (lee `domain.md`, pregunta el tipo de proyecto) y `add-design-system` (diseño en `project/`) y `ROADMAP.md`; verificar con `grep` que no quedan menciones fuera de lo archivado y del JSON histórico

## 4. Verificación final

- [x] 4.1 Ejecutar `openspec validate use-config-yaml-and-domain --strict`, las pruebas del kit y la comparación del generador por defecto de Design Thinking contra el paquete existente usando un config YAML temporal; verificar que todo pasa

## Workflow follow-up

- Diferida (se hará cuando el usuario ejecute `00-init` o `00-init-update`): convertir `project/config.json` en `project/config.yaml` (el JSON no se borra) y crear `project/domain.md`; `tipo` y `ruc` los aporta el usuario en esa ejecución. Mientras tanto no existe `config.yaml` y las skills indicarán ejecutar `00-init`.
- Archivar el cambio y corregir directamente el texto «Purpose» de la spec `project-config` (nombra `config.json`).
- Continuar con el cambio `add-design-system`.
