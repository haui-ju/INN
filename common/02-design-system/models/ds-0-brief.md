# Plantilla: Brief del sistema de diseño

| | |
|---|---|
| **Entregable** | Brief de diseño (se muestra al usuario como propuesta; se guarda en `README.md` solo como lista de decisiones) |
| **Entradas** | `project/config.yaml`, `project/domain.md`, preferencias del usuario |
| **Salida** | Decisiones de tono, referencias, acento, tipografía y modo oscuro, confirmadas |

## Instrucciones para el agente

1. Lee el config (tema, rubro, tipo de proyecto) y `domain.md`. No preguntes lo que ya consta.
2. Pregunta solo lo que falte: **tono** (formal, cercano), **dos o tres referencias visuales**, **colores de marca** si existen, **tipografía** preferida, **modo oscuro** (sí por defecto).
3. Si el usuario no tiene preferencias, propón un sistema completo según el rubro (guía, 1.2).
4. Muestra la propuesta con los valores principales y espera la confirmación.
5. Si pide una fuente concreta, avisa que se declara con respaldo del sistema y no se incrusta.

## Formato

```markdown
# Brief de diseño

- **Proyecto:** [nombre] · [rubro]
- **Tono:** [formal | cercano | técnico]
- **Referencias:** [referencia 1]; [referencia 2]
- **Acento:** [hex] ([origen: marca del usuario | propuesto por rubro])
- **Tipografía:** [serif de titulares + sans de texto + monoespaciada | fuentes solicitadas con respaldo]
- **Modo oscuro:** [sí | no]
- **Decisiones del usuario:** [cambios pedidos sobre la propuesta]
```

## Ejemplo

```markdown
# Brief de diseño

- **Proyecto:** Inventario digital y fichas de tallaje · ropa
- **Tono:** cercano
- **Referencias:** paneles de gestión sobrios con mucho espacio en blanco; tablas limpias
- **Acento:** #D4704F con texto oscuro y #B1472A para texto (tema base)
- **Tipografía:** Newsreader (titulares), Instrument Sans (texto) y monoespaciada del sistema
- **Modo oscuro:** sí
- **Decisiones del usuario:** bordes un poco más redondeados
```

## Checklist

- [ ] No se preguntó nada que ya constara en el config o en `domain.md`.
- [ ] Hay un solo acento.
- [ ] El usuario confirmó la propuesta.
