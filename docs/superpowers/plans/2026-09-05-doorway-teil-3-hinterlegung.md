# Doorway Teil 3: Hinterlegungs-Pfad — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine Seite `site/hinterlegen.html`, die aus sieben Antworten eine Datei im festgehalten-Format erzeugt und sie als vorausgefüllten Pull Request, Download oder Mail an das Zielbuch übergibt.

**Architecture:** Ein reines Modul `site/hinterlegen.mjs` (Eingaben → Datei, Prüfung, PR-URL) ohne DOM, getestet mit Node und per Rundlauf gegen den echten Generator. Eine dünne Seite `site/hinterlegen-seite.js` hängt Felder an das Modul, hält den Entwurf in `localStorage` und fragt auf Klick den Status in der statischen `wettbuch.json` des Zielbuchs ab. Kein Server, keine Speicherung außerhalb des Browsers.

**Tech Stack:** Vanilla ES-Module im Browser, Node ≥ 20 für Tests (`node site/pruefung.mjs`), Python 3.11 + pytest für den Rundlauf, `stil.css` unverändert.

**Spec:** `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`, Abschnitte 2, 3, 4, 6, 7.

**Voraussetzung:** Der festgehalten-Plan `~/wettbuch/docs/superpowers/plans/2026-09-05-hinterlegt-sammelbuch-und-buchliste.md` ist ausgeführt und gepusht. Sein letzter Commit ist `FESTGEHALTEN_SHA` (hier eintragen: `________`).

## Global Constraints

- Nichts verlässt den Browser außer der Statusabfrage auf Klick (Spec §6.4). Kein Fetch beim Ausfüllen.
- Der Hinterlegende sieht nie einen YAML-Feldnamen; Fehler stehen in Worten am Feld.
- Feste Werte laut Spec §3: `herkunft: hinterlegt`, `art: angekuendigt`, `wert: 1.00` bei Ja/Nein, `pruefung_am` = Stichtag + 1 Tag, `verfall_am` = `pruefung_am` + 6 Monate, `gesagt_am` = `hinterlegt_am` = heute.
- id-Muster `^[a-z0-9][a-z0-9-]*$`, Form `<kurz>-<jahr>-<mmdd><hhmm>`, `kurz` ≤ 20 Zeichen.
- Freitextgrenzen: `zitat` ≤ 600 Zeichen, `bedingung` ≤ 300, `institution`/`gesagtVon` ≤ 120. `PR_URL_MAX` vorläufig 8000, wird in Task 6 gemessen.
- `python -m pytest -q` (128 Tests) und `node site/pruefung.mjs` bleiben grün.
- Deutsch in Code, Kommentaren, Texten. Commit-Präfixe wie bisher (`feat:`, `site:`, `test:`, `docs:`).

## Dateien

| Datei | Verantwortung |
|---|---|
| `site/daten/buecher.json` | Kopie der Buchliste von festgehalten, plus `stand` |
| `site/hinterlegen.mjs` | reines Modul: `idBilden`, `uebersetzen`, `prUrl`, `urlZuLang`, `mailUrl`, `PR_URL_MAX` |
| `site/hinterlegen.pruefung.mjs` | Node-Tests des Moduls; exportiert `pruefen() -> anzahlFehler`; mit `--beispiel` gibt es die Beispieldatei aus |
| `site/pruefung.mjs` | ruft zusätzlich `hinterlegen.pruefung.mjs` auf |
| `site/hinterlegen.html` | Seite: sieben Schritte, Vorschau, drei Knöpfe, Entwurf, Status |
| `site/hinterlegen-seite.js` | DOM-Logik, Entwurf, Statusabfrage |
| `site/index.html` | Link „Selbst hinterlegen" |
| `tests/test_hinterlegen_rundlauf.py` | Rundlauf: Node-Beispiel → Generator-`pruefen` → 0 Fehler |
| `pyproject.toml` | Test-Abhängigkeit `festgehalten` gepinnt |

---

### Task 1: Buchliste kopieren, Modul mit `idBilden`

**Files:**
- Create: `site/daten/buecher.json`, `site/hinterlegen.mjs`, `site/hinterlegen.pruefung.mjs`
- Modify: `site/pruefung.mjs` (Ende)

**Interfaces:**
- Produces: `idBilden(institution: string, ordner: string|null, jetzt: Date) -> string`; `kurzBilden(text: string) -> string`; `isoDatum(d: Date) -> "YYYY-MM-DD"`; `pruefen()` in `hinterlegen.pruefung.mjs` gibt Fehlerzahl zurück.

