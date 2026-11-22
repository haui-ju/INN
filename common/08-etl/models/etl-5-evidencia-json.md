# Plantilla: Evidencia del equipo (`evidencia.json`)

| | |
|---|---|
| **Entregable** | `evidencia.json` en la raíz de la corrida |
| **Punto** | Entrada de 3.1 y de los anexos A y B |
| **Códigos** | `REG-nn`; los nombres son códigos de fuente (`FUE-nn`) o tablas del modelo |
| **Entradas** | lo que el equipo anotó en Power Query y, si las exportó, `data/salida/` |
| **Salida** | las cifras con las que se redacta y se valida el capítulo |

## Instrucciones para el agente
1. Pide al equipo los valores con preguntas concretas, una por regla (filas antes y después), una por fuente (filas leídas), una por tabla cargada (filas cargadas) y una por total (ventas, comisión y líneas). Escribe lo que responden, sin corregirlo ni completarlo.
2. `schema` es 1. `reglas` lleva `codigo`, `filas_antes` y `filas_despues`; `tablas`, `nombre` (un `FUE-nn` o una tabla del modelo) y `filas`; `totales`, `ventas_total`, `comision_total` y `lineas_total`.
3. Deja `verificacion` para el comparador: `python3 .claude/skills/_shared/etl_verificacion.py comparar --evidencia <ruta> --actualizar`. Si no hay diferencias, el estado es `coincide` y la lista de diferencias va vacía.
4. Si una cifra falta, no la estimes: pídela. Una regla sin cifras no se redacta.
5. Si el equipo corrige una cifra, cámbiala aquí primero y luego en 3.1 y en el anexo A.

## Formato

```json
{
  "schema": 1,
  "reglas": [{"codigo": "REG-01", "filas_antes": 0, "filas_despues": 0}],
  "tablas": [{"nombre": "FUE-01", "filas": 0}, {"nombre": "fPedidos", "filas": 0}],
  "totales": {"ventas_total": 0.0, "comision_total": 0.0, "lineas_total": 0},
  "verificacion": {"estado": "coincide", "diferencias": []}
}
```

## Ejemplo

```json
{
  "schema": 1,
  "reglas": [
    {"codigo": "REG-01", "filas_antes": 1600, "filas_despues": 1600},
    {"codigo": "REG-02", "filas_antes": 1600, "filas_despues": 1600},
    {"codigo": "REG-03", "filas_antes": 1600, "filas_despues": 1568},
    {"codigo": "REG-04", "filas_antes": 1568, "filas_despues": 1550},
    {"codigo": "REG-05", "filas_antes": 1550, "filas_despues": 1550},
    {"codigo": "REG-06", "filas_antes": 80, "filas_despues": 92}
  ],
  "tablas": [
    {"nombre": "FUE-01", "filas": 1200},
    {"nombre": "FUE-02", "filas": 400},
    {"nombre": "FUE-03", "filas": 80},
    {"nombre": "fPedidos", "filas": 1550},
    {"nombre": "fProduccion", "filas": 60},
    {"nombre": "fPrecioInsumo", "filas": 92},
    {"nombre": "dCalendario", "filas": 92},
    {"nombre": "dProducto", "filas": 12},
    {"nombre": "dCanal", "filas": 3},
    {"nombre": "dLocal", "filas": 2},
    {"nombre": "dTurno", "filas": 3}
  ],
  "totales": {"ventas_total": 79200.0, "comision_total": 9450.0, "lineas_total": 1550},
  "verificacion": {"estado": "coincide", "diferencias": []}
}
```

## Checklist
- [ ] Una fila por cada regla de 3.1, por cada fuente del brief y por cada tabla del modelo.
- [ ] Ninguna cifra estimada: todas las dio el equipo.
- [ ] `verificacion` la escribió el comparador.
