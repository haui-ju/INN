import * as ProgressPrimitive from "@radix-ui/react-progress";
import { cn } from "../lib/utils.js";

export function Progress({ className, value = 0, ...props }) {
  return (
    <ProgressPrimitive.Root className={cn("relative h-2 w-full overflow-hidden rounded-full bg-border", className)} value={value} {...props}>
      <ProgressPrimitive.Indicator className="h-full rounded-full bg-primary" style={{ width: `${value}%` }} />
    </ProgressPrimitive.Root>
  );
}
