import { cva } from "class-variance-authority";
import { cn } from "../lib/utils.js";

const variantes = cva("inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-semibold leading-5 whitespace-nowrap", {
  variants: {
    variant: {
      default: "border-border bg-[color-mix(in_srgb,var(--c-texto)_6%,transparent)] text-muted-foreground",
      brand: "border-[color-mix(in_srgb,var(--c-acento)_55%,transparent)] bg-[color-mix(in_srgb,var(--c-acento)_16%,transparent)] text-primary-strong",
      success: "border-[color-mix(in_srgb,var(--c-exito)_55%,transparent)] bg-[color-mix(in_srgb,var(--c-exito)_16%,transparent)] text-success",
      warning: "border-[color-mix(in_srgb,var(--c-alerta)_55%,transparent)] bg-[color-mix(in_srgb,var(--c-alerta)_16%,transparent)] text-warning",
      destructive: "border-[color-mix(in_srgb,var(--c-error)_55%,transparent)] bg-[color-mix(in_srgb,var(--c-error)_16%,transparent)] text-destructive",
    },
    mono: { true: "font-mono", false: "" },
  },
  defaultVariants: { variant: "default", mono: false },
});

export function Badge({ className, variant, mono, ...props }) {
  return <span className={cn(variantes({ variant, mono }), className)} {...props} />;
}

// Etiqueta con el color de una serie (`k` = `serie-1`…): el texto va en tinta, la identidad la da el punto y el borde.
export function Chip({ k = "serie-3", mono, className, children, ...props }) {
  return (
    <span
      style={{ "--k": `var(--c-${k})` }}
      className={cn("inline-flex items-center gap-1.5 rounded-full border border-[color-mix(in_srgb,var(--k)_55%,transparent)] bg-[color-mix(in_srgb,var(--k)_16%,transparent)] px-2.5 py-0.5 text-xs font-semibold leading-5 whitespace-nowrap text-foreground", mono && "font-mono", className)}
      {...props}
    >
      <i aria-hidden="true" className="block size-1.5 rounded-full bg-[var(--k)]" />
      {children}
    </span>
  );
}
