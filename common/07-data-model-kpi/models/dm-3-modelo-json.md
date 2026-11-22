# Plantilla: Contrato de datos del modelo (`modelo.json`)

| | |
|---|---|
| **Entregable** | `modelo.json` en la raíz de la corrida |
| **Punto** | 2.4 y 2.5 (el mismo modelo y los mismos KPI, como datos) |
| **Códigos** | `FCT-nn`, `DIM-nn`, `REL-nn`, `KPI-nn` |
| **Entradas** | las secciones `2.4.md` y `2.5.md` ya escritas de la misma corrida |
| **Salida** | el archivo que leen la figura `modelo-datos` y las skills del capítulo 3 (ETL y dashboard) |

## Instrucciones para el agente
1. Escribe `modelo.json` **después** de las secciones y copia de ellas, sin cambiar nada, los códigos, nombres, granularidades, medidas, claves, atributos, jerarquías, relaciones y KPI.
2. `schema` es 1. Los nombres de las claves del JSON son los del formato: `hechos`, `dimensiones`, `relaciones` y `kpis`.
3. Cada medida lleva `nombre`, `agregacion` (como en la tabla de hechos) y `tipo` (`entero` o `decimal`), que es lo único que no está en las secciones.
4. Las jerarquías y los atributos son listas de textos; una dimensión sin jerarquías lleva `[]`. El `origen` de cada KPI es una lista de `tabla.campo`.
5. Si cambias una sección, cambia aquí lo mismo: la validación compara ambos y avisa cada diferencia.

## Formato

```json
{
  "schema": 1,
  "hechos": [{"codigo": "FCT-01", "nombre": "f[Nombre]", "granularidad": "Una fila por [grano]", "medidas": [{"nombre": "[medida]", "tipo": "decimal", "agregacion": "suma"}], "claves": ["[clave]_key"]}],
  "dimensiones": [{"codigo": "DIM-01", "nombre": "d[Nombre]", "clave": "[clave]_key", "atributos": ["[atributo]"], "jerarquias": []}],
  "relaciones": [{"codigo": "REL-01", "desde": "f[Nombre]", "hacia": "d[Nombre]", "campos": "[clave]_key", "cardinalidad": "*:1", "filtro": "Simple"}],
  "kpis": [{"codigo": "KPI-01", "nombre": "[indicador]", "formula": "[fórmula]", "medida": "[Medida]", "origen": ["f[Nombre].[campo]"], "meta": "[meta]", "frecuencia": "Mensual", "objetivo": "OE-01", "decision": "[decisión]"}]
}
```

## Ejemplo

El ejemplo de las plantillas `dm-1-modelo` y `dm-2-kpi`, como datos:

