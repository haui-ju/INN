# Procedencia

Modo de datos: generado (config del proyecto). Este sistema de diseño no usa datos.

Decisiones del equipo (respuestas a las preguntas de la skill):
- **Tono:** serio y oscuro, con los colores de Power BI.
- **Acento:** el amarillo de Power BI (#F2C811) en el tema oscuro; en el tema claro, un oro más profundo (#A67C00) para cumplir el contraste mínimo sobre fondos claros.
- **Tema por defecto:** oscuro (`tema-defecto` en `tokens.json`); el claro se activa con el botón.
- **Tipografía:** Segoe UI, como Power BI, con respaldo del sistema; no se incrusta.

Decisiones del agente:
- Partió de los tokens base y cambió la paleta, la tipografía, los radios (4, 6 y 8 px) y las sombras (mínimas).
- Verificó el contraste de los 12 pares declarados en ambos temas (el mínimo es 4,5:1 para texto y 3:1 para elementos de interfaz).
- Para respetar el tema por defecto se amplió el kit: `tokens.json` admite `tema-defecto` y las plantillas de `common/html/` lo leen.
