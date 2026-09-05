# Doorway — Nächste Schritte

**Stand:** 05.09.2026, nachts (Teil 3 entschieden, Spec und zwei Pläne geschrieben; noch keine Zeile Code für Teil 3)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`; **Teil 3: `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`**
**Phase:** Teil 1 und Teil 2 abgeschlossen und veröffentlicht. Teil 3 (Hinterlegungs-Pfad) ist von Felix bestätigt (02.09.), Design abgenommen (05.09.), Umsetzung noch nicht begonnen.

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
  Von Felix abgenommen 01.09.
- **Repo:** https://github.com/Felix3c/doorway, öffentlich. 128 Tests grün (zuletzt 27.08.),
  Kill-Kriterium bestanden.
- **Teil 3 ist entschieden: der Hinterlegungs-Pfad.** Eine Seite `hinterlegen.html`, die aus
  sieben Antworten eine Datei im festgehalten-Format erzeugt und sie als vorausgefüllten
  Pull Request, Download oder Mail an ein Buch im Repo festgehalten übergibt. Kein Server,
  keine Speicherung, Doorway führt kein Buch; der Merge-Commit ist die Hinterlegung.
- **Die sechs Befunde der Probe (01.09.) sind beantwortet** (Spec §1): Quelle immer gefüllt;
  Bedingung mit Frist im Vermerk, Verfall = Prüfdatum + 6 Monate; Formular erzwingt den
  öffentlichen Ort des Nachweises; Zielbuch = Buch der Institution, sonst Sammelbuch
  „Hinterlegt"; Halter hinterlegt nicht im eigenen Buch; Festpreis 0 Euro bis zwei
  Registereinträge vorliegen. Keine Formatänderung.
- **Zwei Pläne, in dieser Reihenfolge auszuführen:**
  1. `~/wettbuch/docs/superpowers/plans/2026-09-05-hinterlegt-sammelbuch-und-buchliste.md`
     (festgehalten: Sammelbuch, `buecher.json`, PR-Prüf-Workflow, Generator baut leeres Buch)
  2. `docs/superpowers/plans/2026-09-05-doorway-teil-3-hinterlegung.md`
     (Doorway: Modul, Seite, Entwurf, Status, Rundlauf-Test, Messung, Abnahme)
- Probe-Dateien `research/hinterlegung-probe/` bleiben privat und gitignored.
  `lind-2026-001` ist Probe, nicht Teil 3.

## Nächster konkreter Schritt

**Plan 1 ausführen** (im Repo `~/wettbuch`, superpowers:subagent-driven-development oder
executing-plans), dann Plan 2. Beide Pläne sind mit Tests und Commit-Schritten geschrieben.

## Wartet auf Felix

- **Mailadresse für `einreichung`** im Sammelbuch (Plan 1, Task 4). Ohne sie fehlt in Doorway
  nur der Mail-Knopf; PR und Download gehen trotzdem.
- **Abnahme am Ende von Plan 2:** erfundener Fall durchklicken bis zum Probelauf-PR im
  Sammelbuch, PR schließen.

## Blocker

Keine.

## Wie eine neue Session hier einsteigt

1. Teil-3-Spec lesen, dann den Plan, der dran ist (Stand oben).
2. `python -m pytest -q` (128 grün) und `node site/pruefung.mjs` (grün).
3. Nichts an der Seite ändern, was nicht in der Spec steht; Abweichungen in die Spec schreiben.
