import { ArrowDownRight, ArrowUpRight, Cpu, Landmark, Leaf, Scale, TrendingUp, Users } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { politico: Landmark, economico: TrendingUp, social: Users, tecnologico: Cpu, ecologico: Leaf, legal: Scale };

// Balance del entorno: una barra con la proporción de oportunidades y amenazas.
function Balance({ o, a }) {
  const total = Math.max(o + a, 1);
  return (
    <div className="mb-6 flex flex-wrap items-center gap-4 rounded-3xl border border-border bg-card px-5 py-3" data-balance>
      <span className="text-xs font-bold uppercase tracking-[0.16em] text-muted-foreground">Balance del entorno</span>
      <div className="flex h-3 min-w-[220px] flex-1 overflow-hidden rounded-full bg-border">
        <i className="block h-full bg-[var(--c-exito)]" style={{ width: `${(100 * o) / total}%` }} />
        <i className="block h-full bg-[var(--c-error)]" style={{ width: `${(100 * a) / total}%` }} />
      </div>
      <Badge variant="success"><ArrowUpRight className="size-3.5" aria-hidden="true" />{o} oportunidades</Badge>
      <Badge variant="destructive"><ArrowDownRight className="size-3.5" aria-hidden="true" />{a} amenazas</Badge>
    </div>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <Balance o={m.oportunidades} a={m.amenazas} />
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {m.factores.map((f) => (
          <Panel key={f.clave} k={f.k} marca={f.letra} icono={ICONO[f.icono]} titulo={f.nombre} cuenta={f.items.length} data-factor={f.clave}>
            <ul className="flex flex-col gap-3">
              {f.items.map((i) => (
                <li key={i.codigo} data-codigo={i.codigo} className="rounded-2xl border border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-3.5 text-sm">
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    <Badge mono>{i.codigo}</Badge>
                    {i.tipo ? (
                      <Badge variant={i.favorable ? "success" : "destructive"}>
                        {i.favorable ? <ArrowUpRight className="size-3.5" aria-hidden="true" /> : <ArrowDownRight className="size-3.5" aria-hidden="true" />}{i.tipo}
                      </Badge>
                    ) : null}
                  </div>
                  <p className="font-semibold leading-snug">{nb(i.texto)}</p>
                  {i.efecto ? <p className="mt-2 leading-snug text-muted-foreground"><b className="font-semibold text-foreground">Efecto:</b> {nb(i.efecto)}</p> : null}
                  {i.fuente ? <p className="mt-1.5 text-xs leading-snug text-muted-foreground">Fuente: {nb(i.fuente)}</p> : null}
                </li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>
    </>
  );
}
