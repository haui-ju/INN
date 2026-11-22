import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...entradas) {
  return twMerge(clsx(entradas));
}

// Espacios duros para que una cifra no se parta en dos líneas: «18 %», «S/ 6.10» y «8:00 p. m.».
export const nb = (t) => String(t ?? "")
  .replace(/(\d) %/g, "$1\u00a0%")
  .replace(/S\/ (\d)/g, "S/\u00a0$1")
  .replace(/\b([ap])\. m\./g, "$1.\u00a0m.");
