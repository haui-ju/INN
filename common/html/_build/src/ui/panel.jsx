import { cn } from "../lib/utils.js";

// Tonos de estado (compatibilidad): cada uno apunta a un color de los tokens.
export const TONOS = {
  marca: { k: "acento" }, exito: { k: "exito" }, alerta: { k: "alerta" }, error: { k: "error" }, neutro: { k: "serie-3" },
};

// Panel con identidad de color: `k` es el nombre de un token (`serie-1`…`serie-8`, `acento`, `exito`…).
// El color tiñe el borde, el fondo y el resplandor; el icono va en un círculo sólido.
export function Panel({ k = "serie-3", tono, icono: Icono, titulo, subtitulo, cuenta, marca, className, children, ...props }) {
  const color = tono ? TONOS[tono].k : k;
  return (
    <section
      style={{ "--k": `var(--c-${color})` }}
      className={cn(
        "relative flex flex-col overflow-hidden rounded-3xl border border-[color-mix(in_srgb,var(--k)_34%,var(--c-borde))] bg-[linear-gradient(155deg,color-mix(in_srgb,var(--k)_13%,var(--c-superficie)),var(--c-superficie)_64%)] p-5 shadow-[0_20px_50px_-28px_var(--k)]",
        className,
      )}
      {...props}
    >
      <span aria-hidden="true" className="pointer-events-none absolute -right-12 -top-12 size-40 rounded-full bg-[var(--k)] opacity-[0.14] blur-2xl" />
      {marca ? <span aria-hidden="true" className="pointer-events-none absolute -bottom-6 right-3 select-none text-[9rem] font-black leading-none text-[var(--k)] opacity-[0.09]">{marca}</span> : null}
      <header className="relative mb-4 flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          {Icono ? <span className="inline-flex size-10 shrink-0 items-center justify-center rounded-2xl bg-[var(--k)] text-[var(--c-superficie)] shadow-[0_8px_20px_-8px_var(--k)]"><Icono className="size-5" aria-hidden="true" /></span> : null}
          <div>
            <h2 className="text-lg leading-tight">{titulo}</h2>
            {subtitulo ? <p className="text-xs text-muted-foreground">{subtitulo}</p> : null}
          </div>
        </div>
        {cuenta != null ? <span className="rounded-full bg-[color-mix(in_srgb,var(--k)_22%,transparent)] px-3 py-0.5 text-sm font-bold tabular-nums text-foreground">{cuenta}</span> : null}
      </header>
      <div className="relative flex flex-1 flex-col">{children}</div>
    </section>
  );
}
