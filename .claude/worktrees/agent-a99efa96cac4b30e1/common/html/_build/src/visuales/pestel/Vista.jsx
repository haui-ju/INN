import { Cpu, Landmark, Leaf, Scale, TrendingUp, Users } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";

const ICONO = { politico: Landmark, economico: TrendingUp, social: Users, tecnologico: Cpu, ecologico: Leaf, legal: Scale };

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {m.factores.map((f) => (
          <Panel key={f.clave} tono="neutro" icono={ICONO[f.icono]} titulo={f.nombre} cuenta={f.items.length} data-factor={f.clave}>
            <ul className="flex flex-col gap-2.5">
              {f.items.map((i) => (
                <li key={i.codigo} data-codigo={i.codigo} className="rounded-xl border border-border bg-background p-3 text-sm">
                  <div className="mb-1.5 flex flex-wrap items-center gap-2">
                    <Badge mono>{i.codigo}</Badge>
                    {i.tipo ? <Badge variant={i.favorable ? "success" : "destructive"}>{i.tipo}</Badge> : null}
                  </div>
                  <p className="font-medium leading-snug">{i.texto}</p>
                  {i.efecto ? <p className="mt-1.5 leading-snug text-muted-foreground">Efecto: {i.efecto}</p> : null}
                  {i.fuente ? <p className="mt-1 text-xs leading-snug text-muted-foreground">Fuente: {i.fuente}</p> : null}
                </li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>
    </>
  );
}
