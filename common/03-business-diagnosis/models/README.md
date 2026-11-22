# Plantillas del diagnóstico del negocio

Formatos del playbook [`../guia.md`](../guia.md). Léelo primero: aquí solo está el formato.

## Convenciones
- **Estructura de cada plantilla:** ficha (entregable, punto, entradas, salida) → instrucciones para el agente → formato → ejemplo → checklist.
- **Encabezado exacto** en la primera línea de cada sección: `## 1.1. Nombre de la empresa`, `## 1.2. Misión y visión`, `## 1.3. Industria y tamaño` y `## 1.4. Modelo de negocio: Business Model Canvas`.
- **Rótulos y columnas exactos** (la validación y el visual los leen): `**Reseña.**`, `**Misión.**`, `**Visión.**`, `**Valores.**`, `**Relación con el proyecto.**`, `**Tamaño de la organización.**`, `**Lectura del modelo.**` y las tablas `Dato | Valor`, `Aspecto | Descripción` y `Bloque | Contenido`.
- El ejemplo es el caso Pollería Don Tito (proyecto con `tipo: propio`), el mismo del brief de ejemplo.

## Índice

| Plantilla | Genera |
|---|---|
| [bd-1-empresa](bd-1-empresa.md) | `secciones/1.1.md` |
| [bd-2-mision-vision](bd-2-mision-vision.md) | `secciones/1.2.md` |
| [bd-3-industria-tamano](bd-3-industria-tamano.md) | `secciones/1.3.md` |
| [bd-4-canvas](bd-4-canvas.md) | `secciones/1.4.md`, la figura `bmc` (`visuales/bmc.html` y `leer-imagen/bmc.md`) |

Orden de trabajo: se confirma el tipo, se revisan los datos modelados de `domain.md`, se muestra el plan y, con la confirmación, se escriben las cuatro secciones, `referencias.md` y `README.md`; luego se construye la figura y se valida.

## Archivos de la corrida

```
project/03-business-diagnosis/<DD-MM-AAAA-HH-MM-SS>/
├── secciones/1.1.md … 1.4.md
├── visuales/bmc.html y bmc.json      (visuales.py construir)
├── leer-imagen/bmc.md                (visuales.py construir)
├── referencias.md
└── README.md                         (procedencia; único lugar para decir qué dato es generado)
```

Ejemplo de `referencias.md` (una referencia por línea, APA 7, orden alfabético):

```markdown
Congreso de la República del Perú. (2013, 2 de julio). Ley N.° 30056, Ley que modifica diversas leyes para facilitar la inversión, impulsar el desarrollo productivo y el crecimiento empresarial. *Diario Oficial El Peruano*.
Osterwalder, A., & Pigneur, Y. (2010). *Business model generation: A handbook for visionaries, game changers, and challengers*. John Wiley & Sons.
```
