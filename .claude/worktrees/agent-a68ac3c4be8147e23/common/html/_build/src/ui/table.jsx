import { cn } from "../lib/utils.js";

export function Table({ className, ...props }) {
  return (
    <div data-scroll className="overflow-x-auto rounded-xl border border-border bg-card">
      <table className={cn("w-full border-collapse text-sm", className)} {...props} />
    </div>
  );
}
export function TableHeader(props) { return <thead {...props} />; }
export function TableBody(props) { return <tbody {...props} />; }
export function TableRow({ className, ...props }) {
  return <tr className={cn("border-b border-border last:border-0", className)} {...props} />;
}
export function TableHead({ className, ...props }) {
  return <th className={cn("px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-muted-foreground", className)} {...props} />;
}
export function TableCell({ className, ...props }) {
  return <td className={cn("px-4 py-3 align-middle whitespace-nowrap", className)} {...props} />;
}
