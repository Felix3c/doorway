// Doorway — die Seite. Zeigt an, was Python in daten/panel.json entschieden
// hat. Rechnet keine Quote nach; wertet nur die exportierten Regeln aus.
import { kompilieren, pruefen, selbstpruefung } from "./regeln.mjs";

const TYPEN = [
  ["Verein", "ein eingetragener Verein"],
  ["Initiative", "eine Gruppe ohne Verein", "Initiative, Nachbarschaft, Freundeskreis"],
  ["Stiftung", "eine Stiftung"],
  ["Kirche", "eine Kirchengemeinde"],
  ["Kommune", "eine Stadt, Gemeinde oder ein Kreis"],
  ["Privatperson", "ich selbst, als Privatperson"],
  ["Firma", "ein Unternehmen"],
];
const BETRAEGE = [
  ["bis_2000", "bis 2.000 €"],
  ["bis_5000", "bis 5.000 €"],
  ["bis_50000", "bis 50.000 €"],
  ["mehr", "mehr als 50.000 €"],
];
const ELEMENTE = ["Heimat-Scheck", "Heimat-Preis", "Heimat-Fonds", "Heimat-Werkstatt", "Heimat-Zeugnis"];

const wahl = { typ: null, betrag: null, element: null, mehrfach: null, vorhaben: "" };
let daten = null;
let regeln = [];
let regelnVerfuegbar = false;

const $ = (id) => document.getElementById(id);
const prozent = (x) => `${Math.round(x * 100)} %`;
const euro = (n) => (n == null ? "–" : n.toLocaleString("de-DE") + " €");

function optionen(container, liste, feld, nachWahl) {
  container.replaceChildren();
  for (const [wert, text, klein] of liste) {
    const b = document.createElement("button");
    b.type = "button";
    b.dataset.wert = wert;
    b.setAttribute("aria-pressed", String(wahl[feld] === wert));
    b.textContent = text;
    if (klein) {
      const s = document.createElement("small");
      s.textContent = klein;
      b.append(s);
    }
    b.addEventListener("click", () => {
      wahl[feld] = wert;
      for (const x of container.querySelectorAll("button")) x.setAttribute("aria-pressed", String(x === b));
      if (nachWahl) nachWahl();
      rendern();
    });
    container.append(b);
  }
}

function elementOptionen() {
  const liste = ELEMENTE.map((el) => {
    const e = daten.elemente[el];
    const typen = e.typen.map(([t, n]) => `${t} (${n})`).join(", ");
    const klein = e.bewilligt_mit_betrag
      ? `in den Berichten ${e.bewilligt_mit_betrag} bewilligte Anträge, meist ${euro(e.median_betrag)}; ${typen}`
      : "in den Berichten ohne Beträge";
    return [el, el, klein];
  });
  optionen($("f-element"), liste, "element");
}

function vorschlagen() {
  if (!wahl.typ || !wahl.betrag) return;
  const v = daten.vorschlag[wahl.betrag][wahl.typ];
  wahl.element = v;
  for (const x of $("f-element").querySelectorAll("button")) x.setAttribute("aria-pressed", String(x.dataset.wert === v));
  const e = daten.elemente[v];
  $("vorschlag-text").textContent = `Vorschlag: ${v} — in den Berichten ${e.bewilligt_mit_betrag} bewilligte Anträge, meist ${euro(e.median_betrag)}. Du kannst ein anderes Element wählen.`;
}

function zeile(tag, klasse, text) {
  const el = document.createElement(tag);
  if (klasse) el.className = klasse;
  if (text !== undefined) el.textContent = text;
  return el;
}

