import { ArrowDown, KeyRound, Layers, Table2 } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../ui/table.jsx";

function Dimension({ d }) {
  return (
    <section data-codigo={d.codigo} data-tabla={d.nombre} className="rounded-xl border border-border bg-card p-3 shadow-sm">
      <header className="mb-2 flex flex-wrap items-center gap-2"><Badge mono>{d.codigo}</Badge><h3 className="text-base font-semibold leading-tight">{d.nombre}</h3></header>
      <p className="mb-2 flex items-center gap-1.5 text-xs text-muted-foreground"><KeyRound className="size-3.5" aria-hidden="true" /><span className="font-mono">{d.clave}</span></p>
      <p className="text-xs leading-snug text-muted-foreground">{d.atributos.join(" · ")}</p>
      {d.jerarquias.length ? <p className="mt-1.5 text-xs leading-snug"><span className="font-medium">Jerarquía:</span> {d.jerarquias.join("; ")}</p> : null}
    </section>
  );
}

function Hecho({ h }) {
  return (
    <section data-codigo={h.codigo} data-tabla={h.nombre} className="rounded-xl border border-border border-t-4 border-t-primary bg-card p-4 shadow-sm">
      <header className="mb-1 flex flex-wrap items-center gap-2"><Badge mono variant="brand">{h.codigo}</Badge><h3 className="text-lg font-semibold leading-tight">{h.nombre}</h3></header>
      <p className="mb-3 text-sm text-muted-foreground">{h.granularidad}</p>
      <ul className="mb-3 flex flex-wrap gap-1.5">
        {h.medidas.map((x) => <li key={x.nombre}><Badge mono>{x.nombre}{x.agregacion ? ` · ${x.agregacion}` : ""}</Badge></li>)}
      </ul>
      <p className="text-xs leading-snug text-muted-foreground"><span className="font-medium">Claves:</span> <span className="font-mono">{h.claves.join(", ")}</span></p>
    </section>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <Panel tono="neutro" icono={Layers} titulo="Dimensiones" subtitulo="Ejes de análisis compartidos" cuenta={m.dimensiones.length}>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{m.dimensiones.map((d) => <Dimension key={d.codigo} d={d} />)}</div>
      </Panel>
      <div className="flex items-center justify-center gap-2 py-3 text-xs font-medium uppercase tracking-wider text-muted-foreground" aria-hidden="true">
        <ArrowDown className="size-4" />Cada hecho filtra por sus dimensiones (varios a uno)<ArrowDown className="size-4" />
      </div>
      <Panel tono="marca" icono={Table2} titulo="Tablas de hechos" subtitulo="Lo que se mide, a su propio grano" cuenta={m.hechos.length}>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{m.hechos.map((h) => <Hecho key={h.codigo} h={h} />)}</div>
      </Panel>
      <h2 className="mb-3 mt-8 text-2xl">Relaciones</h2>
      <Table>
        <TableHeader><TableRow><TableHead>Código</TableHead><TableHead>Desde</TableHead><TableHead>Hacia</TableHead><TableHead>Campo</TableHead><TableHead>Cardinalidad</TableHead><TableHead>Filtro</TableHead></TableRow></TableHeader>
        <TableBody>
          {m.relaciones.map((r) => (
            <TableRow key={r.codigo} data-relacion={r.codigo}>
              <TableCell><Badge mono>{r.codigo}</Badge></TableCell><TableCell className="font-medium">{r.desde}</TableCell><TableCell className="font-medium">{r.hacia}</TableCell>
              <TableCell className="font-mono text-xs">{r.campos}</TableCell><TableCell className="font-mono">{r.cardinalidad}</TableCell><TableCell>{r.filtro}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}
