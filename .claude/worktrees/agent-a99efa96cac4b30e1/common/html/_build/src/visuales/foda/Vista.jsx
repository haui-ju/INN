import { AlertOctagon, Crosshair, LifeBuoy, Rocket, Shield, ShieldAlert, ShieldCheck, Shuffle, TrendingDown } from "lucide-react";
import { Badge } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel, TONOS } from "../../ui/panel.jsx";

const ICONO = { fuerza: ShieldCheck, debil: TrendingDown, oportunidad: Rocket, amenaza: ShieldAlert, fo: Crosshair, fa: Shield, do: Shuffle, da: LifeBuoy };

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div className="mb-3 hidden grid-cols-2 gap-4 text-xs font-medium uppercase tracking-wider text-muted-foreground sm:grid">
        <span>Interno · Microentorno</span><span>Externo · Macroentorno</span>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        {[m.cuadrantes[0], m.cuadrantes[2], m.cuadrantes[1], m.cuadrantes[3]].map((q) => {
          const t = TONOS[q.tono];
          return (
            <Panel key={q.clave} tono={q.tono} icono={ICONO[q.icono] || AlertOctagon} titulo={q.nombre} subtitulo={`${q.grupo} · ${q.signo}`} cuenta={q.items.length} data-cuadrante={q.clave}>
              <ul className="flex flex-col gap-2.5">
                {q.items.map((i) => (
                  <li key={i.codigo} data-codigo={i.codigo} className={`rounded-xl border border-border p-3 text-sm ${t.fondo}`}>
                    <div className="mb-1.5 flex items-center gap-2"><Badge mono variant="default">{i.codigo}</Badge></div>
                    <p className="font-medium leading-snug">{i.texto}</p>
                    {i.evidencia ? <p className="mt-1.5 text-xs leading-snug text-muted-foreground">Evidencia: {i.evidencia}</p> : null}
                  </li>
                ))}
              </ul>
            </Panel>
          );
        })}
      </div>
      {m.conEstrategias ? (
        <>
          <h2 className="mb-3 mt-8 text-2xl">Estrategias cruzadas</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {m.estrategias.map((e) => (
              <Panel key={e.tipo} tono="neutro" icono={ICONO[e.icono]} titulo={e.nombre} subtitulo={e.subtitulo} cuenta={e.items.length} data-estrategia={e.tipo}>
                <ul className="flex flex-col gap-2.5">
                  {e.items.map((i) => (
                    <li key={i.codigo} data-codigo={i.codigo} className="rounded-xl border border-border bg-background p-3 text-sm">
                      <div className="mb-1.5 flex items-center gap-2"><Badge mono>{i.codigo}</Badge></div>
                      <p className="font-medium leading-snug">{i.texto}</p>
                      {i.combina ? <p className="mt-1.5 font-mono text-xs text-muted-foreground">Combina: {i.combina}</p> : null}
                    </li>
                  ))}
                </ul>
              </Panel>
            ))}
          </div>
        </>
      ) : null}
    </>
  );
}
