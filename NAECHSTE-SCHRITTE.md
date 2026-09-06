# Doorway — Nächste Schritte

**Stand:** 06.09.2026, nachmittags (Plan 1 umgesetzt: PR #1 in festgehalten offen, Check grün, noch nicht gemerged; Plan 2 nicht begonnen)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`; **Teil 3: `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`**
**Phase:** Teil 1 und Teil 2 abgeschlossen und veröffentlicht. Teil 3 (Hinterlegungs-Pfad): Plan 1 (festgehalten) fertig und im PR, Plan 2 (Doorway-Seite) wartet auf den Merge.

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
  Von Felix abgenommen 01.09. An der Seite wurde heute nichts geändert.
- **Plan 1 ist umgesetzt** (`~/wettbuch`, Branch `hinterlegt-sammelbuch`,
  PR https://github.com/Felix3c/festgehalten/pull/1, 8 Commits, Check `pruefen` grün,
  mergebar). Inhalt: Generator baut leere Bücher (nur Test, kein Fix nötig); BUCH.md kennt
  `institution`, `einreichung`, `sammelbuch`; `alle` schreibt `buecher.json` (zehn Felder)
  mit `--repo`; Sammelbuch `buecher/hinterlegt/` mit `einreichung: hinterlegt@belegbar.eu`;
  `institution: Stadt …` in den fünf Stadtbüchern; `pruefen.yml` bei jedem PR, nur Leserecht.
  80 Tests grün (vorher 69), lokaler Build: 6 Bücher, genau `hinterlegt` als Sammelbuch.
- **Im PR liegt auch ein fremder Commit** (2bd75f4, `recherche/nachweis-modell/`, aus einem
  anderen Tab, 06.09. 15:39). Gehört nicht zu Plan 1, stört den Merge nicht.
- **Entscheidungen heute (Felix):** Einreichungsadresse `hinterlegt@belegbar.eu`;
  Festpreis-Satz bleibt „Halter dieses Buches" (in Spec §5.1 vermerkt, Commit d5d4e21).
- **Entscheidungen heute (Session, im Ledger belegt):** `pruefen.yml` läuft ohne `--pruefen`
  (Spec-Wortlaut); `_zweig()` liest Git im Bücher-Ordner, Rückfall `origin/HEAD`, „main" nur
  zuletzt; `pages.yml` bekommt `--repo` (Plan-Selbstprüfung, abweichend von Spec §5.3).
  Geparkt: im PR-Workflow fällt `zweig` auf „main", weil der Checkout losgelöst ist; das
  PR-`site/` wird nie ausgeliefert. Nachweis nach dem Deploy: `buecher.json` zeigt
  `"zweig": "master"`.
- **Ledger mit allen Rulings und sechs vertagten Kleinigkeiten:**
  `~/wettbuch/.superpowers/sdd/2026-09-05-hinterlegt-sammelbuch-und-buchliste/progress.md`
  (gitignored; bleibt bis zum Merge liegen).
- **Für Plan 2 vorgemerkt:** Das Sammelbuch hat `institution: null`; das Formular muss es über
  `sammelbuch: true` als Ziel wählen, nicht über `institution`. `buecher.json` nach `ordner`
  keyen, nicht nach Index.
- Probe-Dateien `research/hinterlegung-probe/` bleiben privat und gitignored.

## Nächster konkreter Schritt

**PR #1 in festgehalten mergen** (Felix, oder Freigabe an die Session), dann prüfen:
https://felix3c.github.io/festgehalten/buecher.json hat 6 Einträge und `"zweig": "master"`.
Danach in dieser Reihenfolge: Probelauf-PR mit kaputter Datei (Plan 1, Task 5 Schritt 3),
Merge-SHA als `FESTGEHALTEN_SHA` in `docs/superpowers/plans/2026-09-05-doorway-teil-3-hinterlegung.md`
eintragen, Plan 2 mit superpowers:subagent-driven-development starten.

## Wartet auf Felix

- **Merge von PR #1** oder das Wort, dass die Session mergen darf.
- **Alias `hinterlegt@belegbar.eu` bei ImprovMX anlegen.** Die Adresse steht schon im
  Sammelbuch; ohne Alias laufen Mails ins Leere.
- **Abnahme am Ende von Plan 2:** erfundener Fall durchklicken bis zum Probelauf-PR im
  Sammelbuch, PR schließen.

## Blocker

Keine.

## Wie eine neue Session hier einsteigt

1. Teil-3-Spec lesen, dann Stand oben; Ledger in `~/wettbuch/.superpowers/sdd/…/progress.md`.
2. `~/wettbuch`: `python -m pytest -q` (80 grün); `~/doorway`: `python -m pytest -q` (128 grün,
   zuletzt 27.08.) und `node site/pruefung.mjs`.
3. Nichts an der Seite ändern, was nicht in der Spec steht; Abweichungen in die Spec schreiben.
