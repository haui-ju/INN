import { Activity, Boxes, Coins, Gift, Handshake, HeartHandshake, Receipt, Truck, Users } from "lucide-react";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Panel } from "../../ui/panel.jsx";

const ICONO = { socios: Handshake, actividades: Activity, recursos: Boxes, propuesta: Gift, relaciones: HeartHandshake, canales: Truck, segmentos: Users, costos: Receipt, ingresos: Coins };

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <div className="grid gap-4 lg:grid-cols-10">
        {m.bloques.map((b) => (
          <Panel key={b.clave} tono={b.tono} icono={ICONO[b.icono]} titulo={b.nombre} cuenta={b.items.length} className={b.area} data-bloque={b.clave}>
            <ul className="flex flex-col gap-2 text-sm leading-snug">
              {b.items.map((t, i) => (
                <li key={i} className="flex gap-2"><span aria-hidden="true" className="mt-[0.55em] size-1.5 shrink-0 rounded-full bg-muted-foreground/60" /><span>{t}</span></li>
              ))}
            </ul>
          </Panel>
        ))}
      </div>
    </>
  );
}
