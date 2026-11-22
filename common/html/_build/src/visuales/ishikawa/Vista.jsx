import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { nb } from "../../lib/utils.js";

// Cada categoría es una espina del pez: tarjeta con el color de su serie y una costilla curva hacia la columna vertebral.
function Categoria({ c }) {
  return (
    <section
      data-categoria={c.nombre}
      style={{ "--k": `var(--c-${c.k})` }}
      className="relative overflow-hidden rounded-3xl border border-[color-mix(in_srgb,var(--k)_40%,var(--c-borde))] bg-[linear-gradient(160deg,color-mix(in_srgb,var(--k)_16%,var(--c-superficie)),var(--c-superficie)_70%)] p-4 shadow-[0_18px_40px_-26px_var(--k)]"
    >
      <span aria-hidden="true" className="absolute inset-x-0 top-0 h-1 bg-[var(--k)]" />
      <header className="mb-3 flex items-center justify-between gap-2">
        <h2 className="text-base leading-tight">{c.nombre}</h2>
        <span className="rounded-full bg-[color-mix(in_srgb,var(--k)_26%,transparent)] px-2.5 py-0.5 text-xs font-bold tabular-nums">{c.causas.length}</span>
      </header>
      <ul className="flex flex-col gap-2.5 text-sm">
        {c.causas.map((x) => (
          <li key={x.codigo} data-codigo={x.codigo} className="flex items-start gap-2 leading-snug">
            <Badge mono className="shrink-0 !border-[color-mix(in_srgb,var(--k)_60%,transparent)] !bg-[color-mix(in_srgb,var(--k)_20%,transparent)] !text-foreground">{x.codigo}</Badge>
            <span>{nb(x.texto)}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

// Costilla curva: sale de la tarjeta y se une a la columna vertebral con la inclinación de una espina de pez.
function Costilla({ k, arriba }) {
  const d = arriba ? "M14,0 C14,38 70,34 92,64" : "M14,64 C14,26 70,30 92,0";
  return (
    <svg aria-hidden="true" viewBox="0 0 100 64" preserveAspectRatio="none" className="block h-16 w-full">
      <path d={d} fill="none" stroke={`var(--c-${k})`} strokeWidth="3" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      <circle cx={arriba ? 92 : 92} cy={arriba ? 64 : 0} r="0" fill={`var(--c-${k})`} />
    </svg>
  );
}

function Cola() {
  return (
    <div aria-hidden="true" data-cola className="relative w-[150px] shrink-0 self-stretch">
    <svg viewBox="0 0 150 400" preserveAspectRatio="none" className="absolute inset-0 block h-full w-full">
      <defs>
        <linearGradient id="g-cola" x1="1" y1="0" x2="0" y2="0">
          <stop offset="0" stopColor="var(--c-serie-1)" stopOpacity="0.34" />
          <stop offset="1" stopColor="var(--c-serie-5)" stopOpacity="0.62" />
        </linearGradient>
      </defs>
      <path d="M150,188 C118,184 92,168 72,138 C56,108 42,58 8,8 C16,84 20,150 38,196 L38,204 C20,250 16,316 8,392 C42,342 56,292 72,262 C92,232 118,216 150,212 Z" fill="url(#g-cola)" stroke="var(--c-serie-1)" strokeWidth="2" strokeOpacity="0.75" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <path d="M150,200 C110,200 70,190 30,120 M150,200 C110,200 70,210 30,280" fill="none" stroke="var(--c-serie-1)" strokeOpacity="0.35" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
    </svg>
    </div>
  );
}

function Cabeza({ efecto }) {
  const contorno = "M0,0 C140,-6 290,30 368,128 C378,142 378,158 368,172 C290,270 140,306 0,300";
  return (
    <div className="relative w-[390px] shrink-0 self-center" data-efecto>
      <svg aria-hidden="true" viewBox="0 0 380 300" preserveAspectRatio="none" className="absolute inset-0 h-full w-full [mask-image:linear-gradient(90deg,transparent,black_16%)]">
        <defs>
          <linearGradient id="g-cabeza" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="var(--c-acento)" stopOpacity="0.28" />
            <stop offset="1" stopColor="var(--c-serie-5)" stopOpacity="0.22" />
          </linearGradient>
        </defs>
        <path d={contorno + " Z"} fill="url(#g-cabeza)" />
        <path d={contorno} fill="none" stroke="var(--c-acento)" strokeWidth="2.5" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d="M44,56 C28,112 28,188 44,244" fill="none" stroke="var(--c-acento)" strokeOpacity="0.4" strokeWidth="2" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d="M356,186 C370,184 376,172 374,162" fill="none" stroke="var(--c-acento)" strokeWidth="2.5" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </svg>
      <span aria-hidden="true" className="absolute right-[92px] top-[14%] block size-8 rounded-full border-[3px] border-[var(--c-acento)] bg-[var(--c-texto)] shadow-[0_0_24px_var(--c-acento)]">
        <i className="absolute right-1.5 top-2 block size-3.5 rounded-full bg-[var(--c-fondo)]" />
      </span>
      <div className="relative pb-12 pl-14 pr-24 pt-[76px]">
        <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-primary-strong">Efecto · problema central</p>
        <p className="text-xl font-bold leading-snug">{nb(efecto)}</p>
      </div>
    </div>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  const n = m.columnas;
  const celda = (col, fila) => ({ gridColumn: `${col} / span 1`, gridRow: `${fila} / span 1` });
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div data-scroll className="overflow-x-auto overflow-y-hidden py-5">
        <div className="flex min-w-[1280px] items-stretch">
          <Cola />
          <div className="relative min-w-0 flex-1">
            <svg aria-hidden="true" viewBox="0 0 1000 400" preserveAspectRatio="none" className="absolute inset-x-0 -inset-y-4 h-[calc(100%+2rem)] w-full">
              <defs>
                <linearGradient id="g-cuerpo" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0" stopColor="var(--c-serie-1)" stopOpacity="0.14" />
                  <stop offset="1" stopColor="var(--c-serie-5)" stopOpacity="0.2" />
                </linearGradient>
              </defs>
              <path d="M0,200 C110,28 380,-2 600,14 C820,30 950,110 1000,200 C950,290 820,370 600,386 C380,402 110,372 0,200 Z" fill="url(#g-cuerpo)" stroke="var(--c-serie-1)" strokeWidth="2" strokeOpacity="0.55" vectorEffect="non-scaling-stroke" />
            </svg>
            <div className="relative grid gap-x-5 px-7 py-6" style={{ gridTemplateColumns: `repeat(${n}, minmax(0, 1fr))`, gridTemplateRows: "1fr 12px 1fr" }}>
              {m.arriba.map((c, i) => (
                <div key={c.nombre} className="flex flex-col justify-end" style={celda(i + 1, 1)}><Categoria c={c} /><Costilla k={c.k} arriba /></div>
              ))}
              <div aria-hidden="true" data-columna-vertebral className="flex items-center" style={{ gridColumn: `1 / span ${n}`, gridRow: "2 / span 1" }}>
                <div className="h-[5px] flex-1 rounded-full bg-[linear-gradient(90deg,var(--c-serie-1),var(--c-acento))] shadow-[0_0_18px_var(--c-serie-1)]" />
              </div>
              {m.abajo.map((c, i) => (
                <div key={c.nombre} className="flex flex-col justify-start" style={celda(i + 1, 3)}><Costilla k={c.k} arriba={false} /><Categoria c={c} /></div>
              ))}
            </div>
          </div>
          <Cabeza efecto={m.efecto} />
        </div>
      </div>
    </>
  );
}
