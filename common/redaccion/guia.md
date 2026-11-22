# Reglas de redacción del informe

Fuente única de las reglas de calidad de redacción. La usan el agente `revisor-redactor`, la skill `redaccion-academica` y el revisor `python3 .claude/skills/_shared/redaccion.py`. Cada regla tiene un código (`R-nn`); los informes de revisión citan esos códigos.

**Para qué sirven:** que el informe se lea como un trabajo propio, específico del caso, claro y verificable. No predicen ni garantizan el resultado de Turnitin ni de ningún detector; solo la cuenta de la institución calcula ese porcentaje. Lo que más reduce el contenido genérico es el dato propio del equipo.

## 1. Lo que nunca se toca (inmutables)

| Código | Regla |
|---|---|
| I-1 | Cifras, porcentajes, fechas y unidades. |
| I-2 | Códigos de trazabilidad (`OE-01`, `CAU-03`, `FCT-01`, `KPI-02`, `CAP-04`, `HER-01`…) y nombres de tablas y campos (`fPedidos`, `venta_bruta`). |
| I-3 | Citas en texto (Autor, año) y referencias APA 7. |
| I-4 | Nombres propios, marcas, enlaces y siglas definidas. |
| I-5 | Tablas, títulos «Tabla N:», bloques de código, marcas `<!-- figura: … -->` y marcadores «(INCLUIR IMAGEN: …)». |
| I-6 | Encabezados exactos de cada sección (`## 2.2. Arquitectura de Inteligencia de Negocios`). |
| I-7 | Hechos: no se agrega ningún dato, evidencia ni fuente que el equipo no haya dado. |

Si una mejora exige tocar algo de esta lista, no se hace: se deja la frase y se avisa.

## 2. Reglas de prosa

Gravedad **bloqueante** = se corrige antes de registrar la corrida. **Recomendada** = se corrige o el usuario decide conservarla.

| Código | Tipo de aviso | Gravedad | Regla | Cómo se corrige |
|---|---|---|---|---|
| R-01 | `relleno` | Bloqueante | Sin aperturas ni cierres vacíos («es importante destacar», «en conclusión», «hoy en día», «juega un papel fundamental»). | Empieza por el contenido. |
| R-02 | `inflado` | Bloqueante | Sin adjetivos de relleno («fundamental», «robusto», «innovador», «integral», «holístico»). | Sustitúyelos por el dato o elimínalos. |
| R-03 | `gerundio` | Bloqueante | Sin gerundio de cierre («…permitiendo así optimizar…»). | Parte la frase en dos o corta el gerundio. |
| R-04 | `contraste` | Bloqueante | Sin «no solo… sino» ni «no es X, sino Y» cuando nadie dijo X. | Afirma directamente lo que sí es. |
| R-05 | `arranque-repetido` | Bloqueante | No empiezan igual tres frases seguidas. | Conecta con causa, consecuencia, contraste o secuencia. |
| R-06 | `sigla` | Bloqueante | Toda sigla se define la primera vez: nombre completo y sigla entre paréntesis. | Define la sigla (las comunes del proyecto: BI, ETL, KPI, DAX, UIT, RUC, APA). |
| R-07 | `frase-larga` | Recomendada | Máximo 40 palabras por frase. | Divide en dos; una definición larga puede conservarse. |
| R-08 | `ritmo` | Recomendada | Se alternan frases cortas y largas (la desviación de longitud no es menor de 4 palabras). | Une dos frases cortas o parte una larga. |
| R-09 | `sin-dato` | Recomendada | Cada párrafo de 35 palabras o más lleva al menos una cifra, un código o una cita propios del caso. | Pide al usuario el dato (nunca lo inventes); si no existe, acorta o elimina la frase. |

## 3. Reglas que revisa el agente (sin comando)

| Código | Regla |
|---|---|
| R-10 | **Un término, una forma.** «dashboard» o «tablero», «canal» o «medio»: se elige uno al presentarlo y se usa siempre. |
| R-11 | **Voz y persona.** Prosa académica en tercera persona o impersonal con «se» cuando el agente no importa; sin segunda persona ni primera persona. |
| R-12 | **Concordancia y puntuación.** Género y número, tildes, comas de aposición, mayúsculas solo en nombres propios. |
| R-13 | **Una idea por párrafo**, con la frase principal al inicio y sin repetir lo que ya dice la tabla o la figura contigua. |
| R-14 | **No se explica de nuevo** lo que un capítulo anterior ya definió: se remite al punto. |
| R-15 | **Residuos de herramienta:** sin rutas internas, «Pegar.», etiquetas de plantilla ni «datos al…» en pies de figura. |
| R-16 | **Afirmaciones con respaldo:** toda afirmación sobre el negocio cita su dato del caso o su fuente; sin «según expertos» ni «diversos estudios». |
| R-17 | **Texto limpio:** ningún archivo, salvo `README.md`, califica el contenido como falso, inventado, de prueba o simulado. |

## 4. Proceso de revisión

1. **Medir antes:** `python3 .claude/skills/_shared/redaccion.py revisar <archivo.md>`.
2. **Leer** el texto completo y aplicar R-10 a R-17 a mano.
3. **Proponer** los cambios por sección con el código de regla y «antes → después». Para R-09, preguntar el dato al usuario.
4. **Aplicar** solo lo aprobado, en la corrida (bifurcada con el `-update` si ya estaba registrada).
5. **Medir después:** el comando con `--estricto` no debe devolver avisos bloqueantes; comprobar I-1 a I-5 con `diff`.
6. **Informar** el antes y el después por regla.

## 5. Formato del informe de revisión

```
Archivo: <ruta>
Antes: <n> avisos (bloqueantes <b>, recomendados <r>)
Hallazgos por sección:
- <sección> · R-01 · «<antes>» → «<después>»
Preguntas para el usuario: <dato que falta para R-09 o R-16>
No se tocó: <inmutables que impedían un cambio>
Después (tras aplicar): <n> avisos (bloqueantes <b>, recomendados <r>)
```
