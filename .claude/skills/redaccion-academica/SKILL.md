---
name: redaccion-academica
description: Puerta de calidad de redacción para el informe del proyecto (capítulos, secciones de las skills, anexos): corre el revisor redaccion.py (frases de relleno, palabras infladas, gerundios de cierre, arranques repetidos, frases largas, ritmo uniforme, párrafos sin dato propio, siglas sin definir), propone los cambios agrupados, los aplica solo si el usuario los aprueba y vuelve a medir, sin cambiar cifras, códigos, citas ni tablas. Úsala cuando el usuario pida "mejorar la redacción", "pulir el informe", "revisar la calidad del texto", "que el texto sea más propio y específico", "revisión de redacción antes de entregar" o "bajar el porcentaje de IA".
---

# redaccion-academica

Pase editorial para textos en español de un informe técnico-académico. Se basa en los patrones de escritura automática que documenta el proyecto Humanizer (licencia MIT) y en la guía de Wikipedia «Signs of AI writing», adaptados al español y a un jurado universitario. **No** inyecta personalidad ni cambia el registro: busca claridad, precisión y variedad.

Las reglas viven en `common/redaccion/guia.md` (códigos `R-nn` e inmutables `I-n`); las skills que escriben secciones invocan al agente `revisor-redactor`, que aplica esas mismas reglas. Esta skill es la forma de pedir la revisión a mano.

## Objetivo y honestidad

Dejar el informe con la calidad que pide un jurado: texto específico del caso, claro, consistente y con fuentes. La política del curso puede limitar el contenido generado con IA (por ejemplo, un máximo de 20 % en Turnitin). Esta skill ayuda a **cumplir esa política con un texto mejor**, no a ocultar su origen, y **no predice** el puntaje de ningún detector: solo Turnitin, desde la cuenta de la institución, lo calcula. Lo que más baja el contenido genérico es el contenido propio del equipo; por eso el revisor marca los párrafos sin dato propio. Recomienda además:

- Que cada integrante lea y edite su capítulo y pueda explicarlo en la sustentación.
- Declarar el uso de IA si la política del curso lo pide.
- Preguntar al docente si permite enviar un borrador a Turnitin para ver el porcentaje real antes de la entrega.

## Alcance y límites

- Edita solo **prosa**. No toques: cifras, fechas, códigos (OE-01, CAU-03, KPI-02, FCT-01…), citas (Autor, año), nombres propios, enlaces, tablas, bloques de código ni marcadores «(INCLUIR IMAGEN: …)».
- No agregues hechos, datos ni evidencias. Si una frase no se puede mejorar sin inventar, déjala.
- Texto limpio: no escribas que los datos son simulados, de prueba o inventados.
- Una corrida de otra skill no se edita en su sitio: bifurca con su skill `-update` (`runs.py fork`) o trabaja sobre una copia y registra el cambio en su `README.md`.
- Pide confirmación antes de escribir si el cambio afecta más de un archivo.

## Qué corregir

1. **Apertura y cierre vacíos**: «En conclusión», «Es importante destacar que», «Cabe resaltar». Empieza por el contenido.
2. **Contrastes de escenario**: «no es X, sino Y» cuando nadie dijo X. Afirma Y.
3. **Tríadas forzadas** y listas de tres adjetivos sin apoyo. Deja los elementos que tengan evidencia.
4. **Inflado**: «fundamental», «clave», «robusto», «innovador», «integral», «transformador». Sustituye por el dato o elimina.
5. **Verbos huecos**: «sirve como», «representa», «constituye», «se erige» donde basta «es».
6. **Gerundios de relleno** al final de la frase («…permitiendo así optimizar…»). Parte la oración o corta.
7. **Pasiva y nominalizaciones en cadena** («se realizó la realización de»). Prefiere sujeto y verbo claros; en informes técnicos la pasiva refleja es válida si el agente no importa.
8. **Repetición de arranques**: tres frases seguidas con «Se…» o «El sistema…». Varía y conecta con causa, consecuencia, contraste o secuencia.
9. **Autoridad vaga**: «según expertos», «diversos estudios». Cita la fuente del proyecto o quita la frase.
10. **Rótulos y viñetas donde cabe un párrafo**, y encabezados decorativos. Convierte a prosa los listados de una línea por ítem cuando el contenido sea continuo.
11. **Residuos de herramienta**: rutas de archivos internos, «Pegar.», «Sin captura», etiquetas de plantilla, fechas «datos al …» en pies de figura.
12. **Términos inconsistentes**: fija una sola forma («dashboard» o «tablero») tras presentarlo y úsala siempre. Define cada sigla la primera vez.
13. **Lector equivocado**: no vuelvas a explicar al jurado conceptos que un capítulo anterior ya definió (por ejemplo, la arquitectura del capítulo 2); remite al punto.

## Herramientas

- `python3 .claude/skills/_shared/redaccion.py revisar <archivo.md> [--json] [--max-frase 40] [--estricto]`: avisa por línea, regla y tipo (`relleno`, `inflado`, `gerundio`, `contraste`, `frase-larga`, `arranque-repetido`, `ritmo`, `sin-dato`, `sigla`). Revisa solo la prosa: ignora tablas, código, encabezados, marcas de figura y títulos de tabla.
- `python3 .claude/skills/_shared/validate_run.py <corrida>` para comprobar que la corrida sigue válida después de editar.

## Cómo trabajar

1. Lee el texto completo y el índice del informe (`common/structure/model1.md`). Trabaja capítulo por capítulo sobre `informe.md` o sobre `secciones/<punto>.md` de la corrida.
2. **Mide antes:** corre `redaccion.py revisar` y guarda el conteo por tipo.
3. **Propón** los cambios agrupados por sección con «antes → después» de tres o cuatro ejemplos. Para `sin-dato`, pregunta al usuario qué cifra, código o fuente propia del caso va en ese párrafo; **nunca inventes el dato**. Si no hay dato, la frase se reescribe más corta o se elimina.
4. **Aplica** con Edit solo lo aprobado. Si el texto sale de una skill (p. ej. `04-make-strategic-analysis`), el cambio se hace en una corrida bifurcada con su `-update` y el informe se rearma con `12-make-report`; nunca se edita `informe.md` como única copia.
5. **Mide después** con el mismo comando y comprueba que no cambió ningún número, código ni cita (`diff` y `grep`). Repite hasta que queden solo avisos que el usuario decida conservar (por ejemplo, una frase larga que es una definición).
6. Informa el antes y el después por tipo de aviso, sin juicio sobre el autor, y recuerda las tres recomendaciones del apartado anterior.
