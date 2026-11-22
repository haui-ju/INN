import { cn } from "../lib/utils.js";

// Tonos compartidos por los visuales: color de la barra superior, del icono y del texto de énfasis.
export const TONOS = {
  marca: { barra: "border-t-primary", icono: "bg-primary/15 text-primary-strong", texto: "text-primary-strong", fondo: "bg-primary/8", relleno: "bg-primary" },
  exito: { barra: "border-t-success", icono: "bg-success/15 text-success", texto: "text-success", fondo: "bg-success/8", relleno: "bg-success" },
  alerta: { barra: "border-t-warning", icono: "bg-warning/15 text-warning", texto: "text-warning", fondo: "bg-warning/8", relleno: "bg-warning" },
  error: { barra: "border-t-destructive", icono: "bg-destructive/15 text-destructive", texto: "text-destructive", fondo: "bg-destructive/8", relleno: "bg-destructive" },
  neutro: { barra: "border-t-muted-foreground/50", icono: "bg-border/70 text-muted-foreground", texto: "text-muted-foreground", fondo: "bg-border/30", relleno: "bg-muted-foreground/60" },
};

export function Panel({ tono = "neutro", icono: Icono, titulo, subtitulo, cuenta, className, children, ...props }) {
  const t = TONOS[tono];
  return (
    <section className={cn("flex flex-col rounded-2xl border border-t-4 border-border bg-card p-4 shadow-sm", t.barra, className)} {...props}>
      <header className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          {Icono ? <span className={cn("inline-flex size-8 shrink-0 items-center justify-center rounded-lg", t.icono)}><Icono className="size-[18px]" aria-hidden="true" /></span> : null}
          <div>
            <h2 className="text-lg leading-tight">{titulo}</h2>
            {subtitulo ? <p className="text-xs text-muted-foreground">{subtitulo}</p> : null}
          </div>
        </div>
        {cuenta != null ? <span className={cn("rounded-full px-2.5 py-0.5 text-xs font-semibold tabular-nums", t.icono)}>{cuenta}</span> : null}
      </header>
      {children}
    </section>
  );
}
