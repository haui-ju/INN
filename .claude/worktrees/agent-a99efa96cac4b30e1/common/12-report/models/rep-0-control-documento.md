# Plantilla: Control del documento

| | |
|---|---|
| **Entregable** | Inicio de `informe.md` |
| **Punto** | Control del documento del índice |
| **Códigos** | No define códigos |
| **Entradas** | Config (`proyecto`, `equipo`, `calendario.entrega`), brief vigente (empresa) y lo que informa el usuario (curso y docente) |
| **Salida** | Título del informe, tabla de datos de la portada y nota de formato |

## Instrucciones para el agente

1. Pregunta al usuario el **curso** y el **docente** y pásalos a `report.py construir --curso … --docente …`. Si no los sabe, quedan «Pendiente».
2. El título, el tema, los integrantes (con su rol si lo tienen) y la fecha de entrega salen del config; la empresa, del brief vigente. No los vuelvas a preguntar: si están mal, se corrigen con `00-init-update` o `01-make-project-brief-update`.
3. Todo dato vacío dice «Pendiente» y se lista en `faltantes.md` («Datos de portada»).
4. Una sola entrega: **no** hay historial de versiones ni marcas de avance.
5. Lo escribe `report.py construir`; no se redacta a mano.

## Formato

```markdown
# Informe · [proyecto.nombre]

## Control del documento

| Campo | Dato |
|---|---|
| Título del proyecto | [proyecto.nombre] |
| Tema | [proyecto.tema] |
| Empresa | [Empresa del brief] |
| Curso | [lo que informa el usuario o Pendiente] |
| Docente | [lo que informa el usuario o Pendiente] |
| Integrantes | [nombre (rol), nombre] |
| Fecha de entrega | [calendario.entrega o Pendiente] |

**Formato de entrega.** Word o PDF, letra Arial 11, interlineado 1.5 y márgenes estándar. [...]
```

## Ejemplo

```markdown
# Informe · Rentabilidad por canal de Pollería Don Tito

## Control del documento

| Campo | Dato |
|---|---|
| Título del proyecto | Rentabilidad por canal de Pollería Don Tito |
| Tema | Un dashboard en Power BI para que la gerencia vea cuánto deja cada canal de venta y decida precios, producción y compras con datos. |
| Empresa | Pollería Don Tito, restaurante de pollo a la brasa con dos locales en San Juan de Lurigancho; pequeña empresa. |
| Curso | Inteligencia de Negocios |
| Docente | Pendiente |
| Integrantes | ariel, Piero (Analista de datos) |
| Fecha de entrega | 30-11-2026 |
```

## Checklist

- [ ] Están los siete datos, con «Pendiente» donde falte.
- [ ] Los pendientes figuran en `faltantes.md`.
- [ ] No hay tabla de versiones ni marcas de avance.
- [ ] La fecha de entrega es la del config.
