import { ChevronDown } from "lucide-react";
import { cn } from "../lib/utils.js";

export function Select({ className, children, ...props }) {
  return (
    <span className="relative inline-flex items-center">
      <select
        className={cn("h-9 cursor-pointer appearance-none rounded-md border border-border bg-card pl-3 pr-8 text-sm text-foreground shadow-sm", className)}
        {...props}
      >
        {children}
      </select>
      <ChevronDown aria-hidden="true" className="pointer-events-none absolute right-2.5 size-4 text-muted-foreground" />
    </span>
  );
}
