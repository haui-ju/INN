# Tasks

## 1. Playbook, modelos y esquema

- [x] 1.1 Crear `common/app-plan/guia.md` y `common/app-plan/models/` (plantilla de `implementation-plan.md` en español, plantilla de `plan.json` y secuencias base de cortes por tipo de componente); verificar leyendo que cubren backend, frontend, database y openrpa y que citan el tope de 4 a 6.
- [x] 1.2 Definir el esquema de `plan.json` (campos en inglés, `depends_on`, `covers`, `cross_component_deps`, `justification`) con un validador de esquema en `_shared/`; verificar con una prueba que acepta un plan válido y rechaza uno sin `acceptance`.

## 2. Validación

- [x] 2.1 Crear `_shared/rules/app_plan.py` con las comprobaciones de tope 4 a 6 (con justificación), cobertura exacta del PRD, existencia de flujos y tablas citados, dependencias hacia atrás sin ciclos y dependencias entre componentes; verificar con pruebas que falla cada caso de los escenarios de la spec (sin cubrir, doble cobertura, siete changes, ciclo, dependencia posterior).
- [x] 2.2 Añadir la comprobación de consistencia entre `plan.json` e `implementation-plan.md` y el texto limpio; verificar con una prueba donde el markdown tiene un change menos que el JSON.

## 3. Skill y su update

- [x] 3.1 Crear `.claude/skills/23-make-app-implementation-plan/SKILL.md` con fuentes obligatorias, flujo (leer la definición, proponer changes por componente, confirmar, escribir, validar, registrar) y herramientas; verificar con una ejecución sobre una definición de ejemplo con backend, database y openrpa que genera tres planes y ninguno de frontend.
- [x] 3.2 Crear `23-make-app-implementation-plan-update` (bifurcar, aplicar agregar, quitar, reagrupar o reordenar, dejar idénticos los archivos de otros componentes, revalidar); verificar con una prueba que fusionar dos changes del frontend no altera los bytes de los demás planes.
- [x] 3.3 Registrar el paso en `_shared/pipeline.json` (carpeta `app/implementation-plan`, prerrequisito la definición de la app, `update: true`) y confirmar su número con el orden real de los changes hermanos; verificar con `projectcfg.py check` que avisa si falta la definición.

## 4. Documentación y prueba de punta a punta

- [x] 4.1 Cubrir el flujo completo con una prueba que parte de una definición de ejemplo, genera planes, valida y registra la corrida; verificar que la suite de `_shared/tests/` pasa.
- [x] 4.2 Documentar el contrato de `plan.json` para el cascarón en la guía y en el README de la skill; verificar que `add-app-scaffold-skill` puede leerlo sin campos adicionales.

## Workflow follow-up

- Confirmar con el usuario la ubicación de las corridas y coordinar los códigos de funcionalidad con `add-app-definition-skills` antes de implementar.
