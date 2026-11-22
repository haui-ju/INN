# Design

## Context

`report.py` arma el informe tomando bloques de las corridas fuente según `report_map.json`; `report_prosa.py` convierte a prosa lo que se lee mejor así y resume la bitácora y las pruebas hacia `anexos/bitacora-detalle.md` y `anexos/resultados-pruebas.md`, que es el antecedente de trasladar bloques a anexos. `rules/report.py` valida la estructura. El índice (`common/structure/model1.md`) fija los puntos estables 3.1.1 a 3.1.8 y los anexos B, D, E y F. Este change se aplica después de `improve-report-figure-explanations`, que ya añade propósito por tabla y nuevas explicaciones de figura; aquí no se tocan. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Prosa con pocos códigos: nombre primero, un código por mención, rangos para series.
- Que el usuario decida, bloque a bloque, qué va en el cuerpo y qué en un anexo.
- Eliminar repeticiones evidentes entre secciones.

**Non-Goals:**
- No se cambian ni se resumen los datos de las corridas fuente; el informe sigue sin redactar contenido de capítulo.
- No se quitan secciones del índice.
- No se reescribe el texto de las skills fuente para bajar códigos (eso exigiría `-update` masivos); el control se hace en el ensamblado.

## Decisions

**1. La densidad se controla en el ensamblado sobre la prosa, no sobre las tablas.** Un paso de normalización en `report_prosa.py` colapsa series consecutivas del mismo prefijo en rangos y valida el máximo por frase; las tablas se saltan por completo. *Alternativa descartada:* limitar códigos también dentro de las tablas; son las llaves de trazabilidad y quitarlas rompe las referencias cruzadas.

**2. «Nombre primero, código una vez» solo donde el ensamblado ya redacta.** Se aplica a la prosa que escribe `report_prosa.py` (objetivos, conclusiones, resúmenes de sprint, resúmenes en el cuerpo). Los párrafos que vienen tal cual de una corrida fuente solo se colapsan por rango y, si exceden el máximo, se avisa qué skill `-update` los produce, como ya hace el kit con otras incidencias. *Alternativa descartada:* reescribir esos párrafos al ensamblar; viola la regla de que `19` no redacta.

**3. Colocación por bloque declarada en `report_map.json`.** Una clave `trasladables` lista los cinco bloques con su punto, su colocación por omisión, su destino (G.1 a G.4) y la fuente del resumen del cuerpo. El resumen sale de datos ya calculados (por ejemplo, «44 casos de prueba: 40 pasaron…»), con el patrón de `bitacora-detalle.md`. La pregunta se añade a las de la skill 19 en una sola tanda (`AskUserQuestion` con una opción por bloque), después de la de pendientes y antes de confirmar; se guarda en el `README.md` de la corrida.

**4. Un anexo nuevo G en lugar de ampliar A.** El anexo A es «Evidencias de gestión ágil» (exportes y capturas) y C es el manual; mezclar historias, pruebas y glosario ahí confunde su propósito. G es nuevo, no choca con B, D, E y F, y solo existe cuando al menos un bloque se elige para anexo.

**5. Eliminar duplicados cambiando qué se arma, no qué dicen las fuentes.** En 4.6.1 el armado conserva solo la asignación historia→sprint y la dependencia, y remite a 4.4.2 para título, estimación y prioridad. 4.5 se arma solo cuando los criterios no van dentro de las historias (los valores por omisión actuales mantienen ambos, pero el resumen se acorta a una línea por historia). En 4.7 los participantes se listan una vez cuando las cuatro ceremonias coinciden y se anotan solo las diferencias.

**6. Validación determinista.** `check_densidad`: máximo de 2 códigos por frase y ninguna serie sin colapsar fuera de tablas; `check_colocacion`: un bloque trasladable aparece exactamente una vez (cuerpo o G), con resumen y enlace si va a G, y sin G si ningún bloque se trasladó. Los umbrales son constantes del kit.

## Risks / Trade-offs

- [El máximo de 2 códigos por frase puede chocar con párrafos que vienen de las fuentes] → La validación avisa como advertencia con la skill que lo produce hasta que se ajusten en `-update`; solo es error en la prosa que escribe el ensamblado.
- [Colapsar rangos puede ocultar un código que falta en medio de una serie] → Solo se colapsa si la serie es completa en la fuente; si hay huecos se conserva la lista.
- [Resúmenes en el cuerpo que se desactualizan frente al anexo] → Se calculan de los mismos datos que el anexo en la misma corrida.
- [Más preguntas en la skill 19] → Una sola pregunta con valores por omisión, que se acepta con un clic.
- [Conflicto de archivos con `improve-report-figure-explanations`] → Se aplica después; las tareas parten de leer su estado final de `report.py` y `rules/report.py`.

## Open Questions

- Ninguna que cambie las specs o las tareas; el máximo de códigos por frase se ajusta al medir contra el informe real.
