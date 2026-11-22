import { createRoot } from "react-dom/client";
import { App } from "../../app/App.jsx";
import * as m from "./modelo.js";
import { Vista } from "./Vista.jsx";

const datos = JSON.parse(document.getElementById("datos").textContent);
createRoot(document.getElementById("raiz")).render(<App visual={m.visual} datos={datos} modelo={m.modelo} fecha={m.fecha} Vista={Vista} ancho={m.ancho} anchoImagen={m.anchoImagen} laminas={m.laminas} />);
