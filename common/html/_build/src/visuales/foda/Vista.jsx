import { AlertOctagon, Crosshair, LifeBuoy, Rocket, Shield, ShieldAlert, ShieldCheck, Shuffle, TrendingDown } from "lucide-react";
import { Badge, Chip } from "../../ui/badge.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Lamina, Laminas } from "../../ui/lamina.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { fuerza: ShieldCheck, debil: TrendingDown, oportunidad: Rocket, amenaza: ShieldAlert, fo: Crosshair, fa: Shield, do: Shuffle, da: LifeBuoy };
// Cada código FODA lleva el color de su cuadrante: así se ve de dónde sale cada estrategia.
const COLOR = { FOR: "serie-1", DEB: "serie-4", OPO: "serie-3", AME: "serie-2" };
const colorDe = (codigo) => COLOR[String(codigo).slice(0, 3)] || "serie-5";
const ITEM = "rounded-2xl border border-[color-mix(in_srgb,var(--k)_28%,var(--c-borde))] bg-[color-mix(in_srgb,var(--c-fondo)_55%,transparent)] p-4";

export function Vista({ m }) {
  if (m.vacio) return (<Lamina><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></Lamina>);
  return (
    <Laminas>
      {m.partes.map((p) => (
        <Lamina key={p.id} data-parte={p.id}>
          <Encabezado titulo={p.titulo} proyecto={m.proyecto} />
          <div className="grid grid-cols-2 items-start gap-6">
            {p.cuadrantes.map((q) => (
              <Panel key={q.clave} k={q.k} marca={q.letra} icono={ICONO[q.icono] || AlertOctagon} titulo={q.nombre} subtitulo={`${q.grupo} · ${q.signo}`} cuenta={q.items.length} className="!p-6" data-cuadrante={q.clave}>
                <ul className="flex flex-col gap-2.5">
                  {q.items.map((i) => (
                    <li key={i.codigo} data-codigo={i.codigo} className={`${ITEM} flex items-start gap-3 !px-4 !py-3`}>
                      <Chip k={q.k} mono className="mt-0.5 shrink-0 text-[13px]">{i.codigo}</Chip>
                      <p className="text-[17px] font-semibold leading-snug">{nb(i.texto)}</p>
                    </li>
                  ))}
                </ul>
              </Panel>
            ))}
          </div>
        </Lamina>
      ))}
      {m.conEstrategias ? (
        <Lamina data-parte="estrategias">
          <Encabezado titulo="Estrategias cruzadas del FODA" proyecto={m.proyecto} />
          <div className="grid grid-cols-2 items-start gap-6">
            {m.tipos.map((e) => (
              <Panel key={e.tipo} k={e.k} marca={e.tipo} icono={ICONO[e.icono]} titulo={e.nombre} subtitulo={e.subtitulo} cuenta={e.items.length} className="!p-6" data-estrategia={e.tipo}>
                <ul className="flex flex-col gap-3.5">
                  {e.items.map((i) => (
                    <li key={i.codigo} data-codigo={i.codigo} className={ITEM}>
                      <div className="mb-2 flex flex-wrap items-center gap-1.5">
                        <Badge mono variant="brand">{i.codigo}</Badge>
                        {i.combina.map((c) => <Chip key={c} k={colorDe(c)} mono>{c}</Chip>)}
                      </div>
                      <p className="text-[17px] font-semibold leading-snug">{nb(i.texto)}</p>
                    </li>
                  ))}
                </ul>
              </Panel>
            ))}
          </div>
        </Lamina>
      ) : null}
    </Laminas>
  );
}
