# Doorway — Nächste Schritte

**Stand:** 2026-08-27 (Teil 2 gebaut: `doorway export` + statische Seite in `site/`, im Browser geprüft; Kill-Kriterium weiterhin bestanden)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel mit Leitsatz seit 25.08.)
**Plan Teil 1:** `docs/superpowers/plans/2026-08-25-doorway-ernte-und-urteil.md` — alle 13 Tasks erledigt
**Phase:** Teil 2 gebaut und lokal geprüft. Es fehlt nur noch die Veröffentlichung (privates Repo, GitHub Pages) und Felix' Blick auf die Seite.
**Design Teil 2:** `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`

---

## Leitsatz (25.08.2026)

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Doorway ist nicht "Förderung finden", sondern "Ablehnung nachprüfbar machen". Übergeordnete These: `~/THESE.md`. Prüffrage für jedes Feature: *nachprüfbarer oder nur bequemer?*

## Wo wir stehen

**Gebaut (Git `master`, 108 Tests grün, Arbeitsbaum sauber, kein Remote):**

- `doorway laden` — sechs Landtagsdokumente, SHA-256-Lock; Prüfsummen identisch mit den Kopien vom 24.08.
- `doorway ernten` — Korpus 4.605 Entscheidungen (1.296 aus 2025, 3.309 aus 2018/2019), Register 78 Zeilen, 0 Konflikte, jede Zeile mit Herkunft
- `doorway prognose "<Vorhaben>"` — zweistufig gerechnet, einstufig angezeigt (§12.4)
- `doorway kill-kriterium` — beide Hürden aus §14.2, Rückgabewert 0/1
- Selbstwiderspruchstest (§14.1) läuft: Vorl 18/5027 sagt 598/329 im Text, zählt 596/330 in der Anlage

**Das Urteil (dreimal gemessen, das letzte gilt):**

```
Huerde 1  falsche Absagen   vereinseigene Ausstattung 0/22 = 0.0%   bestanden
Huerde 2  Kalibrierung      5 von 15 Vorhersagen ausserhalb          GERISSEN
ERGEBNIS: v1 geht NICHT live.
```

Alle fünf Fehlschläge haben dieselbe Ursache: der Sprung 2019→2021 (Fonds 26→6 %, Scheck 40→24 %, Werkstatt 54→13 %, Zeugnis 55→17 %) und Scheck 2019, wo nur ein Vorjahr vorliegt und das Intervall deshalb nur der Stichprobenfehler (±2,6 %) ist. Für 2025 liegen alle fünf Elemente im Intervall.

**Gegen die Quellen gelernt (alles im Extraktor korrigiert, nie im Test; Details in den Commit-Nachrichten):**

- Drs 17/9738 ist **nicht** anonymisiert, anders als der Plan annahm: die Antragsteller-Spalte enthält Vereinsnamen und mindestens eine Privatperson. Typ wird jetzt beim Extrahieren auf die elf erlaubten Werte abgebildet (281 Kommunen, 25 "unbekannt").
- 11 Vorhabentitel 2025 tragen den Vereinsnamen → gestrichen; 3 Titel entfallen ganz.
- Regel "vereinseigene Ausstattung" riss mit 41/66 = 62 %, weil 41 von 44 *Vereinsfahnen* bewilligt wurden → Muster auf `trikot|uniform` verengt (0/22).
- Register hatte für 2018/19 keine landesweite Zeile → Summenzeile "über alle" ergänzt (ohne sie sagte die Kalibrierung 2025 allein aus 2021 vorher).
- Quellfehler, nie geraten: "29.02.2019", "13.09.20218", zwei Antragsdaten in einer Zelle (letztes zählt), 5 Antragsjahre nach dem Entscheidungsjahr (kein Förderjahr), Zeile 644 "Overath" in der Elementspalte (behalten als "unbekannt").

## Viertes Urteil (26.08.2026, nach Mindestintervall in Stufe 2)

Untergrenze eingebaut: bei weniger als drei Vorjahren gilt die größte Schwankung, die irgendein Element bis dahin gezeigt hat (`basisrate.uebergreifende_schwankung`). Wirkung: Scheck 2021 ±4,4 → ±7,4 %, Preis 2021 ±2,7 → ±7,4 %. **Hürde 2 reißt trotzdem, 5 von 15** — und zwar strukturell:

- **2019:** erstes Jahr aller Elemente ist 2018; niemand hat zwei Jahre, also gibt es keine Vergleichsschwankung. Scheck 2019 bleibt bei ±2,6 % und liegt 3 Punkte daneben.
- **2021:** Fonds 26→6 %, Scheck 40→24 %, Werkstatt 54→13 %, Zeugnis 55→17 %. Der Einbruch nach der Corona-Lücke ist aus 2018/19 nicht vorhersehbar, mit keinem Intervall, das noch eine Aussage wäre.
- **2025:** alle fünf Elemente im Intervall.

Der Befund: Die Prognose funktioniert, sobald sie drei Jahre kennt. Die Hürde, wie sie in §14.2 steht ("jede Klasse im Backtest innerhalb ihres Intervalls"), verlangt aber auch Treffer in Jahren, in denen es nichts zu wissen gab.

## Fünftes Urteil (26.08.2026, unter dem präzisierten §14.2)

Felix hat entschieden: Kalibrierung und Prozentzahl nur bei mindestens drei belegten Vorjahren; Jahre mit weniger Vorgeschichte sind Lernjahre; ohne eine einzige prüfbare Vorhersage gilt Hürde 2 als nicht bestanden. Datiert in der Spec, im Code (`backtest.kalibrierung`, `prognose.beurteilen`) und getestet (113 Tests).

