# Doorway — Design Teil 2: Die Seite

**Datum:** 2026-08-27
**Status:** Abschnitt 1 mit Felix abgestimmt (26./27.08.); Abschnitte 2–4 von Claude entschieden und hier festgehalten, damit Felix sie prüfen kann. Umsetzung direkt aus dieser Spec, kein eigener Plan (Felix: "bau so weit wie du kannst").
**Voraussetzung:** Teil 1 abgeschlossen, Kill-Kriterium unter §14.2 (präzisiert 26.08.) bestanden.
**Leitsatz:** siehe Präambel der Design-Spec vom 24.08. — *nachprüfbarer oder nur bequemer?*

---

## 0. Entscheidungen von Felix (26./27.08.2026)

1. Eine Seite: Register und Prognose zusammen.
2. Der Spiegel arbeitet mit geführten Fragen, ohne Freitextdeutung durch ein Modell.
3. Weite Intervalle: Spanne statt Punktwert ab einer Schwelle.
4. Ansatz A: statische Seite, Python rechnet vor, der Browser zeigt an. Die Ausschlussregeln werden **exportiert**, nicht abgeschrieben — eine Quelle (`regeln.py`).

## 1. Datenfluss und Export

```
Quellen → Korpus → Register → doorway export → site/daten/panel.json → Browser
```

`doorway export` (`src/doorway/export.py`) schreibt **eine** git-versionierte Datei mit fünf Blöcken:

| Block | Inhalt | Quelle im Code |
|---|---|---|
| `register` | alle Registerzeilen, unverändert | `cli._register_bauen()` |
| `schaetzungen` | je Element (landesweit): `quote`, `halbe_breite`, `untergrenze`, `obergrenze`, `grundlage_n`, `jahre`, `belegte_jahre`, `darstellung`, `gruende`, `beleg` | `prognose.beurteilen()` |
| `regeln` | je Regel `name`, `beleg`, `hinweis`, und entweder `muster` + `flags` oder `bedingung` | `regeln.REGELN` |
| `beispiele` | je Regel Texte mit erwartetem Ergebnis | fest in `export.py`, identisch mit den Fällen in `tests/test_regeln.py` |
| `elemente` | je Element: Zahl bewilligter Anträge mit Betrag, Median-Betrag, häufigste Antragstellertypen | Korpus |
| `stand` | Exportdatum, Korpus-Commit, Quellen-Lock | `git rev-parse`, `daten/quellen.lock.json` |

**`darstellung`** entscheidet Python: `"punkt"` wenn `halbe_breite <= 0.20`, sonst `"spanne"`. Unter drei belegten Jahren: `"keine"` (§14.2).

**Leitplanken als Tests (`tests/test_export.py`):**
- Kein Feld außerhalb der erlaubten Liste; insbesondere nie `kommune`, `vorhabentext`, `antragstellertyp` einer Einzelentscheidung.
- Jedes Muster liegt in der Schnittmenge von Python- und JavaScript-Regex: verboten sind Lookbehind `(?<`, benannte Gruppen `(?P<`, Inline-Flags `(?i)`, Unicode-Klassen `\p{`, possessive Quantoren, atomare Gruppen.
- Jedes Beispiel wird beim Export gegen `regeln.pruefen()` verifiziert; stimmt es nicht, bricht der Export ab.
- `stand.korpus_commit` ist der Commit, in dem `daten/korpus.jsonl` zuletzt geändert wurde.

## 2. Die Seite

`site/` — drei Dateien, kein Framework, kein Build: `index.html`, `app.js`, `stil.css`. Läuft von `file://` und von GitHub Pages. Lädt `daten/panel.json` per `fetch`; schlägt das fehl, zeigt die Seite genau das und nichts Erfundenes.

Aufbau von oben nach unten:

1. **Kopf** — Name, ein Satz ("Doorway sagt vor der Tür, wie die Chancen stehen — belegt aus den Berichten des Landes"), Stand-Zeile aus `stand`.
2. **Spiegel** — die Fragen aus Abschnitt 3.
3. **Panel** — erscheint, sobald der Spiegel beantwortet ist. Gleiche Anordnung wie in der CLI (§12.4): Urteilszeile, Ausschlussprüfung immer sichtbar, Gründeverteilung, Beleg.
4. **Register** — Tabelle aller Zeilen mit Filter nach Element und Jahr; Spalten: Jahr, Element, Stelle, Anträge, bewilligt, abgelehnt, Quote, Herkunft, Quelle/Seite. Konfliktzeilen zeigen beide Werte. Die drei häufigsten Gründe je Zeile ausklappbar.
5. **Fuß** — was Doorway nicht tut (§4 der Design-Spec) und der Weg zur Quelle (Landtags-Archiv-URL je Dokument).

