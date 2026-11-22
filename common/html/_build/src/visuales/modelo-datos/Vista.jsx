import { KeyRound, Layers, Table2 } from "lucide-react";
import { Badge, Chip } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../ui/table.jsx";

function Dimension({ d }) {
  return (
    <section
      data-codigo={d.codigo} data-tabla={d.nombre}
      style={{ left: d.x, top: d.y, width: d.w, height: d.h, "--k": `var(--c-${d.k})` }}
      className="absolute overflow-hidden rounded-3xl border border-[color-mix(in_srgb,var(--k)_45%,var(--c-borde))] bg-[linear-gradient(155deg,color-mix(in_srgb,var(--k)_20%,var(--c-superficie)),var(--c-superficie)_70%)] p-3.5 shadow-[0_18px_40px_-24px_var(--k)]"
    >
      <span aria-hidden="true" className="absolute inset-x-0 top-0 h-1 bg-[var(--k)]" />
      <header className="flex items-center gap-2"><Layers className="size-4 shrink-0 text-[var(--k)]" aria-hidden="true" /><h3 className="truncate text-base">{d.nombre}</h3></header>
      <p className="mt-1.5 flex items-center gap-1.5 text-xs text-muted-foreground"><KeyRound className="size-3.5 shrink-0" aria-hidden="true" /><span className="truncate font-mono">{d.clave}</span></p>
      <p className="mt-1.5 line-clamp-3 text-xs leading-snug text-muted-foreground">{d.atributos.join(" · ")}</p>
      {d.jerarquias.length ? <p className="mt-1 truncate text-xs"><b className="font-semibold">Jerarquía:</b> {d.jerarquias.join("; ")}</p> : null}
    </section>
  );
}

function Hecho({ h }) {
  return (
    <section
      data-codigo={h.codigo} data-tabla={h.nombre}
      style={{ left: h.x, top: h.y, width: h.w, height: h.h }}
      className="absolute overflow-hidden rounded-3xl border-2 border-[var(--c-acento)] bg-[linear-gradient(155deg,color-mix(in_srgb,var(--c-acento)_22%,var(--c-superficie)),var(--c-superficie)_72%)] p-4 shadow-[0_0_60px_-18px_var(--c-acento)]"
    >
      <header className="flex items-center gap-2"><Table2 className="size-5 shrink-0 text-primary-strong" aria-hidden="true" /><h3 className="truncate text-lg">{h.nombre}</h3><Badge mono variant="brand" className="ml-auto">{h.codigo}</Badge></header>
      <p className="mt-1.5 line-clamp-2 text-sm text-muted-foreground">{h.granularidad}</p>
      <ul className="mt-2.5 flex flex-wrap gap-1.5">
        {h.medidas.map((x) => <li key={x.nombre}><Chip k="acento" mono>{x.nombre}{x.agregacion ? ` · ${x.agregacion}` : ""}</Chip></li>)}
      </ul>
    </section>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <p className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.18em] text-muted-foreground"><Layers className="size-4" aria-hidden="true" />Dimensiones · ejes de análisis<span className="ml-auto flex items-center gap-2"><Table2 className="size-4 text-primary-strong" aria-hidden="true" />Hechos · lo que se mide</span></p>
      <div data-scroll className="overflow-x-auto overflow-y-hidden py-6">
        <div className="relative mx-auto" style={{ width: m.ancho, height: m.alto }}>
          <svg aria-hidden="true" viewBox={`0 0 ${m.ancho} ${m.alto}`} width={m.ancho} height={m.alto} className="absolute inset-0">
            {m.lineas.map((l) => (
              <g key={`${l.codigo}`} data-relacion-linea={l.codigo}>
                <path d={l.d} fill="none" stroke={`var(--c-${l.k})`} strokeOpacity="0.2" strokeWidth="9" strokeLinecap="round" />
                <path d={l.d} fill="none" stroke={`var(--c-${l.k})`} strokeWidth="2.5" strokeLinecap="round" />
                <circle cx={l.sx} cy={l.sy + 15} r="10" fill="var(--c-superficie)" stroke={`var(--c-${l.k})`} strokeWidth="2" />
                <text x={l.sx} y={l.sy + 19} textAnchor="middle" fontSize="12" fontWeight="700" fill="var(--c-texto)">{l.ladoHacia}</text>
                <circle cx={l.ex} cy={l.ey - 15} r="10" fill="var(--c-superficie)" stroke={`var(--c-${l.k})`} strokeWidth="2" />
                <text x={l.ex} y={l.ey - 10} textAnchor="middle" fontSize="12" fontWeight="700" fill="var(--c-texto)">{l.ladoDesde === "*" ? "∗" : l.ladoDesde}</text>
              </g>
            ))}
          </svg>
          {m.dimensiones.map((d) => <Dimension key={d.codigo} d={d} />)}
          {m.hechos.map((h) => <Hecho key={h.codigo} h={h} />)}
        </div>
      </div>
      <h2 className="mb-3 mt-8 text-2xl">Relaciones</h2>
      <Table>
        <TableHeader><TableRow><TableHead>Código</TableHead><TableHead>Desde</TableHead><TableHead>Hacia</TableHead><TableHead>Campo</TableHead><TableHead>Cardinalidad</TableHead><TableHead>Filtro</TableHead></TableRow></TableHeader>
        <TableBody>
          {m.relaciones.map((r) => (
            <TableRow key={r.codigo} data-relacion={r.codigo}>
              <TableCell><Badge mono>{r.codigo}</Badge></TableCell><TableCell className="font-semibold">{r.desde}</TableCell><TableCell className="font-semibold">{r.hacia}</TableCell>
              <TableCell className="font-mono text-xs">{r.campos}</TableCell><TableCell className="font-mono">{r.cardinalidad}</TableCell><TableCell>{r.filtro}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}
