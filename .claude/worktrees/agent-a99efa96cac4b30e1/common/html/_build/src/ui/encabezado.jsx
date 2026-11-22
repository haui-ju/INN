import { AlertTriangle, CalendarRange, CheckCircle2, Gauge, Timer, TrendingUp, Users } from "lucide-react";
import { Badge } from "./badge.jsx";

const ICONOS = { gauge: Gauge, check: CheckCircle2, alerta: AlertTriangle, sprint: CalendarRange, tiempo: Timer, ritmo: TrendingUp, equipo: Users };

export function Encabezado({ titulo, proyecto, corte }) {
  return (
    <header className="mb-6 flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 className="text-3xl sm:text-4xl">{titulo}</h1>
        {proyecto ? <p className="mt-1 text-sm text-muted-foreground">{proyecto}</p> : null}
      </div>
      {corte ? <Badge variant="brand" className="px-3 py-1 text-sm" data-ind="corte">{corte}</Badge> : null}
    </header>
  );
}

export function Indicador({ clave, rotulo, texto, icono, tono = "marca" }) {
  const Icono = ICONOS[icono];
  const colores = { marca: "bg-primary/12 text-primary-strong", exito: "bg-success/12 text-success", alerta: "bg-warning/14 text-warning", error: "bg-destructive/12 text-destructive" }[tono];
  return (
    <div className="flex items-start gap-3 rounded-xl border border-border bg-card p-4 shadow-sm">
      {Icono ? <span className={`mt-0.5 inline-flex size-9 shrink-0 items-center justify-center rounded-lg ${colores}`}><Icono className="size-[18px]" aria-hidden="true" /></span> : null}
      <div className="min-w-0">
        <div className="font-serif text-3xl leading-none text-foreground" data-ind={clave}>{texto}</div>
        <div className="mt-2 text-xs leading-snug text-muted-foreground">{rotulo}</div>
      </div>
    </div>
  );
}

export function Avatar({ nombre, className = "" }) {
  const i = String(nombre || "").trim().split(/\s+/).filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join("");
  return (
    <span title={nombre} className={`inline-flex size-6 shrink-0 items-center justify-center rounded-full bg-primary/15 text-[10px] font-semibold text-primary-strong ${className}`}>{i || "?"}</span>
  );
}

export function SinDatos() {
  return <p className="rounded-xl border border-dashed border-border px-4 py-12 text-center text-muted-foreground">Sin datos</p>;
}
