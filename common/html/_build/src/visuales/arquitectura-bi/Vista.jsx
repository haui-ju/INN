import { ArrowRight, Database, LayoutDashboard, Warehouse, Workflow } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel, TONOS } from "../../ui/panel.jsx";

const ICONO = { fuentes: Database, etl: Workflow, almacenamiento: Warehouse, visualizacion: LayoutDashboard };

function Capa({ c }) {
  const t = TONOS[c.tono];
  return (
    <Panel tono={c.tono} icono={ICONO[c.icono] || Database} titulo={`${c.numero}. ${c.nombre}`} subtitulo={c.subtitulo} cuenta={c.componentes.length} data-capa={c.clave} className="h-full">
      <ul className="flex flex-1 flex-col gap-2.5">
        {c.componentes.map((x) => (
          <li key={x.codigo} data-codigo={x.codigo} className={`rounded-xl border border-border p-3 text-sm ${t.fondo}`}>
            <div className="mb-1.5"><Badge mono>{x.codigo}</Badge></div>
            <p className="font-medium leading-snug">{x.nombre}</p>
            {x.funcion ? <p className="mt-1 text-xs leading-snug text-muted-foreground">{x.funcion}</p> : null}
            {x.entradaSalida ? <p className="mt-1.5 text-xs leading-snug text-muted-foreground">{x.entradaSalida}</p> : null}
          </li>
        ))}
      </ul>
      {c.herramientas.length ? (
        <div className="mt-3 flex flex-wrap items-center gap-1.5 border-t border-border pt-3" data-herramientas={c.clave}>
          <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Herramientas</span>
          {c.herramientas.map((h) => <Badge key={h.nombre} variant={h.pendiente ? "warning" : "brand"}>{h.nombre}</Badge>)}
        </div>
      ) : null}
    </Panel>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  const celdas = [];
  m.capas.forEach((c, i) => {
    if (i > 0) celdas.push(<div key={`f${i}`} className="flex items-start justify-center pt-5 text-muted-foreground" aria-hidden="true"><ArrowRight className="size-6" /></div>);
    celdas.push(<Capa key={c.clave} c={c} />);
  });
  const columnas = m.capas.map((_, i) => (i > 0 ? "2rem minmax(0,1fr)" : "minmax(0,1fr)")).join(" ");
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div data-scroll className="overflow-x-auto">
        <div className="grid min-w-[1040px] items-stretch gap-x-1" style={{ gridTemplateColumns: columnas }}>{celdas}</div>
      </div>
    </>
  );
}
