import { Key, Link2, Sigma, Table2 } from "lucide-react";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Lamina } from "../../ui/lamina.jsx";

// Diagrama de base de datos de estilo estándar: tablas blancas con su cabecera gris, sus columnas con la llave primaria (PK),
// las llaves foráneas (FK) y las medidas (Σ), y líneas grises de relación. Usa los valores del tema claro de los tokens
// (clase `forzar-claro`) para verse como un diagrama de base de datos aunque el visual abra en oscuro.
const ICONO = { PK: Key, FK: Link2, "Σ": Sigma };

function Fila({ f }) {
  const Icono = ICONO[f.rol];
  return (
    <li className="flex h-[25px] items-center gap-2 border-t border-border px-3 text-[13px]" data-columna={f.nombre}>
      <span className="inline-flex w-9 shrink-0 items-center gap-1 text-[11px] font-bold text-muted-foreground">{Icono ? <Icono className="size-3.5" aria-hidden="true" /> : null}{f.rol === "Σ" ? null : f.rol}</span>
      <span className={`truncate font-mono ${f.rol === "PK" ? "font-bold" : ""}`}>{f.nombre}</span>
      {f.detalle ? <span className="ml-auto shrink-0 text-[11px] text-muted-foreground">{f.detalle}</span> : null}
    </li>
  );
}

function Tabla({ t, hecho }) {
  return (
    <section
      data-codigo={t.codigo} data-tabla={t.nombre}
      style={{ left: t.x, top: t.y, width: t.w, height: t.h }}
      className="absolute overflow-hidden rounded-md border border-[color-mix(in_srgb,var(--c-texto)_35%,var(--c-borde))] bg-card shadow-[0_2px_6px_rgba(17,22,58,0.12)]"
    >
      <header className={`flex h-[50px] items-center gap-2 px-3 ${hecho ? "bg-[color-mix(in_srgb,var(--c-texto)_16%,var(--c-borde))]" : "bg-border"}`}>
        <Table2 className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
        <div className="min-w-0">
          <h3 className="truncate text-[16px] leading-tight">{t.nombre}</h3>
          <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">{hecho ? "Tabla de hechos" : "Dimensión"} · {t.codigo}</p>
        </div>
      </header>
      <ul>{t.filas.map((f, i) => <Fila key={`${f.nombre}-${i}`} f={f} />)}</ul>
      {hecho && t.granularidad ? <p className="border-t border-border px-3 py-1.5 text-[12px] italic leading-snug text-muted-foreground">{t.granularidad}</p> : null}
      {!hecho && t.jerarquia ? <p className="truncate border-t border-border px-3 py-1.5 text-[12px] italic text-muted-foreground">Jerarquía: {t.jerarquia}</p> : null}
    </section>
  );
}

export function Vista({ m }) {
  const cuerpo = (
    <Lamina className="forzar-claro !bg-none !bg-[var(--c-superficie)] !border-border text-foreground">
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      {m.vacio ? <SinDatos /> : (
        <>
          <div data-scroll className="overflow-x-auto overflow-y-hidden py-2">
            <div className="relative mx-auto" style={{ width: m.ancho, height: m.alto }}>
              <svg aria-hidden="true" viewBox={`0 0 ${m.ancho} ${m.alto}`} width={m.ancho} height={m.alto} className="absolute inset-0">
                {m.lineas.map((l) => (
                  <g key={l.codigo} data-relacion-linea={l.codigo}>
                    <path d={l.d} fill="none" stroke="var(--c-texto-secundario)" strokeWidth="1.6" />
                    <circle cx={l.sx} cy={l.sy + 14} r="9.5" fill="var(--c-superficie)" stroke="var(--c-texto-secundario)" strokeWidth="1.4" />
                    <text x={l.sx} y={l.sy + 18} textAnchor="middle" fontSize="12" fontWeight="700" fill="var(--c-texto)">{l.ladoHacia}</text>
                    <circle cx={l.ex} cy={l.ey - 14} r="9.5" fill="var(--c-superficie)" stroke="var(--c-texto-secundario)" strokeWidth="1.4" />
                    <text x={l.ex} y={l.ey - 10} textAnchor="middle" fontSize="12" fontWeight="700" fill="var(--c-texto)">{l.ladoDesde === "*" ? "∗" : l.ladoDesde}</text>
                  </g>
                ))}
              </svg>
              {m.dimensiones.map((d) => <Tabla key={d.codigo} t={d} hecho={false} />)}
              {m.hechos.map((h) => <Tabla key={h.codigo} t={h} hecho />)}
            </div>
          </div>
          <p className="mt-3 flex flex-wrap items-center justify-center gap-x-6 gap-y-1 text-[13px] text-muted-foreground" data-leyenda>
            <span><b className="text-foreground">PK</b> llave primaria</span>
            <span><b className="text-foreground">FK</b> llave foránea</span>
            <span><b className="text-foreground">Σ</b> medida (tipo y agregación)</span>
            <span><b className="text-foreground">1</b> uno · <b className="text-foreground">∗</b> varios: cada línea es una relación de varios a uno</span>
          </p>
        </>
      )}
    </Lamina>
  );
  return cuerpo;
}
