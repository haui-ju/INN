# Plantilla: Diagrama de Ishikawa (`secciones/1.7.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.7.md` y la figura `ishikawa` |
| **Punto** | 1.7. Diagrama de la problemática: Ishikawa |
| **Códigos** | `CAU-nn` |
| **Entradas** | brief (problema principal y evidencia), FODA (debilidades y amenazas), Canvas |
| **Salida** | el efecto (problema del brief) y sus causas agrupadas en las categorías 6M |

## Instrucciones para el agente
1. La primera línea es `## 1.7. Diagrama de la problemática: Ishikawa`.
2. Un párrafo que presenta el diagrama con su cita (Ishikawa, 1986).
3. **Efecto.** El problema principal del brief, **copiado sin cambios** (sección 2 del brief).
4. La marca `<!-- figura: ishikawa -->` en una línea sola.
5. Tabla `Código | Categoría | Causa | Evidencia`, ordenada por categoría: Método, Mano de obra, Materiales, Maquinaria, Medición y Medio ambiente (nombres exactos). Al menos seis causas en al menos cuatro categorías.
6. Cada causa es concreta y su evidencia cita el código FODA que la respalda o un hecho con su año.
7. **Lectura del diagrama.** Dos frases: dónde se concentran las causas y cuáles se pueden medir con datos.
8. Después de escribir: `python3 .claude/skills/_shared/visuales.py construir --visual ishikawa --run <corrida> --carpeta <corrida>/visuales`.

## Formato

```markdown
## 1.7. Diagrama de la problemática: Ishikawa

[Párrafo que presenta el diagrama, con su cita.]

**Efecto.** [problema principal del brief, sin cambios]

<!-- figura: ishikawa -->

Tabla 1: Causas del diagrama de Ishikawa

| Código | Categoría | Causa | Evidencia |
|---|---|---|---|
| CAU-01 | Método | [causa concreta] | [código FODA o hecho con año] |

**Lectura del diagrama.** [Dónde se concentran las causas y cuáles se pueden medir.]
```

## Ejemplo

```markdown
## 1.7. Diagrama de la problemática: Ishikawa

El diagrama de causa y efecto organiza por categorías las causas posibles de un problema para distinguir las principales de las secundarias (Ishikawa, 1986). Se usan las seis categorías del método 6M y el efecto es la problemática definida en el brief del proyecto.

**Efecto.** Las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %.

<!-- figura: ishikawa -->

Tabla 1: Causas del diagrama de Ishikawa

| Código | Categoría | Causa | Evidencia |
|---|---|---|---|
| CAU-01 | Método | Precios iguales en todos los canales, sin considerar la comisión | DEB-01 |
| CAU-02 | Método | Producción por turno sin pronóstico de demanda | DEB-02 |
| CAU-03 | Mano de obra | Pedidos de WhatsApp registrados a mano por la cajera | Observación en caja, 2026 |
| CAU-04 | Materiales | Precio del pollo vivo volátil y no monitoreado | AME-01 |
| CAU-05 | Maquinaria | El sistema de caja no se integra con las aplicaciones de delivery | DEB-03 |
| CAU-06 | Medición | Tres registros de ventas que no se cruzan: caja, aplicaciones y WhatsApp | DEB-03 |
| CAU-07 | Medición | No se mide la merma por turno ni el margen por canal | DEB-02 |
| CAU-08 | Medio ambiente | Competencia de cadenas y comisiones altas en las aplicaciones | AME-02, AME-04 |

**Lectura del diagrama.** Las causas se concentran en el método y en la medición: se fijan precios y se produce sin datos, y los datos que existen no se cruzan. Casi todas pueden medirse con las ventas, la producción y el precio del insumo, que es lo que integrará la solución de BI.
```

## Checklist
- [ ] Encabezado exacto, efecto igual al problema principal del brief y marca `<!-- figura: ishikawa -->`.
- [ ] Al menos seis causas en al menos cuatro categorías 6M, con su evidencia.
- [ ] Las causas citan debilidades o amenazas del FODA cuando corresponden.
- [ ] Hay lectura del diagrama y la cita de Ishikawa (1986) está en `referencias.md`.