```
Huerde 1  falsche Absagen   vereinseigene Ausstattung 0/22 = 0.0%     bestanden
Huerde 2  Kalibrierung      5 von 5 pruefbaren Vorhersagen (2025)      bestanden
ERGEBNIS: v1 darf live gehen.
```

**Ehrlicher Vorbehalt:** Die fünf Treffer stammen aus *einem* Prüfjahr, und zwei Intervalle sind sehr weit (Werkstatt ±44 %, Zeugnis ±43 %). §14.2 erlaubt weite Intervalle, solange sie ehrlich sind — aber ein Panel, das "Chance rund 64 % ± 44 %" sagt, ist für den Heimat-Zeugnis-Antragsteller kaum eine Auskunft. Das Frühjahr 2027 (nächste Vorlage) bringt das zweite Prüfjahr.

## Teil 2 gebaut (27.08.2026)

- `doorway export` → `site/daten/panel.json` (git-versioniert): Register, Schätzungen je Element mit `darstellung` punkt/spanne/keine (Schwelle ±20 Punkte), exportierte Regeln samt Beispielen, Elementprofile aus dem Korpus, Vorschlagstabelle, Quellen, Stand mit SHA-256 des Korpus.
- `site/index.html`, `stil.css`, `app.js`, `regeln.mjs` — kein Framework, kein Build. Spiegel mit vier geführten Fragen plus Freitext; Panel in derselben Form wie die CLI; Register-Tabelle mit Filter, Herkunft, Gründen, Quelle+Seite; Fuß mit den Quellen-URLs.
- `node site/pruefung.mjs` prüft, dass die JS-Regelauswertung die Python-Beispiele reproduziert (Exit 1 sonst); `app.js` macht dieselbe Prüfung beim Laden und verweigert sonst die Ausschlussprüfung.
- Im Browser geprüft (lokaler Server): Trikots → "Chance nahe null" mit Regel; Ortsarchiv → "Chance rund 64 % (± 13)", 3 von 3 bestanden; keine Konsolenfehler.
- Dabei gefunden und behoben: Der 2025-Extraktor schnitt das erste Wort jedes Ablehnungsgrunds ab (Spaltengrenze 950 statt 920). Zählungen unverändert. 128 Tests.

## Nächster konkreter Schritt

**Pages einschalten** (28.08.: Repo `github.com/Felix3c/doorway` ist öffentlich und gepusht): Settings → Pages → Source "Deploy from a branch" → Branch `master`, Ordner `/site` → Save. Nach ein bis zwei Minuten liegt die Seite unter `https://felix3c.github.io/doorway/`. Dann diese URL hier und in `REIHENFOLGE.txt` eintragen, und im Fuß der Seite (`site/index.html`) den Hinweis auf das Repo ergänzen.

## Wartet auf Felix

- ~~Hürde 2 — präzisieren oder Daten holen?~~ Entschieden 26.08.: präzisieren (siehe fünftes Urteil). Die IFG-Anfrage 2020/2022 bleibt als spätere Option offen — sie würde zwei weitere Prüfjahre bringen.
- ~~Weite Intervalle im Panel~~ — entschieden 27.08.: Spanne statt Punktwert ab ±20 Punkten (Spec Teil 2, §2).
- **Die Seite ansehen.** Abschnitte 2–4 des Teil-2-Designs habe ich ohne dich entschieden (Fragen, Wortlaut, Schwelle). Was dir nicht gefällt, ist ein Abend Arbeit, kein Umbau.
- **Remote anlegen:** privates GitHub-Repo (entschieden 26.08.). Historie seit 26.08. frei von Klarnamen (0 Treffer über alle Commits). Push ist freigegeben — braucht nur dein GitHub-Login.

## Entschieden am 2026-08-26

- **Git-Historie bereinigt.** Das Golden File `golden/drs-17-9738.json` trug in den Commits vom 25.08. den Klarnamen einer Privatperson (Antragsteller-Spalte der Drs 17/9738). Alle Commits per `filter-branch` umgeschrieben, Sicherungs-Refs gelöscht, `gc --prune=now`; `git log -p --all` findet den Namen nicht mehr. Hashes ab dem Extraktor-Commit haben sich geändert (alt `2647a73`, neu `1344894`).
- ~~Repo wird privat, Korpus bleibt versioniert.~~ Geändert 28.08.: öffentlich wie belegt, damit Pages kostenlos ist (Spec §13.1). `daten/korpus.jsonl` ist intern (§13.1); ein privates Repo veröffentlicht nichts, und der Korpus bleibt als Diff nachvollziehbar. Öffentlich wird später nur das Register.
- **Stufe 2: Mindestintervall zuerst,** IFG-Anfrage 2020/2022 erst, wenn Hürde 2 danach immer noch reißt.

## Blocker

Keiner. Alles Weitere ist Entscheidung, nicht Hindernis.

## Wie eine neue Session hier einsteigt

1. Spec lesen (Präambel zuerst), dann diesen Wegweiser.
2. `python -m pytest -q` — muss 108 grün liefern. `PYTHONPATH=src python -m doorway.cli kill-kriterium` zeigt das Urteil.
3. Nicht mit Teil 2 anfangen. Der Plan sagt: Reißt eine Hürde, wird Stufe 1/2 überarbeitet, nicht die Oberfläche gebaut.
