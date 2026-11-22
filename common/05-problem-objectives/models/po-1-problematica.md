# Plantilla: Problemática central del negocio (`secciones/1.8.md`)

| | |
|---|---|
| **Entregable** | `secciones/1.8.md` |
| **Punto** | 1.8. Problemática central del negocio |
| **Códigos** | `CAU-nn` (copiados del Ishikawa) |
| **Entradas** | brief (problema principal, afectados, evidencia), Ishikawa vigente (1.7) |
| **Salida** | el enunciado del problema, sus afectados, sus causas principales y su evidencia |

## Instrucciones para el agente
1. La primera línea es `## 1.8. Problemática central del negocio`.
2. **Enunciado.** Dos o tres frases con el problema principal del brief (con sus cifras), a quién afecta y qué decisión se toma hoy sin datos.
3. **Afectados.** Del brief («Quién lo sufre»).
4. **Causas principales.** Una frase con el criterio de priorización y la tabla `Código | Causa principal | Categoría | Evidencia` con entre dos y cuatro causas **copiadas del Ishikawa** (código, categoría y texto iguales). La evidencia es un dato con su fecha o su fuente.
5. **Evidencia.** Viñetas con los datos que prueban el problema.

## Formato

```markdown
## 1.8. Problemática central del negocio

**Enunciado.** [Problema del brief con sus cifras; a quién afecta; qué se decide hoy sin datos.]

**Afectados.** [Áreas o personas.]

**Causas principales.** [Criterio de priorización.]

Tabla 1: Causas principales de la problemática

| Código | Causa principal | Categoría | Evidencia |
|---|---|---|---|
| CAU-01 | [texto del Ishikawa] | [categoría del Ishikawa] | [dato con fecha o fuente] |

**Evidencia.**
- [dato con fecha o fuente]
```

## Ejemplo

```markdown
## 1.8. Problemática central del negocio

**Enunciado.** Pollería Don Tito vende más, pero gana menos: las ventas crecieron 18 % en el último año, pero el margen neto cayó de 14 % a 8 %. La gerencia fija precios, producción y compras sin ver cuánto deja cada canal ni cuánto pollo se pierde por turno.

**Afectados.** La gerencia y el jefe de cocina, que deciden precios, producción y compras sin ver la rentabilidad por canal ni la merma.

**Causas principales.** Del diagrama de Ishikawa se priorizan las causas que más pesan en el margen y que una solución de BI puede medir y corregir con datos.

Tabla 1: Causas principales de la problemática

| Código | Causa principal | Categoría | Evidencia |
|---|---|---|---|
| CAU-01 | Precios iguales en todos los canales, sin considerar la comisión | Método | Las aplicaciones pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión, según el registro de ventas de 2026 |
| CAU-02 | Producción por turno sin pronóstico de demanda | Método | Merma de 7 % de los pollos preparados frente a un 3 % de referencia, según el control de producción de 2026 |
| CAU-04 | Precio del pollo vivo volátil y no monitoreado | Materiales | El precio del insumo cambia de una semana a otra en los registros de precios de 2026 |
| CAU-06 | Tres registros de ventas que no se cruzan: caja, aplicaciones y WhatsApp | Medición | Ningún reporte de 2026 consolida las ventas de los tres canales |

**Evidencia.**
- Las apps de delivery pasaron de 15 % a 35 % de las ventas y cobran entre 25 % y 30 % de comisión.
- La merma es de 7 % de los pollos preparados, frente a un 3 % de referencia.
```

## Checklist
- [ ] Encabezado exacto en la primera línea.
- [ ] El enunciado recoge el problema del brief con sus cifras.
- [ ] De dos a cuatro causas principales con el mismo código, categoría y texto que en el Ishikawa.
- [ ] Hay afectados y al menos una evidencia.