- [ ] **Step 1: Buchliste kopieren**

Run: `curl -s https://felix3c.github.io/festgehalten/buecher.json -o site/daten/buecher.json`
Dann die Datei zu einem Objekt machen: `{ "stand": "2026-09-05", "buecher": [ …die Liste… ] }` (Datum = heute). Prüfen: genau ein Eintrag mit `"sammelbuch": true`, Ordner `hinterlegt`.

- [ ] **Step 2: Testdatei mit ersten Tests schreiben**

```js
// site/hinterlegen.pruefung.mjs — node site/hinterlegen.pruefung.mjs
import { idBilden, kurzBilden } from "./hinterlegen.mjs";

const faelle = [];
export function fall(name, fn) { faelle.push([name, fn]); }
function gleich(ist, soll, was) { if (ist !== soll) throw new Error(`${was}: ist ${JSON.stringify(ist)}, soll ${JSON.stringify(soll)}`); }

const JETZT = new Date(2026, 8, 5, 14, 32); // 05.09.2026 14:32 lokal

fall("kurz: Umlaute, Leerzeichen, Länge", () => {
  gleich(kurzBilden("Stadt Köln"), "stadt-koeln", "koeln");
  gleich(kurzBilden("Bürgerverein Straße e.V."), "buergerverein-strasse", "strasse");
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
```

- [ ] **Step 3: Test laufen lassen, Fehlschlag sehen**

Run: `node site/hinterlegen.pruefung.mjs`
Expected: Fehler „Cannot find module './hinterlegen.mjs'".

- [ ] **Step 4: Modul anlegen**

```js
// site/hinterlegen.mjs — reines Modul, kein DOM. Eingaben -> Datei im festgehalten-Format v1.
// Spec: docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md §3, §4, §6.

const UMLAUTE = { ä: "ae", ö: "oe", ü: "ue", ß: "ss" };

export function kurzBilden(text) {
  const k = String(text).toLowerCase()
    .replace(/[äöüß]/g, (c) => UMLAUTE[c])
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return k.slice(0, 20).replace(/-+$/g, "");
}

const zwei = (n) => String(n).padStart(2, "0");
export const isoDatum = (d) => `${d.getFullYear()}-${zwei(d.getMonth() + 1)}-${zwei(d.getDate())}`;

export function idBilden(institution, ordner, jetzt) {
  const kurz = ordner || kurzBilden(institution) || "hinterlegt";
  return `${kurz}-${jetzt.getFullYear()}-${zwei(jetzt.getMonth() + 1)}${zwei(jetzt.getDate())}${zwei(jetzt.getHours())}${zwei(jetzt.getMinutes())}`;
}
```

- [ ] **Step 5: Tests laufen lassen**

Run: `node site/hinterlegen.pruefung.mjs`
Expected: `ok: 3 Fälle hinterlegen`.

- [ ] **Step 6: In `pruefung.mjs` einhängen**

In `site/pruefung.mjs` oben `import { pruefen as hinterlegenPruefen } from "./hinterlegen.pruefung.mjs";` und vor der letzten `console.log`-Zeile: `fehler += hinterlegenPruefen();`.

Run: `node site/pruefung.mjs` → endet mit `ok: …`.

- [ ] **Step 7: Commit**

```bash
git add site/daten/buecher.json site/hinterlegen.mjs site/hinterlegen.pruefung.mjs site/pruefung.mjs
git commit -m "feat: Buchliste und id-Bildung für den Hinterlegungs-Pfad"
```

---

### Task 2: `uebersetzen` — Eingaben prüfen und Datei erzeugen

**Files:**
- Modify: `site/hinterlegen.mjs`, `site/hinterlegen.pruefung.mjs`

