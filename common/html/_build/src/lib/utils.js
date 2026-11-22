import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...entradas) {
  return twMerge(clsx(entradas));
}

// Espacio duro antes de «%» para que una cifra no se parta en dos líneas («18 %»).
export const nb = (t) => String(t ?? "").replace(/(\d) %/g, "$1\u00a0%");
