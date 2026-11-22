import { Activity, Boxes, Coins, Gift, Handshake, HeartHandshake, Receipt, Truck, Users } from "lucide-react";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";
import { nb } from "../../lib/utils.js";

const ICONO = { socios: Handshake, actividades: Activity, recursos: Boxes, propuesta: Gift, relaciones: HeartHandshake, canales: Truck, segmentos: Users, costos: Receipt, ingresos: Coins };

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div className="grid gap-5 lg:grid-cols-10">
        {m.bloques.map((b) => (
          <Panel key={b.clave} k={b.k} icono={ICONO[b.icono]} titulo={b.nombre} cuenta={b.items.length} className={b.area} data-bloque={b.clave}>
            <ul className="flex flex-col gap-2 text-sm leading-snug">
              {b.items.map((t, i) => (
                <li key={i} className="rounded-xl border-l-4 border-[var(--k)] bg-[color-mix(in_srgb,var(--c-texto)_6%,transparent)] px-3 py-2">{nb(t)}</li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>
    </>
  );
}
