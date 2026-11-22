# Playbook · Brief del proyecto

Cómo definir con el usuario el **núcleo del proyecto de Inteligencia de Negocios**: de qué trata, qué problema del negocio resuelve, qué objetivos persigue, qué entra y qué no, quiénes usarán el dashboard y qué decisiones apoyará, de qué fuentes saldrán los datos y cuándo se entrega. Lo usa la skill `01-make-project-brief`; todas las demás skills leen el resultado.

## 0. Reglas que se aplican siempre
1. **El brief es la fuente única** del tema, la problemática, los objetivos, el alcance, los usuarios, las fuentes previstas y el calendario. Las demás skills lo leen y **no lo vuelven a preguntar**; si algo cambia, se cambia aquí con `01-make-project-brief-update`.
2. **Una sección a la vez.** En cada una: pregunta lo mínimo, propón una redacción a partir de lo que el usuario cuenta, muéstrala, ajústala con él y pásala a la siguiente solo cuando la confirme.
3. **No inventes.** Lo que el usuario no sabe queda **«Pendiente»**; no lo redactes como hecho. Una propuesta tuya se presenta como propuesta y el usuario la acepta, la corrige o la deja pendiente. Con `modo_datos: real` usa solo lo que el usuario informa.
4. **No presupongas una empresa.** Con `tipo: propio` no hay empresa; con `tipo: empresa` el dominio se busca por el RUC (después, en `domain.md`). Una empresa real sin autorización solo usa datos abiertos o generados.
5. **Texto limpio.** Ningún archivo, salvo el `README.md` de la corrida, dice que algo es falso, inventado, de prueba o simulado.
6. **El brief manda sobre el config.** Tras confirmar, se copian al config el tema y las fechas (`brief.py al-config`) y la validación exige que coincidan.

## 1. Preguntas y pulido por sección

| Sección | Preguntas (lo mínimo) | Cómo pulirla |
|---|---|---|
| **1. Tema y empresa** | ¿Qué empresa o negocio, qué problema de decisión tiene y qué solución de BI proponen? | Una frase con problema y solución; la empresa en una línea (nombre comercial, giro y tamaño) o «Proyecto propio». |
| **2. Problemática** | ¿Qué duele hoy y a quién? ¿Cómo deciden ahora y con qué datos? ¿Qué evidencia tienen? | Separa el problema de la solución; el problema principal en una frase, idealmente con una cifra; cada evidencia en una viñeta (o «Pendiente»). |
| **3. Objetivos** | ¿Qué debe lograr el proyecto al final? ¿Cómo sabrán que se logró? ¿Con qué indicador lo verán en el dashboard? | Un `OG-01` y de 2 a 5 `OE-nn`; cada uno con verbo, métrica, **meta con cifra**, plazo `Entrega (fecha)` e **indicador**; cada `OE` aporta a `OG-01`. Propón una meta si el usuario no la tiene y márcala como propuesta. |
| **4. Justificación y alcance** | ¿Por qué importa (práctica, económica, metodológica)? ¿Qué procesos, áreas y periodo entran? ¿Qué herramientas piensan usar además de Power BI? ¿Qué limita (tiempo, datos, acceso)? | Una o dos frases por justificación; el «no incluye» es tan importante como el «incluye»; las herramientas van en la fila `Herramientas previstas` (o «Pendiente»); cada limitación con su efecto y cómo se maneja. |
| **5. Usuarios y decisiones** | ¿Quién usará el dashboard y quién decide? ¿Qué decisiones concretas tomará con él? | Usuarios en una frase; cada decisión en una viñeta, con verbo («ajustar el precio de…»). |
| **6. Fuentes de datos previstas** | ¿De dónde saldrán los datos? ¿Son internos, abiertos o generados? ¿Tienen autorización? | Una fila `FUE-nn` por fuente con tipo, datos, periodo y acceso; si es una empresa real sin autorización, solo fuentes abiertas o generadas. |
| **7. Calendario** | ¿Cuándo empiezan y cuándo es la entrega (y la exposición)? | Una fila con inicio y entrega en `DD-MM-AAAA`; la entrega no es anterior al inicio; lo que no se sepa queda «Pendiente». |
| **8. Supuestos y riesgos iniciales** | ¿Qué dan por cierto y qué podría fallar (datos, acceso, tiempo)? ¿Cómo lo vigilarán? | Cada fila `INI-nn` con tipo `Supuesto` o `Riesgo`, descripción concreta y cómo se vigila; propón 2 o 3 a partir de lo anterior y que el usuario elija. |

## 2. Objetivos medibles
- **Verbo + qué + para qué**, sin «mejorar» a secas: cada objetivo tiene una métrica, una meta con cifra o criterio y un plazo.
- El plazo es `Entrega (DD-MM-AAAA)` y esa fecha es la entrega de la sección 7; si la entrega es «Pendiente», el plazo es `Entrega (Pendiente)` y se completa cuando haya fecha.
- Cada objetivo nombra en **Indicador** el KPI del dashboard o el indicador del negocio con que se medirá. Los KPI se diseñan en `07-make-data-model-kpi`, que debe cubrir cada indicador citado aquí.
- La rúbrica pide que todos los elementos del diagnóstico estén **articulados a los objetivos**: los objetivos se escriben pensando en la problemática y se retoman en el capítulo 1 (`05-make-problem-objectives`).

## 3. Calendario
- Una sola entrega: el informe y el dashboard se presentan juntos.
- El calendario se copia al config (`calendario.inicio` y `calendario.entrega`).

## 4. `domain.md`
Tras confirmar el brief, la skill crea `project/domain.md` con la plantilla de `01-make-project-brief/references/domain-plantilla.md`: con `tipo: empresa`, los datos salen de buscar el RUC (con su fuente) y lo demás se plantea a partir del tema y el rubro con el marcador «(modelado por el agente, por no contar con X)»; con `tipo: propio`, describe la empresa o solución con lo del brief. El problema, los usuarios y los objetivos no se repiten en `domain.md`.

## 5. Cambios
Un cambio se hace con `01-make-project-brief-update`, que edita solo lo afectado, copia al config lo que cambie y dice qué `-update` correr después. Los datos técnicos (nombre, rubro, tipo, RUC, equipo y modo de datos) se cambian con `00-init-update`.

## 6. Errores frecuentes y checklist
**Errores:** objetivos sin cifra o sin indicador; plazos que no coinciden con la entrega; mezclar problema con solución; redactar como hecho lo que el usuario no dijo; objetivos que no aportan a `OG-01`; fuentes de una empresa real sin autorización; dejar el config con un tema distinto del brief.

**Checklist:**
- [ ] Las ocho secciones están, con títulos exactos, y lo desconocido dice «Pendiente».
- [ ] `OG-01` y al menos dos `OE` con métrica, meta, plazo e indicador.
- [ ] Los plazos coinciden con la entrega del calendario.
- [ ] Hay decisiones que apoyará el dashboard y fuentes con tipo y acceso.
- [ ] El config coincide con el brief y existe `domain.md`.
