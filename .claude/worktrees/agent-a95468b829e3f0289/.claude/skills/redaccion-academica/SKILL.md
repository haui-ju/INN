---
name: redaccion-academica
description: Revisa y mejora la redacción en español de textos del informe del proyecto (capítulos, bloques de las skills, anexos) para que se lean como un trabajo académico escrito por personas, sin muletillas de texto generado, sin cambiar cifras, códigos, citas ni tablas. Úsala cuando el usuario pida "humanizar", "mejorar la redacción", "pulir el informe" o "que no suene a IA" sobre project/.
---

# redaccion-academica

Pase editorial para textos en español de un informe técnico-académico. Se basa en los patrones de escritura automática que documenta el proyecto Humanizer (licencia MIT) y en la guía de Wikipedia «Signs of AI writing», adaptados al español y a un jurado universitario. **No** inyecta personalidad ni cambia el registro: busca claridad, precisión y variedad.

## Alcance y límites

- Edita solo **prosa**. No toques: cifras, fechas, códigos (RF-01, HU-03, TAR-12…), citas (Autor, año), nombres propios, enlaces, tablas, bloques de código ni marcadores «(INCLUIR IMAGEN: …)».
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
12. **Términos inconsistentes**: fija una sola forma («bot de Telegram» o «asistente») tras presentarlo y úsala siempre. Define cada sigla la primera vez.
13. **Lector equivocado**: no vuelvas a explicar al jurado conceptos que el capítulo 2 ya definió; remite al punto.

## Cómo trabajar

1. Lee el texto completo y el índice del informe (`common/structure/model1.md`).
2. Marca los hallazgos por patrón y propón los cambios agrupados por sección; muestra «antes → después» de tres o cuatro ejemplos.
3. Aplica con Edit solo lo aprobado. Después de editar, comprueba que no cambió ningún número, código ni cita (`diff` y `grep`).
4. Si el texto sale de un bloque de una skill (p. ej. `04-make-strategic-analysis`), el cambio se hace en su corrida con el `-update` correspondiente y el informe se rearma con `12-make-report`.
5. Informa qué patrones aparecieron y cuántas veces, sin juicio sobre el autor.
