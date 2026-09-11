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
      if (wetten.some((x) => x.id === id)) { linkText(out, `${FESTGEHALTEN_SEITE}/${b.ordner}/wette/${id}.html`, `aufgenommen in „${b.titel}"`, "Eintrag ", "."); return; }
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
