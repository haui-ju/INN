import { ArrowRight, ChevronsRight, Database, LayoutDashboard, Warehouse, Workflow, Wrench } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Chip } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { fuentes: Database, etl: Workflow, almacenamiento: Warehouse, visualizacion: LayoutDashboard };

function Capa({ c }) {
  return (
    <Panel k={c.k} marca={String(c.numero)} icono={ICONO[c.icono] || Database} titulo={c.nombre} subtitulo={c.subtitulo} cuenta={c.componentes.length} data-capa={c.clave} className="h-full">
      <ul className="flex flex-1 flex-col gap-3">
        {c.componentes.map((x) => (
          <li key={x.codigo} data-codigo={x.codigo} className="rounded-2xl border border-[color-mix(in_srgb,var(--k)_30%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-3.5 text-sm">
            <div className="mb-1.5"><Chip k={c.k} mono>{x.codigo}</Chip></div>
            <p className="font-semibold leading-snug">{nb(x.nombre)}</p>
            {x.funcion ? <p className="mt-1 text-xs leading-snug text-muted-foreground">{nb(x.funcion)}</p> : null}
            {x.entradaSalida ? (
              <p className="mt-2 flex items-start gap-1.5 rounded-lg bg-[color-mix(in_srgb,var(--k)_12%,transparent)] px-2 py-1 text-xs leading-snug"><ArrowRight className="mt-0.5 size-3 shrink-0 text-[var(--k)]" aria-hidden="true" /><span>{nb(x.entradaSalida)}</span></p>
            ) : null}
          </li>
        ))}
      </ul>
      {c.herramientas.length ? (
        <div className="mt-4 flex flex-wrap items-center gap-1.5 border-t border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] pt-3" data-herramientas={c.clave}>
          <Wrench className="size-3.5 text-muted-foreground" aria-hidden="true" />
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
    if (i > 0) celdas.push(
      <div key={`f${i}`} className="flex items-start justify-center pt-8" aria-hidden="true">
        <span className="inline-flex size-9 items-center justify-center rounded-full bg-[var(--c-acento)] text-[var(--c-acento-texto)] shadow-[0_0_28px_var(--c-acento)]"><ChevronsRight className="size-5" /></span>
      </div>,
    );
    celdas.push(<Capa key={c.clave} c={c} />);
  });
  const columnas = m.capas.map((_, i) => (i > 0 ? "3.25rem minmax(0,1fr)" : "minmax(0,1fr)")).join(" ");
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div data-scroll className="overflow-x-auto overflow-y-hidden py-6">
        <div className="grid min-w-[1100px] items-stretch" style={{ gridTemplateColumns: columnas }}>{celdas}</div>
      </div>
    </>
  );
}
