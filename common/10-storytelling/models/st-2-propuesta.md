# Plantilla: Propuesta de hallazgos (se muestra y se confirma; no se guarda)

| | |
|---|---|
| **Entregable** | la propuesta de hallazgos que se muestra al usuario en la conversación |
| **Punto** | Previo a 4. Storytelling con datos |
| **Códigos** | `HLZ-nn`; cita `OE-nn` y `KPI-nn` |
| **Entradas** | `valores.json` y capturas de `09-make-dashboard`, 3.2, `modelo.json`, brief |
| **Salida** | una fila por hallazgo para que el usuario la confirme o la ajuste antes de escribir la sección 4 |

## Instrucciones para el agente
1. Lee `valores.json` de la corrida vigente de 09. **Si falta, detente:** «primero hay que entregar los valores del dashboard».
2. Arma la tabla con una fila por hallazgo y calcula el estado de cada KPI con su meta (`Cumple`, `No cumple` o `Sin meta`). La captura es la página de 3.2 donde se ve el KPI.
3. Comprueba que **cada objetivo específico del brief** tiene al menos un hallazgo y que ningún KPI se cuenta bajo un objetivo que no mide.
4. Propón un orden de prioridad (la brecha mayor frente a su meta primero; los KPI sin meta, al final) y una frase por hallazgo con la decisión de quién la toma.
5. Muestra la tabla y **espera la confirmación**. No escribas la sección hasta tenerla.

## Formato

```markdown
| Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya |
|---|---|---|---|---|---|---|---|---|
| HLZ-01 | [OE-nn] | [KPI-nn] | [valor] | [meta de 2.5] | [estado] | [pag-nn] | [usuario del brief] | [decisión] |

Objetivos sin hallazgo: [ninguno o lista]. Orden de prioridad: [HLZ-nn, HLZ-nn, …].
```

## Ejemplo

```markdown
| Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya |
|---|---|---|---|---|---|---|---|---|
| HLZ-01 | OE-01 | KPI-01 | 97,2 % | 98 % o más | No cumple | pag-01 | Gerente general | Revisar los registros rechazados |
| HLZ-02 | OE-02 | KPI-02 | 8,4 % | 12 % o más en el margen neto global | No cumple | pag-02 | Gerente general | Fijar un precio distinto en las aplicaciones |
| HLZ-04 | OE-03 | KPI-03 | 6,9 % | 3 % o menos | No cumple | pag-03 | Jefe de cocina | Ajustar cuántos pollos se hornean por turno |

Objetivos sin hallazgo: ninguno. Orden de prioridad: HLZ-04, HLZ-02, HLZ-01.
```

## Checklist
- [ ] Cada objetivo del brief tiene al menos un hallazgo.
- [ ] El estado de cada fila sale de comparar el valor con la meta de 2.5.
- [ ] La captura de cada fila es la página donde se ve su KPI.
- [ ] Quién decide es un usuario del brief.
- [ ] El usuario confirmó la propuesta antes de escribir.
