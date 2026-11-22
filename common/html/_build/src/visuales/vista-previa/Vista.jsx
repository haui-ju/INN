import { Badge } from "../../ui/badge.jsx";
import { Button } from "../../ui/button.jsx";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../ui/card.jsx";
import { Encabezado, SinDatos } from "../../ui/encabezado.jsx";
import { Progress } from "../../ui/progress.jsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../ui/table.jsx";

function Seccion({ titulo, children }) {
  return (
    <section className="mt-10">
      <h2 className="mb-4 text-2xl">{titulo}</h2>
      {children}
    </section>
  );
}

export function Vista({ m }) {
  if (m.vacio) return (<><Encabezado titulo={m.titulo} proyecto={m.proyecto} /><SinDatos /></>);
  return (
    <>
      <Encabezado titulo={m.titulo} proyecto={m.proyecto} />
      <Seccion titulo="Color">
        <div className="grid grid-cols-[repeat(auto-fill,minmax(140px,1fr))] gap-3">
          {m.colores.map((k) => (
            <div key={k} className="overflow-hidden rounded-2xl border border-border bg-card text-xs">
              <i className="block h-12" style={{ background: `var(--c-${k})` }} />
              <b className="block px-2 pt-1 font-medium">{k}</b>
              <span className="block px-2 pb-1 font-mono text-muted-foreground">var(--c-{k})</span>
            </div>
          ))}
        </div>
      </Seccion>
      <Seccion titulo="Tipografía">
        <div className="grid gap-4 sm:grid-cols-3">
          <Card><CardHeader><CardDescription>Titulares · Segoe UI</CardDescription></CardHeader><CardContent><p className="text-3xl font-bold">Margen neto por canal</p></CardContent></Card>
          <Card><CardHeader><CardDescription>Texto · Segoe UI</CardDescription></CardHeader><CardContent><p className="text-base">Comparar la rentabilidad de cada canal para decidir precios y producción.</p></CardContent></Card>
          <Card><CardHeader><CardDescription>Códigos · monoespaciada</CardDescription></CardHeader><CardContent><p className="font-mono text-base">OE-02 · CAU-04</p></CardContent></Card>
        </div>
        <div className="mt-4 grid gap-2">
          {m.escala.map((e) => (
            <div key={e.clave} className="flex items-baseline gap-4">
              <span className="font-semibold" style={{ fontSize: `var(--t-${e.clave})` }}>Aa Margen neto por canal</span>
              <code className="text-xs text-muted-foreground">{e.clave} · {e.valor}</code>
            </div>
          ))}
        </div>
      </Seccion>
      <Seccion titulo="Espacio, radio y sombra">
        <div className="grid gap-2">
          {m.espacios.map((e) => (
            <div key={e.clave} className="flex items-center gap-3">
              <i className="block h-3 rounded-sm bg-primary" style={{ width: `var(--espacio-${e.clave})` }} />
              <span className="font-mono text-xs text-muted-foreground">espacio.{e.clave} · {e.valor}</span>
            </div>
          ))}
        </div>
        <div className="mt-4 flex flex-wrap gap-4">
          {m.radios.map((r) => (
            <div key={r.clave} className="flex h-16 w-28 items-end border border-border bg-card p-2" style={{ borderRadius: `var(--radio-${r.clave})` }}>
              <span className="font-mono text-xs text-muted-foreground">radio.{r.clave} · {r.valor}</span>
            </div>
          ))}
          {m.sombras.map((s) => (
            <div key={s} className="flex h-16 w-28 items-end rounded-md bg-card p-2" style={{ boxShadow: `var(--sombra-${s})` }}>
              <span className="font-mono text-xs text-muted-foreground">sombra.{s}</span>
            </div>
          ))}
        </div>
      </Seccion>
      <Seccion titulo="Tarjetas y barra de progreso">
        <div className="grid gap-4 sm:grid-cols-3">
          {[["Calidad de datos del ETL", "Registros de ventas que pasan las reglas de calidad.", 92, "92 % · meta 98 %"],
            ["Canales con margen calculado", "Canales de venta con su margen neto medido.", 60, "3 de 5 canales · 60 %"],
            ["Páginas del dashboard", "Páginas publicadas con sus filtros y KPI.", 100, "4 de 4 páginas · 100 %"]].map(([t, d, v, x]) => (
            <Card key={t}>
              <CardHeader><CardTitle>{t}</CardTitle><CardDescription>{d}</CardDescription></CardHeader>
              <CardContent><Progress value={v} aria-label={t} /><p className="mt-2 text-xs text-muted-foreground">{x}</p></CardContent>
            </Card>
          ))}
        </div>
      </Seccion>
      <Seccion titulo="Tabla y etiquetas de estado">
        <Table>
          <TableHeader><TableRow><TableHead>KPI</TableHead><TableHead>Fuente</TableHead><TableHead>Fecha</TableHead><TableHead>Estado</TableHead></TableRow></TableHeader>
          <TableBody>
            <TableRow><TableCell>Margen neto por canal</TableCell><TableCell>Caja y aplicaciones</TableCell><TableCell>03-11-2026</TableCell><TableCell><Badge variant="success">En meta</Badge></TableCell></TableRow>
            <TableRow className="bg-background"><TableCell>Merma por turno</TableCell><TableCell>Producción de cocina</TableCell><TableCell>10-11-2026</TableCell><TableCell><Badge variant="warning">Bajo la meta</Badge></TableCell></TableRow>
            <TableRow><TableCell>Ticket promedio</TableCell><TableCell>Caja</TableCell><TableCell>14-11-2026</TableCell><TableCell><Badge variant="destructive">Sin datos</Badge></TableCell></TableRow>
            <TableRow><TableCell>Costo del pollo vivo</TableCell><TableCell>MIDAGRI</TableCell><TableCell>30-11-2026</TableCell><TableCell><Badge>Pendiente</Badge></TableCell></TableRow>
          </TableBody>
        </Table>
      </Seccion>
      <Seccion titulo="Botones">
        <div className="flex flex-wrap items-center gap-3">
          <Button>Guardar</Button>
          <Button variant="outline">Cancelar</Button>
          <Button variant="ghost">Omitir</Button>
          <Button disabled>Deshabilitado</Button>
        </div>
      </Seccion>
    </>
  );
}
