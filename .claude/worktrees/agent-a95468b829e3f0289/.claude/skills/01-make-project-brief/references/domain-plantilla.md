# Plantilla de `project/domain.md`

Un solo archivo con todo lo que se sabe del dominio. Lo leen las skills del capítulo 1 (por ejemplo `03-make-business-diagnosis`, que toma de aquí el nombre, la misión, la visión, la industria y el tamaño) y no se duplica en otro lugar.

**Regla del marcador.** Todo dato que no tiene fuente se plantea a partir del rubro, el tema y el resto del contexto, y se marca **al lado, entre paréntesis**: `(modelado por el agente, por no contar con <qué faltó>)`. Ejemplos: `(modelado por el agente, por no contar con una misión publicada)`, `(modelado por el agente, por no contar con la reseña de la empresa)`. Un dato con fuente lleva su fuente: `(fuente: <sitio o documento>)`. Los capítulos que se generen a partir de este archivo copian el contenido sin el marcador.

## Plantilla con `tipo: empresa`

```markdown
# Dominio del proyecto

Tipo: empresa · RUC: <ruc>

## Datos generales
| Dato | Valor |
|---|---|
| Razón social | ... (fuente: ...) |
| RUC | ... |
| Estado y condición | ... |
| Tipo de contribuyente | ... |
| Domicilio fiscal | ... |
| Actividad económica | ... |
| Inicio de actividades | ... |
| Industria (CIIU) | ... |
| Tamaño (según ventas anuales y trabajadores) | ... |

## Reseña histórica
...

## Misión
...

## Visión
...

## Valores
- ...

## Objetivos de la empresa
- ...

## Productos o servicios
...

## Clientes y competencia
...

## Contexto del proyecto
Qué parte de la empresa toca el proyecto y quién es el contacto.
```

## Plantilla con `tipo: propio`

La consigna admite una empresa propia: aquí se describe esa empresa con lo que el usuario cuente. El problema, los usuarios y los objetivos del proyecto viven en el brief (secciones 2, 5 y 3); aquí no se repiten.

```markdown
# Dominio del proyecto

Tipo: propio (empresa planteada por el equipo, sin RUC)

## Datos generales
| Dato | Valor |
|---|---|
| Nombre comercial | ... |
| Actividad económica | ... |
| Industria (CIIU) | ... |
| Tamaño (según ventas anuales y trabajadores) | ... |
| Locales y canales | ... |

## Descripción de la empresa
Qué hace y cómo funciona, en pocas líneas.

## Misión
...

## Visión
...

## Valores
- ...

## Clientes y competencia
...

## Contexto del proyecto
Qué área de la empresa toca el proyecto de BI y quién usará el dashboard.
```
