import { idBilden, kurzBilden } from "./hinterlegen.mjs";

const faelle = [];
export function fall(name, fn) { faelle.push([name, fn]); }
function gleich(ist, soll, was) { if (ist !== soll) throw new Error(`${was}: ist ${JSON.stringify(ist)}, soll ${JSON.stringify(soll)}`); }

const JETZT = new Date(2026, 8, 5, 14, 32); // 05.09.2026 14:32 lokal

fall("kurz: Umlaute, Leerzeichen, Länge", () => {
  gleich(kurzBilden("Stadt Köln"), "stadt-koeln", "koeln");
  gleich(kurzBilden("Bürgerverein Straße e.V."), "buergerverein-strass", "strasse");
  gleich(kurzBilden("A".repeat(40)).length, 20, "gekürzt");
  gleich(kurzBilden("--x--"), "x", "kein Rand-Bindestrich");
});
fall("id: aus Ordner, wenn Buch bekannt", () => {
  gleich(idBilden("Stadt Köln", "koeln", JETZT), "koeln-2026-09051432", "ordner");
});
fall("id: aus Institution, wenn frei", () => {
  gleich(idBilden("Bürgerverein Nord", null, JETZT), "buergerverein-nord-2026-09051432", "frei");
  gleich(/^[a-z0-9][a-z0-9-]*$/.test(idBilden("Ärzte ohne Grenzen!", null, JETZT)), true, "muster");
});

export function pruefen() {
  let fehler = 0;
  for (const [name, fn] of faelle) {
    try { fn(); } catch (e) { fehler++; console.error("hinterlegen:", name, "—", e.message); }
  }
  return fehler;
}

if (process.argv[1] && process.argv[1].endsWith("hinterlegen.pruefung.mjs")) {
  const f = pruefen();
  console.log(f === 0 ? `ok: ${faelle.length} Fälle hinterlegen` : `${f} Fehler`);
  process.exit(f === 0 ? 0 : 1);
}
