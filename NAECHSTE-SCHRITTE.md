# Doorway — Nächste Schritte

**Stand:** 08.09.2026, abends (PR #1 in festgehalten gemerged, Probelauf-PR erledigt; Plan 2 läuft, Task 1 und 2 fertig)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`; **Teil 3: `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`**
**Phase:** Teil 1 und Teil 2 veröffentlicht. Teil 3: Plan 1 (festgehalten) abgeschlossen und gemerged. Plan 2 (Doorway-Seite `hinterlegen.html`) in Arbeit, Task 3 von 7.

---

## Leitsatz

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Übergeordnete These: `~/THESE.md`. Prüffrage für jedes Feature: *nachprüfbarer oder nur bequemer?*

## Zielbild (01.09.2026, aus ~/GUARD.md Ebene 3 und FORMAT.md §8.4)

**Doorway ist der Zugang zu allem, was Bindung belohnt.** Wer etwas will, das andere vergeben
— Geld, Genehmigung, Legitimität — hinterlegt vorab, datiert und öffentlich, was er erwartet.
Doorway baut die Tür für diese Hinterlegung und die Werkzeuge für die Seite, die vergibt.
Die Stadt ist das Produkt, nicht der Kunde. Kundenliste und Regel `herkunft: hinterlegt`:
Commit ab2ad9a bzw. FORMAT.md §8.4.

## Wo wir stehen

- **Live:** https://felix3c.github.io/doorway/ — Spiegel, Panel, Nein-Register, Quellen.
  Von Felix abgenommen 01.09. An der veröffentlichten Seite wurde seitdem nichts geändert.
- **Plan 1 (festgehalten) ist fertig und gemerged.** PR #1 am 08.09. gemerged, Merge-Commit
  `f848d8089500edaf82bb82f290ef9d7061a62ddd` auf `master`. Der Merge nahm neun Commits mit,
  darunter einen aus einem anderen Tab (`cec32e9`, Herkunft-Spalte in der Wettenliste).
  Deploy grün. Live geprüft: https://felix3c.github.io/festgehalten/buecher.json hat sechs
  Einträge, alle mit `"zweig": "master"`, genau einer mit `"sammelbuch": true`
  (Ordner `hinterlegt`, `einreichung: hinterlegt@belegbar.eu`).
- **Probelauf der PR-Prüfung erledigt** (Plan 1, Task 5, Schritt 3). PR #2 mit absichtlich
  kaputter Datei: Check `Pull Request prüfen` rot, Meldung `hinterlegt/kaputt.md: institution
  — Pflichtfeld fehlt`, insgesamt „13 Fehler, nichts geschrieben". PR geschlossen, Zweig
  `probelauf-ci` gelöscht. Die GitHub-Mail über den fehlgeschlagenen Lauf ist erwartet.
- **Plan 2 läuft** auf dem Zweig **`hinterlegen`** in `~/doorway` (noch nicht gepusht, kein
  Upstream). Commits über `master` hinaus: `65c050e` (`.superpowers/` ignorieren),
  `8922b6f` + `f23a449` (Task 1), `013e648` (Task 2). Arbeitsverzeichnis sauber.
  - Task 1 (Buchliste `site/daten/buecher.json` Stand 08.09., Modul `site/hinterlegen.mjs`
    mit `kurzBilden`/`isoDatum`/`idBilden`, Node-Tests in `site/hinterlegen.pruefung.mjs`,
    eingehängt in `site/pruefung.mjs`): fertig, Review nach einer Fix-Runde sauber.
  - Task 2 (`uebersetzen`, `pruefeEingaben`, `datumPlus`, `yamlText`, `GRENZEN`): fertig,
    Review ohne Beanstandung.
  - **Task 3 (PR-, Mail- und Status-Adressen) war beim Umsetzer, als die Sitzung endete.
    Es liegt kein Commit und kein Bericht vor — er gilt als nicht begonnen.**
- **Gemessen in dieser Sitzung:** `~/doorway`: `python -m pytest -q` 128 grün,
  `node site/pruefung.mjs` grün, `node site/hinterlegen.pruefung.mjs` „ok: 8 Fälle".
  `~/wettbuch` (master nach dem Merge): 83 grün.
- **Ledger mit Vorab-Check, allen Rulings und den vertagten Kleinigkeiten:**
  `.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/progress.md` (gitignored).
  Dort liegen auch die fertigen Aufgabenzettel `task-2..5-brief.md`.
- **Rulings dieser Sitzung** (alle im Ledger begründet): A `kurz` bleibt bei höchstens 20
  Zeichen, Testerwartung `buergerverein-strass`; B Kombinationszeichen als `\u`-Escape;
  C Statuslink zeigt auf `<ordner>/wette/<id>.html` (Schema aus `seiten.py`); K die Messung
  von `PR_URL_MAX` in Task 6 macht die Session im Browser; L Plan 2 endet mit einem PR gegen
  `master`, Pages-Abnahme und Probelauf danach.
- **Vertagt für den Schlussreview:** kein Test für `yamlText` mit `"` oder `\` im Text;
  `istZahl` lehnt deutsches Komma („0,10") ab; zwei ungetestete Randfälle
  (`bedingungFrist` ohne `bedingung`, ungültiger `typ`).
- Probe-Dateien `research/hinterlegung-probe/` bleiben privat und gitignored.

## Nächster konkreter Schritt

**Task 3 von Plan 2 starten** (PR-URL, Längengrenze, Mail-Link). Vorher `git log --oneline
013e648..HEAD` prüfen — ist dort nichts, ist Task 3 unangetastet. Dann mit
superpowers:subagent-driven-development weiter: Aufgabenzettel
`.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/task-3-brief.md`, BASE `013e648`,
Ziel `ok: 12 Fälle hinterlegen`. Anschließend Task 4 bis 7 laut Plan
`docs/superpowers/plans/2026-09-05-doorway-teil-3-hinterlegung.md`.

## Wartet auf Felix

- **Alias `hinterlegt@belegbar.eu` bei ImprovMX anlegen.** Die Adresse steht im Sammelbuch;
  ohne Alias laufen Mails ins Leere.
- **Abnahme am Ende von Plan 2:** erfundener Fall auf `hinterlegen.html` durchklicken bis zum
  Probelauf-PR im Sammelbuch, PR schließen. Danach Merge des Doorway-PRs nach `master`.

## Blocker

Keine.

## Wie eine neue Session hier einsteigt

1. Diesen Stand lesen, dann den Ledger
   `.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/progress.md` (Vorab-Check + Rulings).
2. `git branch --show-current` muss `hinterlegen` sagen; sonst `git checkout hinterlegen`.
3. `node site/pruefung.mjs` und `python -m pytest -q` als Ausgangslage.
4. Nichts an der Seite ändern, was nicht in der Spec steht; Abweichungen in die Spec schreiben.
5. `gh` ist auf diesem Rechner nicht installiert. GitHub lesend über die API (curl), schreibend
   über `git push` oder die Chrome-Werkzeuge.
