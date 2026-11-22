import { cn } from "../lib/utils.js";

// Lámina: una parte de un visual con ancho y proporción de diapositiva. Cada lámina lleva su propio fondo y su propio título,
// de modo que se puede recortar de la captura y pegar sola en una diapositiva.
export function Lamina({ className, children, ...props }) {
  return <section data-lamina className={cn("lienzo rounded-[28px] p-10", className)} {...props}>{children}</section>;
}

// Contenedor de láminas: las separa con un espacio del color de la página para que sea fácil recortar cada una.
export function Laminas({ children }) {
  return <div className="flex flex-col gap-10">{children}</div>;
}
