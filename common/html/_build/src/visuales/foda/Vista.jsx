import { AlertOctagon, Crosshair, LifeBuoy, Rocket, Shield, ShieldAlert, ShieldCheck, Shuffle, TrendingDown } from "lucide-react";
import { Badge, Chip } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { fuerza: ShieldCheck, debil: TrendingDown, oportunidad: Rocket, amenaza: ShieldAlert, fo: Crosshair, fa: Shield, do: Shuffle, da: LifeBuoy };
// Cada código FODA lleva el color de su cuadrante: así se ve de dónde sale cada estrategia.
const COLOR = { FOR: "serie-1", DEB: "serie-4", OPO: "serie-3", AME: "serie-2" };
const colorDe = (codigo) => COLOR[String(codigo).slice(0, 3)] || "serie-5";

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div className="mb-3 hidden grid-cols-2 gap-5 text-xs font-bold uppercase tracking-[0.18em] text-muted-foreground sm:grid">
        <span>Interno · Microentorno</span><span>Externo · Macroentorno</span>
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        {[m.cuadrantes[0], m.cuadrantes[2], m.cuadrantes[1], m.cuadrantes[3]].map((q) => (
          <Panel key={q.clave} k={q.k} marca={q.letra} icono={ICONO[q.icono] || AlertOctagon} titulo={q.nombre} subtitulo={`${q.grupo} · ${q.signo}`} cuenta={q.items.length} data-cuadrante={q.clave}>
            <ul className="flex flex-col gap-2.5">
              {q.items.map((i) => (
                <li key={i.codigo} data-codigo={i.codigo} className="rounded-2xl border border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-3.5 text-sm">
                  <div className="mb-1.5"><Chip k={q.k} mono>{i.codigo}</Chip></div>
                  <p className="font-semibold leading-snug">{nb(i.texto)}</p>
                  {i.evidencia ? <p className="mt-1.5 text-xs leading-snug text-muted-foreground">Evidencia: {nb(i.evidencia)}</p> : null}
                </li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>
      {m.conEstrategias ? (
        <>
          <h2 className="mb-4 mt-10 text-3xl">Estrategias cruzadas</h2>
          <div className="grid gap-5 sm:grid-cols-2">
            {m.estrategias.map((e) => (
              <Panel key={e.tipo} k="serie-5" marca={e.tipo} icono={ICONO[e.icono]} titulo={e.nombre} subtitulo={e.subtitulo} cuenta={e.items.length} data-estrategia={e.tipo}>
                <ul className="flex flex-col gap-2.5">
                  {e.items.map((i) => (
                    <li key={i.codigo} data-codigo={i.codigo} className="rounded-2xl border border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-3.5 text-sm">
                      <div className="mb-1.5 flex flex-wrap items-center gap-1.5">
                        <Badge mono variant="brand">{i.codigo}</Badge>
                        {(i.combinaLista || []).map((c) => <Chip key={c} k={colorDe(c)} mono>{c}</Chip>)}
                      </div>
                      <p className="font-semibold leading-snug">{nb(i.texto)}</p>
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
