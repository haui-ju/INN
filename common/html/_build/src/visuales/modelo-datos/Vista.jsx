import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Lamina } from "../../ui/lamina.jsx";

// Diagrama de base de datos de estilo estándar: tablas con cabecera sólida (gris azulado las dimensiones, roja las de hechos) y el nombre
// centrado, una fila por columna con su nombre, su tipo en gris y su marca (PK o FK) a la derecha, y líneas de relación con la notación
// de pata de gallo. Usa los valores del tema claro de los tokens (clase `forzar-claro`) aunque el visual abra en oscuro.
function Tabla({ t, hecho }) {
  return (
    <section
      data-codigo={t.codigo} data-tabla={t.nombre}
      style={{ left: t.x, top: t.y, width: t.w, height: t.h }}
      className="absolute overflow-hidden border-2 border-[color-mix(in_srgb,var(--c-texto)_30%,var(--c-borde))] bg-card"
    >
      <h3 className={`flex h-[34px] items-center justify-center text-[15px] font-bold text-white ${hecho ? "bg-[var(--c-error)]" : "bg-[var(--c-texto-secundario)]"}`}>{t.nombre}</h3>
      <ul className="px-2.5 pt-1">
        {t.filas.map((f, i) => (
          <li key={`${f.nombre}-${i}`} data-columna={f.nombre} className="grid h-[25px] grid-cols-[minmax(0,1fr)_auto_2rem] items-center gap-2 text-[14px]">
            <span className={`truncate ${f.marca === "PK" ? "font-semibold" : ""}`}>{f.nombre}</span>
            <span className="text-[13px] text-muted-foreground">{f.tipo}</span>
            <span className="text-right text-[13px] font-extrabold">{f.marca}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export function Vista({ m }) {
  return (
    <Lamina className="forzar-claro !bg-[var(--c-superficie)] !bg-[linear-gradient(180deg,var(--c-superficie),var(--c-fondo))] !border-border text-foreground">
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      {m.vacio ? <SinDatos /> : (
        <>
          <div data-scroll className="overflow-x-auto overflow-y-hidden py-2">
            <div className="relative mx-auto" style={{ width: m.ancho, height: m.alto }}>
              <svg aria-hidden="true" viewBox={`0 0 ${m.ancho} ${m.alto}`} width={m.ancho} height={m.alto} className="absolute inset-0">
                {m.lineas.map((l) => (
                  <g key={l.codigo} data-relacion-linea={l.codigo} stroke="var(--c-texto-secundario)" strokeWidth="1.8" fill="none">
                    <line x1={l.sx} y1={l.sy} x2={l.ex} y2={l.ey} />
                    <path d={l.simbolos} />
                    {l.circulos.map((c, i) => <circle key={i} cx={c.x} cy={c.y} r="5" fill="var(--c-superficie)" />)}
                  </g>
                ))}
              </svg>
              {m.dimensiones.map((d) => <Tabla key={d.codigo} t={d} hecho={false} />)}
              {m.hechos.map((h) => <Tabla key={h.codigo} t={h} hecho />)}
            </div>
          </div>
          <p className="mt-3 flex flex-wrap items-center justify-center gap-x-8 gap-y-1 text-[13px] text-muted-foreground" data-leyenda>
            <span><b className="text-foreground">PK</b> llave primaria</span>
            <span><b className="text-foreground">FK</b> llave foránea</span>
            <span><b className="text-foreground">| |</b> uno</span>
            <span><b className="text-foreground">o&lt;</b> cero o varios: cada línea es una relación de varios a uno</span>
          </p>
        </>
      )}
    </Lamina>
  );
}
