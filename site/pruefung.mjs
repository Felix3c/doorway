// node site/pruefung.mjs — prueft, dass Regeln und Seite zusammenpassen.
import { readFileSync } from "node:fs";
import { kompilieren, selbstpruefung, pruefen } from "./regeln.mjs";

const daten = JSON.parse(readFileSync(new URL("./daten/panel.json", import.meta.url), "utf-8"));
const regeln = kompilieren(daten.regeln);
const abweichungen = selbstpruefung(regeln, daten.beispiele);

let fehler = abweichungen.length;
for (const a of abweichungen) console.error("Abweichung:", a);

// Bedingungsregeln
if (!pruefen(regeln, "", "Firma", false).some((r) => r.bedingung === "typ_firma")) { console.error("typ_firma greift nicht"); fehler++; }
if (!pruefen(regeln, "", "Verein", true).some((r) => r.bedingung === "mehrfachantrag")) { console.error("mehrfachantrag greift nicht"); fehler++; }
if (pruefen(regeln, "Digitalisierung des Ortsarchivs", "Verein", false).length !== 0) { console.error("unauffaelliges Vorhaben loest Regel aus"); fehler++; }

// Vorschlagstabelle vollstaendig
for (const klasse of ["bis_2000", "bis_5000", "bis_50000", "mehr"]) {
  for (const typ of ["Verein", "Initiative", "Stiftung", "Kirche", "Kommune", "Privatperson", "Firma"]) {
    if (!daten.schaetzungen[daten.vorschlag[klasse][typ]]) { console.error("Vorschlag ohne Schaetzung:", klasse, typ); fehler++; }
  }
}

console.log(fehler === 0 ? `ok: ${Object.values(daten.beispiele).flat().length} Beispiele, ${regeln.length} Regeln` : `${fehler} Fehler`);
process.exit(fehler === 0 ? 0 : 1);
