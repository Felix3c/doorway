# Doorway — Nächste Schritte

**Stand:** 2026-08-29 (Seite ist live unter https://felix3c.github.io/doorway/ ; Repo öffentlich; ai-firma gelöscht)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`
**Phase:** Teil 1 und Teil 2 abgeschlossen und veröffentlicht. Vor Teil 3 steht keine Programmierarbeit, sondern Felix' Urteil über die Seite und die Frage, was als Nächstes den Leitsatz am stärksten voranbringt.

---

## Leitsatz

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Übergeordnete These: `~/THESE.md`. Prüffrage für jedes Feature: *nachprüfbarer oder nur bequemer?*

## Wo wir stehen

- **Live:** https://felix3c.github.io/doorway/ — Spiegel (vier Fragen + Freitext), Panel, Nein-Register, Quellen. Ausgeliefert per Actions-Workflow `.github/workflows/pages.yml` aus `site/`; jeder Push auf `master` veröffentlicht neu.
- **Repo:** https://github.com/Felix3c/doorway, öffentlich (Entscheidung 28.08., Spec §13.1), 40 Commits, Arbeitsbaum sauber, alles gepusht. Historie frei von Klarnamen (bereinigt 26.08.). `research/` (401 MB Rohdaten) ist nicht im Repo.
- **Werkzeug:** `doorway laden | ernten | prognose | kill-kriterium | export`. 128 Tests grün (zuletzt 27.08.), `node site/pruefung.mjs` grün.
- **Kill-Kriterium (§14.2, präzisiert 26.08.):** beide Hürden bestanden — Hürde 1: 0/22 falsche Absagen; Hürde 2: 5 von 5 prüfbaren Vorhersagen (2025) im Intervall. Vorbehalt: ein Prüfjahr; Werkstatt/Zeugnis mit Intervall ±43 % (Seite zeigt dort Spanne statt Punktwert).
- **Design:** "amtlich, aber schön" (28.08.), nur `site/stil.css`; Tokens am Dateianfang.
- **Nebenbei am 28.08.:** `~/ai-firma` (SiteWerk) auf Felix' Wunsch komplett in den Papierkorb — kein Projekt mehr.

## Nächster konkreter Schritt

**Felix schaut sich die Live-Seite an und sagt, was falsch, unklar oder hässlich ist.** Alles, was dann kommt, ist Feinarbeit an `site/` oder eine neue Designentscheidung — kein Umbau. Erst danach die Frage nach Teil 3 stellen (Kandidaten laut Teil-2-Spec §5: IFG-Anfrage 2020/2022 für zwei weitere Prüfjahre; Bezirksregierung im Spiegel; Extraktoren für `vorl-17-2268` und `vorl-18-2806` für die Gründeverteilung; Nutzermeldungen mit Scoring Rule).

## Wartet auf Felix

- Urteil über die Live-Seite (Wortlaut der Fragen, ±20-Schwelle, Farben — alles Abschnitt 2–4 der Teil-2-Spec, von Claude allein entschieden).
- Was Teil 3 wird (siehe oben). Empfehlung: IFG-Anfrage zuerst, weil sie am längsten dauert und nichts blockiert.

## Blocker

Keiner.

## Wie eine neue Session hier einsteigt

1. Beide Specs lesen, Präambel zuerst.
2. `python -m pytest -q` (128 grün) und `PYTHONPATH=src python -m doorway.cli kill-kriterium` (beide Hürden bestanden).
3. Lokal ansehen: `cd site && python -m http.server 8765` → http://127.0.0.1:8765/ — Hintergrundprozesse aus der Session werden beendet, im Zweifel per PowerShell `Start-Process` starten.
4. Nichts an Teil 3 anfangen, bevor Felix die Seite abgenommen hat.
