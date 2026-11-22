import { ArrowDownRight, ArrowUpRight, Cpu, Landmark, Leaf, Scale, TrendingUp, Users } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Lamina, Laminas } from "../../ui/lamina.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { politico: Landmark, economico: TrendingUp, social: Users, tecnologico: Cpu, ecologico: Leaf, legal: Scale };

// Balance de los factores de la imagen: una barra con la proporción de oportunidades y amenazas.
function Balance({ o, a }) {
  const total = Math.max(o + a, 1);
  return (
    <div className="mb-7 flex flex-wrap items-center gap-5 rounded-3xl border border-border bg-card px-6 py-4" data-balance>
      <span className="text-sm font-bold uppercase tracking-[0.16em] text-muted-foreground">Balance</span>
      <div className="flex h-3.5 min-w-[260px] flex-1 overflow-hidden rounded-full bg-border">
        <i className="block h-full bg-[var(--c-exito)]" style={{ width: `${(100 * o) / total}%` }} />
        <i className="block h-full bg-[var(--c-error)]" style={{ width: `${(100 * a) / total}%` }} />
      </div>
      <Badge variant="success" className="text-sm"><ArrowUpRight className="size-4" aria-hidden="true" />{o} {o === 1 ? "oportunidad" : "oportunidades"}</Badge>
      <Badge variant="destructive" className="text-sm"><ArrowDownRight className="size-4" aria-hidden="true" />{a} {a === 1 ? "amenaza" : "amenazas"}</Badge>
    </div>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<Lamina><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></Lamina>);
  return (
    <Laminas>
      {m.partes.map((p) => (
        <Lamina key={p.titulo}>
          <Encabezado titulo={p.titulo} proyecto={m.proyecto} />
          <Balance o={p.oportunidades} a={p.amenazas} />
          <div className="grid grid-cols-3 items-start gap-6">
            {p.factores.map((f) => (
              <Panel key={f.clave} k={f.k} marca={f.letra} icono={ICONO[f.icono]} titulo={f.nombre} cuenta={f.items.length} className="!p-6" data-factor={f.clave}>
                <ul className="flex flex-col gap-4">
                  {f.items.map((i) => (
                    <li key={i.codigo} data-codigo={i.codigo} className="rounded-2xl border border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-4">
                      <div className="mb-2.5 flex flex-wrap items-center gap-2">
                        <Badge mono className="text-[13px]">{i.codigo}</Badge>
                        {i.tipo ? (
                          <Badge variant={i.favorable ? "success" : "destructive"} className="text-[13px]">
                            {i.favorable ? <ArrowUpRight className="size-3.5" aria-hidden="true" /> : <ArrowDownRight className="size-3.5" aria-hidden="true" />}{i.tipo}
                          </Badge>
                        ) : null}
                      </div>
                      <p className="text-[17px] font-semibold leading-snug">{nb(i.texto)}</p>
                      {i.efecto ? <p className="mt-2.5 text-[15px] leading-snug text-muted-foreground"><b className="font-semibold text-foreground">Efecto:</b> {nb(i.efecto)}</p> : null}
                      {i.fuente ? <p className="mt-2 text-[13px] leading-snug text-muted-foreground">Fuente: {nb(i.fuente)}</p> : null}
                    </li>
                  ))}
                </ul>
              </Panel>
            ))}
          </div>
        </Lamina>
      ))}
    </Laminas>
  );
}
