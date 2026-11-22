# Plantilla: Valores y capturas del equipo (`valores.json` y `capturas/`)

| | |
|---|---|
| **Entregable** | `valores.json` y `capturas/pag-nn.png` (con `capturas/pag-nn.md` opcional), en la corrida |
| **Punto** | Entrada de 3.2 y de los anexos C y D: lo que el equipo midió |
| **Códigos** | `KPI-nn` y `MED-nn`; la captura de `PAG-nn` es `pag-nn` |
| **Entradas** | el dashboard construido por el equipo en Power BI |
| **Salida** | el valor real de cada KPI y una captura por página, de los que sale todo lo que 3.2 cita |

## Instrucciones para el agente
1. **No lo escribes tú: lo entrega el equipo.** Pídeselo con una lista: el valor real de cada KPI tal como lo muestra el dashboard (con su unidad y el periodo), y una captura por página. Guárdalo en la corrida sin cambiar una cifra.
2. `valores.json` tiene `schema: 1` y un elemento por cada KPI de `modelo.json` en `kpis`: `codigo`, `valor` (número), `unidad`, `meta` (número, o `null` si el KPI no tiene meta) y `periodo`. `medidas` es opcional: `{codigo, valor}` de las medidas que el equipo quiera registrar.
3. La `meta` coincide con la de 2.5 (la cifra de «98 % o más» es `98`). Si 2.5 dice «Pendiente», va `null`.
4. Cada captura es `capturas/pag-nn.png`, con el número de su `PAG-nn` en minúscula. `capturas/pag-nn.md` (opcional) trae en una línea el pie de la captura.
5. Si falta el valor de un KPI o la captura de una página, no redactes 3.2: pídelos.
6. **Metas pendientes.** Con el valor real de un KPI sin meta, propón una meta con su justificación, pide la confirmación del usuario y **no la escribas en 2.5**: se registra con `07-make-data-model-kpi-update`. Después el equipo la agrega en `valores.json`.

## Formato

```json
{
  "schema": 1,
  "kpis": [
    {"codigo": "KPI-01", "valor": 0, "unidad": "%", "meta": 0, "periodo": "AAAA-MM"}
  ],
  "medidas": [
    {"codigo": "MED-08", "valor": 0}
  ]
}
```

## Ejemplo

```json
{
  "schema": 1,
  "kpis": [
    {"codigo": "KPI-01", "valor": 97.2, "unidad": "%", "meta": 98, "periodo": "2026-10"},
    {"codigo": "KPI-02", "valor": 8.4, "unidad": "%", "meta": 12, "periodo": "2026-10"},
    {"codigo": "KPI-03", "valor": 6.9, "unidad": "%", "meta": 3, "periodo": "2026-10"},
    {"codigo": "KPI-04", "valor": 71.0, "unidad": "%", "meta": 70, "periodo": "2026-10"},
    {"codigo": "KPI-05", "valor": 6.55, "unidad": "S/ por kg", "meta": null, "periodo": "2026-10"}
  ],
  "medidas": [
    {"codigo": "MED-08", "valor": 97.2}
  ]
}
```

## Checklist
- [ ] Un elemento por cada KPI de `modelo.json`, con `valor` numérico, `unidad` y `periodo`.
- [ ] La `meta` coincide con la de 2.5 (`null` si está «Pendiente»).
- [ ] Una captura `capturas/pag-nn.png` por cada página de 3.2.
- [ ] Ninguna cifra fue cambiada ni completada por la skill.