```json
{
  "schema": 1,
  "hechos": [
    {
      "codigo": "FCT-01",
      "nombre": "fPedidos",
      "granularidad": "Una fila por línea de pedido, canal y día",
      "medidas": [
        {
          "nombre": "cantidad",
          "tipo": "entero",
          "agregacion": "suma"
        },
        {
          "nombre": "venta_bruta",
          "tipo": "decimal",
          "agregacion": "suma"
        },
        {
          "nombre": "comision",
          "tipo": "decimal",
          "agregacion": "suma"
        },
        {
          "nombre": "costo_estimado",
          "tipo": "decimal",
          "agregacion": "suma"
        },
        {
          "nombre": "pollos_equivalentes",
          "tipo": "decimal",
          "agregacion": "suma"
        },
        {
          "nombre": "registro_valido",
          "tipo": "entero",
          "agregacion": "suma"
        }
      ],
      "claves": [
        "fecha_key",
        "producto_key",
        "canal_key",
        "local_key",
        "turno_key"
      ]
    },
    {
      "codigo": "FCT-02",
      "nombre": "fProduccion",
      "granularidad": "Una fila por local, turno y día",
      "medidas": [
        {
          "nombre": "pollos_preparados",
          "tipo": "entero",
          "agregacion": "suma"
        },
        {
          "nombre": "pollos_vendidos",
          "tipo": "entero",
          "agregacion": "suma"
        },
        {
          "nombre": "pollos_merma",
          "tipo": "entero",
          "agregacion": "suma"
        }
      ],
      "claves": [
        "fecha_key",
        "local_key",
        "turno_key"
      ]
    },
    {
      "codigo": "FCT-03",
      "nombre": "fPrecioInsumo",
      "granularidad": "Una fila por día",
      "medidas": [
        {
          "nombre": "precio_kg",
          "tipo": "decimal",
          "agregacion": "promedio"
        }
      ],
      "claves": [
        "fecha_key"
      ]
    }
  ],
  "dimensiones": [
    {
      "codigo": "DIM-01",
      "nombre": "dCalendario",
      "clave": "fecha_key",
      "atributos": [
        "fecha",
        "anio",
        "mes",
        "nombre_mes",
        "dia_semana",
        "es_feriado"
      ],
      "jerarquias": [
        "Año > Mes > Fecha"
      ]
    },
    {
      "codigo": "DIM-02",
      "nombre": "dProducto",
      "clave": "producto_key",
      "atributos": [
        "producto",
        "categoria"
      ],
      "jerarquias": [
        "Categoría > Producto"
      ]
    },
    {
      "codigo": "DIM-03",
      "nombre": "dCanal",
      "clave": "canal_key",
      "atributos": [
        "canal",
        "tipo_canal",
        "comision_pct"
      ],
      "jerarquias": []
    },
    {
      "codigo": "DIM-04",
      "nombre": "dLocal",
      "clave": "local_key",
      "atributos": [
        "local",
        "zona"
      ],
      "jerarquias": []
    },
    {
      "codigo": "DIM-05",
      "nombre": "dTurno",
      "clave": "turno_key",
      "atributos": [
        "turno",
        "hora_inicio",
        "hora_fin"
      ],
      "jerarquias": []
    }
  ],
  "relaciones": [
    {
      "codigo": "REL-01",
      "desde": "fPedidos",
      "hacia": "dCalendario",
      "campos": "fecha_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-02",
      "desde": "fPedidos",
      "hacia": "dProducto",
      "campos": "producto_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-03",
      "desde": "fPedidos",
      "hacia": "dCanal",
      "campos": "canal_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-04",
      "desde": "fPedidos",
      "hacia": "dLocal",
      "campos": "local_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-05",
      "desde": "fPedidos",
      "hacia": "dTurno",
      "campos": "turno_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-06",
      "desde": "fProduccion",
      "hacia": "dCalendario",
      "campos": "fecha_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-07",
      "desde": "fProduccion",
      "hacia": "dLocal",
      "campos": "local_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-08",
      "desde": "fProduccion",
      "hacia": "dTurno",
      "campos": "turno_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    },
    {
      "codigo": "REL-09",
      "desde": "fPrecioInsumo",
      "hacia": "dCalendario",
      "campos": "fecha_key",
      "cardinalidad": "*:1",
      "filtro": "Simple"
    }
  ],
  "kpis": [
    {
      "codigo": "KPI-01",
      "nombre": "Calidad de datos del ETL",
      "formula": "Registros válidos entre registros cargados",
      "medida": "% Registros válidos",
      "origen": [
        "fPedidos.registro_valido"
      ],
      "meta": "98 % o más",
      "frecuencia": "Por carga",
      "objetivo": "OE-01",
      "decision": "Confiar en las cifras del dashboard antes de decidir"
    },
    {
      "codigo": "KPI-02",
      "nombre": "Margen neto por canal",
      "formula": "(Venta bruta menos comisión menos costo estimado) entre venta bruta, por canal",
      "medida": "Margen neto %",
      "origen": [
        "fPedidos.venta_bruta",
        "fPedidos.comision",
        "fPedidos.costo_estimado",
        "dCanal.canal"
      ],
      "meta": "12 % o más en el margen neto global",
      "frecuencia": "Mensual",
      "objetivo": "OE-02",
      "decision": "Ajustar el precio de los combos en las apps de delivery"
    },
    {
      "codigo": "KPI-03",
      "nombre": "Porcentaje de merma por turno",
      "formula": "Pollos de merma entre pollos preparados, por turno",
      "medida": "% Merma",
      "origen": [
        "fProduccion.pollos_merma",
        "fProduccion.pollos_preparados",
        "dTurno.turno"
      ],
      "meta": "3 % o menos",
      "frecuencia": "Diaria",
      "objetivo": "OE-03",
      "decision": "Definir cuántos pollos hornear por turno y día de la semana"
    },
    {
      "codigo": "KPI-04",
      "nombre": "Participación del canal directo",
      "formula": "Ventas de los canales propios entre las ventas totales",
      "medida": "% Canal directo",
      "origen": [
        "fPedidos.venta_bruta",
        "dCanal.tipo_canal"
      ],
      "meta": "70 % o más",
      "frecuencia": "Mensual",
      "objetivo": "OE-02",
      "decision": "Ajustar el precio de los combos en las apps de delivery"
    },
    {
      "codigo": "KPI-05",
      "nombre": "Precio promedio del pollo vivo por kilogramo",
      "formula": "Promedio del precio diario por kilogramo en el periodo",
      "medida": "Precio pollo vivo",
      "origen": [
        "fPrecioInsumo.precio_kg",
        "dCalendario.fecha"
      ],
      "meta": "Pendiente",
      "frecuencia": "Semanal",
      "objetivo": "OE-02",
      "decision": "Anticipar compras ante subidas del precio del pollo vivo"
    }
  ]
}
```

## Checklist
- [ ] Mismos códigos, nombres, medidas, claves, atributos, relaciones y KPI que las secciones 2.4 y 2.5.
- [ ] Cada medida tiene `tipo` entero o decimal y la agregación de la tabla de hechos.
- [ ] Cada `origen` es una lista de `tabla.campo` que existe en el modelo.
- [ ] Es un JSON válido (sin comas finales ni comentarios).
