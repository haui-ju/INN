import { AlertTriangle, CalendarRange, CheckCircle2, Gauge, Timer, TrendingUp, Users } from "lucide-react";
import { Badge } from "./badge.jsx";

const ICONOS = { gauge: Gauge, check: CheckCircle2, alerta: AlertTriangle, sprint: CalendarRange, tiempo: Timer, ritmo: TrendingUp, equipo: Users };

// Encabezado del visual: título grande con una barra de acento y los colores de la serie como firma.
export function Encabezado({ titulo, proyecto, corte, etiqueta = "Inteligencia de Negocios" }) {
  return (
    <header data-encabezado className="mb-7 flex flex-wrap items-end justify-between gap-4">
      <div>
        <p className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-primary-strong">
          <span aria-hidden="true" className="flex gap-1">{[1, 2, 3, 5].map((i) => <i key={i} className="block h-1.5 w-5 rounded-full" style={{ background: `var(--c-serie-${i})` }} />)}</span>
          {etiqueta}
        </p>
        <h1 className="text-4xl">{titulo}</h1>
        <span aria-hidden="true" className="mt-3 block h-1 w-24 rounded-full bg-[linear-gradient(90deg,var(--c-acento),var(--c-serie-1))]" />
        {proyecto ? <p className="mt-3 text-sm text-muted-foreground">{proyecto}</p> : null}
      </div>
      {corte ? <Badge variant="brand" className="px-3 py-1 text-sm" data-ind="corte">{corte}</Badge> : null}
    </header>
  );
}

export function Indicador({ clave, rotulo, texto, icono, tono = "marca" }) {
  const Icono = ICONOS[icono];
  const colores = { marca: "bg-primary/15 text-primary-strong", exito: "bg-success/15 text-success", alerta: "bg-warning/15 text-warning", error: "bg-destructive/15 text-destructive" }[tono];
  return (
    <div className="flex items-start gap-3 rounded-3xl border border-border bg-card p-4 shadow-sm">
      {Icono ? <span className={`mt-0.5 inline-flex size-10 shrink-0 items-center justify-center rounded-2xl ${colores}`}><Icono className="size-5" aria-hidden="true" /></span> : null}
      <div className="min-w-0">
        <div className="text-3xl font-bold leading-none text-foreground" data-ind={clave}>{texto}</div>
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
  return <p className="rounded-3xl border border-dashed border-border px-4 py-12 text-center text-muted-foreground">Sin datos</p>;
}
