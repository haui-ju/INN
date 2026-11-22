import { cva } from "class-variance-authority";
import { cn } from "../lib/utils.js";

const variantes = cva("inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium leading-5 whitespace-nowrap", {
  variants: {
    variant: {
      default: "border-border bg-background text-muted-foreground",
      brand: "border-primary-strong/40 bg-primary/10 text-primary-strong",
      success: "border-success/40 bg-success/10 text-success",
      warning: "border-warning/40 bg-warning/10 text-warning",
      destructive: "border-destructive/40 bg-destructive/10 text-destructive",
    },
    mono: { true: "font-mono", false: "" },
  },
  defaultVariants: { variant: "default", mono: false },
});

export function Badge({ className, variant, mono, ...props }) {
  return <span className={cn(variantes({ variant, mono }), className)} {...props} />;
}
