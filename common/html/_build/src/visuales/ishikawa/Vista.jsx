import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";

function Categoria({ c }) {
  return (
    <section data-categoria={c.nombre} className="rounded-xl border border-border bg-card p-3 shadow-sm">
      <header className="mb-2 flex items-center justify-between gap-2">
        <h2 className="text-base leading-tight">{c.nombre}</h2>
        <span className="rounded-full bg-border/70 px-2 py-0.5 text-xs font-semibold tabular-nums text-muted-foreground">{c.causas.length}</span>
      </header>
      <ul className="flex flex-col gap-2 text-sm">
        {c.causas.map((x) => (
          <li key={x.codigo} data-codigo={x.codigo} className="flex items-start gap-2 leading-snug">
            <Badge mono className="shrink-0">{x.codigo}</Badge><span>{x.texto}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

// Espina oblicua de una categoría hacia la espina central (arriba baja hacia la derecha; abajo sube hacia la derecha).
function Rama({ arriba }) {
  return (
    <svg aria-hidden="true" viewBox="0 0 100 40" preserveAspectRatio="none" className="block h-10 w-full">
      <line x1={arriba ? 20 : 92} y1="0" x2={arriba ? 92 : 20} y2="40" stroke="var(--c-texto-secundario)" strokeWidth="2" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  const n = m.columnas;
  const celda = (col, fila) => ({ gridColumn: `${col} / span 1`, gridRow: `${fila} / span 1` });
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div data-scroll className="overflow-x-auto">
        <div className="grid min-w-[980px] gap-x-4" style={{ gridTemplateColumns: `repeat(${n}, minmax(0, 1fr)) minmax(220px, 0.9fr)` }}>
          {m.arriba.map((c, i) => (
            <div key={c.nombre} className="flex flex-col justify-end" style={celda(i + 1, 1)}><Categoria c={c} /><Rama arriba /></div>
          ))}
          <div className="flex items-center" style={{ gridColumn: `1 / span ${n}`, gridRow: "2 / span 1" }} aria-hidden="true">
            <div className="h-[3px] flex-1 rounded-full bg-primary-strong" />
            <svg width="16" height="18" viewBox="0 0 16 18" className="shrink-0"><path d="M0 0 L16 9 L0 18 Z" fill="var(--c-acento-fuerte)" /></svg>
          </div>
          <div className="self-center py-2" style={{ gridColumn: `${n + 1} / span 1`, gridRow: "1 / span 3" }}>
            <div data-efecto className="rounded-2xl border border-t-4 border-border border-t-primary bg-card p-4 shadow-sm">
              <p className="mb-1.5 text-xs font-medium uppercase tracking-wider text-muted-foreground">Efecto · problema central</p>
              <p className="font-serif text-xl leading-snug">{m.efecto}</p>
            </div>
          </div>
          {m.abajo.map((c, i) => (
            <div key={c.nombre} className="flex flex-col justify-start" style={celda(i + 1, 3)}><Rama arriba={false} /><Categoria c={c} /></div>
          ))}
        </div>
      </div>
    </>
  );
}