**Darstellung des Urteils** (aus `darstellung`):
- `punkt`: "Chance rund 64 % (± 16)" plus "Basis: 926 Anträge, Förderjahre 2021–2025".
- `spanne`: "Chance irgendwo zwischen 25 und 100 %. Die Quote dieses Elements schwankt stark von Jahr zu Jahr." — kein Punktwert.
- `keine`: "Eine Zahl gibt es erst ab drei belegten Förderjahren. Bisher belegt: 2."
- Regel getroffen: "Chance nahe null" mit Regelname, Hinweis, Beleg — kein Prozent.

## 3. Der Spiegel

Vier Fragen in Alltagssprache, jede mit fester Auswahl, plus ein Freitextfeld. Keine Frage verwendet die Wörter "Förderelement", "Antragstellertyp" oder "Bewilligungsstelle".

1. **"Wer stellt den Antrag?"** → Antragstellertyp. Auswahl: ein eingetragener Verein · eine Gruppe ohne Verein (Initiative, Nachbarschaft) · eine Stiftung · eine Kirchengemeinde · eine Stadt, Gemeinde oder ein Kreis · ich selbst als Privatperson · ein Unternehmen.
2. **"Wie viel Geld braucht ihr ungefähr?"** → Betragsklasse: bis 2.000 € · bis 5.000 € · bis 50.000 € · mehr.
3. **"Das passt zu …"** → Elementvorschlag aus 1 und 2, mit Beleg: "Heimat-Scheck: in den Berichten 2.405 bewilligte Anträge, fast immer 2.000 €, meist Vereine." Der Vorschlag ist eine Vorauswahl, keine Entscheidung — alle fünf Elemente bleiben wählbar, jedes mit seiner Belegzeile aus `elemente`.
4. **"Habt ihr in diesem Jahr schon einen Heimat-Scheck beantragt?"** → Mehrfachantrag (nur beim Heimat-Scheck gestellt).
5. **"Was habt ihr vor?"** (Freitext, optional) → nur für die Ausschlussregeln. Der Text verlässt den Browser nicht; die Seite sagt das neben dem Feld.

Zuordnung Betragsklasse × Typ → Vorschlag, belegt aus dem Korpus (Median-Beträge, Typverteilung): bis 2.000 € → Heimat-Scheck; bis 5.000 € und Kommune → Heimat-Preis, sonst Heimat-Scheck; bis 50.000 € und Kommune → Heimat-Fonds, sonst Heimat-Werkstatt; mehr → Heimat-Zeugnis. Die Zuordnung liegt in `export.py` und wird als `vorschlag`-Tabelle mit exportiert — der Browser rechnet sie nicht selbst.

Bezirksregierung wird **nicht** abgefragt: Je Stelle liegen höchstens drei Jahre vor (2018, 2019, 2024), und 2024 ohne Element — keine Kombination erreicht drei belegte Jahre für ein Element. Sobald das anders ist, kommt die Frage dazu.

## 4. Tests

- **Python** (`tests/test_export.py`): Leitplanken aus Abschnitt 1, Vorschlagstabelle, `darstellung`-Schwelle, Beispiele verifiziert.
- **JavaScript** (`site/pruefung.mjs`, läuft mit `node site/pruefung.mjs`): lädt `panel.json`, kompiliert jedes Muster mit `new RegExp`, wertet alle `beispiele` aus und vergleicht mit dem erwarteten Ergebnis; prüft die Vorschlagstabelle gegen die Fragen. Exit 1 bei Abweichung. `app.js` führt dieselbe Prüfung beim Laden aus; schlägt sie fehl, zeigt die Seite keine Ausschlussprüfung, sondern den Hinweis "Regelprüfung nicht verfügbar — Regeln und Seite passen nicht zusammen".
- **Sichtprüfung:** die Seite wird nach dem Bau im Browser geöffnet; beide Fälle (Trikots / Ortsarchiv) werden durchgeklickt.

## 5. Nicht in Teil 2

Nutzermeldungen mit Scoring Rule (§8), Bezirksregierung im Spiegel, IFG-Lückenschließung 2020/2022, Extraktoren für `vorl-17-2268` und `vorl-18-2806`, jede Form von Konto oder Speicherung von Eingaben.
