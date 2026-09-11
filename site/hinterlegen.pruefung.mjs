import { idBilden, kurzBilden, uebersetzen, datumPlus, prUrl, urlZuLang, mailUrl, statusUrl, prListeUrl, PR_URL_MAX } from "./hinterlegen.mjs";

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

export const BUECHER = { stand: "2026-09-05", buecher: [
  { ordner: "koeln", titel: "Köln gegen Köln", institution: "Stadt Köln", halter: "Felix Lind", kontakt: "https://belegbar.eu", einreichung: null, repo: "Felix3c/festgehalten", zweig: "main", pfad: "buecher/koeln/wetten", sammelbuch: false },
  { ordner: "hinterlegt", titel: "Hinterlegt", institution: null, halter: "Felix Lind", kontakt: "https://belegbar.eu", einreichung: "buch@example.org", repo: "Felix3c/festgehalten", zweig: "main", pfad: "buecher/hinterlegt/wetten", sammelbuch: true },
]};
export const EINGABE_OK = {
  institution: "Bürgerverein Nord", gesagtVon: "Vorstand", zitat: "Bis Ende Juni 2027 liegt ein spielbarer Build öffentlich vor.",
  stichtag: "2027-06-30", typ: "ja_nein", einheit: "", wert: "", toleranz: "",
  nachweisUrl: "https://example.org/build", bedingung: "Bewilligung des Förderantrags", bedingungFrist: "2027-03-31", quelleUrl: "",
};

fall("datumPlus über Jahresgrenze", () => {
  gleich(datumPlus("2027-12-31", { tage: 1 }), "2028-01-01", "tag");
  gleich(datumPlus("2027-08-31", { monate: 6 }), "2028-02-29", "monat, Monatsende geklemmt");
});
fall("uebersetzen: gültige Eingabe, Sammelbuch", () => {
  const r = uebersetzen(EINGABE_OK, BUECHER, JETZT);
  gleich(Object.keys(r.fehler).length, 0, "keine Fehler " + JSON.stringify(r.fehler));
  gleich(r.zielbuch.ordner, "hinterlegt", "zielbuch");
  gleich(r.id, "buergerverein-nord-2026-09051432", "id");
  for (const z of ["id: buergerverein-nord-2026-09051432", "institution: \"Bürgerverein Nord\"", "gesagt_am: 2026-09-05",
    "quelle: https://github.com/Felix3c/festgehalten/blob/main/buecher/hinterlegt/wetten/buergerverein-nord-2026-09051432.md",
    "typ: ja_nein", "pruefung_am: 2027-07-01", "verfall_am: 2028-01-01", "herkunft: hinterlegt",
    "    wert: 1.00", "    art: angekuendigt", "ausgang: null", "## Nachweis", "## Bedingung", "Bewilligung des Förderantrags", "31.03.2027"]) {
    gleich(r.datei.includes(z), true, "enthält " + z);
  }
});
fall("uebersetzen: Zielbuch aus Liste, eigene Quelle", () => {
  const r = uebersetzen({ ...EINGABE_OK, institution: "Stadt Köln", quelleUrl: "https://stadt-koeln.example/erwartung" }, BUECHER, JETZT);
  gleich(r.zielbuch.ordner, "koeln", "koeln");
  gleich(r.id, "koeln-2026-09051432", "id aus ordner");
  gleich(r.datei.includes("quelle: https://stadt-koeln.example/erwartung"), true, "eigene quelle");
});
fall("uebersetzen: Fehler je Regel", () => {
  const f = (aenderung) => uebersetzen({ ...EINGABE_OK, ...aenderung }, BUECHER, JETZT).fehler;
  gleich("institution" in f({ institution: " " }), true, "institution leer");
  gleich("zitat" in f({ zitat: "x".repeat(601) }), true, "zitat zu lang");
  gleich("stichtag" in f({ stichtag: "2026-09-05" }), true, "stichtag nicht in Zukunft");
  gleich("stichtag" in f({ stichtag: "31.12.2027" }), true, "stichtag falsches Format");
  gleich("nachweisUrl" in f({ nachweisUrl: "ftp://x" }), true, "nachweis keine http-URL");
  gleich("quelleUrl" in f({ quelleUrl: "kein-link" }), true, "quelle keine URL");
  gleich("bedingungFrist" in f({ bedingungFrist: "" }), true, "bedingung ohne frist");
  gleich("einheit" in f({ typ: "punkt", wert: "3", einheit: "" }), true, "punkt ohne einheit");
  gleich("wert" in f({ typ: "punkt", wert: "abc", einheit: "Mio EUR" }), true, "punkt wert keine zahl");
  gleich("toleranz" in f({ typ: "punkt", wert: "3", einheit: "Mio EUR", toleranz: "x" }), true, "toleranz keine zahl");
});
fall("uebersetzen: punkt schreibt einheit, wert, toleranz", () => {
  const r = uebersetzen({ ...EINGABE_OK, typ: "punkt", wert: "2000", einheit: "Plätze", toleranz: "0.10" }, BUECHER, JETZT);
  gleich(Object.keys(r.fehler).length, 0, "ok");
  for (const z of ["typ: punkt", "einheit: \"Plätze\"", "toleranz: 0.10", "    wert: 2000"]) gleich(r.datei.includes(z), true, z);
});
fall("prUrl: GitHub neue Datei mit Pfad und Inhalt", () => {
  const u = prUrl(BUECHER.buecher[1], "x-2026-01010000", "---\nid: x\n---\n");
  gleich(u.startsWith("https://github.com/Felix3c/festgehalten/new/main/buecher/hinterlegt/wetten?filename=x-2026-01010000.md&value="), true, "anfang");
  gleich(decodeURIComponent(u.split("&value=")[1]), "---\nid: x\n---\n", "inhalt");
});
fall("urlZuLang: an der Grenze", () => {
  gleich(urlZuLang("a".repeat(PR_URL_MAX)), false, "genau");
  gleich(urlZuLang("a".repeat(PR_URL_MAX + 1)), true, "drüber");
});
fall("mailUrl: nur mit einreichung", () => {
  gleich(mailUrl(BUECHER.buecher[0], "k-1"), null, "koeln ohne");
  const m = mailUrl(BUECHER.buecher[1], "k-1");
  gleich(m.startsWith("mailto:buch@example.org?subject=Hinterlegung%20k-1&body="), true, "sammelbuch");
});
fall("statusUrl und prListeUrl", () => {
  gleich(statusUrl(BUECHER.buecher[0]), "https://felix3c.github.io/festgehalten/koeln/wettbuch.json", "status");
  gleich(prListeUrl(BUECHER.buecher[0]), "https://github.com/Felix3c/festgehalten/pulls", "prs");
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
