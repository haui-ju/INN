# Plantilla: Nombre de la empresa (`secciones/1.1.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.1.md` |
| **Punto** | 1.1. Nombre de la empresa |
| **Entradas** | `domain.md` (datos generales, reseña), config (`tipo`, `ruc`), brief (sección 1) |
| **Salida** | presentación de la empresa con sus datos generales y su reseña |

## Instrucciones para el agente
1. La primera línea es `## 1.1. Nombre de la empresa`.
2. Un párrafo de presentación: qué hace la empresa, dónde y por qué canales vende.
3. Tabla `Dato | Valor` con, en este orden, **Razón social, Nombre comercial, RUC, Actividad económica, Inicio de actividades (opcional), Ubicación y Locales y canales (opcional)**. Los valores salen de `domain.md` sin el marcador de datos modelados.
4. **RUC:** con `tipo: empresa`, el del config; con `tipo: propio`, «No aplica (empresa planteada por el equipo)».
5. **Reseña.** De dos a cuatro frases: origen, hitos y situación actual.

## Formato

```markdown
## 1.1. Nombre de la empresa

[Párrafo de presentación.]

| Dato | Valor |
|---|---|
| Razón social | [razón social] |
| Nombre comercial | [nombre comercial] |
| RUC | [RUC del config o «No aplica (empresa planteada por el equipo)»] |
| Actividad económica | [actividad (CIIU nnnn)] |
| Inicio de actividades | [mes y año] |
| Ubicación | [distrito, ciudad] |
| Locales y canales | [locales; canales de venta] |

**Reseña.** [Origen, hitos y situación actual.]
```

## Ejemplo

```markdown
## 1.1. Nombre de la empresa

Pollería Don Tito es un restaurante de pollo a la brasa con dos locales en San Juan de Lurigancho, Lima. Atiende en salón, para llevar y por delivery, tanto con reparto propio como por aplicaciones.

| Dato | Valor |
|---|---|
| Razón social | Inversiones Tito Brasas S.A.C. |
| Nombre comercial | Pollería Don Tito |
| RUC | No aplica (empresa planteada por el equipo) |
| Actividad económica | Actividades de restaurantes y de servicio móvil de comidas (CIIU 5610) |
| Inicio de actividades | Marzo de 2019 |
| Ubicación | San Juan de Lurigancho, Lima |
| Locales y canales | Zárate y Canto Grande; salón, para llevar, delivery propio por WhatsApp, Rappi y PedidosYa |

**Reseña.** La pollería abrió su primer local en Zárate en 2019 con un horno y un salón para cuarenta personas. En 2022 abrió el segundo local en Canto Grande y desde 2023 vende por aplicaciones de delivery, que hoy son su canal de mayor crecimiento.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] Razón social, nombre comercial, RUC, actividad económica y ubicación presentes.
- [ ] El RUC corresponde al tipo de proyecto.
- [ ] El nombre comercial coincide con `domain.md`.
- [ ] Hay reseña y no lleva el marcador de datos modelados.