function panel() {
  const ziel = $("panel");
  if (!wahl.element) {
    ziel.replaceChildren();
    return;
  }
  const s = daten.schaetzungen[wahl.element];
  const getroffen = regelnVerfuegbar ? pruefen(regeln, wahl.vorhaben, wahl.typ, wahl.mehrfach === "ja") : [];
  const chancenlos = getroffen.length > 0;

  const karte = zeile("div", "karte");
  karte.append(zeile("div", "kopf", chancenlos ? "Chancenlos" : s.darstellung === "keine" ? "Noch keine Zahl" : "Aussichtsreich"));

  const urteil = zeile("p", "urteil");
  const basis = zeile("p", "basis");
  const jahre = s.jahre.length ? `${s.jahre[0]}–${s.jahre[s.jahre.length - 1]}` : "";
  if (chancenlos) {
    urteil.classList.add("schlecht");
    urteil.textContent = "Chance nahe null";
    basis.textContent = `${getroffen[0].name} — ${getroffen[0].hinweis}`;
  } else if (s.darstellung === "keine") {
    urteil.classList.add("offen");
    urteil.textContent = "Eine Zahl gibt es erst ab drei belegten Förderjahren.";
    basis.textContent = `Bisher belegt: ${s.belegte_jahre}.`;
  } else if (s.darstellung === "spanne") {
    urteil.classList.add("offen");
    urteil.textContent = `Chance irgendwo zwischen ${prozent(1 - s.obergrenze)} und ${prozent(1 - s.untergrenze)}`;
    basis.textContent = `Die Quote dieses Elements schwankt stark von Jahr zu Jahr. Basis: ${s.grundlage_n} Anträge, Förderjahre ${jahre}.`;
  } else {
    urteil.classList.add("gut");
    urteil.textContent = `Chance rund ${prozent(1 - s.quote)} (± ${Math.round(s.halbe_breite * 100)})`;
    basis.textContent = `Basis: ${s.grundlage_n} Anträge, Förderjahre ${jahre}.`;
  }
  karte.append(urteil, basis);

  if (regelnVerfuegbar) {
    karte.append(zeile("h3", "", `Ausschlussprüfung — ${regeln.length - getroffen.length} von ${regeln.length} bestanden`));
    const ul = zeile("ul");
    for (const r of regeln) {
      const traf = getroffen.includes(r);
      const li = zeile("li", traf ? "getroffen" : "");
      li.append(zeile("span", "haken", traf ? "✕" : "✓"), document.createTextNode(r.name));
      ul.append(li);
    }
    karte.append(ul);
  } else {
    karte.append(zeile("h3", "", "Ausschlussprüfung"), zeile("p", "fehler", "Regelprüfung nicht verfügbar — Regeln und Seite passen nicht zusammen."));
  }

  const gruende = Object.entries(s.gruende || {});
  if (gruende.length) {
    const gesamt = gruende.reduce((a, [, n]) => a + n, 0);
    karte.append(zeile("h3", "", "Woran es hier scheitert"));
    const ul = zeile("ul", "gruende");
    for (const [grund, n] of gruende.slice(0, 5)) {
      const dein = chancenlos && grund.toLowerCase().includes(getroffen[0].name.toLowerCase().slice(0, 12));
      const li = zeile("li", dein ? "dein-fall" : "");
      li.append(zeile("span", "", grund + (dein ? " ← dein Fall" : "")), zeile("span", "", prozent(n / gesamt)));
      ul.append(li);
    }
    karte.append(ul);
  }

  const beleg = zeile("p", "beleg", "Beleg: ");
  const [quelleId, seite] = s.beleg.split(", ");
  const q = daten.quellen[quelleId];
  if (q) {
    const a = zeile("a", "", q.dokument);
    a.href = q.url;
    beleg.append(a, document.createTextNode(`, ${seite || ""} (${q.datum})`));
  } else {
    beleg.append(document.createTextNode(s.beleg));
  }
  karte.append(beleg);
  ziel.replaceChildren(karte);
}

