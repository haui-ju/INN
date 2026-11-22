# Plantilla · PESTEL

Seis paneles, uno por factor (político, económico, social, tecnológico, ecológico y legal), con cada hallazgo, su código, su efecto en el negocio, su tipo (Oportunidad en tono de éxito o Amenaza en tono de error, siempre con texto) y su fuente. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual pestel …` lo hace; en una corrida, `visuales.py construir --visual pestel --run <corrida>`. **No se edita nada más** del HTML.

## De dónde salen los datos
De la tabla `Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente` de `secciones/1.5.md` de la corrida de `04-make-strategic-analysis`. Si cambia, se corrige con `04-make-strategic-analysis-update` y se vuelve a construir.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `factores`: seis objetos con `clave` (`politico`, `economico`, `social`, `tecnologico`, `ecologico`, `legal`), `nombre` e `items`; cada ítem trae `codigo`, `texto` (hallazgo), `efecto`, `tipo` (`Oportunidad` o `Amenaza`) y `fuente`.

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `pestel.png`).

## Datos de ejemplo y versión vacía
`mock.json` trae el PESTEL del caso Pollería Don Tito, para revisar el diseño. **La skill nunca lo usa como datos del proyecto.** `html_tpl.py limpiar --visual pestel` da la versión vacía, que muestra «Sin datos».
