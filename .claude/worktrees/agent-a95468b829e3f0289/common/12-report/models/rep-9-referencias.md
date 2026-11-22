# Plantilla: Referencias bibliográficas

| | |
|---|---|
| **Entregable** | Sección «Referencias bibliográficas» de `informe.md` |
| **Punto** | Referencias bibliográficas del índice |
| **Códigos** | No define códigos |
| **Entradas** | `referencias.md` de cada corrida usada en el informe |
| **Salida** | Entradas APA 7 sin duplicados y en orden alfabético |

## Instrucciones para el agente

1. Cada skill de contenido deja en su corrida un `referencias.md` opcional con **una entrada APA 7 por línea** (se acepta una viñeta `- ` al inicio; las líneas vacías y los encabezados se ignoran). Cada skill responde por sus citas.
2. El armado (`report.py construir`) reúne las entradas de las corridas usadas, quita las repetidas (mismo texto, sin importar los espacios) y las ordena alfabéticamente por autor, sin tener en cuenta las tildes.
3. Una entrada mal escrita se corrige en la skill que la aportó (con su `-update`), no en el informe.
4. Sin entradas, la sección dice «Pendiente» y `faltantes.md` lo anota.
5. Formato: `common/citation-style/APA7.md`.

## Formato

```markdown
# Referencias bibliográficas

[referencia APA completa]

[referencia APA completa]
```

## Ejemplo

```markdown
# Referencias bibliográficas

Kotler, P., & Keller, K. L. (2016). *Marketing management* (15.ª ed.). Pearson.

Osterwalder, A., & Pigneur, Y. (2010). *Business model generation*. John Wiley & Sons.
```

## Checklist

- [ ] Ninguna entrada se repite.
- [ ] Las entradas están en orden alfabético.
- [ ] Cada entrada sigue APA 7.