function registerTabelle() {
  const fe = $("filter-element").value;
  const fj = $("filter-jahr").value;
  const tbody = $("register-tabelle").querySelector("tbody");
  tbody.replaceChildren();
  for (const z of daten.register) {
    if (fe && z.foerderelement !== fe) continue;
    if (fj && String(z.foerderjahr) !== fj) continue;
    const tr = zeile("tr", z.herkunft === "konflikt" ? "konflikt" : "");
    const q = daten.quellen[z.quelle_id];
    const zahl = (f) => (z.konflikt ? `${z.konflikt.gemessen[f]} / ${z.konflikt.gezaehlt[f]}` : z[f] ?? "–");
    const quote = z.antraege ? prozent((z.abgelehnt || 0) / z.antraege) : "–";
    tr.append(
      zeile("td", "", String(z.foerderjahr)),
      zeile("td", "", z.foerderelement ?? "alle"),
      zeile("td", "", z.bewilligungsstelle ?? "landesweit"),
      zeile("td", "zahl", String(zahl("antraege"))),
      zeile("td", "zahl", String(zahl("bewilligt"))),
      zeile("td", "zahl", String(zahl("abgelehnt"))),
      zeile("td", "zahl", quote),
    );
    const herkunft = zeile("td", "", z.herkunft);
    const gruende = Object.entries(z.ablehnungsgruende || {}).slice(0, 3);
    if (gruende.length) {
      const d = zeile("details");
      d.append(zeile("summary", "", "Gründe"), document.createTextNode(gruende.map(([g, n]) => `${g} (${n})`).join("; ")));
      herkunft.append(d);
    }
    const quelle = zeile("td");
    if (q) {
      const a = zeile("a", "", q.dokument);
      a.href = q.url;
      quelle.append(a, document.createTextNode(`, S. ${z.quelle_seite}`));
    } else {
      quelle.textContent = z.quelle_id;
    }
    tr.append(herkunft, quelle);
    tbody.append(tr);
  }
}

function rendern() {
  $("fs-mehrfach").hidden = wahl.element !== "Heimat-Scheck";
  panel();
}

async function start() {
  try {
    const antwort = await fetch("daten/panel.json", { cache: "no-store" });
    if (!antwort.ok) throw new Error(`HTTP ${antwort.status}`);
    daten = await antwort.json();
  } catch (e) {
    $("stand").textContent = `Die Daten konnten nicht geladen werden (${e.message}). Ohne Daten zeigt diese Seite nichts.`;
    return;
  }
  regeln = kompilieren(daten.regeln);
  const abweichungen = selbstpruefung(regeln, daten.beispiele);
  regelnVerfuegbar = abweichungen.length === 0;
  if (!regelnVerfuegbar) console.error("Selbstpruefung fehlgeschlagen", abweichungen);

  const st = daten.stand;
  const lock = Object.keys(st.quellen_lock || {}).length;
  $("stand").textContent = `Stand ${st.datum} · Korpus ${st.korpus_commit} · ${lock} Quelldokumente per Prüfsumme eingefroren`;
  $("stand-lang").textContent = `Jede Zahl auf dieser Seite stammt aus daten/panel.json, erzeugt am ${st.datum} aus dem Korpus im Commit ${st.korpus_commit}. Was dort nicht steht, steht auch hier nicht.`;

  optionen($("f-typ"), TYPEN, "typ", vorschlagen);
  optionen($("f-betrag"), BETRAEGE, "betrag", vorschlagen);
  elementOptionen();
  optionen($("f-mehrfach"), [["nein", "nein"], ["ja", "ja, schon einen"]], "mehrfach");
  $("f-vorhaben").addEventListener("input", (ev) => {
    wahl.vorhaben = ev.target.value;
    rendern();
  });

  const jahre = [...new Set(daten.register.map((z) => z.foerderjahr))].sort();
  for (const el of ELEMENTE) $("filter-element").append(new Option(el, el));
  for (const j of jahre) $("filter-jahr").append(new Option(String(j), String(j)));
  $("filter-element").addEventListener("change", registerTabelle);
  $("filter-jahr").addEventListener("change", registerTabelle);
  registerTabelle();

  const ul = $("quellen");
  for (const q of Object.values(daten.quellen)) {
    const li = zeile("li");
    const a = zeile("a", "", q.dokument);
    a.href = q.url;
    li.append(a, document.createTextNode(` (${q.datum}) — ${q.beschreibung}`));
    ul.append(li);
  }
}

start();
