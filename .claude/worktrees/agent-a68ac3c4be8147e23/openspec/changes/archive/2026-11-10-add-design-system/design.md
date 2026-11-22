# Design

## Context

Estado observado: el kit compartido (`_shared/`) ya tiene `projectcfg.py` (con `set-diseno` que respeta `fijada`), `runs.py` (corridas y forks) y `validate_run.py` (reglas genéricas y por códigos mediante `rules/<paso>.py` con `PREFIJOS`). `pipeline.json` define `01-design-system` (verbo `design`, carpeta `design-system`, `update: true`, requiere `00-init`). El campo `diseno` del config está en `null`. `common/` tiene `design-thinking/` (playbook y 17 plantillas con ficha, instrucciones, formato, ejemplo y checklist) como modelo de estructura. Las spec principales `project-config` (ubicación del diseño) y `run-versioning` (corridas, fork, texto limpio) ya aplican. No existe ningún HTML ni diseño visual del proyecto.

## Goals / Non-Goals

**Goals:** un sistema de diseño único y verificable; tokens legibles por otras skills; accesibilidad de color comprobada por script; un `-update` barato.

**Non-Goals:** aplicar el diseño a tableros o informe, crear pantallas del sistema, publicar o explorar en Claude Design, ejecutar las skills.

## Decisions

### D1. `tokens.json` como fuente única
```json
{
  "schema": 1,
  "color": {"claro": {"fondo": "#...", "superficie": "#...", "texto": "#...", "texto-secundario": "#...", "borde": "#...", "acento": "#...", "acento-texto": "#...", "exito": "#...", "alerta": "#...", "error": "#..."},
            "oscuro": { "...mismas claves..." }},
  "pares": [{"texto": "texto", "fondo": "fondo", "tipo": "normal"}, ...],
  "tipografia": {"familia": "...", "familia-mono": "...", "escala": {"xs": "...", "sm": "...", "base": "...", "lg": "...", "xl": "...", "2xl": "..."}, "peso": {...}, "interlineado": {...}},
  "espacio": {"1": "4px", "2": "8px", "3": "12px", "4": "16px", "6": "24px", "8": "32px"},
  "radio": {"sm": "...", "md": "...", "lg": "..."},
  "sombra": {"sm": "...", "md": "..."}
}
```
`pares` declara qué combinaciones se validan por contraste (y su tipo: normal, grande o interfaz). `DESIGN.md` documenta los mismos valores y `preview.html` los usa como variables CSS. **Alternativa:** `DESIGN.md` como fuente; descartada porque cuesta leerlo con scripts.

### D2. Valores por defecto de estilo
Minimalista: escala de grises fríos, un solo acento, sin degradados. Moderno: radio medio (6 a 12 px), sombras suaves, espacio amplio, tipografía sans del sistema. Profesional: acento sobrio (azul o verde azulado) y color de estado reservado a estados. Son el punto de partida que se presenta en el plan y que el usuario cambia. En claro y oscuro los pares cumplen AA.

### D3. Tipografía autónoma
`tipografia.familia` es una pila del sistema (por ejemplo `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`) para que `preview.html` funcione sin conexión. Si el usuario pide una fuente concreta, se declara la fuente con la pila del sistema como respaldo y se avisa de que no se incrusta.

### D4. Vista previa generada por un script
`scripts/render_preview.py` (dentro de la skill) construye `preview.html` a partir de `tokens.json` y de la lista de componentes, de forma determinista. Así `preview.html` siempre coincide con los tokens y el `-update` solo cambia `tokens.json`, la tabla de `DESIGN.md` y vuelve a renderizar la vista previa. Es la misma excepción justificada al «no regenerar» que usa el cambio de tableros HTML: el archivo es derivado.

### D5. Validación por gancho
`validate_run.py` carga `rules/<modulo>.py` según la carpeta del paso. Hoy solo usa `PREFIJOS`. Se añade un gancho opcional `validar(run) -> [(archivo, mensaje)]` que se llama si el módulo lo define. `rules/design_system.py` implementa: claves de claro y oscuro iguales, contraste WCAG (luminancia relativa y razón (L1+0,05)/(L2+0,05)) de cada par, tokens citados en `DESIGN.md` (`color.claro.acento`, etc.) existentes, ausencia de recursos externos en `preview.html`, componentes con estados. Texto limpio y enlaces ya los cubre el validador genérico.

### D6. Estructura de `DESIGN.md`
Secciones: *Principios* (minimalista, moderno, profesional y qué implican aquí), *Color* (tabla claro y oscuro con uso de cada token), *Tipografía*, *Espacio, radio y sombra*, *Componentes* (encabezado, tarjeta, tabla, etiqueta de estado, barra de progreso, botón: estados, tokens, regla de uso), *Tema claro y oscuro*, *Accesibilidad*, *Cómo usarlo* (cómo otra skill lee `tokens.json`). Los ejemplos usan contenido realista del proyecto (por ejemplo una tarjeta de historia de usuario).

### D7. Playbook y modelos
`common/design-system/guia.md` con secciones 0 (reglas comunes y códigos: no usa códigos de trazabilidad; define nombres de tokens), 1 (principios), 2 (tokens), 3 (accesibilidad), 4 (componentes), 5 (HTML autónomo), 6 (cómo se consume), 7 (errores frecuentes y checklist). Modelos en `models/`: `ds-0-brief.md` (preferencias del usuario), `ds-1-tokens.md` (formato de `tokens.json` y tabla), `ds-2-componentes.md` (especificación por componente), `ds-3-design-md.md` (plantilla de `DESIGN.md`) y `README.md`.

### D8. Preguntas
El flujo es: leer config y `domain.md` (rubro, tipo, tono), preguntar tono y referencias, colores de marca, tipografía y modo oscuro, proponer, confirmar. No se pregunta lo que el config ya trae. Claude Design es una exploración opcional que la skill puede mencionar, pero no es parte del flujo.

### D9. Registro
Tras validar: `projectcfg.py register --step 01-design-system --run <carpeta>` y `projectcfg.py set-diseno --value project/design-system/<carpeta>/DESIGN.md`. En el `-update` con incidencias se usa `--no-mover` y no se cambia `diseno`.

## Risks / Trade-offs

- [Paleta que no gusta] → Se confirma antes de escribir y el `-update` la cambia sin rehacer todo.
- [Contraste AA calculado por script difiere de herramientas externas] → Se usa la fórmula WCAG 2.x estándar y se documenta; las pruebas incluyen pares conocidos (negro/blanco 21:1).
- [Fuente concreta no disponible sin conexión] → Pila del sistema como respaldo y aviso.
- [Gancho `validar` nuevo en el kit] → Opcional y con pruebas; no cambia el comportamiento de los pasos que no lo usan.
- [Dos fuentes de verdad] → `tokens.json` manda; el validador detecta desalineaciones de `DESIGN.md` y `preview.html`.

## Migration Plan

Sin migración: el paso es nuevo. `diseno` sigue en `null` hasta que el usuario ejecute la skill.

## Open Questions

- Si el sistema de diseño se explora o se publica en Claude Design (opcional y posterior).
- Cantidad de componentes adicionales que pedirán las skills de los tableros (se añaden con `01-design-system-update`).