**Interfaces:**
- Consumes: `idBilden`, `isoDatum`, Buchliste `{ stand, buecher: [{ordner, titel, institution, halter, kontakt, einreichung, repo, zweig, pfad, sammelbuch}] }`
- Produces: `uebersetzen(eingaben, buecher, jetzt) -> { datei, id, zielbuch, fehler }`. `eingaben` = `{ institution, gesagtVon, zitat, stichtag (YYYY-MM-DD), typ ("ja_nein"|"punkt"), einheit, wert, toleranz, nachweisUrl, bedingung, bedingungFrist (YYYY-MM-DD), quelleUrl }`, alle Werte Strings. `fehler` = `{ feldname: "Text in Worten" }`, leer bei Erfolg. `zielbuch` = Eintrag der Buchliste.
- Produces: `pruefeEingaben(e, jetzt) -> fehler`, `datumPlus(iso, {tage, monate}) -> iso`, `yamlText(s) -> string` (in doppelten Anführungszeichen, `\` und `"` escaped), `GRENZEN`.

- [ ] **Step 1: Tests schreiben**

```js
// site/hinterlegen.pruefung.mjs, ergänzen (Import erweitern):
import { idBilden, kurzBilden, uebersetzen, datumPlus } from "./hinterlegen.mjs";

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
```

- [ ] **Step 2: Laufen lassen, Fehlschlag sehen**

Run: `node site/hinterlegen.pruefung.mjs` → Importfehler `uebersetzen`.

- [ ] **Step 3: Implementieren**

```js
// site/hinterlegen.mjs, ergänzen
export const GRENZEN = { institution: 120, gesagtVon: 120, zitat: 600, bedingung: 300 };
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
```

- [ ] **Step 4: Tests laufen lassen**

Run: `node site/hinterlegen.pruefung.mjs` → `ok: 8 Fälle hinterlegen`. Bei Abweichung im `datei.includes`-Test die Erwartung gegen die Spec prüfen, nicht den Test lockern.

- [ ] **Step 5: Commit**

```bash
git add site/hinterlegen.mjs site/hinterlegen.pruefung.mjs
git commit -m "feat: uebersetzen — Eingaben prüfen und Eintragsdatei im festgehalten-Format erzeugen"
```

---

### Task 3: PR-URL, Längengrenze, Mail-Link

**Files:**
- Modify: `site/hinterlegen.mjs`, `site/hinterlegen.pruefung.mjs`

**Interfaces:**
- Produces: `PR_URL_MAX` (Zahl, vorläufig 8000), `FESTGEHALTEN_SEITE`, `prUrl(zielbuch, id, datei) -> string`, `urlZuLang(url) -> boolean`, `mailUrl(zielbuch, id) -> string|null`, `statusUrl(zielbuch) -> string`, `prListeUrl(zielbuch) -> string`.

- [ ] **Step 1: Tests schreiben**

```js
// site/hinterlegen.pruefung.mjs, Import erweitern um prUrl, urlZuLang, mailUrl, statusUrl, prListeUrl, PR_URL_MAX
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
```

- [ ] **Step 2: Laufen lassen** → Importfehler.

- [ ] **Step 3: Implementieren**

```js
// site/hinterlegen.mjs, ergänzen
export const PR_URL_MAX = 8000; // ungemessen; Messung gegen GitHub in Plan-Task 6, dann Datum hier eintragen
export const FESTGEHALTEN_SEITE = "https://felix3c.github.io/festgehalten";

export const prUrl = (b, id, datei) =>
  `https://github.com/${b.repo}/new/${b.zweig}/${b.pfad}?filename=${encodeURIComponent(id + ".md")}&value=${encodeURIComponent(datei)}`;
export const urlZuLang = (url) => url.length > PR_URL_MAX;
export const mailUrl = (b, id) => b.einreichung
  ? `mailto:${b.einreichung}?subject=${encodeURIComponent("Hinterlegung " + id)}&body=${encodeURIComponent(`Bitte die heruntergeladene Datei ${id}.md anhängen. Zielbuch: ${b.titel}.`)}`
  : null;
export const statusUrl = (b) => `${FESTGEHALTEN_SEITE}/${b.ordner}/wettbuch.json`;
export const prListeUrl = (b) => `https://github.com/${b.repo}/pulls`;
```

- [ ] **Step 4: Tests laufen lassen** → `ok: 12 Fälle hinterlegen`; `node site/pruefung.mjs` grün.

- [ ] **Step 5: Commit**

```bash
git add site/hinterlegen.mjs site/hinterlegen.pruefung.mjs
git commit -m "feat: PR-, Mail- und Status-Adressen für die Übergabe"
```

---

### Task 4: Rundlauf gegen den echten Generator

**Files:**
- Modify: `pyproject.toml` (`dev`-Extra), `site/hinterlegen.pruefung.mjs` (`--beispiel`)
- Create: `tests/test_hinterlegen_rundlauf.py`

**Interfaces:**
- Consumes: `lesen.buch_lesen(ordner: Path) -> {"meta", "wetten", "ordner"}` und `pruefen.buch_pruefen(buch) -> list[Fehler]` aus dem Paket `wettbuch` (festgehalten); `EINGABE_OK`, `BUECHER`, `JETZT` aus der Node-Testdatei.
- Produces: `node site/hinterlegen.pruefung.mjs --beispiel` schreibt die Beispieldatei nach stdout.

- [ ] **Step 1: Abhängigkeit pinnen**

In `pyproject.toml`: `dev = ["pytest>=8.0", "festgehalten @ git+https://github.com/Felix3c/festgehalten@FESTGEHALTEN_SHA"]` (SHA aus der Voraussetzung oben einsetzen). Dann `python -m pip install -e ".[dev]"`.

- [ ] **Step 2: Test schreiben**

```python
# tests/test_hinterlegen_rundlauf.py
"""Die von site/hinterlegen.mjs erzeugte Datei muss der Generator von festgehalten
ohne Fehler lesen und prüfen (Spec Teil 3 §7.2)."""
import shutil
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("wettbuch")
from wettbuch import lesen, pruefen  # noqa: E402

WURZEL = Path(__file__).resolve().parents[1]
BUCH_MD = """---
titel: Hinterlegt
halter: Testhalter
kontakt: https://example.org
seit: 2026-09-05
lizenz: CC0
format: v1
sammelbuch: true
---
Test.
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")
def test_beispieldatei_besteht_generatorpruefung(tmp_path: Path):
    r = subprocess.run(["node", str(WURZEL / "site" / "hinterlegen.pruefung.mjs"), "--beispiel"],
                       capture_output=True, text=True, encoding="utf-8", check=True)
    datei = r.stdout
    assert datei.startswith("---\nid: ")
    ident = datei.splitlines()[1].split(": ", 1)[1]

    (tmp_path / "BUCH.md").write_text(BUCH_MD, encoding="utf-8")
    (tmp_path / "wetten").mkdir()
    (tmp_path / "wetten" / f"{ident}.md").write_text(datei, encoding="utf-8")

    buch = lesen.buch_lesen(tmp_path)
    fehler = pruefen.buch_pruefen(buch)

    assert fehler == [], [f"{f.datei}: {f.feld} — {f.text}" for f in fehler]
    w = buch["wetten"][0]
    assert w["herkunft"] == "hinterlegt"
    assert w["prognosen"][0]["wert"] == 1.0
```

- [ ] **Step 3: `--beispiel` in der Node-Testdatei**

Am Ende von `site/hinterlegen.pruefung.mjs`, vor dem `if (process.argv[1] …)`-Block:

```js
if (process.argv.includes("--beispiel")) {
  process.stdout.write(uebersetzen(EINGABE_OK, BUECHER, JETZT).datei);
  process.exit(0);
}
```

- [ ] **Step 4: Test laufen lassen**

Run: `python -m pytest -q tests/test_hinterlegen_rundlauf.py -v`
Expected: PASS. Bei Fehlern des Generators (z. B. `toleranz`, `frage`, Datumsformat) das Modul anpassen, nicht den Test.

- [ ] **Step 5: Gesamtlauf und Commit**

Run: `python -m pytest -q` → 129 grün. `node site/pruefung.mjs` → grün.

```bash
git add pyproject.toml tests/test_hinterlegen_rundlauf.py site/hinterlegen.pruefung.mjs
git commit -m "test: Rundlauf — erzeugte Datei besteht die Prüfung des festgehalten-Generators"
```

---

### Task 5: Seite, Entwurf, Status, Link

**Files:**
- Create: `site/hinterlegen.html`, `site/hinterlegen-seite.js`
- Modify: `site/index.html` (Header)

**Interfaces:**
- Consumes: alles aus `hinterlegen.mjs`; `site/daten/buecher.json`; Klassen aus `stil.css` (`fieldset`, `.hinweis`, `.optionen`, `.stand`, `button`).
- Produces: Seite mit sieben Schritten, Vorschau, drei Knöpfen, Entwurf, Status. `localStorage`-Schlüssel `doorway.hinterlegen.entwurf` = `{ gespeichert: "YYYY-MM-DD", eingaben: {…} }`.

- [ ] **Step 1: `hinterlegen.html`**

```html
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Doorway — selbst hinterlegen</title>
<link rel="stylesheet" href="stil.css">
</head>
<body>
<header>
  <h1>Doorway</h1>
  <p class="claim">Halte vorab fest, was du erwartest. Datiert, öffentlich, nachprüfbar.</p>
  <p class="stand"><a href="index.html">Zurück zum Spiegel</a></p>
</header>
<main>
  <section id="formular" aria-labelledby="formular-titel">
    <h2 id="formular-titel">Was erwartest du?</h2>
    <p class="hinweis" id="datenschutz">Nichts, was du hier eingibst, verlässt deinen Browser. Ein Entwurf bleibt nur auf diesem Gerät gespeichert; auf einem geteilten Rechner können andere ihn sehen.</p>
    <p class="hinweis" id="entwurf-hinweis" hidden></p>
    <form id="f" novalidate>
      <fieldset><legend>1. Wer erwartet das?</legend>
        <label>Institution, Verein oder Person <input id="f-institution" list="buecher-liste" maxlength="120" autocomplete="organization"></label>
        <datalist id="buecher-liste"></datalist>
        <label>Wer spricht dafür (Person oder Organ) <input id="f-gesagtVon" maxlength="120"></label>
        <p class="hinweis" id="zielbuch-text"></p>
      </fieldset>
      <fieldset><legend>2. Was wird erwartet?</legend>
        <label>In eigenen Worten, ein bis drei Sätze <textarea id="f-zitat" maxlength="600" rows="3"></textarea></label>
      </fieldset>
      <fieldset><legend>3. Bis wann?</legend>
        <label>Stichtag <input id="f-stichtag" type="date"></label>
        <p class="hinweis">Der Stichtag gilt wörtlich. Teilerfüllung ist Nein. Geprüft wird ab dem Tag danach; ohne Beleg verfällt der Eintrag sechs Monate später.</p>
      </fieldset>
      <fieldset><legend>4. Woran erkennt man es?</legend>
        <div class="optionen" id="f-typ"></div>
        <div id="punkt-felder" hidden>
          <label>Zahl <input id="f-wert" inputmode="decimal"></label>
          <label>Einheit <input id="f-einheit" placeholder="z. B. Plätze, Mio EUR"></label>
          <label>Toleranz (freiwillig, z. B. 0.10 für ±10 %) <input id="f-toleranz" inputmode="decimal"></label>
        </div>
      </fieldset>
      <fieldset><legend>5. Wo wird das Ergebnis öffentlich sichtbar sein?</legend>
        <label>Adresse <input id="f-nachweisUrl" type="url" placeholder="https://…"></label>
        <p class="hinweis">Ohne diesen Ort gibt es keinen Beleg. Ist dort am Prüftag nichts, gilt das als Nein.</p>
      </fieldset>
      <fieldset><legend>6. Hängt es von etwas ab? <span class="optional">(freiwillig)</span></legend>
        <label>Bedingung <input id="f-bedingung" maxlength="300" placeholder="z. B. Bewilligung des Förderantrags"></label>
        <label>Steht fest bis <input id="f-bedingungFrist" type="date"></label>
      </fieldset>
      <fieldset><legend>7. Steht die Erwartung schon irgendwo öffentlich? <span class="optional">(freiwillig)</span></legend>
        <label>Adresse <input id="f-quelleUrl" type="url" placeholder="https://…"></label>
        <p class="hinweis">Wenn nicht, wird die Datei im Buch selbst zur Quelle.</p>
      </fieldset>
      <p><button type="button" id="k-entwurf-loeschen">Entwurf löschen</button></p>
    </form>
  </section>
  <section id="vorschau" aria-live="polite" hidden>
    <h2>So wird der Eintrag im Buch stehen</h2>
    <p class="hinweis">Das hier wird nach Aufnahme nicht mehr geändert. Prüfen Sie Stichtag und Ort des Nachweises.</p>
    <pre id="datei"></pre>
    <p class="optionen">
      <a id="k-pr" class="button" target="_blank" rel="noopener">Als Pull Request anlegen</a>
      <a id="k-download" class="button">Herunterladen</a>
      <a id="k-mail" class="button" hidden>Per Mail einreichen</a>
    </p>
    <p class="hinweis" id="pr-zu-lang" hidden>Der Eintrag ist zu lang für den direkten Pull-Request-Link. Bitte herunterladen und per Mail einreichen oder die Datei selbst im Buch anlegen.</p>
    <p class="hinweis" id="danach" hidden></p>
  </section>
  <section id="status" aria-labelledby="status-titel">
    <h2 id="status-titel">Ist mein Eintrag drin?</h2>
    <label>id <input id="s-id" placeholder="z. B. koeln-2026-09051432"></label>
    <button type="button" id="k-status">Nachsehen</button>
    <p id="status-text" aria-live="polite"></p>
  </section>
</main>
<footer>
  <h2>Was diese Seite nicht tut</h2>
  <p>Sie öffnet keinen Pull Request in deinem Namen, speichert nichts auf einem Server und führt kein Buch. Der Eintrag wird erst mit dem Merge im Buch wirksam; dieser Zeitpunkt zählt.</p>
  <p class="stand" id="buecher-stand"></p>
  <p class="stand">Code und jede Änderung: <a href="https://github.com/Felix3c/doorway">github.com/Felix3c/doorway</a></p>
</footer>
<script type="module" src="hinterlegen-seite.js"></script>
</body>
</html>
```

- [ ] **Step 2: `hinterlegen-seite.js`**

```js
// Doorway — Seite für den Hinterlegungs-Pfad. Hängt Felder an hinterlegen.mjs, hält den
// Entwurf lokal, fragt auf Klick den Status ab. Kein Server, nichts verlässt den Browser
// außer der Statusabfrage (Spec Teil 3 §6).
import { uebersetzen, prUrl, urlZuLang, mailUrl, statusUrl, prListeUrl, FESTGEHALTEN_SEITE } from "./hinterlegen.mjs";

const FELDER = ["institution", "gesagtVon", "zitat", "stichtag", "wert", "einheit", "toleranz", "nachweisUrl", "bedingung", "bedingungFrist", "quelleUrl"];
const SCHLUESSEL = "doorway.hinterlegen.entwurf";
const $ = (id) => document.getElementById(id);
let buecher = { stand: "?", buecher: [] };
let typ = "ja_nein";

function speicher() { try { return window.localStorage; } catch { return null; } }
function eingabenLesen() {
  const e = { typ };
  for (const f of FELDER) e[f] = $("f-" + f).value;
  return e;
}
function eingabenSetzen(e) {
  for (const f of FELDER) if (e[f] !== undefined) $("f-" + f).value = e[f];
  typ = e.typ === "punkt" ? "punkt" : "ja_nein";
  typKnoepfe();
}
function entwurfSpeichern() {
  const s = speicher(); if (!s) return;
  try { s.setItem(SCHLUESSEL, JSON.stringify({ gespeichert: new Date().toISOString().slice(0, 10), eingaben: eingabenLesen() })); } catch {}
}
function entwurfLaden() {
  const s = speicher();
  if (!s) { $("entwurf-hinweis").textContent = "Dein Browser erlaubt keinen lokalen Entwurf; die Eingaben gehen beim Schließen verloren."; $("entwurf-hinweis").hidden = false; return; }
  try {
    const roh = s.getItem(SCHLUESSEL); if (!roh) return;
    const { gespeichert, eingaben } = JSON.parse(roh);
    eingabenSetzen(eingaben);
    const [j, m, t] = gespeichert.split("-");
    $("entwurf-hinweis").textContent = `Entwurf vom ${t}.${m}.${j} wiederhergestellt.`; $("entwurf-hinweis").hidden = false;
  } catch {}
}
function entwurfLoeschen() {
  const s = speicher(); if (s) { try { s.removeItem(SCHLUESSEL); } catch {} }
  eingabenSetzen(Object.fromEntries(FELDER.map((f) => [f, ""])));
  $("entwurf-hinweis").hidden = true; aktualisieren();
}
function typKnoepfe() {
  const c = $("f-typ"); c.replaceChildren();
  for (const [wert, text] of [["ja_nein", "Ja oder Nein"], ["punkt", "eine Zahl"]]) {
    const b = document.createElement("button"); b.type = "button"; b.textContent = text;
    b.setAttribute("aria-pressed", String(typ === wert));
    b.addEventListener("click", () => { typ = wert; typKnoepfe(); aktualisieren(); });
    c.appendChild(b);
  }
  $("punkt-felder").hidden = typ !== "punkt";
}
function fehlerZeigen(fehler) {
  for (const f of [...FELDER, "typ"]) {
    const el = $("f-" + f); if (!el) continue;
    let p = el.parentElement.querySelector(".fehler");
    if (fehler[f]) { if (!p) { p = document.createElement("p"); p.className = "fehler hinweis"; el.parentElement.appendChild(p); } p.textContent = fehler[f]; }
    else if (p) p.remove();
  }
}
function aktualisieren() {
  entwurfSpeichern();
  const e = eingabenLesen();
  const r = uebersetzen(e, buecher, new Date());
  fehlerZeigen(r.fehler);
  $("zielbuch-text").textContent = r.zielbuch ? `Zielbuch: ${r.zielbuch.titel} (Halter: ${r.zielbuch.halter})` : "";
  const fertig = Object.keys(r.fehler).length === 0;
  $("vorschau").hidden = !fertig;
  if (!fertig) return;
  $("datei").textContent = r.datei;
  const url = prUrl(r.zielbuch, r.id, r.datei);
  const zuLang = urlZuLang(url);
  $("k-pr").href = zuLang ? "#" : url; $("k-pr").setAttribute("aria-disabled", String(zuLang)); $("pr-zu-lang").hidden = !zuLang;
  $("k-download").href = "data:text/markdown;charset=utf-8," + encodeURIComponent(r.datei); $("k-download").download = r.id + ".md";
  const m = mailUrl(r.zielbuch, r.id); $("k-mail").hidden = !m; if (m) $("k-mail").href = m;
  $("danach").hidden = false;
  $("danach").textContent = `Nach dem Anlegen: automatische Formprüfung, dann Prüfung durch ${r.zielbuch.halter} nach den vier Punkten der BUCH.md, Aufnahme durch Merge. Der Merge-Zeitpunkt zählt. Rückfragen: ${r.zielbuch.kontakt}. Deine id: ${r.id}`;
}
function linkText(ziel, href, text, vor, nach) {
  ziel.replaceChildren(); const a = document.createElement("a"); a.href = href; a.textContent = text; ziel.append(vor, a, nach);
}
async function statusNachsehen() {
  const id = $("s-id").value.trim(); const out = $("status-text");
  if (!id) { out.textContent = "Bitte eine id eingeben."; return; }
  const praefix = id.split("-")[0];
  const kandidaten = buecher.buecher.filter((b) => b.ordner === praefix);
  const liste = kandidaten.length ? kandidaten : buecher.buecher;
  out.textContent = "Sehe nach …";
  for (const b of liste) {
    try {
      const r = await fetch(statusUrl(b)); if (!r.ok) throw new Error(String(r.status));
      const daten = await r.json();
      const wetten = Array.isArray(daten) ? daten : (daten.wetten || []);
      if (wetten.some((x) => x.id === id)) { linkText(out, `${FESTGEHALTEN_SEITE}/${b.ordner}/${id}.html`, `aufgenommen in „${b.titel}"`, "Eintrag ", "."); return; }
    } catch { linkText(out, prListeUrl(b), "PR-Liste des Buches", "Abfrage fehlgeschlagen. Selbst nachsehen: ", "."); return; }
  }
  linkText(out, prListeUrl(liste[0]), "offene Pull Requests", "Noch nicht aufgenommen. Eingereicht? Siehe ", ".");
}
async function start() {
  try { buecher = await (await fetch("daten/buecher.json")).json(); } catch { $("buecher-stand").textContent = "Buchliste konnte nicht geladen werden."; return; }
  $("buecher-stand").textContent = `Buchliste vom ${buecher.stand}, Quelle: ${FESTGEHALTEN_SEITE}/buecher.json`;
  const dl = $("buecher-liste");
  for (const b of buecher.buecher) if (b.institution) { const o = document.createElement("option"); o.value = b.institution; dl.appendChild(o); }
  typKnoepfe(); entwurfLaden();
  for (const f of FELDER) $("f-" + f).addEventListener("input", aktualisieren);
  $("k-entwurf-loeschen").addEventListener("click", entwurfLoeschen);
  $("k-status").addEventListener("click", statusNachsehen);
  $("k-pr").addEventListener("click", (ev) => { if ($("k-pr").getAttribute("aria-disabled") === "true") ev.preventDefault(); });
  aktualisieren();
}
start();
```

Die Eintragsseite auf festgehalten heißt hier `<ordner>/<id>.html`; das tatsächliche Schema in `~/wettbuch/generator/wettbuch/seiten.py` (`seiten_schreiben`) nachsehen und den Link anpassen. Die Form von `wettbuch.json` (Liste oder Objekt mit `wetten`) ebenfalls dort prüfen; der Code oben verträgt beides. Falls `stil.css` keine Klasse `.button` für Links hat, in `stil.css` `a.button` wie `button` gestalten (einzige erlaubte CSS-Änderung).

- [ ] **Step 3: Link von der Startseite**

In `site/index.html` im `<header>` nach `<p id="stand" …>` eine Zeile `<p class="stand"><a href="hinterlegen.html">Selbst hinterlegen: Erwartung vorab festhalten</a></p>`.

- [ ] **Step 4: Lokal ansehen und durchklicken**

Run (PowerShell): `Start-Process python -ArgumentList "-m http.server 8765" -WorkingDirectory site` → http://127.0.0.1:8765/hinterlegen.html

Prüfen: (a) Fehlertexte erscheinen am Feld und verschwinden; (b) Vorschau erscheint erst, wenn alles gültig ist; (c) Tab schließen, neu öffnen: Entwurf zurück; „Entwurf löschen" leert; (d) Knopf 1 öffnet GitHub mit Pfad und Inhalt; (e) Download liefert `<id>.md`; (f) Status mit einer existierenden id aus Köln zeigt „aufgenommen", mit Fantasie-id „noch nicht aufgenommen".

- [ ] **Step 5: Tests und Commit**

Run: `node site/pruefung.mjs` und `python -m pytest -q` → grün.

```bash
git add site/hinterlegen.html site/hinterlegen-seite.js site/index.html site/stil.css
git commit -m "site: Seite hinterlegen.html — Formular, Vorschau, Übergabe, Entwurf, Status"
```

---

### Task 6: `PR_URL_MAX` messen

**Files:**
- Modify: `site/hinterlegen.mjs` (Konstante und Kommentar), ggf. `site/hinterlegen.html` (`maxlength`)

- [ ] **Step 1: Messen**

Im Browser (bei GitHub angemeldet) die PR-URL für eine Beispieldatei mit `zitat` = 600 Zeichen Umlaut-Text und `bedingung` = 300 Zeichen öffnen. Länge der URL vorher in der Konsole messen (`prUrl(...).length`). Funktioniert die Vorbefüllung: Grenze ≥ diese Länge. Dann den Kontext-Absatz in der Konsole künstlich in 2000er-Schritten verlängern, bis GitHub den Inhalt abschneidet oder eine Fehlerseite zeigt. `PR_URL_MAX` = letzte funktionierende Länge minus 500 (Sicherheitsrand). Kommentar: `// gemessen am <Datum> gegen github.com: bis <n> Zeichen vorbefüllt`.

- [ ] **Step 2: Freitextgrenzen prüfen**

Ist die Beispieldatei mit maximalen Freitexten länger als `PR_URL_MAX`, `GRENZEN.zitat` und `GRENZEN.bedingung` so senken, dass sie darunter bleibt; `maxlength` in `hinterlegen.html` angleichen; Test „zitat zu lang" auf die neue Grenze anpassen.

- [ ] **Step 3: Tests und Commit**

Run: `node site/pruefung.mjs` → grün.

```bash
git add site/hinterlegen.mjs site/hinterlegen.html site/hinterlegen.pruefung.mjs
git commit -m "site: PR_URL_MAX gegen GitHub gemessen"
```

---

### Task 7: Abnahme und Statusdateien

- [ ] **Step 1: Pushen, Pages abwarten**

`git push`; https://felix3c.github.io/doorway/hinterlegen.html öffnen.

- [ ] **Step 2: Probelauf durch Felix**

Erfundener Fall (Institution „Probelauf e.V."), bis zum PR im Sammelbuch. PR-Titel mit „Probelauf" beginnen. Erwartet: Check „Pull Request prüfen" grün. PR schließen, nicht mergen.

- [ ] **Step 3: Status per id prüfen**

Die id des Probelaufs auf der Seite eingeben → „Noch nicht aufgenommen" mit Link. Eine echte Köln-id → „aufgenommen".

- [ ] **Step 4: Statusdateien**

`NAECHSTE-SCHRITTE.md`: Stand, Teil 3 fertig, Befunde erledigt, offen: `einreichung`-Mail, erster echter hinterlegter Eintrag (nicht Felix' eigener). `~/REIHENFOLGE.txt` Doorway-Block angleichen. Commit `docs: Teil 3 abgenommen`, push.

---

## Selbstprüfung gegen die Spec

- §2 Ablauf: Task 5 (Seite lädt nur `daten/buecher.json`, gleiche Origin).
- §3 sieben Schritte, feste Werte, id, Textteile: Task 2 (Modul), Task 5 (Felder).
- §4 drei Knöpfe, zu lange Datei, Text danach, kein eigener PR: Tasks 3, 5, 6.
- §6.1 reines Modul, `index.html`-Link: Tasks 1–3, 5. Abweichung: Tests liegen in `hinterlegen.pruefung.mjs` und werden von `pruefung.mjs` aufgerufen (Spec sagt „erweitert"), damit `pruefung.mjs` klein bleibt.
- §6.2 Prüfregeln: Task 2 (`pruefeEingaben`).
- §6.3 Entwurf mit Datum, Löschen, Warnung, fehlender Speicher: Task 5.
- §6.4 Status per statischer `wettbuch.json`, Fehlerfall: Task 5.
- §7 Tests: Modul (Tasks 1–3), Rundlauf gepinnt (Task 4), Abnahme (Task 7).
- §8 Reihenfolge eingehalten; festgehalten-Plan ist Voraussetzung.
- Typen geprüft: `uebersetzen`, `prUrl`, `mailUrl`, `statusUrl`, `prListeUrl`, `FESTGEHALTEN_SEITE`, `EINGABE_OK`, `BUECHER`, `JETZT` heißen in allen Tasks gleich.
