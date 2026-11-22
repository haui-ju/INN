import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import { cn } from "../lib/utils.js";

const variantes = cva(
  "inline-flex shrink-0 items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-semibold transition-[filter,background-color,box-shadow] disabled:pointer-events-none disabled:opacity-50 [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-[0_8px_24px_-10px_var(--c-acento)] hover:brightness-110 active:brightness-95",
        outline: "border border-border bg-card text-foreground hover:border-primary hover:text-primary-strong",
        ghost: "text-foreground hover:bg-card",
      },
      size: { default: "h-10 px-5", sm: "h-8 px-3", icon: "size-10" },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export function Button({ className, variant, size, asChild = false, ...props }) {
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn(variantes({ variant, size }), className)} {...props} />;
}
