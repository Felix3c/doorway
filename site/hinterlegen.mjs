// site/hinterlegen.mjs — reines Modul, kein DOM. Eingaben -> Datei im festgehalten-Format v1.
// Spec: docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md §3, §4, §6.

const UMLAUTE = { ä: "ae", ö: "oe", ü: "ue", ß: "ss" };

export function kurzBilden(text) {
  const k = String(text).toLowerCase()
    .replace(/[äöüß]/g, (c) => UMLAUTE[c])
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return k.slice(0, 20).replace(/-+$/g, "");
}

const zwei = (n) => String(n).padStart(2, "0");
export const isoDatum = (d) => `${d.getFullYear()}-${zwei(d.getMonth() + 1)}-${zwei(d.getDate())}`;

export function idBilden(institution, ordner, jetzt) {
  const kurz = ordner || kurzBilden(institution) || "hinterlegt";
  return `${kurz}-${jetzt.getFullYear()}-${zwei(jetzt.getMonth() + 1)}${zwei(jetzt.getDate())}${zwei(jetzt.getHours())}${zwei(jetzt.getMinutes())}`;
}

export const GRENZEN = { institution: 120, gesagtVon: 120, zitat: 400, bedingung: 200 };
const ISO = /^\d{4}-\d{2}-\d{2}$/;
const istUrl = (s) => /^https?:\/\/\S+$/.test(s);
const istZahl = (s) => s !== "" && Number.isFinite(Number(s));

export function datumPlus(iso, { tage = 0, monate = 0 }) {
  const [j, m, t] = iso.split("-").map(Number);
  const ziel = new Date(j, m - 1 + monate, 1);
  const letzter = new Date(ziel.getFullYear(), ziel.getMonth() + 1, 0).getDate();
  ziel.setDate(Math.min(t, letzter) + tage);
  return isoDatum(ziel);
}

export const yamlText = (s) => `"${String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
const deDatum = (iso) => { const [j, m, t] = iso.split("-"); return `${t}.${m}.${j}`; };

function zielbuchFinden(institution, buecher) {
  const treffer = buecher.buecher.find((b) => b.institution && b.institution.toLowerCase() === institution.toLowerCase());
  return treffer || buecher.buecher.find((b) => b.sammelbuch) || null;
}

export function pruefeEingaben(e, jetzt) {
  const f = {};
  for (const [feld, max] of Object.entries(GRENZEN)) {
    const wert = (e[feld] || "").trim();
    if (["institution", "gesagtVon", "zitat"].includes(feld) && !wert) f[feld] = "Bitte ausfüllen.";
    else if (wert.length > max) f[feld] = `Höchstens ${max} Zeichen.`;
  }
  if (!ISO.test(e.stichtag || "")) f.stichtag = "Bitte ein Datum wählen.";
  else if (e.stichtag <= isoDatum(jetzt)) f.stichtag = "Der Stichtag muss in der Zukunft liegen.";
  if (!istUrl((e.nachweisUrl || "").trim())) f.nachweisUrl = "Bitte eine Adresse mit http:// oder https:// angeben, unter der das Ergebnis am Stichtag sichtbar sein wird.";
  if ((e.quelleUrl || "").trim() && !istUrl(e.quelleUrl.trim())) f.quelleUrl = "Wenn angegeben, muss die Quelle eine Adresse mit http:// oder https:// sein.";
  if ((e.bedingung || "").trim() && !ISO.test(e.bedingungFrist || "")) f.bedingungFrist = "Eine Bedingung braucht eine Frist, bis zu der sie feststeht.";
  if (e.typ === "punkt") {
    if (!(e.einheit || "").trim()) f.einheit = "Bei einer Zahl braucht es eine Einheit, z. B. Plätze oder Mio EUR.";
    if (!istZahl((e.wert || "").trim())) f.wert = "Bitte eine Zahl angeben.";
    if ((e.toleranz || "").trim() && !istZahl(e.toleranz.trim())) f.toleranz = "Die Toleranz muss eine Zahl sein, z. B. 0.10 für ±10 %.";
  } else if (e.typ !== "ja_nein") f.typ = "Bitte Ja/Nein oder Zahl wählen.";
  return f;
}

export function uebersetzen(e, buecher, jetzt) {
  const fehler = pruefeEingaben(e, jetzt);
  if (Object.keys(fehler).length) return { datei: "", id: "", zielbuch: null, fehler };
  const institution = e.institution.trim();
  const zielbuch = zielbuchFinden(institution, buecher);
  if (!zielbuch) return { datei: "", id: "", zielbuch: null, fehler: { institution: "Kein Buch gefunden, das diesen Eintrag aufnehmen kann." } };
  const ordner = zielbuch.institution && zielbuch.institution.toLowerCase() === institution.toLowerCase() ? zielbuch.ordner : null;
  const id = idBilden(institution, ordner, jetzt);
  const heute = isoDatum(jetzt);
  const pruefungAm = datumPlus(e.stichtag, { tage: 1 });
  const verfallAm = datumPlus(pruefungAm, { monate: 6 });
  const quelle = (e.quelleUrl || "").trim() || `https://github.com/${zielbuch.repo}/blob/${zielbuch.zweig}/${zielbuch.pfad}/${id}.md`;
  const punkt = e.typ === "punkt";
  const kern = e.zitat.trim().replace(/[.!?]+$/, "");
  const frage = punkt
    ? `${kern} — welcher Wert in ${e.einheit.trim()} am ${deDatum(e.stichtag)}?`
    : `Trifft am ${deDatum(e.stichtag)} zu: ${kern}?`;
  const bedingung = (e.bedingung || "").trim();
  const vermerke = bedingung
    ? `vermerke:\n  - am: ${heute}\n    text: ${yamlText(`Bedingung: ${bedingung}. Muss feststehen bis ${deDatum(e.bedingungFrist)}. Fällt sie nachweislich aus, wird der Eintrag nach verfall_am mit Beleg des Ausfalls auf verfallen gesetzt.`)}`
    : "vermerke: []";
  const kopf = [
    "---", `id: ${id}`, `institution: ${yamlText(institution)}`, `gesagt_von: ${yamlText(e.gesagtVon.trim())}`,
    `gesagt_am: ${heute}`, `quelle: ${quelle}`, `zitat: ${yamlText(e.zitat.trim())}`, `frage: ${yamlText(frage)}`,
    `typ: ${e.typ}`, ...(punkt ? [`einheit: ${yamlText(e.einheit.trim())}`] : []),
    ...(punkt && (e.toleranz || "").trim() ? [`toleranz: ${e.toleranz.trim()}`] : []),
    `pruefung_am: ${pruefungAm}`, `verfall_am: ${verfallAm}`, "herkunft: hinterlegt",
    "prognosen:", `  - von: ${yamlText(institution)}`, `    wert: ${punkt ? e.wert.trim() : "1.00"}`,
    `    hinterlegt_am: ${heute}`, "    art: angekuendigt",
    "ausgang: null", "aufgeloest_am: null", "beleg_ausgang: null", vermerke, "---",
  ].join("\n");
  const text = [
    "", "## Kontext",
    `Hinterlegt von ${institution} (${e.gesagtVon.trim()}) am ${deDatum(heute)} über Doorway, Zielbuch „${zielbuch.titel}". Die Erwartung wurde vorab festgehalten, nicht aus einer Veröffentlichung zitiert.`,
    "", "## Übersetzung",
    `Die Erwartung wird wörtlich genommen: ${punkt ? "eine Zahl" : "Ja oder Nein"} am ${deDatum(e.stichtag)}, Prüfung ab ${deDatum(pruefungAm)}. Teilerfüllung ist Nein (Format §2.2). Verfall am ${deDatum(verfallAm)} (Halter-Regel: Prüfdatum plus sechs Monate).`,
    "", "## Nachweis",
    `Das Ergebnis wird am Stichtag hier sichtbar sein: ${e.nachweisUrl.trim()} . Ein Schnappschuss dieses Ortes am Prüftag ohne das Artefakt gilt als Beleg für Nein.`,
    ...(bedingung ? ["", "## Bedingung", `${bedingung}. Muss feststehen bis ${deDatum(e.bedingungFrist)}.`] : []),
    "", `## Begründung ${institution}`,
    `„${e.zitat.trim()}" — beim Wort genommen, ohne Vorbehalt (${punkt ? `Wert ${e.wert.trim()} ${e.einheit.trim()}` : "1,00"}).`, "",
  ].join("\n");
  return { datei: kopf + "\n" + text, id, zielbuch, fehler: {} };
}

export const PR_URL_MAX = 6400; // gemessen am 11.09.2026 gegen github.com (curl, nicht eingeloggt): bis 6905 Zeichen HTTP 302, ab 7043 HTTP 500; Grenze = 6900 − 500 Sicherheitsrand
export const FESTGEHALTEN_SEITE = "https://felix3c.github.io/festgehalten";

export const prUrl = (b, id, datei) =>
  `https://github.com/${b.repo}/new/${b.zweig}/${b.pfad}?filename=${encodeURIComponent(id + ".md")}&value=${encodeURIComponent(datei)}`;
export const urlZuLang = (url) => url.length > PR_URL_MAX;
export const mailUrl = (b, id) => b.einreichung
  ? `mailto:${b.einreichung}?subject=${encodeURIComponent("Hinterlegung " + id)}&body=${encodeURIComponent(`Bitte die heruntergeladene Datei ${id}.md anhängen. Zielbuch: ${b.titel}.`)}`
  : null;
export const statusUrl = (b) => `${FESTGEHALTEN_SEITE}/${b.ordner}/wettbuch.json`;
export const prListeUrl = (b) => `https://github.com/${b.repo}/pulls`;
